from collections import defaultdict

from .common import *

class A(Analyse):

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
    def _uniform_(f): return lambda loc, name, v: A._gl_uniform_(f, loc, name, v)

    @staticmethod
    def _uniformv_(f): return lambda loc, name, *vec: A._gl_uniformv_(f, loc, name, vec)

    @staticmethod
    def _uniformf_(f): return lambda loc, name, v: A._gl_uniformf_(f, loc, name, v)

    @staticmethod
    def _uniformfv_(f): return lambda loc, name, *vec: A._gl_uniformfv_(f, loc, name, vec)

    @staticmethod
    def _gl_uniform_matrix_(f, loc, name, mat):
        if sn_logging.log_on_uniform_update():
            logging.debug('Uniform[{0}]:\n{1}\n'.format(name, mat))
        f(loc, 1, GL_FALSE, mat.T)  # Row-major --> Column-major conversion
        # f(loc, 1, GL_FALSE, mat)

    @staticmethod
    def umatrix(f): return lambda loc, mat: f(loc, 1, GL_FALSE, mat.T)

    @staticmethod
    def _uniform_matrix_(f): return lambda loc, name, mat: A._gl_uniform_matrix_(f, loc, name, mat)

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
        (GL_FLOAT_MAT4x3, glUniformMatrix4x3fv),
    
        (GL_SAMPLER_2D, _uniform_.__func__(glUniform1i))])

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

        ibuf = sp.zeros(5, dtype=sp.int32)
        glGetProgramInterfaceiv(p, GL_UNIFORM, GL_ACTIVE_RESOURCES, ibuf)
        n = ibuf[0]
        if sn_logging.log_on_shader_variables():
            logging.info('#uniforms = {0}'.format(n))

        bbuf = bytes(256)
        properties = sp.array([GL_NAME_LENGTH, GL_TYPE, GL_LOCATION, GL_BLOCK_INDEX])
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
