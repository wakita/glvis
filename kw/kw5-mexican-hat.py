from sn.gl.geometry.plane import D as Demo

import sn.gl.debug
sn.gl.debug._logOnSetUniform_ = True

class KW5(Demo):
    def paintGL(self):
        self.program.u['t'](self.time)
        super().paintGL()
        sn.gl.debug._logOnSetUniform_ = False

    def onTick(self):
        self.updateGL()

KW5.start(KW5, fullscreen=True)
