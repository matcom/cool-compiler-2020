from engine.cp import visitor, ErrorType, SelfType, SemanticError, Scope
from engine.parser import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode
from engine.parser import IfThenElseNode, WhileLoopNode, BlockNode, LetInNode, CaseOfNode
from engine.parser import AssignNode, UnaryNode, BinaryNode, LessEqualNode, LessNode, EqualNode, ArithmeticNode
from engine.parser import NotNode, IsVoidNode, ComplementNode, FunctionCallNode, MemberCallNode, NewNode, AtomicNode
from engine.parser import IntegerNode, IdNode, StringNode, BoolNode
from engine.semantic_errors import NON_TYPE_ARGUMENTS, ERROR_ON_LN_COL, WRONG_SIGNATURE, SELF_IS_READONLY, LOCAL_ALREADY_DEFINED, INCOMPATIBLE_TYPES, VARIABLE_NOT_DEFINED, INVALID_OPERATION, CYCLIC_HERITAGE


class Checker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

        # Tipos Built-in
        self.object_type = self.context.get_type('Object')
        self.io_type = self.context.get_type('IO')
        self.int_type = self.context.get_type('Int')
        self.string_type = self.context.get_type('String')
        self.bool_type = self.context.get_type('Bool')

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for d in node.declarations:
            self.visit(d, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id.lex)

        attrs = []
        self.current_type.parent = (
            self.current_type.parent
            if self.current_type.parent
            else self.context.get_type('Object'))
        parent = self.current_type.parent
        self.context.inheritance[self.current_type.name] = parent.name

        while parent:

            if parent == self.current_type:
                self.errors.append(ERROR_ON_LN_COL % (
                    node.line, node.column) + "SemanticError: " + CYCLIC_HERITAGE % (parent.name))
                self.current_type.parent = self.object_type
                break
            attrs += parent.attributes
            parent = parent.parent

        for a in self.current_type.attributes + attrs:
            if a.name == 'self':
                line, column = [(attrib.line, attrib.column) for attrib in node.features if type(
                    attrib) is AttrDeclarationNode and attrib.id.lex == 'self'][0]
                self.errors.append(ERROR_ON_LN_COL % (
                    line, column) + "SemanticError: " + "Incorrect use of self in attribute declaration")

            scope.define_variable(a.name, a.type)

        for f in node.features:
            self.visit(f, scope.create_child())

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        expr = node.expression
        if expr:
            scope_child: Scope = scope.create_child()
            scope_child.define_variable('self', self.current_type)
            self.visit(expr, scope_child)
            expr_type = expr.static_type

            attr = self.current_type.get_attribute(node.id.lex)
            node_type = attr.type
            node_type = self.current_type if isinstance(
                node_type, SelfType) else node_type
            if not expr_type.conforms_to(node_type):
                self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                                   "TypeError: " + INCOMPATIBLE_TYPES % (expr_type.name, node_type.name))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id.lex)

        # check ilegal redefined func
        parent = self.current_type.parent
        if parent:
            try:
                parent_method = parent.get_method(node.id.lex)
            except SemanticError:
                pass
            else:
                if parent_method.param_types != self.current_method.param_types or parent_method.return_type != self.current_method.return_type:
                    self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "SemanticError: " +
                                       WRONG_SIGNATURE % (self.current_method.name, self.current_type.name, parent.name))

        scope.define_variable('self', self.current_type)

        for pname, ptype in zip(self.current_method.param_names, self.current_method.param_types):
            if pname == 'self':
                self.errors.append(ERROR_ON_LN_COL % (
                    node.line, node.column) + "SemanticError: " + "Wrong use of self as method parameter")

            try:
                scope.define_variable(pname, ptype)
            except SemanticError:
                self.errors.append(ERROR_ON_LN_COL % (
                    node.line, node.column) + "SemanticError: " + f"Parameter {pname} can only be used once")

        body = node.body
        self.visit(body, scope.create_child())

        body_type = body.static_type
        return_type = self.current_type if isinstance(
            self.current_method.return_type, SelfType) else self.current_method.return_type

        if not body_type.conforms_to(return_type):
            self.errors.append(ERROR_ON_LN_COL % (body.line, body.column) +
                               "TypeError: " + INCOMPATIBLE_TYPES % (body_type.name, return_type.name))

    @visitor.when(IfThenElseNode)
    def visit(self, node, scope):
        condition = node.condition
        self.visit(condition, scope.create_child())

        condition_type = condition.static_type
        if not condition_type.conforms_to(self.bool_type):
            self.errors.append(ERROR_ON_LN_COL % (condition.line, condition.column) +
                               "TypeError: " + INCOMPATIBLE_TYPES % (condition_type.name, self.bool_type.name))

        self.visit(node.if_body, scope.create_child())
        self.visit(node.else_body, scope.create_child())

        if_type = node.if_body.static_type
        else_type = node.else_body.static_type
        node.static_type = if_type.type_union(else_type)

    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        condition = node.condition
        self.visit(condition, scope.create_child())

        condition_type = condition.static_type
        if not condition_type.conforms_to(self.bool_type):
            self.errors.append(ERROR_ON_LN_COL % (condition.line, condition.column) +
                               "TypeError: " + INCOMPATIBLE_TYPES % (condition_type.name, self.bool_type.name))

        self.visit(node.body, scope.create_child())

        node.static_type = self.object_type

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.expressions:
            self.visit(expr, scope.create_child())

        node.static_type = node.expressions[-1].static_type

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        for idx, typex, expr in node.let_body:
            try:
                node_type = self.context.get_type(typex.lex)
            except SemanticError as ex:
                self.errors.append(ERROR_ON_LN_COL % (
                    typex.line, typex.column) + "TypeError: " + ex.text)
                node_type = ErrorType()

            id_type = self.current_type if isinstance(
                node_type, SelfType) else node_type

            if idx.lex == 'self':
                self.errors.append(ERROR_ON_LN_COL % (expr.line, expr.column) +
                                   "SemanticError: " + "'self' cannot be bound in a 'let' expression.")

            child = scope.create_child()

            if expr:
                self.visit(expr, child)
                expr_type = expr.static_type
                if not expr_type.conforms_to(id_type):
                    self.errors.append(ERROR_ON_LN_COL % (
                        expr.line, expr.column) + "TypeError: " + INCOMPATIBLE_TYPES % (expr_type.name, id_type.name))

            try:
                scope.define_variable(idx.lex, id_type, True)
            except SemanticError as e:
                self.errors.append(ERROR_ON_LN_COL % (
                    idx.line, idx.column) + "SemanticError: " + e.text)

        self.visit(node.in_body, scope.create_child())

        node.static_type = node.in_body.static_type

    @visitor.when(CaseOfNode)
    def visit(self, node, scope):
        self.visit(node.expression, scope.create_child())

        node.static_type = None

        case_types = []

        for idx, typex, expr in node.branches:
            try:
                node_type = self.context.get_type(typex.lex)
                if node_type in case_types:
                    self.errors.append(ERROR_ON_LN_COL % (
                        typex.line, typex.column) + "SemanticError: " + f"Duplicate Branch {node_type} in case declaration")
                else:
                    case_types.append(node_type)
            except SemanticError as ex:
                self.errors.append(ERROR_ON_LN_COL % (
                    typex.line, typex.column) + "TypeError: " + ex.text)
                node_type = ErrorType()
            else:
                if isinstance(node_type, SelfType):
                    self.errors.append(ERROR_ON_LN_COL % (
                        typex.line, typex.column) + "SemanticError: " + f'Type "{node_type.name}" can not be used as case type')
                    node_type = ErrorType()

            id_type = node_type

            child_scope = scope.create_child()
            child_scope.define_variable(idx.lex, id_type)
            self.visit(expr, child_scope)
            expr_type = expr.static_type

            node.static_type = node.static_type.type_union(
                expr_type) if node.static_type else expr_type

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        expression = node.expression
        node_type = ErrorType()

        if scope.is_defined(node.id.lex):
            var = scope.find_variable(node.id.lex)
            node_type = var.type

            if var.name == 'self':
                self.errors.append(ERROR_ON_LN_COL % (
                    node.line, node.column) + "SemanticError: " + SELF_IS_READONLY)
        else:
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "NameError: " +
                               VARIABLE_NOT_DEFINED % (node.id.lex, self.current_method.name))

        self.visit(expression, scope.create_child())
        expr_type = expression.static_type

        if not expr_type.conforms_to(node_type):
            self.errors.append(ERROR_ON_LN_COL % (expression.line, expression.column) +
                               "TypeError: " + INCOMPATIBLE_TYPES % (expr_type.name, node_type.name))

        node.static_type = expr_type

    @visitor.when(NotNode)
    def visit(self, node, scope):
        expression = node.expression
        self.visit(expression, scope.create_child())

        expr_type = expression.static_type
        if not expr_type.conforms_to(self.bool_type):
            self.errors.append(ERROR_ON_LN_COL % (expression.line, expression.column) +
                               "TypeError: " + INCOMPATIBLE_TYPES % (expr_type.name, self.bool_type.name))

        node.static_type = self.bool_type

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        self.visit(node.left, scope.create_child())
        left_type = node.left.static_type

        self.visit(node.right, scope.create_child())
        right_type = node.right.static_type

        if not left_type.conforms_to(self.int_type) or not right_type.conforms_to(self.int_type):
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                               "TypeError: " + INVALID_OPERATION % (right_type.name, self.int_type.name))

        node.static_type = self.bool_type

    @visitor.when(LessNode)
    def visit(self, node, scope):
        self.visit(node.left, scope.create_child())
        left_type = node.left.static_type

        self.visit(node.right, scope.create_child())
        right_type = node.right.static_type

        if not left_type.conforms_to(self.int_type) or not right_type.conforms_to(self.int_type):
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                               "TypeError: " + INVALID_OPERATION % (right_type.name, self.int_type.name))

        node.static_type = self.bool_type

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        self.visit(node.left, scope.create_child())
        left_type = node.left.static_type

        self.visit(node.right, scope.create_child())
        right_type = node.right.static_type

        if left_type.conforms_to(self.int_type) ^ right_type.conforms_to(self.int_type):
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                               "TypeError: " + INVALID_OPERATION % (left_type.name, right_type.name))
        elif left_type.conforms_to(self.string_type) ^ right_type.conforms_to(self.string_type):
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                               "TypeError: " + INVALID_OPERATION % (left_type.name, right_type.name))
        elif left_type.conforms_to(self.bool_type) ^ right_type.conforms_to(self.bool_type):
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                               "TypeError: " + INVALID_OPERATION % (left_type.name, right_type.name))

        node.static_type = self.bool_type

    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        self.visit(node.left, scope.create_child())
        left_type = node.left.static_type

        self.visit(node.right, scope.create_child())
        right_type = node.right.static_type

        if not left_type.conforms_to(self.int_type) or not right_type.conforms_to(self.int_type):
            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                               "TypeError: " + INVALID_OPERATION % (left_type.name, right_type.name))

        node.static_type = self.int_type

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expression, scope.create_child())

        node.static_type = self.bool_type

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        expression = node.expression
        self.visit(expression, scope.create_child())

        expr_type = expression.static_type
        if not expr_type.conforms_to(self.int_type):
            self.errors.append(ERROR_ON_LN_COL % (expression.line, expression.column) +
                               "TypeError: " + INCOMPATIBLE_TYPES % (expr_type.name, self.int_type.name))

        node.static_type = self.int_type

    @visitor.when(FunctionCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope.create_child())
        obj_type = node.obj.static_type

        try:
            if node.type:
                try:
                    node_type = self.context.get_type(node.type.lex)
                except SemanticError as ex:
                    self.errors.append(ERROR_ON_LN_COL % (
                        node.type.line, node.type.column) + "TypeError: " + ex.text)
                    node_type = ErrorType()
                    return
                else:
                    if isinstance(node_type, SelfType):
                        self.errors.append(ERROR_ON_LN_COL % (node.type.line, node.type.column) +
                                           "SemanticError: " + f'Type "{node_type}" cannot be used as type dispatch')
                        node_type = ErrorType()

                if not obj_type.conforms_to(node_type):
                    self.errors.append(ERROR_ON_LN_COL % (node.obj.line, node.obj.column) +
                                       "TypeError: " + INCOMPATIBLE_TYPES % (obj_type.name, node_type.name))

                obj_type = node_type

            obj_method = obj_type.get_method(node.id.lex)

            node_type = obj_type if isinstance(
                obj_method.return_type, SelfType) else obj_method.return_type
        except SemanticError as ex:
            self.errors.append(ERROR_ON_LN_COL % (
                node.line, node.column) + "AttributeError: " + ex.text)
            node_type = ErrorType()
            obj_method = None

        else:
            if obj_method and len(node.args) == len(obj_method.param_types):
                for arg, param_type in zip(node.args, obj_method.param_types):
                    self.visit(arg, scope.create_child())
                    arg_type = arg.static_type

                    if not arg_type.conforms_to(param_type):
                        self.errors.append(ERROR_ON_LN_COL % (
                            arg.line, arg.column) + "TypeError: " + INCOMPATIBLE_TYPES % (arg_type.name, param_type.name))
            else:
                self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                                   "SemanticError: " + f'Method "{node.id.lex}" can not be dispatched')

        node.static_type = node_type

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        obj_type = self.current_type

        try:
            obj_method = obj_type.get_method(node.id.lex)

            node_type = obj_type if isinstance(
                obj_method.return_type, SelfType) else obj_method.return_type
        except SemanticError as ex:
            self.errors.append(ERROR_ON_LN_COL % (
                node.line, node.column) + "AttributeError: " + ex.text)
            node_type = ErrorType()
            obj_method = None

        else:
            if obj_method and len(node.args) == len(obj_method.param_types):
                for arg, param_type in zip(node.args, obj_method.param_types):
                    self.visit(arg, scope.create_child())
                    arg_type = arg.static_type

                    if not arg_type.conforms_to(param_type):
                        self.errors.append(ERROR_ON_LN_COL % (
                            arg.line, arg.column) + "TypeError: " + INCOMPATIBLE_TYPES % (arg_type.name, param_type.name))
            else:
                self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) +
                                   "SemanticError: " + f'Method "{node.id.lex}" can not be dispatched')

        node.static_type = node_type

    @visitor.when(NewNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type.lex)
        except SemanticError as ex:
            self.errors.append(ERROR_ON_LN_COL % (
                node.line, node.column) + "TypeError: " + ex.text)
            node_type = ErrorType()

        node.static_type = node_type

    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        node.static_type = self.int_type

    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.static_type = self.string_type

    @visitor.when(IdNode)
    def visit(self, node, scope):
        if scope.is_defined(node.token.lex):
            var = scope.find_variable(node.token.lex)
            node_type = var.type
        else:

            self.errors.append(ERROR_ON_LN_COL % (node.line, node.column) + "NameError: " +
                               VARIABLE_NOT_DEFINED % (node.token.lex, self.current_method.name if self.current_method else ''))
            node_type = ErrorType()

        node.static_type = node_type

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        node.static_type = self.bool_type
