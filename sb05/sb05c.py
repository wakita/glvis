# シェーダのみで描画する例
# 最初、真っ黒ですが10秒くらい眺め続けて下さい。見えてきます。

from sb05 import *

class W(SB05):
    program = None

    def initializeGL(self):
        super().initializeGL('sb05c.shaders')
        self.setTime = self.program.u['time_u']

    def paintGL(self):
        super().paintGL()

        self.program.use()
        self.setTime(Time.time)
        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
