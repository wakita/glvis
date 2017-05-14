from PyQt5 import QtCore
from sn.gl import *
from sn.qt import *
import sn.gl.geometry.t3d as T
import sn.sn_logging as sn_logging

sn_logging.log_on_uniform_update(True)


class RT1(GLWidget3D):
    def __init__(self):
        super().__init__()

        eye, target, up = T.vec3(0, -10, 25), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)
        self.program = None  # type: Program

    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(1000, 800)

    def initializeGL(self):
        super().initializeGL()
        self.program = Program('rt1.shaders')
        self.program.use()
        VertexArray().bind()

        glDisable(GL_DEPTH_TEST)
        [glEnable(p) for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_BLEND]]
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        super().paintGL()
        p = self.program
        p.u['time'](Time.time)
        n = int(max(min(Time.time - 10, 120)**3, 1))
        p.u['pointsize'](100.0 / pow(n, 1./3))
        glDrawArrays(GL_POINTS, 0, n)

RT1.start()
