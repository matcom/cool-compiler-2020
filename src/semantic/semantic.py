from .types import *


def program_visitor(program: ProgramNode):
    if not (check_type_declaration(program) and check_type_hierarchy(program)):
        return
    # Check Main class exists
    try:
        TypesByName['Main']
    except KeyError:
        add_semantic_error(0, 0, f'Main class undeclared')
        return
    # Initialize MethodEnv
    types_already_check = [ObjectType, IntType, StringNode, BoolType, IOType]
    classes = program.classes.copy()
    while len(classes) != 0:
        c: DefClassNode = classes.pop()
        if c.parent_type is not None:
            parent_type = TypesByName[c.parent_type]
            if parent_type not in types_already_check:
                classes = [c] + classes
                continue
        classType = TypesByName[c.type]
        for f in c.feature_nodes:
            if type(f) is DefFuncNode:
                param_types = [param[1] for param in f.params]
                result, msg = classType.add_method(f.id, param_types, f.return_type)
                if not result:
                    add_semantic_error(f.lineno, f.colno, msg)
            elif type(f) is DefAttrNode:
                # Add all attributes to types
                result, msg = classType.add_attr(f.id, f.type, f.expr)
                if not result:
                    add_semantic_error(f.lineno, f.colno, msg)
        types_already_check.append(classType)
    # Visit each class inside
    for c in program.classes:
        class_visitor(c, None, {})


def class_visitor(_class: DefClassNode, current_class: CoolType, local_scope: dict):
    current_class = TypesByName[_class.type]
    local_scope = local_scope.copy()
    local_scope['self'] = current_class
    # Check all features
    for feature in _class.feature_nodes:
        if type(feature) is DefAttrNode:
            def_attr_class_visitor(feature, current_class, local_scope)
        if type(feature) is DefFuncNode:
            def_func_visitor(feature, current_class, local_scope)


def def_attr_class_visitor(attr: DefAttrNode, current_class: CoolType, local_scope: dict):
    if attr.expr:
        expr_type = expression_visitor(attr.expr, current_class, {})
        attr_type = type_by_name(attr.type)
        if attr_type is not None and not check_inherits(expr_type, attr_type):
            add_semantic_error(attr.lineno, attr.colno, f'cannot save type \'{expr_type}\' inside type \'{attr_type}\'')
        else:
            return attr_type


def def_func_visitor(function: DefFuncNode, current_class: CoolType, local_scope: dict):
    local_scope = local_scope.copy()
    for arg in function.params:
        local_scope[arg[0]] = type_by_name(arg[1])
    body_type = expression_visitor(function.expressions, current_class, local_scope)
    return_type = type_by_name(function.return_type)
    if return_type == SelfType:
        return_type = current_class
    if check_inherits(body_type, return_type):
        return return_type
    elif body_type is not None:
        add_semantic_error(function.lineno, function.colno, f'invalid returned type \'{function.return_type}\'')


def int_visitor(expr: IntNode, current_class, local_scope):
    expr.returned_type = IntType
    return IntType


def string_visitor(expr: StringNode, current_class, local_scope):
    expr.returned_type = StringType
    return StringType


def bool_visitor(expr: BoolNode, current_class, local_scope):
    expr.returned_type = BoolType
    return BoolType


def var_visitor(var: VarNode, current_class: CoolType, local_scope: dict):
    if var.id in local_scope.keys():
        var.returned_type = local_scope[var.id]
    attribute, _ = get_attribute(current_class, var.id)
    if attribute is not None:
        var.returned_type = attribute.attrType
    else:
        add_semantic_error(var.lineno, var.colno, f'unknown variable \'{var.id}\'')
    return var.returned_type


