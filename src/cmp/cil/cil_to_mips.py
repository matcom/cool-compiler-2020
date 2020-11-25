from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode, MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode, ArgNode, ReturnNode, ReadStrNode, ReadIntNode, PrintStrNode, PrintIntNode, LengthNode, ConcatNode, PrefixNode, SubstringNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode, DataNode, LessNode, LessEqNode, ComplementNode, IsVoidNode, EqualNode, ConformNode, CleanArgsNode, ErrorNode, CopyNode, TypeNameNode, StringEqualNode
from .utils.mips_syntax import Mips, Register as Reg


class CIL_TO_MIPS(Mips):
    def __init__(self):
        self.DOTTEXT = []
        self.DOTDATA = []
        self.types = []
        self.types_offsets = dict()
        self.local_vars_offsets = dict()
        self.actual_args = dict()

    def write_inst(self, instruction: str, tabs=0):
        self.DOTTEXT.append(f'{instruction}')

    def write_data(self, data: str, tabs=0):
        self.DOTDATA.append(f'{data}')

    def build_types_data(self, types):
        for idx, typex in enumerate(types):
            self.types_offsets[typex.name] = TypeData(idx, typex)

    def compile(self):
        return '\n'.join(['.data'] + self.DOTDATA + ['.text'] + self.DOTTEXT)

    def write_push(self, register: str):
        """
        `add $sp , $sp , -8`

        And then write to address `0($sp)`
        """
        self.write_inst(Mips.addi(Reg.sp, Reg.sp, -8))
        self.write_store_memory(register, Mips.reg_offset(Reg.sp))


    def write_pop(self, register: str):
        """
        First, load from to address `0($sp)` and then write `add $sp , $sp , 8` to restore the stack pointer
        """
        self.write_load_memory(register, "0($sp)")
        self.write_inst(f"add $sp , $sp , 8")

    def write_load_memory(self, register: str, address: str):
        """
        Load from a specific address a 32 bits register
        """
        self.write_inst(f"lw $t0 , {address}")
        self.write_inst(f"sll $t0 , $t0 , 16")
        self.write_inst(f"lw $t1, {address} + 4")
        self.write_inst(f"or {register} ,$t0 , $t1")

    def write_store_memory(self, register: str, address: str):
        """
        Write to a specific address a 32 bits register
        """
        self.write_inst(f"sw $t1 , {address} + 4")
        self.write_inst(f"srl $t1 , $t1 , 16")
        self.write_inst(f"sw $t0 , {address}")
        self.write_inst(f"or {register} ,$t0 , $t1")

    @on('node')
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.types = node.dottypes
        self.build_types_data(self.types)

        for datanode in node.dotdata:
            self.visit(datanode)

        self.write_inst(f'main: ;')

        self.write_inst(f'jal entry')

        self.write_inst('li $v0, 10')
        self.write_inst('syscall')

        for function in node.dotcode:
            self.visit(function)

    @when(DataNode)
    def visit(self, node: DataNode):
        self.write_data(f'{node.name}: .asciiz "{node.value}"')

    @when(TypeNode)
    def visit(self, node: TypeNode):
        pass

    @when(FunctionNode)
    def visit(self, node: FunctionNode):
        self.write_inst('')
        self.write_inst(f'{node.name}: ;')
        self.write_push('$fp')
        self.write_inst('add $fp, $0, $sp')
        self.actual_args = dict()

        self.write_inst('')
        for idx, param in enumerate(node.params):
            self.visit(param, index=idx)

        self.write_inst('')
        for idx, local in enumerate(node.localvars):
            self.visit(local, index=idx)

        self.write_inst('')
        # self.store_registers()
        self.write_inst('')
        for instruction in node.instructions:
            self.visit(instruction)

        self.actual_args = None
        self.write_inst('')
        # self.load_registers()

        for _ in node.localvars:
            self.write_inst('addi $sp, $sp, 8')
        self.write_pop('$fp')
        self.write_inst('jr $ra')
        self.write_inst('')

    @when(ParamNode)
    def visit(self, node: ParamNode, index=0):
        self.actual_args[node.name] = index

    @when(LocalNode)
    def visit(self, node: LocalNode, index=0):
        self.write_push('$zero')
        assert not node.name in self.local_vars_offsets, f'Impossible {node.name}...'
        self.local_vars_offsets[node.name] = index

    @when(CopyNode)
    def visit(self, node: CopyNode):
        pass

    @when(TypeNameNode)
    def visit(self, node: TypeNameNode):
        pass

    @when(ErrorNode)
    def visit(self, node: ErrorNode):
        pass

    @when(AssignNode)
    def visit(self, node: AssignNode):
        pass

    @when(ConformNode)
    def visit(self, node: ConformNode):
        pass

    @when(IsVoidNode)
    def visit(self, node: IsVoidNode):
        pass

    @when(ComplementNode)
    def visit(self, node: ComplementNode):
        pass

    @when(LessNode)
    def visit(self, node: LessNode):
        pass

    @when(EqualNode)
    def visit(self, node: EqualNode):
        pass

    @when(LessEqNode)
    def visit(self, node: LessEqNode):
        pass

    @when(PlusNode)
    def visit(self, node: PlusNode):
        pass

    @when(MinusNode)
    def visit(self, node: MinusNode):
        pass

    @when(StarNode)
    def visit(self, node: StarNode):
        pass

    @when(DivNode)
    def visit(self, node: DivNode):
        pass

    @when(AllocateNode)
    def visit(self, node: AllocateNode):
        pass

    @when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        pass

    @when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        pass

    @when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        pass

    @when(ArgNode)
    def visit(self, node: ArgNode):
        pass

    @when(CleanArgsNode)
    def visit(self, node: CleanArgsNode):
        pass

    @when(ReturnNode)
    def visit(self, node: ReturnNode):
        pass

    @when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        pass

    @when(ReadStrNode)
    def visit(self, node: ReadStrNode):
        pass

    @when(PrintIntNode)
    def visit(self, node: PrintIntNode):
        pass

    @when(PrintStrNode)
    def visit(self, node: PrintStrNode):
        pass

    @when(LengthNode)
    def visit(self, node: LengthNode):
        pass

    @when(ConcatNode)
    def visit(self, node: ConcatNode):
        pass

    @when(PrefixNode)
    def visit(self, node: PrefixNode):
        pass

    @when(SubstringNode)
    def visit(self, node: SubstringNode):
        pass

    @when(StringEqualNode)
    def visit(self, node: StringEqualNode):
        pass

    @when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        pass

    @when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        pass

    @when(LabelNode)
    def visit(self, node: LabelNode):
        pass

    @when(GotoNode)
    def visit(self, node: GotoNode):
        pass

    @when(GotoIfNode)
    def visit(self, node: GotoIfNode):
        pass
