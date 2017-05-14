from sn.qt import *
from sn.gl import *
import sn.sn_logging as sn_logging
import sn.gl.geometry.t3d as T

from sn.gl.geometry.pointgrid import V as POINT_GRID
from sn.gl.geometry.volume import D as DEMO_WIDGET


class KW1Widget(DEMO_WIDGET):
    def __init__(self):
        super().__init__()
        self.eye = T.homogeneous(T.vec3(0.2, 1.1, 1.2))
        self.target, self.up = T.vec3(0.5, 0.6, 0.7), T.vec3(0, 1, 0)

    def initializeGL(self):
        size = 100
        super().initializeGL('kw1.shaders', lambda program: POINT_GRID(program, size))

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](800 / size)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        eye = T.cartesian(T.rotateY(np.pi / 20 * self.time).dot(self.eye))
        self.View = T.lookat(eye, self.target, self.up)
        super().paintGL()
        sn_logging.log_on_uniform_update(False)

KW1Widget.start(fullscreen=True)
