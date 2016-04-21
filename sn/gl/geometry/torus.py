from math import sin, cos
from sn.gl.geometry.volume import V as Volume

class V(Volume):

    program = None

    def __init__(self, program, r1, r2, sides, rings):
        '''
        r1: inner radius
        r2: outer radius
        sides: ???
        rings: ???'''

        super().__init__(program)

        nV = sides * (rings + 1)
        TWO_PI = np.pi * 2

        V = np.zeros(3 * nV, dtype = np.float32)
        N = np.zeros(3 * nV, dtype = np.float32)
        T = np.zeros(2 * nV, dtype = np.float32)

        p = 0, q = 0
        for ring in range(rings):
            u = TWO_PI * ring / rings
            cu, su = cos(u), sin(u)
            rx, rz = r1 + r2 * cu, r2 * su
            nx, nz = cu, su
            for side in range(sides):
                v = TWO_PI * side / sides
                cv, sv = cos(v), sin(v)
                V[p:p+3] = rx * cv, rx * sv, rz
                N[p:p+3] = nx * cv, nx * sv, nz
                T[q:q+2] = u / TWO_PI, v / TwoPi
                p += 3; q += 2

        faces = sides * rings
        E = np.zeros(6 * sides * rings, dtype = np.uint16)
        p = 0
        for ring in range(rings):
            r0 = ring * sides
            r1 = (ring + 1) * sides
            for side in range(sides):
                i00, i01 = r0 + side, r0 + (side + 1) % sides
                i10, i11 = r1 + side, r1 + (side + 1) % sides
                E[p:p+3] = i00, i10, i11; p += 3
                E[p:p+3] = i11, i01, i00; p += 3

        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, V.nbytes, V, GL_STATIC_DRAW)
        position_l = program.A['position_vs']
        glVertexAttribPointer(position_l, 3, GL_FLOAT, GL_FALSE, 0, None)

        if program.A['normal_vs']:
            glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
            glBufferData(GL_ARRAY_BUFFER, N.nbytes, N, GL_STATIC_DRAW)
            normal_l = program.A['normal_vs']
            glVertexAttribPointer(normal_l, 3, GL_FLOAT, GL_FALSE, 0, None)

        if program.A['texture_l']:
            glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
            glBufferData(GL_ARRAY_BUFFER, T.nbytes, T, GL_STATIC_DRAW)
            texture_l = program.A['texture_vs']
            glVertexAttribPointer(texture_l, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, E.nbytes, E, GL_STATIC_DRAW)
