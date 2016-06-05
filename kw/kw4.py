import locale

from ctypes import *

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
from sn.gl.geometry.points import V as Points
import sn.gl.geometry.T3D as T

import sn.gl.debug


sn.gl.debug.logOnShaderVariables(True)
sn.gl.debug.logOnSetUniform(True)

# points.D を継承して簡素化できないか？


class SSB(Structure):
    '''SSBの構造をctypesの構造体として抽象化したクラス．
    シェーダ定義におけるバッファstd430形式に合せること．
    '''
    _fields_ = [('pick_z', c_float), ('pick_oid', c_uint)]


class KW4(Demo):

    def __init__(self, W):
        super().__init__(W)
        self.should_handle_mouse_click = False

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        S = 5
        vvals = np.array(range(S)) * 2. / (S - 1) - 1.
        points = [(x, y, 0) for x in vvals for y in vvals]
        super().initializeGL('kw4.shaders', lambda program: Points(program, points))

        eye, target, up = T.vec3(0, 0, 3), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](800 / S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # SSBの作成
        ssbo = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, ssbo)
        # SSBの領域の確保
        ssb = SSB(pick_z = 1000, pick_oid = -1)
        glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(ssb), pointer(ssb), GL_DYNAMIC_READ)
        # なんでしたっけ，これ？
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, ssbo)

    def paintGL(self):
        super().paintGL()
        self.handleMouseClick()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        pos = ev.pos()
        print('Mouse released: {0}, {1}'.format(pos.x(), pos.y()))
        clicked_position = np.array([pos.x(), pos.y()], dtype=np.uint32)
        self.program.u['clickedPosition'](clicked_position)
        self.should_handle_mouse_click = True

    def handleMouseClick(self):
        if self.should_handle_mouse_click:
            # GPUのSSBをアプリケーション側にマップ
            buf = glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_READ_ONLY)
            # マップされたSSB領域をPythonオブジェクトとして仮想化
            ssb = cast(buf, POINTER(SSB)).contents
            print('id:', ssb.pick_oid)
            # SSB領域を開放
            glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
            # Pick判定処理の終了
            self.should_handle_mouse_click = False

if __name__ == '__main__':
    KW4.start(KW4)