from errors import add_semantic_error
from lexer_parser.ast import *
from .types import *


class Visitor:
    def __init__(self, current_class, local_scope=None):
        self.CurrentClass = current_class
        self.LocalScope = local_scope if local_scope else {}

    def visit(self, node):
        pass


class ProgramVisitor(Visitor):
    def __init__(self):
        super().__init__(None)

    def visit(self, node: ProgramNode):
        if not (check_type_declaration(node) and check_type_hierarchy(node)):
            return
        # Check Main class exists
        try:
            TypesByName['Main']
        except KeyError:
            add_semantic_error(0, 0, f'Main class undeclared')
            return
        # Initialize MethodEnv
        for c in node.classes:
            classType = TypesByName[c.type]
            for f in c.feature_nodes:
                if type(f) is DefFuncNode:
                    param_types = [param[1] for param in f.params]
                    result, msg = classType.add_method(f.id, param_types, f.return_type)
                    if not result:
                        add_semantic_error(0, 0, msg)
                elif type(f) is DefAttrNode:
                    # Add all attributes to types
                    result, msg = classType.add_attr(f.id, f.type)
                    if not result:
                        add_semantic_error(0, 0, msg)
        # Visit each class inside
        for c in node.classes:
            c.accept(DefClassVisitor())


class DefClassVisitor(Visitor):
    def __init__(self):
        super().__init__(None)

    def visit(self, node: DefClassNode):
        self.CurrentClass = TypesByName[node.type]
        # Check all features
        for feature in node.feature_nodes:
            if type(feature) is DefAttrNode:
                feature.accept(DefAttrVisitor(self.CurrentClass))
            if type(feature) is DefFuncNode:
                feature.accept(DefFuncVisitor(self.CurrentClass))


class DefAttrVisitor(Visitor):
    def __init__(self, current_class):
        super().__init__(current_class)

    def visit(self, node: DefAttrNode):
        if node.expr:
            expr_type = node.expr.accept(DefExpressionVisitor(self.CurrentClass))
            attr_type = self.CurrentClass.attributes[node.id].attrType
            if not check_inherits(expr_type, attr_type):
                add_semantic_error(0, 0, f'Invalid type {expr_type}')
            else:
                return attr_type


class DefFuncVisitor(Visitor):
    def __init__(self, current_class):
        super().__init__(current_class)

    def visit(self, node: DefFuncNode):
        local_scope = self.LocalScope.copy()
        for arg in node.params:
            local_scope[arg[0]] = type_by_name(arg[1])
        if type(node.expressions) is list:
            for exp in node.expressions:
                body_type = exp.accept(DefExpressionVisitor(self.CurrentClass, local_scope))
                if body_type is None:
                    break
        else:
            body_type = node.expressions.accept(DefExpressionVisitor(self.CurrentClass, local_scope))
        return_type = type_by_name(node.return_type)
        if check_inherits(body_type, return_type):
            return return_type
        elif body_type is not None:
            add_semantic_error(0, 0, f'invalid returned type {body_type}')


class DefExpressionVisitor(Visitor):
    def __init__(self, current_class, local_scope=None):
        super().__init__(current_class, local_scope)

    def visit(self, node):
        if type(node) is IntNode:
            return IntType
        if type(node) is StringNode:
            return StringType
        if type(node) in [BoolNode, EqNode]:
            return BoolType
        if type(node) is VarNode:
            if node.id in self.LocalScope.keys():
                return self.LocalScope[node.id]
            try:
                return self.CurrentClass.attributes[node.id].attrType
            except KeyError:
                add_semantic_error(0, 0, f'invalid variable {node.id}')
                return None
        if type(node) in [StarNode, PlusNode, DivNode, MinusNode]:
            lvalue_type = node.lvalue.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
            if lvalue_type != IntType and lvalue_type is not None:
                add_semantic_error(0, 0, f'invalid left value type')
                return None
            rvalue_type = node.rvalue.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
            if rvalue_type != IntType and rvalue_type is not None:
                add_semantic_error(0, 0, f'invalid right value type')
                return None
            return IntType
        if type(node) is AssignNode:
            try:
                varType = self.CurrentClass.attributes[node.id].attrType
            except KeyError:
                add_semantic_error(0, 0, f'invalid variable {node.id}')
                return None
            expressionType = node.accept(DefExpressionVisitor(self.CurrentClass))
            if check_inherits(expressionType, varType):
                return varType
            else:
                return None
        if type(node) is DefAttrNode:
            attr_type = type_by_name(node.type)
            if attr_type is None:
                add_semantic_error(0, 0, f'unknown type {node.type}')
                return None
            if node.expr:
                expr_type = node.expr.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
                if check_inherits(expr_type, attr_type):
                    return attr_type
                else:
                    add_semantic_error(0, 0, f'type {expr_type.name} cannot be stored in an {attr_type.name}')
                    return None
            return attr_type
        if type(node) is LetNode:
            for attr in node.let_attrs:
                attr_type = attr.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
                if attr_type is None:
                    return None
                self.LocalScope[attr.id] = attr_type
            return None
        if type(node) is IfNode:
            if_expr_type = node.if_expr.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
            if if_expr_type != BoolType:
                add_semantic_error(0, 0, f'\"if\" expression must be a Bool type')
                return
            then_expr_type = node.then_expr.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
            else_expr_type = node.else_expr.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
            if then_expr_type is None or else_expr_type is None:
                return
            return pronounced_join(then_expr_type, else_expr_type)
        if type(node) is FuncCallNode:
            args_types = []
            for a in node.args:
                a_type = a.accept(DefExpressionVisitor(self.CurrentClass, self.LocalScope))
                if a_type:
                    args_types.append(a_type)
            if node.object:
                print('Not rule for FuncCall from var')
            else:
                method, msg = self.CurrentClass.get_method(node.id, args_types)
                if method.returnedType == SelfType:
                    return self.CurrentClass
                return method.returnedType
        print(f'Not rule for {type(node)} in DefExpressionVisitor')


def semantic_check(node):
    if type(node) is ProgramNode:
        node.accept(ProgramVisitor())
