from functools import wraps
from typing import Dict, List

from ..cool_lang.semantics.semantic_utils import Context
from .ast import (
    AllocateNode,
    AbortNode,
    ArgNode,
    ArithmeticNode,
    AssignNode,
    CleanArgsNode,
    ComplementNode,
    ConcatNode,
    CopyNode,
    DataNode,
    DivNode,
    DynamicCallNode,
    EqualNode,
    ErrorNode,
    FunctionNode,
    GetAttribNode,
    GotoIfNode,
    GotoNode,
    IsVoidNode,
    LabelNode,
    LengthNode,
    LessEqNode,
    LessNode,
    LocalNode,
    MinusNode,
    ParamNode,
    PlusNode,
    PrintIntNode,
    PrintStrNode,
    ProgramNode,
    ReadIntNode,
    ReadStrNode,
    ReturnNode,
    SetAttribNode,
    StarNode,
    StaticCallNode,
    StringEqualNode,
    SubstringNode,
    TypeNameNode,
    TypeNode,
    TypeOfNode,
    VoidNode,
)
from .utils import TypeData, on, when
from .utils.mips_syntax import DATA_SIZE, Mips
from .utils.mips_syntax import Register as Reg


def mips_comment(msg: str):
    def inner(fn):
        @wraps(fn)
        def wrapped(self: CIL_TO_MIPS, *args, **kwargs):
            self.mips.comment("")
            result = fn(self, *args, **kwargs)
            self.mips.empty()
            return result

        return wrapped

    return inner


