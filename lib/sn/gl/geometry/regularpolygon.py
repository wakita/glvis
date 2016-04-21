import os.path
from math import cos, sin
from .. import *
from .shape import S as Shape
from .shape import D as Demo

class S(Shape):

    def __init__(self, program, r, nVerts):
        super().__init__(program)
        self.nVerts = nVerts

        v = np.zeros((nVerts + 1) * 2, dtype=np.float32)
        for i in range(nVerts + 1):
            theta = np.pi * 2 * i / nVerts
            v[i*2 : i*2+2] = r * cos(theta), r * sin(theta)

        position_vs = program.a['position_vs'].loc
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)
        glVertexAttribPointer(position_vs, 2, GL_FLOAT, GL_FALSE, 8, None)
        glEnableVertexAttribArray(position_vs)

    def render(self):
        super().render()
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.nVerts + 1)

class D(Demo):
    def initializeGL(self):
        shaderpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'regularpolygon.shaders')
        super().initializeGL(shaderpath,
                lambda program: S(program, .8, 5))
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
