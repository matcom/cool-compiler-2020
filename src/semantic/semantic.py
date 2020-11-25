"""
Copyright (c) 2020 School of Math and Computer Science, University of Havana

COOL compiler project
"""

import cool_types as CT
from lexer_parser.ast import *
from errors import *


def program_visitor(program: ProgramNode):
    '''
    Check semantic for a program.
    1) Check type declaration (check duplicated types...)
    2) Check type hierarchy
    3) Check class Main
    4) Check all methos and attributes for all declared types, and add them to respective type
    5) Check recursive each delared class
    '''
    # 1) and 2)
    if not (CT.check_type_declaration(program) and CT.check_type_hierarchy(program)):
        return

    # 3)
    try:
        CT.TypesByName['Main']
    except KeyError:
        add_semantic_error(0, 0, f'Main class undeclared')
        return

    # 4)
    types_already_check = [CT.ObjectType, CT.IntType,
                           CT.StringType, CT.BoolType, CT.IOType]
    classes = program.classes.copy()
    while len(classes) != 0:
        c: DefClassNode = classes.pop()
        if c.parent_type is not None:
            parent_type = CT.TypesByName[c.parent_type]
            if parent_type not in types_already_check:
                classes = [c] + classes
                continue
        classType = CT.TypesByName[c.type]
        for f in c.feature_nodes:
            if type(f) is DefFuncNode:
                param_types = [param[1] for param in f.params]
                result, msg = classType.add_method(
                    f.id, param_types, f.return_type)
                if not result:
                    add_semantic_error(f.lineno, f.colno, msg)
            elif type(f) is DefAttrNode:
                result, msg = classType.add_attr(f.id, f.type, f.expr)
                if not result:
                    add_semantic_error(f.lineno, f.colno, msg)
        types_already_check.append(classType)

    # 5)
    for c in program.classes:
        class_visitor(c, None, {})


def class_visitor(_class: DefClassNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check class

    class MY_TYPE inherits INHERITS_TYPE{
        FEATURE_LIST
    }

    1) Check each feature in FEATURE_LIST
    '''
    current_class = CT.TypesByName[_class.type]
    local_scope = local_scope.copy()
    local_scope['self'] = current_class
    # 1)
    for feature in _class.feature_nodes:
        if type(feature) is DefAttrNode:
            def_attr_class_visitor(feature, current_class, local_scope)
        if type(feature) is DefFuncNode:
            def_func_visitor(feature, current_class, local_scope)


def def_attr_class_visitor(attr: DefAttrNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check class attribute 

    ID:TYPE <- EXPR

    If EXPR is not None:
    1) Check EXPR
    2) Check type(EXPR) <= TYPE
    '''
    if attr.expr:
        # 1)
        expr_type = expression_visitor(attr.expr, current_class, local_scope)
        attr_type = CT.type_by_name(attr.type)
        # 2)
        if attr_type is not None and not CT.check_inherits(expr_type, attr_type):
            add_semantic_error(
                attr.lineno, attr.colno, f'cannot save type \'{expr_type}\' inside type \'{attr_type}\'')
        else:
            return attr_type


def def_attribute_visitor(def_attr: DefAttrNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check attribute (except class attribute)

    ID:TYPE <- EXPR

    1) Check if TYPE exists
    2) Check if EXPR is not None
        2.1) Check EXPR
        2.2) Check type(EXPR) <= TYPE
    3) Type of the attribute is TYPE
    '''
    # 1)
    id_type = CT.type_by_name(def_attr.type)
    if id_type is None:
        add_semantic_error(def_attr.lineno, def_attr.colno,
                           f'unknown type \'{def_attr.type}\'')
    # 2)
    if def_attr.expr:
        # 2.1)
        expr_type = expression_visitor(
            def_attr.expr, current_class, local_scope)
        # 2.2)
        if not CT.check_inherits(expr_type, id_type) and id_type is not None and expr_type is not None:
            add_semantic_error(def_attr.lineno, def_attr.colno,
                               f'Type \'{expr_type}\' cannot be stored in type \'{id_type}\'')
    # 3)
    return id_type


def def_func_visitor(function: DefFuncNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check function declaration

    ID (PARAMS): RETURN_TYPE{
        EXPR
    }

    1) Add PARAMS to local_scope. Type of PARAMS already check in program_visitor(4)
    2) Check EXPR
    3) Update RETURN_TYPE with current class type if that is SELFTYPE
    4) Check type(EXPR) <= RETURN_TYPE
    '''
    local_scope = local_scope.copy()
    # 1)
    for arg in function.params:
        local_scope[arg[0]] = CT.type_by_name(arg[1])
    # 2)
    body_type = expression_visitor(
        function.expressions, current_class, local_scope)
    return_type = CT.type_by_name(function.return_type)
    # 3)
    if return_type == CT.SelfType:
        return_type = current_class
    # 4)
    if CT.check_inherits(body_type, return_type):
        return return_type
    elif body_type is not None:
        add_semantic_error(function.lineno, function.colno,
                           f'invalid returned type \'{function.return_type}\'')