def arithmetic_operator_visitor(operator: BinaryNode, current_class: CoolType, local_scope: dict):
    lvalue_type = expression_visitor(operator.lvalue, current_class, local_scope)
    if lvalue_type != IntType and lvalue_type is not None:
        add_semantic_error(operator.lvalue.lineno, operator.lvalue.colno,
                           f'invalid left value type {lvalue_type}, must be a {IntType}')
    rvalue_type = expression_visitor(operator.rvalue, current_class, local_scope)
    if rvalue_type != IntType and rvalue_type is not None:
        add_semantic_error(operator.rvalue.lineno, operator.rvalue.colno,
                           f'invalid left value type {rvalue_type}, must be a {IntType}')
    operator.returned_type = IntType
    return IntType


def equal_visitor(equal: EqNode, current_class: CoolType, local_scope: dict):
    lvalue_type = expression_visitor(equal.lvalue, current_class, local_scope)
    rvalue_type = expression_visitor(equal.rvalue, current_class, local_scope)
    static_types = [IntType, BoolType, StringType]
    if (lvalue_type in static_types or rvalue_type in static_types) and lvalue_type != rvalue_type:
        add_semantic_error(equal.lineno, equal.colno, f'impossible compare {lvalue_type} and {rvalue_type} types')
    equal.returned_type = BoolType
    return BoolType


def comparison_visitor(cmp: BinaryNode, current_class: CoolType, local_scope: dict):
    lvalue_type = expression_visitor(cmp.lvalue, current_class, local_scope)
    if lvalue_type != IntType and lvalue_type is not None:
        add_semantic_error(cmp.lvalue.lineno, cmp.lvalue.colno, f'lvalue type must be a {IntType}')
    rvalue_type = expression_visitor(cmp.rvalue, current_class, local_scope)
    if rvalue_type != IntType and rvalue_type is not None:
        add_semantic_error(cmp.rvalue.lineno, cmp.rvalue.colno, f'rvalue type must be a {IntType}')
    cmp.returned_type = BoolType
    return BoolType


def assignment_visitor(assign: AssignNode, current_class: CoolType, local_scope: dict):
    try:
        id_type = local_scope[assign.id]
    except KeyError:
        attr, _ = get_attribute(current_class, assign.id)
        if attr is None:
            add_semantic_error(assign.id.lineno, assign.id.colno, f'unknown variable \'{assign.id}\'')
            id_type = None
        else:
            id_type = attr.attrType
    expr_type = expression_visitor(assign.expr, current_class, local_scope)
    if not check_inherits(expr_type, id_type) and id_type is not None and expr_type is not None:
        add_semantic_error(assign.expr.lineno, assign.expr.colno,
                           f'Type \'{expr_type}\' cannot be stored in type \'{id_type}\'')
    assign.returned_type = expr_type
    return expr_type


def def_attribute_visitor(def_attr: DefAttrNode, current_class: CoolType, local_scope: dict):
    id_type = type_by_name(def_attr.type)
    if id_type is None:
        add_semantic_error(def_attr.lineno, def_attr.colno, f'unknown type \'{def_attr.type}\'')
    if def_attr.expr:
        expr_type = expression_visitor(def_attr.expr, current_class, local_scope)
        if not check_inherits(expr_type, id_type) and id_type is not None and expr_type is not None:
            add_semantic_error(def_attr.lineno, def_attr.colno,
                               f'Type \'{expr_type}\' cannot be stored in type \'{id_type}\'')
    return id_type


def let_visitor(let: LetNode, current_class: CoolType, local_scope: dict):
    local_scope = local_scope.copy()
    for attribute in let.let_attrs:
        id_type = type_by_name(attribute.type)
        if id_type is None:
            add_semantic_error(attribute.lineno, attribute.colno, f'unknown type \'{attribute.type}\'')
            return None
        attribute_type = expression_visitor(attribute, current_class, local_scope)
        if attribute_type is None:
            return None
        if not check_inherits(attribute_type, id_type):
            add_semantic_error(attribute.lineno, attribute.colno,
                               f'Type \'{attribute_type}\' cannot be stored in type \'{id_type}\'')
            return None
        local_scope[attribute.id] = ObjectType
    let.returned_type = expression_visitor(let.expr, current_class, local_scope)
    return let.returned_type


