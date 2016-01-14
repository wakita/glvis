#!/usr/bin/env python3

from PyQt5 import QtGui, QtOpenGL, QtWidgets
from PyQt5.QtOpenGL import QGLWidget

from OpenGL.GL import *

class GLPlotWidget(QGLWidget):
    width, height = 600, 600

    def __init__(self, format = None):
        super(GLPlotWidget, self).__init__(format, None)

    c = [1.0, 0.0, 0.0, 1.0]
    def initializeGL(self):
        c = self.c
        glClearColor(c[0], c[1], c[2], c[3])

    def paintGL(self):
        print('paintGL')
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
            self.setWindowTitle('sb02b: 複数の値をシェーダに送る')
            self.setCentralWidget(self.widget)
            self.show()

    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()
