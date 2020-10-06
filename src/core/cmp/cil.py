import core.cmp.visitor as visitor

#AST
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
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.labels_count = 0

class ParamNode(Node):
    def __init__(self, name):
        self.name = name

class LocalNode(Node):
    def __init__(self, name):
        self.name = name

class InstructionNode(Node):
    def __init__(self):
        self.leader = False


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source
    
    def __repr__(self):
        return f"{self.dest} = {self.source}"

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class LessEqualNode(ArithmeticNode):
    pass

class LessNode(ArithmeticNode):
    pass

class EqualNode(ArithmeticNode):
    def __repr__(self):
        return f"{self.dest} = {self.left} == {self.right}"

class GetAttribNode(InstructionNode):
    def __init__(self, dest, obj, attr, computed_type):
        self.dest = dest
        self.obj = obj
        self.attr = attr
        self.computed_type = computed_type
    
    def __repr__(self):
        return f"{self.dest} = GETATTR {self.obj} {self.attr}"

class SetAttribNode(InstructionNode):
    def __init__(self, obj, attr, value, computed_type):
        self.obj = obj
        self.attr = attr
        self.value = value
        self.computed_type = computed_type

class GetIndexNode(InstructionNode):
    pass

class SetIndexNode(InstructionNode):
    pass

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

class ArrayNode(InstructionNode):
    pass

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = TYPEOF {self.obj}"

class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label
    
    def __repr__(self):
        return f"LABEL {self.label}:"

class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label
    
    def __repr__(self):
        return f"GOTO {self.label}"

class GotoIfNode(InstructionNode):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label
    
    def __repr__(self):
        return f"GOTO {self.label} if {self.condition}"

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest, computed_type):
        self.type = xtype
        self.method = method
        self.dest = dest
        self.computed_type = computed_type
    
    def __repr__(self):
        return f"{self.dest} = VCALL {self.type} {self.method}"

class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"ARG {self.name}"

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value
    
    def __repr__(self):
        return f"RETURN {self.value}"

class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

class ExitNode(InstructionNode):
    pass

class TypeNameNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class NameNode(InstructionNode):
    def __init__(self, dest, name):
        self.dest = dest
        self.name = name

class CopyNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class LengthNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ConcatNode(InstructionNode):
    def __init__(self, dest, prefix, suffix):
        self.dest = dest
        self.prefix = prefix
        self.suffix = suffix

class SubstringNode(InstructionNode):
    def __init__(self, dest, str_value, index, length):
        self.dest = dest
        self.str_value = str_value
        self.index = index
        self.length = length

class ReadStrNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class PrintStrNode(InstructionNode):
    def __init__(self, value):
        self.value = value

class PrintIntNode(InstructionNode):
    def __init__(self, value):
        self.value = value

class ComplementNode(InstructionNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj

class VoidNode(InstructionNode):
    pass

class ErrorNode(InstructionNode):
    def __init__(self, data_node):
        self.data_node = data_node
    
    def __repr__(self):
        return f"ERROR {self.data_node}"

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

        @visitor.when(ParamNode)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node):
            return f'{node.dest} = {node.source}'

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

        @visitor.when(AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.type}'

        @visitor.when(StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgNode)
        def visit(self, node):
            return f'ARG {node.name}'

        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))
    
