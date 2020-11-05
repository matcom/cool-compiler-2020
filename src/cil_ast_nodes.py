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
        self.methods = {}

    def __str__(self):
        text = f'type {self.name} {{'
        
        for attr in self.attributes:
            text += f'\n    {attr}'

        for method in self.methods:
            text += f'\n    {method}'
        
        text += '\n}'

        return text


class Function(AST):
    def __init__(self, name, params=[], localvars=[], instructions =[]):
        super(Function, self).__init__()
        self.name = name
        self.params = params # list of Param
        self.localvars = localvars # list of LocalDec
        self.instructions = instructions # list of Instructions
    
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
    def __init__(self, dest, instance, attr, static_type):
        self.instance = instance
        self.attr = attr
        self.local_dest = dest
        self.static_type = static_type

class SetAttr(Expr):
    def __init__(self,instance, attr, value, static_type):
        self.instance = instance
        self.attr = attr
        self.value = value
        self.static_type = static_type
    
    def __str__(self):
        return f'SETATTR {self.instance} {self.attr} {self.value};'

class Call(Expr):
    def __init__(self, local_dest, function, params, static_type):
        self.function = function
        self.params = params
        self.static_type = static_type
        self.local_dest = local_dest
        

class VCall(Expr):
    def __init__(self, local_dest, function, params, dynamic_type, instance):
        self.function = function
        self.params = params
        self.dynamic_type = dynamic_type
        self.local_dest = local_dest
        self.instance = instance
    
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

class UnaryOperator(Expr):
    def __init__(self, local_dest, expr_value, op):
        self.local_dest = local_dest
        self.expr_value = expr_value
        self.op = op

class BinaryOperator(Expr):
    def __init__(self, local_dest, left, right, op):
        self.local_dest = local_dest
        self.left = left
        self.right = right
        self.op = op

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

class LoadInt(Expr):
    def __init__(self, num, dest):
        self.num = num
        self.local_dest = dest

class LoadStr(Expr):
    def __init__(self, msg, dest):
        self.msg = msg
        self.local_dest = dest
    
    def __str__(self):
        return f'LOAD {self.msg};'

class Length(Expr):
    def __init__(self, variable, result):
        self.variable = variable
        self.result = result

class Concat(Expr):
    def __init__(self, local1, local2, result):
        self.string1 = local1
        self.string2 = local2
        self.result = result

class StringVar(Expr):
    def __init__(self, variable):
        self.variable = variable

class SubStr(Expr):
    def __init__(self, i, length, string, result):
        self.i = i
        self.length = length
        self.string = string
        self.result = result

class Read(Expr):
    def __init__(self, result):
        self.result = result

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


class IsVoid(Expr):
    def __init__(self, result_local, expre_value):
        self.result_local = result_local
        self.expre_value = expre_value

class Copy(Expr):
    def __init__(self, type, local_dest):
        self.type = type
        self.local_dest = local_dest



def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(Program)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes.values())
            dotdata = '\n'.join(f'{t}: {node.dotdata[t]}' for t in node.dotdata.keys())
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(Type)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x} : {node.methods[x]}' for x in node.methods.keys())

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

        @visitor.when(UnaryOperator)
        def visit(self, node):
            return f'{node.local_dest} = {node.op} {node.expr_value}'

        @visitor.when(BinaryOperator)
        def visit(self, node):
            return f'{node.local_dest} = {node.left} {node.op} {node.right}'

        @visitor.when(Allocate)
        def visit(self, node):
            return f'{node.local_dest} = ALLOCATE {node.type}'

        @visitor.when(LoadStr)
        def visit(self, node):
            return f'{node.local_dest} = LOAD {node.msg}'

        @visitor.when(LoadInt)
        def visit(self, node):
            return f'{node.local_dest} = LOAD {node.num}'

        @visitor.when(GetAttr)
        def visit(self, node):
            return f'{node.local_dest} = GetAttr {node.instance} {node.attr} '

        @visitor.when(SetAttr)
        def visit(self, node):
            return f'SetAttr {node.instance} {node.attr} {node.value}'


        @visitor.when(TypeOf)
        def visit(self, node):
            return f'{node.local_dest} = TYPEOF {node.variable}'

        @visitor.when(Call)
        def visit(self, node):
            return f'{node.local_dest} = CALL {node.function}'

        @visitor.when(VCall)
        def visit(self, node):
            return f'{node.local_dest} = VCALL {node.dynamic_type} {node.function} '

        @visitor.when(Arg)
        def visit(self, node):
            return f'ARG {node.arg}'

        @visitor.when(Return)
        def visit(self, node):
            return f'\n RETURN {node.value if node.value is not None else ""}'

        @visitor.when(IsVoid)
        def visit(self, node):
            return f'{node.result_local} ISVOID {node.expre_value}'

        @visitor.when(Halt)
        def visit(self, node):
            return 'HALT'
        
        @visitor.when(Copy)
        def visit(self, node):
            return f'{node.local_dest} = COPY {node.type}'

        @visitor.when(Length)
        def visit(self, node):
            return f'{node.result} = LENGTH {node.variable}'

        @visitor.when(Concat)
        def visit(self, node):
            return f'{node.result} = CONCAT {node.string1}  {node.string2}'

        @visitor.when(SubStr)
        def visit(self, node):
            return f'{node.result} = SUBSTR {node.i}  {node.length}  {node.string}'

        @visitor.when(Read)
        def visit(self, node):
            return f'{node.result} = READ'

        @visitor.when(Print)
        def visit(self, node):
            return f'PRINT {node.variable}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))
