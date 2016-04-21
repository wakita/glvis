import os.path
from .. import *
from .shape import S as Shape
from .shape import D as Demo

class S(Shape):
    def __init__(self, program):
        super().__init__(program)

        position_vs = program.a['position_vs'].loc
        v = np.array([0, 0], dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)
        glVertexAttribPointer(position_vs, 2, GL_FLOAT, GL_FALSE, 8, None)
        glEnableVertexAttribArray(position_vs)

    def render(self):
        super().render()
        glDrawArrays(GL_POINTS, 0, 1)

class D(Demo):
    def initializeGL(self):
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        shaderpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'point.shaders')
        super().initializeGL(shaderpath, S)
        self.program.u['pointsize'](20)
