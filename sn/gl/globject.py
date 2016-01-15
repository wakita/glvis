from OpenGL.GL import *

class GLObject(object):
    def create(self): pass
    def delete(self): pass

    def __del__(self):  self.delete()
    def __init__(self, *args, **kwargs): self.create(*args, **kwargs)

class VertexArray(GLObject):
    def create(self):
        self._h = glGenVertexArrays(1)

    def delete(self):
        if self._h and bool(glDeleteVertexArrays):
            h = self._h; self._h = None
            glDeleteVertexArrays(1, [h])

    def bind(self):
        glBindVertexArray(self._h)

class VertexBuffer(GLObject):
    def create(self, names):
        '''VertexBuffer('position normal color texture')'''
        names = names.split()
        self._buffers = dict(zip(names, glGenBuffers(len(names))))

    def delete(self):
        if self._buffers and bool(glDeleteBuffers):
            buffers = list(self._buffers.values()); self._buffers = None
            glDeleteBuffers(len(buffers), buffers)

    def bind(self, name):
        glBindBuffer(GL_ARRAY_BUFFER, self._buffers[name])

    def data(self, data, usage):
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, usage)

if __name__ == '__main__':
    from sn.qt import Application, GLWidget
    app = Application()

    class Widget(GLWidget):
        def initializeGL(self):
            va = VertexArray()
            va.bind()
            vbs = VertexBuffer('position normal color texture')
            vbs.bind('position')
            vbs.bind('normal')
            vbs.bind('color')
            vbs.bind('texture')

    window = Widget(None)
    window.show()
