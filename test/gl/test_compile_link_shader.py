from sn.qt import *
from sn.gl import *

class Widget(GLWidget):
    def __init__(self, parent):
        print('__init__@Widget')
        super(Widget, self).__init__(parent)

    def initializeGL(self):
        print('Compile/link test_compile_error.shaders')
        try:
            Program('test_compile_error.shaders')
        except Exception as e:
            pass

        print('Compile/link test_link_error.shaders')
        try:
            Program('test_link_error.shaders')
        except Exception as e:
            raise

        print('Compile/link test_link_empty.shaders')
        program3 = Program('test_link_empty.shaders')
        print(1)
        print(program3.u['non_existent_uniform_variable'])
        print(2)
        print(program3.u['non_existent_uniform_variable'].loc)
        print(3)
        print(program3.u['non_existent_uniform_variable'].name)
        print(4)
        print(program3.u['non_existent_uniform_variable'](5))
        print(5)

Widget.start(Widget)
