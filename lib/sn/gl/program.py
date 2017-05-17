import logging
import re
from collections import defaultdict
from ctypes import *
from typing import Dict
import numpy as np

import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *

from .globject import GLObject
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


class ProgramResource(Structure):
    @staticmethod
    def specs(specs):
        return [(name, c_uint) for name, _ in specs], [feature for _, feature in specs]

    def bufinfo(self):
        return len(self._features_), self._features_, sizeof(self), glres.pointer(), self.pointer()

    def pointer(self):
        return pointer(self)

    def query(self, p, interface, target):
        glGetProgramResourceiv(p, interface, target,
                               len(self._features_), self._features_,
                               sizeof(self), glres.pointer(), pointer(self))


class UINT(ProgramResource):
    _fields_, _features_ = ProgramResource.specs([('val', c_uint)])


glres = UINT()


class SIZEI(UINT):
    pass


name_buf = bytes(256)


def resource_name(p, interface, target, length):
    glGetProgramResourceName(p, interface, target, len(name_buf), glres.pointer(), name_buf)
    return name_buf[:length - 1].decode('utf-8')


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

    def load(self, path):
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
            shader_set.append((kind, ''.join(code)))
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


class Analyse:
    def examine(self):
        pass


class ProgramVertexAttributes(Analyse):
    vertex_attribute_handler = dict([
        (GL_FLOAT_VEC2, glVertexAttrib2f),
        (GL_FLOAT_VEC3, glVertexAttrib3f),
        (GL_FLOAT_VEC4, glVertexAttrib4f)])

    def __init__(self, *args):
        logging.debug('__init__@ProgramVertexAttributes')
        self.a = dict()
        super().__init__()

    def examine(self):
        p = self._program
        logging.debug('examine@ProgramVertexAttributes({})'.format(p))

        n = np.zeros(1, dtype=np.int32)
        glGetProgramInterfaceiv(p, GL_PROGRAM_INPUT, GL_ACTIVE_RESOURCES, n)
        if sn_logging.log_on_shader_variables():
            logging.info('#vertex attributes = {0}'.format(n[0]))

        types = list(self.vertex_attribute_handler.keys())
        properties = np.array([GL_NAME_LENGTH, GL_TYPE, GL_LOCATION])

        bbuf = bytes(256)
        info = np.zeros(3, dtype=np.int32)
        lengths = np.zeros(1, dtype=np.int32)
        a = self.a
        for attr in range(n[0]):
            glGetProgramResourceiv(p, GL_PROGRAM_INPUT, attr,
                                   3, properties, 3, lengths,
                                   info)
            logging.info('length = {0}, info = {1}'.format(lengths, info))
            glGetProgramResourceName(p, GL_PROGRAM_INPUT, attr, len(bbuf), lengths, bbuf)
            location = info[2]
            if location == -1:
                continue
            name = bbuf[:lengths[0]].decode('utf-8')
            typestr = types[types.index(info[1])].__repr__()
            if sn_logging.log_on_shader_variables():
                logging.info('attribute {0}:{1}@{2}'.format(name, typestr, location))
            f = self.vertex_attribute_handler[info[1]]
            a[name] = (lambda *args, f=f, l=location: f(*([l] + list(args))))
            a[name].name, a[name].loc = name, location

        super().examine()


