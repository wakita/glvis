import os.path

from sn.gl import *
from sn.qt import *
import sn.gl.debug

sn.gl.debug.logOnShaderVariables(True)

class KW2(GLWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    def initializeGL(self):
        super().initializeGL()
        self.program = Program('kw2.shaders')
        vao = VertexArray()
        vao.bind()
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def paintGL(self):
        super().paintGL()
        program = self.program
        program.use()

        t = Time.time
        glDrawArrays(GL_PATCHES, 0, 3)
        glFlush()

if __name__ == '__main__':
    app = Application()
    widget = KW2(None)
    widget.show()
    app.startTimer(timeout = 1000/60, onTick = widget.onTick)
    app.run()
