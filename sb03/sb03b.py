import math
from sb03 import *

class W(SB03):
    '''glVertexAttrib... を使って複数のデータをシェーダに送る例'''

    program = None

    def initializeGL(self):
        super(self.__class__, self).initializeGL()
        self.program = self.program or Program('sb03b.shaders')
        self.vao = VertexArray()

    def paintGL(self):
        super(self.__class__, self).paintGL()

        self.program.use()

        self.vao.bind()
        t = Time.time
# Todo: 変数をlocation(=0)ではなく，シンボルで指定したい．
        glVertexAttrib2f(0, math.cos(t) / 2, math.sin(t) / 2)
        glVertexAttrib4f(1, (math.cos(t) + 1) / 2, (math.sin(t) + 1) / 2, 0, 1)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
