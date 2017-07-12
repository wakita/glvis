import argparse
import sys
import sympy as sp
import typing

from symdoc import Markdown, doit, symfunc, gsym

cmdline_parser = argparse.ArgumentParser()
Markdown.add_parser_option(cmdline_parser)

M = Markdown('test.t3d', title='T3D (Transform 3D) for Python')
markdown, cmdline = M.markdown, M.cmdline


######################################################################
# 大域的な環境設定

import numpy as np
import sympy as sp

######################################################################
# ユーティリティ関数

def _subs(EXPR, repl):
    '数式EXPR中に出現する名前を辞書replにしたがって置換する。辞書内のすべての名前を並列置換する。'
    return EXPR.subs(repl, simultaneous=True)

def _mat32(ARGS, EXPR):
    f = sp.lambdify(ARGS, EXPR, 'numpy')
    return lambda *args: np.array(f(*args), dtype=np.float32)

def _vec32(ARGS, EXPR):
    f = mat32(ARGS, EXPR)
    return lambda *args: f(*args).reshape((len(ARGS),))

def mat32(ARGS: typing.List[sp.Symbol], Matrix:sp.Basic) -> np.ndarray:
    '行列を表す数式Matrixに出現する記号のうち，ARGSについてλ抽象しつつ，その行列を評価するPython関数を与える．'
    return _mat32(ARGS, Matrix)

def vec32(ARGS: typing.List[sp.Symbol], Vector:sp.Basic) -> np.ndarray:
    'ベクトルを表す数式Vectorに出現する記号のうち，ARGSについてλ抽象しつつ，その行列を評価するPython関数を与える．'
    return _vec32(ARGS, Vector)


# 数式としてのベクトルの雛形の定義
gsym.x, gsym.y, gsym.z, gsym.w = sp.var('x y z w')

VEC2 = sp.Matrix([x, y])
VEC3 = sp.Matrix([x, y, z])
VEC4 = sp.Matrix([x, y, z, w])
def VEC(name: str, n: int) -> sp.MatrixSymbol:
    'n次元ベクトルを表す記号を返す'
    return sp.MatrixSymbol(name, n, 1)

def Vec2(X: sp.Basic, Y: sp.Basic) -> sp.Matrix:
    'X, Yを要素とする2次元ベクトルの式を与える'
    return _subs(VEC2, {x: X, y: Y})

def Vec3(X: sp.Basic, Y: sp.Basic, Z: sp.Basic) -> sp.Matrix:
    'X, Y, Zを要素とする3次元ベクトルの式を与える'
    return _subs(VEC3, {x: X, y: Y, z: Z})

def Vec4(X: sp.Basic, Y: sp.Basic, Z: sp.Basic, W: sp.Basic) -> sp.Matrix:
    'X, Y, Z, Wを要素とする4次元ベクトルの式を与える'
    return _subs(VEC4, {x: X, y: Y, z: Z, w: W})

def Vec(n: int, name: str) -> sp.MatrixSymbol:
    'n次元ベクトルの記号を与える'
    return sp.MatrixSymbol(sp.Symbol(name), n, 1)

_vec2 = vec32((x, y), VEC2)
_vec3 = vec32((x, y, z), VEC3)
_vec4 = vec32((x, y, z, w), VEC4)

def vec2(x:float, y:float) -> np.ndarray:
    'floatの値x, yを要素とする2次元ベクトルのNumpy 32-bit float形式のndarrayを与える'
    return _vec2(x, y)

def vec3(x, y, z):
    'floatの値x, y, zを要素とする2次元ベクトルのNumpy 32-bit float形式のndarrayを与える'
    return _vec3(x, y, z)

def vec4(x, y, z, w):
    'floatの値x, y, z, wを要素とする2次元ベクトルのNumpy 32-bit float形式のndarrayを与える'
    return _vec4(x, y, z, w)

def normalize(v: np.ndarray) -> np.ndarray:
    'Numpy ndarray形式のデータ列で表現されたベクトルを正規化したものを与える'
    norm=np.linalg.norm(v)
    if norm==0: return v
    return v/norm

######################################################################