class ProgramUniforms(Analyse):

    @staticmethod
    def _gl_uniform_(f, loc, name, v):
        if sn_logging.log_on_uniform_update():
            logging.debug('Uniform[{0}]: {1}\n'.format(name, v))
        f(loc, v)

    @staticmethod
    def _gl_uniformv_(f, loc, name, vec):
        if sn_logging.log_on_uniform_update():
            logging.debug('UniformV[{0}]: {1}\n'.format(name, vec))
        f(loc, *vec)

    @staticmethod
    def _gl_uniformf_(f, loc, name, v):
        if sn_logging.log_on_uniform_update():
            logging.debug('Uniformf[{0}]: {1}\n'.format(name, v))
        f(loc, v)

    @staticmethod
    def _gl_uniformfv_(f, loc, name, vec):
        if sn_logging.log_on_uniform_update():
            logging.debug('UniformFV[{0}]: {1}\n'.format(name, vec))
        f(loc, *vec)

    @staticmethod
    def _uniform_(f): return lambda loc, name, v: Program._gl_uniform_.__func__(f, loc, name, v)

    @staticmethod
    def _uniformv_(f): return lambda loc, name, *vec: Program._gl_uniformv_(f, loc, name, vec)

    @staticmethod
    def _uniformf_(f): return lambda loc, name, v: Program._gl_uniformf_(f, loc, name, v)

    @staticmethod
    def _uniformfv_(f): return lambda loc, name, *vec: Program._gl_uniformfv_(f, loc, name, vec)

    @staticmethod
    def _gl_uniform_matrix_(f, loc, name, mat):
        if sn_logging.log_on_uniform_update():
            logging.debug('Uniform[{0}]:\n{1}\n'.format(name, mat))
        f(loc, 1, GL_FALSE, mat.T)  # Row-major --> Column-major conversion
        # f(loc, 1, GL_FALSE, mat)

    @staticmethod
    def umatrix(f): return lambda loc, mat: f(loc, 1, GL_FALSE, mat.T)

    @staticmethod
    def _uniform_matrix_(f): return lambda loc, name, mat: Program._gl_uniform_matrix_(f, loc, name, mat)

    @staticmethod
    def _uniform_matrix_ignored_(): return lambda *args: None

    uniform_handler = dict([
        (GL_INT, _uniform_.__func__(glUniform1i)),
        (GL_INT_VEC2, _uniformv_.__func__(glUniform2i)),
        (GL_INT_VEC3, _uniformv_.__func__(glUniform3i)),
        (GL_INT_VEC4, _uniformv_.__func__(glUniform4i)),
        (GL_FLOAT, _uniformfv_.__func__(glUniform1f)),
        (GL_FLOAT_VEC2, _uniformfv_.__func__(glUniform2f)),
        (GL_FLOAT_VEC3, _uniformfv_.__func__(glUniform3f)),
        (GL_FLOAT_VEC4, _uniformfv_.__func__(glUniform4f)),


        (GL_FLOAT_MAT2, glUniformMatrix2fv),
        (GL_FLOAT_MAT3, glUniformMatrix3fv),
        (GL_FLOAT_MAT4, _uniform_matrix_.__func__(glUniformMatrix4fv)),
        (GL_FLOAT_MAT2x3, glUniformMatrix2x3fv),
        (GL_FLOAT_MAT2x4, glUniformMatrix2x4fv),
        (GL_FLOAT_MAT3x2, glUniformMatrix3x2fv),
        (GL_FLOAT_MAT3x4, glUniformMatrix3x4fv),
        (GL_FLOAT_MAT4x2, glUniformMatrix4x2fv),
        (GL_FLOAT_MAT4x3, glUniformMatrix4x3fv)])

    def __init__(self, *args):
        logging.debug('__init__@ProgramUniforms')
        self.u = defaultdict(lambda *args1, **kwargs1:
                             lambda *args2, **kwargs2:
                             logging.warning('なによ、この謎の Uniform 変数は！{}:{} / {}:{}'.format(
                                 args1, kwargs1, args2, kwargs2)))
        super().__init__()

    def examine(self):
        p = self._program
        logging.debug('examine@ProgramUniforms({})'.format(p))

        types = list(self.uniform_handler.keys())

        u = self.u

        ibuf = np.zeros(5, dtype=np.int32)
        glGetProgramInterfaceiv(p, GL_UNIFORM, GL_ACTIVE_RESOURCES, ibuf)
        n = ibuf[0]
        if sn_logging.log_on_shader_variables():
            logging.info('#uniforms = {0}'.format(n))

        bbuf = bytes(256)
        properties = np.array([GL_NAME_LENGTH, GL_TYPE, GL_LOCATION, GL_BLOCK_INDEX])
        for i in range(n):
            glGetProgramResourceiv(p, GL_UNIFORM, i, len(properties), properties,
                                   len(ibuf), ibuf[len(properties):], ibuf)
            loc = ibuf[2]
            if loc == -1:
                continue

            logging.info("loc = {0}, len = {1}, type = {2}".format(loc, ibuf[0], ibuf[1]))
            length = ibuf[0] + 1
            _t = ibuf[1]
            t = types[types.index(ibuf[1])].__repr__()
            logging.info('length = {0}, type = {1}, location = {2}' .format(length, t, loc))

            glGetProgramResourceName(p, GL_UNIFORM, i, len(bbuf), ibuf[:1], bbuf)
            length = ibuf[0]
            name = bbuf[:length].decode('utf-8')
            if sn_logging.log_on_shader_variables():
                logging.info('uniform {0}:{1}@{2}'.format(name, t, loc))
            f = self.uniform_handler[_t]
            u[name] = (lambda *args, f=f, loc=loc, name=name: f(*([loc, name] + list(args))))
            u[name].name = name
            u[name].loc = loc

        super().examine()


