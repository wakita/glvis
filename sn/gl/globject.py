from ctypes import c_void_p
import numpy as np
from OpenGL.GL import *

class _GLObject_(object):
    def create(self): pass
    def delete(self): pass

    def __del__(self):  self.delete()
    def __init__(self, *args, **kwargs): self.create(*args, **kwargs)

class VertexArray(_GLObject_):
    def create(self):
        self._h = glGenVertexArrays(1)
        self.bind()
        self.enable()

    def delete(self):
        if self._h and bool(glDeleteVertexArrays):
            h = self._h; self._h = None
            glDeleteVertexArrays(1, [h])

    def bind(self):
        glBindVertexArray(self._h)

    def unbind(self):
        glBindVertexArray(0)

    def enable(self):
        glEnableVertexAttribArray(self._h)

    def disable(self):
        glDisableVertexAttribArray(self._h)

class VertexBuffer(_GLObject_):
    def __init__(self, buf):
        self._buffer = buf

    @classmethod
    def create(self, n):
        return [VertexBuffer(buf) for buf in glGenBuffers(n)]

    def delete(self):
        if self._buffer and bool(glDeleteBuffers):
            buffer = self._buffer; self._buffer = None
            glDeleteBuffers(1, [buffer])

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self._buffer)

    _np2glType = dict()
    for npT, glT in [(np.float64, GL_DOUBLE), (np.float32, GL_FLOAT), (np.int32, GL_INT),
            (np.int16, GL_SHORT), (np.int8, GL_UNSIGNED_BYTE), (np.uint8, GL_BYTE)]:
        _np2glType[np.dtype(npT)] = glT

    def allocate(self, data, usage):
        # print('data: {0}, usage: {1}'.format(data.nbytes, usage))
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, usage)

    def initialize(self, data, usage, normalized=GL_FALSE, stride=0, offset=None):
        self.bind()
        self.allocate(data, usage)

    def dataFormat(self, elem, nelems, normalized=GL_FALSE, stride=0, offset=None):
        t = self._np2glType[elem.dtype]
        # print('dataFormat: buffer: {0}, bytes: {1}, type: {2}, offset: {3}'.format(self._buffer, elem.nbytes, t, offset))
        glVertexAttribPointer(self._buffer, nelems, t, normalized, stride, offset)

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
