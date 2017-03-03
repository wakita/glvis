import math

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget

from sn.qt import *
from sn.gl import *
#from sn.gl.geometry.volume import D as DemoWidget

from glwindow import Ui_MainWindow


class Application(QApplication):
    _timer = None

    def __init__(self, argv):
        super().__init__(argv)
        if not Application._timer:
            timer = Application._timer = QtCore.QTimer(self)
        timer.start(1000/60.)

    @classmethod
    def addOnTick(cls, f):
        if cls._timer: cls._timer.timeout.connect(f)


class MyWidget(GLWidget):
    program = None

    def __init__(self, parent, width=200, height=300):
        super().__init__(parent)
        self._width = width; self._height = height

    def minimuSizeHint(self):
        return QtCore.QSize(self._width, self._height)

    def onTick(self):
        self.updateGL()

    def initializeGL(self):
        self.program = self.program or Program('kw8e.shaders')
        self.va = VertexArray()

    def paintGL(self):
        super().paintGL()

        program = self.program
        program.use()
        t = Time.time
        program.a['offset_vs'](math.cos(t) / 2, math.sin(t) / 2)
        program.u['color_u']((math.cos(t) + 1) / 2, (math.sin(t) + 1) / 2)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glFlush()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    import sys
    app = Application(sys.argv)

    main = MainWindow()
    main.show()
    GLWidget.printGLInfo()
    Application.addOnTick(main.ui.glView.onTick)
    main.ui.quitButton.clicked.connect(lambda *args: app.quit())
    sys.exit(app.exec_())
