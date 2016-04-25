import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import QTimer
from kw.kw1 import KW8Widget

class StatusBar(QMainWindow):
    def __init__(self):
        super(StatusBar, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 600, 200, 200)
        self.setWindowTitle('Status bar test')
        glWidget = self.glWidget = KW8Widget(self)
        self.setCentralWidget(glWidget)
        self.show()
        self.windowHandle().setVisibility(QWindow.FullScreen)

        statusTimer = QTimer(self)
        statusTimer.timeout.connect(self.laptime)
        statusTimer.start(1000)

        glTimer = QTimer(self)
        glTimer.timeout.connect(glWidget.onTick)
        glTimer.start(1000/60)

    def laptime(self):
        self.statusBar().showMessage('FPS = {0}'.format(self.glWidget.fps))

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StatusBar()
    sys.exit(app.exec_())
