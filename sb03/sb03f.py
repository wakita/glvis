import math
from OpenGL.GL import *

from sn.qt import Time
from sn.gl import Program
import sb03

class W(sb03.SB03):
    def initializeGL(self):
        super(self.__class__, self).initializeGL()
        self.program = Program('sb03f.shaders')
        self.VAO = glGenVertexArrays(1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPointSize(10)

    def paintGL(self):
        super(self.__class__, self).paintGL()

        self.program.use()
        glBindVertexArray(self.VAO)
        t = Time.time
        c = math.cos(t); s = math.sin(t)
        glVertexAttrib2f(0, c / 2, s / 2)
        glVertexAttrib4f(1, (c + 1) / 2, (s + 1) / 2, 0, 1)

        glDrawArrays(GL_PATCHES, 0, 3)
        glFlush()

if __name__ == '__main__': sb03.start(W)
