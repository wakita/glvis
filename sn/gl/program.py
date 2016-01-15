import re, sys
from PyQt5 import QtGui, QtOpenGL, QtWidgets
from OpenGL.GL import *
from OpenGL.GL.shaders import *

from sn.gl.globject import GLObject
from sn.qt import (Application, GLWidget)

class Program(GLObject):
    shadertypes = dict(
            vs       = GL_VERTEX_SHADER,
            vert     = GL_VERTEX_SHADER,
            vertex   = GL_VERTEX_SHADER,
            tcs      = GL_TESS_CONTROL_SHADER,
            tesscontrol
                     = GL_TESS_CONTROL_SHADER,
            tessellationcontrol
                     = GL_TESS_CONTROL_SHADER,
            tes      = GL_TESS_EVALUATION_SHADER,
            tesseval = GL_TESS_EVALUATION_SHADER,
            tessevaluation
                     = GL_TESS_EVALUATION_SHADER,
            tessellationevaluation
                     = GL_TESS_EVALUATION_SHADER,
            gs       = GL_GEOMETRY_SHADER,
            geometry = GL_GEOMETRY_SHADER,
            fs       = GL_FRAGMENT_SHADER,
            fragment = GL_FRAGMENT_SHADER,
            cs       = GL_COMPUTE_SHADER,
            compute  = GL_COMPUTE_SHADER)

    def __init__(self, path):
        self.load(path)
        self.create()
        self.compile()

    def __del__(self):
        self.delete()

    def delete(self):
        if self._program and bool(glDeleteProgram):
            p = self._program; self._program = None
            glDeleteProgram(p)

    def load(self, path):
        shadertypes = self.shadertypes
        shaderset = []
        kind = None; code = []
        with open(path, 'r') as f:
            for line in f:
                k = ''.join(line.strip('#\n').split(' ')).lower().replace('shader', '')
                if k in shadertypes.keys():
                    if kind != None:
                        shaderset.append((kind, ''.join(code)))
                    kind = shadertypes[k]; code = []
                else:
                    code.append(line)
        if kind != None:
            shaderset.append((kind, ''.join(code)))
        self._shaderset = shaderset

    def create(self):
        self._program = glCreateProgram()
        self._validated = self._linked = False
        self._variables = dict(vertex=set(), uniform=set())
        self._samplers = {}
        self._known_invalid = set()

    def compile(self):
        self._linked = False
        program = self._program
        shaderlist = []
        for t, code in self._shaderset:
            shader = glCreateShader(t)
            shaderlist.append(shader)
            glShaderSource(shader, code)
            glCompileShader(shader)
            if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                errors = str(glGetShaderInfoLog(shader), 'utf-8')
                msg = self._get_error(code, errors, 4)
                raise RuntimeError('Shader compilation failure error in {0}:\n{1}'
                        .format(t, msg))
            glAttachShader(program, shader)

        glLinkProgram(program)
        if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError('Program linking error:\n{0}'
                    .format(glGetProgramInfoLog(program).decode('utf-8')))
        for shader in shaderlist:
            glDetachShader(program, shader)
            glDeleteShader(shader)
        self._linked = True

    def _get_error(self, code, errors, indentation=0):
        results = []
        lines = None
        if code is not None:
            lines = [line.strip() for line in code.split('\n')]

        for error in errors.split('\n'):
            #error = error.split()
            if not error:
                continue

            lineno, error = self._parse_error(error)
            if None in (lineno, lines):
                results.append(str(error))
            else:
                results.append('on line {0}: {1}'.format(lineno, error))
                if lineno > 0 and lineno < len(lines):
                    results.append('  {0}'.format(lines[lineno - 1]))
        results = [' ' * indentation + r for r in results]
        return '\n'.join(results)

    def _parse_error(self, error):
        error = str(error)
        # Nvidia
        # 0(7): error C1008: undefined variable "MV"
        m = re.match(r'(\d+)\((\d+)\)\s*:\s(.*)', error)
        if m:
            return int(m.group(2)), m.group(3)
        # ATI / Intel
        # ERROR: 0:131: '{' : syntax error parse error
        m = re.match(r'ERROR:\s(\d+):(\d+):\s(.*)', error)
        if m:
            return int(m.group(2)), m.group(3)
        # Nouveau
        # 0:28(16): error: syntax error, unexpected ')', expecting '('
        m = re.match(r'(\d+):(\d+)\((\d+)\):\s(.*)', error)
        if m:
            return int(m.group(2)), m.group(4)
        # Other ...
        return None, error

    def use(self):
        glUseProgram(self._program)

if __name__ == '__main__':

    from sn.qt import (Application, GLWidget)

    class Test(GLWidget):
        def initializeGL(self):
            super(self.__class__, self).initializeGL()
            self.program = Program('program.shaders')

    app = Application()
    window = Test(None)
    window.show()
    sys.exit(app.exec_())
