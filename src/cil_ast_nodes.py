class AST:
    def __init__(self):
        pass

class Program(AST):
    def __init__(self):
        super(Program, self).__init__()
        self.types = [] # list of AST.Type
        self.data = [] # list of AST.Data
        self.code = [] # list of AST.Function
    
    def __str__(self):
        text = '.TYPES'

        for type in self.types:
            text += f'\n\n{type}'
        
        text += '\n\n.DATA'

        for data in self.data:
            text += f'\n\n{data}'
        
        text += '\n\n.CODE'

        for code in self.code:
            text += f'\n\n{code}'
        
        return text

class Type(AST):
    def __init__(self, name, atrributes, methods):
        super(Type, self).__init__()
        self.name = name
        self.attributes = atrributes
        self.methods = methods
    
    def __str__(self):
        text = f'type {self.name} {{'
        
        for attr in self.attributes:
            text += f'\n    {attr}'

        for method in self.methods:
            text += f'\n    {method}'
        
        text += '\n}'

        return text

class Attribute(AST):
    def __init__(self, name):
        super(Attribute, self).__init__()
        self.name = name
    
    def __str__(self):
        return f'attribute {self.name};'

class Method(AST):
    def __init__(self, method_name, cil_function):
        super(Method, self).__init__()
        self.method_name = method_name
        self.cil_function = cil_function

    def __str__(self):
        return f'method {self.method_name}: {self.cil_function};'