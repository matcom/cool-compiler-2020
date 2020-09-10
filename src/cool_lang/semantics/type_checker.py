from .semantic_utils import Context, SemanticException, Type, ErrorType, VoidType, Var, Scope
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

    def is_basic(self, typex):
        return typex in [self.type_str, self.type_bool, self.type_int]

    @on('node')
    def visit(self, node, scope):
        pass

    @when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope):
        pass

    @when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        pass

    @when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        pass

    @when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, scope:Scope):
        pass

    @when(IfThenElseNode)
    def visit(self, node:IfThenElseNode, scope:Scope):
        pass

    @when(WhileLoopNode)
    def visit(self, node:WhileLoopNode, scope:Scope):
        pass

    @when(BlockNode)
    def visit(self, node:BlockNode, scope:Scope):
        pass

    @when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        pass
        
    @when(LetInNode)
    def visit(self, node:LetInNode, scope:Scope):
        pass

    @when(CaseNode)
    def visit(self, node:CaseNode, scope:Scope):
        pass

    @when(CaseOfNode)
    def visit(self, node:CaseOfNode, scope:Scope):
        pass

    @when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        pass

    @when(MemberCallNode)
    def visit(self, node:MemberCallNode, scope:Scope):
        pass

    @when(FunctionCallNode)
    def visit(self, node:FunctionCallNode, scope:Scope):
        pass

    @when(NewNode)
    def visit(self, node:NewNode, scope:Scope):
        try:
            node_type = self.context.get_type(node.type)
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
            node_type = ErrorType()
        node.static_type = node_type

    @when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope:Scope):
        self.visit(node.expression, scope)
        node.static_type = self.type_bool

    @when(NotNode)
    def visit(self, node:NotNode, scope:Scope):
        self.visit(node.expression, scope)
        if not node.expression.static_type == self.type_bool:
            self.errors.append(SemanticError(node.line, node.column, f'Invalid boolean complement over type {node.expression.static_type}.'))
        node.static_type = self.type_bool

    @when(ComplementNode)
    def visit(self, node:ComplementNode, scope:Scope):
        self.visit(node.expression, scope)
        if not node.expression.static_type == self.type_int:
            self.errors.append(SemanticError(node.line, node.column, f'Invalid integer complement over type {node.expression.static_type}.'))
        node.static_type = self.type_int

    @when(ArithmeticNode)
    def visit(self, node:ArithmeticNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        if not(node.left.static_type == self.type_int and node.left.static_type == self.type_int):
            self.errors.append(SemanticError(node.line, node.column, f'Invalid arithmetic operation between types {node.left.static_type.name} and {node.right.static_type.name}.'))
        node.static_type = self.type_int

    @when(EqualNode)
    def visit(self, node:EqualNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        if self.is_basic(node.left.static_type) or self.is_basic(node.right.static_type):
            if not node.left.static_type == node.right.static_type:
                self.errors.append(SemanticError(node.line, node.column, f'Invalid comparison between types {node.left.static_type.name} and {node.right.static_type.name}.'))
        node.static_type = self.type_bool

    @when(LessEqualNode)
    @when(LessNode)
    def visit(self, node:LessNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        if not(node.left.static_type == self.type_int and node.left.static_type == self.type_int):
            self.errors.append(SemanticError(node.line, node.column, f'Invalid comparison between types {node.left.static_type.name} and {node.right.static_type.name}.'))
        node.static_type = self.type_bool
        
    @when(IdNode)
    def visit(self, node:IdNode, scope:Scope):
        try:
            node_type = scope.get_var(node.token).type
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
            node_type = ErrorType()
        node.static_type = node_type

    @when(BoolNode)
    def visit(self, node:BoolNode, scope:Scope):
        node.static_type = self.type_bool

    @when(IntegerNode)
    def visit(self, node:IntegerNode, scope:Scope):
        node.static_type = self.type_int

    @when(StringNode)
    def visit(self, node:StringNode, scope:Scope):
        node.static_type = self.type_str
