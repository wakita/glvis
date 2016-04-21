from sn.gl import *
from sn.qt import *

class S(GLWidget):

    program = None

    def initializeGL(self, shaderpath, Geometry):
        super().initializeGL()
        self.program = self.program or Program(shaderpath)
        self.program.use()
        self.geometry = Geometry(self.program)

    def paintGL(self):
        super().paintGL()
        self.geometry.render()

    def minimumSizeHint(self): return QtCore.QSize(200, 200)
