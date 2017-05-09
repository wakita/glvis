from sn.qt import *
from sn.gl import *

class Widget(GLWidget):
    def __init__(self, parent):
        print('__init__@Widget')
        super(Widget, self).__init__(parent)

    def initializeGL(self):
        try:
            program1 = Program('test_compile_error.shaders')
        except:
            pass # simply ignore the compilation error
        program2 = Program('test_link_error.shaders')

Widget.start(Widget)
