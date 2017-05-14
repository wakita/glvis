import logging
import numpy as np
from typing import Type
from PyQt5 import (QtGui, QtOpenGL)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QWindow
from OpenGL.GL import *
from . import *
from ..gl.geometry import t3d as T
from .application import Application
from .window import Window


class GLWidget(QtOpenGL.QGLWidget):

    format = QtOpenGL.QGLFormat()
    format.setVersion(4, 5)
    format.setProfile(QtOpenGL.QGLFormat.CoreProfile)
    format.setSampleBuffers(True)
    format.setStereo(False)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(self.format, parent)
        self.parent = parent
        self.time = Time.time
        self.nextFPS = self.time + 1
        self.frames = 0
        self.fps = 0

    def minimumSizeHint(self) -> QSize:
        return QSize(800, 600)

    def initializeGL(self):
        super().initializeGL()
        GLWidget.print_gl_info() if not self.parent else None
        glClearColor(.0, .0, .0, 1)

    def resizeGL(self, w: int, h: int):
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)

    def paintGL(self):
        self.time = t = Time.time
        if t > self.nextFPS:
            self.fps = self.frames
            logging.info('Frames/sec = {0}'.format(self.fps))
            self.nextFPS = t + 1
            self.frames = 0
        self.frames = self.frames + 1
        super().paintGL()
        glClear(GL_COLOR_BUFFER_BIT)

    def on_tick(self):
        self.updateGL()

    keyPressEvent = Window.keyPressEvent

    @classmethod
    def print_gl_info(cls, fmt : QtGui.QSurfaceFormat = None):
        profiles = ['No profile', 'Core profile', 'Compatibility profile']
        if fmt is None:
            fmt = QtGui.QOpenGLContext.currentContext().format()
        logging.info('{0:8} {1}.{2}'.format('Version',  fmt.majorVersion(), fmt.minorVersion()))
        logging.info('{0:8} {1}'    .format('Profile',  profiles[fmt.profile()]))
        logging.info('{0:8} {1}'    .format('Vendor',   glGetString(GL_VENDOR).decode('utf-8')))
        logging.info('{0:8} {1}'    .format('Renderer', glGetString(GL_RENDERER).decode('utf-8')))
        logging.info('{0:8} {1}\n'  .format('GLSL',     glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')))

    @classmethod
    def start(cls, fullscreen=False, timeout=1000/60):
        app = Application()
        widget = cls()
        widget.show()
        app.startTimer(timeout=timeout, on_tick=widget.on_tick)
        # if fullscreen: app.activeWindow().setVisibility(QWindow.FullScreen)
        if fullscreen:
            widget.windowHandle().setVisibility(QWindow.FullScreen)
        app.run()


class GLWidget3D(GLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Model: np.ndarray = np.eye(4, dtype=np.float32)
        self.View: np.ndarray = T.translate(0, 0, -3)
        self.Projection: np.ndarray = None

    def initializeGL(self, *args):
        super().initializeGL()
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w: int, h: int):
        super().resizeGL(w, h)
        if self.program.u['V']:
            self.program.u['V'](self.View)

        self.Projection = T.perspective(45., w/float(h), 0.1, 1000.)
        self.program.u['P'](self.Projection)

    def paintGL(self):
        super().paintGL()
        glClear(GL_DEPTH_BUFFER_BIT)
        self.program.u['MV'](self.View.dot(self.Model))
