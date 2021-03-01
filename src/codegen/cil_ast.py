class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode, idx=None):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode
        self.index = idx

class TypeNode(Node):
    def __init__(self, name, atributes=None, methods=None, idx=None):
        self.name = name
        self.attributes = atributes if atributes is not None else []
        self.methods = methods if methods is not None else []
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
    def __init__(self, name, typex, idx=None):
        self.name = name
        self.type = typex
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
        self.index = idx

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
        self.out = dest

class NotNode(UnaryNode):
    pass

class LogicalNotNode(UnaryNode):
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
    def __init__(self, obj, attr, typex, dest, attr_type, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        self.type_name = typex
        # self.attr_offset = offset
        self.dest = dest
        self.attr_type = attr_type

        self.out = dest
        self.in1 = obj

class SetAttribNode(InstructionNode):
    def __init__(self, obj, attr, typex, value, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        # self.attr_offset = offset
        self.value = value
        self.type_name = typex

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

class GotoIfFalseNode(InstructionNode):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.in1 = cond

class StaticCallNode(InstructionNode):
    def __init__(self, xtype, function, dest, args, return_type, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.function = function
        self.dest = dest
        self.args = args
        self.return_type = return_type
        
        self.out = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, obj, method, dest, args, return_type, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.method = method
        self.dest = dest
        self.args = args
        self.return_type = return_type
        self.obj = obj

        self.out = dest
        self.in1 = obj

class ArgNode(InstructionNode):
    def __init__(self, name, idx=None):
        super().__init__(idx)
        self.dest = name

        self.out = name

class ReturnNode(InstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.out = value

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
    def __init__(self, dest, word, begin, end, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.begin = begin
        self.word = word
        self.end = end

        self.out = dest
        self.in1 = begin
        self.in2 = end

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.ivalue = ivalue

        self.out = dest
        self.in1 = ivalue

class OutStringNode(InstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.in1 = value

class OutIntNode(InstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.in1 = value

class ReadStringNode(InstructionNode):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest

        self.out = dest

class ReadIntNode(InstructionNode):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest

        self.out = dest

class ExitNode(InstructionNode):
    def __init__(self, classx, value=0, idx=None):
        super().__init__(idx)
        self.classx = classx        # instance of the method that called the class
        self.value = value

        self.in1 = value
        self.in2 = classx

class CopyNode(InstructionNode):
    def __init__(self, dest, source, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source

        self.out = dest
        self.in1 = source

class ConformsNode(InstructionNode):
    "Checks if the type of expr conforms to type2"
    def __init__(self, dest, expr, type2, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.expr = expr
        self.type = type2

        self.out = dest
        self.in1 = expr    # is a string, so is always a variable
        
class VoidConstantNode(InstructionNode):
    def __init__(self, obj, idx=None):
        super().__init__(idx)
        self.obj = obj

        self.out = obj

class ErrorNode(InstructionNode):
    "Generic class to report errors in mips"
    def __init__(self, typex, idx=None):
        super().__init__(idx)
        self.type = typex

class BoxingNode(InstructionNode):
    def __init__(self, dest, type_name, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.type = type_name

        self.out = dest
