import random

from PyQt5 import QtCore
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
from sn.gl.geometry.points import V as Points
import sn.gl.geometry.t3d as T


class RT1(Demo):

    def __init__(self, W):
        super().__init__(W)
        S = self.S = 100
        self.points = points = [(random.gauss(0, 1) * 1, (random.random()**2 * 0.8 + 0.2) * 5,
                                 10.0 * i / S**3)
                                for i in range(S ** 3)]

    def onTick(self): self.updateGL()

    def initializeGL(self):
        points = self.points
        super().initializeGL('rt1.shaders', lambda program: Points(program, points))

        eye, target, up = T.vec3(0, 0, 30), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        glDisable(GL_DEPTH_TEST)
        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](50 / self.S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        self.program.u['t'](Time.time % 10.0)
        super().paintGL()

if __name__ == '__main__':
    import sn.gl.debug
    sn.gl.debug.logOnShaderVariables(True)
    RT1.start(RT1, fullscreen=True)