def assignment_visitor(assign: AssignNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check assigment

    ID <- EXPR

    1) Check type(ID)
        1.1) First find in local_scope
        1.2) Second find in current class attributes
    2) Check EXPR
    3) Check type(EXPR) <= type(ID)
    4) Type of assigment is type(EXPR)
    '''
    # 1)
    try:
        # 1.1)
        id_type = local_scope[assign.id]
    except KeyError:
        # 1.2)
        attr, _ = CT.get_attribute(current_class, assign.id)
        if attr is None:
            add_semantic_error(assign.id.lineno, assign.id.colno,
                               f'unknown variable \'{assign.id}\'')
            id_type = None
        else:
            id_type = attr.attrType
    # 2)
    expr_type = expression_visitor(assign.expr, current_class, local_scope)
    # 3)
    if not CT.check_inherits(expr_type, id_type) and id_type is not None and expr_type is not None:
        add_semantic_error(assign.expr.lineno, assign.expr.colno,
                           f'Type \'{expr_type}\' cannot be stored in type \'{id_type}\'')
    # 4)
    assign.returned_type = expr_type
    return expr_type


def func_call_visitor(func_call: FuncCallNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check function call

    Exist three forms of function call:

    1- EXPR@TYPE.ID(ARGS)
    2- EXPR.ID(ARGS)
    3- ID(ARGS)

    1) Compute args type, not check yet, because check need wait to find the specific function
    2) EXPR is not None (cases 1 and 2)
        2.1) Check type(EXPR)
        2.2) TYPE is not None
            2.2.1) Check TYPE
            2.2.2) Check type(EXPR) <= TYPE
            2.2.3) If returned type of the funtion is SELFTYPE then returned type is TYPE
    3) If EXPR is None
        3.2) If returned type of the function is SELFTYPE then returned type is current class type
    4) Type of function call is the returned type of function

    '''
    args_types = []
    method = None
    msg = None
    func_call.self_type = current_class
    # 1)
    for arg in func_call.args:
        arg_type = expression_visitor(arg, current_class, local_scope)
        args_types.append(arg_type)
    # 2)
    if func_call.object:
        # 2.1)
        object_type = expression_visitor(
            func_call.object, current_class, local_scope)
        if object_type is None:
            return None
        # 2.2)
        if func_call.type:
            # 2.2.1)
            specific_type = CT.type_by_name(func_call.type)
            if specific_type is None:
                add_semantic_error(
                    func_call.lineno, func_call.colno, f'unknown type \'{func_call.type}\'')
            # 2.2.2)
            elif CT.check_inherits(object_type, specific_type):
                method, msg = specific_type.get_method_without_hierarchy(
                    func_call.id, args_types)
                # 2.2.3)
                if method is not None and method.returnedType == CT.SelfType:
                    method.returnedType = specific_type
            else:
                add_semantic_error(func_call.lineno, func_call.colno,
                                   f'type {object_type} not inherits from {specific_type}')
        else:
            method, msg = object_type.get_method(func_call.id, args_types)
            if method is not None and method.returnedType == CT.SelfType:
                method.returnedType = object_type
    # 3)
    else:
        method, msg = current_class.get_method(func_call.id, args_types)
    if method is None and msg is not None:
        add_semantic_error(func_call.lineno, func_call.colno, msg)
    # 3.1)
    elif method.returnedType == CT.SelfType:
        func_call.returned_type = current_class
    else:
        # 4)
        func_call.returned_type = method.returnedType
    return func_call.returned_type


