#!/bin/env python3

import os
from pathlib import PurePath
import sys
import sympy as sp

project_root = PurePath('d:/wakita/work/glvis')
doc_root = project_root.joinpath('doc', 'note')

class LaTeXMath(object):
    def __init__(self, *xs, delimiters=['{\\(', '\\)}']):
        self.delimiters = delimiters
        self.elements = [isinstance(x, str) and x or '{' + sp.latex(x) + '}' for x in xs]

    @classmethod
    def simple(cls, *xs):
        return cls(*xs)

    @classmethod
    def display(cls, *xs):
        return cls(*xs, delimiters=['\n\\[', '\\]\n' ])

def math(*xs):
    return LaTeXMath.simple(*xs)

def Math(*xs):
    return LaTeXMath.display(*xs)

class Markdown(object):
    def __init__(self, output=None):
        self.output = output

    def __enter__(self):
        output = self.output
        if output is None:
            self.w = sys.stdout
        else:
            p = str(doc_root.joinpath(output.replace('.', '/') + '.md'))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            self.w = open(p, 'w')
        self.md(
'''---
layout: symdoc
title: "Documentation of the {output} package"
---
'''.format(output=output))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.w.close()

    def md(self, *xs):
        s = []
        for x in xs:
            if isinstance(x, (sp.Basic, sp.MutableDenseMatrix, tuple)):
                s.append(sp.latex(x))
            elif isinstance(x, str):
                s.append(x)
            elif isinstance(x, (int, float)):
                s.append(str(x))
            elif isinstance(x, LaTeXMath):
                s.extend([x.delimiters[0], *x.elements, x.delimiters[1]])
            else: print(type(x))
        self.w.write(''.join(s))
        self.w.write('\n')

def _subs(EXPR, repl):
    return EXPR.subs(repl, simultaneous=True)
