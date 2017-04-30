# This program does not work
# I attempted to use OpenGL.arrays.vbo feature of PyOpenGL but so far unsuccessful.
# The app crashes.

# なにかやりたかったらしいが、今となっては意味不明。

from sb05 import *

from OpenGL.arrays import vbo

class W(SB05):
    program = None

    def initializeGL(self):
        super().initializeGL('sb05a.shaders')

        v = np.array([
             0.25, -0.25,  0.50, 1.0, 0.0, 0.0,
            -0.25, -0.25,  0.50, 0.0, 1.0, 0.0,
             0.00,  0.25,  0.50, 0.0, 0.0, 1.0], dtype=np.float32)

        vertex_b = vbo.VBO(v)
        vertex_b.bind()

        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

        glVertexAttribPointer(self.program.a['position_vs'].loc, 3, GL_FLOAT, GL_FALSE, 24, None)
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glVertexAttribPointer(self.program.a['color_vs'].loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        print('initialization done')

    def paintGL(self):
        super().paintGL()

        self.program.use()
        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)

