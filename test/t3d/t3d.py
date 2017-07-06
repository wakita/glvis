import sympy as sp
import typing

def doit(f):
    f()
    return f

if __name__ == '__main__':
    import argparse
    from md import Markdown
    markdown = Markdown('test.t3d.t3d', title='T3D (Transform 3D) for Python').markdown

    parser = argparse.ArgumentParser()
    Markdown.add_parser_option(parser)

    class Symdoc(object): pass
    sym = Symdoc()
    sym.begin_align = r'\begin{align}'
    sym.end_align = r'\end{align}'
else:
    def markdown(*args, **kwds): pass

######################################################################
# 大域的な環境設定

import numpy as np
import sympy as sp

######################################################################
# ユーティリティ関数

def _subs(EXPR, repl):
    '数式EXPR中に出現する名前を辞書replにしたがって置換する。置換は辞書内のすべての名前について同時に実施する。'
    return EXPR.subs(repl, simultaneous=True)

def mat32(ARGS, EXPR):
    f = sp.lambdify(ARGS, EXPR, 'numpy')
    return lambda *args: np.array(f(*args), dtype=np.float32)

def vec32(ARGS, EXPR):
    f = mat32(ARGS, EXPR)
    return lambda *args: f(*args).reshape((len(ARGS),))


# 数式としてのベクトルの雛形の定義
sp.var('x y z w')
sym.x, sym.y, sym.z, sym.w = x, y, z, w

VEC2 = sp.Matrix([x, y])
VEC3 = sp.Matrix([x, y, z])
VEC4 = sp.Matrix([x, y, z, w])
def VEC(name, n): return sp.MatrixSymbol(name, n, 1)

def Vec2(X, Y):       return _subs(VEC2, {x: X, y: Y})
def Vec3(X, Y, Z):    return _subs(VEC3, {x: X, y: Y, z: Z})
def Vec4(X, Y, Z, W): return _subs(VEC4, {x: X, y: Y, z: Z, w: W})
def Vec(n, name):     return sp.MatrixSymbol(sp.Symbol(name), n, 1)

vec2 = vec32((x, y), VEC2)
vec3 = vec32((x, y, z), VEC3)
vec4 = vec32((x, y, z, w), VEC4)

# ベクトルの正規化
def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: return v
    return v/norm

######################################################################

def symfunc(f):
    name = f.__name__
    setattr(sym, 'f' + name, name)
    return f

@symfunc
def Homogeneous(p, w=1):
    '記号的に与えられたデカルト座標(p)に対して、その同次座標を記号的に与える。'
    return (p * w).col_join(sp.Matrix([w]))

@symfunc
def Cartesian(h):
    '記号的に与えられた同次座標(c)に対して、そのデカルト座標を記号的に与える。'
    return h[0:3,-1] / h[3,0]

pc = sym.pc = Vec3(x, y, z)
ph = sym.ph = Homogeneous(pc, w)

@doit
def __homogeneous_coordinate__():
    pc2 = Cartesian(ph)

    markdown(r'''
# 同次座標系 (Homogeneous coordinate system)

三次元デカルト座標系(*Cartesian coordinate system*)における点の座標の**同次座標**(*Homogeneous coordinate*)は，任意の非零実数${w}$を用いて変換されます。

$${fHomogeneous}\left({pc}, {w}\right) = {ph}$$

同次座標を用いた座標系のことを**同次座標系**(*Homogeneous coordinate system*)と呼びます．

逆に，同次座標をデカルト座標に変換することもできます。

$${fCartesian}\left({ph}\right) = {pc2}$$''',
             
             **locals(), **vars(sym))

# Homogeneous変換とCartesian変換が逆変換であることを記号的に検証
if __name__ == '__main__':
    p = Vec3(x, y, z)
    assert sp.Eq(p, Cartesian(Homogeneous(p, w=w)))

def homogeneous(c:np.ndarray, w:float=1) -> np.ndarray:
    'デカルト座標cを同次座標に変換する。'
    return np.append(c * w, w)

def cartesian(h:np.ndarray) -> np.ndarray:
    '同次座標hをデカルト座標に変換する。'
    w = h[-1]
    return h[0:-1] / w


######################################################################
markdown('# モデル変換')

######################################################################
# 拡大縮小変換

