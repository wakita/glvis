import math
from sb03 import *

class W(SB03):
    '''
    見た目はsb03bと同じ。シェーダの書き方だけが異なる。
    
    今回はvsからfsに受け渡すデータの記述にInterface Blockを用いた。これを用いる
    ことで関連する複数のデータをひとまとめに扱うとともに、異なるシェーダから見え
    る同じデータを異なる名前で参照できる。 '''

    program = None

    def initializeGL(self):
        super(self.__class__, self).initializeGL()
        self.program = self.program or Program('sb03c.shaders')
        self.vao = VertexArray()

    def paintGL(self):
        super(self.__class__, self).paintGL()

        program = self.program
        program.use()

        self.vao.bind()
        t = Time.time
        c = math.cos(t); s = math.sin(t)
        program.a['offset_vs'](c / 2, s / 2)
        program.a['color_vs']((c + 1) / 2, (s + 1) / 2, 0)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
