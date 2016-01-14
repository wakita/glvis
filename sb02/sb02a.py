#!/usr/bin/env python

from PyQt5 import QtGui, QtOpenGL, QtWidgets
from PyQt5.QtOpenGL import QGLWidget

from OpenGL.GL import *

class GLPlotWidget(QGLWidget):
    width, height = 600, 600

    def __init__(self, format = None):
        super(GLPlotWidget, self).__init__(format, None)

    def initializeGL(self):
        glClearColor(1.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glFlush()

if __name__ == '__main__':
    import sys

    class TestWindow(QtWidgets.QMainWindow):
        def __init__(self, parent = None):
            super(TestWindow, self).__init__(parent)

            glformat = QtOpenGL.QGLFormat()
            glformat.setVersion(4, 5)
            glformat.setProfile(QtOpenGL.QGLFormat.CoreProfile)
            glformat.setSampleBuffers(True)
            self.widget = GLPlotWidget(glformat)

            self.setGeometry(100, 100, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.setWindowTitle('sb02a')
            self.show()

    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()
