import numpy as np
from OpenGL.GL import *

class Volume(object):
    def __init__(self):
        self._va = va = glGenVertexArrays(1)
        glBindVertexArray(va)

    def bind(self):
        glBindVertexArray(self._va)
