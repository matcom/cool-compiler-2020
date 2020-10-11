class AST:
    def __init__(self):
        pass

    def __repr__(self):
        return str(self)

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

class Function(AST):
    def __init__(self, name, params=[], locals=[], body=[]):
        super(Function, self).__init__()
        self.name = name
        self.params = params # list of Param
        self.locals = locals # list of LocalDec
        self.body = body # list of Line
    
    def __str__(self):
        text = f'function {self.name} {{'
        
        for line in self.params:
            text += f'\n    {line}'
        
        for line in self.locals:
            text += f'\n    {line}'

        for line in self.body:
            text += f'\n    {line}'

        text += '\n}'

        return text

class Expr(AST):
    def __init__(self):
        super(Expr, self).__init__()

class ParamDec(Expr):
    def __init__(self, name):
        super(ParamDec, self).__init__()
        self.name = name
    
    def __str__(self):
        return f'PARAM {self.name};'

class LocalDec(Expr):
    def __init__(self, name):
        super(LocalDec, self).__init__()
        self.name = name
    
    def __str__(self):
        return f'LOCAL {self.name};'

class Halt(Expr):
    def __init__(self):
        super(Halt, self).__init__()
    
    def __str__(self):
        return 'HALT;'

class GetAttr(Expr):
    def __init__(self, instance, attr):
        self.instance = instance
        self.attr = attr

class SetAttr(Expr):
    def __init__(self, instance, attr, value):
        super(SetAttr, self).__init__()
        self.instance = instance
        self.attr = attr
        self.value = value
    
    def __str__(self):
        return f'SETATTR {self.type} {self.attr} {self.value};'

class Allocate(Expr):
    def __init__(self, instance_name, type):
        super(Allocate, self).__init__()
        self.instance_name = instance_name
        self.type = type
    
    def __str__(self):
        return f'{self.instance_name} = ALLOCATE {self.type};'

class VCall(Expr):
    def __init__(self, _type, function, params_count):
        self.type = _type
        self.function = function
        self.params_count = params_count

class AssignVCall(Expr):
    def __init__(self, var_name, type, method):
        super(AssignVCall, self).__init__()
        self.var_name = var_name
        self.type = type
        self.method = method

class INTEGER(Expr):
    def __init__(self, value):
        super(INTEGER, self).__init__()
        self.value = value
    
    def __str__(self):
        return f'{self.value};'

class STRING(Expr):
    def __init__(self, value):
        super(STRING, self).__init__()
        self.value = value
    
    def __str__(self):
        return f'{self.value};'

class Assign(Expr):
    def __init__(self, local, right_expr):
        self.local = local
        self.right_expr = right_expr
    
    def __str__(self):
        return f'{self.local} = {self.right_expr}'

class BinaryOperator(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Plus(BinaryOperator):
    pass

class Minus(BinaryOperator):
    pass

class Star(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Allocate(Expr):
    def __init__(self, type):
        self.type = type

class TypeOf(Expr):
    def __init__(self, variable):
        self.variable = variable

class Call(Expr):
    def __init__(self, function):
        self.function = function

class Param(Expr):
    def __init__(self, param, shift = 0):
        self.param = param
        self.shift = shift

class Arg(Expr):
    def __init__(self, arg):
        self.arg = arg
    
    def __str__(self):
        return f'ARG {self.arg};'

class Case(Expr):
    def __init__(self, local_typeof, types_list, label_list):
        self.local_typeof = local_typeof
        self.types_list = types_list
        self.label_list = label_list

class IfGoto(Expr):
    def __init__(self, variable, label):
        self.variable = variable
        self.label = label

class Goto(Expr):
    def __init__(self, label):
        self.label = label

class Label(Expr):
    def __init__(self, label):
        self.label = label

class Return(Expr):
    def __init__(self, variable):
        self.variable = variable

class Load(Expr):
    def __init__(self, msg):
        self.msg = msg

class Length(Expr):
    def __init__(self, variable):
        self.variable = variable

class Concat(Expr):
    def __init__(self, local1, local2):
        self.string1 = local1
        self.string2 = local2

class StringVar(Expr):
    def __init__(self, variable):
        self.variable = variable

class SubStr(Expr):
    def __init__(self, i, j, string):
        self.i = i
        self.j = j
        self.string = string

class Read(Expr):
    pass

class ReadString(Read):
    pass

class ReadInteger(Read):
    pass

class Print(Expr):
    def __init__(self, variable):
        self.variable = variable

class PrintString(Print):
    pass

class PrintInteger(Print):
    pass

class Compare(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class IsVoid(Expr):
    def __init__(self, local):
        self.local = local

class Equals(Compare):
    pass

class EqualsString(Compare):
    pass
    
class LessThan(Compare):
    pass
    
class LessThanEquals(Compare):
    pass