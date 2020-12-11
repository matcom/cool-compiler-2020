

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
        self.name_dir = ""
        self.attributes = []
        self.methods = []
        self.features = []


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


class ParamNode(Node):
    def __init__(self, name):
        self.name = name


class LocalNode(Node):
    def __init__(self, name):
        self.name = name


class InstructionNode(Node):
    pass


class GetAttribNode(InstructionNode):
    def __init__(self, dest, obj, attrib, typex):
        self.dest = dest
        self.obj = obj
        self.attrib = attrib
        self.type = typex


class SetAttribNode(InstructionNode):
    def __init__(self, obj, attrib, value, typex):
        self.obj = obj
        self.attrib = attrib
        self.value = value
        self.type = typex


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class EmptyArgs(InstructionNode):
    def __init__(self, args):
        self.args = args


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class UnaryNode(InstructionNode):
    def __init__(self, dest, expression):
        self.dest = dest
        self.expression = expression


class ComplementNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


class NotNode(UnaryNode):
    pass


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class EqualNode(ArithmeticNode):
    pass


class LessNode(ArithmeticNode):
    pass


class LessEqNode(ArithmeticNode):
    pass


class BoxNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value


class AbortNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, dest, itype):
        self.dest = dest
        self.type = itype


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest


class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class IfGotoNode(InstructionNode):
    def __init__(self, value, label):
        self.value = value
        self.label = label


class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.dest = dest
        self.function = function


class DynamicCallNode(InstructionNode):
    def __init__(self, obj, xtype, method, dest):
        self.obj = obj
        self.type = xtype
        self.method = method
        self.dest = dest


class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class ErrorNode(InstructionNode):
    def __init__(self, error=0):
        self.error = error


class CopyNode(InstructionNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj


class TypeNameNode(InstructionNode):
    def __init__(self, dest, typex):
        self.dest = dest
        self.type = typex


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class LengthNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class ConcatNode(InstructionNode):
    def __init__(self, dest, msg1, msg2):
        self.dest = dest
        self.msg1 = msg1
        self.msg2 = msg2


class StringEqualNode(InstructionNode):
    def __init__(self, dest, msg1, msg2):
        self.dest = dest
        self.msg1 = msg1
        self.msg2 = msg2


class SubstringNode(InstructionNode):
    def __init__(self, dest, msg1, start, length):
        self.dest = dest
        self.msg1 = msg1
        self.start = start
        self.length = length


class PrintStrNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class PrintIntNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class ReadStrNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

################# nodes que me tengo que definir ##############

# class ConformNode(InstructionNode):
#     def __init__(self, dest, obj, typex):
#         self.dest = dest
#         self.obj = obj
#         self.type = typex