class SSBlockInformation(ProgramResource):
    _fields_, _features_ = ProgramResource.specs([
        ('name_length', GL_NAME_LENGTH),
        ('num_active_variables', GL_NUM_ACTIVE_VARIABLES),
        ('buffer_binding', GL_BUFFER_BINDING),
        ('buffer_data_size', GL_BUFFER_DATA_SIZE)])


class SSBVariableInformation(ProgramResource):
    _fields_, _features_ = ProgramResource.specs([
        ('type', GL_TYPE),
        ('array_size', GL_ARRAY_SIZE),
        ('offset', GL_OFFSET),
        ('array_stride', GL_ARRAY_STRIDE),
        ('name_length', GL_NAME_LENGTH),
        ('top_level_array_size', GL_TOP_LEVEL_ARRAY_SIZE)])


class ProgramShaderStorageBlock(Analyse):
    def __init__(self, *args):
        logging.debug('__init__@ProgramShaderStorageBlock')
        self.ssb = dict()
        super().__init__()

    def examine(self):
        logging.debug('examine@ProgramShaderStorageBlock')
        p = self._program
        ssb = self.ssb

        glGetProgramInterfaceiv(p, GL_SHADER_STORAGE_BLOCK, GL_ACTIVE_RESOURCES, pointer(glres))
        active_blocks = glres.val
        logging.info('#active shader storage block(s) = {}'.format(active_blocks))

        ssb_info = SSBlockInformation()
        ssb_varinfo = SSBVariableInformation()
        for block in range(active_blocks):
            ssb_info.query(p, GL_SHADER_STORAGE_BLOCK, block)
            logging.info('block = {}, name length = {}, #active variables = {}'.format(
                block, ssb_info.name_length, ssb_info.num_active_variables))
            logging.info('buffer binding = {}, buffer data size = {}'.format(
                ssb_info.buffer_binding, ssb_info.buffer_data_size))

            # Retrieving an active SS-Block name
            name = resource_name(p, GL_SHADER_STORAGE_BLOCK, block, ssb_info.name_length)
            logging.info('Shader storage block name: "{}"'.format(name))
            ssb[name] = block

            variables = np.zeros(ssb_info.num_active_variables, dtype=np.int32)
            glGetProgramResourceiv(p, GL_SHADER_STORAGE_BLOCK, block, 1,
                                   [GL_ACTIVE_VARIABLES], ssb_info.num_active_variables, pointer(glres), variables)
            logging.info('Active variables: {}'.format(variables))

            # Retrieving indices of the active member variables
            for var in variables:
                ssb_varinfo.query(p, GL_BUFFER_VARIABLE, var)
                logging.info('{}'.format([ssb_varinfo.type, ssb_varinfo.array_size,
                                          ssb_varinfo.offset, ssb_varinfo.array_stride,
                                          ssb_varinfo.name_length,
                                          ssb_varinfo.top_level_array_size]))
                var_name = resource_name(p, GL_BUFFER_VARIABLE, var, ssb_varinfo.name_length)
                logging.info('active variable[{}]: length: {}, name: "{}"'.format(
                    var, ssb_varinfo.name_length,  var_name))

        super().examine()


class _ProgramCore(GLObject):
    def examine(self, *args):
        pass


class Program(ProgramCore, ProgramVertexAttributes, ProgramUniforms, ProgramShaderStorageBlock, _ProgramCore):
    def __init__(self, path):
        logging.debug('__init__@Program')
        super().__init__(path)
        logging.debug('__init__@Program done!')

    def create(self, *args):
        logging.debug('create@Program')
        super().create()
        super().examine()

    def _get_active_resources(self, interface) -> np.ndarray:
        ibuf = np.zeros(5, dtype=np.int32)
        glGetProgramInterfaceiv(self._program, interface, GL_ACTIVE_RESOURCES, ibuf)
        return ibuf

    def use(self):
        logging.debug('use@Program({})'.format(self._program))
        glUseProgram(self._program)
