import numpy as np
from PyQt5.QtCore import QSize
from PyQt5 import (QtGui, QtOpenGL, QtWidgets)
#import OpenGL
#OpenGL.ERROR_CHEKING = True
#OpenGL.FULL_LOGGING = True
from OpenGL.GL import *
# import vispy.util.transforms as T
#from sn.gl import t3d as T
from lib import t3d as T
from .application import Application
from .window import Window
from ..gl.util import *

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
        glClearColor(.8, .8, .8, 1)

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
    def start(cls, W):
        app = Application()
        widget = W(None)
        widget.show()
        app.startTimer(timeout = 1000/60, onTick = widget.onTick)
        app.run()

class GLWidget3D(GLWidget):

    def initializeGL(self, *args):
        super().initializeGL()
        glEnable(GL_DEPTH_TEST)
        self.Model = np.eye(4, dtype=np.float32)
        self.View = T.translate(0, 0, -3)
        try:
            self.program.u['V'](self.View)
            print('Uniform[V]:\n{0}\n'.format(self.View))
        except: pass

    def resizeGL(self, w, h):
        super().resizeGL(w, h)
        self.Projection = T.perspective(45., w/float(h), 0.1, 10.)
        try:
            self.program.u['P'](self.Projection)
            print('Uniform[P]:\n{0}\n'.format(self.Projection))
        except: pass

    def paintGL(self):
        super().paintGL()
        glClear(GL_DEPTH_BUFFER_BIT)
        try:
            MV = np.dot(self.View, self.Model)
            self.program.u['MV'](MV)
            print('Uniform[MV]:\n{0}\n'.format(MV))
        except: pass
