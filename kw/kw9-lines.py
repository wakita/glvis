from sn.gl import *
import sn.gl.debug

from sn.gl.geometry.lines import S as Lines
from sn.gl.geometry.lines import D as DemoWidget


class KW9Widget(DemoWidget):
    def initializeGL(self):

        super().initializeGL(None, lambda program: Lines(program))

        for p in [ GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND ]:
            glEnable(p)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    def paintGL(self):
        super().paintGL()

    def onTick(self):
        self.updateGL()

DemoWidget.start(DemoWidget)
