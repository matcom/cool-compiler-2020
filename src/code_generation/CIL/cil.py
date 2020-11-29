from . import ast as CilAST
import lexer_parser.ast as CoolAST
import cool_types as CT
from .optimization import optimization_locals, remove_unused_locals

__DATA__ = {}


def add_str_data(data: str):
    try:
        return __DATA__[data]
    except KeyError:
        data_count = len(__DATA__) + 1
        __DATA__[data] = f'data_{data_count}'
        return __DATA__[data]


__LOCALS__ = {}


def add_local(id=None):
    global __LOCALS__
    if id is None:
        id = f'local_{len(__LOCALS__)}'
    local = CilAST.LocalNode(id)
    __LOCALS__[id] = local
    return local


labels_count = 0


def add_label():
    global labels_count
    labels_count += 1
    return f'label_{labels_count}'


def ast_to_cil(ast):
    if type(ast) == CoolAST.ProgramNode:
        return program_to_cil_visitor(ast)
    raise Exception(f'AST root must be program')


__DATA_LOCALS__ = {}


def add_data_local(string_addr):
    try:
        return __DATA_LOCALS__[string_addr], False
    except KeyError:
        local_data = add_local()
        __DATA_LOCALS__[string_addr] = local_data
        return local_data, True


__TYPEOF__ = {}


def get_typeof(obj):
    try:
        return __TYPEOF__[obj], False
    except KeyError:
        type_local = add_local()
        __TYPEOF__[obj] = type_local
        return type_local, True


__ATTR__ = {}
__CURRENT_TYPE__ = None


def program_to_cil_visitor(program):
    types = []
    code = []
    built_in_code = []

    # completing .TYPE section
    for t in CT.TypesByName:
        _type = CilAST.TypeNode(t)
        value = CT.TypesByName[t]
        __ATTR__[t] = []
        for attr in value.get_all_attributes():
            _type.attributes.append(attr.id)
            __ATTR__[t].append(attr.id)

        for met in value.get_all_inherited_methods():
            _type.methods[met.id] = met.owner

        for met in value.get_all_self_methods():
            _type.methods[met] = t

        types.append(_type)

    """
    Building main function
    """
    main_init = new_to_cil_visitor(CoolAST.NewNode('Main'))
    body = main_init.body
    main_result = add_local('main_result')
    body.append(CilAST.ArgNode(main_init.value))
    body.append(CilAST.VCAllNode('Main', 'main', main_result))
    
    main_function = CilAST.FuncNode(
        'main', [], [__LOCALS__[k] for k in __LOCALS__.keys()], body)
    built_in_code.append(main_function)

    # completing .CODE and .DATA sections

    for c in program.classes:
        for f in c.feature_nodes:
            if type(f) == CoolAST.DefFuncNode:
                fun = func_to_cil_visitor(c.type, f)
                code.append(fun)

    built_in_code += built_in_to_cil()

    data = [CilAST.DataNode(__DATA__[data_value], data_value)
            for data_value in __DATA__.keys()]

    cil_program = CilAST.ProgramNode(types, data, code, built_in_code)
    remove_unused_locals(cil_program)
    #aqui se esta perdiendo un vcall
    optimization_locals(cil_program)
    return cil_program


def built_in_to_cil():
    return [out_int_to_cil(), out_string_to_cil(), in_string_to_cil(), in_int_to_cil(), type_name_to_cil(), copy_to_cil(), length_to_cil(), concat_to_cil(), substring_to_cil()]


def out_string_to_cil():
    return CilAST.FuncNode('IO_out_string', [CilAST.ParamNode('self'),  CilAST.ParamNode('str')], [], [CilAST.PrintNode('str'),  CilAST.ReturnNode('self')])


def out_int_to_cil():
    return CilAST.FuncNode('IO_out_int', [CilAST.ParamNode('self'),  CilAST.ParamNode('int')], [], [CilAST.PrintNode('int'),  CilAST.ReturnNode('self')])


def in_string_to_cil():
    _str = CilAST.LocalNode('str')
    return CilAST.FuncNode('IO_in_string', [CilAST.ParamNode('self')], [_str], [CilAST.ReadNode(_str),   CilAST.ReturnNode(_str)])


def in_int_to_cil():
    i = CilAST.LocalNode('int')
    return CilAST.FuncNode('IO_in_int', [CilAST.ParamNode('self')], [i], [CilAST.ReadIntNode(i),   CilAST.ReturnNode(i)])


def type_name_to_cil():
    t = CilAST.LocalNode('type')
    return CilAST.FuncNode('Object_type_name', [CilAST.ParamNode('self')], [t], [CilAST.TypeOfNode(t, 'self'),   CilAST.ReturnNode(t)])


