import numpy as np

#import OpenGL
#OpenGL.ERROR_CHEKING = True
#OpenGL.FULL_LOGGING = True
from OpenGL.GL import *

from .program import Program, open_ssb, allocate_ssb, dispatch_cs
from .globject import VertexArray, VertexBuffer
