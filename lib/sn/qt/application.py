import sys
from PyQt5.QtCore import (QTime, QTimer)
from PyQt5.QtWidgets import (QApplication, QWidget)

class __TIME__(type):
    @property
    def time(cls):
        return cls._time.elapsed() / 1000.

class Time(metaclass = __TIME__):
    _time = QTime(); _time.start()

class Application(QApplication):

    def __init__(self):
        super(QApplication, self).__init__(sys.argv)

    def startTimer(self, timeout=(1000/60.), onTick=None):
        cls = self.__class__
        cls._timer = QTimer(self)
        cls._timer.start(timeout)
        if onTick != None: cls.addOnTick(onTick)

    @classmethod
    def addOnTick(cls, onTick): cls._timer.timeout.connect(onTick)

    def run(self):
        sys.exit(self.exec_())

if __name__ == '__main__':
    app = Application()
    app.startTimer(1000, lambda: print('*', Time.time))
    sys.exit(app.exec_())
