from md import Markdown, math, Math
import sympy as sp

if __name__ == '__main__':
    with Markdown('test.t3d.t3d') as markdown:
        md = markdown.md

        VEC3 = sp.Matrix(sp.var('X Y Z'))
        md('今、', Math(VEC3), Math((VEC3, VEC3)), Math(X, Y, Z), 'が熱い！')
