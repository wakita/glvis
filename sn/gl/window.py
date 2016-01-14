from PyQt5 import QtCore, QtWidgets

class Window(QtWidgets.QMainWindow):
    _time = QtCore.QTime()
    _timer = None

    @property
    def time(self):
        return self._time.elapsed() / 1000.
    _time.start()

    def __init__(self, Widget = None, title = 'A Window'):
        super(Window, self).__init__(None)

        timer = self._timer = QtCore.QTimer(self)

        if Widget != None:
            self.widget = Widget(self)
            self.setGeometry(100, 100, self.widget.W, self.widget.H)
        else:
            self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle(title)

        timer.start(1000 / 60)

        self.show()

    def keyPressEvent(self, ev):
        k = ev.key()
        if k == QtCore.Qt.Key_Escape or k == QtCore.Qt.Key_Q:
            self.close()

if __name__ == '__main__':
    import sys
    from sn.gl.glwidget import GLWidget

    app = QtWidgets.QApplication(sys.argv)
    window = Window(Widget = GLWidget, title = 'A Test Window')
    sys.exit(app.exec_())
