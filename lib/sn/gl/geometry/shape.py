from ...qt.glwidget import GLWidget
from .. import *

class S(object):
    def __init__(self, program):
        self.program = program
        program.use()
        self._va = VertexArray()
        self.bind()

    def bind(self):
        self._va.bind()

    def unbind(self):
        self._va.unbind()

    def enable(props):
        for p in props: glEnable(p)

    def use(self):
        self.bind()
        self.program.use()

    def render(self):
        pass

class D(GLWidget):
    program = None

    def initializeGL(self, shaderpath, Geometry):
        super().initializeGL()
        self.program = self.program or Program(shaderpath)
        self.program.use()
        if Geometry:
            self.geometry = Geometry(self.program)
            self.geometry.use()

    def paintGL(self):
        super().paintGL()
        self.geometry.render()

    def minimumSizeHint(self): return QtCore.QSize(200, 200)
