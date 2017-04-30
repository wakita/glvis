'''
未完成
シェーダのコードを見ると、意図したのは三角形が回転しながら、色を変化させる様子。
たぶん、Uniform Blockの使い方を示したかったのだろう。アプリケーションから Uniform Block にデータを送り込んでいないので、画面は静止したまま。
'''

from sb05 import *

class W(SB05):
    program = None

    def initializeGL(self):
        super().initializeGL('sb05d.shaders')

    def paintGL(self):
        super().paintGL()

        self.program.use()
        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
