---
layout: page
title: T3D (Transform 3D) for Python
---



# 同次座標系 (Homogeneous coordinate system)

三次元デカルト座標系(*Cartesian coordinate system*)における点の座標の**同次座標**(*Homogeneous coordinate*)は，任意の非零実数$w$を用いて変換されます。

$$Homogeneous\left(\left[\begin{matrix}x\\y\\z\end{matrix}\right], w\right) = \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right]$$

同次座標を用いた座標系のことを**同次座標系**(*Homogeneous coordinate system*)と呼びます．

逆に，同次座標をデカルト座標に変換することもできます。

$$Cartesian\left(\left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right]\right) = \left[\begin{matrix}x\\y\\z\end{matrix}\right]$$

# モデル変換

## 拡大縮小変換: $\operatorname{Scale}{\left (s_{x},s_{y},s_{z} \right )}$

以下の拡大縮小変換行列 $\operatorname{Scale}{\left (s_{x},s_{y},s_{z} \right )}$ に同次座標を乗ずると，その座標の$X$-, $Y$-, $Z$-成分をそれぞれ$\left ( s_{x}, \quad s_{y}, \quad s_{z}\right )$倍した同次座標を与えます．

$$\operatorname{Scale}{\left (s_{x},s_{y},s_{z} \right )} = \left[\begin{matrix}s_{x} & 0 & 0 & 0\\0 & s_{y} & 0 & 0\\0 & 0 & s_{z} & 0\\0 & 0 & 0 & 1\end{matrix}\right]$$

実際に確認してみると、確かにそのとおりになっていることがわかります。

\begin{align}
\operatorname{Scale}{\left (s_{x},s_{y},s_{z} \right )} Homogeneous\left(\left[\begin{matrix}x\\y\\z\end{matrix}\right]\right)
    &= \left[\begin{matrix}s_{x} & 0 & 0 & 0\\0 & s_{y} & 0 & 0\\0 & 0 & s_{z} & 0\\0 & 0 & 0 & 1\end{matrix}\right] \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right]  \\
    &= \left[\begin{matrix}s_{x} w x\\s_{y} w y\\s_{z} w z\\w\end{matrix}\right] = Homogeneous\left(\left[\begin{matrix}s_{x} x\\s_{y} y\\s_{z} z\end{matrix}\right]\right)
\end{align}


## 回転変換: $\operatorname{Rotate_{X}}{\left (\theta \right )}, \operatorname{Rotate_{Y}}{\left (\theta \right )}, \operatorname{Rotate_{Z}}{\left (\theta \right )}$


- 回転変換行列 ($\operatorname{Rotate_{X}}{\left (\theta \right )}$) に同次座標を乗ずると，その座標を$X$軸のまわりに$\theta$だけ回転した点の同次座標を与えます．

    $$\operatorname{Rotate_{X}}{\left (\theta \right )} \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right] = \left[\begin{matrix}1 & 0 & 0 & 0\\0 & \cos{\left (\theta \right )} & \sin{\left (\theta \right )} & 0\\0 & - \sin{\left (\theta \right )} & \cos{\left (\theta \right )} & 0\\0 & 0 & 0 & 1\end{matrix}\right] \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right] = \left[\begin{matrix}w x\\w y \cos{\left (\theta \right )} + w z \sin{\left (\theta \right )}\\- w y \sin{\left (\theta \right )} + w z \cos{\left (\theta \right )}\\w\end{matrix}\right]$$


- 回転変換行列 ($\operatorname{Rotate_{Y}}{\left (\theta \right )}$) に同次座標を乗ずると，その座標を$Y$軸のまわりに$\theta$だけ回転した点の同次座標を与えます．

    $$\operatorname{Rotate_{Y}}{\left (\theta \right )} \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right] = \left[\begin{matrix}\cos{\left (\theta \right )} & 0 & - \sin{\left (\theta \right )} & 0\\0 & 1 & 0 & 0\\\sin{\left (\theta \right )} & 0 & \cos{\left (\theta \right )} & 0\\0 & 0 & 0 & 1\end{matrix}\right] \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right] = \left[\begin{matrix}w x \cos{\left (\theta \right )} - w z \sin{\left (\theta \right )}\\w y\\w x \sin{\left (\theta \right )} + w z \cos{\left (\theta \right )}\\w\end{matrix}\right]$$


- 回転変換行列 ($\operatorname{Rotate_{Z}}{\left (\theta \right )}$) に同次座標を乗ずると，その座標を$Z$軸のまわりに$\theta$だけ回転した点の同次座標を与えます．

    $$\operatorname{Rotate_{Z}}{\left (\theta \right )} \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right] = \left[\begin{matrix}\cos{\left (\theta \right )} & \sin{\left (\theta \right )} & 0 & 0\\- \sin{\left (\theta \right )} & \cos{\left (\theta \right )} & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{matrix}\right] \left[\begin{matrix}w x\\w y\\w z\\w\end{matrix}\right] = \left[\begin{matrix}w x \cos{\left (\theta \right )} + w y \sin{\left (\theta \right )}\\- w x \sin{\left (\theta \right )} + w y \cos{\left (\theta \right )}\\w z\\w\end{matrix}\right]$$


