from .. import *
from .volume import V as Volume

class V(Volume):

    program = None

    def __init__(self, program, S):
        super().__init__(program)

        N = self.N = S * S * S

        vvals = [ s / (S-1) - 0.5 for s in range(S) ]
        points = [ (x, y, z) for x in vvals for y in vvals for z in vvals ]
        v = np.array(points, dtype=np.float32).flatten()

        v = np.zeros(3 * N, dtype=np.float32)
        p = 0
        for x in range(S):
            for y in range(S):
                for z in range(S):
                    v[p:p+3] = x, y, z
                    p += 3
        v = v * 2 / float(S - 1) - 1
        print(v.shape, v)

        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

        position_l = program.A['position_vs']
        glVertexAttribPointer(position_l, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position_l)
        self.unbind()

    def render(self):
        super().render()
        glDrawArrays(GL_POINTS, 0, self.N)
