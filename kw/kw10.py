from ctypes import *
import sn.sn_logging as sn_logging

from PyQt5 import QtCore
from sn.gl import *
from sn.qt import *

sn_logging.log_on_uniform_update(True)
sn_logging.log_on_uniform_update(True)

N = 20
compute  = None  # type: Program
graphics = None  # type: Program


class KW10(GLWidget):
    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(800, 800)

    def initializeGL(self):
        super().initializeGL()
        glBindVertexArray(glGenVertexArrays(1))

        global compute, graphics
        graphics, compute = Program('kw10.shaders'), Program('kw10.cs')

        position, color = glGenBuffers(2)

        glBindBuffer(GL_SHADER_STORAGE_BUFFER, position)
        glBufferData(GL_SHADER_STORAGE_BUFFER, 4 * 2 * N, None, GL_STATIC_DRAW)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, compute.ssb['position_buf'], position)

        glBindBuffer(GL_SHADER_STORAGE_BUFFER, color)
        glBufferData(GL_SHADER_STORAGE_BUFFER, 4 * 3 * N, None, GL_STATIC_DRAW)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, compute.ssb['color_buf'], color)

        graphics.use()

        glBindBuffer(GL_ARRAY_BUFFER, position)
        position_l = graphics.a['position_vs'].loc
        glVertexAttribPointer(position_l, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position_l)

        glBindBuffer(GL_ARRAY_BUFFER, color)
        color_l = graphics.a['color_vs'].loc
        glVertexAttribPointer(color_l, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(color_l)

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)

    def paintGL(self):
        super().paintGL()

        compute.use()
        compute.u['time'](self.time)
        glDispatchCompute(1, 1, 1)

        graphics.use()
        glDrawArrays(GL_POINTS, 0, N)

        sn_logging.log_on_uniform_update(False)

KW10.start()
