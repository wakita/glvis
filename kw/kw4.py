from ctypes import *
import sys

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as DEMO
from sn.gl.geometry.points import V as POINTS
import sn.gl.geometry.T3D as T

import sn.gl.debug
sn.gl.debug.logOnShaderVariables(True)
sn.gl.debug.logOnSetUniform(False)
logging = True


class SSB(Structure):
    _fields_ = [('clicked_x', c_uint), ('clicked_y', c_uint),
                ('pick_z', c_float),   ('pick_lock', c_int),
                ('pick_id', c_int)]


class KW4(DEMO):

    def __init__(self, widget):
        super().__init__(widget)
        self.should_handle_pick = False

        s = self.S = 5
        vvals = np.array(range(s)) * 2. / (s - 1) - 1.
        self.points = [(x, y, z) for x in vvals for y in vvals for z in vvals]

        self.click_buffer = 0

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        points = self.points
        super().initializeGL('kw4.shaders', lambda _program: POINTS(_program, points))

        eye, target, up = T.vec3(0, 0, 3), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE]:
            glEnable(p)
        self.program.u['pointsize'](800 / self.S)

        # Prepare an application-side SSB region
        self.click_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.click_buffer)
        # Bind the 0'th binding point of the SSB to the application-side SSB area
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, self.click_buffer)
        # Allocate a storage area on the application
        ssb = SSB()
        ssb.clicked_x = 100
        # Create and initialize the application-side SSB area
        glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(ssb), pointer(ssb), GL_DYNAMIC_READ)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    def paintGL(self):
        super().paintGL()
        self.handle_pick()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        pos = ev.pos()

        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.click_buffer)
        # Map the GPU-side shader-storage-buffer on the application, allowing for write-only access
        ssb = cast(glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_WRITE_ONLY), POINTER(SSB)).contents
        # Save the clicked location information
        ssb.clicked_x, ssb.clicked_y = pos.x(), pos.y()
        # Initialize fields
        ssb.pick_z = float('-inf')         # Initially -infty
        ssb.pick_lock, ssb.pick_id = 0, -1  # Initially UNLOCKED (c.f., Unlocked@kw4.shader)
        if logging:
            print('float.min: {0}'.format(sys.float_info.min))
            print('Mouse released: pos: ({0}, {1}), z: {2}'.format(ssb.clicked_x, ssb.clicked_y, ssb.pick_z))
        # Unmap the SSB
        glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
        # Tell the next rendering cycle to perform pick-identification
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
        self.should_handle_pick = True

    def handle_pick(self):
        if self.should_handle_pick:
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.click_buffer)
            # Map the GPU-side shader-storage-buffer on the application, allowing for read-only access
            ssb = cast(glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_READ_ONLY), POINTER(SSB)).contents
            if logging:
                print('SSB: ({0}, {1})'.format(ssb.clicked_x, ssb.clicked_y))
                print('id: {0} (z: {1})'.format(ssb.pick_id, ssb.pick_z))
            # Unmap the SSB
            glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
            # Pick-identification finished
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
            self.should_handle_pick = False

if __name__ == '__main__':
    KW4.start(KW4)
