from .cil_ast import *
from ..cp import visitor
from .mips import MipsCode, TypeData
from .mips import Registers as reg
from typing import Dict, List


class CIL_TO_MIPS:

    def __init__(self, data_size=8):
        self.types = []
        self.types_offsets: Dict[str, TypeData] = dict()
        self.arguments = {}
        self.local_vars = {}
        self.data_size = data_size
        self.registers_to_save = [reg.ra]
        self.label_count = 0
        self.mips = MipsCode()

    def build_types(self, types):
        for idx, typex in enumerate(types):
            self.types_offsets[typex.name] = TypeData(idx, typex)

    def get_pc(self, dst):
        label = self.get_label()
        end = self.get_label()

        self.mips.j(end)
        self.mips.label(label)
        self.mips.move(dst, reg.ra)
        self.mips.jr(reg.ra)
        self.mips.label(end)

        return label

    def get_label(self):
        return f"mip_label_{self.label_count}"
        self.label_count += 1

    def load_memory(self, dst, arg: str):
        if arg in self.arguments or arg in self.local_vars:
            offset = (
                self.arguments[arg] + 1
                if arg in self.arguments
                else -self.local_vars[arg]
            ) * self.data_size

            self.mips.load_memory(dst, self.mips.offset(reg.fp, offset))
        else:
            raise Exception(
                f"load_memory: The direction {arg} isn't an address")

    def store_memory(self, dst, arg: str):
        if arg in self.local_vars:
            offset = -self.local_vars[arg] * self.data_size
            self.mips.store_memory(dst, self.mips.offset(reg.fp, offset))
        else:
            raise Exception(
                f"store_memory: The direction {arg} isn't an address")

    def load_arithmetic(self, node: ArithmeticNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)

    def store_registers(self):
        for reg in self.registers_to_save:
            self.mips.push(reg)

    def load_registers(self):
        for reg in reversed(self.registers_to_save):
            self.mips.pop(reg)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):

        self.types = node.dottypes
        self.build_types(self.types)

        for data in node.dotdata:
            self.visit(data)

        self.mips.label('main')
        self.mips.jal('entry')
        self.mips.empty_line()
        self.mips.exit()

        for code in node.dotcode:
            self.visit(code)

    @visitor.when(TypeNode)
    def visit(self, node):
        pass

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        self.mips.label(node.name)

        self.mips.comment("Set stack frame")
        self.mips.push(reg.fp)
        self.mips.move(reg.fp, reg.sp)
        self.mips.empty_line()
        self.arguments = dict()

        for idx, param in enumerate(node.params):
            self.visit(param, index=idx)

        self.mips.comment("Allocate memory for Local variables")
        for idx, local in enumerate(node.localvars):
            self.visit(local, index=idx)

        self.store_registers()
        self.mips.comment("Generating body code")
        for instruction in node.instructions:
            self.visit(instruction)
        self.mips.empty_line()
        self.arguments = None
        self.load_registers()

        self.mips.comment("Clean stack variable space")
        self.mips.addi(reg.sp, reg.sp, len(node.localvars) * self.data_size)
        self.mips.comment("Return")
        self.mips.pop(reg.fp)
        self.mips.jr(reg.ra)

    @visitor.when(DataNode)
    def visit(self, node: DataNode):
        self.mips.data_label(node.name)
        self.mips.asciiz(node.value)

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode, index=0):
        self.arguments[node.name] = index

    @visitor.when(LocalNode)
    def visit(self, node: LocalNode, index=0):
        self.mips.push(reg.zero)
        if node.name in self.local_vars:
            pass
        else:
            self.local_vars[node.name] = index

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        self.mips.comment("GetAttribNode")
        self.load_memory(reg.t0, node.obj)
        type_data = self.types_offsets[node.type]
        offset = type_data.attr_offsets[node.attrib]
        self.mips.load_memory(reg.t1, self.mips.offset(reg.t0, offset))
        self.store_memory(reg.t1, node.dest)

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        self.mips.comment("SetAttribNode")
        self.load_memory(reg.t0, node.obj)
        type_data = self.types_offsets[node.type]
        offset = type_data.attr_offsets[node.attrib]
        if node.value in self.local_vars_offsets:
            self.load_memory(reg.t1, node.value)
        else:
            try:
                value = int(node.value)
                high = value >> 16
                self.mips.li(reg.t2, high)
                self.mips.li(reg.t3, value)
                self.mips.sll(reg.t4, reg.t2, 16)
                self.mips.or_(reg.t1, reg.t2, reg.t4)
            except ValueError:
                self.mips.la(reg.t1, node.value)
        self.mips.store_memory(reg.t1, self.mips.offset(reg.t0, offset))

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        self.mips.comment("AssignNode")
        self.load_memory(reg.t0, node.source)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(ComplementNode)
    def visit(self, node: ComplementNode):
        self.mips.comment("ComplementNode")
        self.load_memory(reg.t0, node.body)
        self.mips.nor(reg.t1, reg.t0, reg.t0)
        self.store_memory(reg.t1, node.dest)

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        self.load_arithmetic(node)
        self.mips.add(reg.t2, reg.t0, reg.t1)
        self.store_memory(reg.t2, node.dest)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        self.load_arithmetic(node)
        self.mips.sub(reg.t2, reg.t0, reg.t1)
        self.store_memory(reg.t2, node.dest)

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        self.load_arithmetic(node)
        self.mips.mult(reg.t2, reg.t0, reg.t1)
        self.mips.mflo(reg.t0)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        self.load_arithmetic(node)
        self.mips.div(reg.t2, reg.t0, reg.t1)
        self.mips.mflo(reg.t0)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        self.load_arithmetic(node)
        self.mips.slt(reg.t2, reg.t0, reg.t1)
        self.mips.slt(reg.t3, reg.t1, reg.t0)

        self.mips.add(reg.t0, reg.t2, reg.t3)
        self.mips.slti(reg.t1, reg.t0, 1)

        self.store_memory(reg.t1, node.dest)

    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode):
        self.load_arithmetic(node)
        self.mips.slt(reg.t2, reg.t1, reg.t0)
        self.mips.li(reg.t3, 1)
        self.mips.sub(reg.t0, reg.t3, reg.t2)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(LessNode)
    def visit(self, node: LessNode):
        self.load_arithmetic(node)
        self.mips.slt(reg.t2, reg.t0, reg.t1)
        self.store_memory(reg.t2, node.dest)

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode):
        self.mips.comment("IsVoidNode")
        self.load_memory(reg.t0, node.body)

        label = self.get_label()

        self.mips.li(reg.t1, 0)
        self.mips.bne(reg.t0, reg.t1, label)
        self.mips.li(reg.t1, 1)
        self.mips.label(label)
        self.store_memory(reg.t1, node.dest)

    @visitor.when(AllocateNode)
    def visit(self, node: AllocateNode):
        type_data = self.types_offsets[node.type]

        length = len(type_data.attr_offsets) + len(type_data.func_offsets) + 2
        length *= self.data_size / 2
        self.mips.li(reg.a0, length)
        self.mips.sbrk()
        self.store_memory(reg.v0, node.dest)
        self.mips.li(reg.t0, type_data.type)
        self.mips.store_memory(reg.t0, reg.v0)
        self.mips.la(reg.t0, type_data.str)
        self.mips.store_memory(
            reg.t0, self.mips.offset(reg.v0, 1 * self.data_size))

        for offset in type_data.attr_offsets.values():
            self.mips.store_memory(reg.zero, self.mips.offset(
                reg.v0, offset * self.data_size))

        for name, offset in type_data.func_offsets.items():
            direct_name = type_data.func_names[name]
            self.mips.la(reg.t0, direct_name)
            self.mips.store_memory(
                reg.t0,
                self.mips.offset(reg.v0, offset * self.data_size))

    @visitor.when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        self.mips.comment("TypeOfNode")
        self.mips.la(reg.t0, node.obj)
        self.load_memory(reg.t1, reg.t0)
        self.store_memory(reg.t1, node.dest)

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode):
        self.mips.label(node.label)

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode):
        self.mips.comment("GotoNode")
        self.mips.j(node.label)

    @visitor.when(IfGotoNode)
    def visit(self, node: IfGotoNode):
        self.mips.comment("IfGotoNode")
        self.load_memory(reg.t0, node.value)
        self.mips.li(reg.t1, 0)
        self.mips.bne(reg.t0, reg.t1, node.label)

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        self.mips.comment("StaticCallNode")
        self.mips.jal(node.function)

    @visitor.when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        self.mips.comment("DynamicCallNode")
        type_data = self.types_offsets[node.type]
        offset = type_data.func_offsets[node.method]
        self.load_memory(reg.t0, node.obj)
        self.mips.load_memory(reg.t1, self.mips.offset(reg.t0, offset))
        label_get_pc = self.get_pc(reg.t2)
        self.mips.jal(label_get_pc)
        self.mips.move(reg.ra, reg.t2)
        self.mips.addi(reg.ra, 12)
        self.mips.jr(reg.t1)

    @visitor.when(ArgNode)
    def visit(self, node: ArgNode):
        self.mips.comment("ArgNode")
        self.load_memory(reg.t0, node.name)
        self.mips.push(reg.t0)

    @visitor.when(ErrorNode)
    def visit(self, node: ErrorNode):
        self.mips.comment("ErrorNode")
        self.mips.li(reg.a0, 1)
        self.mips.syscall(17)

    @visitor.when(CopyNode)
    def visit(self, node):
        pass

    @visitor.when(TypeNameNode)
    def visit(self, node: TypeNameNode):
        self.mips.comment("TypeNameNode")
        self.load_memory(reg.t0, node.type)
        self.mips.load_memory(reg.t1, self.mips.offset(reg.t0, self.data_size))
        self.store_memory(reg.t1, node.dest)

    @visitor.when(LengthNode)
    def visit(self, node):
        pass

    @visitor.when(ConcatNode)
    def visit(self, node):
        pass

    @visitor.when(StringEqualNode)
    def visit(self, node):
        pass

    @visitor.when(ConcatNode)
    def visit(self, node):
        pass

    @visitor.when(LoadNode)
    def visit(self, node):
        pass

    @visitor.when(SubstringNode)
    def visit(self, node):
        pass

    @visitor.when(ToStrNode)
    def visit(self, node):
        pass

    @visitor.when(ToIntNode)
    def visit(self, node):
        pass

    @visitor.when(ReadNode)
    def visit(self, node):
        pass

    @visitor.when(PrintNode)
    def visit(self, node: PrintNode):
        self.load_memory(reg.a0, node.str_addr)
        self.mips.print_str(node.str_addr)

    @visitor.when(ReturnNode)
    def visit(self, node: ReturnNode):
        self.mips.comment("ReturnNode")
        self.load_memory(reg.v0, node.value)
