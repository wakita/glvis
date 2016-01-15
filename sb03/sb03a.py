import math
from sb03 import *

class W(SB03):
    '''glVertexAttrib2fvを使ってデータをシェーダに送る例'''

    program = None

    def initializeGL(self):
        super(self.__class__, self).initializeGL()
        self.program = self.program or Program('sb03a.shaders')
        self.va = VertexArray()

    def paintGL(self):
        super(self.__class__, self).paintGL()

        self.program.use()

        self.va.bind()
        t = Time.time
# Todo: 変数をlocation(=0)ではなく，シンボルで指定したい．program.a['v_offset'] = self.v_offset と書きたい
        glVertexAttrib2f(0, math.cos(t) * 0.5, math.sin(t) * 0.5)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
