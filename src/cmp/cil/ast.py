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


class ErrorNode(InstructionNode):
    def __init__(self, error=1):
        self.error = error


class CopyNode(InstructionNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj


class TypeNameNode(InstructionNode):
    def __init__(self, dest, typex):
        self.dest = dest
        self.type = typex


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class ComplementNode(InstructionNode):
    def __init__(self, dest, body):
        self.dest = dest
        self.body = body


class NotNode(InstructionNode):
    def __init__(self, dest, body):
        self.dest = dest
        self.body = body


class IsVoidNode(InstructionNode):
    def __init__(self, dest, body):
        self.dest = dest
        self.body = body


class VoidNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class LessNode(ArithmeticNode):
    pass


class EqualNode(ArithmeticNode):
    pass


class LessEqNode(ArithmeticNode):
    pass


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
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


class GetIndexNode(InstructionNode):
    def __init__(self, dest, array, index):
        self.dest = dest
        self.array = array
        self.index = index


class SetIndexNode(InstructionNode):
    def __init__(self, array, index, value):
        self.array = array
        self.index = index
        self.value = value


class SetNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value


class AllocateNode(InstructionNode):
    def __init__(self, dest, itype):
        self.dest = dest
        self.type = itype


class ArrayNode(InstructionNode):
    def __init__(self, dest, size):
        self.dest = dest
        self.size = size


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest


class StaticTypeOfNode(InstructionNode):
    def __init__(self, typex, dest):
        self.type = typex
        self.dest = dest


class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class GotoIfNode(InstructionNode):
    def __init__(self, value, label):
        self.value = value
        self.label = label


class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, obj, xtype, method, dest):
        self.obj = obj
        self.type = xtype
        self.method = method
        self.dest = dest


class AbortNode(InstructionNode):
    pass


class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class CleanArgsNode(InstructionNode):
    def __init__(self, nargs):
        self.nargs = nargs


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value


class LengthNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class ConcatNode(InstructionNode):
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


class StringEqualNode(InstructionNode):
    def __init__(self, dest, msg1, msg2):
        self.dest = dest
        self.msg1 = msg1
        self.msg2 = msg2


class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class ReadStrNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class PrintIntNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class PrintStrNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr
