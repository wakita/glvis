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
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

        position_l, color_l = p.A['position_vs'], p.A['color_vs']
        glVertexAttribPointer(position_l, 3, GL_FLOAT, GL_FALSE, 24, None)
        glEnableVertexAttribArray(position_l)
        glVertexAttribPointer(color_l, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color_l)

    def paintGL(self):
        super().paintGL()

        self.program.use()
        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
