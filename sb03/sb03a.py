import math
from sb03 import *


class W(SB03):
    program = None

    def initializeGL(self):
        super().initializeGL()
        self.program = self.program or Program('sb03a.shaders')
        self.va = VertexArray()

    def paintGL(self):
        super().paintGL()

        program = self.program
        program.use()

        self.va.bind()
        t = Time.time
        program.a['offset_vs'](math.cos(t) / 2, math.sin(t) / 2)
        program.u['color_u']((math.cos(t) + 1) / 2, (math.sin(t) + 1) / 2)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
