from sn.gl import *
from sn.qt import *
import lib.t3d as T
vec3 = T.vec3

from shape import S as ShapeDemo

class W(ShapeDemo, GLWidget3D):
    def __init__(self, parent):
        super(W, self).__init__(parent)

    def initializeGL(self, shaderpath, Geometry):
        super(W, self).initializeGL(shaderpath, Geometry)
        eye, target, up = vec3(0, 0, 5), vec3(0, 0, 0), vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)
        try:
            self.program.u['worldlight'] = normalize(vec3(5, 10, 20))
            print('U[worldlight] = {0}\n'.format(normalize(vec3(5, 10, 20))))
        except: pass

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        self.Projection = T.perspective(45, w/float(h), 1., 200.)
