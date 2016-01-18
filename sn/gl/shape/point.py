from sn.gl.shape.volume import *

class Point(Volume):

    def __init__(self, program, r):
        super().__init__()
        v = np.array([0, 0, 0, r], dtype=np.float32)

        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

        position_l = program.A['position_vs']
        glVertexAttribPointer(position_l, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position_l)


    def render(self):
        self.bind()
        glPatchParameteri(GL_PATCH_VERTICES, 1)
        glDrawArrays(GL_PATCHES, 0, 1)

if __name__ == '__main__':
    from sn.qt import Application, GLWidget, Window
    from sn.gl import Program

    class W(GLWidget):

        program = None

        def __init__(self): super().__init__(None)

        def initializeGL(self):
            super().initializeGL()
            self.program = self.program or Program('point.shaders')
            self.p = Point(self.program, 50)

        def paintGL(self):
            super().paintGL()
            self.program.use()
            glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
            self.p.bind()
            self.p.render()

        keyPressEvent = Window.keyPressEvent

    app = Application()
    widget = W()
    widget.show()
    app.run()
