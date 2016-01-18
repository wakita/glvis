from sb05 import *

class W(SB05):
    program = None

    def initializeGL(self):
        super().initializeGL('sb05c.shaders')
        self.time_l = self.program.U['time_u']

    def paintGL(self):
        super().paintGL()

#       time_b = np.array([Time.time], dtype=np.float32)
#       glUniform1fv(self.time_l, 1, time_b)

        self.program.use()
        glUniform1f(self.time_l, float(Time.time))

        self.va.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