class CIL_TO_MIPS(object):
    def __init__(self, context=Context):
        self.types = []
        self.types_offsets: Dict[str, TypeData] = dict()
        self.local_vars_offsets = dict()
        self.actual_args = dict()
        self.mips = Mips()
        self.label_count = -1
        self.registers_to_save: List[Reg] = [
            Reg.ra,
            Reg.s0,
            Reg.s1,
            Reg.s2,
            Reg.s3,
            Reg.s4,
            Reg.s5,
            Reg.s6,
            Reg.s7,
        ]
        self.context: Context = context

        self.mips.write_data("eol:")
        self.mips.asciiz("\\n")

    def build_types_data(self, types):
        for idx, typex in enumerate(types):
            self.types_offsets[typex.name] = TypeData(idx, typex)

    def get_label(self):
        self.label_count += 1
        return f"mip_label_{self.label_count}"

    @mips_comment("DEBUG PRINT")
    def print_debug(self, msg: str):
        self.mips.push(Reg.a0)
        self.mips.push(Reg.v0)

        data_label = self.get_label()

        self.mips.data_label(data_label)
        self.mips.asciiz(msg)

        self.mips.la(Reg.a0, data_label)
        self.mips.print_string()

        self.mips.pop(Reg.v0)
        self.mips.pop(Reg.a0)

    def get_offset(self, arg: str):
        if arg in self.actual_args or arg in self.local_vars_offsets:
            offset = (
                self.actual_args[arg]
                if arg in self.actual_args
                else self.local_vars_offsets[arg]
            ) * DATA_SIZE
            return self.mips.offset(Reg.fp, offset)
        else:
            raise Exception(f"load_memory: The direction {arg} isn't an address")

    @mips_comment("LOAD MEMORY")
    def load_memory(self, dst: Reg, arg: str):
        self.mips.comment(f"from {arg} to {dst}")
        self.mips.load_memory(dst, self.get_offset(arg))

    @mips_comment("STORE MEMORY")
    def store_memory(self, dst: Reg, arg: str):
        self.mips.comment(f"from {arg} to {dst}")
        if arg in self.actual_args or arg in self.local_vars_offsets:
            offset = (
                self.actual_args[arg]
                if arg in self.actual_args
                else self.local_vars_offsets[arg]
            ) * DATA_SIZE
            self.mips.store_memory(dst, self.mips.offset(Reg.fp, offset))
        else:
            raise Exception(f"store_memory: The direction {arg} isn't an address")
        self.mips.empty()

    def load_arithmetic(self, node: ArithmeticNode):
        self.load_memory(Reg.s0, node.left)
        self.load_memory(Reg.s1, node.right)

    def store_registers(self):
        for reg in self.registers_to_save:
            self.mips.push(reg)

    def load_registers(self):
        for reg in reversed(self.registers_to_save):
            self.mips.pop(reg)

    @on("node")
    def visit(self, node):
        pass

    @mips_comment("ProgramNode")
    @when(ProgramNode)
    def visit(self, node: ProgramNode):  # noqa: F811
        self.types = node.dottypes
        self.build_types_data(self.types)

        for datanode in node.dotdata:
            self.visit(datanode)

        self.mips.label("main")

        self.mips.jal("entry")

        self.mips.exit()

        for function in node.dotcode:
            self.visit(function)

        self.mips.empty()

    @when(DataNode)
    def visit(self, node: DataNode):  # noqa: F811
        self.mips.data_label(node.name)
        self.mips.asciiz(node.value)

    @when(TypeNode)
    def visit(self, node: TypeNode):  # noqa: F811
        pass

    @mips_comment("FunctionNode")
    @when(FunctionNode)
    def visit(self, node: FunctionNode):  # noqa: F811
        self.mips.label(node.name)

        self.mips.comment("Set stack frame")
        self.mips.push(Reg.fp)
        self.mips.move(Reg.fp, Reg.sp)

        self.actual_args = dict()

        for idx, param in enumerate(node.params):
            self.visit(param, index=idx)

        self.mips.empty()
        self.mips.comment("Allocate memory for Local variables")
        for idx, local in enumerate(node.localvars):
            self.visit(local, index=idx)

        # self.mips.move(Reg.a0, Reg.ra)
        # self.mips.print_int()
        # self.mips.la(Reg.a0, "eol")
        # self.mips.print_string()

        self.mips.empty()
        self.store_registers()
        self.mips.empty()
        self.mips.comment("Generating body code")
        for instruction in node.instructions:
            # if type(instruction) == AssignNode:
            #     print(node.name)
            #     print("     \n".join(map(lambda x: str(x), node.instructions)))
            self.visit(instruction)

        self.mips.empty()
        self.load_registers()

        # self.mips.move(Reg.a0, Reg.ra)
        # self.mips.print_int()
        # self.mips.la(Reg.a0, "eol")
        # self.mips.print_string()

        self.mips.comment("Clean stack variable space")
        for _ in node.localvars:
            self.mips.pop(None)
        self.actual_args = None
        self.mips.comment("Return")
        self.mips.pop(Reg.fp)
        self.mips.jr(Reg.ra)

    @when(ParamNode)
    def visit(self, node: ParamNode, index=0):  # noqa: F811
        self.actual_args[node.name] = index + 1

    @mips_comment("LocalNode")
    @when(LocalNode)
    def visit(self, node: LocalNode, index=0):  # noqa: F811
        self.mips.push(Reg.zero)
        assert node.name not in self.local_vars_offsets, f"Impossible {node.name}..."
        self.local_vars_offsets[node.name] = -(index + 1)

    @mips_comment("Auxiliar - Copy data")
    def copy_data(self, src: Reg, dst: Reg, length: Reg):
        """
        length: fixed in bytes size.
        """
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(Reg.t0, src)
        self.mips.move(Reg.t1, dst)

        self.mips.move(Reg.t3, length)  # i = length

        self.mips.label(loop)

        self.mips.lb(Reg.t2, self.mips.offset(Reg.t0))
        self.mips.sb(Reg.t2, self.mips.offset(Reg.t1))

        self.mips.addi(Reg.t0, Reg.t0, 2)
        self.mips.addi(Reg.t1, Reg.t1, 2)

        self.mips.addi(Reg.t3, Reg.t3, -1)  # i --

        self.mips.beqz(Reg.t3, end)
        self.mips.j(loop)

        self.mips.label(end)

    @mips_comment("CopyNode")
    @when(CopyNode)
    def visit(self, node: CopyNode):  # noqa: F811
        # TODO: Fill src and length values
        length = 0

        # reserve heap space
        self.mips.addi(Reg.a0, length)
        self.mips.sbrk()
        self.mips.move(Reg.s1, Reg.v0)
        # copy data raw byte to byte
        self.mips.li(Reg.s3, len)
        self.copy_data(Reg.s0, Reg.s1, Reg.s3)

    @mips_comment("TypeNameNode")
    @when(TypeNameNode)
    def visit(self, node: TypeNameNode):  # noqa: F811
        self.load_memory(Reg.s0, node.type)
        self.mips.load_memory(Reg.s1, self.mips.offset(Reg.s0, DATA_SIZE))
        self.store_memory(Reg.s1, node.dest)

    @mips_comment("ErrorNode")
    @when(ErrorNode)
    def visit(self, node: ErrorNode):  # noqa: F811
        self.mips.li(Reg.a0, int(node.error))
        self.mips.exit2()

    @when(AbortNode)
    def visit(self, node: AbortNode):  # noqa: F811
        self.mips.comment("AbortNode")
        self.mips.exit()
        self.mips.empty()

    @mips_comment("AssignNode")
    @when(AssignNode)
    def visit(self, node: AssignNode):  # noqa: F811
        self.load_memory(Reg.s0, node.source)
        self.store_memory(Reg.s0, node.dest)

    @mips_comment("VoidNode")
    @when(VoidNode)
    def visit(self, node: VoidNode):  # noqa: F811
        self.store_memory(Reg.zero, node.dest)

    @mips_comment("IsVoidNode")
    @when(IsVoidNode)
    def visit(self, node: IsVoidNode):  # noqa: F811
        self.load_memory(Reg.s0, node.body)

        label = self.get_label()

        self.mips.li(Reg.s1, 0)
        self.mips.bne(Reg.s0, Reg.s1, label)
        self.mips.li(Reg.s1, 1)
        self.mips.label(label)
        self.store_memory(Reg.s1, node.dest)

    @mips_comment("ComplementNode")
    @when(ComplementNode)
    def visit(self, node: ComplementNode):  # noqa: F811

        self.load_memory(Reg.s0, node.body)
        # self.mips.move(Reg.a0, Reg.s0)
        # self.mips.print_int()
        self.mips.move(Reg.s1, Reg.s0)
        self.mips.nor(Reg.s2, Reg.s1, Reg.s0)
        self.store_memory(Reg.s2, node.dest)
        # self.mips.move(Reg.a0, Reg.s1)
        # self.mips.print_int()

    @mips_comment("LessNode")
    @when(LessNode)
    def visit(self, node: LessNode):  # noqa: F811
        self.load_arithmetic(node)
        self.mips.slt(Reg.s2, Reg.s0, Reg.s1)
        self.store_memory(Reg.s2, node.dest)

    @mips_comment("EqualNode")
    @when(EqualNode)
    def visit(self, node: EqualNode):  # noqa: F811
        """
        ((a < b) + (b < a)) < 1  -> ==
        """
        self.load_arithmetic(node)
        # self.mips.move(Reg.a0, Reg.s0)
        # self.mips.print_int()
        # self.mips.move(Reg.a0, Reg.s1)
        # self.mips.print_int()
        self.mips.slt(Reg.s2, Reg.s0, Reg.s1)
        self.mips.slt(Reg.s3, Reg.s1, Reg.s0)

        self.mips.add(Reg.s0, Reg.s2, Reg.s3)
        self.mips.slti(Reg.s1, Reg.s0, 1)

        # self.mips.move(Reg.a0, Reg.s1)
        # self.mips.print_int()

        self.store_memory(Reg.s1, node.dest)

    @mips_comment("LessEqNode")
    @when(LessEqNode)
    def visit(self, node: LessEqNode):  # noqa: F811
        """
        a <= b -> ! b < a -> 1 - (b < a)
        """
        self.load_arithmetic(node)
        self.mips.slt(Reg.s2, Reg.s1, Reg.s0)
        self.mips.li(Reg.s3, 1)
        self.mips.sub(Reg.s0, Reg.s3, Reg.s2)
        self.store_memory(Reg.s0, node.dest)

    @mips_comment("PlusNode")
    @when(PlusNode)
    def visit(self, node: PlusNode):  # noqa: F811
        self.load_arithmetic(node)
        self.mips.add(Reg.s2, Reg.s0, Reg.s1)
        self.store_memory(Reg.s2, node.dest)

    @mips_comment("MinusNode")
    @when(MinusNode)
    def visit(self, node: MinusNode):  # noqa: F811
        self.load_arithmetic(node)
        self.mips.sub(Reg.s2, Reg.s0, Reg.s1)
        self.store_memory(Reg.s2, node.dest)

    @mips_comment("StarNode")
    @when(StarNode)
    def visit(self, node: StarNode):  # noqa: F811
        self.load_arithmetic(node)
        self.mips.mult(Reg.s0, Reg.s1)
        self.mips.mflo(Reg.s0)
        self.store_memory(Reg.s0, node.dest)

    @mips_comment("DivNode")
    @when(DivNode)
    def visit(self, node: DivNode):  # noqa: F811
        self.load_arithmetic(node)
        self.mips.div(Reg.s0, Reg.s1)
        self.mips.mflo(Reg.s0)
        self.store_memory(Reg.s0, node.dest)

    @mips_comment("AllocateNode")
    @when(AllocateNode)
    def visit(self, node: AllocateNode):  # noqa: F811
        self.mips.comment(f"dest: {node.dest}, type: {node.type}")

        type_data = self.types_offsets[node.type]

        self.mips.comment(str(type_data))

        length = len(type_data.attr_offsets) + len(type_data.func_offsets) + 2
        length *= DATA_SIZE
        self.mips.li(Reg.a0, length)
        self.mips.sbrk()
        self.mips.move(Reg.s1, Reg.v0)
        self.store_memory(Reg.s1, node.dest)

        self.mips.li(Reg.s0, type_data.type)
        self.mips.store_memory(Reg.s0, self.mips.offset(Reg.s1))

        self.mips.la(Reg.s0, type_data.str)
        self.mips.store_memory(Reg.s0, self.mips.offset(Reg.s1, DATA_SIZE))

        for offset in type_data.attr_offsets.values():
            self.mips.store_memory(
                Reg.zero,
                self.mips.offset(Reg.s1, offset * DATA_SIZE),
            )

        for name, offset in type_data.func_offsets.items():
            direct_name = type_data.func_names[name]
            self.mips.la(Reg.s0, direct_name)
            self.mips.store_memory(
                Reg.s0,
                self.mips.offset(
                    Reg.s1,
                    offset * DATA_SIZE,
                ),
            )

    @mips_comment("TypeOfNode")
    @when(TypeOfNode)
    def visit(self, node: TypeOfNode):  # noqa: F811
        self.load_memory(Reg.s0, node.obj)
        self.mips.load_memory(Reg.s1, self.mips.offset(Reg.s0))
        self.store_memory(Reg.s1, node.dest)

    @mips_comment("StaticCallNode")
    @when(StaticCallNode)
    def visit(self, node: StaticCallNode):  # noqa: F811
        self.mips.jal(node.function)
        self.mips.comment(f"Returning {node.dest}")
        self.store_memory(Reg.v0, node.dest)

    @mips_comment("DynamicCallNode")
    @when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):  # noqa: F811
        type_data = self.types_offsets[node.type]
        offset = type_data.func_offsets[node.method] * DATA_SIZE
        self.load_memory(Reg.s0, node.obj)
        self.mips.load_memory(Reg.s1, self.mips.offset(Reg.s0, offset))
        self.mips.jalr(Reg.s1)
        self.mips.comment(f"Returning {node.dest}")
        self.store_memory(Reg.v0, node.dest)

    @mips_comment("ArgNode")
    @when(ArgNode)
    def visit(self, node: ArgNode):  # noqa: F811
        self.load_memory(Reg.s0, node.name)
        self.mips.push(Reg.s0)

    @mips_comment("CleanArgsNode")
    @when(CleanArgsNode)
    def visit(self, node: CleanArgsNode):  # noqa: F811
        for _ in range(node.nargs):
            self.mips.pop(None)

    @mips_comment("ReturnNode")
    @when(ReturnNode)
    def visit(self, node: ReturnNode):  # noqa: F811
        self.mips.comment(f"Returning {node.value}")
        self.load_memory(Reg.v0, node.value)

    @mips_comment("ReadIntNode")
    @when(ReadIntNode)
    def visit(self, node: ReadIntNode):  # noqa: F811
        self.mips.read_int()
        self.store_memory(Reg.v0, node.dest)

    @mips_comment("ReadStrNode")
    @when(ReadStrNode)
    def visit(self, node: ReadStrNode):  # noqa: F811
        self.mips.li(Reg.a0, 1024)
        self.mips.sbrk()
        self.mips.move(Reg.a0, Reg.v0)
        self.store_memory(Reg.v0, node.dest)
        self.mips.li(Reg.a1, 1024)  # Change this later
        self.mips.read_string()

    @mips_comment("PrintIntNode")
    @when(PrintIntNode)
    def visit(self, node: PrintIntNode):  # noqa: F811
        # self.load_memory(Reg.s0, node.str_addr)
        # type_data = self.types_offsets["Int"]
        # offset = type_data.attr_offsets["value"] * DATA_SIZE
        # self.mips.load_memory(Reg.a0, self.mips.offset(Reg.s0, offset))
        self.load_memory(Reg.a0, node.str_addr)
        self.mips.print_int()

    @mips_comment("PrintStrNode")
    @when(PrintStrNode)
    def visit(self, node: PrintStrNode):  # noqa: F811
        self.load_memory(Reg.a0, node.str_addr)
        self.mips.print_string()

    @mips_comment("Auxiliar - Get string length")
    def get_string_length(self, src: Reg, dst: Reg):
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(Reg.t0, src)
        self.mips.li(Reg.t1, 0)

        self.mips.label(loop)

        self.mips.lb(Reg.t3, self.mips.offset(Reg.t0))
        self.mips.beqz(Reg.t3, end)

        self.mips.addi(Reg.t1, Reg.t1, 1)
        self.mips.addi(Reg.t0, Reg.t0, 1)

        self.mips.j(loop)
        self.mips.label(end)

        self.mips.move(dst, Reg.t1)

    @mips_comment("LengthNode")
    @when(LengthNode)
    def visit(self, node: LengthNode):  # noqa
        self.mips.comment("LengthNode")
        self.load_memory(Reg.s1, node.msg)
        self.get_string_length(Reg.s1, Reg.s0)
        self.store_memory(Reg.s0, node.dest)

    @mips_comment("Auxiliar - Copy string")
    def copy_str(self, src: Reg, dst: Reg, result: Reg):
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(Reg.t0, src)
        self.mips.move(Reg.t1, dst)

        self.mips.label(loop)

        self.mips.lb(Reg.t2, self.mips.offset(Reg.t0))
        self.mips.sb(Reg.t2, self.mips.offset(Reg.t1))

        self.mips.beqz(Reg.t2, end)

        self.mips.addi(Reg.t0, Reg.t0, 1)
        self.mips.addi(Reg.t1, Reg.t1, 1)

        self.mips.j(loop)
        self.mips.label(end)

        self.mips.move(result, Reg.t1)

    @mips_comment("ConcatNode")
    @when(ConcatNode)
    def visit(self, node: ConcatNode):  # noqa
        self.load_memory(Reg.s0, node.msg1)
        self.load_memory(Reg.s1, node.msg2)

        self.get_string_length(Reg.s0, Reg.s4)
        self.get_string_length(Reg.s1, Reg.s5)

        self.mips.add(Reg.a0, Reg.s4, Reg.s5)  # WARNING: Divide in 2, from half to byte
        self.mips.sbrk()
        self.mips.move(Reg.s3, Reg.v0)  # The new space reserved

        self.copy_str(Reg.s0, Reg.s3, Reg.v0)
        self.copy_str(Reg.s1, Reg.v0, Reg.v0)

        self.store_memory(Reg.s3, node.dest)

    @mips_comment("Auxiliar - Copy substring")
    def copy_substr(self, src: Reg, dst: Reg, length: Reg):
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(Reg.t0, src)
        self.mips.move(Reg.t1, dst)

        self.mips.move(Reg.t3, length)  # i = length

        self.mips.label(loop)

        self.mips.lb(Reg.t2, self.mips.offset(Reg.t0))
        self.mips.sb(Reg.t2, self.mips.offset(Reg.t1))

        self.mips.addi(Reg.t0, Reg.t0, 1)
        self.mips.addi(Reg.t1, Reg.t1, 1)

        self.mips.addi(Reg.t3, Reg.t3, -1)  # i --

        self.mips.beqz(Reg.t3, end)
        self.mips.j(loop)

        self.mips.label(end)

        self.mips.move(Reg.t2, Reg.zero)
        self.mips.sb(Reg.t2, self.mips.offset(Reg.t1))  # copy zero to the end

    @mips_comment("SubstringNode")
    @when(SubstringNode)
    def visit(self, node: SubstringNode):  # noqa: F811
        # self.mips.li(Reg.a0, 10)
        # self.mips.print_int()
        self.load_memory(Reg.s0, node.msg1)
        self.load_memory(Reg.s1, node.length)
        self.load_memory(Reg.s3, node.start)

        self.mips.add(Reg.s0, Reg.s0, Reg.s3)

        self.mips.move(Reg.a0, Reg.s1)  # allocate heap memory
        # self.mips.print_int()
        self.mips.sbrk()
        self.copy_substr(Reg.s0, Reg.v0, Reg.s1)

        self.store_memory(Reg.v0, node.dest)

    @mips_comment("StringEqualNode")
    @when(StringEqualNode)
    def visit(self, node: StringEqualNode):  # noqa: F811
        end_label = self.get_label()
        end_ok_label = self.get_label()
        loop_label = self.get_label()

        self.load_memory(Reg.s0, node.msg1)  # load string address
        self.load_memory(Reg.s1, node.msg2)

        self.get_string_length(Reg.s0, Reg.s2)  # load size of string
        self.get_string_length(Reg.s1, Reg.s3)

        self.mips.move(Reg.v0, Reg.zero)  # return 0
        self.mips.bne(Reg.s2, Reg.s3, end_label)  # end and return 0 if size not equal

        self.mips.move(Reg.s2, Reg.s0)  # lets use temporal register
        self.mips.move(Reg.s3, Reg.s1)

        self.mips.label(loop_label)

        self.mips.lb(Reg.s4, self.mips.offset(Reg.s2))  # load string character
        self.mips.lb(Reg.s5, self.mips.offset(Reg.s3))

        self.mips.bne(Reg.s4, Reg.s5, end_label)  # if no equal then return 0

        self.mips.addi(Reg.s2, Reg.s2, 1)  # move next character
        self.mips.addi(Reg.s3, Reg.s3, 1)

        self.mips.beqz(
            Reg.s4, end_ok_label
        )  # if end the string return 1 (they are equal)
        self.mips.j(loop_label)  # continue loop

        self.mips.label(end_ok_label)
        self.mips.li(Reg.v0, 1)  # return 1
        self.mips.label(end_label)
        self.mips.store_memory(Reg.v0, node.dest)  # store value in dst

    @mips_comment("GetAttribNode")
    @when(GetAttribNode)
    def visit(self, node: GetAttribNode):  # noqa: F811
        self.load_memory(Reg.s0, node.obj)

        type_data = self.types_offsets[node.type]
        offset = type_data.attr_offsets[node.attrib] * DATA_SIZE
        self.mips.load_memory(Reg.s1, self.mips.offset(Reg.s0, offset))

        # label = self.get_label()
        # tag = f"{label}_{node.type}_{node.attrib}"
        # self.mips.write_data(tag + ":")
        # self.mips.asciiz(f"{node.attrib}, {node.type}")
        # self.mips.la(Reg.a0, tag)
        # self.mips.print_string()
        # self.mips.la(Reg.a0, "eol")
        # self.mips.print_string()
        # self.mips.move(Reg.a0, Reg.s1)
        # self.mips.print_int()
        # self.mips.la(Reg.a0, "eol")
        # self.mips.print_string()

        self.store_memory(Reg.s1, node.dest)

    @mips_comment("SetAttribNode")
    @when(SetAttribNode)
    def visit(self, node: SetAttribNode):  # noqa: F811
        self.load_memory(Reg.s0, node.obj)
        type_data = self.types_offsets[node.type]
        offset = type_data.attr_offsets[node.attrib] * DATA_SIZE
        if node.value in self.local_vars_offsets or node.value in self.actual_args:
            self.mips.comment(f"Setting local var {node.value}")
            self.load_memory(Reg.s1, node.value)

            # label = self.get_label()
            # tag = f"{label}_{node.type}_{node.attrib}"
            # self.mips.write_data(tag + ":")
            # self.mips.asciiz(f"{node.attrib}, {node.type}, {offset}")
            # self.mips.la(Reg.a0, tag)
            # self.mips.print_string()
            # self.mips.la(Reg.a0, "eol")
            # self.mips.print_string()
            # self.mips.move(Reg.a0, Reg.s1)
            # self.mips.print_int()
            # self.mips.la(Reg.a0, "eol")
            # self.mips.print_string()
        else:
            try:
                value = int(node.value)
                # high = value >> 16
                # self.mips.comment(f"Seting literal int {node.value}")
                # self.mips.li(Reg.s2, high)
                # self.mips.li(Reg.s3, value)
                # self.mips.sll(Reg.s4, Reg.s2, 16)
                # self.mips.orr(Reg.s1, Reg.s3, Reg.s4)
                self.mips.li(Reg.s1, value)
            except ValueError:
                self.mips.comment(f"Setting data {node.value}")
                self.mips.la(Reg.s1, node.value)
        self.mips.store_memory(Reg.s1, self.mips.offset(Reg.s0, offset))

    @mips_comment("LabelNode")
    @when(LabelNode)
    def visit(self, node: LabelNode):  # noqa: F811
        self.mips.label(node.label)

    @mips_comment("GotoNode")
    @when(GotoNode)
    def visit(self, node: GotoNode):  # noqa: F811
        self.mips.j(node.label)

    @mips_comment("GotoIfNode")
    @when(GotoIfNode)
    def visit(self, node: GotoIfNode):  # noqa: F811: F811
        self.load_memory(Reg.s0, node.value)
        self.mips.li(Reg.s1, 0)
        self.mips.bne(Reg.s0, Reg.s1, node.label)
