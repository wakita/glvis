# 頂点属性 position_vs と color_vs に与えるデータを同じバッファに指定している。
# それぞれ FLOAT の三つ組なので、各頂点のデータ量は 4 * (3 + 3) = 24 Bytes
# color_vs のオフセットは position_vs の分のデータとなるので 4 * 3 = 12 Bytes となる。
# glVertexAttribPointer へのオフセット値の与え方で苦労した。

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

        position_l, color_l = p.a['position_vs'].loc, p.a['color_vs'].loc
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
