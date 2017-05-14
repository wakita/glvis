import logging
import re
import sys
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


def _examine_uniforms_(self):
    p = self._program

    types = list(self.uniformHandler.keys())

    # u = self.u = defaultdict(lambda: lambda *args: None)
    def _unbound_uniform_(*args):
        logging.warning('なにこのユニフォーム変数、知らないわよ！\n{}'.format(args))
    _unbound_uniform_.loc = -1
    _unbound_uniform_.name = 'なにこのユニフォーム変数、知らないわよ！'
    u = self.u = defaultdict(lambda *args: _unbound_uniform_(*args))

    ibuf = np.zeros(5, dtype=np.int32)
    glGetProgramInterfaceiv(self._program, GL_UNIFORM, GL_ACTIVE_RESOURCES, ibuf)
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
        f = self.uniformHandler[_t]
        u[name] = (lambda *args, f=f, loc=loc, name=name: f(*([loc, name] + list(args))))
        u[name].name = name
        u[name].loc = loc
        logging.debug(u)


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


def _examine_shader_storage_block_(self):
    p = self._program
    ssb = self.ssb = dict()

    glGetProgramInterfaceiv(p, GL_SHADER_STORAGE_BLOCK, GL_ACTIVE_RESOURCES, pointer(glres))
    active_blocks = glres.val
    logging.info('#active shader storage block(s) = {}\n'.format(active_blocks))

    ssb_info = SSBlockInformation()
    ssb_varinfo = SSBVariableInformation()
    for block in range(active_blocks):
        ssb_info.query(p, GL_SHADER_STORAGE_BLOCK, block)
        logging.info('block = {}, name length = {}, #active variables = {}\nbuffer binding = {}, buffer data size = {}'.
                     format(block, ssb_info.name_length,
                            ssb_info.num_active_variables, ssb_info.buffer_binding, ssb_info.buffer_data_size))

        # Retrieving an active SS-Block name
        name = resource_name(p, GL_SHADER_STORAGE_BLOCK, block, ssb_info.name_length)
        logging.info('ssb name: "{}"'.format(name))
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
            logging.info('active variable[{}]: length: {}, name: "{}"\n'.format(
                var, ssb_varinfo.name_length,  var_name))


