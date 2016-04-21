
# coding: utf-8

# # T3D (Transform 3D module)
# ## A transform 3D module for Python

# In[2]:

from math import cos, sin, tan

import numpy as np
import sympy as sp
sp.init_printing()

from sn.nbsupport import md, _subs

Symbolic = {}


# # 基本的なユーティリティ関数

# In[3]:

def __M32__(ARGS, EXPR):
    f = sp.lambdify(ARGS, EXPR, 'numpy')
    return lambda *args: np.array(f(*args), dtype=np.float32)

def __V32__(ARGS, EXPR):
    f = __M32__(ARGS, EXPR)
    return lambda *args: f(*args).reshape((len(ARGS),))

Symbolic['M32'] = __M32__
Symbolic['V32'] = __V32__


# ## ベクトルの扱い
# 
# ベクトルの定義

# In[4]:

# 数式としてのベクトルの雛形の定義
sp.var('x y z w')

VEC2 = sp.Matrix([x, y])
VEC3 = sp.Matrix([x, y, z])
VEC4 = sp.Matrix([x, y, z, w])
def VEC(name, n): return sp.MatrixSymbol(name, n, 1)

def Vec2(X, Y):       return _subs(VEC2, {x: X, y: Y})
def Vec3(X, Y, Z):    return _subs(VEC3, {x: X, y: Y, z: Z})
def Vec4(X, Y, Z, W): return _subs(VEC4, {x: X, y: Y, z: Z, w: W})
def Vec(n, name):     return sp.MatrixSymbol(sp.Symbol(name), n, 1)

vec2 = Symbolic['vec2'] = Symbolic['V32']((x, y), VEC2)
vec3 = Symbolic['vec3'] = Symbolic['V32']((x, y, z), VEC3)
vec4 = Symbolic['vec4'] = Symbolic['V32']((x, y, z, w), VEC4)

# ベクトルの正規化
def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: return v
    return v/norm


# # 同次座標系 (Homogeneous coordinate system)
# 
# 
# 三次元デカルト座標系(*Cartesian coordinate system*)における点の座標$(x, y, z)$の**同次座標**(*Homogeneous coordinate*)は，任意の非零実数$w$を用いて，$(wx, wy, wz, w)$で表します．
# 
# 逆に，同次座標$(x, y, z, w)$のデカルト座標は$(x/w, y/w, z/w)$で与えられます．同次座標を用いた座標系のことを**同次座標系**(*Homogeneous coordinate system*)と呼びます．

# In[5]:

def Homogeneous(p, w=1):
    return (p * w).col_join(sp.Matrix([w]))

def Cartesian(h):
    return h[0:3,-1] / h[3,0]

def homogeneous(c, w=1):
    return np.append(c * w, w)
    
def cartesian(h):
    w = h[-1]
    return h[0:-1] / w

if __name__ == '__main__':
    p = Vec3(x, y, z)
    assert sp.Eq(p, Cartesian(Homogeneous(p, w=w)))


# $e_1, e_2, e_3 \mapsto e_1', e_2', e_3'$に写す写像$T$について考えてみよう．
# 
# \begin{align}
#   T\begin {pmatrix}e_1 & e_2 & e_3\end {pmatrix} &= \begin {pmatrix}e_1' & e_2' & e_3'\end {pmatrix} \\
#   T &= \begin {pmatrix}e_1' & e_2' & e_3'\end {pmatrix} \cdot \begin {pmatrix}e_1 & e_2 & e_3\end {pmatrix}^{-1}
# \end{align}

# # 行列
# 
# 以下は行列の構成子です．Pythonのライブラリ関数の実装に用いています．

# In[6]:

# すべてのAPIをSymbolicに記述したら不要になる

def mat4x4(m00, m01, m02, m03, m10, m11, m12, m13,
        m20, m21, m22, m23, m30, m31, m32, m33):
    return np.array([[m00, m01, m02, m03], [m10, m11, m12, m13],
        [m20, m21, m22, m23], [m30, m31, m32, m33]], dtype=np.float32)

def tmat4x4(m00, m01, m02, m03, m10, m11, m12, m13,
        m20, m21, m22, m23, m30, m31, m32, m33):
    return mat4x4(m00, m01, m02, m03, m10, m11, m12, m13,
        m20, m21, m22, m23, m30, m31, m32, m33).transpose()

if __name__ == '__main__':
    print('行列の構成子のテスト')
    print('mat4x4(1, 2, ..., 16):\n{0}'.format(mat4x4(*range(1, 17))))
    print('tmat4x4(1, 2, ..., 16):\n{0}'.format(tmat4x4(*range(1, 17))))