@doit
def __scale__():
    global impl_scale

    Scales = sp.var('s_x s_y s_z')
    fScale = sp.Function('Scale')(*Scales)
    Scale = sp.diag(*Scales, 1)  # 記号的拡大縮小行列
    Scale_ph = Scale * ph
    Scale_pc = Cartesian(Scale_ph)

    impl_scale = mat32(Scales, Scale)

    # Symbolic test

    assert(sp.Eq(Cartesian(Scale * Homogeneous(pc, w)), Vec3(s_x * x, s_y * y, s_z * z)))

    # Documentation of the implementation

    markdown(r'''## 拡大縮小変換: ${fScale}$

以下の拡大縮小変換行列 ${fScale}$ に同次座標を乗ずると，その座標の$X$-, $Y$-, $Z$-成分をそれぞれ${Scales}$倍した同次座標を与えます．

$${fScale} = {Scale}$$

実際に確認してみると、確かにそのとおりになっていることがわかります。

{begin_align}
{fScale} {fHomogeneous}\left({pc}\right)
    &= {Scale} {ph}  \\
    &= {Scale_ph} = {fHomogeneous}\left({Scale_pc}\right)
{end_align}
''',

             **locals(), **vars(sym))

def scale(sx:float, sy:float, sz:float) -> np.ndarray:
    '(X, Y, Z)-軸について、それぞれ(sx, sy, sz)倍するモデル変換行列を与える'
    return impl_scale(sx, sy, sz)


######################################################################

