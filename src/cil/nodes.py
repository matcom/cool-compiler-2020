"""
Define a hierachy to represent each CIL instruction.
Every CIL Instruction would be a Node of an AST, and every\
node would known how to generate its corresponding MIPS Code.
"""


class CilNode:
    pass


class CilProgramNode(CilNode):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode


class TypeNode(CilNode):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []


class DataNode(CilNode):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value


class FunctionNode(CilNode):
    def __init__(self, fname, params, lvars, instr):
        self.name = fname
        self.params = params
        self.localvars = lvars
        self.instructions = instr


class ParamNode(CilNode):
    def __init__(self, name):
        self.name = name


class LocalNode(CilNode):
    def __init__(self, name):
        self.name


class InstructionNode(CilNode):
    pass


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.dest = right


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    def __init__(self, x: str, y: str, dest: str):
        self.x = x
        self.y = y
        self.dest = dest


class StarNode(ArithmeticNode):
    def __init__(self, x: str, y: str, dest: str):
        self.x = x
        self.y = y
        self.dest = dest


class DivNode(ArithmeticNode):
    pass


class GetAttributeNode(InstructionNode):
    def __init__(self, itype: str, attrname: str, dest: str):
        self.itype = itype
        self.attrname = attrname
        self.dest = dest


class SetAttributeNode(InstructionNode):
    def __init__(self, itype: str, attrname: str, source: str):
        self.source = source
        self.itype = itype
        self.attrname = attrname


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype: str, dest: str):
        self.itype = itype
        self.dest = dest


class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, variable: str, dest: str):
        self.variable = variable
        self.dest = dest


class LabelNode(InstructionNode):
    def __init__(self, label: str):
        self.label: str = label


class JumpIfGreaterThanZeroNode(InstructionNode):
    def __init__(self, variable: str, label: str):
        self.label = label
        self.variable = variable


class IfZeroJump(InstructionNode):
    def __init__(self, variable: str, label: str):
        self.variable = variable
        self.label = label


class NotZeroJump(InstructionNode):
    def __init__(self, variable: str, label: str):
        self.variable: str = variable
        self.label: str = label


class UnconditionalJump(InstructionNode):
    def __init__(self, label: str):
        self.label: str = label


class StaticCallNode(InstructionNode):
    def __init__(self, function: str, dest: str):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest):
        self.xtype = xtype
        self.method = method
        self.dest = dest


class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value


class LoadNode(InstructionNode):
    def __init__(self, dest, message):
        self.dest = dest
        self.message = message


class LengthNode(InstructionNode):
    pass


class ConcatNode(InstructionNode):
    pass


class PrefixNode(InstructionNode):
    pass


class SubstringNode(InstructionNode):
    pass


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class ReadNode(InstructionNode):
    def __init__(self, dest: str):
        self.dest = dest


class PrintNode(InstructionNode):
    def __init__(self, string_address: str):
        self.string_address = string_address


class TdtLookupNode(InstructionNode):
    def __init__(self, index_varA: str, index_varB: str, dest: str):
        self.i = index_varA
        self.j = index_varB
        self.dest = dest


class GetTypeIndex(InstructionNode):
    def __init__(self, itype: str, dest: str):
        self.itype = itype
        self.dest = dest
