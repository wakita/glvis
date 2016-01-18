import math
from sb05 import *

class W(SB05):
    program = None

    position = np.array([
         0.25, -0.25,  0.50,
        -0.25, -0.25,  0.50,
         0.00,  0.25,  0.50], dtype=np.float32)

    color = np.array([
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0], dtype=np.float32)

    def initializeGL(self):
        super().initializeGL('sb05a.shaders')

        p, c, [position_b, color_b] = self.position, self.color, glGenBuffers(2)

        glBindBuffer(GL_ARRAY_BUFFER, position_b)
        glBufferData(GL_ARRAY_BUFFER, p.nbytes, p, GL_STATIC_DRAW)
        glVertexAttribPointer(self.program.A['position_vs'], 3, GL_FLOAT, GL_FALSE, 12, None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, color_b)
        glBufferData(GL_ARRAY_BUFFER, c.nbytes, c, GL_STATIC_DRAW)
        glVertexAttribPointer(self.program.A['color_vs'], 3, GL_FLOAT, GL_FALSE, 12, None)
        glEnableVertexAttribArray(1)

    def paintGL(self):
        super().paintGL()

        self.program.use()
        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
