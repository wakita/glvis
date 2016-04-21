from sn.gl import *
from shape import S as ShapeDemo
from sn.gl.geometry.point import S as Point

class W(ShapeDemo):
    def initializeGL(self):
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        super().initializeGL('../point.shaders', Point)
        self.program.u['pointsize'](20)
