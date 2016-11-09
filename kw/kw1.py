import inspect, math, os.path

from sn.qt import *
from sn.gl import *
import sn.gl.geometry.t3d as T

import sn.gl.debug
debug.logOnSetUniform(True)

from sn.gl.geometry.pointgrid import V as PointGrid
from sn.gl.geometry.volume import D as DemoWidget


class KW1Widget(DemoWidget):
    def initializeGL(self):

        S = 100
        super().initializeGL('kw1.shaders', lambda program: PointGrid(program, S))

        self.eye = T.homogeneous(T.vec3(0.2, 1.1, 1.2))
        self.target, self.up = T.vec3(0.5, 0.6, 0.7), T.vec3(0, 1, 0)

        for p in [ GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND ]:
            glEnable(p)
        self.program.u['pointsize'](800/S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    def paintGL(self):
        eye = T.cartesian(T.rotateY(np.pi /20 * self.time).dot(self.eye))
        self.View = T.lookat(eye, self.target, self.up)
        super().paintGL()

    def onTick(self):
        debug.logOnSetUniform(False)
        self.updateGL()

KW1Widget.start(KW1Widget, fullscreen=True)
