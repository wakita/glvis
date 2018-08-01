from .common import *

class A(Analyse):

    def __init__(self, *args):
        logging.debug('__init__@sn.gl.subroutine.A')
        F = self.F = Object()
        F.vs = Object(); F.tcs = Object(); F.tes = Object(); F.fs = Object(); F.cs = Object()
        self._F = {
            GL_VERTEX_SUBROUTINE_UNIFORM:          (F.vs,  GL_VERTEX_SHADER),
            GL_TESS_CONTROL_SUBROUTINE_UNIFORM:    (F.tcs, GL_TESS_CONTROL_SHADER),
            GL_TESS_EVALUATION_SUBROUTINE_UNIFORM: (F.tes, GL_TESS_EVALUATION_SHADER),
            GL_FRAGMENT_SUBROUTINE_UNIFORM:        (F.fs,  GL_FRAGMENT_SHADER),
            GL_COMPUTE_SUBROUTINE_UNIFORM:         (F.cs,  GL_COMPUTE_SHADER) 
        }
        super().__init__()

    def examine(self):
        p = self._program

        _n = sp.zeros(1, dtype=sp.int32)
        _properties = [GL_NAME_LENGTH, GL_LOCATION]
        properties = sp.array(_properties)
        lengths = sp.zeros(1, dtype=sp.int32)
        info = sp.zeros(len(properties), dtype=sp.int32)

        bbuf = bytes(256)

# Counting the number of subroutine uniform variables
        for uniform_kind in [GL_VERTEX_SUBROUTINE_UNIFORM,
                             GL_TESS_CONTROL_SUBROUTINE_UNIFORM,
                             GL_TESS_EVALUATION_SUBROUTINE_UNIFORM,
                             GL_FRAGMENT_SUBROUTINE_UNIFORM,
                             GL_COMPUTE_SUBROUTINE_UNIFORM]:
            glGetProgramInterfaceiv(p, uniform_kind, GL_ACTIVE_RESOURCES, _n)
            nvars = _n[0]
            logging.critical('#uniform variables({}) = {}'.format(uniform_kind, nvars))

            for i in range(nvars):
                glGetProgramResourceiv(p, uniform_kind, i,
                                       len(_properties), properties, len(_properties), lengths,
                                       info)
                location = info[1]
                glGetProgramResourceName(p, uniform_kind, i, len(bbuf), lengths, bbuf)
                var_name = bbuf[:lengths[0]].decode('utf-8')
                logging.critical('Univorm variable: {}@{}'.format(var_name, location))

                subroutines, shader_type = self._F[uniform_kind]

                # var_index = glGetSubroutineIndex(p, shader_type, var_name)

                params = [p, shader_type, location]

                glGetActiveSubroutineUniformiv(*params, GL_NUM_COMPATIBLE_SUBROUTINES, _n)
                logging.critical('#Subroutines = {}@{}'.format(_n[0], var_name))

                subroutine_ids = sp.zeros(_n[0], dtype=sp.int32)
                glGetActiveSubroutineUniformiv(*params, GL_COMPATIBLE_SUBROUTINES, subroutine_ids)
                logging.critical('subroutines = {}'.format(subroutine_ids))
                for i in subroutine_ids:
                    glGetActiveSubroutineName(p, shader_type, i, len(bbuf), _n, bbuf)
                    subroutine_name = bbuf[:_n[0]].decode('utf-8')
                    index = glGetSubroutineIndex(p, shader_type, subroutine_name)
                    logging.critical('{}: {}'.format(subroutine_name, index))

                    setattr(subroutines, subroutine_name,
                            (lambda t, i: lambda: glUniformSubroutinesuiv(t, 1, sp.array([i], dtype=sp.uint32)))(shader_type, index))

        super().examine()