# ## 拡大縮小行列: $\mathrm {Scale}(s_x, s_y, s_z)$

# In[7]:

ScaleSymbols = sp.var('s_x s_y s_z')
Symbolic['Scale'] = sp.diag(s_x, s_y, s_z, 1)
scale = Symbolic['scale'] = Symbolic['M32'](ScaleSymbols, Symbolic['Scale'])

if __name__ == '__main__':
    md('拡大縮小変換行列$\mathrm {Scale}(s_x, s_y, s_z)$に同次座標を乗ずると，',
       'その座標の$X$-, $Y$-, $Z$-成分をそれぞれ$s_x, s_y, s_z$倍した同次座標を与えます．')
    p = Vec3(x, y, z)
    md('$$\mathrm {Scale}(s_x, s_y, s_z)', Homogeneous(p), '=',
       Symbolic['Scale'], Homogeneous(p), '=',
       (Symbolic['Scale'] * Homogeneous(p)), '$$')


# ## 回転変換: Rotate_

# In[8]:

sp.var('theta')
c, s = sp.cos(theta), sp.sin(theta)

Symbolic['RotateX'] = sp.diag(1, sp.Matrix(2, 2, [ c, s, -s, c]), 1)
Symbolic['RotateY'] = sp.diag(sp.Matrix(3, 3, [ c, 0, -s, 0, 1, 0, s, 0, c ]), 1)
Symbolic['RotateZ'] = sp.diag(sp.Matrix(2, 2, [ c, s, -s, c ]), 1, 1)

rotateX, rotateY, rotateZ = [Symbolic['M32'](theta, Symbolic['Rotate' + R])
                             for R in ['X', 'Y', 'Z']]
if __name__ == '__main__':
    md(r'回転変換行列($\mathrm {Rotate}_X(\theta)$に同次座標を乗ずると，',
       r'その座標を$X$軸のまわりに$\theta$だけ回転した点の同次座標を与えます．',
       'ほかの軸に対する回転行列の働きも同様です．')
    for R in 'X Y Z'.split():
        md('### 回転変換$\mathit{Rotate}_', R, '(\\theta)$: ',
           R, '軸を中心に回転\n$$', Symbolic['Rotate' + R], '$$')


# ## 並行移動行列 ($\mathit {Translate}$)

# In[9]:

[tx, ty, tz] = TranslateSymbols = sp.symbols('t_x t_y t_z')
Symbolic['Translate'] = sp.eye(3).row_join(sp.Matrix(TranslateSymbols)).col_join(sp.Matrix([[0, 0, 0, 1]]))
translate = Symbolic['M32'](TranslateSymbols, Symbolic['Translate'])

if __name__ == '__main__':
    p = Homogeneous(Vec3(x, y, z))

    md('並行移動変換行列$\mathrm {Translate}(t_x, t_y, t_z)$に同次座標を乗ずると，',
       'その座標を$X, Y, Z$軸方向にそれぞれ$t_x, t_y, t_z$だけ',
       '並行移動した点の同次座標を与えます．')
    md('$\mathrm {Translate}(t_x, t_y, t_z)', p, '=',
       Symbolic['Translate'], p, '=',
       Symbolic['Translate'] * p, '$')


# ## 空間変換のための関数群
# 
# ### 視野変換 (LookAt)
# 
# 視野変換は**全体座標系** (*Global coordinate system*)に配置されたオブジェクトを観察者の立場から眺めたときの様子，すなわち**視野座標系**(*Viewing coordinate system*)に変換します．観察者の立ち位置を表現するために観察者の視点(*eye*)，観察者の視線の先の点(*center*)，そして観察者の頭の向き(*up*)を与えます．
# 
# 視野変換は全体座標系を視点に平行移動する変換$\mathit {LookAtTranslate}$と，視線の向きを$Z$軸方向から視線の向きに回転する変換$\mathit {LookAtRotate}$を合成($\mathit {LooAtRotate} \times \mathit {LookAtTranslate}$)したものと考えられます．

# In[10]:

LookAtVectors = [Eye, Side, Head, Forward] = [
    sp.var('I_x I_y I_z'), sp.var('S_x S_y S_z'),
    sp.var('H_x H_y H_z'), sp.var('F_x F_y F_z')]
[I, S, H, F] = [sp.Matrix(3, 1, M) for M in LookAtVectors]

