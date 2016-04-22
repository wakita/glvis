#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QGridLayout, QWidget)
from sn.qt import (Application, GLWidget, Window)

class SB03(GLWidget):

    def __init__(self, parent, width=200, height=200):
        super().__init__(parent)
        self._width = width; self._height = height

    def minimumSizeHint(self): return QtCore.QSize(self._width, self._height)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

def start(Widget):
    app = Application()
    widget = Widget(None)
    widget.show()
    app.startTimer(timeout = 1000/60, onTick = widget.onTick)
    app.run()

if __name__ == '__main__':
    import sb03a, sb03b, sb03c, sb03d, sb03e, sb03f, sb03g

    app = Application()
    app.startTimer(1000/60)

    w = SB03(None)
    grid = QGridLayout(w)
    for r, c, W in [
            (1, 0, sb03a.W), (1, 1, sb03b.W), (1, 2, sb03c.W),
            (2, 0, sb03d.W), (2, 1, sb03e.W), (2, 2, sb03f.W),
            (3, 1, sb03g.W) ]:
        wx = W(w, width=400, height=300)
        Application.addOnTick(wx.onTick)
        grid.addWidget(wx, r, c)
    w.setLayout(grid)
    w.show()

    import sys
    sys.exit(app.exec_())
