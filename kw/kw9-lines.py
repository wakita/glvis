from sn.gl import *
from sn.qt import *
from sn.gl.geometry.lines import D as LINES


class KW9Widget(LINES):
    def initializeGL(self):
        super().initializeGL()
        [glEnable(p) for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]]
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

KW9Widget.start()
