import sys
from PyQt5.QtWidgets import QApplication, QDialog
from dialog import Ui_Dialog


class ImageDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(ImageDialog, self).__init__()
        self.setupUi(self)

    def accept(self):
        print('Accepted')
        super().accept()

    def reject(self):
        print('Rejected')
        super().reject()

app = QApplication(sys.argv)
window = ImageDialog()
window.show()
sys.exit(app.exec_())
