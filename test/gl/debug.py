from sn.qt import *
from sn.gl import *

def onDebugMessage(*args, **kwargs):
    println('args = {0}, kwargs = {1}'.format(args, kwargs))

class W(GLWidget):

    def initializeGL(self):
        super().initializeGL()
        glEnable(GL_DEBUG_OUTPUT)
        glDebugMessageCallback(onDebugMessage, None)
        glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE, 0, None, GL_TRUE)
        glDebugMessageInsert(GL_DEBUG_SOURCE_APPLICATION, GL_DEBUG, GL_DEBUG_TYPE_MARKER, 0, GL_DEBUG_SEVERITY_NOTIFICATION, -1, "Starting debug messaging service")

app = Application()
window = W(None)
window.show()
app.run()
