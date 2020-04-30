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
                def_func_visitor(feature, self.CurrentClass, {})


class DefAttrVisitor(Visitor):
    def __init__(self, current_class):
        super().__init__(current_class)

    def visit(self, node: DefAttrNode):
        if node.expr:
            expr_type = expression_visitor(node.expr, self.CurrentClass, {})
            attr_type = self.CurrentClass.attributes[node.id].attrType
            if not check_inherits(expr_type, attr_type):
                add_semantic_error(0, 0, f'Invalid type {expr_type}')
            else:
                return attr_type


def def_func_visitor(function: DefFuncNode, current_class: CoolType, local_scope: dict):
    local_scope = local_scope.copy()
    for arg in function.params:
        local_scope[arg[0]] = type_by_name(arg[1])
    body_type = expression_visitor(function.expressions, current_class, local_scope)
    return_type = type_by_name(function.return_type)
    if check_inherits(body_type, return_type):
        return return_type
    elif body_type is not None:
        add_semantic_error(0, 0, f'invalid returned type {body_type}')


def int_visitor(expr, current_class, local_scope):
    return IntType


def string_visitor(expr, current_class, local_scope):
    return StringType


def bool_visitor(expr, current_class, local_scope):
    return BoolType


def var_visitor(var: VarNode, current_class: CoolType, local_scope: dict):
    if var.id in local_scope.keys():
        return local_scope[var.id]
    attribute, _ = get_attribute(current_class, var.id)
    if attribute is not None:
        return attribute.attrType
    else:
        raise Exception(f'unknown variable {var.id}')


def arithmetic_operator_visitor(operator: BinaryNode, current_class: CoolType, local_scope: dict):
    lvalue_type = expression_visitor(operator.lvalue, current_class, local_scope)
    if lvalue_type != IntType:
        raise Exception(f'invalid left value type {lvalue_type}, must be a {IntType}')
    rvalue_type = expression_visitor(operator.rvalue, current_class, local_scope)
    if rvalue_type != IntType:
        raise Exception(f'invalid left value type {rvalue_type}, must be a {IntType}')
    return IntType


def equal_visitor(equal: EqNode, current_class: CoolType, local_scope: dict):
    lvalue_type = expression_visitor(equal.lvalue, current_class, local_scope)
    rvalue_type = expression_visitor(equal.rvalue, current_class, local_scope)
    static_types = [IntType, BoolType, StringType]
    if (lvalue_type in static_types or rvalue_type in static_types) and lvalue_type != rvalue_type:
        raise Exception(f'impossible compare {lvalue_type} and {rvalue_type} types')
    return BoolType


def comparison_visitor(cmp: BinaryNode, current_class: CoolType, local_scope: dict):
    lvalue_type = expression_visitor(cmp.lvalue, current_class, local_scope)
    if lvalue_type != IntType:
        raise Exception(f'lvalue type must be a {IntType}')
    rvalue_type = expression_visitor(cmp.rvalue, current_class, local_scope)
    if rvalue_type != IntType:
        raise Exception(f'rvalue type must be a {IntType}')
    return BoolType


def assignment_visitor(assign: AssignNode, current_class: CoolType, local_scope: dict):
    try:
        id_type = local_scope[assign.id]
    except KeyError:
        attr, _ = get_attribute(current_class, assign.id)
        if attr is None:
            raise Exception(f'unknown variable {assign.id}')
        else:
            id_type = attr.attrType
    expr_type = expression_visitor(assign.expr, current_class, local_scope)
    if check_inherits(expr_type, id_type):
        return expr_type
    raise Exception(f'Type {expr_type} cannot be stored in type {id_type}')


def def_attribute_visitor(def_attr: DefAttrNode, current_class: CoolType, local_scope: dict):
    id_type = type_by_name(def_attr.type)
    if id_type is None:
        raise Exception(f'unknown type {def_attr.type}')
    if def_attr.expr:
        expr_type = expression_visitor(def_attr.expr, current_class, local_scope)
        if not check_inherits(expr_type, id_type):
            raise Exception(f'Type {expr_type} cannot be stored in type {id_type}')
    return id_type


def let_visitor(let: LetNode, current_class: CoolType, local_scope: dict):
    local_scope = local_scope.copy()
    for attribute in let.let_attrs:
        attribute_type = expression_visitor(attribute, current_class, local_scope)
        local_scope[attribute.id] = attribute_type
    return expression_visitor(let.expr, current_class, local_scope)


def list_expr_visitor(expressions: list, current_class: CoolType, local_scope: dict):
    final_type = None
    for expr in expressions:
        final_type = expression_visitor(expr, current_class, local_scope)
    return final_type


def if_visitor(if_struct: IfNode, current_class: CoolType, local_scope: dict):
    predicate_type = expression_visitor(if_struct.if_expr, current_class, local_scope)
    if predicate_type != BoolType:
        raise Exception(f'\"if\" condition must be a {BoolType}')
    then_type = expression_visitor(if_struct.then_expr, current_class, local_scope)
    else_type = expression_visitor(if_struct.else_expr, current_class, local_scope)
    return pronounced_join(then_type, else_type)


def func_call_visitor(func_call: FuncCallNode, current_class: CoolType, local_scope: dict):
    args_types = []
    method = None
    msg = None
    for arg in func_call.args:
        arg_type = expression_visitor(arg, current_class, local_scope)
        args_types.append(arg_type)
    if func_call.object:
        if func_call.type:
            specific_type = type_by_name(func_call.type)
            if specific_type is None:
                raise Exception(f'unknown type {func_call.type}')
            if check_inherits(current_class, specific_type):
                method, msg = specific_type.get_method_without_hierarchy(func_call.id, args_types)
            else:
                raise Exception(f'type {current_class} not inherits from {specific_type}')
        else:
            object_type = expression_visitor(func_call.object, current_class, local_scope)
            method, msg = object_type.get_method(func_call.id, args_types)
    else:
        method, msg = current_class.get_method(func_call.id, args_types)
    if method is None:
        raise Exception(msg)
    if method.returnedType == SelfType:
        return current_class
    return method.returnedType


__visitors__ = {
    list: list_expr_visitor,
    IntNode: int_visitor,
    StringNode: string_visitor,
    BoolNode: bool_visitor,
    VarNode: var_visitor,
    PlusNode: arithmetic_operator_visitor,
    MinusNode: arithmetic_operator_visitor,
    StarNode: arithmetic_operator_visitor,
    DivNode: arithmetic_operator_visitor,
    EqNode: equal_visitor,
    LessThanNode: comparison_visitor,
    LessEqNode: comparison_visitor,
    AssignNode: assignment_visitor,
    DefAttrNode: def_attribute_visitor,
    LetNode: let_visitor,
    IfNode: if_visitor,
    FuncCallNode: func_call_visitor
}


def expression_visitor(expression, current_class: CoolType, local_scope: dict) -> CoolType:
    try:
        return __visitors__[type(expression)](expression, current_class, local_scope)
    except KeyError:
        print(f'Not visitor for {expression}')


def semantic_check(node):
    if type(node) is ProgramNode:
        node.accept(ProgramVisitor())
