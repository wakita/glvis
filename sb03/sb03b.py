import math
from sb03 import *

class W(SB03):
    '''glVertexAttrib... を使って複数のデータをシェーダに送る例'''

    program = None

    def initializeGL(self):
        super().initializeGL()
        self.program = self.program or Program('sb03b.shaders')
        self.vao = VertexArray()

    def paintGL(self):
        super().paintGL()

        program = self.program
        program.use()

        self.vao.bind()
        t = Time.time
        program.a['offset_vs'](math.cos(t) / 2, math.sin(t) / 2)
        program.a['color_vs']((math.cos(t) + 1) / 2, (math.sin(t) + 1) / 2, 0, 1)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