def if_visitor(if_struct: IfNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check \"if\" stament

    if IF_EXPR then THEN_EXPR else ELSE_EXPR fi

    1) Check IF_EXPR. type(IF_EXPR) must be a Bool
    2) Check THEN_EXPR
    3) Check ELSE_EXPR
    4) Type of \"if\" stament is the pronounced join of THEN_EXPR and ELSE_EXPR
    '''
    # 1)
    predicate_type = expression_visitor(
        if_struct.if_expr, current_class, local_scope)
    if predicate_type != CT.BoolType and predicate_type is not None:
        add_semantic_error(if_struct.if_expr.lineno, if_struct.if_expr.colno,
                           f'\'if\' condition must be a {CT.BoolType}')
    # 2)
    then_type = expression_visitor(
        if_struct.then_expr, current_class, local_scope)
    # 3)
    else_type = expression_visitor(
        if_struct.else_expr, current_class, local_scope)
    # 4)
    if_struct.returned_type = CT.pronounced_join(then_type, else_type)
    return if_struct.returned_type


def loop_expr_visitor(loop: WhileNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check loop

     while CONDITION_EXPR loop EXPR pool

    1) Check CONDITION_EXPR. type(CONDITION_EXPR) must be a Bool
    2) Check EXPR
    3) Type of loop is Oject
    '''
    # 1)
    predicate_type = expression_visitor(loop.cond, current_class, local_scope)
    if predicate_type != CT.BoolType and predicate_type is not None:
        add_semantic_error(loop.cond.lineno, loop.cond.colno,
                           f'\"loop\" condition must be a {CT.BoolType}')
    # 2)
    expression_visitor(loop.body, current_class, local_scope)
    # 3)
    loop.returned_type = CT.ObjectType
    return CT.ObjectType


def block_expr_visitor(block: BlockNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check block

    { EXPR_LIST }

    1) Check each epression in EXPR_LIST
    2) Type of block is type of the last expression in EXPR_LIST
    '''
    final_type = None
    # 1)
    for expr in block.expressions:
        final_type = expression_visitor(expr, current_class, local_scope)
    # 2)
    block.returned_type = final_type
    return final_type


def let_visitor(let: LetNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check let

    let LET_ATTRS in EXPR

    1) Check all attributes in LET_ATTRS
    2) Check EXPR
    3) Type of let is type(EXPR)


    '''
    local_scope = local_scope.copy()
    # 1)
    for attribute in let.let_attrs:
        attribute_type = expression_visitor(
            attribute, current_class, local_scope)
        if attribute_type is None:
            return None
        local_scope[attribute.id] = attribute_type
    # 2) and 3)
    let.returned_type = expression_visitor(
        let.expr, current_class, local_scope)
    return let.returned_type