@doit
def __rotate__():
    global impl_rotX, impl_rotY, impl_rotZ

    theta = sp.var(r'\theta')
    fRotate = [sp.Function('Rotate_' + V)(theta) for V in 'X Y Z'.split()]

    c, s = sp.cos(theta), sp.sin(theta)
    Rotate = [
        sp.diag(1, sp.Matrix(2, 2, [ c, s, -s, c]), 1),
        sp.diag(sp.Matrix(3, 3, [ c, 0, -s, 0, 1, 0, s, 0, c ]), 1),
        sp.diag(sp.Matrix(2, 2, [ c, s, -s, c ]), 1, 1)]

    impl_rotX, impl_rotY, impl_rotZ = [(R, mat32(theta, R)) for R in Rotate]

    # Symbolic test

    # X-軸を中心とした回転によって
    axisX = Vec3(1, 0, 0)
    RotateX = Rotate[0]
    px = Cartesian(RotateX * Homogeneous(pc))

    # 1. 原点からの距離は変化しないこと（ノルムの二乗が等しいこと）
    pcpc, pxpx = pc.dot(pc), px.dot(px)
    assert(sp.simplify(sp.Eq(pcpc, pxpx)))

    # 2. 移動前後のベクトルの差分はX軸に直交すること
    assert(sp.simplify(sp.Eq((px-pc).dot(axisX), 0)))

    proj = px.dot(axisX) * axisX
    # 3. v1 = (pc - proj) と v2 = (px - proj) がなす角度がθであること
    v1, v2 = pc - proj, px - proj
    l1, l2 = sp.sqrt(v1.T.dot(v1)), sp.simplify(sp.sqrt(v2.T.dot(v2)))
    iprod_v1v2 = v1.dot(v2)
    iprod_v1v2_simplified = sp.simplify(iprod_v1v2)

    cos_theta=sp.cos(theta)
    l1_l2_cos_theta = l1 * l2 * cos_theta

    assert(sp.simplify(sp.Eq(iprod_v1v2, l1_l2_cos_theta)))

    # Documentation of the implementation
    markdown('## 回転変換: ${}, {}, {}$', *fRotate)

    for axis, fRot, Rot in zip('X Y Z'.split(), fRotate, Rotate):
        markdown('''
- 回転変換行列 (${fRot}$) に同次座標を乗ずると，その座標を${axis}$軸のまわりに${theta}$だけ回転した点の同次座標を与えます．

    $${fRot} {ph} = {Rot} {ph} = {result}$$''',
                 
                 result=Rot * ph, **locals(), **vars(sym))

    fRotX = fRotate[0]
    RotateX = Rotate[0]
    px = sp.simplify(Cartesian(RotateX * ph))
    pcpc = pc.dot(pc)
    pxpx = sp.simplify(px.dot(px))
    px_pc = px - pc
    movex_axisX=px_pc.dot(axisX)

    markdown(r'''
では、ここで得られた変換${fRotX}$が確かに回転であることを確認してみよう。この変換で点$p$が$p'$に移ったものとすると：

{begin_align}
p &= {pc} \\
p' &= {px}
{end_align}

+ 変換前後でベクトルと原点の距離は変化しないこと

    {begin_align}
    \|p\|^2 &= \left\|{v1}\right\|^2 = {pcpc} \\
    \|p'\|^2 &= \left\|{v2}\right\|^2 = {pxpx}
    {end_align}

+ 変換前後のベクトルの差分が回転軸となるX軸と直交すること

    $p$をX軸を中心として回転するとき、その回転のあいだ$p$はX軸と直交する平面を移動します。したがって、移動後の$p'$もそのX軸と直交する平面にあるはずです。$p, p'$がともにX軸と直交する平面上の点ということは、$p' - p$はこの平面上のベクトルということになるので、X軸と直交するはずです。

    $$\left({px_pc}, {axisX}\right) = {movex_axisX}$$

    内積が0なので直交していることが確認できました。

+ 回転角が確かに${theta}$であること

    X軸を中心として$p$を${theta}$回転して$p'$に移すということは、$p$と$p'$のなす角度が${theta}$というような気もしますが、実はそうではありません。ベクトル$p$は円錐の表面を撫でるようにして$p'$に写るからです。${theta}$となるのは、$p$からX軸への垂線の足となる$p_x$について$p$と$p'$がなす角度です。

    では、まず$p_x$を求めてみましょう。これをベクトルだと思うとX軸方向の単位ベクトル${axisX}$と同じ向きで、長さが前述の垂線の足にあたる点と原点の距離です。この距離は$p$と${axisX}$の内積で与えられますので、結局$p_x = (p_x, {axisX}) {axisX} = {proj}$となります。

    角度が${theta}$であることは($p-p_x$)と($p'-p_x$)の内積に関する性質について確認すればよいでしょう。

    {begin_align}
    (p - p_x, p' - p_x) &= ({v1}, {v2}) \\
        &= {iprod_v1v2} \\
        &= {iprod_v1v2_simplified}
    {end_align}

    一方、$p-p_x$と$p'-p_x$のなす角が{theta}ならば、その内積は$\ell_1 \ell_2 {cos_theta}$になるはずです。

    {begin_align}
    \ell_1 &= \|p - p_x\| = {l1} \\
    \ell_2 &= \|p' - p_x\| = {l2} \\
    \ell_1 \ell_2 {cos_theta} &= {l1} {l2} {cos_theta} = {l1_l2_cos_theta}
    {end_align}

    以上より$(p-p_x, p'-p_x) = \ell_1 \ell_2 {cos_theta}$が確認できました。''',
             **locals(), **vars(sym))

def rotateX(theta:float) -> np.ndarray:
    '(X)-軸を中心にtheta回転するモデル変換行列を与える'
    return impl_rotX(theta)

def rotateY(theta:float) -> np.ndarray:
    '(Y)-軸を中心にtheta回転するモデル変換行列を与える'
    return impl_rotY(theta)

def rotateZ(theta:float) -> np.ndarray:
    '(Z)-軸を中心にtheta回転するモデル変換行列を与える'
    return impl_rotZ(theta)

######################################################################
# 並行移動変換

@doit
def __translate__():
    global impl_translate

    tTranslate = sp.var('t_x t_y t_z')
    fTranslate = sp.Function('Translate')(*tTranslate)
    Translate = sp.eye(3).row_join(sp.Matrix(tTranslate)).col_join(sp.Matrix([[0, 0, 0, 1]]))

    impl_translate = mat32(tTranslate, Translate)

    pt = Cartesian(Translate * ph)
    dt = Vec3(*tTranslate)
    markdown('$${}$$', sp.Eq(pt, pc + dt))
    assert(sp.simplify(sp.Eq(pt, pc + dt)))

    markdown('## 並行移動変換: {fTranslate}', **locals())

def translate(tx:float, ty:float, tz:float) -> np.ndarray:
    '(tx, ty, tz)だけ並行移動するモデル変換行列を与える'
    impl_translate(tx, ty, tz)
