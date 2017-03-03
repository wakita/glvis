from sn.gl import *
from sn.qt import *
import sn.gl.debug

sn.gl.debug._logOnSetUniform_ = True

class KW6(GLWidget):
    def onTick(self): self.updateGL()

    def initializeGL(self):
        super().initializeGL()
        self.program = Program('kw6.shaders')
        VertexArray().bind()

    def paintGL(self):
        super().paintGL()
        self.program.use()

        self.program.u['t'](self.time)
        glDrawArrays(GL_PATCHES, 0, 4)
        glFlush()
        sn.gl.debug._logOnSetUniform_ = False

KW6.start(KW6)
