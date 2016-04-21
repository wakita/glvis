from sn.gl import *
from volume import W as VolumeDemo
from sn.gl.geometry.pointgrid import V as PointGrid
from lib import t3d as T

class W(VolumeDemo):

    def initializeGL(self):
        S = 2
        super().initializeGL('../pointgrid.shaders',
                lambda program: PointGrid(program, S))
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        try:
            self.program.u['pointsize'](300/S)
            print('Pointgrid:initializeGL: Uniform[pointsize] = {0}'.format(300/S))
        except: pass

    def resizeGL(self, w, h):
        super().resizeGL(w, h)

    def paintGL(self):
        super().paintGL()
        MVP = np.dot(self.Projection, np.dot(self.View, self.Model))
        [ print(T.vec3(*v), T.cartesian(np.dot(MVP, T.homogeneous(T.vec3(*v)))))
          for v in [ (0, 0, 0), (1, 1, 1), (-1, -1, -1) ] ]
