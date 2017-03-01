import os.path
from .. import *
from .shape import S as Shape
from .shape import D as Demo
import sn.gl.geometry.t3d as T

class S(Shape):

    program = None

    def __init__(self, program, points, edges, colors=None):
        super().__init__(program)

        print(points)
        print(edges)

        self.N = len(points)
        v = np.array(points, dtype=np.float32).flatten()

        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

        position_l = program.a['position_vs'].loc
        glVertexAttribPointer(position_l, int(len(v) / self.N), GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position_l)

        self.E = len(edges)
        if (len(edges) < 1 << 16):
            self.e = np.array(edges, dtype=np.uint16).flatten()
            self.edgetype = GL_UNSIGNED_SHORT
        else:
            self.e = np.array(edges, dtype=np.uint32).flatten()
            self.edgetype = GL_UNSIGNED_INT

        if colors:
            c = np.array(colors, dtype=np.float32).flatten()
            glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
            glBufferData(GL_ARRAY_BUFFER, c.nbytes, c, GL_STATIC_DRAW)

            color_l = program.a['color_vs'].loc
            glVertexAttribPointer(color_l, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(color_l)

        self.unbind()

    def render(self):
        super().render()
        glDrawElements(GL_LINES, self.E, self.edgetype, self.e)

class D(Demo):

    def initializeGL(self):
        N = 36
        points = [(0, 0, 0) ] + [(np.cos(2 * np.pi * t / N), np.sin(2 * np.pi * t / N), 0) for t in range(N)]
        edges = []
        for i in range(N):
            edges += [0, i+1]
        shaderpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lines.shaders')
        super().initializeGL(shaderpath, lambda program: S(program, points, edges))

        eye, target, up = T.vec3(0, 0, 2), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

    def resizeGL(self, w, h):
        super().resizeGL(w, h)

    def paintGL(self):
        super().paintGL()