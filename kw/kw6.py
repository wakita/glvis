from sn.gl import *
from sn.qt import *
import sn.sn_logging as sn_logging

sn_logging.log_on_uniform_update(True)


class KW6(GLWidget):
    def initializeGL(self):
        super().initializeGL()
        VertexArray().bind()
        Program('kw6.shaders').use()

    def paintGL(self):
        super().paintGL()
        glDrawArrays(GL_PATCHES, 0, 4)
        sn_logging.log_on_uniform_update(False)

KW6.start()
