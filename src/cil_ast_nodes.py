class AST:
    def __init__(self):
        pass

class Program(AST):
    def __init__(self):
        super(Program, self).__init__()
        self.types = [] # list of AST.Type
        self.data = {}  # string, name dict, ex "Hello": "s3"
        self.code = [] # list of AST.Function
    
    def __str__(self):
        def scape_special_chars(s):
            special_chars = [('\n', 'n'), ('\r', 'r'), ('\t', 't')]
            for schar, char in special_chars:
                s = s.replace(schar, f'\\{char}', len(s))
            return s

        text = '.TYPES'

        for type in self.types:
            text += f'\n\n{type}'
        
        text += '\n\n.DATA\n'

        for string, var in self.data.items():
            string = scape_special_chars(string)
            text += f'\n{var} = "{string}";' 
        
        text += self.data.items() and '\n\n.CODE' or '\n.CODE'

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