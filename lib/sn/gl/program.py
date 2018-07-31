import logging
import re
import string
from ctypes import *
from typing import Dict
import numpy as np

import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *

from   .globject import GLObject
from   .types import *
import sn.sn_logging as sn_logging

OpenGL.FORWARD_COMPATIBLE_ONLY = True
OpenGL.USE_ACCELERATE = False
# OpenGL.ERROR_CHECKING = False


# logging.getLogger().setLevel(logging.DEBUG)

class ShaderProgramSyntaxError(Exception):
    def __init__(self, message):
        self.message = message


class ShaderProgramLinkingError(Exception):
    def __init__(self, message):
        self.message = message


class SIZEI(UINT):
    pass


class ProgramCore:
    shader_types = dict(
            vs=GL_VERTEX_SHADER, vert=GL_VERTEX_SHADER, vertex=GL_VERTEX_SHADER,
            tcs=GL_TESS_CONTROL_SHADER, tesscontrol=GL_TESS_CONTROL_SHADER, tessellationcontrol=GL_TESS_CONTROL_SHADER,
            tes=GL_TESS_EVALUATION_SHADER, tesseval=GL_TESS_EVALUATION_SHADER, tessevaluation=GL_TESS_EVALUATION_SHADER,
            tessellationevaluation=GL_TESS_EVALUATION_SHADER,
            gs=GL_GEOMETRY_SHADER, geometry=GL_GEOMETRY_SHADER,
            fs=GL_FRAGMENT_SHADER, fragment=GL_FRAGMENT_SHADER,
            cs=GL_COMPUTE_SHADER, compute=GL_COMPUTE_SHADER)
    '''@type: Dict[str, int]'''

    def __init__(self, path):
        logging.debug('__init__@ProgramCore')
        self._program_path = path
        self._program = None
        self._shader_set = []
        # self._known_invalid = set()
        # self._samplers = {}
        super().__init__()
        self._validated = self._linked = False

    def create(self):
        logging.debug('create@ProgramCore')
        self._program = glCreateProgram()
        self.load(self._program_path)
        self.compile_link()
        self.validate()
        logging.debug('create@ProgramCore: _program = {}'.format(self._program))

    def load(self, path, substitute=False):
        logging.debug('load@ProgramCore')
        shader_types, shader_set = self.shader_types, []
        kind, code = None, []
        with open(path, 'r') as f:
            for line in f:
                k = ''.join(line.strip('#\n').split(' ')).lower().replace('shader', '')
                if k in shader_types.keys():
                    if kind is not None:
                        shader_set.append((kind, ''.join(code)))
                    kind, code = shader_types[k], []
                else:
                    code.append(line)
        if kind is not None:
            code = ''.join(code)
            if substitute:
                code = string.Template(code).substitute(substitute)
            shader_set.append((kind, code))
        self._shader_set = shader_set

    def compile_link(self):
        logging.debug('compile_link@ProgramCore')
        self._linked = False
        p = self._program
        shader_list = []
        for t, code in self._shader_set:
            logging.info('Compiling a shader: {0}'.format(t))
            shader = glCreateShader(t)
            shader_list.append(shader)
            glShaderSource(shader, code)
            glCompileShader(shader)
            if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                errors = str(glGetShaderInfoLog(shader), 'utf-8')
                raise ShaderProgramSyntaxError(Program._get_error(code, errors, 4))
            glAttachShader(p, shader)

        logging.info('Linking a program({})'.format(p))
        glLinkProgram(p)
        if glGetProgramiv(p, GL_LINK_STATUS) != GL_TRUE:
            errors = glGetProgramInfoLog(p)
            if len(errors) > 0:
                raise ShaderProgramLinkingError(errors.decode('utf-8'))

        self._linked = True
        for shader in shader_list:
            glDetachShader(p, shader)
            glDeleteShader(shader)

    def validate(self):
        logging.debug('validate@ProgramCore')
        self._validated = True
        glValidateProgram(self._program)
        if glGetProgramiv(self._program, GL_VALIDATE_STATUS) != GL_TRUE:
            raise RuntimeError('Program validation error:\n{0}'.format(
                glGetProgramInfoLog(self._program).decode('utf-8')))

    @staticmethod
    def _get_error(code, errors, indentation=0) -> str:
        results = []
        lines = None
        if code is not None:
            lines = [line.strip() for line in code.split('\n')]

        for error in errors.split('\n'):
            # error = error.split()
            if not error:
                continue

            lineno, error = Program._parse_error(error)
            if None in (lineno, lines):
                results.append(str(error))
            else:
                results.append('on line {0}: {1}'.format(lineno, error))
                if 0 < lineno < len(lines):
                    results.append('  {0}'.format(lines[lineno - 1]))
        results = [' ' * indentation + r for r in results]
        return '\n'.join(results)

    @staticmethod
    def _parse_error(error) -> (int, str):
        error = str(error)
        # Nvidia
        # 0(7): error C1008: undefined variable "MV"
        m = re.match(r'(\d+)\((\d+)\)\s*:\s(.*)', error)
        if m:
            return int(m.group(2)), m.group(3)
        # ATI / Intel
        # ERROR: 0:131: '{' : syntax error parse error
        m = re.match(r'ERROR:\s(\d+):(\d+):\s(.*)', error)
        if m:
            return int(m.group(2)), m.group(3)
        # Nouveau
        # 0:28(16): error: syntax error, unexpected ')', expecting '('
        m = re.match(r'(\d+):(\d+)\((\d+)\):\s(.*)', error)
        if m:
            return int(m.group(2)), m.group(4)
        # Other ...
        return None, error

    def delete(self):
        logging.debug('delete@ProgramCore')
        if self._program is not None and bool(glDeleteProgram):
            p = self._program
            self._program = None
            glDeleteProgram(p)

    def use(self):
        logging.debug('use@ProgramCore({})'.format(self._program))
        glUseProgram(self._program)


class _Program(GLObject):
    def examine(self, *args):
        pass


from .analyse import *

class Program(ProgramCore,
              AnalyseVertexAttributes, AnalyseUniforms, AnalyseShaderStorageBlock, AnalyseSubroutines,
              _Program):
    def __init__(self, path):
        logging.debug('__init__@Program')
        super().__init__(path)
        logging.debug('__init__@Program done!')

    def create(self, *args):
        logging.debug('create@Program')
        super().create()
        super().examine()
