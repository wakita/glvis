import sys
from PyQt5.QtCore import (QTime, QTimer)
from PyQt5.QtWidgets import (QApplication, QWidget)

class __TIME__(type):
    @property
    def time(cls) -> float:
        return cls._time.elapsed() / 1000.

class Time(metaclass = __TIME__):
    _time = QTime(); _time.start()

class Application(QApplication):

    def __init__(self):
        super(QApplication, self).__init__(sys.argv)
        import traceback
        def excepthook(type, value, tback):
            print('{}:\n    {}'.format(type.__name__, value), file=sys.stderr)
            traceback.print_exception(type, value, tback, file=sys.stderr)
            exit(1)
        sys.excepthook = excepthook


    def startTimer(self, timeout=(1000/60.), on_tick=None):
        cls = self.__class__
        cls._timer = QTimer(self)
        cls._timer.start(timeout)
        if on_tick != None: cls.add_on_tick(on_tick)

    @classmethod
    def add_on_tick(cls, on_tick): cls._timer.timeout.connect(on_tick)

    def run(self):
        sys.exit(self.exec_())

if __name__ == '__main__':
    app = Application()
    app.startTimer(1000, lambda: print('*', Time.time))
    sys.exit(app.exec_())
