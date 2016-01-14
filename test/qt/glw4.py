import math
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QGridLayout, QWidget)
from PyQt5.QtGui import QColor
from sn.qt import (Application, GLWidget, Time, Window)
from OpenGL.GL import *

class GLW(GLWidget):
    serial = 0

    def __init__(self, parent):
        super(GLW, self).__init__(parent)
        self.id = self.__class__.serial
        self.__class__.serial = self.__class__.serial + 1

    def minimumSizeHint(self): return QSize(200, 200)

    def initializeGL(self):
# 当初、__init__のなかでタイマー動作を設定していたが、タイミングバグを引き起こしていた。
# 原因は、OpenGLの初期化が完了するまえにタイマーイベントを拾って、描画してしまうことのようだ。
# paintGLにタイマー動作の設定コードを移動することで対応。
        Application.addOnTick(self.tick)

    def paintGL(self):
        theta = Time.time / 10
        c = QColor.fromHsvF(math.fmod(self.id / 25. + theta, 1), 1., .5)
        glClearColor(c.redF(), c.greenF(), c.blueF(), .5)
        super(self.__class__, self).paintGL()

    def tick(self):
        self.updateGL()

app = Application()
app.startTimer(timeout=1000/60)
window = Window(None)
widget = QWidget(window)
window.setCentralWidget(widget)
grid = QGridLayout(widget)
for i in range(25):
    grid.addWidget(GLW(widget), i/5, i%5)
widget.setLayout(grid)
window.show()
app.run()
