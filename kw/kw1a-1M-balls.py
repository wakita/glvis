# kw1.pyはPointGridでモデルを構成した。kw1a.pyはPointsを用いている。実質的には同じ。

from sn.qt import *
from sn.gl import *
import sn.gl.geometry.t3d as T
import sn.sn_logging as sn_logging

from sn.gl.geometry.points import V as POINTS
from sn.gl.geometry.volume import D as DEMO_WIDGET


class KW1AWidget(DEMO_WIDGET):
    def __init__(self):
        super().__init__()
        self.eye = T.homogeneous(T.vec3(0.2, 1.1, 1.2))
        self.target, self.up = T.vec3(0.5, 0.6, 0.7), T.vec3(0, 1, 0)

    def initializeGL(self):
        size = 100
        vvals = np.array(range(size)) * 2. / (size - 1) - 1.
        points = [(x, y, z) for x in vvals for y in vvals for z in vvals]
        super().initializeGL('kw1.shaders', lambda program: POINTS(program, points))

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](800/size)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        eye = T.cartesian(T.rotateY(np.pi / 20 * self.time).dot(self.eye))
        self.View = T.lookat(eye, self.target, self.up)
        super().paintGL()
        sn_logging.log_on_uniform_update(False)

KW1AWidget.start(fullscreen=True)
