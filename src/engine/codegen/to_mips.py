from .cil_ast import *
from ..cp import visitor
from .mips import MipsCode, MemoryType, MipsLabel, VTable, GlobalDescriptor, word_size, string_max_size
from .mips import Registers as reg
from typing import Dict, List


class CIL_TO_MIPS:

    def __init__(self, data_size=4):
        self.types = []
        # self.types_offsets: Dict[str, MemoryType] = dict()
        self.arguments = {}
        self.local_vars = {}
        self.data_segment = []
        self.data_size = data_size
        self.registers_to_save = [
            reg.ra,
            reg.s0,
            reg.s1,
            reg.s2,
            reg.s3,
            reg.s4,
            reg.s5,
            reg.s6,
        ]
        self.label_count = 0
        self.vtable_reg = reg.s7
        self.mips = MipsCode()

    # def build_types(self, types):
    #     for idx, typex in enumerate(types):
    #         self.types_offsets[typex.name] = TypeData(idx, typex)

    def fill_vtable(self):
        index = 0

        self.mips.comment("Build VTable")
        for name, tag in self.global_descriptor.vTable.methods.items():
            self.mips.comment(name)
            self.mips.la(reg.s0, tag)
            self.mips.store_memory(reg.s0, self.mips.offset(
                self.vtable_reg, index*self.data_size))
            index += 1

    def build_tags(self, dottypes: List[TypeNode]):
        base_tag = "classname_"

        tags = dict()

        for dottype in dottypes:
            name = base_tag + dottype.name
            tags[dottype.name] = name
            self.mips.data_label(name)
            self.mips.asciiz(dottype.name)

        return tags

    def get_offset(self, arg: str):
        if arg in self.arguments or arg in self.local_vars:
            offset = (
                self.arguments[arg]
                if arg in self.arguments
                else self.local_vars[arg]
            ) * 4
            return self.mips.offset(reg.fp, offset)
        else:
            raise Exception(
                f"load_memory: The direction {arg} isn't an address")

    def get_label(self):
        self.label_count += 1
        return f"mips_label_{self.label_count}"

    def load_memory(self, dst, arg: str):
        self.mips.comment(f"Load from {arg} to {dst}")
        if arg in self.arguments or arg in self.local_vars:
            offset = (
                self.arguments[arg]
                if arg in self.arguments
                else self.local_vars[arg]
            ) * self.data_size
            self.mips.load_memory(dst, self.mips.offset(reg.fp, offset))
        elif arg in self.data_segment:
            self.mips.la(dst, arg)
        else:
            raise Exception(
                f"load_memory: The direction {arg} isn't an address")

    def store_memory(self, src, dst: str):

        self.mips.comment(f"from src: {src} to dst: {dst}")
        if dst in self.arguments or dst in self.local_vars:
            offset = (
                self.arguments[dst]
                if dst in self.arguments
                else self.local_vars[dst]
            ) * self.data_size
            offset = self.mips.offset(reg.fp, offset)
            self.mips.store_memory(src, offset)
        else:
            raise Exception(
                f"store_memory: The direction {dst} isn't an address")
        self.mips.empty_line()

    def store_registers(self):
        self.mips.comment("Saving Registers")
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

        tags = self.build_tags(node.dottypes)

        self.global_descriptor = GlobalDescriptor(node.dottypes, tags)

        for data in node.dotdata:
            self.visit(data)
            self.data_segment.append(data.name)

        self.mips.label('main')
        self.mips.allocate_vtable(
            self.global_descriptor.vTable.size(), self.vtable_reg)

        self.fill_vtable()
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
        localvars_count = len(node.localvars)
        self.mips.addi(reg.sp, reg.sp, - self.data_size * localvars_count)
        self.mips.empty_line()
        for idx, local in enumerate(node.localvars):
            self.visit(local, index=idx)

        self.mips.empty_line()
        self.store_registers()
        self.mips.empty_line()
        self.mips.comment("Generating body code")
        for instruction in node.instructions:
            self.visit(instruction)

        self.mips.empty_line()
        self.mips.comment("Restore registers")
        self.load_registers()
        self.mips.empty_line()

        self.mips.comment("Clean stack variable space")
        self.mips.addi(reg.sp, reg.sp, localvars_count * self.data_size)
        self.arguments = None
        self.mips.comment("Return")
        self.mips.pop(reg.fp)
        self.mips.jr(reg.ra)

    @visitor.when(DataNode)
    def visit(self, node: DataNode):
        self.mips.data_label(node.name)
        self.mips.asciiz(node.value)

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode, index=0):
        self.arguments[node.name] = index + 1

    @visitor.when(LocalNode)
    def visit(self, node: LocalNode, index=0):
        if node.name in self.local_vars:
            pass
        else:
            self.local_vars[node.name] = -(index + 1)

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        self.mips.comment(
            f"GetAttribNode {node.dest} = {node.obj}.{node.attrib} Type:{node.type}")
        self.load_memory(reg.t0, node.obj)
        # get type info
        type_descritptor: MemoryType = self.global_descriptor.Types[node.type]
        # get attr offset
        offset = type_descritptor.get_attr_index(node.attrib)
        # retrieve offset from memory
        self.mips.load_memory(reg.t1, self.mips.offset(
            reg.t0, offset * self.data_size))
        self.store_memory(reg.t1, node.dest)

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        self.mips.comment(
            f"SetAttribNode {node.obj}.{node.attrib} Type:{node.type} = {node.value}")
        # get type info
        type_descritptor: MemoryType = self.global_descriptor.Types[node.type]
        # get attr offset
        offset = type_descritptor.get_attr_index(node.attrib)
        # get object reference into s0
        self.load_memory(reg.s0, node.obj)

        if node.value in self.local_vars or node.value in self.arguments:
            self.mips.comment(f"SET local var {node.value}")
            self.load_memory(reg.s1, node.value)
        else:
            try:
                value = int(node.value)
                self.mips.li(reg.s1, value)
            except ValueError:
                if node.value in self.data_segment:
                    self.mips.comment(f"SET data {node.value}")
                    self.mips.la(reg.s1, node.value)
                else:
                    raise Exception(f"Setattr: label {node.value} not found")

        self.mips.store_memory(reg.s1, self.mips.offset(
            reg.s0, offset * self.data_size))

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        self.load_memory(reg.t0, node.source)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(ComplementNode)
    def visit(self, node: ComplementNode):
        self.load_memory(reg.t0, node.expression)
        self.mips.nor(reg.t1, reg.t0, reg.t0)
        self.store_memory(reg.t1, node.dest)

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)
        self.mips.add(reg.t2, reg.t0, reg.t1)
        self.store_memory(reg.t2, node.dest)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)
        self.mips.sub(reg.t2, reg.t0, reg.t1)
        self.store_memory(reg.t2, node.dest)

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)
        self.mips.mult(reg.t0, reg.t1)
        self.mips.mflo(reg.t0)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)
        self.mips.div(reg.t2, reg.t0, reg.t1)
        self.mips.mflo(reg.t0)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)
        self.mips.slt(reg.t2, reg.t0, reg.t1)
        self.mips.slt(reg.t3, reg.t1, reg.t0)

        self.mips.add(reg.t0, reg.t2, reg.t3)
        self.mips.slti(reg.t1, reg.t0, 1)

        self.store_memory(reg.t1, node.dest)

    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)
        self.mips.slt(reg.t2, reg.t1, reg.t0)
        self.mips.li(reg.t3, 1)
        self.mips.sub(reg.t0, reg.t3, reg.t2)
        self.store_memory(reg.t0, node.dest)

    @visitor.when(LessNode)
    def visit(self, node: LessNode):
        self.load_memory(reg.t0, node.left)
        self.load_memory(reg.t1, node.right)
        self.mips.slt(reg.t2, reg.t0, reg.t1)
        self.store_memory(reg.t2, node.dest)

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode):
        self.mips.comment("IsVoidNode")
        self.load_memory(reg.t0, node.expression)

        label = self.get_label()

        self.mips.li(reg.t1, 0)
        self.mips.bne(reg.t0, reg.t1, label)
        self.mips.li(reg.t1, 1)
        self.mips.label(label)
        self.store_memory(reg.t1, node.dest)

    @visitor.when(AllocateNode)
    def visit(self, node: AllocateNode):
        #   ----------
        #   |   ID   |
        #   ----------
        #   |  Size  |
        #   ----------
        #   |Ptr_Name|
        #   ----------
        #   |Ptr_Vtbl|
        #   ----------
        #   |  Attr1 |
        #   ----------
        #   |  Attr2 |
        #   ..........
        #   ..........
        #
        #   s1 start addr of the class
        #
        self.mips.comment(f"Allocate space for {node.type}")
        type_descritptor: MemoryType = self.global_descriptor.Types[node.type]

        length = type_descritptor.size()
        length *= self.data_size

        # sbrk call
        self.mips.li(reg.a0, length)
        self.mips.sbrk()
        self.mips.move(reg.s1, reg.v0)

        # pass object reference to node.dest
        self.store_memory(reg.s1, node.dest)

        # Store Class ID
        self.mips.li(reg.s0, type_descritptor.id)
        self.mips.store_memory(reg.s0, self.mips.offset(reg.s1))

        # Store Class size
        self.mips.li(reg.s0, length)
        self.mips.store_memory(
            reg.s0, self.mips.offset(reg.s1, self.data_size))

        # Store Class Name Ptr
        self.mips.la(reg.s0, type_descritptor.ptr_name)
        self.mips.store_memory(
            reg.s0, self.mips.offset(reg.s1, 2 * self.data_size))

        # Store Class Vtable Ptr
        self.mips.li(reg.s0, type_descritptor.vtable *
                     self.data_size)  # first function on vtable
        self.mips.store_memory(
            reg.s0, self.mips.offset(reg.s1, 3 * self.data_size))

        # Reserve Attrs Space
        for number, _ in enumerate(type_descritptor.attrs):
            _offset = 4 + number
            self.mips.store_memory(reg.zero, self.mips.offset(
                reg.s1, _offset * self.data_size))

    @visitor.when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        self.mips.comment(f"TypeOfNode of {node.obj}")
        # Cargar la direccion de memoria
        self.load_memory(reg.s0, node.obj)
        # El offset 3 para ptr al name
        self.mips.load_memory(reg.s1, self.mips.offset(reg.s0, 3))
        self.store_memory(reg.s1, node.dest)

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
        self.store_memory(reg.v0, node.dest)

    @visitor.when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        self.mips.comment(f"DynamicCallNode {node.type} {node.method}")
        type_descritptor: MemoryType = self.global_descriptor.Types[node.type]

        # self.mips.move(reg.a0, reg.s7)
        # self.mips.syscall(1)

        offset = type_descritptor.get_method_index(
            node.method) * self.data_size
        # print("offset", offset, node.method, node.type, type_descritptor.methods)
        # print(node.obj, node.type)
        self.load_memory(reg.s0, node.obj)

        # vtable ptr in position 4 (0 .. 3)
        self.mips.load_memory(
            reg.s1, self.mips.offset(reg.s0, 3 * self.data_size))

        # print(type_descritptor.get_method_index(node.method))
        self.mips.addi(reg.s2, reg.s1, offset)
        self.mips.addu(reg.s3, reg.s2, reg.s7)

        # retrieve function location
        self.mips.load_memory(reg.s4, self.mips.offset(reg.s3))

        # retrieve result from v0
        self.mips.jalr(reg.s4)
        self.store_memory(reg.v0, node.dest)

    @visitor.when(ArgNode)
    def visit(self, node: ArgNode):
        self.mips.comment(f"ArgNode {node.name} to s0")
        self.load_memory(reg.s0, node.name)
        self.mips.push(reg.s0)

    @visitor.when(ErrorNode)
    def visit(self, node: ErrorNode):
        self.mips.comment("ErrorNode")
        self.mips.li(reg.a0, 1)
        self.mips.syscall(17)

    @visitor.when(BoxNode)
    def visit(self, node: BoxNode):
        self.mips.li(reg.s0, node.value)
        self.store_memory(reg.s0, node.dest)

    @visitor.when(AbortNode)
    def visit(self, node: AbortNode):
        self.mips.exit()
        self.mips.empty_line()

    def copy_data(self, src, dst, length):
        """
        length: fixed in bytes size.
        """
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(reg.t0, src)
        self.mips.move(reg.t1, dst)
        self.mips.move(reg.t3, length)  # i = length

        self.mips.label(loop)

        self.mips.lb(reg.t2, self.mips.offset(reg.t0))
        self.mips.sb(reg.t2, self.mips.offset(reg.t1))

        self.mips.addi(reg.t0, reg.t0, 2)
        self.mips.addi(reg.t1, reg.t1, 2)

        self.mips.addi(reg.t3, reg.t3, -1)  # i --

        self.mips.beqz(reg.t3, end)
        self.mips.j(loop)

        self.mips.label(end)

    @visitor.when(CopyNode)
    def visit(self, node):
        self.mips.comment(f"Copy Node {node.dest} {node.obj}")
        # load object
        self.load_memory(reg.s0, node.obj)
        # load size
        self.load_memory(reg.s1, self.mips.offset(reg.s0, self.data_size))
        # load dest
        self.load_memory(reg.s3, node.dest)
        # copy byte to byte
        self.copy_data(reg.s0, reg.s3, reg.s1)

    @visitor.when(TypeNameNode)
    def visit(self, node: TypeNameNode):
        self.mips.comment(f"TypeNameNode {node.dest} Type:{node.type}")
        self.load_memory(reg.t0, node.type)
        self.mips.load_memory(reg.t1, self.mips.offset(reg.t0, self.data_size))
        self.store_memory(reg.t1, node.dest)

    def get_string_length(self, src, dst):
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(reg.t0, src)
        self.mips.li(reg.t1, 0)

        self.mips.label(loop)

        self.mips.lb(reg.t3, self.mips.offset(reg.t0))
        self.mips.beqz(reg.t3, end)

        self.mips.addi(reg.t1, reg.t1, 1)
        self.mips.addi(reg.t0, reg.t0, 1)

        self.mips.j(loop)
        self.mips.label(end)

        self.mips.move(dst, reg.t1)

    @visitor.when(LengthNode)
    def visit(self, node: LengthNode):
        self.mips.comment("LengthNode")
        self.load_memory(reg.s1, node.msg)
        self.get_string_length(reg.s1, reg.s0)
        self.store_memory(reg.s0, node.dest)

    def copy_str(self, src, dst, result):
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(reg.t0, src)
        self.mips.move(reg.t1, dst)

        self.mips.label(loop)

        self.mips.lb(reg.t2, self.mips.offset(reg.t0))
        self.mips.sb(reg.t2, self.mips.offset(reg.t1))

        self.mips.beqz(reg.t2, end)

        self.mips.addi(reg.t0, reg.t0, 1)
        self.mips.addi(reg.t1, reg.t1, 1)

        self.mips.j(loop)
        self.mips.label(end)

        self.mips.move(result, reg.t1)

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        self.load_memory(reg.s0, node.msg1)
        self.load_memory(reg.s1, node.msg2)

        self.get_string_length(reg.s0, reg.s4)
        self.get_string_length(reg.s1, reg.s5)

        self.mips.add(reg.a0, reg.s4, reg.s5)
        self.mips.sbrk()
        self.mips.move(reg.s3, reg.v0)

        self.copy_str(reg.s0, reg.s3, reg.v0)
        self.copy_str(reg.s1, reg.v0, reg.v0)

        self.store_memory(reg.s3, node.dest)

    @visitor.when(StringEqualNode)
    def visit(self, node: StringEqualNode):
        self.mips.empty_line()
        self.mips.comment('Comparing Strings --')
        end_label = self.get_label()
        end_ok_label = self.get_label()
        end_wrong_label = self.get_label()
        loop_label = self.get_label()
        self.load_memory(reg.s0, node.msg1)

        self.mips.move(reg.a0, reg.s0)
        self.mips.syscall(1)

        self.load_memory(reg.s1, node.msg2)

        self.mips.move(reg.t8, reg.s0)
        self.mips.move(reg.t9, reg.s1)

        self.mips.label(loop_label)
        # me parece q aki esta fallando xq esta cargando un "0"
        # en $t8, y cuando le pide el offset, no tiene nada, hay q ver ahi
        # pero con el "1" hace lo mismo

        self.mips.lb(reg.a0, self.mips.offset(reg.t8))
        self.mips.lb(reg.a1, self.mips.offset(reg.t9))

        self.mips.beqz(reg.a0, end_ok_label)
        self.mips.beqz(reg.a1, end_wrong_label)
        self.mips.seq(reg.v0, reg.a0, reg.a1)
        self.mips.beqz(reg.v0, end_wrong_label)

        self.mips.addi(reg.t8, reg.t8, 1)
        self.mips.addi(reg.t9, reg.t9, 1)
        self.mips.j(loop_label)

        self.mips.label(end_wrong_label)
        self.mips.li(reg.v0, 0)
        self.mips.j(end_label)
        self.mips.label(end_ok_label)
        self.mips.bnez(reg.a1, end_wrong_label)
        self.mips.li(reg.v0, 1)
        self.mips.label(end_label)

        self.store_memory(reg.v0, node.dest)

    @visitor.when(LoadNode)
    def visit(self, node: LoadNode):
        self.load_memory(reg.s0, node.msg)
        self.store_memory(reg.s0, node.dest)

    def copy_substr(self, src, dst, length):
        loop = self.get_label()
        end = self.get_label()

        self.mips.move(reg.t0, src)
        self.mips.move(reg.t1, dst)

        self.mips.move(reg.t3, length)

        self.mips.label(loop)

        self.mips.lb(reg.t2, self.mips.offset(reg.t0))
        self.mips.sb(reg.t2, self.mips.offset(reg.t1))

        self.mips.addi(reg.t0, reg.t0, 1)
        self.mips.addi(reg.t1, reg.t1, 1)

        self.mips.addi(reg.t3, reg.t3, -1)

        self.mips.beqz(reg.t3, end)
        self.mips.j(loop)

        self.mips.label(end)

        self.mips.move(reg.t2, reg.zero)
        self.mips.sb(reg.t2, self.mips.offset(reg.t1))

    @visitor.when(SubstringNode)
    def visit(self, node):
        self.load_memory(reg.s0, node.msg1)
        self.load_memory(reg.s1, node.length)
        self.load_memory(reg.s3, node.start)

        self.mips.add(reg.s0, reg.s0, reg.s3)

        self.mips.move(reg.a0, reg.s1)
        self.mips.sbrk()
        self.copy_substr(reg.s0, reg.v0, reg.s1)

        self.store_memory(reg.v0, node.dest)

    @visitor.when(ReadStrNode)
    def visit(self, node):
        self.mips.li(reg.a0, 1024)
        self.mips.sbrk()
        self.mips.move(reg.a0, reg.v0)
        self.store_memory(reg.v0, node.dest)
        self.mips.li(reg.a1, 1024)
        self.mips.read_string()

    @visitor.when(PrintStrNode)
    def visit(self, node: PrintStrNode):
        self.mips.comment(f"Print str {node.str_addr}")
        self.load_memory(reg.a0, node.str_addr)
        self.mips.print_str(node.str_addr)

    @visitor.when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        self.mips.read_int()
        self.store_memory(reg.v0, node.dest)

    @visitor.when(PrintIntNode)
    def visit(self, node: PrintIntNode):
        self.load_memory(reg.a0, node.str_addr)
        self.mips.print_int(node.str_addr)

    @visitor.when(EmptyArgs)
    def visit(self, node: EmptyArgs):
        self.mips.addi(reg.sp, reg.sp, node.args * self.data_size)

    @visitor.when(ReturnNode)
    def visit(self, node: ReturnNode):
        self.mips.comment("ReturnNode")
        self.load_memory(reg.v0, node.value)

    @visitor.when(VoidNode)
    def visit(self, node: VoidNode):
        self.store_memory(reg.zero, node.dest)
