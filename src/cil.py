import visitor as visitor


class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []

class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions, labels):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.labels = labels

class ParamNode(Node):
    def __init__(self, name):
        self.name = name

class LocalNode(Node):
    def __init__(self, name):
        self.name = name

class InstructionNode(Node):
    pass

class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class ComplementNode(InstructionNode):
    def __init__(self, expression, dest):
        self.expression = expression
        self.dest = dest

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class LessNode(InstructionNode):
    def __init__(self, result, left, right, labelTrue, labelEnd):
        self.result = result
        self.left = left
        self.right =right
        self.labelTrue = labelTrue
        self.labelEnd = labelEnd

class LessEqualNode(ArithmeticNode):
    def __init__(self, result, left, right, labelTrue, labelEnd):
        self.result = result
        self.left = left
        self.right =right
        self.labelTrue = labelTrue
        self.labelEnd = labelEnd

class GetAttribNode(InstructionNode):
    def __init__(self, ins,att,dest):
        self.ins = ins
        self.att = att
        self.dest = dest

class SetAttribNode(InstructionNode):
     def __init__(self, ins,att, value):
        self.ins = ins
        self.att = att
        self.value = value

class GetIndexNode(InstructionNode):
    pass

class SetIndexNode(InstructionNode):
    pass

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

class JumpNode(InstructionNode):
    def __init__(self, method, dest):
        self.method = method
        self.dest = dest

class ArrayNode(InstructionNode):
    pass

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

class IsVoidNode(InstructionNode):
    def __init__(self, obj, dest, label):
        self.obj = obj
        self.dest = dest
        self.label = label

class CaseOption(InstructionNode):
    def __init__(self, expression, label, typex):
        self.expression = expression
        self.label = label
        self.typex = typex

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class GotoNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class GotoIfNode(InstructionNode):
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest,ins):
        self.type = xtype
        self.method = method
        self.dest = dest
        self.ins = ins

class ArgsNode(InstructionNode):
    def __init__(self, names):
        self.names = names

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

class LoadNode(InstructionNode):
    def __init__(self, dest, msg, desp=0):
        self.dest = dest
        self.msg = msg
        self.desp = desp

class LoadAddressNode(LoadNode):
    pass

class LoadIntNode(InstructionNode):
    def __init__(self, dest, msg, desp):
        self.dest = dest
        self.msg = msg
        self.desp = desp

class LengthNode(InstructionNode):
    pass

class ConcatNode(InstructionNode):
    pass

class PrefixNode(InstructionNode):
    pass

class SubstringNode(InstructionNode):
    pass

class StringComparer(InstructionNode):
    def __init__(self, result, left, right):
        self.result = result
        self.left = left
        self.right = right

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(DataNode)
        def visit(self, node):
            return f'{node.name}:  "{node.value}"'

        @visitor.when(TypeNode)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(FunctionNode)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        # @visitor.when(Node)
        # def visit(self, node):
        #     return f'----------------------------------{node.__class__.__name__}'

        @visitor.when(ParamNode)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node:AssignNode):
            return f'{node.dest} = {node.source}'

        @visitor.when(GetAttribNode)
        def visit(self, node:GetAttribNode):
           return f'{node.dest} = GETATTR {node.ins} {node.att}' 

        @visitor.when(SetAttribNode)
        def visit(self, node:SetAttribNode):
           return f'SETATTR {node.ins} {node.att} {node.value}' 

        @visitor.when(PlusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} + {node.right}'        

        @visitor.when(MinusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} - {node.right}'

        @visitor.when(StarNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} * {node.right}'

        @visitor.when(DivNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} / {node.right}'

        @visitor.when(LessEqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} <= {node.right}'

        @visitor.when(LessNode)
        def visit(self, node):
            return f'{node.result} = {node.left} < {node.right}'

        @visitor.when(AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(LabelNode)
        def visit(self, node):
            return f'LABEL {node.name}'

        @visitor.when(JumpNode)
        def visit(self, node):
            return f'JUMP {node.method}'

        @visitor.when(GotoNode)
        def visit(self, node):
            return f'GOTO {node.name}'

        @visitor.when(GotoIfNode)
        def visit(self, node):
            return f'IF {node.condition} GOTO {node.name}'

        @visitor.when(TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.type}'

        @visitor.when(StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgsNode)
        def visit(self, node):
            return '\n\t'.join(f'ARG {x}' for x in node.names)

        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'

        @visitor.when(LoadNode)
        def visit(self, node):
            return f'LOAD {node.dest} {node.msg} {node.desp}'
        
        @visitor.when(LoadAddressNode)
        def visit(self, node):
            return f'LOAD_ADDRESS {node.dest} {node.msg} {node.desp}'

        @visitor.when(LoadIntNode)
        def visit(self, node):
            return f'LOAD_INT {node.dest} {node.msg} {node.desp}'

        @visitor.when(StringComparer)
        def visit(self,node):
            return f'STRCOMP {node.result}, {node.left}, {node.right}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))