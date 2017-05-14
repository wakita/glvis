import logging
from sn.qt import *
from sn.gl import *

from OpenGL.GL.NVX.gpu_memory_info import *


def show(constants, n=None):
    if n is not None:
        for c in constants:
            logging.info('    {0}: {1}'.format(c, [glGetIntegeri_v(c, i)[0] for i in range(n)]))
    else:
        for c in constants:
            try:
                v = glGetIntegerv(c)
                logging.info('    {0}: {1}'.format(c, v))
            except:
                logging.info('    {0}: ???'.format(c))
    logging.info('')


class KW3(GLWidget):
    def initializeGL(self):
        GLWidget.printGLInfo()

        logging.info('GPU memory (NVX)')
        show([
          GL_GPU_MEMORY_INFO_DEDICATED_VIDMEM_NVX,
          GL_GPU_MEMORY_INFO_TOTAL_AVAILABLE_MEMORY_NVX,
          GL_GPU_MEMORY_INFO_CURRENT_AVAILABLE_VIDMEM_NVX,
          GL_GPU_MEMORY_INFO_EVICTION_COUNT_NVX,
          GL_GPU_MEMORY_INFO_EVICTED_MEMORY_NVX])

        logging.info('Generic limits')
        show([
            GL_MAX_SUBROUTINE_UNIFORM_LOCATIONS,
            GL_MAX_COMBINED_ATOMIC_COUNTERS,
            GL_MAX_COMBINED_SHADER_STORAGE_BLOCKS,
            GL_MAX_PROGRAM_TEXEL_OFFSET,
            GL_MIN_PROGRAM_TEXEL_OFFSET,
            GL_MAX_COMBINED_UNIFORM_BLOCKS,
            GL_MAX_UNIFORM_BUFFER_BINDINGS,
            GL_MAX_UNIFORM_BLOCK_SIZE,
            GL_MAX_UNIFORM_LOCATIONS,
            GL_MAX_VARYING_COMPONENTS,
            GL_MAX_VARYING_VECTORS,
            GL_MAX_VARYING_FLOATS,
            GL_MAX_SHADER_STORAGE_BUFFER_BINDINGS,
            GL_MAX_SHADER_STORAGE_BLOCK_SIZE,
            GL_MAX_COMBINED_SHADER_OUTPUT_RESOURCES,
            GL_SHADER_STORAGE_BUFFER_OFFSET_ALIGNMENT,
            GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT,
            GL_NUM_PROGRAM_BINARY_FORMATS,
            GL_NUM_SHADER_BINARY_FORMATS,
            GL_PROGRAM_BINARY_FORMATS])

        logging.info('Vertex shader information')
        show([
          GL_MAX_VERTEX_ATOMIC_COUNTERS,
          GL_MAX_VERTEX_SHADER_STORAGE_BLOCKS,
          GL_MAX_VERTEX_ATTRIBS,
          GL_MAX_VERTEX_OUTPUT_COMPONENTS,
          GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS,
          GL_MAX_VERTEX_UNIFORM_COMPONENTS,
          GL_MAX_VERTEX_UNIFORM_VECTORS,
          GL_MAX_VERTEX_UNIFORM_BLOCKS,
          GL_MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS])

        logging.info('Geometry shader information')
        show([
          GL_MAX_GEOMETRY_ATOMIC_COUNTERS,
          GL_MAX_GEOMETRY_SHADER_STORAGE_BLOCKS,
          GL_MAX_GEOMETRY_INPUT_COMPONENTS,
          GL_MAX_GEOMETRY_OUTPUT_COMPONENTS,
          GL_MAX_GEOMETRY_TEXTURE_IMAGE_UNITS,
          GL_MAX_GEOMETRY_UNIFORM_BLOCKS,
          GL_MAX_GEOMETRY_UNIFORM_COMPONENTS,
          GL_MAX_COMBINED_GEOMETRY_UNIFORM_COMPONENTS,
          GL_MAX_VERTEX_STREAMS])

        logging.info('Tessellation control shader information')
        show([
          GL_MAX_TESS_CONTROL_ATOMIC_COUNTERS,
          GL_MAX_TESS_CONTROL_SHADER_STORAGE_BLOCKS,
          GL_MAX_TESS_CONTROL_INPUT_COMPONENTS,
          GL_MAX_TESS_CONTROL_OUTPUT_COMPONENTS,
          GL_MAX_TESS_CONTROL_TEXTURE_IMAGE_UNITS,
          GL_MAX_TESS_CONTROL_UNIFORM_BLOCKS,
          GL_MAX_TESS_CONTROL_UNIFORM_COMPONENTS,
          GL_MAX_COMBINED_TESS_CONTROL_UNIFORM_COMPONENTS])
        self.close()

        logging.info('Tessellation evaluation shader information')
        show([
          GL_MAX_TESS_EVALUATION_ATOMIC_COUNTERS,
          GL_MAX_TESS_EVALUATION_SHADER_STORAGE_BLOCKS,
          GL_MAX_TESS_EVALUATION_INPUT_COMPONENTS,
          GL_MAX_TESS_EVALUATION_OUTPUT_COMPONENTS,
          GL_MAX_TESS_EVALUATION_TEXTURE_IMAGE_UNITS,
          GL_MAX_TESS_EVALUATION_UNIFORM_BLOCKS,
          GL_MAX_TESS_EVALUATION_UNIFORM_COMPONENTS,
          GL_MAX_COMBINED_TESS_EVALUATION_UNIFORM_COMPONENTS])

        logging.info('Computation shader limits')
        show([
          GL_MAX_COMPUTE_SHADER_STORAGE_BLOCKS,
          GL_MAX_COMPUTE_UNIFORM_BLOCKS,
          GL_MAX_COMPUTE_TEXTURE_IMAGE_UNITS,
          GL_MAX_COMPUTE_IMAGE_UNIFORMS,
          GL_MAX_COMPUTE_UNIFORM_COMPONENTS,
          GL_MAX_COMBINED_COMPUTE_UNIFORM_COMPONENTS,
          GL_MAX_COMPUTE_ATOMIC_COUNTERS,
          GL_MAX_COMPUTE_ATOMIC_COUNTER_BUFFERS,
          GL_MAX_COMPUTE_SHARED_MEMORY_SIZE,
          GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS])
        show([
          GL_MAX_COMPUTE_WORK_GROUP_COUNT,
          GL_MAX_COMPUTE_WORK_GROUP_SIZE], n=3)

        logging.info('Puling information')
        show([
          GL_MAX_ELEMENTS_INDICES,
          GL_MAX_ELEMENTS_VERTICES,
          GL_MAX_VERTEX_ATTRIB_RELATIVE_OFFSET,
          GL_MAX_VERTEX_ATTRIB_BINDINGS,
          GL_MAX_ELEMENT_INDEX])

        logging.info('Rasterizer information')
        show([
          GL_SUBPIXEL_BITS,
          GL_MAX_CLIP_DISTANCES,
          GL_MAX_VIEWPORTS,
          GL_VIEWPORT_SUBPIXEL_BITS])

        logging.info('Framebuffer information')
        show([
          GL_MAX_COLOR_ATTACHMENTS,
          GL_MAX_FRAMEBUFFER_WIDTH,
          GL_MAX_FRAMEBUFFER_HEIGHT,
          GL_MAX_FRAMEBUFFER_LAYERS,
          GL_MAX_FRAMEBUFFER_SAMPLES,
          GL_MAX_RENDERBUFFER_SIZE,
          GL_MAX_SAMPLE_MASK_WORDS])

        logging.info('Buffer information')
        show([
          GL_MAX_TRANSFORM_FEEDBACK_BUFFERS,
          GL_MIN_MAP_BUFFER_ALIGNMENT])

        logging.info('Texture information')
        show([
          GL_MAX_TEXTURE_IMAGE_UNITS,
          GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS,
          GL_MAX_TEXTURE_LOD_BIAS,
          GL_MAX_TEXTURE_SIZE,
          GL_MAX_RECTANGLE_TEXTURE_SIZE,
          GL_MAX_3D_TEXTURE_SIZE,
          GL_MAX_ARRAY_TEXTURE_LAYERS,
          GL_MAX_CUBE_MAP_TEXTURE_SIZE,
          GL_MAX_COLOR_TEXTURE_SAMPLES,
          GL_MAX_DEPTH_TEXTURE_SAMPLES,
          GL_MAX_INTEGER_SAMPLES,
          GL_MAX_TEXTURE_BUFFER_SIZE,
          GL_NUM_COMPRESSED_TEXTURE_FORMATS
          # GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT
          ])

        logging.info('Program information')
        show([
          GL_MAX_SUBROUTINES,
          GL_MAX_SUBROUTINE_UNIFORM_LOCATIONS,
          GL_MAX_COMBINED_ATOMIC_COUNTERS,
          GL_MAX_COMBINED_SHADER_STORAGE_BLOCKS,
          GL_MAX_PROGRAM_TEXEL_OFFSET,
          GL_MIN_PROGRAM_TEXEL_OFFSET,
          GL_MAX_COMBINED_UNIFORM_BLOCKS,
          GL_MAX_UNIFORM_BUFFER_BINDINGS,
          GL_MAX_UNIFORM_BLOCK_SIZE,
          GL_MAX_UNIFORM_LOCATIONS,
          GL_MAX_VARYING_COMPONENTS,
          GL_MAX_VARYING_VECTORS,
          GL_MAX_VARYING_FLOATS,
          GL_MAX_SHADER_STORAGE_BUFFER_BINDINGS,
          GL_MAX_SHADER_STORAGE_BLOCK_SIZE,
          GL_MAX_COMBINED_SHADER_OUTPUT_RESOURCES,
          GL_SHADER_STORAGE_BUFFER_OFFSET_ALIGNMENT,
          GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT,
          GL_NUM_PROGRAM_BINARY_FORMATS,
          GL_NUM_SHADER_BINARY_FORMATS,
          GL_PROGRAM_BINARY_FORMATS])

if __name__ == '__main__':
    app = Application()
    widget = KW3()
    app.run()
