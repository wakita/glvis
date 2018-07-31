from   ctypes import *

import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *

class ProgramResource(Structure):
    @staticmethod
    def specs(specs):
        return [(name, c_uint) for name, _ in specs], [feature for _, feature in specs]

    def bufinfo(self):
        return len(self._features_), self._features_, sizeof(self), glres.pointer(), self.pointer()

    def pointer(self):
        return pointer(self)

    def query(self, p, interface, target):
        glGetProgramResourceiv(p, interface, target,
                               len(self._features_), self._features_,
                               sizeof(self), glres.pointer(), pointer(self))


class UINT(ProgramResource):
    _fields_, _features_ = ProgramResource.specs([('val', c_uint)])


glres = UINT()


class SSBlockInformation(ProgramResource):
    _fields_, _features_ = ProgramResource.specs([
        ('name_length', GL_NAME_LENGTH),
        ('num_active_variables', GL_NUM_ACTIVE_VARIABLES),
        ('buffer_binding', GL_BUFFER_BINDING),
        ('buffer_data_size', GL_BUFFER_DATA_SIZE)])


class SSBVariableInformation(ProgramResource):
    _fields_, _features_ = ProgramResource.specs([
        ('type', GL_TYPE),
        ('array_size', GL_ARRAY_SIZE),
        ('offset', GL_OFFSET),
        ('array_stride', GL_ARRAY_STRIDE),
        ('name_length', GL_NAME_LENGTH),
        ('top_level_array_size', GL_TOP_LEVEL_ARRAY_SIZE)])