def copy_to_cil():
    copy = CilAST.LocalNode('copy')
    return CilAST.FuncNode('Object_copy', [CilAST.ParamNode('self')], [copy], [CilAST.CopyNode('self', copy),   CilAST.ReturnNode(copy)])


def length_to_cil():
    result = CilAST.LocalNode('len_result')
    return CilAST.FuncNode('String_length', [CilAST.ParamNode('self')], [result], [CilAST.LengthNode('self', result),   CilAST.ReturnNode(result)])


def concat_to_cil():
    result = CilAST.LocalNode('concat_result')
    return CilAST.FuncNode('String_concat', [CilAST.ParamNode('self'),   CilAST.ParamNode('x')], [result], [CilAST.ConcatNode('self', 'x', result),   CilAST.ReturnNode(result)])


def substring_to_cil():
    result = CilAST.LocalNode('substring_result')
    return CilAST.FuncNode('String_substr', [CilAST.ParamNode('self'),   CilAST.ParamNode('i'),   CilAST.ParamNode('l')], [result], [CilAST.SubStringNode('self', 'i', 'l', result),   CilAST.ReturnNode(result)])


def abort_to_cil():
    result = CilAST.LocalNode('abort_result')
    return CilAST.FuncNode('Object_abort', [CilAST.ParamNode('self')], [result], CilAST.ReturnNode(result))


def func_to_cil_visitor(type_name, func):
    '''
    Converts from FunctionNode in COOL AST to FuncionNode in CIL AST. \n
    1) Builds ParamNodes for each param in FunctionNode.params\n
    2) Builds function body by putting together each instruction's body\n
    3) Creates an array of necessary local variables

    '''
    global __LOCALS__, __DATA_LOCALS__, __TYPEOF__, labels_count, __CURRENT_TYPE__
    name = f'{type_name}_{func.id}'
    params = [CilAST.ParamNode('self')]
    params += [CilAST.ParamNode(id) for (id, t) in func.params]
    __LOCALS__ = {}
    __DATA_LOCALS__ = {}
    __TYPEOF__ = {}
    __CURRENT_TYPE__ = type_name
    body = []

    instruction = expression_to_cil_visitor(
        func.expressions)
    body += instruction.body

    body.append(CilAST.ReturnNode(instruction.value))

    _locals = __LOCALS__.copy()
    return CilAST.FuncNode(name, params, [_locals[k] for k in _locals.keys()], body)


def expression_to_cil_visitor(expression):
    '''
    Selects the appropriate CIL converter for each expression type and calls it. \n
    If there is no appropriate CIL converter it throws the exception \'There is no visitor for [type(expression)]\'
    '''
    try:
        return __visitor__[type(expression)](expression)
    except:
        raise Exception(f'There is no visitor for {type(expression)}')


def case_to_cil_visitor(case):
    '''
    CaseNode CIL converter.\n
    1) Attaches the body of case expression to instruction body.\n
    2) Finds out string repr of case expression dynamic type.\n
    3) For each branch it builts a labeled body in which it is compared branch type to case expression type.\n
    4) Inside the labeled body the branch expression body is attached.

    '''
    body = []
    expr_cil = expression_to_cil_visitor(case.expr)
    body += expr_cil.body
    t = add_local()
    body.append(CilAST.TypeOfNode(t, expr_cil.value))
    types = []
    labels = []
    for c in case.case_list:
        types.append(c.type)

    for _ in range(len(case.case_list)):
        labels.append(add_label())

    value = None

    for i, branch in enumerate(case.case_list):
        predicate = add_local()
        body.append(CilAST.MinusNode(t, branch.type, predicate))
        body.append(CilAST.ConditionalGotoNode(predicate, labels[i]))
        val = add_local(branch.id)
        body.append(CilAST.AssignNode(val, expr_cil.value))
        branch_cil = expression_to_cil_visitor(
            branch.expr)
        body += branch_cil.body
        value = branch_cil.value
        body.append(CilAST.LabelNode(labels[i]))

    return CIL_block(body, value)


def assign_to_cil_visitor(assign):
    '''
    AssignNode CIL converter.\n
    1) Pendiente
    '''

    expr = expression_to_cil_visitor(assign.expr)
    if assign.id in __ATTR__[__CURRENT_TYPE__]:
        index = __ATTR__[__CURRENT_TYPE__].index(assign.id)
        body = expr.body + \
            [CilAST.SetAttrNode('self', assign.id, expr.value, index+2)]
        return CIL_block(body, expr.value)
    else:
        val = add_local(assign.id)
        body = expr.body + [CilAST.AssignNode(val, expr.value)]
        return CIL_block(body, val)


