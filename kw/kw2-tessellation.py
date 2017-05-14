from sn.gl import *
from sn.qt import *


class KW2(GLWidget):
    def __init__(self):
        super().__init__()
        self.program = None

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

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
        glDrawArrays(GL_PATCHES, 0, 3)
        glFlush()

KW2.start()
