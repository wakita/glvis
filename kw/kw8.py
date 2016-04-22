import inspect, math, os.path

from PyQt5.QtGui import QColor

from sn.qt import *
from sn.gl import *
import sn.gl.geometry.t3d as T

import sn.gl.debug
debug.logOnSetUniform(True)

from sn.gl.geometry.pointgrid import V as PointGrid
from sn.gl.geometry.volume import D as Demo

class KW8(Demo):
    def initializeGL(self):
        S = 100
        super().initializeGL('kw8a.shaders', lambda program: PointGrid(program, S))

        self.eye, self.target, self.up = T.vec3(0, 0.5, 0.9), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(self.eye, self.target, self.up)

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
        hue = math.fmod(self.t / 10, 1)
        c = QColor.fromHsvF(hue, 1., .5)
        glClearColor(c.redF(), c.greenF(), c.blueF(), 1)
        glClear(GL_COLOR_BUFFER_BIT)

        eye = T.cartesian(T.rotateY(np.pi * (.9 - self.t / 20)).dot(T.homogeneous(self.eye)))
        self.View = T.lookat(eye, self.target, self.up)
        super().paintGL()
        self.frames = self.frames + 1

    def onTick(self):
        debug.logOnSetUniform(False)
        self.updateGL()

KW8.start(KW8)
