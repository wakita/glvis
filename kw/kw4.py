from ctypes import *
import sys

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
from sn.gl.geometry.points import V as Points
import sn.gl.geometry.T3D as T

import sn.gl.debug
sn.gl.debug.logOnShaderVariables(True)
sn.gl.debug.logOnSetUniform(False)
logging = True


class SSB(Structure):
    _fields_ = [('clicked_x', c_uint), ('clicked_y', c_uint),
                ('pick_z', c_float),   ('pick_lock', c_int),
                ('pick_id', c_int)]


class KW4(Demo):

    def __init__(self, W):
        super().__init__(W)
        self.should_handle_mouse_click = False

        s = self.S = 5
        vvals = np.array(range(s)) * 2. / (s - 1) - 1.
        self.points = points = [(x, y, z) for x in vvals for y in vvals for z in vvals]

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        points = self.points
        super().initializeGL('kw4.shaders', lambda program: Points(program, points))

        eye, target, up = T.vec3(0, 0, 3), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](800 / self.S)
        self.program.u['pick_color'](*T.vec4(1, 0, 0, 1))
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Prepare an application-side SSB region
        ssbo = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, ssbo)
        # Allocate a storage area on the application
        ssb = SSB()
        # Create and initialize the application-side SSB area
        glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(ssb), pointer(ssb), GL_DYNAMIC_READ)
        # Bind the 0'th binding point of the SSB to the application-side SSB area
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, ssbo)

    def paintGL(self):
        super().paintGL()
        self.handleMouseClick()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        pos = ev.pos()

        # Map the GPU-side shader-storage-buffer on the application, allowing for write-only access
        buf = glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_WRITE_ONLY)
        # Virtualize the SSB as a Python ctypes object
        ssb = cast(buf, POINTER(SSB)).contents
        # Save the clicked location information
        ssb.clicked_x = pos.x(); ssb.clicked_y = pos.y()
        # Inifialize fields
        ssb.pick_z    = -float('inf') # Initially -infty
        ssb.pick_lock = 0             # Initially unlocked (c.f., Unlocked@kw4.shader)
        ssb.pick_id   = -1            # Initially unknown
        if logging:
          print('float.min: {0}'.format(sys.float_info.min))
          print('Mouse released: pos: ({0}, {1}), z: {2}'.format(ssb.clicked_x, ssb.clicked_y, ssb.pick_z))
        # Unmap the SSB
        glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
        # Tell the next rendering cycle to perform pick-identification
        self.should_handle_mouse_click = True

    def handleMouseClick(self):
        if self.should_handle_mouse_click:
            # Map the GPU-side shader-storage-buffer on the application, allowing for read-only access
            buf = glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_READ_ONLY)
            # Virtualize the SSB as a Python ctype object
            ssb = cast(buf, POINTER(SSB)).contents
            if logging:
              print('id: {0} (z: {1})'.format(ssb.pick_id, ssb.pick_z))
            # Unmap the SSB
            glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
            # Pick-identification finished
            self.should_handle_mouse_click = False

if __name__ == '__main__':
    KW4.start(KW4)