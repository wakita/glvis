from PyQt5 import QtCore
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
import sn.gl.geometry.t3d as T


class RT1(GLWidget3D):

    def __init__(self, W):
        super().__init__(W)
        self.MAX_DELAY = 20

    def minimumSizeHint(self): return QtCore.QSize(1000, 800)

    def onTick(self): self.updateGL()

    def initializeGL(self):
        super().initializeGL()
        self.program = Program('rt1.shaders')
        self.program.use()
        self.vao = VertexArray()
        self.vao.bind()

        self.program.u['max_delay'](self.MAX_DELAY)

        eye, target, up = T.vec3(0, -10, 25), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        glDisable(GL_DEPTH_TEST)
        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_BLEND]:
            glEnable(p)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        super().paintGL()
        self.program.use()
        t = Time.time
        self.program.u['time'](t)
        N = int(max(min(Time.time - 10, 120)**3, 1))
        self.program.u['pointsize'](100.0 / pow(N, 1./3))
        glDrawArrays(GL_POINTS, 0, N)
        glFlush()

if __name__ == '__main__':
    import sn.gl.debug
    sn.gl.debug.logOnShaderVariables(True)

    from PyQt5.QtGui import QWindow

    app = Application()
    widget = RT1(None)
    widget.windowHandle().setVisibility(QWindow.FullScreen)
    widget.show()
    app.startTimer(timeout = 1000/60, onTick = widget.onTick)
    app.run()
