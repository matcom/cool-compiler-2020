from .semantic_utils import Context, SemanticException, Type, ErrorType, VoidType, Var, Scope, find_common_ancestor
from ..utils import on, when
from ..errors import SemanticError
from ..ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode, IdNode,\
                    IfThenElseNode, WhileLoopNode, BlockNode, LetInNode, ArithmeticNode, BoolNode,    \
                    CaseOfNode, LetNode, CaseNode, AssignNode, FunctionCallNode, NewNode, IntegerNode,\
                    MemberCallNode, LessEqualNode, LessNode, EqualNode, ComplementNode, StringNode,   \
                    IsVoidNode, NotNode

class COOL_TYPE_CHECKER(object):
    def __init__(self, context: Context, errors=[]):
        self.current_type: Type = None
        self.context: Context = context
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
    def visit(self, node:ProgramNode, scope:Scope=None):
        scope = Scope()
        for classx_node in node.classes:
            self.visit(classx_node, scope)
        

    @when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self.context.get_type(node.id)

        attrs = []
        actual = self.current_type
        while actual:
            attrs += actual.attributes
            actual = actual.parent

        class_scope = Scope(parent=scope)
        for attr in attrs:
            class_scope.define_var(attr.name, attr.type)

        for feature_node in node.features:
            self.visit(feature_node, scope if feature_node is AttrDeclarationNode else class_scope) #Ensures an attribute cannot be defined from another one           

    @when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        if node.expression:
            self.visit(node.expression, scope)

            attr_type = self.context.get_type(node.type)

            if not node.expression.static_type.is_subtype(attr_type):
                self.errors.append(SemanticError(node.line, node.column, f'Invalid attribute initialization. Type {node.expression.static_type.name} is not subtype of {attr_type.name}.'))

    @when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, scope:Scope):
        func_scope = Scope(parent=scope)
        func_scope.define_var('self', self.current_type)

        for param in node.params:
            try:
                func_scope.define_var(param.id, self.context.get_type(param.type))
            except SemanticException: # Check if params names are differnt
                self.errors.append(SemanticError(node.line, node.column, f'Identifier "{param.name}" can only be used once.'))

        self.visit(node.expression, func_scope)

        ret_type = self.context.get_type(node.type)
        if not node.expression.static_type.is_subtype(ret_type):
            self.errors.append(SemanticError(node.line, node.column, f'Invalid return type. Type {node.expression.static_type.name} is not subtype of {ret_type.name}.'))


    @when(IfThenElseNode)
    def visit(self, node:IfThenElseNode, scope:Scope):
        self.visit(node.condition, scope)
        if not node.condition.static_type == self.type_bool:
            self.errors.append(SemanticError(node.line, node.column, f'Invalid predicate type. Found {node.condition.static_type.name} instead of {self.type_bool.name}.'))

        self.visit(node.if_body, Scope(parent=scope))
        self.visit(node.else_body, Scope(parent=scope))

        node.static_type = find_common_ancestor(node.if_body.static_type, node.else_body.static_type)

    @when(WhileLoopNode)
    def visit(self, node:WhileLoopNode, scope:Scope):
        self.visit(node.condition, scope)
        if not node.condition.static_type == self.type_bool:
            self.errors.append(SemanticError(node.line, node.column, f'Invalid predicate type. Found {node.condition.static_type.name} instead of {self.type_bool.name}.'))

        self.visit(node.body, Scope(parent=scope))
        node.static_type = self.type_obj

    @when(BlockNode)
    def visit(self, node:BlockNode, scope:Scope):
        block_scope = Scope(parent=scope)
        for expr in node.expressions:
            self.visit(expr, block_scope)

        node.static_type = node.expressions[-1].static_type

    @when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        node_type = ErrorType()
        try:
            node_type = self.context.get_type(node.type)
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))         

        if node.expression:
            self.visit(node.expression, scope)
            if not node.expression.static_type == node_type:
                self.errors.append(SemanticError(node.line, node.column, f'Invalid initialization. Type {node.expression.static_type.name} is not subtype of {node_type}.'))
        try:
            scope.define_var(node.id, node_type)
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
        node.static_type = node_type
        
    @when(LetInNode)
    def visit(self, node:LetInNode, scope:Scope):
        letin_scope = Scope(parent=scope)
        for letnode in node.let_body:
            self.visit(letnode, letin_scope)# The defined variable is added to the scope, thus usable
                                            # in the next assignation. To avoid this change the definition
                                            # in the visit method for LetNode.
        
        self.visit(node.in_body, letin_scope)
        node.static_type = node.in_body.static_type

    @when(CaseNode)
    def visit(self, node:CaseNode, scope:Scope):
        case_scope = Scope(parent=scope)
        node_type = ErrorType()
        try:
            node_type = self.context.get_type(node.type)
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.columns, e.text))

        case_scope.define_var(node.id, node_type)
        self.visit(node.expression, case_scope)

        node.static_type = node.expression.static_type

    @when(CaseOfNode)
    def visit(self, node:CaseOfNode, scope:Scope):
        self.visit(node.expression, scope)

        node_type = None
        for case in node.cases:
            self.visit(case, scope)
            if node_type:
                node_type = find_common_ancestor(node_type, case.static_type)
            else:
                node_type = case.static_type

        node.static_type = node_type

    @when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        var_type = ErrorType()
        try:
            var = scope.get_var(node.id)
            var_type = var.type
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))

        self.visit(node.expression, scope)
        if not node.expression.static_type.is_subtype(var_type):
            self.errors.append(SemanticError(node.line, node.column, f'Invalid assignment. Type {node.expression.static_type.name} is not subtype of {var_type.name}.'))
    
    @when(FunctionCallNode)
    @when(MemberCallNode)
    def visit(self, node:FunctionCallNode, scope:Scope):
        obj_type = self.current_type

        if node is FunctionCallNode:
            self.visit(node.obj, scope)
            if node.type:
                cast_type = ErrorType()
                try:
                    cast_type = self.context.get_type(node.type)
                except SemanticException as e:
                    self.errors.append(SemanticError(node.line, node.column, e.text))
                if cast_type is ErrorType:
                    return
                elif not node.obj.static_type.is_subtype(cast_type):
                    self.errors.append(SemanticError(node.line, node.column, f'Invalid cast. Type {node.obj.static_type.name} is not subtype of {cast_type.name}.'))
                obj_type = cast_type
            else:
                obj_type = node.obj.static_type

        node_type = ErrorType()
        try:
            method = obj_type.get_method(node.id)
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
        else:
            if len(node.args) != len(method.names):
                self.errors.append(SemanticError(node.line, node.column, f'Invalid dispatch. Expected {len(method.names)} parameter(s), found {len(node.args)}.'))
            else:
                node_type = method.return_type
                for pname, ptype, expr in zip(method.param_names, method.param_types, node.args):
                    self.visit(expr, scope)
                    expected_type = ptype
                    if not expr.static_type.is_subtype(expected_type):
                        self.errors.append(SemanticError(node.line, node.column, f'Invalid dispatch. Parameter "{pname}" type {expr.static_type.name} is not subtype of {expected_type.name}.'))    

        node.static_type = node_type

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
