from .semantic_utils import Context, SemanticException, Type, ErrorType, VoidType
from ..utils import on, when
from ..errors import SemanticError
from ..ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode, IdNode,\
                    IfThenElseNode, WhileLoopNode, BlockNode, LetInNode, ArithmeticNode, BoolNode,    \
                    CaseOfNode, LetNode, CaseNode, AssignNode, FunctionCallNode, NewNode, IntegerNode,\
                    MemberCallNode, LessEqualNode, LessNode, EqualNode, ComplementNode, StringNode,   \
                    IsVoidNode, NotNode

class COOL_FORMATTER(object):
    def __init__(self, context: Context, errors=[]):
        self.current_class = None
        self.current_method = None
        self.context = context
        self.errors = errors

        self.type_int = self.context.get_type('Int')
        self.type_str = self.context.get_type('String')
        self.type_obj = self.context.get_type('Object')
        self.type_io = self.context.get_type('IO')
        self.type_bool = self.context.get_type('Bool')

    @on('node')
    def visit(self, node, tabs):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode, scope):
        pass

    @when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope):
        pass

    @when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope):
        pass

    @when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope):
        pass

    @when(IfThenElseNode)
    def visit(self, node: IfThenElseNode, scope):
        pass

    @when(WhileLoopNode)
    def visit(self, node: WhileLoopNode, scope):
        pass

    @when(BlockNode)
    def visit(self, node: BlockNode, scope):
        pass

    @when(LetNode)
    def visit(self, node: LetNode, scope):
        pass
        
    @when(LetInNode)
    def visit(self, node: LetInNode, scope):
        pass

    @when(CaseNode)
    def visit(self, node: CaseNode, scope):
        pass

    @when(CaseOfNode)
    def visit(self, node: CaseOfNode, scope):
        pass

    @when(AssignNode)
    def visit(self, node: AssignNode, scope):
        pass

    @when(MemberCallNode)
    def visit(self, node: MemberCallNode, scope):
        pass

    @when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope):
        pass

    @when(NewNode)
    def visit(self, node: NewNode, scope):
        pass

    @when(NotNode)
    def visit(self, node: NotNode, scope):
        pass

    @when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope):
        pass

    @when(ComplementNode)
    def visit(self, node: ComplementNode, scope):
        pass

    @when(ArithmeticNode)
    def visit(self, node: ArithmeticNode, scope):
        pass

    @when(EqualNode)
    def visit(self, node: EqualNode, scope):
        pass

    @when(LessEqualNode)
    def visit(self, node: LessEqualNode, scope):
        pass

    @when(LessNode)
    def visit(self, node: LessNode, scope):
        pass

    @when(IdNode)
    def visit(self, node: IdNode, scope):
        pass

    @when(BoolNode)
    def visit(self, node: BoolNode, scope):
        node.static_type = self.type_bool

    @when(IntegerNode)
    def visit(self, node: IntegerNode, scope):
        node.static_type = self.type_int

    @when(StringNode)
    def visit(self, node: StringNode, scope):
        node.static_type = self.type_str
