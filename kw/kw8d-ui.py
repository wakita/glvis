from PyQt5.QtWidgets import QApplication, QWidget

from echo import Ui_Echo


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Echo()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.add)

    def add(self):
        self.ui.textBrowser.append(self.ui.input.text())
        self.ui.input.clear()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
