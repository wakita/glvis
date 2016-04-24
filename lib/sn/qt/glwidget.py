import numpy as np
from PyQt5 import (QtGui, QtOpenGL, QtWidgets)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QWindow
#import OpenGL
#OpenGL.ERROR_CHEKING = True
#OpenGL.FULL_LOGGING = True
from OpenGL.GL import *
from ..gl.geometry import t3d as T
from .application import Application
from .window import Window

class GLWidget(QtOpenGL.QGLWidget):

    format = QtOpenGL.QGLFormat()
    format.setVersion(4, 5)
    format.setProfile(QtOpenGL.QGLFormat.CoreProfile)
    format.setSampleBuffers(True)
    format.setStereo(False)

    def __init__(self, parent):
        super(GLWidget, self).__init__(self.format, parent)
        self.parent = parent

    def minimumSizeHint(self):
        return QSize(800, 600)

    def initializeGL(self):
        super().initializeGL()
        if not self.parent: GLWidget.printGLInfo()
        glClearColor(.0, .0, .0, 1)

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        glViewport(0, 0, w, h)

    def paintGL(self):
        super().paintGL()
        glClear(GL_COLOR_BUFFER_BIT)

    def onTick(self): pass

    keyPressEvent = Window.keyPressEvent

    @classmethod
    def printGLInfo(cls, fmt=None):
        profiles = ['No profile', 'Core profile', 'Compatibility profile']
        if fmt == None:
            fmt = QtGui.QOpenGLContext.currentContext().format()
        print("{0:8} {1}.{2}".format('Version',  fmt.majorVersion(), fmt.minorVersion()))
        print("{0:8} {1}"    .format('Profile',  profiles[fmt.profile()]))
        print("{0:8} {1}"    .format('Vendor',   glGetString(GL_VENDOR).decode('utf-8')))
        print('{0:8} {1}'    .format('Renderer', glGetString(GL_RENDERER).decode('utf-8')))
        print('{0:8} {1}'    .format('GLSL',     glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')))
        print()

    @classmethod
    def start(cls, W, fullscreen=False, timeout=1000/60):
        app = Application()
        widget = W(None)
        widget.show()
        app.startTimer(timeout = timeout, onTick = widget.onTick)
        #if fullscreen: app.activeWindow().setVisibility(QWindow.FullScreen)
        if fullscreen: widget.windowHandle().setVisibility(QWindow.FullScreen)
        app.run()

class GLWidget3D(GLWidget):

    Model = np.eye(4, dtype=np.float32)
    View = T.translate(0, 0, -3)

    def initializeGL(self, *args):
        super().initializeGL()
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        self.program.u['V'](self.View)

        self.Projection = T.perspective(45., w/float(h), 0.1, 1000.)
        self.program.u['P'](self.Projection)

    def paintGL(self):
        super().paintGL()
        glClear(GL_DEPTH_BUFFER_BIT)
        self.program.u['MV'](self.View.dot(self.Model))
