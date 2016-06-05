import locale

from ctypes import *
import sys

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
from sn.gl.geometry.points import V as Points
import sn.gl.geometry.T3D as T

import sn.gl.debug


sn.gl.debug.logOnShaderVariables(True)
# sn.gl.debug.logOnSetUniform(True)

# points.D を継承して簡素化できないか？


class SSB(Structure):
    '''SSBの構造をctypesの構造体として抽象化したクラス．
    シェーダ定義におけるバッファ(std430形式)に合せること．
    '''
    _fields_ = [('clicked_x', c_uint), ('clicked_y', c_uint),
                ('pick_z', c_float),   ('pick_lock', c_int),
                ('pick_id', c_int)]


class KW4(Demo):

    def __init__(self, W):
        super().__init__(W)
        self.should_handle_mouse_click = False

        s = self.S = 5
        vvals = np.array(range(s)) * 2. / (s - 1) - 1.
        self.points = points = [(x, y, z) for x in vvals for y in vvals for z in vvals]

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        points = self.points
        super().initializeGL('kw4.shaders', lambda program: Points(program, points))

        eye, target, up = T.vec3(0, 0, 3), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](800 / self.S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # SSBの作成
        ssbo = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, ssbo)
        # SSBのためのアプリケーション側メモリ領域の確保
        ssb = SSB()
        # ssboで参照しているSSBとそのためのメモリ領域(ssb)を関連づけ
        glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(ssb), pointer(ssb), GL_DYNAMIC_READ)
        # なんでしたっけ，これ？でも，これがないと動かない．．．
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, ssbo)

    def paintGL(self):
        super().paintGL()
        self.handleMouseClick()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        pos = ev.pos()

        buf = glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_WRITE_ONLY)
        ssb = cast(buf, POINTER(SSB)).contents
        ssb.clicked_x = pos.x(); ssb.clicked_y = pos.y()
        ssb.pick_z    = -float('inf') # Initially -∞
        ssb.pick_lock = 0             # Initially unlocked (c.f., Unlocked@kw4.shader)
        ssb.pick_id   = -1            # Initially unknown
        # print('float.min: {0}'.format(sys.float_info.min))
        # print('Mouse released: pos: ({0}, {1}), z: {2}'.format(ssb.clicked_x, ssb.clicked_y, ssb.pick_z))
        glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)

        self.should_handle_mouse_click = True

    def handleMouseClick(self):
        if self.should_handle_mouse_click:
            # GPUのSSBをアプリケーション側にマップ
            buf = glMapBuffer(GL_SHADER_STORAGE_BUFFER, GL_READ_ONLY)
            # マップされたSSB領域をPythonオブジェクトとして仮想化
            ssb = cast(buf, POINTER(SSB)).contents
            print('id: {0} (z: {1})'.format(ssb.pick_id, ssb.pick_z))
            # SSB領域を開放
            glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
            # Pick判定処理の終了
            self.should_handle_mouse_click = False

if __name__ == '__main__':
    KW4.start(KW4)