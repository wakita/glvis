from OpenGL.GL import *
from OpenGL.arrays.arraydatatype import *
import re

Datatype_CommandPrefix = '''# Table 11.3@p. 366, OpenGL 4.5 (Core Profile) - May 28, 2015
int    glVertexAttribI1i
ivec2  glVertexAttribI2i
ivec3  glVertexAttribI2i
ivec4  glVertexAttribI2i
uint   glVertexAttribI1ui
uvec2  glVertexAttribI2ui
uvec3  glVertexAttribI2ui
uvec4  glVertexAttribI2ui
float  glVertexAttrib1
vec2   glVertexAttrib2
vec3   glVertexAttrib3
vec4   glVertexAttrib4
double glVertexAttribL1d
dvec2  glVertexAttribL2d
dvec3  glVertexAttribL3d
dvec4  glVertexAttribL4d'''.split('\n')

Datatype_CommandPrefix = [ tuple(re.compile(' +').split(line)) for line in Datatype_CommandPrefix if line[0] != '#']

VertexAttribNames = '''
void glVertexAttrib1f(	GLuint index,
 	GLfloat v0);
 
void glVertexAttrib1s(	GLuint index,
 	GLshort v0);
 
void glVertexAttrib1d(	GLuint index,
 	GLdouble v0);
 
void glVertexAttribI1i(	GLuint index,
 	GLint v0);
 
void glVertexAttribI1ui(	GLuint index,
 	GLuint v0);
 
void glVertexAttrib2f(	GLuint index,
 	GLfloat v0,
 	GLfloat v1);
 
void glVertexAttrib2s(	GLuint index,
 	GLshort v0,
 	GLshort v1);
 
void glVertexAttrib2d(	GLuint index,
 	GLdouble v0,
 	GLdouble v1);
 
void glVertexAttribI2i(	GLuint index,
 	GLint v0,
 	GLint v1);
 
void glVertexAttribI2ui(	GLuint index,
 	GLuint v0,
 	GLuint v1);
 
void glVertexAttrib3f(	GLuint index,
 	GLfloat v0,
 	GLfloat v1,
 	GLfloat v2);
 
void glVertexAttrib3s(	GLuint index,
 	GLshort v0,
 	GLshort v1,
 	GLshort v2);
 
void glVertexAttrib3d(	GLuint index,
 	GLdouble v0,
 	GLdouble v1,
 	GLdouble v2);
 
void glVertexAttribI3i(	GLuint index,
 	GLint v0,
 	GLint v1,
 	GLint v2);
 
void glVertexAttribI3ui(	GLuint index,
 	GLuint v0,
 	GLuint v1,
 	GLuint v2);
 
void glVertexAttrib4f(	GLuint index,
 	GLfloat v0,
 	GLfloat v1,
 	GLfloat v2,
 	GLfloat v3);
 
void glVertexAttrib4s(	GLuint index,
 	GLshort v0,
 	GLshort v1,
 	GLshort v2,
 	GLshort v3);
 
void glVertexAttrib4d(	GLuint index,
 	GLdouble v0,
 	GLdouble v1,
 	GLdouble v2,
 	GLdouble v3);
 
void glVertexAttrib4Nub(	GLuint index,
 	GLubyte v0,
 	GLubyte v1,
 	GLubyte v2,
 	GLubyte v3);
 
void glVertexAttribI4i(	GLuint index,
 	GLint v0,
 	GLint v1,
 	GLint v2,
 	GLint v3);
 
void glVertexAttribI4ui(	GLuint index,
 	GLuint v0,
 	GLuint v1,
 	GLuint v2,
 	GLuint v3);
 
void glVertexAttribL1d(	GLuint index,
 	GLdouble v0);
 
void glVertexAttribL2d(	GLuint index,
 	GLdouble v0,
 	GLdouble v1);
 
void glVertexAttribL3d(	GLuint index,
 	GLdouble v0,
 	GLdouble v1,
 	GLdouble v2);
 
void glVertexAttribL4d(	GLuint index,
 	GLdouble v0,
 	GLdouble v1,
 	GLdouble v2,
 	GLdouble v3);
 
void glVertexAttrib1fv(	GLuint index,
 	const GLfloat *v);
 
void glVertexAttrib1sv(	GLuint index,
 	const GLshort *v);
 
void glVertexAttrib1dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttribI1iv(	GLuint index,
 	const GLint *v);
 
void glVertexAttribI1uiv(	GLuint index,
 	const GLuint *v);
 
void glVertexAttrib2fv(	GLuint index,
 	const GLfloat *v);
 
void glVertexAttrib2sv(	GLuint index,
 	const GLshort *v);
 
void glVertexAttrib2dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttribI2iv(	GLuint index,
 	const GLint *v);
 
void glVertexAttribI2uiv(	GLuint index,
 	const GLuint *v);
 
void glVertexAttrib3fv(	GLuint index,
 	const GLfloat *v);
 
void glVertexAttrib3sv(	GLuint index,
 	const GLshort *v);
 
void glVertexAttrib3dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttribI3iv(	GLuint index,
 	const GLint *v);
 
void glVertexAttribI3uiv(	GLuint index,
 	const GLuint *v);
 
void glVertexAttrib4fv(	GLuint index,
 	const GLfloat *v);
 
void glVertexAttrib4sv(	GLuint index,
 	const GLshort *v);
 
void glVertexAttrib4dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttrib4iv(	GLuint index,
 	const GLint *v);
 
void glVertexAttrib4bv(	GLuint index,
 	const GLbyte *v);
 
void glVertexAttrib4ubv(	GLuint index,
 	const GLubyte *v);
 
void glVertexAttrib4usv(	GLuint index,
 	const GLushort *v);
 
void glVertexAttrib4uiv(	GLuint index,
 	const GLuint *v);
 
void glVertexAttrib4Nbv(	GLuint index,
 	const GLbyte *v);
 
void glVertexAttrib4Nsv(	GLuint index,
 	const GLshort *v);
 
void glVertexAttrib4Niv(	GLuint index,
 	const GLint *v);
 
void glVertexAttrib4Nubv(	GLuint index,
 	const GLubyte *v);
 
void glVertexAttrib4Nusv(	GLuint index,
 	const GLushort *v);
 
void glVertexAttrib4Nuiv(	GLuint index,
 	const GLuint *v);
 
void glVertexAttribI4bv(	GLuint index,
 	const GLbyte *v);
 
void glVertexAttribI4ubv(	GLuint index,
 	const GLubyte *v);
 
void glVertexAttribI4sv(	GLuint index,
 	const GLshort *v);
 
void glVertexAttribI4usv(	GLuint index,
 	const GLushort *v);
 
void glVertexAttribI4iv(	GLuint index,
 	const GLint *v);
 
void glVertexAttribI4uiv(	GLuint index,
 	const GLuint *v);
 
void glVertexAttribL1dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttribL2dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttribL3dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttribL4dv(	GLuint index,
 	const GLdouble *v);
 
void glVertexAttribP1ui(	GLuint index,
 	GLenum type,
 	GLboolean normalized,
 	GLuint value);
 
void glVertexAttribP2ui(	GLuint index,
 	GLenum type,
 	GLboolean normalized,
 	GLuint value);
 
void glVertexAttribP3ui(	GLuint index,
 	GLenum type,
 	GLboolean normalized,
 	GLuint value);
 
void glVertexAttribP4ui(	GLuint index,
 	GLenum type,
 	GLboolean normalized,
 	GLuint value);'''.split('\n')

