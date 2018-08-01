from ctypes import *
import logging

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as DEMO
from sn.gl.geometry.points import V as POINTS
import sn.gl.geometry.t3d as T

S = 100


class SSB(Structure):
    _fields_ = [('clicked_x', c_uint), ('clicked_y', c_uint),
                ('pick_z', c_float),   ('pick_lock', c_int),
                ('pick_id', c_int)]


class KW4(DEMO):
    def __init__(self):
        super().__init__()
        self.clicked_pos = None
        self.click_buffer = 0

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
        allocate_ssb(0, self.click_buffer, SSB, GL_DYNAMIC_READ)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    def paintGL(self):
        self.geometry.use()
        p = self.program

        if self.should_handle_pick():
            self.handle_pick_before()
            p.F.fs.pick()
            super().paintGL()
            self.handle_pick_after()

        p.F.fs.paint()
        super().paintGL()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        self.should_handle_pick(pos=ev.pos())

    def should_handle_pick(self, pos=None):
        should_handle = self.clicked_pos is not None
        if not should_handle and pos is not None:
            logging.debug('should handle pick ...')
            self.clicked_pos = pos
            should_handle = True
        return should_handle

    def handle_pick_before(self):
        logging.debug('before - lock ssb')
        with open_ssb(self.click_buffer, SSB, GL_WRITE_ONLY) as ssb:
            # Save the clicked location information
            ssb.clicked_x, ssb.clicked_y = self.clicked_pos.x(), self.clicked_pos.y()
            # Initialize fields
            ssb.pick_z = float('-inf')         # Initially -infty
            ssb.pick_lock, ssb.pick_id = 0, -1  # Initially UNLOCKED (c.f., Unlocked@kw4.shader)
            logging.debug('clicked pos: ({}, {})'.format(ssb.clicked_x, ssb.clicked_y))

    def handle_pick_after(self):
        logging.debug('after - glBindBuffer')
        glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)
        with open_ssb(self.click_buffer, SSB, GL_READ_ONLY) as ssb:
            logging.debug('x: {}, y: {}'.format(ssb.clicked_x, ssb.clicked_y))
            logging.info('id: {} (z: {})'.format(ssb.pick_id, ssb.pick_z))
        self.clicked_pos = None

KW4.start()
