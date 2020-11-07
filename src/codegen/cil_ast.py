class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode, idx=None):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode
        self.index = idx

class TypeNode(Node):
    def __init__(self, name, idx=None):
        self.name = name
        self.attributes = []
        self.methods = []
        self.index = idx

class DataNode(Node):
    def __init__(self, vname, value, idx=None):
        self.name = vname
        self.value = value
        self.index = idx


class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions, idx=None):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.index = idx

class ParamNode(Node):
    def __init__(self, name, idx=None):
        self.name = name
        self.index = idx

class LocalNode(Node):
    def __init__(self, name, idx=None):
        self.name = name
        self.index = idx

class InstructionNode(Node):
    def __init__(self, idx=None):
        self.in1 = None
        self.in2 = None
        self.out = None
        self.idx = idx

class AssignNode(InstructionNode):
    def __init__(self, dest, source, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source 
        
        self.in1 = source
        self.out = dest

class UnaryNode(InstructionNode):
    def __init__(self, dest, expr, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.expr = expr

        self.in1 = expr
        self.dest = dest

class NotNode(UnaryNode):
    pass

class IsVoidNode(UnaryNode):
    pass

class BinaryNode(InstructionNode):
    def __init__(self, dest, left, right, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.left = left
        self.right = right 

        self.in1 = left
        self.in2 = right
        self.out = dest

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class LessNode(BinaryNode):
    pass

class LessEqNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class GetAttribNode(InstructionNode):
    def __init__(self, obj, attr, dest, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        self.dest = dest

        self.out = dest
        self.in1 = obj

class SetAttribNode(InstructionNode):
    def __init__(self, obj, attr, value, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        self.value = value

        # TODO: Im not sure this is right, out shoul be attr and obj
        self.out = obj
        self.in1 = value

class GetIndexNode(InstructionNode):
    pass

class SetIndexNode(InstructionNode):
    pass

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest, idx=None):
        super().__init__(idx)
        self.type = itype
        self.dest = dest

        self.out = dest

class ArrayNode(InstructionNode):
    pass

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.dest = dest

        self.out = dest
        self.in1 = obj

class LabelNode(InstructionNode):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label

class GotoNode(InstructionNode):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label

class GotoIfNode(InstructionNode):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.in1 = cond

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest, idx=None):
        super().__init__(idx)
        self.function = function
        self.dest = dest

        self.out = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.method = method
        self.dest = dest

        self.out = dest

class ArgNode(InstructionNode):
    def __init__(self, name, idx=None):
        super().__init__(idx)
        self.name = name

class ReturnNode(InstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

class LoadNode(InstructionNode):
    def __init__(self, dest, msg, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.msg = msg

        self.out = dest

class LengthNode(InstructionNode):
    def __init__(self, dest, arg, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.arg = arg

        self.out = dest
        self.in1 = arg

class ConcatNode(InstructionNode):
    def __init__(self, dest, arg1, arg2, idx=None):
        super().__init__(idx)

        self.dest = dest
        self.arg1 = arg1
        self.arg2 = arg2

        self.out = dest
        self.in1 = arg1
        self.in2 = arg2

class PrefixNode(InstructionNode):
    def __init__(self, dest, word, n, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.word = word
        self.n = n

        self.out = dest
        self.in1 = word
        self.in2 = n

class SubstringNode(InstructionNode):
    def __init__(self, dest, word, n, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.word = word
        self.n = n

        self.out = dest
        self.in1 = word
        self.in2 = n

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.ivalue = ivalue

        self.out = dest
        self.in1 = ivalue

class ReadNode(InstructionNode):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest

        self.out = dest

class PrintNode(InstructionNode):
    def __init__(self, str_addr, idx=None):
        super().__init__(idx)
        self.str_addr = str_addr

        self.out = str_addr

class SelfNode(Node):
    def __init__(self, idx=None):
        super().__init__(idx)
