import math

from OpenGL.GL import *

from sn.qt import Time
from sn.gl import Program
import sb03

class W(sb03.SB03):
    '''glVertexAttrib... を使って複数のデータをシェーダに送る例'''

    program = None

    def initializeGL(self):
        super(self.__class__, self).initializeGL()
        self.program = self.program or Program('sb03b.shaders')
        self.VAO = glGenVertexArrays(1)

    def paintGL(self):
        super(self.__class__, self).paintGL()

        self.program.use()

        glBindVertexArray(self.VAO)
        t = Time.time
# Todo: 変数をlocation(=0)ではなく，シンボルで指定したい．
        glVertexAttrib2f(0, math.cos(t) / 2, math.sin(t) / 2)
        glVertexAttrib4f(1, (math.cos(t) + 1) / 2, (math.sin(t) + 1) / 2, 0, 1)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': sb03.start(W)
