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
        position_vs = self.program.a['position_vs'].loc
        glVertexAttribPointer(position_vs, 3, GL_FLOAT, GL_FALSE, 12, None)
        glEnableVertexAttribArray(position_vs)

        glBindBuffer(GL_ARRAY_BUFFER, color_b)
        glBufferData(GL_ARRAY_BUFFER, c.nbytes, c, GL_STATIC_DRAW)
        color_vs = self.program.a['color_vs'].loc
        glVertexAttribPointer(color_vs, 3, GL_FLOAT, GL_FALSE, 12, None)
        glEnableVertexAttribArray(color_vs)

    def paintGL(self):
        super().paintGL()

        self.program.use()
        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
