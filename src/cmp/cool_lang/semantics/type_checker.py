from ..ast import (
    ArithmeticNode,
    AssignNode,
    AttrDeclarationNode,
    BlockNode,
    BoolNode,
    CaseNode,
    CaseOfNode,
    ClassDeclarationNode,
    ComplementNode,
    EqualNode,
    FuncDeclarationNode,
    FunctionCallNode,
    IdNode,
    IfThenElseNode,
    IntegerNode,
    IsVoidNode,
    LessEqualNode,
    LessNode,
    LetInNode,
    LetNode,
    MemberCallNode,
    NewNode,
    NotNode,
    ProgramNode,
    StringNode,
    WhileLoopNode,
)
from ..errors import CAttributeError, CNameError, CTypeError, SemanticError
from ..utils import on, when
from .semantic_utils import (
    Context,
    ErrorType,
    Scope,
    SemanticException,
    Type,
    find_common_ancestor,
)


class COOL_TYPE_CHECKER(object):
    def __init__(self, context: Context, errors=[]):
        self.current_type: Type = None  # type:ignore
        self.context: Context = context
        self.errors = errors

        self.type_int = self.context.get_type("Int")
        self.type_str = self.context.get_type("String")
        self.type_obj = self.context.get_type("Object")
        self.type_io = self.context.get_type("IO")
        self.type_bool = self.context.get_type("Bool")

    def is_basic(self, typex):
        return typex in [self.type_str, self.type_bool, self.type_int]

    @on("node")
    def visit(self, node, scope):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope = None):  # noqa:F811
        scope = Scope()
        for classx_node in node.classes:
            self.visit(classx_node, scope)

    @when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):  # noqa:F811
        self.current_type = self.context.get_type(node.id)

        attrs = []
        actual = self.current_type
        while actual:
            attrs += actual.attributes
            actual = actual.parent

        class_scope = Scope(parent=scope)
        for attr in attrs:
            if attr.name == "self":
                line, column = [
                    (attrib.line, attrib.column)
                    for attrib in node.features
                    if type(attrib) is AttrDeclarationNode and attrib.id == "self"
                ][0]
                self.errors.append(
                    SemanticError(
                        line,
                        column,
                        'Identifier "self" cannot be used in Attribute declarations.',
                    )
                )
                continue
            class_scope.define_var(attr.name, attr.type)

        for feature_node in node.features:
            self.visit(
                feature_node,
                scope if feature_node is AttrDeclarationNode else class_scope,
            )  # Ensures an attribute cannot be defined from another one

    @when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope):  # noqa:F811
        if node.expression:
            new_scope = Scope(parent=scope)
            new_scope.define_var("self", self.current_type)
            self.visit(node.expression, new_scope)

            attr_type = self.context.get_type(node.type)

            if not node.expression.static_type.is_subtype(attr_type):
                self.errors.append(
                    CTypeError(
                        node.line,
                        node.column,
                        "Invalid attribute initialization. "
                        + f"Type {node.expression.static_type.name} "
                        + f"is not subtype of {attr_type.name}.",
                    )
                )

    @when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):  # noqa:F811
        func_scope = Scope(parent=scope)
        func_scope.define_var("self", self.current_type)

        func = self.current_type.get_method(node.id)

        for param, param_type in zip(node.params, func.param_types):
            try:
                func_scope.define_var(param.id, param_type)
            except SemanticException:  # Check if params names are differnt
                self.errors.append(
                    SemanticError(
                        param.line,
                        param.column,
                        f'Identifier "{param.id}" can only be used once.',
                    )
                )

        self.visit(node.expression, func_scope)

        ret_type = func.return_type
        if not node.expression.static_type.is_subtype(ret_type):
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid return type. "
                    + f"Type {node.expression.static_type.name} "
                    + f"is not subtype of {ret_type.name}.",
                )
            )

    @when(IfThenElseNode)
    def visit(self, node: IfThenElseNode, scope: Scope):  # noqa:F811
        self.visit(node.condition, scope)
        if not node.condition.static_type == self.type_bool:
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid predicate type. "
                    + f"Found {node.condition.static_type.name} "
                    + f"instead of {self.type_bool.name}.",
                )
            )

        self.visit(node.if_body, Scope(parent=scope))
        self.visit(node.else_body, Scope(parent=scope))

        node.static_type = find_common_ancestor(
            node.if_body.static_type, node.else_body.static_type
        )

    @when(WhileLoopNode)
    def visit(self, node: WhileLoopNode, scope: Scope):  # noqa:F811
        self.visit(node.condition, scope)
        if not node.condition.static_type == self.type_bool:
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid predicate type. "
                    + f"Found {node.condition.static_type.name} "
                    + f"instead of {self.type_bool.name}.",
                )
            )

        self.visit(node.body, Scope(parent=scope))
        node.static_type = self.type_obj

    @when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):  # noqa:F811
        block_scope = Scope(parent=scope)
        for expr in node.expressions:
            self.visit(expr, block_scope)

        node.static_type = node.expressions[-1].static_type

    @when(LetNode)
    def visit(self, node: LetNode, scope: Scope):  # noqa:F811
        node_type = ErrorType()
        try:
            node_type = self.context.get_type(node.type)
        except SemanticException as e:
            self.errors.append(CTypeError(node.line, node.column, e.text))

        if node.expression:
            self.visit(node.expression, scope)
            if not node.expression.static_type.is_subtype(node_type):
                self.errors.append(
                    CTypeError(
                        node.line,
                        node.column,
                        "Invalid initialization. "
                        + f"Type {node.expression.static_type.name} "
                        + f"is not subtype of {node_type.name}.",
                    )
                )
        if node.id == "self":
            self.errors.append(
                SemanticError(node.line, node.column, 'Var "self" is read-only.')
            )
        try:
            scope.define_var(node.id, node_type)
        except SemanticException as e:
            self.errors.append(CNameError(node.line, node.column, e.text))
        node.static_type = node_type

    @when(LetInNode)
    def visit(self, node: LetInNode, scope: Scope):  # noqa:F811
        letin_scope = scope
        for letnode in node.let_body:
            letin_scope = Scope(parent=letin_scope)
            self.visit(letnode, letin_scope)

        self.visit(node.in_body, letin_scope)
        node.static_type = node.in_body.static_type

    @when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):  # noqa:F811
        case_scope = Scope(parent=scope)
        node_type = ErrorType()
        try:
            node_type = self.context.get_type(node.type)
        except SemanticException as e:
            self.errors.append(CTypeError(node.line, node.column, e.text))

        case_scope.define_var(node.id, node_type)
        self.visit(node.expression, case_scope)

        node.static_type = node.expression.static_type

    @when(CaseOfNode)
    def visit(self, node: CaseOfNode, scope: Scope):  # noqa:F811
        self.visit(node.expression, scope)

        node_type = None
        cases_types = set()
        for case in node.cases:
            self.visit(case, scope)
            try:
                case_type = self.context.get_type(case.type)
                if case_type in cases_types:
                    self.errors.append(
                        SemanticError(
                            case.line,
                            case.column,
                            f"Duplicate case for type {case_type.name}.",
                        )
                    )
                else:
                    cases_types.add(case_type)
            except SemanticException:
                pass

            if node_type:
                node_type = find_common_ancestor(node_type, case.static_type)
            else:
                node_type = case.static_type

        node.static_type = node_type

    @when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):  # noqa:F811
        var_type = ErrorType()
        try:
            var = scope.get_var(node.id)
            if node.id == "self":
                raise SemanticException('Var "self" is read-only.')
            var_type = var.type
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))

        self.visit(node.expression, scope)
        if not node.expression.static_type.is_subtype(var_type):
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid assignment. "
                    + f"Type {node.expression.static_type.name} "
                    + f"is not subtype of {var_type.name}.",
                )
            )

        node.static_type = node.expression.static_type

    @when(MemberCallNode)
    def visit(self, node: MemberCallNode, scope: Scope):  # noqa:F811
        obj_type = self.current_type

        node_type = ErrorType()
        try:
            method = obj_type.get_method(node.id)
        except SemanticException as e:
            self.errors.append(CAttributeError(node.line, node.column, e.text))
        else:
            if len(node.args) != len(method.param_names):
                self.errors.append(
                    SemanticError(
                        node.line,
                        node.column,
                        "Invalid dispatch. "
                        + f"Expected {len(method.names)} parameter(s), "
                        + f"found {len(node.args)}.",
                    )
                )
            else:
                node_type = method.return_type
                for pname, ptype, expr in zip(
                    method.param_names, method.param_types, node.args
                ):
                    self.visit(expr, scope)
                    expected_type = ptype
                    if not expr.static_type.is_subtype(expected_type):
                        self.errors.append(
                            CTypeError(
                                node.line,
                                node.column,
                                "Invalid dispatch. "
                                + f'Parameter "{pname}" type {expr.static_type.name} '
                                + f"is not subtype of {expected_type.name}.",
                            )
                        )

        node.static_type = node_type

    @when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):  # noqa:F811
        obj_type = None

        self.visit(node.obj, scope)
        if node.type:
            cast_type = ErrorType()
            try:
                cast_type = self.context.get_type(node.type)
            except SemanticException as e:
                self.errors.append(CTypeError(node.line, node.column, e.text))
                node.static_type = ErrorType()
                return
            if not node.obj.static_type.is_subtype(cast_type):
                self.errors.append(
                    CTypeError(
                        node.line,
                        node.column,
                        "Invalid cast. "
                        + f"Type {node.obj.static_type.name} "
                        + f"is not subtype of {cast_type.name}.",
                    )
                )
            obj_type = cast_type
        else:
            obj_type = node.obj.static_type

        node_type = ErrorType()
        try:
            method = obj_type.get_method(node.id)
        except SemanticException as e:
            self.errors.append(CAttributeError(node.line, node.column, e.text))
        else:
            if len(node.args) != len(method.param_names):
                self.errors.append(
                    SemanticError(
                        node.line,
                        node.column,
                        "Invalid dispatch. "
                        + f"Expected {len(method.param_names)} "
                        + f"parameter(s), found {len(node.args)}.",
                    )
                )
            else:
                node_type = method.return_type
                for pname, ptype, expr in zip(
                    method.param_names, method.param_types, node.args
                ):
                    self.visit(expr, scope)
                    expected_type = ptype
                    if not expr.static_type.is_subtype(expected_type):
                        self.errors.append(
                            CTypeError(
                                node.line,
                                node.column,
                                "Invalid dispatch. "
                                + f'Parameter "{pname}" type {expr.static_type.name} '
                                + f"is not subtype of {expected_type.name}.",
                            )
                        )

        node.static_type = node_type

    @when(NewNode)
    def visit(self, node: NewNode, scope: Scope):  # noqa:F811
        try:
            node_type = self.context.get_type(node.type)
        except SemanticException as e:
            self.errors.append(CTypeError(node.line, node.column, e.text))
            node_type = ErrorType()
        node.static_type = node_type

    @when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):  # noqa:F811
        self.visit(node.expression, scope)
        node.static_type = self.type_bool

    @when(NotNode)
    def visit(self, node: NotNode, scope: Scope):  # noqa:F811
        self.visit(node.expression, scope)
        if not node.expression.static_type == self.type_bool:
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid boolean complement over type "
                    + f"{node.expression.static_type.name}.",
                )
            )
        node.static_type = self.type_bool

    @when(ComplementNode)
    def visit(self, node: ComplementNode, scope: Scope):  # noqa:F811
        self.visit(node.expression, scope)
        if not node.expression.static_type == self.type_int:
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid integer complement over "
                    + f"type {node.expression.static_type.name}.",
                )
            )
        node.static_type = self.type_int

    @when(ArithmeticNode)
    def visit(self, node: ArithmeticNode, scope: Scope):  # noqa:F811
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        if not (
            node.left.static_type == self.type_int
            and node.right.static_type == self.type_int
        ):
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid arithmetic operation between "
                    + f"types {node.left.static_type.name} "
                    + f"and {node.right.static_type.name}.",
                )
            )
        node.static_type = self.type_int

    @when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):  # noqa:F811
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        if self.is_basic(node.left.static_type) or self.is_basic(
            node.right.static_type
        ):
            if not node.left.static_type == node.right.static_type:
                self.errors.append(
                    CTypeError(
                        node.line,
                        node.column,
                        "Invalid comparison between "
                        + f"types {node.left.static_type.name} "
                        + f"and {node.right.static_type.name}.",
                    )
                )
        node.static_type = self.type_bool

    @when(LessEqualNode)
    def visit(self, node: LessEqualNode, scope: Scope):  # noqa:F811
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        if not (
            node.left.static_type == self.type_int
            and node.right.static_type == self.type_int
        ):
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid comparison between "
                    + f"types {node.left.static_type.name} "
                    + f"and {node.right.static_type.name}.",
                )
            )
        node.static_type = self.type_bool

    @when(LessNode)
    def visit(self, node: LessNode, scope: Scope):  # noqa:F811
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        if not (
            node.left.static_type == self.type_int
            and node.right.static_type == self.type_int
        ):
            self.errors.append(
                CTypeError(
                    node.line,
                    node.column,
                    "Invalid comparison between "
                    + f"types {node.left.static_type.name} "
                    + f"and {node.right.static_type.name}.",
                )
            )
        node.static_type = self.type_bool

    @when(IdNode)
    def visit(self, node: IdNode, scope: Scope):  # noqa:F811
        try:
            node_type = scope.get_var(node.token).type
        except SemanticException as e:
            self.errors.append(CNameError(node.line, node.column, e.text))
            node_type = ErrorType()
        node.static_type = node_type

    @when(BoolNode)
    def visit(self, node: BoolNode, scope: Scope):  # noqa:F811
        node.static_type = self.type_bool

    @when(IntegerNode)
    def visit(self, node: IntegerNode, scope: Scope):  # noqa:F811
        node.static_type = self.type_int

    @when(StringNode)
    def visit(self, node: StringNode, scope: Scope):  # noqa:F811
        node.static_type = self.type_str