@symfunc
def Homogeneous(p, w=1):
    '記号的に与えられたデカルト座標(p)に対して、その同次座標を記号的に与える。'
    return (p * w).col_join(sp.Matrix([w]))

@symfunc
def Cartesian(h):
    '記号的に与えられた同次座標(c)に対して、そのデカルト座標を記号的に与える。'
    return h[0:3,-1] / h[3,0]

pc = gsym.pc = Vec3(x, y, z)
ph = gsym.ph = Homogeneous(pc, w)

@doit
def __homogeneous_coordinate__():
    pc2 = Cartesian(ph)

    markdown(
r'''
# 同次座標系 (Homogeneous coordinate system)

三次元デカルト座標系(*Cartesian coordinate system*)における点の座標の**同次座標**(*Homogeneous coordinate*)は，任意の非零実数${w}$を用いて変換されます。

$${fHomogeneous}\left({pc}, {w}\right) = {ph}$$

同次座標を用いた座標系のことを**同次座標系**(*Homogeneous coordinate system*)と呼びます．

逆に，同次座標をデカルト座標に変換することもできます。

$${fCartesian}\left({ph}\right) = {pc2}$$''',
             
             **locals())

# Homogeneous変換とCartesian変換が逆変換であることを記号的に検証
if __name__ == '__main__':
    p = Vec3(x, y, z)
    if cmdline.symtest:
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
# Implementation
    global impl_scale

    Scales = sp.var('s_x s_y s_z')
    Scale = sp.diag(*Scales, 1)  # 記号的拡大縮小行列
    impl_scale = mat32(Scales, Scale)

# Documentation of the implementation
    fScale = sp.Function('Scale')(*Scales)
    Scale_ph = Scale * ph
    Scale_pc = Cartesian(Scale_ph)

    markdown(
r'''
## 拡大縮小変換: ${fScale}$

以下の行列 ${fScale}$ に同次座標を乗ずると，その座標の$X$-, $Y$-, $Z$-成分をそれぞれ${Scales}$倍した同次座標を与えます．

$${fScale} = {Scale}$$''', **locals())

# Symbolic test
    assert_lhs = Cartesian(Scale * Homogeneous(pc, w))
    assert_rhs = Vec3(s_x * x, s_y * y, s_z * z)
    if cmdline.symtest:
        assert(sp.Eq(assert_lhs, assert_rhs))

    markdown(
r'''
実際に確認してみると、確かにそのとおりになっていることがわかります。

\begin{align}
{fScale} {fHomogeneous}\left({pc}\right)
    &= {Scale} {ph}  \\
    &= {Scale_ph} = {fHomogeneous}\left({Scale_pc}\right)
\end{align}''', **locals())

def scale(sx:float, sy:float, sz:float) -> np.ndarray:
    '(X, Y, Z)-軸について、それぞれ(sx, sy, sz)倍するモデル変換行列を与える'
    return impl_scale(sx, sy, sz)


######################################################################

@doit
def __rotate__():
# Implementation
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

    # test 1. 原点からの距離は変化しないこと（ノルムの二乗が等しいこと）
    pcpc, pxpx = pc.dot(pc), px.dot(px)
    if cmdline.symtest:
        assert(sp.simplify(sp.Eq(pcpc, pxpx)))

    # test 2. 移動前後のベクトルの差分はX軸に直交すること
    if cmdline.symtest:
        assert(sp.simplify(sp.Eq((px-pc).dot(axisX), 0)))

    proj = px.dot(axisX) * axisX
    # test 3. v1 = (pc - proj) と v2 = (px - proj) がなす角度がθであること
    v1, v2 = pc - proj, px - proj
    l1, l2 = sp.sqrt(v1.T.dot(v1)), sp.simplify(sp.sqrt(v2.T.dot(v2)))
    iprod_v1v2 = v1.dot(v2)
    iprod_v1v2_simplified = sp.simplify(iprod_v1v2)

    cos_theta=sp.cos(theta)
    l1_l2_cos_theta = l1 * l2 * cos_theta

    if cmdline.symtest:
        assert(sp.simplify(sp.Eq(iprod_v1v2, l1_l2_cos_theta)))

