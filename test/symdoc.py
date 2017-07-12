#!/bin/env python3

import argparse
import os
from pathlib import PurePath
import sys
import sympy as sp

project_root = PurePath('{}/glvis'.format(os.environ['WORK']))
doc_root = project_root.joinpath('doc', 'note')

def doit(f):
    f()
    return f

def symfunc(f):
    name = f.__name__
    setattr(gsym, 'f' + name, name)
    return f

class SymdocSymbols(object): pass
gsym = SymdocSymbols()
gsym.align = '{align}'

class Markdown(object):
    cmdline_parser = None

    def __init__(self, output=None, **kwds):
        self.cmdline = self.cmdline_parser.parse_args(sys.argv[1:])
        if self.cmdline.symdoc:
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
        if self.cmdline.symdoc:
            self.w.close()

    @classmethod
    def add_parser_option(cls, cmdline_parser):
        cls.cmdline_parser = cmdline_parser
        cmdline_parser.add_argument('--symdoc', dest='symdoc', action='store_true')
        cmdline_parser.add_argument('--symtest', dest='symtest', action='store_true')

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
        if self.cmdline.symdoc:
            xs = [Markdown.convert(x) for x in xs]
            kwds = dict([(k, Markdown.convert(v)) for k, v in kwds.items()])
            _gsym = dict([(k, Markdown.convert(v)) for k, v in vars(gsym).items()])
            self.w.write(document.format(*xs, **kwds, **_gsym) + '\n\n')