def case_expr_visitor(case: CaseNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check case

    case EXPR_0 of
        ID_1:TYPE_1 => EXPR_1;
            ...
            ...
        ID_n:TYPE_n => EXPR_n;
    esac

    1) Check EXPR_0
    2) Check first branch
        2.1) Check TYPE_1
        2.2) Update local scope with ID_1
        2.3) Check EXPR_1 and set current type as type(EXPR_1)
    3) Check rest of branches (k=2,...,n)
        3.1) Check TYPE_k
        3.2) Update local scope with ID_k
        3.3) Check EXPR_k and set current type as pronounced join of current type and  type(EXPR_k)
    4) Type of case is the pronounced join of all branch expressions types, then is the current type at final of step 3)
    '''

    # 1)
    expr_0 = expression_visitor(case.expr, current_class, local_scope)

    # 2)
    branch_0 = case.case_list[0]
    # 2.1)
    branch_0_type = CT.type_by_name(branch_0.type)
    temp = local_scope.copy()
    if branch_0_type is None:
        add_semantic_error(branch_0.line, branch_0.column,
                           f"unknow type \"{branch_0.type}\"")
    else:
        # 2.2)
        temp[branch_0.id] = branch_0_type
    # 2.3)
    current_type = expression_visitor(branch_0.expr, current_class, temp)

    # 3)
    for branch in case.case_list[1:]:
        temp = local_scope.copy()
        # 3.1)
        branch_type = CT.type_by_name(branch.type)
        if branch_type is None:
            add_semantic_error(branch_0.line, branch_0.column,
                               f"unknow type \"{branch.type}\"")
        # 3.2)
        temp[branch.id] = branch_type
        # 3.3)
        current_type = CT.pronounced_join(
            current_type, expression_visitor(branch.expr, current_class, temp))
    # 4)
    case.returned_type = current_type
    return case.returned_type


def arithmetic_operator_visitor(operator: BinaryNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check arithmetic operator (binary)

    LEXPR operator REXPR

    1) Check LEXPR, must be Int
    2) Check REXPR, must be a Int
    3) Type of the arithmetic operator (binary) is Int
    '''
    # 1)
    lvalue_type = expression_visitor(
        operator.lvalue, current_class, local_scope)
    if lvalue_type != CT.IntType and lvalue_type is not None:
        add_semantic_error(operator.lvalue.lineno, operator.lvalue.colno,
                           f'{ERR_TYPE}: non-Int arguments: {lvalue_type} + {CT.IntType}')
    # 2)
    rvalue_type = expression_visitor(
        operator.rvalue, current_class, local_scope)
    if rvalue_type != CT.IntType and rvalue_type is not None:
        add_semantic_error(operator.rvalue.lineno, operator.rvalue.colno,
                           f'{ERR_TYPE}: non-Int arguments: {CT.IntType} + {rvalue_type}')
    # 3)
    operator.returned_type = CT.IntType
    return CT.IntType


def comparison_visitor(cmp: BinaryNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check comparison

    LEXPR operator REXPR

    1) Check LEXPR, must be Int
    2) Check REXPR, must be Int
    3) Type of the comparison is Bool
    '''
    # 1)
    lvalue_type = expression_visitor(cmp.lvalue, current_class, local_scope)
    if lvalue_type != CT.IntType and lvalue_type is not None:
        add_semantic_error(cmp.lvalue.lineno, cmp.lvalue.colno,
                           f'lvalue type must be a {CT.IntType}')
    # 2)
    rvalue_type = expression_visitor(cmp.rvalue, current_class, local_scope)
    if rvalue_type != CT.IntType and rvalue_type is not None:
        add_semantic_error(cmp.rvalue.lineno, cmp.rvalue.colno,
                           f'rvalue type must be a {CT.IntType}')
    # 3)
    cmp.returned_type = CT.BoolType
    return CT.BoolType


def equal_visitor(equal: EqNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check equal

    LEXPR = REXPR

    1) Check LEXPR
    2) Check REXPR
    3) Check type(LEXPR) is equal to type(REXPR) and must be Int, Bool or String
    4) Type of the equal is Bool
    '''
    # 1)
    lvalue_type = expression_visitor(equal.lvalue, current_class, local_scope)
    # 2)
    rvalue_type = expression_visitor(equal.rvalue, current_class, local_scope)
    # 3)
    static_types = [CT.IntType, CT.BoolType, CT.StringType]
    if (lvalue_type in static_types or rvalue_type in static_types) and lvalue_type != rvalue_type:
        add_semantic_error(equal.lineno, equal.colno,
                           f'impossible compare {lvalue_type} and {rvalue_type} types')
    # 4)
    equal.returned_type = CT.BoolType
    return CT.BoolType


