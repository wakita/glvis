import os.path
from .. import *
from .volume import V as Volume
from .volume import D as Demo
import sn.gl.geometry.t3d as T


class V(Volume):

    program = None

    def __init__(self, program, S, colors=None):
        super().__init__(program)

        S = S + 1
        N = self.N = S * S
        vs = np.array(range(S)) * 2. / (S - 1) - 1.

        positions = np.array([(x, 0, z) for x in vs for z in vs], dtype=np.float32).flatten()
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_STATIC_DRAW)

        position_l = program.a['position_vs'].loc
        glVertexAttribPointer(position_l, int(len(positions) / N), GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position_l)

        normals = np.array([(0, 1, 0) for x in vs for z in vs], dtype=np.float32).flatten()
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)

        normal_l = program.a['normal_vs'].loc
        glVertexAttribPointer(normal_l, int(len(normals) / N), GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(normal_l)

        elements = np.zeros(6 * S * S, dtype=np.uint32)
        p = 0
        for i in range(S-1):
            r0, r1 = i * S, (i+1) * S
            for j in range(S-1):
                p00, p10 = r0  + j,  r1 + j
                p01, p11 = p00 + 1, p10 + 1
                elements[p:p+6] = [p00, p11, p10, p00, p01, p11]
                p += 6
        print(len(elements), elements)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elements.nbytes, elements, GL_STATIC_DRAW)

        self.unbind()

    def render(self):
        super().render()
        glDrawElements(GL_TRIANGLES, 6 * self.N, GL_UNSIGNED_INT, None)


class D(Demo):

    def initializeGL(self):
        S = 30
        shader_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plane.shaders')
        super().initializeGL(shader_path, lambda program: V(program, S))

        eye, target, up = T.vec3(1.5, 0.3, 2.5), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)
