
class NodeIL():
    pass

class ProgramNodeIL(NodeIL):
    def __init__(self, dottypes, dotdata, dotcode, idx=None):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode
        self.index = idx

    def __str__(self):
        dottypes = '\n'.join(str(t) for t in self.dottypes)
        dotdata = '\n'.join(str(t) for t in self.dotdata)
        dotcode = '\n'.join(str(t) for t in self.dotcode)

        return ".TYPES\n{}\n.DATA\n{}\n.CODE\n{}".format(dottypes, dotdata, dotcode)

class TypeNodeIL(NodeIL):
    def __init__(self, name, atributes=None, methods=None, idx=None):
        self.name = name
        self.attributes = atributes if atributes is not None else []
        self.methods = methods if methods is not None else []
        self.index = idx

    def __str__(self):
        attributes = "\n\t"
        methods = "\n\t"
        for x,y in self.attributes:
            attributes += ("attribute {}: {}".format(x,y))
        
        for x,y in self.methods:
            methods += ("method {}: {}".format(x,y))

        return ("type {} {{{}\n\t{}\n\t}}".format(self.name, attributes, methods))

class DataNodeIL(NodeIL):
    def __init__(self, vname, value, idx=None):
        self.name = vname
        self.value = value
        self.index = idx

    def __str__(self):
        return str(self.name) + " = " + '"' + str(node.value) + '"'


class FunctionNodeIL(NodeIL):
    def __init__(self, fname, params, localvars, instructions, idx=None):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.index = idx

    def __str__(self):
        params = "\n".join(str(x) for x in self.params)
        localvars = "\n".join(str(x) for x in self.localvars)
        instruction = "\n".join(str(x) for x in self.instructions)

        return ("function {}\n {{\n\t{}\n\n\t{}\n\n\t{}}}".format(self.name, params, localvars, instructions))

class ParamNodeIL(NodeIL):
    def __init__(self, name, typex=None, idx=None):
        self.name = name
        self.type = typex
        self.index = idx

    def __str__(self):
        return ("PARAM {}".format(self.name))

class LocalNodeIL(NodeIL):
    def __init__(self, name, idx=None):
        self.name = name
        self.index = idx
    
    def __str__(self):
        return ("LOCAL {}".format(self.name))

class HaltNodeIL(NodeIL):
    
    def __str__(self):
        return 'HALT;'

class InstructionNodeIL(NodeIL):
    def __init__(self, idx=None):
        self.in1 = None
        self.in2 = None
        self.out = None
        self.index = idx