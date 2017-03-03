# coding: utf-8

# kw1b.pyはkw1a.pyのシェーダプログラムにサブルーチンUniformを導入した作例
# 一秒ごとに表示方法を彩色と灰色に切り替える。

import math

import sn.gl.debug as debug
import sn.gl.geometry.T3D as T
from sn.gl import *
from sn.gl.geometry.points import V as POINTS
from sn.gl.geometry.volume import D as DEMO
debug.logOnSetUniform(True)


class KW1AWidget(DEMO):

    def __init__(self, widget):
        super().__init__(widget)
        self.eye = T.homogeneous(T.vec3(0.2, 1.1, 1.2))
        self.target = T.vec3(0.5, 0.6, 0.7)
        self.up = T.vec3(0, 1, 0)
        self.paint = None
        self.doPaint = -1

    @staticmethod
    def points(s):
        vvals = np.array(range(s)) * 2. / (s - 1) - 1.
        return [(x, y, z) for x in vvals for y in vvals for z in vvals]

    def initializeGL(self):

        s = 100
        super().initializeGL('kw1b.shaders', lambda _program: POINTS(_program, self.points(s)))

        for p in [ GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND ]:
            glEnable(p)
        self.program.u['pointsize'](800/s)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        stage = [self.program._program, GL_FRAGMENT_SHADER]

        print('Active subroutines: {0}'.format(glGetProgramStageiv(*stage, GL_ACTIVE_SUBROUTINES)))
        self.paint = [glGetSubroutineIndex(*stage, 'paint' + f) for f in 'Color Gray'.split()]
        print(self.paint)

    def paintGL(self):
        eye = T.cartesian(T.rotateY(np.pi /20 * self.time).dot(self.eye))
        self.View = T.lookat(eye, self.target, self.up)
        dp = math.floor(self.time / 5) % 2
        if self.doPaint != dp:
            self.doPaint = dp
            glUniformSubroutinesuiv(GL_FRAGMENT_SHADER, 1, [self.doPaint])
        super().paintGL()

    def onTick(self):
        debug.logOnSetUniform(False)
        self.updateGL()

KW1AWidget.start(KW1AWidget, fullscreen=True)
