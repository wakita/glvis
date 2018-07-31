from .common import *

class A(Analyse):
    def __init__(self, *args):
        logging.debug('__init__@sn.gl.subroutine.A')
        self.subs = object()
        super().__init__()

    def examine(self):
        p = self._program

        n = sp.zeros(1, dtype=sp.int32)
        glGetProgramInterfaceiv(p, GL_VERTEX_SUBROUTINE, GL_ACTIVE_RESOURCES, n)
        logging.critical('#vertex subroutines = {}'.format(n[0]))
        glGetProgramInterfaceiv(p, GL_FRAGMENT_SUBROUTINE, GL_ACTIVE_RESOURCES, n)
        logging.critical('#fragment subroutines = {}'.format(n[0]))
