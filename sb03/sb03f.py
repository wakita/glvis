import math
from sb03 import *

class W(SB03):

    program = None

    def initializeGL(self):
        super(self.__class__, self).initializeGL()
        self.program = self.program or Program('sb03f.shaders')
        self.vao = VertexArray()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPointSize(10)

    def paintGL(self):
        super(self.__class__, self).paintGL()

        program = self.program
        program.use()
        self.vao.bind()

        t = Time.time
        c = math.cos(t); s = math.sin(t)
        program.a['offset_vs'](c / 2, s / 2)
        program.a['color_vs']((c + 1) / 2, (s + 1) / 2, 0, 1)

        glDrawArrays(GL_PATCHES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