# Documentation of the implementation
    markdown('## 回転変換: ${}, {}, {}$', *fRotate)

    for axis, fRot, Rot in zip('X Y Z'.split(), fRotate, Rotate):
        markdown(
'''
- 回転変換行列 (${fRot}$) に同次座標を乗ずると，その座標を${axis}$軸のまわりに${theta}$だけ回転した点の同次座標を与えます．

    $${fRot} {ph} = {Rot} {ph} = {result}$$''',
                 
                 result=Rot * ph, **locals())

    fRotX = fRotate[0]
    RotateX = Rotate[0]
    px = sp.simplify(Cartesian(RotateX * ph))
    pcpc = pc.dot(pc)
    pxpx = sp.simplify(px.dot(px))
    px_pc = px - pc
    movex_axisX=px_pc.dot(axisX)

    markdown(
r'''
では、ここで得られた変換${fRotX}$が確かに回転であることを確認してみよう。この変換で点$p$が$p'$に移ったものとすると：

\begin{align}
p &= {pc} \\
p' &= {px}
\end{align}

+ 変換前後でベクトルと原点の距離は変化しないこと

    \begin{align}
    \|p\|^2 &= \left\|{v1}\right\|^2 = {pcpc} \\
    \|p'\|^2 &= \left\|{v2}\right\|^2 = {pxpx}
    \end{align}

+ 変換前後のベクトルの差分が回転軸となるX軸と直交すること

    $p$をX軸を中心として回転するとき、その回転のあいだ$p$はX軸と直交する平面を移動します。したがって、移動後の$p'$もそのX軸と直交する平面にあるはずです。$p, p'$がともにX軸と直交する平面上の点ということは、$p' - p$はこの平面上のベクトルということになるので、X軸と直交するはずです。

    $$\left({px_pc}, {axisX}\right) = {movex_axisX}$$

    内積が0なので直交していることが確認できました。

+ 回転角が確かに${theta}$であること

    X軸を中心として$p$を${theta}$回転して$p'$に移すということは、$p$と$p'$のなす角度が${theta}$というような気もしますが、実はそうではありません。ベクトル$p$は円錐の表面を撫でるようにして$p'$に写るからです。${theta}$となるのは、$p$からX軸への垂線の足となる$p_x$について$p$と$p'$がなす角度です。

    では、まず$p_x$を求めてみましょう。これをベクトルだと思うとX軸方向の単位ベクトル${axisX}$と同じ向きで、長さが前述の垂線の足にあたる点と原点の距離です。この距離は$p$と${axisX}$の内積で与えられますので、結局$p_x = (p_x, {axisX}) {axisX} = {proj}$となります。

    角度が${theta}$であることは($p-p_x$)と($p'-p_x$)の内積に関する性質について確認すればよいでしょう。

    \begin{align}
    (p - p_x, p' - p_x) &= ({v1}, {v2}) \\
        &= {iprod_v1v2} \\
        &= {iprod_v1v2_simplified}
    \end{align}

    一方、$p-p_x$と$p'-p_x$のなす角が{theta}ならば、その内積は$\ell_1 \ell_2 {cos_theta}$になるはずです。

    \begin{align}
    \ell_1 &= \|p - p_x\| = {l1} \\
    \ell_2 &= \|p' - p_x\| = {l2} \\
    \ell_1 \ell_2 {cos_theta} &= {l1} {l2} {cos_theta} = {l1_l2_cos_theta}
    \end{align}

    以上より$(p-p_x, p'-p_x) = \ell_1 \ell_2 {cos_theta}$が確認できました。''',
             **locals())

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
# Implementation
    global impl_translate

    Translates = sp.var('t_x t_y t_z')
    fTranslate = sp.Function('Translate')(*Translates)
    Translate = sp.eye(3).row_join(sp.Matrix(Translates)).col_join(sp.Matrix([[0, 0, 0, 1]]))

    impl_translate = mat32(Translates, Translate)

