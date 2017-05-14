import math

from PyQt5.QtGui import QColor

from sn.qt import *
from sn.gl import *

class Widget(GLWidget):
    v_offset = np.array([[.1, .1], [.9, .1], [.1, .9]], dtype = np.float32)

    def __init__(self, parent):
        super(Widget, self).__init__(parent)

    def initializeGL(self):
        super(self.__class__, self).initializeGL()

        VAO = self.VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        VBO = self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        v_offset = self.v_offset
        glBufferData(GL_ARRAY_BUFFER, v_offset.nbytes, v_offset, GL_STATIC_DRAW)

        self.program = Program('test1.shaders')
        print(self.program.u['no_uniform_var'].loc)

#       pos = glGetAttribLocation(self.program._program, 'v_offset')
#       print('pos:', pos)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

    def paintGL(self):
        super(Widget, self).paintGL()
        glBindVertexArray(self.VAO)
        self.program.use()
        glDrawArrays(GL_TRIANGLES, 0, self.v_offset.nbytes)
        glFlush()

    def on_tick(self):
        t = Time.time
        hue = math.fmod(t / 10, 1)
        c = QColor.fromHsvF(hue, 1., .5)
        glClearColor(c.redF(), c.greenF(), c.blueF(), 1)

#       c, s = math.cos(t), math.sin(t)
#       v_offset = self.v_offset
#       v_offset[0][0] = c; v_offset[0][1] = s
#       v_offset[1][0] = c; v_offset[1][1] = s
#       v_offset[2][0] = c; v_offset[2][1] = s
        self.updateGL();

    keyPressEvent = Window.keyPressEvent

app = Application()
window = Widget(None)
window.show()
app.startTimer(on_tick = window.on_tick)
app.run()
