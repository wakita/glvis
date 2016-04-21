from sn.gl import *
from shape import S as ShapeDemo
from sn.gl.geometry.regularpolygon import S as RegularPolygon

class W(ShapeDemo):
    def initializeGL(self):
        super().initializeGL('../regularpolygon.shaders',
                lambda program: RegularPolygon(program, .8, 5))
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
