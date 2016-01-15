import math
from sb03 import *
from PyQt5.QtGui import QColor

class W(SB03):
    program = None

    def initializeGL(self):
        super(self.__class__, self).initializeGL()
        self.program = self.program or Program('sb03e.shaders')
        self.vao = VertexArray()
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPointSize(5)

    def paintGL(self):
        super(self.__class__, self).paintGL()

        self.program.use()
        self.vao.bind()
        t = Time.time
        glVertexAttrib2f(0, math.cos(t) / 2, math.sin(t) / 2)
        c = QColor.fromHsvF(math.fmod(t / math.pi, 1), 1, .5)
        glVertexAttrib3f(1, c.redF(), c.greenF(), c.blueF())

        glDrawArrays(GL_PATCHES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
