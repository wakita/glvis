from PyQt5.QtCore import QSize
from PyQt5 import (QtGui, QtOpenGL, QtWidgets)
from OpenGL.GL import *
from vispy.util.transforms import perspective

class GLWidget(QtOpenGL.QGLWidget):

    format = QtOpenGL.QGLFormat()
    format.setVersion(4, 5)
    format.setProfile(QtOpenGL.QGLFormat.CoreProfile)
    format.setSampleBuffers(True)

    def __init__(self, parent):
        super(GLWidget, self).__init__(parent)

    def minimumSizeHint(self):
        return QSize(800, 600)

    def initializeGL(self):
        glClearColor(.8, .8, .8, 1)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        self.Projection = perspective(45., w/float(h), 1., 1000.)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

    @classmethod
    def printGLInfo(cls, fmt=None):
        profiles = ['No profile', 'Core profile', 'Compatibility profile']
        if fmt == None:
            fmt = QtGui.QOpenGLContext.currentContext().format()
        ver = fmt.version()
        print("{0:8} {1}.{2}".format('Version', ver[0], ver[1]))
        print("{0:8} {1}"    .format('Profile', profiles[fmt.profile()]))
        print("{0:8} {1}"    .format('Vendor', glGetString(GL_VENDOR).decode('utf-8')))
        print('{0:8} {1}'    .format('Renderer', glGetString(GL_RENDERER).decode('utf-8')))
        print('{0:8} {1}'    .format('GLSL', glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')))

if __name__ == '__main__':
    import sys
    from sn.gl.window import Window
    from sn.gl.program import Program

    class AGLWidget(GLWidget):
        W = 600; H = 300

        def __init__(self, parent):
            super(AGLWidget, self).__init__(parent)

        def onTick(self):
            pass

    app = QtWidgets.QApplication(sys.argv)
    window = GLWidget(None)
    window.show()
    window.printGLInfo()

    sys.exit(app.exec_())
