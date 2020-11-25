from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode \
    , MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode    \
    , ArgNode, ReturnNode, ReadStrNode, ReadIntNode, PrintStrNode, PrintIntNode, LengthNode, ConcatNode, PrefixNode     \
    , SubstringNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode    \
    , DataNode, LessNode, LessEqNode, ComplementNode, IsVoidNode, EqualNode, ConformNode         \
    , CleanArgsNode, ErrorNode, CopyNode, TypeNameNode, StringEqualNode
from .utils import on, when, TypeData


class CIL_TO_MIPS(object):
    def __init__(self):
        self.DOTTEXT = []
        self.DOTDATA = []
        self.types = []
        self.types_offsets = dict()
        self.local_vars_offsets = dict()
        self.actual_args = dict()

    def write_inst(self, instruction:str, tabs=0):
        self.DOTTEXT.append(f'{instruction}')
    
    def write_data(self, data:str, tabs=0):
        self.DOTDATA.append(f'{data}')

    def build_types_data(self, types):
        for idx, typex in enumerate(types):
            self.types_offsets[typex.name] = TypeData(idx, typex)

    def compile(self):
        return '\n'.join([ '.data'] + self.DOTDATA + ['.text'] + self.DOTTEXT)

    def write_push(self, register:str):
        pass

    def write_pop(self, register:str):
        pass

    @on('node')
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.types = node.dottypes
        self.build_types_data(self.types)

        for datanode in node.dotdata:
            self.visit(datanode)

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
        pass

    @when(ParamNode)
    def visit(self, node: ParamNode):
        pass

    @when(LocalNode)
    def visit(self, node: LocalNode):
        pass

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
    def visit(self, node:CleanArgsNode):
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
