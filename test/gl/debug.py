from sn.qt import *
from sn.gl import *


def onDebugMessage(*args, **kwargs):
    print('error')
    print('args = {0}, kwargs = {1}'.format(args, kwargs))


def cb_dbg_msg(source, msg_type, msg_id, severity, length, raw, user):
    print('Callback debug message')
    msg = raw[0:length]
    print(source, msg_type, msg_id, severity, msg)


class W(GLWidget):

    def initializeGL(self):
        super().initializeGL()
        glEnable(GL_DEBUG_OUTPUT)
        glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
        glDebugMessageCallback(GLDEBUGPROC(cb_dbg_msg), None)
        glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE, 0, None, GL_TRUE)
        m = 'Starting debug messaging service'
#       glUseProgram(1234)
#       glDebugMessageInsert(GL_DEBUG_SOURCE_APPLICATION, GL_DEBUG_TYPE_MARKER,
        message = ctypes.create_string_buffer(b'Starting debug messaging service')
        glDebugMessageInsert(GL_DEBUG_SOURCE_APPLICATION, GL_DEBUG_TYPE_MARKER,
                             0, GL_DEBUG_SEVERITY_NOTIFICATION, -1, message)

app = Application()
window = W(None)
window.show()
app.run()
