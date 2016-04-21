def keyPressEvent(self, ev):
    k = ev.key()
    if k == QtCore.Qt.Key_Escape or k == QtCore.Qt.Key_Q:
        self.close()
