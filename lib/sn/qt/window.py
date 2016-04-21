from PyQt5 import QtCore, QtWidgets

class Window(QtWidgets.QMainWindow):
    _time = QtCore.QTime()
    _timer = None

    @property
    def time(self):
        return self._time.elapsed() / 1000.
    _time.start()

    def __init__(self, title = 'A Window'):
        super(Window, self).__init__(None)
        self.setWindowTitle(title)
        self.show()

    def keyPressEvent(self, ev):
        k = ev.key()
        if k == QtCore.Qt.Key_Escape or k == QtCore.Qt.Key_Q:
            self.close()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window(title = 'A Test Window')
    sys.exit(app.exec_())
