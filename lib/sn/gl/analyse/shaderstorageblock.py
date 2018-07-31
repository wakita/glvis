from .common import *

class A(Analyse):
    def __init__(self, *args):
        logging.debug('__init__@ProgramShaderStorageBlock')
        self.ssb = dict()
        super().__init__()

    def examine(self):
        logging.debug('examine@ProgramShaderStorageBlock')
        p = self._program
        ssb = self.ssb

        glGetProgramInterfaceiv(p, GL_SHADER_STORAGE_BLOCK, GL_ACTIVE_RESOURCES, pointer(glres))
        active_blocks = glres.val
        logging.info('#active shader storage block(s) = {}'.format(active_blocks))

        ssb_info = SSBlockInformation()
        ssb_varinfo = SSBVariableInformation()
        for block in range(active_blocks):
            ssb_info.query(p, GL_SHADER_STORAGE_BLOCK, block)
            logging.info('block = {}, name length = {}, #active variables = {}'.format( block, ssb_info.name_length, ssb_info.num_active_variables))
            logging.info('buffer binding = {}, buffer data size = {}'.format(
                ssb_info.buffer_binding, ssb_info.buffer_data_size))

            # Retrieving an active SS-Block name
            name = resource_name(p, GL_SHADER_STORAGE_BLOCK, block, ssb_info.name_length)
            logging.info('Shader storage block name: "{}"'.format(name))
            ssb[name] = block

            variables = sp.zeros(ssb_info.num_active_variables, dtype=sp.int32)
            glGetProgramResourceiv(p, GL_SHADER_STORAGE_BLOCK, block, 1,
                                   [GL_ACTIVE_VARIABLES], ssb_info.num_active_variables, pointer(glres), variables)
            logging.info('Active variables: {}'.format(variables))

            # Retrieving indices of the active member variables
            for var in variables:
                ssb_varinfo.query(p, GL_BUFFER_VARIABLE, var)
                logging.info('{}'.format([ssb_varinfo.type, ssb_varinfo.array_size,
                                          ssb_varinfo.offset, ssb_varinfo.array_stride,
                                          ssb_varinfo.name_length,
                                          ssb_varinfo.top_level_array_size]))
                var_name = resource_name(p, GL_BUFFER_VARIABLE, var, ssb_varinfo.name_length)
                logging.info('active variable[{}]: length: {}, name: "{}"'.format(
                    var, ssb_varinfo.name_length,  var_name))

        super().examine()

