from ctypes import *
import logging
import sys

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as DEMO
from sn.gl.geometry.points import V as POINTS
import sn.gl.geometry.t3d as T

S = 5


class SSB(Structure):
    _fields_ = [('clicked_x', c_uint), ('clicked_y', c_uint),
                ('pick_z', c_float),   ('pick_lock', c_int),
                ('pick_id', c_int)]


class KW4(DEMO):
    def __init__(self):
        super().__init__()
        self.clicked_pos = None
        self.click_buffer = 0
        self.fragment = dict()
        '@type: Dict[str, int]'

    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(600, 600)

    def initializeGL(self):
        vvals = np.array(range(S)) * 2. / (S - 1) - 1.
        points = [(x, y, z) for x in vvals for y in vvals for z in vvals]
        super().initializeGL('kw4.shaders', lambda _program: POINTS(_program, points))

        eye, target, up = T.vec3(0, 0, 3), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_BLEND]:
            glEnable(p)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.program.u['pointsize'](1000 / S)

        # Prepare an application-side SSB region
        self.click_buffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.click_buffer)
        # Bind the 0'th binding point of the SSB to the application-side SSB area
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, self.click_buffer)
        # Allocate a storage area on the application
        ssb = SSB()
        # Create and initialize the application-side SSB area
        glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(ssb), pointer(ssb), GL_DYNAMIC_READ)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

        for f in 'paint pick'.split():
            self.fragment[f] = glGetSubroutineIndex(self.program._program, GL_FRAGMENT_SHADER, f)
        logging.debug(self.fragment)

    def paintGL(self):
        self.geometry.use()
        self.handle_pick_before()
        pick_or_paint = self.fragment['pick' if self.should_handle_pick() else 'paint']
        glUniformSubroutinesuiv(GL_FRAGMENT_SHADER, 1, pick_or_paint)
        super().paintGL()
        self.handle_pick_after()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        self.clicked_pos = ev.pos()

    def should_handle_pick(self):
        return self.clicked_pos is not None

    def handle_pick_before(self):
        if self.should_handle_pick():
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.click_buffer)
            # Map the GPU-side shader-storage-buffer on the application, allowing for write-only access
            ssb = cast(glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_WRITE_ONLY), POINTER(SSB)).contents
            # Save the clicked location information
            pos = self.clicked_pos
            ssb.clicked_x, ssb.clicked_y = pos.x(), pos.y()
            # Initialize fields
            ssb.pick_z = float('-inf')         # Initially -infty
            ssb.pick_lock, ssb.pick_id = 0, -1  # Initially UNLOCKED (c.f., Unlocked@kw4.shader)
            logging.info('float.min: {0}'.format(sys.float_info.min))
            logging.info('Mouse released: pos: ({0}, {1}), z: {2}'.format(ssb.clicked_x, ssb.clicked_y, ssb.pick_z))
            # Unmap the SSB
            glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
            # Tell the next rendering cycle to perform pick-identification
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    def handle_pick_after(self):
        if self.should_handle_pick():
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.click_buffer)
            # Map the GPU-side shader-storage-buffer on the application, allowing for read-only access
            ssb = cast(glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_READ_ONLY), POINTER(SSB)).contents
            logging.info('SSB: ({0}, {1})'.format(ssb.clicked_x, ssb.clicked_y))
            logging.info('id: {0} (z: {1})'.format(ssb.pick_id, ssb.pick_z))
            # Unmap the SSB
            glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
            # Pick-identification finished
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
            self.clicked_pos = None

KW4.start()
