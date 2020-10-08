class AST:
    def __init__(self):
        pass

class Program(AST):
    def __init__(self):
        super(Program, self).__init__()
        self.types = [] # list of AST.Type
        self.data = [] # list of AST.Data
        self.code = [] # list of AST.Function

class Type(AST):
    def __init__(self, name, atrributes, methods):
        super(Type, self).__init__()
        self.name = name
        self.attributes = atrributes
        self.methods = methods

class Attribute(AST):
    def __init__(self, name):
        super(Attribute, self).__init__()
        self.name = name

class Method(AST):
    def __init__(self, method_name, cil_function):
        super(Method, self).__init__()
        self.method_name = method_name
        self.cil_function = cil_function