def arith_to_cil_visitor(arith):
    l = expression_to_cil_visitor(arith.lvalue)
    r = expression_to_cil_visitor(arith.rvalue)

    cil_result = add_local()

    body = l.body + r.body

    if type(arith) == CoolAST.PlusNode:
        body.append(CilAST.PlusNode(l.value, r.value, cil_result))
    elif type(arith) == CoolAST.MinusNode:
        body.append(CilAST.MinusNode(l.value, r.value, cil_result))
    elif type(arith) == CoolAST.StarNode:
        body.append(CilAST.StarNode(l.value, r.value, cil_result))
    elif type(arith) == CoolAST.DivNode:
        body.append(CilAST.DivNode(l.value, r.value, cil_result))

    return CIL_block(body, cil_result)


def if_to_cil_visitor(_if):
    predicate = expression_to_cil_visitor(
        _if.if_expr)

    then = expression_to_cil_visitor(_if.then_expr)

    else_expression = expression_to_cil_visitor(
        _if.else_expr)

    label_1 = add_label()
    label_2 = add_label()
    value = add_local()

    body = predicate.body + [CilAST.ConditionalGotoNode(predicate.value, label_1)] + else_expression.body + [
        CilAST.AssignNode(value, else_expression.value),  CilAST.GotoNode(label_2),  CilAST.LabelNode(label_1)] + then.body + [
        CilAST.AssignNode(value, then.value),  CilAST.LabelNode(label_2)]

    return CIL_block(body, value)


def loop_to_cil_visitor(loop):
    predicate = expression_to_cil_visitor(loop.cond)

    loop_block = expression_to_cil_visitor(loop.body)

    value = add_local()

    predicate_label = add_label()
    loop_label = add_label()
    end_label = add_label()

    body = [CilAST.LabelNode(predicate_label)] + predicate.body + [CilAST.ConditionalGotoNode(predicate.value, loop_label),  CilAST.GotoNode(end_label),
                                                                   CilAST.LabelNode(loop_label)] + loop_block.body + [CilAST.GotoNode(predicate_label),  CilAST.LabelNode(end_label),  CilAST.AssignNode(value, 0)]

    return CIL_block(body, value)


def equal_to_cil_visitor(equal):
    l = expression_to_cil_visitor(equal.lvalue)
    r = expression_to_cil_visitor(equal.rvalue)

    cil_result = add_local()
    end_label = add_label()
    value = add_local()

    body = l.body + r.body + [CilAST.MinusNode(l.value, r.value, cil_result),  CilAST.AssignNode(value, 0),
                              CilAST.ConditionalGotoNode(
        cil_result, end_label),  CilAST.AssignNode(value, 1),
        CilAST.LabelNode(end_label)]

    return CIL_block(body, value)


def lessthan_to_cil_visitor(lessthan):
    l = expression_to_cil_visitor(lessthan.lvalue)
    r = expression_to_cil_visitor(lessthan.rvalue)

    value = add_local()
    body = l.body + r.body + [CilAST.LessNode(l.value, r.value, value)]
    return CIL_block(body, value)


def lesseqthan_to_cil_visitor(lessthan):
    l = expression_to_cil_visitor(lessthan.lvalue)
    r = expression_to_cil_visitor(lessthan.rvalue)

    value = add_local()
    body = l.body + r.body + [CilAST.LessEqNode(l.value, r.value, value)]
    return CIL_block(body, value)


def integer_to_cil_visitor(integer):
    return CIL_block([], integer.value)


def bool_to_cil_visitor(bool):
    return CIL_block([], 1) if bool.value == 'true' else CIL_block([], 0)


def id_to_cil_visitor(id):
    if id.id in __ATTR__[__CURRENT_TYPE__]:
        result = add_local()
        index = __ATTR__[__CURRENT_TYPE__].index(id.id)
        return CIL_block([CilAST.GetAttrNode('self', id.id, result, index+2)], result)
    try:
        val = __LOCALS__[id.id]
        return CIL_block([], val)
    except:
        return CIL_block([], id.id)


def new_to_cil_visitor(new_node):
    global __CURRENT_TYPE__
    value = add_local()
    t = new_node.type
    body = []

    if t == 'SELF_TYPE':
        t, need_typeof = get_typeof(__CURRENT_TYPE__)
        if need_typeof:
            body.append(CilAST.TypeOfNode(t, __CURRENT_TYPE__))

    body.append(CilAST.AllocateNode(t, value))
    init_attr = CT.TypesByName[t].get_all_attributes()

    #
    t_data = add_str_data(t)
    t_local = add_local()
    size_local = add_local()
    #

    body.append(CilAST.LoadNode(t_data, t_local))
    body.append(CilAST.SetAttrNode(value, '@type', t_local))
    body.append(CilAST.AssignNode(size_local, (len(init_attr)+2)*4))
    body.append(CilAST.SetAttrNode(value, '@size', size_local, 1))

    old_current_type = __CURRENT_TYPE__
    __CURRENT_TYPE__ = new_node.type
    for index, attr in enumerate(init_attr, 2):
        if attr.expression:
            attr_cil = expression_to_cil_visitor(
                attr.expression)
            body += attr_cil.body
            body.append(CilAST.SetAttrNode(
                value, attr.id, attr_cil.value, index))
    __CURRENT_TYPE__ = old_current_type
    return CIL_block(body, value)


