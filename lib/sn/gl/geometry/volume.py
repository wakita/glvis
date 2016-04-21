from .. import *
from sn.qt.glwidget import GLWidget3D
from .shape import S as Shape
from .shape import D as Demo
import sn.gl.geometry.t3d as T

class V(Shape): pass

class D(Demo, GLWidget3D):
    def __init__(self, parent):
        super(D, self).__init__(parent)

    def initializeGL(self, shaderpath, Geometry):
        eye, target, up = T.vec3(0, 0, 5), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)
        super(D, self).initializeGL(shaderpath, Geometry)

        try:
            self.program.u['worldlight'] = normalize(T.vec3(5, 10, 20))
            print('U[worldlight] = {0}\n'.format(normalize(T.vec3(5, 10, 20))))
        except: pass

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        self.Projection = T.perspective(45, w/float(h), 1., 200.)
