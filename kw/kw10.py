from ctypes import *

import sn.gl.debug

sn.gl.debug._logOnSetUniform_ = True
sn.gl.debug._logOnShaderVariables_ = True

from PyQt5 import QtCore
from sn.gl import *
from sn.qt import *
#from sn.gl.geometry.shape import D as DEMO


global N, cs, graphics
N = 200000
compute = graphics = None


class KW10(GLWidget):

    def __init__(self, widget):
        super().__init__(widget)

    def onTick(self):
        self.updateGL()

    def minimumSizeHint(self):
        return QtCore.QSize(800, 800)

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        super().initializeGL()

        global compute, graphics

        glBindVertexArray(glGenVertexArrays(1))

        graphics = Program('kw10.shaders')
        compute = Program('kw10.cs')
        print('SSB binding@kw10.cs')
        for k, v in compute.ssb.items():
            print('- {}: {}'.format(k, v))

        ssbo = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, ssbo)
        glBufferData(GL_SHADER_STORAGE_BUFFER, 4 * 2 * N, None, GL_STATIC_DRAW)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, ssbo)

        graphics.use()
        glBindBuffer(GL_ARRAY_BUFFER, ssbo)
        pos_l = graphics.a['pos'].loc
        glVertexAttribPointer(pos_l, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(pos_l)

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)

    def paintGL(self):
        super().paintGL()

        compute.use()
        compute.u['time'](self.time)
        #glDispatchCompute(128, 1, 1)
        glDispatchCompute(N // 1024, 1, 1)

        graphics.use()
        glClear(GL_COLOR_BUFFER_BIT)
        #glDrawArrays(GL_POINTS, 0, min(int(100 * self.time), N))
        glDrawArrays(GL_POINTS, 0, N)
        sn.gl.debug._logOnSetUniform_ = False

if __name__ == '__main__':
    KW10.start(KW10)