VertexAttribNames = [ line[5:].split('(')[0] for line in VertexAttribNames if line[:4] == 'void']

# str -> set(Functions) --- glVertexAttrib*
Datatype_Functions = dict()

for datatype, _ in Datatype_CommandPrefix:
    Datatype_Functions[datatype] = set()

re1234 = re.compile('[1234]')
for name in VertexAttribNames:
    # 関数の名称から関数本体を OpenGL.GL モジュールより取得
    f = getattr(OpenGL.GL, name)
    # 関数が要求するデータ数をその arity 属性に保存するハック (e.g., glVertexAttrib2f.arity = 2)
    f.arity = int(re1234.search(name)[0])
    for datatype, command_prefix in Datatype_CommandPrefix:
        if name.startswith(command_prefix):
            Datatype_Functions[datatype].add(f)

def lookup(datatype, *signature):
    sig0 = signature[0]
    if (type(sig0) == list):
        for f in Datatype_Functions[datatype]:
            fsignature = f.argtypes[1:]
            fsig0 = fsignature[0]
            if not issubclass(fsig0, ArrayDatatype): continue
            assert (len(signature), len(fsignature)) == (1, 1)
            if len(sig0) == f.arity and (sig0[0], fsig0) == (GL_FLOAT, GLfloatArray):
                return f
    else:
        for f in Datatype_Functions[datatype]:
            fsig0 = f.argtypes[1]
            for sig in signature[1:]:
                assert sig0 == sig
            for _, t in ARRAY_TYPE_TO_CONSTANT:
                if t == sig0:
                    if (sig0, fsig0) in [
                        (GL_SHORT, ctypes.c_short),
                        (GL_FLOAT, ctypes.c_float),
                        (GL_DOUBLE, ctypes.c_double)]:
                        return f

if __name__ == '__main__':
    GL_FLOATS2 = [GL_FLOAT, GL_FLOAT]
    GL_FLOATS3 = [GL_FLOAT, *GL_FLOATS2]
    GL_FLOATS4 = [GL_FLOAT, *GL_FLOATS3]

    assert lookup('float', GL_SHORT)    == glVertexAttrib1s
    assert lookup('float', GL_FLOAT)    == glVertexAttrib1f
    assert lookup('float', GL_DOUBLE)   == glVertexAttrib1d
    assert lookup('vec2',  *GL_FLOATS2) == glVertexAttrib2f
    assert lookup('vec3',  *GL_FLOATS3) == glVertexAttrib3f
    assert lookup('vec4',  *GL_FLOATS4) == glVertexAttrib4f
    assert lookup('vec2',  GL_FLOATS2)  == glVertexAttrib2fv, lookup('vec2', GL_FLOATS2)
    assert lookup('vec3',  GL_FLOATS3)  == glVertexAttrib3fv
    assert lookup('vec4',  GL_FLOATS4)  == glVertexAttrib4fv
