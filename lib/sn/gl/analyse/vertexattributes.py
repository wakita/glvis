from   .common import *
from   ..raw.vertexattrib import lookup as lookup_vertex_attrib

class A(Analyse):
    vertex_attribute_handler = dict([
        (GL_FLOAT_VEC2, glVertexAttrib2f),
        (GL_FLOAT_VEC3, glVertexAttrib3f),
        (GL_FLOAT_VEC4, glVertexAttrib4f)])

    def __init__(self, *args):
        logging.debug('__init__@ProgramVertexAttributes')
        self.a = dict()
        super().__init__()

    def examine(self):
        p = self._program
        logging.debug('examine@ProgramVertexAttributes({})'.format(p))

        n = sp.zeros(1, dtype=sp.int32)
        glGetProgramInterfaceiv(p, GL_PROGRAM_INPUT, GL_ACTIVE_RESOURCES, n)
        if sn_logging.log_on_shader_variables():
            logging.info('#vertex attributes = {0}'.format(n[0]))

        types = list(self.vertex_attribute_handler.keys())
        properties = sp.array([GL_NAME_LENGTH, GL_TYPE, GL_LOCATION])

        bbuf = bytes(256)
        info = sp.zeros(3, dtype=sp.int32)
        lengths = sp.zeros(1, dtype=sp.int32)
        a = self.a
        for attr in range(n[0]):
            glGetProgramResourceiv(p, GL_PROGRAM_INPUT, attr,
                                   3, properties, 3, lengths,
                                   info)
            logging.info('length = {0}, info = {1}'.format(lengths, info))
            glGetProgramResourceName(p, GL_PROGRAM_INPUT, attr, len(bbuf), lengths, bbuf)
            location = info[2]
            if location == -1:
                continue
            name = bbuf[:lengths[0]].decode('utf-8')
            typestr = '???'
            try:
                typestr = types[types.index(info[1])].__repr__()
                f = self.vertex_attribute_handler[info[1]]
                a[name] = (lambda *args, f=f, l=location: f(*([l] + list(args))))
            except: pass
            if sn_logging.log_on_shader_variables():
                logging.info('attribute {0}:{1}@{2}'.format(name, typestr, location))
            a[name].name, a[name].loc, a[name].type = name, location, info[1]
            # assumption: vec3 in pos_vs
            # pos_vs_f = prog.vertexAttrib('pos_vs', GL_Float, GL_Float, GL_Float) => glVertexAttrib1f)
            # pos_vs_f(1.0, 1.0)
            # pos_vs_sv = prog.vertexAttrib('pos_vs', [GL_Short, GL_Short, GL_Short]) => glVertexAttrib1sv)
            # pos_vs_sv(sp.array([1, 1]), dtype=sp.short)

        super().examine()

    def vertexAttrib(self, name, *signature):
        attr = self.a[name]
        loc = attr.loc
        f = lookup_vertex_attrib(attr.type, *signature)
        return lambda *args, loc=loc: f(loc, *args)