def is_void_to_cil_visitor(isvoid):
    expr_cil = expression_to_cil_visitor(
        isvoid.val)

    body = expr_cil.body

    return CIL_block(body, 1) if not expr_cil.value else CIL_block(body, 0)


def string_to_cil_visitor(str):
    str_addr = add_str_data(str.value)
    str_id, need_load = add_data_local(str_addr)

    if need_load:
        body = [CilAST.LoadNode(str_addr, str_id)]
    else:
        body = []

    return CIL_block(body, str_id)


def let_to_cil_visitor(let):
    body = []
    for attr in let.let_attrs:
        if attr.expr:
            attr_cil = expression_to_cil_visitor(attr.expr)
            body += attr_cil.body
            val = add_local(attr.id)
            body.append(CilAST.AssignNode(val, attr_cil.value))

    expr_cil = expression_to_cil_visitor(let.expr)
    body += expr_cil.body

    return CIL_block(body, expr_cil.value)


def logic_not_to_cil_visitor(not_node):
    expr_cil = expression_to_cil_visitor(
        not_node.val)

    value = add_local()
    end_label = add_label()

    body = expr_cil.body + [CilAST.AssignNode(value, 0),  CilAST.ConditionalGotoNode(expr_cil.value, end_label),
                            CilAST.AssignNode(value, 1),  CilAST.LabelNode(end_label)]

    return CIL_block(body, value)


def not_to_cil_visitor(not_node):
    expr_cil = expression_to_cil_visitor(
        not_node.val)

    value = add_local()

    body = expr_cil.body + [CilAST.NotNode(expr_cil.value, value)]

    return CIL_block(body, value)


def block_to_cil_visitor(block):
    body = []
    value = None

    for expr in block.expressions:
        expr_cil = expression_to_cil_visitor(expr)
        body += expr_cil.body
        value = expr_cil.value

    return CIL_block(body, value)


def func_call_to_cil_visitor(call):
    body = []
    t = None
    if call.object:
        obj_cil = expression_to_cil_visitor(
            call.object)
        body += obj_cil.body
        obj = obj_cil.value
        _, t, _ = call.object.returned_type.get_method(
            call.id, [arg.returned_type for arg in call.args])
    else:
        obj = 'self'
        t = __CURRENT_TYPE__

    arg_values = []

    for arg in call.args:
        arg_cil = expression_to_cil_visitor(arg)
        body += arg_cil.body
        arg_values.append(arg_cil.value)

    body.append(CilAST.ArgNode(obj))

    for arg in arg_values:
        body.append(CilAST.ArgNode(arg))

    result = add_local()
    if not call.type:
        body.append(CilAST.VCAllNode(t, call.id, result))
    else:
        body.append(CilAST.VCAllNode(call.type, call.id, result))

    return CIL_block(body, result)


__visitor__ = {
    CoolAST.AssignNode: assign_to_cil_visitor,
    CoolAST.BlockNode: block_to_cil_visitor,
    CoolAST.BoolNode: bool_to_cil_visitor,
    CoolAST.IfNode: if_to_cil_visitor,
    CoolAST.WhileNode: loop_to_cil_visitor,
    CoolAST.EqNode: equal_to_cil_visitor,
    CoolAST.LogicNegationNode: logic_not_to_cil_visitor,
    CoolAST.LetNode: let_to_cil_visitor,
    CoolAST.NewNode: new_to_cil_visitor,
    CoolAST.IntNode: integer_to_cil_visitor,
    CoolAST.StringNode: string_to_cil_visitor,
    CoolAST.PlusNode: arith_to_cil_visitor,
    CoolAST.MinusNode: arith_to_cil_visitor,
    CoolAST.StarNode: arith_to_cil_visitor,
    CoolAST.DivNode: arith_to_cil_visitor,
    CoolAST.VarNode: id_to_cil_visitor,
    CoolAST.FuncCallNode: func_call_to_cil_visitor,
    CoolAST.IsVoidNode: is_void_to_cil_visitor,
    CoolAST.NegationNode: not_to_cil_visitor,
    CoolAST.LessThanNode: lessthan_to_cil_visitor,
    CoolAST.LessEqNode: lesseqthan_to_cil_visitor,
    CoolAST.CaseNode: case_to_cil_visitor,
}


class CIL_block:
    def __init__(self, body, value):
        self.body = body
        self.value = value
