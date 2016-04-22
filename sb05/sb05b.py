from PyQt5.QtGui import QColor
from sb05 import *

class W(SB05):
    program = None

    def initializeGL(self):
        super().initializeGL('sb05a.shaders')
        p = self.program

        v = np.array([
             0.25, -0.25,  0.50, 1.0, 0.0, 0.0,
            -0.25, -0.25,  0.50, 0.0, 1.0, 0.0,
             0.00,  0.25,  0.50, 0.0, 0.0, 1.0], dtype=np.float32)

        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_DYNAMIC_DRAW)

        glVertexAttribPointer(p.A['position_vs'], 3, GL_FLOAT, GL_FALSE, 24, None)
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(p.A['color_vs'], 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

    def onTick(self):
        c = QColor.fromHsvF(math.fmod(Time.time / 10, 1), 1, 0.5)
        glClearColor(c.redF(), c.greenF(), c.blueF(), 1)
        super().onTick()

    def paintGL(self):
        super().paintGL()

        self.program.use()
        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
