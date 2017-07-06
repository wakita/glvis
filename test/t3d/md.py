#!/bin/env python3

import argparse
import os
from pathlib import PurePath
import sys
import sympy as sp

project_root = PurePath('{}/glvis'.format(os.environ['WORK']))
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
    @staticmethod
    def add_parser_option(parser):
        parser.add_argument('--symdoc', dest='symdoc', action='store_true')

    def __init__(self, output=None, **kwds):
        if output is None:
            self.output = None
            self.w = sys.stdout
        else:
            self.output = str(doc_root.joinpath(output.replace('.', '/') + '.md'))
            os.makedirs(os.path.dirname(self.output), exist_ok=True)
            self.w = open(self.output, 'w')
        kwds.setdefault('layout', 'page')
        kwds.setdefault('title', output or '???')
        self.markdown('---\n{}\n---\n', '\n'.join(['{}: {}'.format(k, v) for k, v in kwds.items()]))

    def __del__(self):
        if self.output is not None:
            print('closing ' + self.output)
        self.w.close()

    @staticmethod
    def convert(x):
        if isinstance(x, (sp.Basic, sp.MutableDenseMatrix, tuple)):
            return sp.latex(x)
        elif isinstance(x, str):
            return x
        elif isinstance(x, (int, float)):
            return str(x)
        else: pass

    def markdown(self, document, *xs, **kwds):
        xs = [Markdown.convert(x) for x in xs]
        kwds = dict([(k, Markdown.convert(v)) for k, v in kwds.items()])
        self.w.write(document.format(*xs, **kwds) + '\n\n')

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
