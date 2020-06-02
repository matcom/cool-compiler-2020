import code_generation.CIL.ast as cil
import lexer_parser.ast as lp_ast
from semantic.types import *
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
    local = cil.LocalNode(id)
    __LOCALS__[id] = local
    return local


labels_count = 0


def add_label():
    global labels_count
    labels_count += 1
    return f'label_{labels_count}'


def ast_to_cil(ast):
    if type(ast) == lp_ast.ProgramNode:
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
    for t in TypesByName:
        _type = cil.TypeNode(t)
        value = TypesByName[t]
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

    function main {
	    LOCAL __main__ ;
	    LOCAL main_result ;
	    __main__ = ALLOCATE Main ;
	    ARG __main__ ;
	    main_result = VCALL Main main ;
    }
    """
    main_instance = '__main__'
    main_result = 'main_result'
    main_function = cil.FuncNode('main', [], [cil.LocalNode(main_instance), cil.LocalNode(main_result)],
                                 [cil.AllocateNode('Main', main_instance),
                                  cil.ArgNode(main_instance),
                                  cil.VCAllNode('Main', 'main', main_result)])
    built_in_code.append(main_function)

    # completing .CODE and .DATA sections

    for c in program.classes:
        for f in c.feature_nodes:
            if type(f) == DefFuncNode:
                fun = func_to_cil_visitor(c.type, f)
                code.append(fun)

    built_in_code += built_in_to_cil()

    data = [cil.DataNode(__DATA__[data_value], data_value)
            for data_value in __DATA__.keys()]

    cil_program = cil.ProgramNode(types, data, code, built_in_code)
    remove_unused_locals(cil_program)
    optimization_locals(cil_program)
    return cil_program


def built_in_to_cil():
    return [out_int_to_cil(), out_string_to_cil(), in_string_to_cil(), in_int_to_cil(), type_name_to_cil(), copy_to_cil(), length_to_cil(), concat_to_cil(), substring_to_cil()]


def out_string_to_cil():
    return cil.FuncNode('IO_out_string', [cil.ParamNode('self'), cil.ParamNode('str')], [], [cil.PrintNode('str'), cil.ReturnNode('self')])


def out_int_to_cil():
    return cil.FuncNode('IO_out_int', [cil.ParamNode('self'), cil.ParamNode('int')], [], [cil.PrintNode('int'), cil.ReturnNode('self')])


def in_string_to_cil():
    return cil.FuncNode('IO_in_string', [cil.ParamNode('self')], [cil.LocalNode('str')], [cil.ReadNode('str'), cil.ReturnNode('str')])


def in_int_to_cil():
    return cil.FuncNode('IO_in_int', [cil.ParamNode('self')], [cil.LocalNode('int')], [cil.ReadIntNode('int'), cil.ReturnNode('int')])


def type_name_to_cil():
    return cil.FuncNode('Object_type_name', [cil.ParamNode('self')], [cil.LocalNode('type'), cil.LocalNode('str')], [cil.TypeOfNode('type', 'self'), cil.ReturnNode('type')])


def copy_to_cil():
    return cil.FuncNode('Object_copy', [cil.ParamNode('self')], [cil.LocalNode('copy')], [cil.CopyNode('self', 'copy'), cil.ReturnNode('copy')])


def length_to_cil():
    return cil.FuncNode('length_String', [cil.ParamNode('self')], [cil.LocalNode('result')], [cil.LengthNode('self', 'result'), cil.ReturnNode('result')])


def concat_to_cil():
    return cil.FuncNode('concat_String', [cil.ParamNode('self'), cil.ParamNode('x')], [cil.LocalNode('result')], [cil.ConcatNode('self', 'x', 'result'), cil.ReturnNode('result')])


def substring_to_cil():
    return cil.FuncNode('substr_String', [cil.ParamNode('self'), cil.ParamNode('i'), cil.ParamNode('l')], [cil.LocalNode('result')], [cil.SubStringNode('self', 'i', 'l', 'result'), cil.ReturnNode('result')])


def func_to_cil_visitor(type_name, func):
    '''
    Converts from FunctionNode in parsing AST to FuncionNode in cil AST. \n
    1) Builds ParamNodes for each param in FunctionNode.params\n
    2) Builds function body by putting together each instruction's body\n
    3) Creates an array of necessary local variables

    '''
    global __LOCALS__, __DATA_LOCALS__, __TYPEOF__, labels_count, __CURRENT_TYPE__
    name = f'{type_name}_{func.id}'
    params = [cil.ParamNode('self')]
    params += [cil.ParamNode(id) for (id, t) in func.params]
    __LOCALS__ = {}
    labels_count = 0
    __DATA_LOCALS__ = {}
    __TYPEOF__ = {}
    __CURRENT_TYPE__ = type_name
    body = []

    instruction = expression_to_cil_visitor(
        func.expressions)
    body += instruction.body

    body.append(cil.ReturnNode(instruction.value))

    _locals = __LOCALS__.copy()
    return cil.FuncNode(name, params, [_locals[k] for k in _locals.keys()], body)


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
    body.append(cil.TypeOfNode(t, expr_cil.value))
    types = []
    labels = []
    for c in case.case_list:
        types.append(c.type)

    for _ in range(len(case.case_list)):
        labels.append(add_label())

    value = None

    for i, branch in enumerate(case.case_list):
        predicate = add_local()
        body.append(cil.MinusNode(t, branch.type, predicate))
        body.append(cil.ConditionalGotoNode(predicate, labels[i]))
        val = add_local(branch.id)
        body.append(cil.AssignNode(val, expr_cil.value))
        branch_cil = expression_to_cil_visitor(
            branch.expr)
        body += branch_cil.body
        value = branch_cil.value
        body.append(cil.LabelNode(labels[i]))

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
            [cil.SetAttrNode('self', assign.id, expr.value, index)]
        return CIL_block(body, expr.value)
    else:
        val = add_local(assign.id)
        body = expr.body + [cil.AssignNode(val, expr.value)]
        return CIL_block(body, val)


def arith_to_cil_visitor(arith):
    l = expression_to_cil_visitor(arith.lvalue)
    r = expression_to_cil_visitor(arith.rvalue)

    cil_result = add_local()

    body = l.body + r.body

    if type(arith) == lp_ast.PlusNode:
        body.append(cil.PlusNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.MinusNode:
        body.append(cil.MinusNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.StarNode:
        body.append(cil.StarNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.DivNode:
        body.append(cil.DivNode(l.value, r.value, cil_result))

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

    body = predicate.body + [cil.ConditionalGotoNode(predicate.value, label_1)] + else_expression.body + [
        cil.AssignNode(value, else_expression.value), cil.GotoNode(label_2), cil.LabelNode(label_1)] + then.body + [
        cil.AssignNode(value, then.value), cil.LabelNode(label_2)]

    return CIL_block(body, value)


def loop_to_cil_visitor(loop):
    predicate = expression_to_cil_visitor(loop.cond)

    loop_block = expression_to_cil_visitor(loop.body)

    value = add_local()

    predicate_label = add_label()
    loop_label = add_label()
    end_label = add_label()

    body = [cil.LabelNode(predicate_label)] + predicate.body + [cil.ConditionalGotoNode(predicate.value, loop_label), cil.GotoNode(end_label),
                                                                cil.LabelNode(loop_label)] + loop_block.body + [cil.GotoNode(predicate_label), cil.LabelNode(end_label), cil.AssignNode(value, 0)]

    return CIL_block(body, value)


def equal_to_cil_visitor(equal):
    l = expression_to_cil_visitor(equal.lvalue)
    r = expression_to_cil_visitor(equal.rvalue)

    cil_result = add_local()
    end_label = add_label()
    value = add_local()

    body = l.body + r.body + [cil.MinusNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(
                                  cil_result, end_label), cil.AssignNode(value, 1),
                              cil.LabelNode(end_label)]

    return CIL_block(body, value)


def lessthan_to_cil_visitor(lessthan):
    l = expression_to_cil_visitor(lessthan.lvalue)
    r = expression_to_cil_visitor(lessthan.rvalue)

    value = add_local()
    body = l.body + r.body + [cil.LessNode(l.value, r.value, value)]
    return CIL_block(body, value)


def lesseqthan_to_cil_visitor(lessthan):
    l = expression_to_cil_visitor(lessthan.lvalue)
    r = expression_to_cil_visitor(lessthan.rvalue)

    value = add_local()
    body = l.body + r.body + [cil.LessEqNode(l.value, r.value, value)]
    return CIL_block(body, value)


def integer_to_cil_visitor(integer):
    return CIL_block([], integer.value)


def bool_to_cil_visitor(bool):
    return CIL_block([], 1) if bool.value == 'true' else CIL_block([], 0)


def id_to_cil_visitor(id):
    if id.id in __ATTR__[__CURRENT_TYPE__]:
        result = add_local()
        index = __ATTR__[__CURRENT_TYPE__].index(id.id)
        return CIL_block([cil.GetAttrNode('self', id.id, result, index)], result)
    try:
        val = __LOCALS__[id.id]
        return CIL_block([], val)
    except:
        return CIL_block([], id.id)


def new_to_cil_visitor(new_node):
    value = add_local()
    t = new_node.type
    body = []

    if t == 'SELF_TYPE':
        t, need_typeof = get_typeof(t, 'self')
        if need_typeof:
            body.append(cil.TypeOfNode(t, 'self'))

    body.append(cil.AllocateNode(t, value))
    init_attr = TypesByName[t].get_all_attributes()

    for index, attr in enumerate(init_attr):
        if attr.expression:
            attr_cil = expression_to_cil_visitor(
                attr.expression)
            body += attr_cil.body
            body.append(cil.SetAttrNode(value, attr.id, attr_cil.value, index))

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
        body = [cil.LoadNode(str_addr, str_id)]
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
            body.append(cil.AssignNode(val, attr_cil.value))

    expr_cil = expression_to_cil_visitor(let.expr)
    body += expr_cil.body

    return CIL_block(body, expr_cil.value)


def logic_not_to_cil_visitor(not_node):
    expr_cil = expression_to_cil_visitor(
        not_node.val)

    value = add_local()
    end_label = add_label()

    body = expr_cil.body + [cil.AssignNode(value, 0), cil.ConditionalGotoNode(expr_cil.value, end_label),
                            cil.AssignNode(value, 1), cil.LabelNode(end_label)]

    return CIL_block(body, value)


def not_to_cil_visitor(not_node):
    expr_cil = expression_to_cil_visitor(
        not_node.val)

    value = add_local()

    body = expr_cil.body + [cil.NotNode(expr_cil.value, value)]

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
    if call.object:
        obj_cil = expression_to_cil_visitor(
            call.object)
        body += obj_cil.body
        obj = obj_cil.value
    else:
        obj = 'self'

    arg_values = []

    for arg in call.args:
        arg_cil = expression_to_cil_visitor(arg)
        body += arg_cil.body
        arg_values.append(arg_cil.value)

    t, need_typeof = get_typeof(obj)
    if need_typeof:
        body.append(cil.TypeOfNode(t, obj))

    body.append(cil.ArgNode(obj))

    for arg in arg_values:
        body.append(cil.ArgNode(arg))

    result = add_local()
    if not call.type:
        body.append(cil.VCAllNode(t, call.id, result))
    else:
        body.append(cil.VCAllNode(call.type, call.id, result))

    return CIL_block(body, result)


__visitor__ = {
    lp_ast.AssignNode: assign_to_cil_visitor,
    lp_ast.BlockNode: block_to_cil_visitor,
    lp_ast.BoolNode: bool_to_cil_visitor,
    lp_ast.IfNode: if_to_cil_visitor,
    lp_ast.WhileNode: loop_to_cil_visitor,
    lp_ast.EqNode: equal_to_cil_visitor,
    lp_ast.LogicNegationNode: logic_not_to_cil_visitor,
    lp_ast.LetNode: let_to_cil_visitor,
    lp_ast.NewNode: new_to_cil_visitor,
    lp_ast.IntNode: integer_to_cil_visitor,
    lp_ast.StringNode: string_to_cil_visitor,
    lp_ast.PlusNode: arith_to_cil_visitor,
    lp_ast.MinusNode: arith_to_cil_visitor,
    lp_ast.StarNode: arith_to_cil_visitor,
    lp_ast.DivNode: arith_to_cil_visitor,
    lp_ast.VarNode: id_to_cil_visitor,
    lp_ast.FuncCallNode: func_call_to_cil_visitor,
    lp_ast.IsVoidNode: is_void_to_cil_visitor,
    lp_ast.NegationNode: not_to_cil_visitor,
    lp_ast.LessThanNode: lessthan_to_cil_visitor,
    lp_ast.LessEqNode: lesseqthan_to_cil_visitor,
    lp_ast.CaseNode: case_to_cil_visitor,
}


class CIL_block:
    def __init__(self, body, value):
        self.body = body
        self.value = value
