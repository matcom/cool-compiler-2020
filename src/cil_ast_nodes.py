import visitor

class AST:
    def __init__(self):
        pass

    def __repr__(self):
        return str(self)

class Program(AST):
    def __init__(self, dottypes, dotdata, dotcode):
        super(Program, self).__init__()
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode
    
    def __str__(self):
        def scape_special_chars(s):
            special_chars = [('\n', 'n'), ('\r', 'r'), ('\t', 't'), ('\b', 'b'), ('\f', 'f')]
            for schar, char in special_chars:
                s = s.replace(schar, f'\\{char}', len(s))
            return s

        text = '.TYPES'

        for type in self.types:
            text += f'\n\n{type}'
        
        text += '\n\n.DATA\n'

        for string, var in self.data:
            string = scape_special_chars(string)
            text += f'\n{var} = "{string}";' 
        
        text += self.data and '\n\n.CODE' or '\n.CODE'

        for code in self.code:
            text += f'\n\n{code}'
        
        return text

class Type(AST):
    def __init__(self, name):
        super(Type, self).__init__()
        self.name = name
        self.attributes = []
        self.methods = []

    def __str__(self):
        text = f'type {self.name} {{'
        
        for attr in self.attributes:
            text += f'\n    {attr}'

        for method in self.methods:
            text += f'\n    {method}'
        
        text += '\n}'

        return text

class DataNode(AST):
    def __init__(self, vname, value):
        super(DataNode, self).__init__()
        self.name = vname
        self.value = value

# ?
class Attribute(AST):
    def __init__(self, name):
        super(Attribute, self).__init__()
        self.name = name
    
    def __str__(self):
        return f'attribute {self.name};'

# ?
class Method(AST):
    def __init__(self, name, virtual_type):
        super(Method, self).__init__()
        self.name = name
        self.virtual_type = virtual_type

    def __str__(self):
        return f'method {self.virtual_type}_{self.name}: func_{self.virtual_type}_{self.name};'

class Function(AST):
    def __init__(self, name, params=[], localvars=[], instructions =[], labels = []):
        super(Function, self).__init__()
        self.name = name
        self.params = params # list of Param
        self.localvars = localvars # list of LocalDec
        self.instructions = instructions # list of Instructions
        self.labels = labels
    
    def __str__(self):
        # params = '\n\t'.join(x for x in self.params)
        # localvars = '\n\t'.join(x.name for x in self.localvars)
        # instructions = '\n\t'.join(x for x in self.instructions)

        return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

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
        return f'SETATTR {self.instance} {self.attr} {self.value};'

class VCall(Expr):
    def __init__(self, dest, itype, vtype, method, params_count):
        self.local_dest = dest
        self.instance_type = itype
        self.virtual_type = vtype
        self.method = method
        self.params_count = params_count
    
    def __str__(self):
        return f'VCALL {self.instance_type} {self.virtual_type}_{self.method};'

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
    def __init__(self, local_dest, right_expr):
        self.local_dest = local_dest
        self.right_expr = right_expr
    
    def __str__(self):
        return f'{self.local} = {self.right_expr}'

class BinaryOperator(Expr):
    def __init__(self, local_dest, left, right):
        self.local_dest = local_dest
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
    def __init__(self, t, dest):
        self.type = t
        self.local_dest = dest
    
    def __str__(self):
        return f'ALLOCATE {self.type};'

class TypeOf(Expr):
    def __init__(self, variable, local_dest):
        self.variable = variable
        self.local_dest = local_dest

class Call(Expr):
    def __init__(self, function, local_dest):
        self.function = function
        self.local_dest = local_dest

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
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f'RETURN {self.expr}'

class Load(Expr):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return f'LOAD {self.msg};'

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



def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(Program)
        def visit(self, node):
            print("DOTTYPES LEN:", len(node.dottypes))
            print("DOTDATA LEN:", len(node.dotdata))
            print("DOTCODE LEN:", len(node.dotcode))
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes.values())
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(Type)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(Function)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(ParamDec)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalDec)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(Assign)
        def visit(self, node):
            return f'{node.local_dest} = {node.right_expr}'

        @visitor.when(IfGoto)
        def visit(self, node):
            return f'IF {node.variable} GOTO {node.label}'
        
        @visitor.when(Label)
        def visit(self, node):
            return f'LABEL {node.label}'
        
        @visitor.when(Goto)
        def visit(self, node):
            return f'GOTO {node.label}'



        @visitor.when(Plus)
        def visit(self, node):
            return f'{node.local_dest} = {node.left} + {node.right}'

        @visitor.when(Minus)
        def visit(self, node):
            return f'{node.local_dest} = {node.left} - {node.right}'

        @visitor.when(Star)
        def visit(self, node):
            return f'{node.local_dest} = {node.left} * {node.right}'

        @visitor.when(Div)
        def visit(self, node):
            return f'{node.local_dest} = {node.left} / {node.right}'

        @visitor.when(Allocate)
        def visit(self, node):
            return f'{node.local_dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOf)
        def visit(self, node):
            return f'{node.local_dest} = TYPEOF {node.variable}'

        @visitor.when(Call)
        def visit(self, node):
            return f'{node.local_dest} = CALL {node.function}'

        @visitor.when(VCall)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.instance_type} {node.virtual_type}_{node.method}'

        @visitor.when(Arg)
        def visit(self, node):
            return f'ARG {node.arg}'

        @visitor.when(Return)
        def visit(self, node):
            return f'\n RETURN {node.value if node.value is not None else ""}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))