LookAtTranslate = Symbolic['Translate'].subs({ tx: -I_x, ty: -I_y, tz: -I_z })
invLookAtRotate = sp.Matrix(sp.BlockMatrix([[S, H, -F, sp.zeros(3, 1)]])).col_join(sp.Matrix([[0, 0, 0, 1]]))
LookAtRotate = invLookAtRotate.T  # 回転行列は正規直交行列なので，逆行列は転置行列

Symbolic['LookAt'] = LookAtRotate * LookAtTranslate
__lookat__ = Symbolic['M32'](Eye + Forward + Side + Head, Symbolic['LookAt'])

def lookat(eye, center, up):
    i = eye
    f = normalize(center - eye)
    s = normalize(np.cross(f, up))
    h = np.cross(s, f)
    return __lookat__(i[0], i[1], i[2],
                      f[0], f[1], f[2],
                      s[0], s[1], s[2],
                      h[0], h[1], h[2])

Symbolic['lookat'] = lookat

if __name__ == '__main__':
    md('### 視点へのカメラの移動 (LookAtTranslate)\n',
       '最初の変換は視点($I$)を原点に平行移動します．',
       r'移動のベクトルは$(0 - \mathit {eye}) = -\mathit {eye}$ですので：'
       r'$$\mathit {LookAtTranslate} = \mathit {Translate}(-I) =',
       LookAtTranslate, '$$')
    
    md('念のため、$\mathit {LookAtTranslate}$が視点($I$)を原点に移動することを確認しましょう．',
       r'$$\mathrm {LookAtTranslate} \times', Homogeneous(I), '=',
       LookAtTranslate, r'\times', Homogeneous(I), '=',
       LookAtTranslate * Homogeneous(I), '$$')

    md('### 視線の設定 (LookAtRotate)\n',
       '次に回転変換ですが，視野座標系を定める3つの軸は，',
       '視線の向き(*Forward*)，頭の向き(*Head*)，',
       'そして両者に直交する横方向の向き(*Side*)で構成できそうなのですが，',
       '一般には視線の向きと頭の向きが直交しているとは限りません．',
       'そこで，3軸は以下のように取ります．\n',
       '- 視線の向き ($F$): $(\mathit {center} - \mathit {eye})$\n',
       '- 横の向き ($S$): 「視線の向き」と「頭の向き」に直交するベクトル\n',
       '- 上の向き ($H$): 「横の向き」と「視線の向き」に直交するベクトル\n\n',
       r'すなわち：\begin{align}',
       r'F &= \mathit {normalize}(\mathit {center} - \mathit {eye}) \\',
       r'S &= \mathit {normalize}(F \times \mathit {up}) \\',
       r'H &= S \times F\end{align}', '\n\n'
       
       r'逆回転変換$\mathit {LookAtRotate}^{-1}$は標準的な基底を$S, H, -F$に移動します．',
       'ここで$-F$と反転しているのは，全体座標系は右手系で与え，',
       '視野座標系は左手系で与える慣習に沿ったためです．',
       '$$', r'\mathrm {LookAtRotate}^{-1} = ', invLookAtRotate, '$$',
       'では，この逆回転変換が実際に基底ベクトルを$S, H, F$に写すことを確認しておきましょう．$$',
       Vec3(1, 0, 0), r'\mapsto',
       Cartesian(invLookAtRotate * Homogeneous(Vec3(1, 0, 0))), r'\qquad',
       Vec3(0, 1, 0), r'\mapsto',
       Cartesian(invLookAtRotate * Homogeneous(Vec3(0, 1, 0))), r'\qquad',
       Vec3(0, 0, 1), r'\mapsto',
       Cartesian(invLookAtRotate * Homogeneous(Vec3(0, 0, 1))),
       '$$')
    md(r'求めたい回転変換行列$\mathit {LookAtRotate}$はこの変換の逆行列にあたります．',
       'ここで$S, H, F$は正規標準基底を構成し、',
       '正規直交行列の逆行列は転置行列になるので，回転行列は以下のように簡単に得られます．$$',
       r'\mathrm {LookAtRotate} =',
       r'(\mathrm {LookAtRotate}^{-1})^{-1} =',
       r'(\mathrm {LookAtRotate}^{-1})^T =',
       invLookAtRotate, '^T =', LookAtRotate, '$$')
    
    md('### 視野変換 (LookAt行列)')
    md('平行移動行列と回転行列を合成することで視野変換行列が得られます．$$',
       r'\mathrm {LookAt} = \mathrm {LookAtRotate} \times \mathrm {LookAtTranslate} =',
       Symbolic['LookAt'], '$$')


