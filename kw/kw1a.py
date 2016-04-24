import inspect, math, os.path

from sn.qt import *
from sn.gl import *
import sn.gl.geometry.t3d as T

import sn.gl.debug
debug.logOnSetUniform(True)

from sn.gl.geometry.points import V as Points
from sn.gl.geometry.volume import D as DemoWidget

class KW8AWidget(DemoWidget):
    def points(self, S):
        vvals = np.array(range(S)) * 2. / (S - 1) - 1.
        return [ (x, y, z) for x in vvals for y in vvals for z in vvals ]

    def initializeGL(self):

        S = 100
        super().initializeGL('kw1.shaders', lambda program: Points(program, self.points(S)))

        self.eye = T.homogeneous(T.vec3(0.2, 1.1, 1.2))
        self.target, self.up = T.vec3(0.5, 0.6, 0.7), T.vec3(0, 1, 0)
#       self.eye, self.target, self.up = T.vec3(1.2, 1.1, 0.2), T.vec3(0.5, 0.6, 0.7), T.vec3(0, 1, 0)
#       self.View = T.lookat(self.eye, self.target, self.up)

        for p in [ GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND ]:
            glEnable(p)
        self.program.u['pointsize'](800/S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    t = 0
    nextFPS = 1
    frames = 0

    def paintGL(self):
        self.t = Time.time
        if self.t > self.nextFPS:
            self.nextFPS = self.nextFPS + 1
            print('Frames/sec = {0}'.format(self.frames))
            self.frames = 0
        glClear(GL_COLOR_BUFFER_BIT)

        eye = T.cartesian(T.rotateY(np.pi /20 * self.t).dot(self.eye))
        self.View = T.lookat(eye, self.target, self.up)
        super().paintGL()
        self.frames = self.frames + 1

    def onTick(self):
        debug.logOnSetUniform(False)
        self.updateGL()

KW8AWidget.start(KW8AWidget, fullscreen=True)