def negation_visitor(negation: NegationNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check binary negation

    ~EXPR

    1) Check EXPR
    2) Check type(EXPR) must be Int
    3) Type of the binary negation (~) is Int
    '''
    # 1)
    value_type = expression_visitor(negation.val, current_class, local_scope)
    # 2)
    if value_type != CT.IntType and value_type is not None:
        add_semantic_error(negation.lineno, negation.colno,
                           f'type {value_type} invalid. The \'~\' operator can only be used with type {CT.IntType}')
    # 3)
    return CT.IntType


def logic_negation_visitor(negation: LogicNegationNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check logic negation

    not EXPR

    1) Check EXPR
    2) Check type(EXPR) must be Bool
    3) Type of the logic negation is Bool

    '''
    # 1)
    value_type = expression_visitor(negation.val, current_class, local_scope)
    # 2)
    if value_type != CT.BoolType and value_type is not None:
        add_semantic_error(negation.lineno, negation.colno,
                           f'type {value_type} invalid. The \'not\' operator can only be used with type {CT.BoolType}')
    # 3)
    return CT.BoolType


def is_void_expr_visitor(isvoid: IsVoidNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check isvoid

    isvoid EXPR

    1) Check EXPR
    2) Type of the isvoid is Bool
    '''
    # 1)
    expression_visitor(isvoid.val, current_class, local_scope)
    # 2)
    isvoid.returned_type = CT.BoolType
    return CT.BoolType


def var_visitor(var: VarNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check var

    ID

    1) Check if ID is in local scope
    2) Check if ID is an class attribute
    3) Type of var is the already funded type
    '''
    # 1)
    if var.id in local_scope.keys():
        var.returned_type = local_scope[var.id]
    else:
        # 2)
        attribute, _ = CT.get_attribute(current_class, var.id)
        if attribute is not None:
            var.returned_type = attribute.attrType
        else:
            add_semantic_error(var.lineno, var.colno,
                               f'unknown variable \'{var.id}\'')
    # 3)
    return var.returned_type


def new_expr_visitor(new: NewNode, current_class: CT.CoolType, local_scope: dict):
    '''
    Check new

    new TYPE

    1) Check TYPE exists
    2) Is TYPE is SELFTYPE then TYPE is updated to current class type
    3) Type of new is TYPE
    '''
    # 1)
    t = CT.type_by_name(new.type)
    if not t:
        add_semantic_error(
            new.lineno, new.colno, f'Type {new.type} does not exist. Cannot create instance.')
    # 2)
    if t == CT.SelfType:
        new.returned_type = current_class
    else:
        new.returned_type = t
    # 3)
    return new.returned_type


def int_visitor(expr: IntNode, current_class, local_scope):
    '''
    Check int

    number

    1) Type os int is Int :)
    '''
    # 1)
    expr.returned_type = CT.IntType
    return CT.IntType


def bool_visitor(expr: BoolNode, current_class, local_scope):
    '''
    Check bool

    [True|Fsle]

    1) Type of bool is Bool :)
    '''
    # 1)
    expr.returned_type = CT.BoolType
    return CT.BoolType


def string_visitor(expr: StringNode, current_class, local_scope):
    '''
    Check string

    "string"

    1) Type of string is String :)
    '''
    expr.returned_type = CT.StringType
    return CT.StringType


__visitors__ = {
    BlockNode: block_expr_visitor,
    IntNode: int_visitor,
    StringNode: string_visitor,
    BoolNode: bool_visitor,
    VarNode: var_visitor,
    PlusNode: arithmetic_operator_visitor,
    MinusNode: arithmetic_operator_visitor,
    StarNode: arithmetic_operator_visitor,
    DivNode: arithmetic_operator_visitor,
    EqNode: equal_visitor,
    NegationNode: negation_visitor,
    LogicNegationNode: logic_negation_visitor,
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


def expression_visitor(expression, current_class: CT.CoolType, local_scope: dict) -> CT.CoolType:
    '''
    This is the main function to check any expression. This function search the
    right function for check the expression.

    expression: expression to check
    current_class: class containing the expression
    local_scope: local scope at the moment
    '''
    try:
        return __visitors__[type(expression)](expression, current_class, local_scope)
    except KeyError:
        print(f'Not visitor for {expression}')


def semantic_check(node):
    '''
    Start semantic check for the entire program. It only works if the node type is ProgramNode
    '''
    if type(node) is ProgramNode:
        program_visitor(node)
