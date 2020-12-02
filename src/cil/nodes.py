from __future__ import annotations
from time import clock_settime
from typing import List, Tuple, Union
from abstract.semantics import Attribute, Method, Type
"""
Define a hierachy to represent each CIL instruction.
Every CIL Instruction would be a Node of an AST, and every\
node would known how to generate its corresponding MIPS Code.
"""


class CilNode:
    pass


class BuiltInNode(CilNode):
    def __init__(self, dest: LocalNode) -> None:
        self.dest = dest


class CilProgramNode(CilNode):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes: List[TypeNode] = dottypes
        self.dotdata: List[DataNode] = dotdata
        self.dotcode: List[FunctionNode] = dotcode


class TypeNode(CilNode):
    def __init__(self, name: str):
        self.name = name
        self.attributes: List[Attribute] = []
        self.methods: List[Tuple[str, str]] = []


class DataNode(CilNode):
    def __init__(self, vname: str, value):
        self.name = vname
        self.value = value


class FunctionNode(CilNode):
    def __init__(self, fname, params, lvars, instr):
        self.name = fname
        self.params: List[ParamNode] = params
        self.localvars = lvars
        self.instructions = instr


class ParamNode(CilNode):
    def __init__(self, name):
        self.name = name


class LocalNode(CilNode):
    def __init__(self, name):
        self.name = name


class InstructionNode(CilNode):
    pass


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    def __init__(self, x: Union[LocalNode, int, ParamNode],
                 y: Union[LocalNode, int, ParamNode], dest: LocalNode):
        self.x = x
        self.y = y
        self.dest = dest


class StarNode(ArithmeticNode):
    def __init__(self, x: LocalNode, y: LocalNode, dest: LocalNode):
        self.x = x
        self.y = y
        self.dest = dest


class DivNode(ArithmeticNode):
    pass


class GetAttributeNode(InstructionNode):
    def __init__(self, itype: Type, attrname: str, dest: LocalNode):
        self.itype = itype
        self.attrname = attrname
        self.dest = dest


class SetAttributeNode(InstructionNode):
    def __init__(self, itype: Type, attrname: str, source: LocalNode):
        self.source = source
        self.itype = itype
        self.attrname = attrname


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype: Type, dest: LocalNode):
        self.itype = itype
        self.dest = dest


class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, variable: Union[LocalNode, ParamNode], dest: LocalNode):
        self.variable = variable
        self.dest = dest


class LabelNode(InstructionNode):
    def __init__(self, label: str):
        self.label: str = label


class JumpIfGreaterThanZeroNode(InstructionNode):
    def __init__(self, variable: LocalNode, label: str):
        self.label = label
        self.variable = variable


class IfZeroJump(InstructionNode):
    def __init__(self, variable: LocalNode, label: str):
        self.variable = variable
        self.label = label


class NotZeroJump(InstructionNode):
    def __init__(self, variable: LocalNode, label: str):
        self.variable = variable
        self.label = label


class UnconditionalJump(InstructionNode):
    def __init__(self, label: str):
        self.label: str = label


class StaticCallNode(InstructionNode):
    def __init__(self, function: str, dest: LocalNode):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, xtype: LocalNode, method: str, dest: LocalNode):
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
    def __init__(self, dest: LocalNode, message: DataNode):
        self.dest = dest
        self.message = message


class InitSelfNode(InstructionNode):
    def __init__(self, src: LocalNode) -> None:
        self.src = src


class SetAtAddress(InstructionNode):
    pass

class LengthNode(BuiltInNode):
    pass


class ConcatNode(BuiltInNode):
    pass


class PrefixNode(BuiltInNode):
    pass


class SubstringNode(BuiltInNode):
    pass


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class ReadIntNode(InstructionNode):
    def __init__(self, dest) -> None:
        self.dest = dest


class PrintNode(InstructionNode):
    def __init__(self, src) -> None:
        self.src = src


class PrintIntNode(InstructionNode):
    def __init__(self, src) -> None:
        self.src = src


class TdtLookupNode(InstructionNode):
    def __init__(self, index_varA: str, index_varB: LocalNode,
                 dest: LocalNode):
        self.i = index_varA
        self.j = index_varB
        self.dest = dest


class GetTypeIndex(InstructionNode):
    def __init__(self, itype: str, dest: str):
        self.itype = itype
        self.dest = dest


class SelfNode(InstructionNode):
    def __init__(self, dest: LocalNode) -> None:
        self.dest = dest


class NotNode(InstructionNode):
    def __init__(self, src: LocalNode) -> None:
        self.src = src


class CopyNode(InstructionNode):
    def __init__(self, selfsrc: LocalNode, dest: LocalNode) -> None:
        self.selfsrc = selfsrc
        self.dest = dest


class TypeName(InstructionNode):
    def __init__(self, dest: LocalNode) -> None:
        self.dest = dest


class SaveSelf(InstructionNode):
    pass

class RestoreSelf(InstructionNode):
    pass