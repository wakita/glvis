import IPython.display as Display
import sympy as sp

_Document_ = {}

def md(*args):
    s = ''
    for x in args:
        if (isinstance(x, sp.Basic) or isinstance(x, sp.MutableDenseMatrix) or isinstance(x, tuple)):
            s = s + sp.latex(x)
        elif (isinstance(x, str)): s = s + x
        elif (isinstance(x, int) or isinstance(x, float)): s = s + str(x)
        else: print(type(x))
    Display.display_markdown(s, raw=True)

def line(name, *args):
  def conv(x):
    if (isinstance(x, sp.Basic) or
        isinstance(x, sp.MutableDenseMatrix) or
        isinstance(x, tuple)): return sp.latex(x)
    elif isinstance(x, str): return x
    else: print(type(x))

  line = [ conv(x) for x in args ]
  try:
    _Document_[name].append(line)
  except:
    _Document_[name] = [line]

def document(name):
  for line in _Document_[name]:
    Display.display_markdown(''.join(line), raw=True)

def _subs(EXPR, repl):
    return EXPR.subs(repl, simultaneous=True)
