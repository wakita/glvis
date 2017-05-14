from sn.gl.geometry.plane import D as DEMO
import sn.sn_logging as sn_logging

sn_logging.log_on_uniform_update(True)


class KW5(DEMO):
    def paintGL(self):
        self.program.u['t'](self.time)
        super().paintGL()
        sn_logging.log_on_uniform_update(False)

KW5.start(fullscreen=True)
