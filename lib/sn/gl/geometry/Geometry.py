#!/usr/bin/env python

from collections import defaultdict
import os, os.path, sys
import numpy as np

np.set_printoptions(precision=4)

root_path = os.path.join(os.path.normpath(os.environ['DROPBOX']), 'work', 'pyqt')
sys.path.append(os.path.join(root_path, 'lib'))

def demo(Demo):
    try: Demo.start(Demo)
    except: pass

def Point():
    from sn.gl.geometry.point import D
    demo(D)

def RegularPolygon():
    from sn.gl.geometry.regularpolygon import D
    demo(D)

def PointGrid():
    from sn.gl.geometry.pointgrid import D
    demo(D)

d = defaultdict(lambda: lambda: None)
d['Point'] = Point
d['RegularPolygon'] = RegularPolygon
d['PointGrid'] = PointGrid

for arg in sys.argv[1:]: d[arg]()