# ## 正射影 (Orthographic transformation)

# In[11]:

sp.var('width, height near far')

PointsCamera = sp.Matrix([Homogeneous(Vec3(*v)).T
                          for v in [(0, 0, -near),
                                    (width/2, 0, -near),
                                    (0, height/2, -near),
                                    (width/2, 0, -far)]]).T

PointsOrtho = sp.Matrix([Homogeneous(Vec3(*v)).T
                         for v in [(0, 0, -1), (1, 0, -1), (0, 1, -1), (1, 0, 1)]]).T

Symbolic['Orthographic'] = sp.simplify(PointsOrtho * PointsCamera.inv())
orthographic = Symbolic['M32']((width, height, near, far), Symbolic['Orthographic'])

if __name__ == '__main__':
    md('正射影は空間から視線を中心線とする直方体領域を切り取り，',
       'それを原点を中心とした一辺の長さが2の立方体に射影します．',
       r'直方体の表面から適宜4点を選んで、それらの写る先を考えてみましょう：\begin{align}',
       r'(0, 0, -\mathit {near}) &\mapsto (0, 0, -1)\\',
       r'(\mathit {width}/2, 0, -\mathit {near}) &\mapsto (1, 0, -1)\\',
       r'(0, \mathit {height}/2, -\mathit {near}) &\mapsto (0, 1, -1)\\',
       r'(\mathit {width}/2, 0, -\mathit {far}) &\mapsto (1, 0, 1)',
       r'\end{align}', '\n\n',
       r'正射影が行列で表されるとしたら、',
       r'以下のように定義された$\mathit {PointsCamera}$と$\mathit {PointsOrtho}$を用いて、',
       '以下のように得られます。',
       r'\begin{align}', '\n',
       r'\mathit {Orthographic}',
       r'&= \mathit {PointsOrtho} \times \mathit {PointsCamera}^{-1}',
       '=', PointsOrtho, r'\times', PointsCamera, r'^{-1} \\',
       '&= ', Symbolic['Orthographic'], '\n', r'\end{align}', '\n\n')


# ## 錐台変換？ (Frustum transformation)
# 
# 正射影との違いを理解していない．．．式は異なるようだが，何をしている？？？

# In[12]:

def frustum(left, right, bottom, top, near, far):
    rl, tb, fn = right - left, top - bottom, far - near
    return mat4x4(
            2 * near / rl, 0, (right + left) / rl, 0,
            0, 2 * near / tb, (top + bottom) / tb, 0,
            0, 0, -(far + near) / fn, -2 * far * near / fn,
            0, 0, 0, 0)

''' GLM implementation
template <typename T> GLM_FUNC_QUALIFIER tmat4x4<T, defaultp>
frustum (T left, T right, T bottom, T top, T nearVal, T farVal) {
    tmat4x4<T, defaultp> Result(0);
    Result[0][0] = (static_cast<T>(2) * nearVal) / (right - left);
    Result[1][1] = (static_cast<T>(2) * nearVal) / (top - bottom);
    Result[2][0] = (right + left) / (right - left);
    Result[2][1] = (top + bottom) / (top - bottom);
    Result[2][2] = -(farVal + nearVal) / (farVal - nearVal);
    Result[2][3] = static_cast<T>(-1);
    Result[3][2] = -(static_cast<T>(2) * farVal * nearVal) / (farVal - nearVal);
    return Result;
}
'''

if __name__ == '__main__':
    print('Frustum(0, 10, 0, 10, 2, 12):\n{0}'.format(frustum(0, 10, 0, 10, 2, 12)))


# ## 透視投影 (Perspective transformation)

# In[14]:

PerspectiveSymbols = sp.var('fovy aspect near far')
ny = near * sp.tan(fovy / 2)
nx = ny * aspect
fy = far * sp.tan(fovy / 2)

PointsCamera = sp.Matrix([Homogeneous(Vec3(*v)).T
                          for v in [(0, 0, -near), (nx, 0, -near), (0, ny, -near),
                                    (0, fy, -far)]]).T

PointsPerspective = sp.Matrix([Homogeneous(Vec3(*v), w=near).T
                               for v in [(0, 0, -1), (1, 0, -1), (0, 1, -1)]]).T
PointsPerspective = PointsPerspective.row_join(Homogeneous(Vec3(0, 1, 1), w=far))

Symbolic['Perspective'] = sp.simplify(PointsPerspective * PointsCamera.inv())
perspective = Symbolic['M32'](PerspectiveSymbols, Symbolic['Perspective'])