class Program(GLObject):
    shadertypes = dict(
            vs=GL_VERTEX_SHADER, vert=GL_VERTEX_SHADER, vertex=GL_VERTEX_SHADER,
            tcs=GL_TESS_CONTROL_SHADER, tesscontrol=GL_TESS_CONTROL_SHADER, tessellationcontrol=GL_TESS_CONTROL_SHADER,
            tes=GL_TESS_EVALUATION_SHADER, tesseval=GL_TESS_EVALUATION_SHADER, tessevaluation=GL_TESS_EVALUATION_SHADER,
            tessellationevaluation=GL_TESS_EVALUATION_SHADER,
            gs=GL_GEOMETRY_SHADER, geometry=GL_GEOMETRY_SHADER,
            fs=GL_FRAGMENT_SHADER, fragment=GL_FRAGMENT_SHADER,
            cs=GL_COMPUTE_SHADER, compute=GL_COMPUTE_SHADER)
    '''@type: Dict[str, int]'''

    def __init__(self, path):
        self._program = None
        self.u = self.a = self.ssb = None
        super().__init__(path)

    def create(self, path):
        self._load(path)
        self._create()
        self._compile_link()
        self._validate()
        self._examine_variables()
        self._examine_uniforms()
        self._examine_uniform_blocks()
        self._examine_shader_storage_block()

    def delete(self):
        if self._program is not None and bool(glDeleteProgram):
            p = self._program
            self._program = None
            glDeleteProgram(p)

    def _load(self, path):
        shadertypes, shaderset = self.shadertypes, []
        kind, code = None, []
        with open(path, 'r') as f:
            for line in f:
                k = ''.join(line.strip('#\n').split(' ')).lower().replace('shader', '')
                if k in shadertypes.keys():
                    if kind is not None:
                        shaderset.append((kind, ''.join(code)))
                    kind, code = shadertypes[k], []
                else:
                    code.append(line)
        if kind is not None:
            shaderset.append((kind, ''.join(code)))
        self._shaderset = shaderset

    def _create(self):
        self._program = glCreateProgram()
        self._validated = self._linked = False
        self._variables = dict(vertex=set(), uniform=set())
        self._samplers = {}
        self._known_invalid = set()

    def _compile_link(self):
        self._linked = False
        program = self._program
        shaderlist = []
        for t, code in self._shaderset:
            logging.info('Compiling a shader: {0}\n'.format(t))
            shader = glCreateShader(t)
            shaderlist.append(shader)
            glShaderSource(shader, code)
            glCompileShader(shader)
            if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                errors = str(glGetShaderInfoLog(shader), 'utf-8')
                raise ShaderProgramSyntaxError(Program._get_error(code, errors, 4))
            glAttachShader(program, shader)

        glLinkProgram(program)
        if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            errors = glGetProgramInfoLog(program)
            if len(errors) > 0:
                raise ShaderProgramLinkingError(errors.decode('utf-8'))
        for shader in shaderlist:
            glDetachShader(program, shader)
            glDeleteShader(shader)
        self._linked = True

    def _validate(self):
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

    def _examine_variables(self):
        self._examine_attributes()

    vertexAttribHandler = dict()
    vertexAttribHandler[GL_FLOAT_VEC2] = glVertexAttrib2f
    vertexAttribHandler[GL_FLOAT_VEC3] = glVertexAttrib3f
    vertexAttribHandler[GL_FLOAT_VEC4] = glVertexAttrib4f

    def _examine_attributes(self):
        program = self._program

        n = np.zeros(1, dtype=np.int32)
        glGetProgramInterfaceiv(program, GL_PROGRAM_INPUT, GL_ACTIVE_RESOURCES, n)
        if sn_logging.log_on_shader_variables():
            logging.info('#attributes = {0}'.format(n[0]))

        types = list(self.vertexAttribHandler.keys())
        properties = np.array([GL_NAME_LENGTH, GL_TYPE, GL_LOCATION])

        bbuf = bytes(256)
        info = np.zeros(3, dtype=np.int32)
        lengths = np.zeros(1, dtype=np.int32)
        a = self.a = dict()
        for attr in range(n[0]):
            glGetProgramResourceiv(program, GL_PROGRAM_INPUT, attr,
                                   3, properties, 3, lengths,
                                   info)
            logging.info('length = {0}, info = {1}'.format(lengths, info))
            glGetProgramResourceName(program, GL_PROGRAM_INPUT, attr, len(bbuf), lengths, bbuf)
            location = info[2]
            if location == -1:
                continue
            name = bbuf[:lengths[0]].decode('utf-8')
            typestr = types[types.index(info[1])].__repr__()
            if sn_logging.log_on_shader_variables():
                logging.info('attribute {0}:{1}@{2}'.format(name, typestr, location))
            f = self.vertexAttribHandler[info[1]]
            a[name] = (lambda *args, f=f, l=location: f(*([l] + list(args))))
            a[name].name, a[name].loc = name, location

    uniformHandler = dict()

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

    uniformHandler[GL_INT]        = _uniform_.__func__(glUniform1i)
    uniformHandler[GL_INT_VEC2]   = _uniformv_.__func__(glUniform2i)
    uniformHandler[GL_INT_VEC3]   = _uniformv_.__func__(glUniform3i)
    uniformHandler[GL_INT_VEC4]   = _uniformv_.__func__(glUniform4i)
    uniformHandler[GL_FLOAT]      = _uniformfv_.__func__(glUniform1f)
    uniformHandler[GL_FLOAT_VEC2] = _uniformfv_.__func__(glUniform2f)
    uniformHandler[GL_FLOAT_VEC3] = _uniformfv_.__func__(glUniform3f)
    uniformHandler[GL_FLOAT_VEC4] = _uniformfv_.__func__(glUniform4f)

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

    uniformHandler[GL_FLOAT_MAT2] = glUniformMatrix2fv
    uniformHandler[GL_FLOAT_MAT3] = glUniformMatrix3fv
    uniformHandler[GL_FLOAT_MAT4] = _uniform_matrix_.__func__(glUniformMatrix4fv)
    uniformHandler[GL_FLOAT_MAT2x3] = glUniformMatrix2x3fv

    uniformHandler[GL_FLOAT_MAT2x4] = glUniformMatrix2x4fv
    uniformHandler[GL_FLOAT_MAT3x2] = glUniformMatrix3x2fv
    uniformHandler[GL_FLOAT_MAT3x4] = glUniformMatrix3x4fv
    uniformHandler[GL_FLOAT_MAT4x2] = glUniformMatrix4x2fv
    uniformHandler[GL_FLOAT_MAT4x3] = glUniformMatrix4x3fv

    def _examine_uniforms(self):
        _examine_uniforms_(self)

    def was_examine_uniforms(self):
        p = self._program

        types = list(self.uniformHandler.keys())
        u = self.u = defaultdict(lambda: lambda *args: None)

        ibuf = np.zeros(5, dtype=np.int32)
        glGetProgramInterfaceiv(self._program, GL_UNIFORM, GL_ACTIVE_RESOURCES, ibuf)
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

            logging.debug("loc = {0}, len = {1}, type = {2}".format(loc, ibuf[0], ibuf[1]))
            length = ibuf[0] + 1
            _t = ibuf[1]
            t = types[types.index(ibuf[1])].__repr__()
            logging.debug('length = {0}, type = {1}, location = {2}' .format(length, t, loc))

            glGetProgramResourceName(p, GL_UNIFORM, i, len(bbuf), ibuf[:1], bbuf)
            length = ibuf[0]
            name = bbuf[:length].decode('utf-8')
            if sn_logging.log_on_shader_variables():
                logging.info('uniform {0}:{1}@{2}'.format(name, t, loc))
            f = self.uniformHandler[_t]
            u[name] = (lambda *args, f=f, loc=loc, name=name: f(*([loc, name] + list(args))))
            u[name].name, u[name].loc = name, loc
        logging.debug(u)

    def _examine_uniform_blocks(self):
        pass

    def _get_active_resources(self, interface) -> np.ndarray:
        ibuf = np.zeros(5, dtype=np.int32)
        glGetProgramInterfaceiv(self._program, interface, GL_ACTIVE_RESOURCES, ibuf)
        return ibuf

    def _examine_shader_storage_block(self):
        _examine_shader_storage_block_(self)

    def use(self):
        glUseProgram(self._program)