# Documentation of the implementation
    vTranslates = Vec3(*Translates)
    Translate_ph = Translate * ph
    Translate_pc = Cartesian(Translate_ph)

    markdown(
r'''## 並行移動変換: {fTranslate}

以下の行列 ${fTranslate}$ に同次座標を乗じたものは，デカルト座標を${Translates}$だけ平行移動したものの同次座標を与えます．

ここで平行移動を表す行列${fTranslate}$は以下で与えられます．

$$ {fTranslate} = {Translate} $$

では，本当に平行移動になっているか確認してみましょう．

\begin{align}
{fTranslate}{fHomogeneous}\left({pc}\right)
    &= {Translate} {ph} \\
    &= {Translate_ph} = {fHomogeneous}\left({pc} + {vTranslates}\right)
\end{align}
''', **locals())

# Symbolic test
    if cmdline.symtest:
        assert(sp.simplify(sp.Eq(Translate_pc, pc + vTranslates)))

    gsym.tx, gsym.ty, gsym.tz = Translates
    gsym.Translate = Translate

def translate(tx:float, ty:float, tz:float) -> np.ndarray:
    '(tx, ty, tz)だけ並行移動するモデル変換行列を与える'
    impl_translate(tx, ty, tz)

@doit
def __lookat__():
    global impl_lookat
# Implementation
    LookAtVectors = [Eye, Side, Head, Forward] = [
        sp.var('I_x I_y I_z'), sp.var('S_x S_y S_z'),
        sp.var('H_x H_y H_z'), sp.var('F_x F_y F_z')]
    [I, S, H, F] = [sp.Matrix(3, 1, M) for M in LookAtVectors]

    LookAtTranslate = gsym.Translate.subs({ gsym.tx: -I_x, gsym.ty: -I_y, gsym.tz: -I_z })
    invLookAtRotate = sp.Matrix(sp.BlockMatrix([[S, H, -F, sp.zeros(3, 1)]])).col_join(sp.Matrix([[0, 0, 0, 1]]))
    LookAtRotate = invLookAtRotate.T  # 回転行列は正規直交行列なので，逆行列は転置行列

    LookAt = LookAtRotate * LookAtTranslate
    impl_lookat = mat32(Eye + Forward + Side + Head, LookAt)

# Documentation

    mLookAtRotate, mLookAtTranslate = sp.var('LookAtRotate LookAtTranslate')

    markdown(
r'''
### 視野変換 (LookAt)

視野変換は**全体座標系** (*Global coordinate system*)に配置されたオブジェクトを観察者の立場から眺めたときの様子，すなわち**視野座標系**(*Viewing coordinate system*)に変換します．観察者の立ち位置を表現するために観察者の視点(*eye*)，観察者の視線の先の点(*center*)，そして観察者の頭の向き(*up*)を与えます．

視野変換は全体座標系を視点に平行移動する変換${mLookAtTranslate}$と，視線の向きを$Z$軸方向から視線の向きに回転する
変換${mLookAtRotate}$を合成(${mLookAtRotate} \times {mLookAtTranslate}$)したものと考えられます．''', **locals())

    fTranslate = sp.latex(sp.Function('Translate'))
    eye = sp.Symbol('eye')

    markdown(r'''
### 視点へのカメラの移動 (LookAtTranslate)
最初の変換は視点($I$; 眼の eye になぞらえてこの記号を使います)を原点に平行移動します．移動のベクトルは$(0 - I) = -I$ですので：

$${mLookAtTranslate} = {fTranslate}\left(-{I}\right) = {LookAtTranslate}$$''', **locals())

    Ih = Homogeneous(I)
    LookAtTranslate_Ih = LookAtTranslate * Ih

    markdown(r'''
念のため、${mLookAtTranslate}$が視点($I$)を原点に移動することを確認しましょう．

\begin{align}
{mLookAtTranslate} \times {fHomogeneous}\left({I}\right) &= {LookAtTranslate} \times {Ih} \\
    &= {LookAtTranslate_Ih}
\end{align}
    
確かに原点に移動しました．''', **locals())

# Symbolic test
    pass

def lookat(eye: np.ndarray, center: np.ndarray, up: np.ndarray) -> np.ndarray:
    i = eye
    f = normalize(center - eye)
    s = normalize(np.cross(f, up))
    h = np.cross(s, f)
    return impl_lookat(*i, *f, *s, *h)
