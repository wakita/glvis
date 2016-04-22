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