では、ここで得られた変換$\operatorname{Rotate_{X}}{\left (\theta \right )}$が確かに回転であることを確認してみよう。この変換で点$p$が$p'$に移ったものとすると：

\begin{align}
p &= \left[\begin{matrix}x\\y\\z\end{matrix}\right] \\
p' &= \left[\begin{matrix}x\\y \cos{\left (\theta \right )} + z \sin{\left (\theta \right )}\\- y \sin{\left (\theta \right )} + z \cos{\left (\theta \right )}\end{matrix}\right]
\end{align}

+ 変換前後でベクトルと原点の距離は変化しないこと

    \begin{align}
    \|p\|^2 &= \left\|\left[\begin{matrix}0\\y\\z\end{matrix}\right]\right\|^2 = x^{2} + y^{2} + z^{2} \\
    \|p'\|^2 &= \left\|\left[\begin{matrix}0\\y \cos{\left (\theta \right )} + z \sin{\left (\theta \right )}\\- y \sin{\left (\theta \right )} + z \cos{\left (\theta \right )}\end{matrix}\right]\right\|^2 = x^{2} + y^{2} + z^{2}
    \end{align}

+ 変換前後のベクトルの差分が回転軸となるX軸と直交すること

    $p$をX軸を中心として回転するとき、その回転のあいだ$p$はX軸と直交する平面を移動します。したがって、移動後の$p'$もそのX軸と直交する平面にあるはずです。$p, p'$がともにX軸と直交する平面上の点ということは、$p' - p$はこの平面上のベクトルということになるので、X軸と直交するはずです。

    $$\left(\left[\begin{matrix}0\\y \cos{\left (\theta \right )} - y + z \sin{\left (\theta \right )}\\- y \sin{\left (\theta \right )} + z \cos{\left (\theta \right )} - z\end{matrix}\right], \left[\begin{matrix}1\\0\\0\end{matrix}\right]\right) = 0$$

    内積が0なので直交していることが確認できました。

+ 回転角が確かに$\theta$であること

    X軸を中心として$p$を$\theta$回転して$p'$に移すということは、$p$と$p'$のなす角度が$\theta$というような気もしますが、実はそうではありません。ベクトル$p$は円錐の表面を撫でるようにして$p'$に写るからです。$\theta$となるのは、$p$からX軸への垂線の足となる$p_x$について$p$と$p'$がなす角度です。

    では、まず$p_x$を求めてみましょう。これをベクトルだと思うとX軸方向の単位ベクトル$\left[\begin{matrix}1\\0\\0\end{matrix}\right]$と同じ向きで、長さが前述の垂線の足にあたる点と原点の距離です。この距離は$p$と$\left[\begin{matrix}1\\0\\0\end{matrix}\right]$の内積で与えられますので、結局$p_x = (p_x, \left[\begin{matrix}1\\0\\0\end{matrix}\right]) \left[\begin{matrix}1\\0\\0\end{matrix}\right] = \left[\begin{matrix}x\\0\\0\end{matrix}\right]$となります。

    角度が$\theta$であることは($p-p_x$)と($p'-p_x$)の内積に関する性質について確認すればよいでしょう。

    \begin{align}
    (p - p_x, p' - p_x) &= (\left[\begin{matrix}0\\y\\z\end{matrix}\right], \left[\begin{matrix}0\\y \cos{\left (\theta \right )} + z \sin{\left (\theta \right )}\\- y \sin{\left (\theta \right )} + z \cos{\left (\theta \right )}\end{matrix}\right]) \\
        &= y \left(y \cos{\left (\theta \right )} + z \sin{\left (\theta \right )}\right) + z \left(- y \sin{\left (\theta \right )} + z \cos{\left (\theta \right )}\right) \\
        &= \left(y^{2} + z^{2}\right) \cos{\left (\theta \right )}
    \end{align}

    一方、$p-p_x$と$p'-p_x$のなす角が\thetaならば、その内積は$\ell_1 \ell_2 \cos{\left (\theta \right )}$になるはずです。

    \begin{align}
    \ell_1 &= \|p - p_x\| = \sqrt{y^{2} + z^{2}} \\
    \ell_2 &= \|p' - p_x\| = \sqrt{y^{2} + z^{2}} \\
    \ell_1 \ell_2 \cos{\left (\theta \right )} &= \sqrt{y^{2} + z^{2}} \sqrt{y^{2} + z^{2}} \cos{\left (\theta \right )} = \left(y^{2} + z^{2}\right) \cos{\left (\theta \right )}
    \end{align}

    以上より$(p-p_x, p'-p_x) = \ell_1 \ell_2 \cos{\left (\theta \right )}$が確認できました。

$$\left[\begin{matrix}\frac{1}{w} \left(t_{x} w + w x\right)\\\frac{1}{w} \left(t_{y} w + w y\right)\\\frac{1}{w} \left(t_{z} w + w z\right)\end{matrix}\right] = \left[\begin{matrix}t_{x} + x\\t_{y} + y\\t_{z} + z\end{matrix}\right]$$

## 並行移動変換: \operatorname{Translate}{\left (t_{x},t_{y},t_{z} \right )}