def list_expr_visitor(block: BlockNode, current_class: CoolType, local_scope: dict):
    final_type = None
    for expr in block.expressions:
        final_type = expression_visitor(expr, current_class, local_scope)
    block.returned_type = final_type
    return final_type


def if_visitor(if_struct: IfNode, current_class: CoolType, local_scope: dict):
    predicate_type = expression_visitor(if_struct.if_expr, current_class, local_scope)
    if predicate_type != BoolType:
        add_semantic_error(if_struct.if_expr.lineno, if_struct.if_expr.colno, f'\'if\' condition must be a {BoolType}')
    then_type = expression_visitor(if_struct.then_expr, current_class, local_scope)
    else_type = expression_visitor(if_struct.else_expr, current_class, local_scope)
    if_struct.returned_type = pronounced_join(then_type, else_type)
    return if_struct.returned_type


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
                add_semantic_error(func_call.lineno, func_call.colno, f'unknown type \'{func_call.type}\'')
            elif check_inherits(current_class, specific_type):
                method, msg = specific_type.get_method_without_hierarchy(func_call.id, args_types)
            else:
                add_semantic_error(func_call.lineno, func_call.colno,
                                   f'type {current_class} not inherits from {specific_type}')
        else:
            object_type = expression_visitor(func_call.object, current_class, local_scope)
            if object_type is None:
                return None
            else:
                method, msg = object_type.get_method(func_call.id, args_types)
    else:
        method, msg = current_class.get_method(func_call.id, args_types)
    if method is None:
        add_semantic_error(func_call.lineno, func_call.colno, msg)
    elif method.returnedType == SelfType:
        func_call.returned_type = current_class
    else:
        func_call.returned_type = method.returnedType
    return func_call.returned_type


def case_expr_visitor(case: CaseNode, current_class: CoolType, local_scope: dict):
    expr_0 = expression_visitor(case.expr, current_class, local_scope)

    branch_0 = case.case_list[0]
    temp = local_scope.copy()
    temp[branch_0.id] = expr_0
    current_type = expression_visitor(branch_0.expr, current_class, temp)

    for branch in case.case_list[1:]:
        temp = local_scope.copy()
        temp[branch.id] = expr_0
        current_type = pronounced_join(current_type, expression_visitor(branch.expr, current_class, temp))
    case.returned_type = current_type
    return case.returned_type


def is_void_expr_visitor(isvoid: IsVoidNode, current_class: CoolType, local_scope: dict):
    expression_visitor(isvoid.val, current_class, local_scope)
    isvoid.returned_type = BoolType
    return BoolType


def loop_expr_visitor(loop: WhileNode, current_class: CoolType, local_scope: dict):
    predicate_type = expression_visitor(loop.cond, current_class, local_scope)
    if predicate_type != BoolType and predicate_type is not None:
        add_semantic_error(loop.cond.lineno, loop.cond.colno, f'\"loop\" condition must be a {BoolType}')
    expression_visitor(loop.body, current_class, local_scope)
    loop.returned_type = ObjectType
    return ObjectType


def new_expr_visitor(new: NewNode, current_class: CoolType, local_scope: dict):
    t = type_by_name(new.type)
    if not t:
        add_semantic_error(new.lineno, new.colno, f'Type {new.type} does not exist. Cannot create instance.')
    if t == SelfType:
        new.returned_type = current_class
    else:
        new.returned_type = t
    return new.returned_type


__visitors__ = {
    BlockNode: list_expr_visitor,
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
    FuncCallNode: func_call_visitor,
    CaseNode: case_expr_visitor,
    IsVoidNode: is_void_expr_visitor,
    WhileNode: loop_expr_visitor,
    NewNode: new_expr_visitor
}


def expression_visitor(expression, current_class: CoolType, local_scope: dict) -> CoolType:
    try:
        return __visitors__[type(expression)](expression, current_class, local_scope)
    except KeyError:
        print(f'Not visitor for {expression}')


def semantic_check(node):
    if type(node) is ProgramNode:
        program_visitor(node)
