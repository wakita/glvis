from PyQt5 import QtCore
from PyQt5.QtWidgets import (QGridLayout, QWidget)
from sn.qt import *
from sn.gl import *

class SB05(GLWidget):

    def __init__(self, parent, width=200, height=200):
        super().__init__(parent)
        self._width = width; self._height = height

    def initializeGL(self, path):
        super().initializeGL()
        self.program = self.program or Program(path)
        self.va = VertexArray()

    def minimumSizeHint(self): return QtCore.QSize(self._width, self._height)

    def onTick(self):
        self.updateGL()

    keyPressEvent = Window.keyPressEvent

def start(Widget):
    app = Application()
    widget = Widget(None)
    widget.show()
    app.startTimer(timeout = 1000/60, onTick = widget.onTick)
    app.run()

if __name__ == '__main__' and False:
    import sb05a, sb05b, sb05c, sb05d, sb05e, sb05f, sb05g

    app = Application()
    app.startTimer(1000/60)

    w = SB05(None)
    grid = QGridLayout(w)
    for r, c, W in [
            (1, 0, sb05a.W), (1, 1, sb05b.W), (1, 2, sb05c.W),
            (2, 0, sb05d.W), (2, 1, sb05e.W), (2, 2, sb05f.W),
            (3, 1, sb05g.W) ]:
        wx = W(w, width=400, height=300)
        Application.addOnTick(wx.onTick)
        grid.addWidget(wx, r, c)
    w.setLayout(grid)
    w.show()

    import sys
    sys.exit(app.exec_())
