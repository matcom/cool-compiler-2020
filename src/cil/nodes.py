from __future__ import annotations
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


class TypeOffsetNode(InstructionNode):
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
    def __init__(self, obj: LocalNode, type_: Type, function: str, dest: LocalNode):
        self.function = function
        self.dest = dest
        self.obj = obj
        self.type_ = type_


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


class SubstringNode(InstructionNode):
    def __init__(self, dest, l, r) -> None:
        self.dest = dest
        self.l = l
        self.r = r


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


class AllocateStringNode(InstructionNode):
    def __init__(self, dest: LocalNode, value: DataNode, length: int) -> None:
        self.dest = dest
        self.value = value
        self.length = length


class ConcatString(InstructionNode):
    def __init__(self, dest: LocalNode, s: ParamNode) -> None:
        self.dest = dest
        self.s = s


class AbortNode(InstructionNode):
    def __init__(self, calling, abortion, newLine) -> None:
        self.src = calling
        self.abortion = abortion
        self.nl = newLine


class AllocateBoolNode(InstructionNode):
    def __init__(self, dest: LocalNode, value: int) -> None:
        self.dest = dest
        self.value = value


class AllocateIntNode(InstructionNode):
    def __init__(self, dest: LocalNode, value):
        self.dest = dest
        self.value = value


class JumpIfGreater(InstructionNode):
    def __init__(self, src1: LocalNode, src2: LocalNode, label: str) -> None:
        self.left = src1
        self.rigt = src2
        self.label = label


class BitwiseNotNode(InstructionNode):
    def __init__(self, src, dest) -> None:
        self.dest = dest
        self.src = src


class EqualToCilNode(InstructionNode):
    def __init__(self, left, right, dest) -> None:
        self.left = left
        self.right = right
        self.dest = dest


class GetValue(InstructionNode):
    def __init__(self, dest, src) -> None:
        self.dest = dest
        self.src = src


class CompareType(InstructionNode):
    def __init__(self, dest, src, type_) -> None:
        self.dest = dest
        self.src = src
        self.type = type_

class CompareSTRType(InstructionNode):
    def __init__(self, dest, src) -> None:
        self.dest = dest
        self.src = src


class CompareStringLengthNode(InstructionNode):
    def __init__(self, dest, left, rigth) -> None:
        self.dest = dest
        self.left = left
        self.right = rigth


class ReferenceEqualNode(InstructionNode):
    def __init__(self, left, right, dest):
        self.dest = dest
        self.right = right
        self.left = left

class CharToCharStringCompare(InstructionNode):
    def __init__(self, dest, left, rigth, while_label, end_label) -> None:
        self.dest = dest
        self.left = left
        self.right = rigth
        self.while_label = while_label
        self.end_label = end_label


class MinusNodeComp(InstructionNode):
    def __init__(self, left, right, dest):
        self.dest = dest
        self.right = right
        self.left = left

class PureMinus(InstructionNode):
    def __init__(self, left, right, dest):
        self.dest = dest
        self.right = right
        self.left = left