if __name__ == '__main__':
    md('透視投影は，視野空間において視点から視る視野錐台(*view frustum*)を',
       'クリッピング空間上の立方体に射影する変換で，遠近法を表現します．',
       '透視投影は視野角(*fovy*; field of view $y$)，',
       r'アスペクト比($\mathit {aspect} = \mathit {width} / \mathit {height}$)，',
       'そして正射影と同様に奥行方向に切り取るための*near*と*far*を用います．',
       '視野角はラジアンによって左右方向の視野を定めます．',
       'この視野角とアスペクト比によって上下方向の視野角が定まります．\n\n',
       '錐台の表面から4点を選んで、それらの写る先を考えてみましょう：',
       r'\begin{align}',
       sp.latex((0, 0, -near)),  r'&\mapsto (0, 0, -1)\\',
       sp.latex((nx, 0, -near)), r'&\mapsto (1, 0, -1) \\',
       sp.latex((0, ny, -near)), r'&\mapsto (0, 1, -1) \\',
       sp.latex((0, ny, -far)),  r'&\mapsto (0, 1,  1)',
       r'\end{align}',
       '透視投影変換が行列で表現できるとしたら、以下のように得られるはずです：',
       r'\begin{align}', '\n',
       r'\mathit {Perspective}',
       r'&= \mathit {PointsPerspective} \times \mathit {PointsCamera}^{-1} \\', '\n'
       '&= ', Symbolic['Perspective'], r'\\', '\n',
       r'& \text {ただし、ここで}\\','\n',
       r'\mathit {PointsCamera} &= ', PointsCamera, r'\\', '\n',
       r'\mathit {PointsPerspective} &= ', PointsPerspective, r'\\', '\n',
       r'\end{align}', '\n\n')

    # デカルト座標系において視野錐台が確かに、単位立方体に射影されることの確認
    Points = sp.simplify(Symbolic['Perspective'] * PointsCamera)
    for c in range(4):
        assert(Cartesian(Points[:,c]) == Cartesian(PointsPerspective[:,c]))


# In[13]:

def perspectiveFov(fov, width, height, near, far):
    h = cos(fov/2) / sin(fov/2)
    w = h * height / width
    return mat4x4(
            w, 0, 0, 0,
            0, h, 0, 0,
            0, 0, -(far + near) / (far - near), -1, 
            0, 0, -2 * far * near / (far - near))

'''GLM implementation
template <typename T> GLM_FUNC_QUALIFIER tmat4x4<T, defaultp>
perspectiveFov (T fov, T width, T height, T zNear, T zFar) {
    assert(width > static_cast<T>(0));
    assert(height > static_cast<T>(0));
    assert(fov > static_cast<T>(0));

    T const rad = fov;
    T const h = glm::cos(static_cast<T>(0.5) * rad) / glm::sin(static_cast<T>(0.5) * rad);
    T const w = h * height / width; ///todo max(width , Height) / min(width , Height)?

    tmat4x4<T, defaultp> Result(static_cast<T>(0));
    Result[0][0] = w;
    Result[1][1] = h;
    Result[2][2] = - (zFar + zNear) / (zFar - zNear);
    Result[2][3] = - static_cast<T>(1);
    Result[3][2] = - (static_cast<T>(2) * zFar * zNear) / (zFar - zNear);
    return Result;
}'''

if __name__ == '__main__':
    pass


# In[14]:

def project(obj, Model, Proj, viewport):
    V = Proj.dot(Model.dot(obj))
    V = V / V[3] / 2 + 0.5
    V[0] = V[0] * viewport[2] + viewport[0]
    V[1] = V[1] * viewport[3] + viewport[1]
    return V

'''GLM implementation
template <typename T, typename U, precision P> GLM_FUNC_QUALIFIER tvec3<T, P>
project (tvec3<T, P> const & obj, tmat4x4<T, P> const & model, tmat4x4<T, P> const & proj, tvec4<U, P> const & viewport) {
    tvec4<T, P> tmp = tvec4<T, P>(obj, T(1));
    tmp = model * tmp;
    tmp = proj * tmp;

    tmp /= tmp.w;
    tmp = tmp * T(0.5) + T(0.5);
    tmp[0] = tmp[0] * T(viewport[2]) + T(viewport[0]);
    tmp[1] = tmp[1] * T(viewport[3]) + T(viewport[1]);

    return tvec3<T, P>(tmp);
}'''

if __name__ == '__main__':
#    print('Project(obj, Model, Proj, viewport):\n{0}'.format(perspective(np.pi / 3, 1, 2, 12)))
    pass

