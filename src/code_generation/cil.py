import lexer_parser.ast as lp_ast
from semantic.types import *
import code_generation.ast as cil


__DATA__ = {}


def add_str_data(data: str):
    try:
        return __DATA__[data]
    except KeyError:
        data_count = len(__DATA__) + 1
        __DATA__[data] = f'data_{data_count}'
        return __DATA__[data]


def ast_to_cil(ast):
    if type(ast) == lp_ast.ProgramNode:
        return program_to_cil_visitor(ast)
    raise Exception(f'AST root must be program')


def program_to_cil_visitor(program):
    types = []
    code = []

    # completing .TYPE section
    for t in TypesByName:
        _type = cil.TypeNode(t)
        value = TypesByName[t]
        for attr in value.get_all_attributes():
            _type.attributes.append(attr)

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
    code.append(main_function)

    # completing .CODE and .DATA sections

    for c in program.classes:
        for f in c.feature_nodes:
            if type(f) == DefFuncNode:
                fun = func_to_cil_visitor(c.type, f)
                code.append(fun)

    data = [cil.DataNode(__DATA__[data_value], data_value)
            for data_value in __DATA__.keys()]

    return cil.ProgramNode(types, data, code)


def func_to_cil_visitor(type_name, func):
    name = f'{type_name}_{func.id}'
    params = [cil.ParamNode('self')]
    params += [cil.ParamNode(id) for (id, t) in func.params]
    locals = []
    body = []
    locals_count = 0

    instruction = expression_to_cil_visitor(
        func.expressions, locals_count)
    locals += instruction.locals
    body += instruction.body
    locals_count += len(instruction.locals)

    return cil.FuncNode(name, params, locals, body)


def expression_to_cil_visitor(expression, locals_count):
    try:
        return __visitor__[type(expression)](expression, locals_count)
    except:
        raise Exception(f'There is no visitor for {type(expression)}')


def case_to_cil_visitor(case, locals_count):
    locals = []
    body = []
    expr_cil = expression_to_cil_visitor(case.expr, locals_count)
    locals_count += len(expr_cil.locals)
    locals += expr_cil.locals
    body += expr_cil.body
    t = f'local_{locals_count}'
    locals_count += 1
    locals.append(cil.LocalNode(t))
    body.append(cil.TypeOfNode(t, expr_cil.value))
    types = []
    labels = []
    for c in case.case_list:
        types.append(c.type)

    for l in range(len(case.case_list)):
        labels.append(f'local_{locals_count}')
        locals_count += 1

    value = None

    for i, branch in enumerate(case.case_list):
        predicate = f'local_{locals_count}'
        locals_count += 1
        locals += [cil.LocalNode(predicate), cil.LocalNode(branch.id)]
        body.append(cil.MinusNode(t, branch.type, predicate))
        body.append(cil.ConditionalGotoNode(predicate, labels[i]))
        body.append(cil.AssignNode(branch.id, expr_cil.value))
        branch_cil = expression_to_cil_visitor(
            branch.expr, locals_count)
        locals += branch_cil.locals
        body += branch_cil.body
        locals_count += len(branch_cil.locals)
        value = branch_cil.value
        body.append(cil.LabelNode(labels[i]))

    return CIL_block(locals, body, value)


def assign_to_cil_visitor(assign, locals_count):
    expr = expression_to_cil_visitor(assign.expr, locals_count)
    locals_count += len(expr.locals)
    value = [f'local_{locals_count}']
    locals = expr.locals + [cil.LocalNode(value)]
    body = expr.body + [cil.AssignNode(assign.id, expr.value)]
    return CIL_block(locals, body, value)


def arith_to_cil_visitor(arith, locals_count):
    l = expression_to_cil_visitor(arith.lvalue, locals_count)
    locals_count += len(l.locals)
    r = expression_to_cil_visitor(arith.rvalue, locals_count)
    locals_count += len(r.locals)

    cil_result = f'local_{locals_count}'

    locals = l.locals + r.locals + [cil.LocalNode(cil_result)]
    body = l.body + r.body

    if type(arith) == lp_ast.PlusNode:
        body.append(cil.PlusNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.MinusNode:
        body.append(cil.MinusNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.StarNode:
        body.append(cil.StarNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.DivNode:
        body.append(cil.DivNode(l.value, r.value, cil_result))

    return CIL_block(locals, body, cil_result)


def if_to_cil_visitor(_if, locals_count):
    predicate = expression_to_cil_visitor(
        _if.if_expr, locals_count)
    locals_count += len(predicate.locals)

    then = expression_to_cil_visitor(_if.then_expr, locals_count)
    locals_count += len(then.locals)

    else_expression = expression_to_cil_visitor(
        _if.else_expr, locals_count)
    locals_count += len(else_expression.locals)

    label_1 = f'local_{locals_count}'
    label_2 = f'local_{locals_count + 1}'
    value = f'local_{locals_count + 2}'

    locals = predicate.locals + then.locals + \
        else_expression.locals + [cil.LocalNode(value)]
    body = [cil.ConditionalGotoNode(predicate.value, label_1)] + else_expression.body + [
        cil.AssignNode(value, else_expression.value), cil.GotoNode(label_2), cil.LabelNode(label_1)] + then.body + [
        cil.AssignNode(value, then.value), cil.LabelNode(label_2)]

    return CIL_block(locals, body, value)


def loop_to_cil_visitor(loop, locals_count):
    predicate = expression_to_cil_visitor(loop.cond, locals_count)
    locals_count += len(predicate.locals)

    loop_block = expression_to_cil_visitor(loop.body, locals_count)
    locals_count += len(loop_block.locals)

    value = f'local_{locals_count}'

    locals = predicate.locals + loop_block.locals + [cil.LocalNode(value)]

    loop_label = f'local_{locals_count + 1}'
    end_label = f'local_{locals_count + 2}'

    body = [cil.ConditionalGotoNode(predicate.value, loop_label), cil.GotoNode(end_label),
            cil.LabelNode(loop_label)] + loop_block.body + [cil.LabelNode(end_label), cil.AssignNode(value, 0)]

    return CIL_block(locals, body, value)


def equal_to_cil_visitor(equal, locals_count):
    l = expression_to_cil_visitor(equal.lvalue, locals_count)
    locals_count += len(l.locals)
    r = expression_to_cil_visitor(equal.rvalue, locals_count)
    locals_count += len(r.locals)

    cil_result = f'local_{locals_count}'
    end_label = f'local_{locals_count + 1}'
    value = f'local_{locals_count + 2}'

    locals = l.locals + r.locals + \
        [cil.LocalNode(cil_result), cil.LocalNode(value)]
    body = l.body + r.body + [cil.MinusNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(
                                  cil_result, end_label), cil.AssignNode(value, 1),
                              cil.LabelNode(end_label)]

    return CIL_block(locals, body, value)


def lessthan_to_cil_visitor(lessthan, locals_count):
    l = expression_to_cil_visitor(lessthan.lvalue, locals_count)
    locals_count += len(l.locals)
    r = expression_to_cil_visitor(lessthan.rvalue, locals_count)
    locals_count += len(r.locals)

    cil_result = f'local_{locals_count}'
    end_label = f'local_{locals_count + 1}'
    value = f'local_{locals_count + 2}'

    locals = l.locals + r.locals + \
        [cil.LocalNode(cil_result), cil.LocalNode(value)]
    body = l.body + r.body + [cil.DivNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(
                                  cil_result, end_label), cil.AssignNode(value, 1),
                              cil.LabelNode(end_label)]

    return CIL_block(locals, body, value)


def lesseqthan_to_cil_visitor(lessthan, locals_count):
    l = expression_to_cil_visitor(lessthan.lvalue, locals_count)
    locals_count += len(l.locals)
    r = expression_to_cil_visitor(lessthan.rvalue, locals_count)
    locals_count += len(r.locals)

    cil_less = f'local_{locals_count}'
    cil_equal = f'local_{locals_count + 1}'
    eq_label = f'local_{locals_count + 2}'
    end_label = f'local_{locals_count + 3}'
    value = f'local_{locals_count + 4}'

    locals = l.locals + r.locals + \
        [cil.LocalNode(cil_less), cil.LocalNode(
            cil_equal), cil.LocalNode(value)]
    body = l.body + r.body + [cil.DivNode(l.value, r.value, cil_less), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(
                                  cil_less, eq_label), cil.AssignNode(value, 1),
                              cil.GotoNode(end_label), cil.LabelNode(eq_label),
                              cil.MinusNode(l.value, r.value, cil_equal), cil.ConditionalGotoNode(
                                  cil_equal, end_label),
                              cil.AssignNode(value, 1), cil.LabelNode(end_label)]

    return CIL_block(locals, body, value)


def integer_to_cil_visitor(integer, locals_count):
    return CIL_block([], [], integer.value)


def bool_to_cil_visitor(bool, locals_count):
    return CIL_block([], [], 1) if bool.value == 'true' else CIL_block([], [], 0)


def id_to_cil_visitor(id, locals_count):
    return CIL_block([], [], id.id)


def new_to_cil_visitor(new_node, locals_count):
    value = f'local_{locals_count}'
    locals = [cil.LocalNode(value)]
    locals_count += 1
    body = [cil.AllocateNode(new_node.type, value)]
    init_attr = TypesByName[new_node.type].get_all_attributes()

    for attr in init_attr:
        if attr.expression:
            attr_cil = expression_to_cil_visitor(
                attr.expression, locals_count)
            locals_count += len(attr_cil.locals)
            locals.append(attr_cil.locals)
            body.append(attr_cil.body)
            body.append(cil.SetAttrNode(value, attr.id, attr_cil.value))

    return CIL_block(locals, body, value)


def is_void_to_cil_visitor(isvoid, locals_count):
    pass


def string_to_cil_visitor(str, locals_count):
    str_addr = add_str_data(str.value)
    str_id = f'local_{locals_count}'

    locals = [cil.LocalNode(str_id)]
    body = [cil.LoadNode(str_addr, str_id)]

    return CIL_block(locals, body, str_id)


def let_to_cil_visitor(let, locals_count):
    body = []
    locals = []
    for attr in let.let_attr:
        attr_cil = expression_to_cil_visitor(attr, locals_count)
        locals_count += len(attr_cil.locals)
        body.append(cil.AssignNode(attr.id, attr_cil.value))
        body += attr_cil.body
        locals += attr_cil.locals

    expr_cil = expression_to_cil_visitor(let.expr, locals_count)
    locals += expr_cil.locals
    body += expr_cil.locals

    return CIL_block(locals, body, expr_cil.value)


def logic_not_to_cil_visitor(not_node, locals_count):
    expr_cil = expression_to_cil_visitor(
        not_node.val, locals_count)
    locals_count += len(expr_cil.locals)

    value = f'local_{locals_count}'
    end_label = f'local_{locals_count + 1}'

    locals = expr_cil.locals + [cil.LocalNode(value)]
    body = expr_cil.body + [cil.AssignNode(value, 0), cil.ConditionalGotoNode(expr_cil.value, end_label),
                            cil.AssignNode(value, 1), cil.LabelNode(end_label)]

    return CIL_block(locals, body, value)


def block_to_cil_visitor(block, locals_count):
    locals = []
    body = []
    value = None

    for expr in block.expressions:
        expr_cil = expression_to_cil_visitor(expr, locals_count)
        locals_count += len(expr_cil.locals)
        locals += expr_cil.locals
        body += expr_cil.body
        value = expr_cil.value

    return CIL_block(locals, body, value)


def func_call_to_cil_visitor(call, locals_count):
    locals = []
    body = []
    if call.object:
        obj_cil = expression_to_cil_visitor(
            call.object, locals_count)
        locals_count += len(obj_cil.locals)
        locals += obj_cil.locals
        body += obj_cil.body
        obj = obj_cil.value
    else:
        obj = 'self'

    arg_values = []

    for arg in call.args:
        arg_cil = expression_to_cil_visitor(arg, locals_count)
        locals_count += len(arg_cil.locals)
        locals += arg_cil.locals
        body += arg_cil.body
        arg_values.append(arg_cil.value)

    t = f'local_{locals_count}'
    locals.append(cil.LocalNode(t))
    body.append(cil.TypeOfNode(t, obj))

    body.append(cil.ArgNode(obj))

    for arg in arg_values:
        body.append(cil.ArgNode(arg))

    result = f'local_{locals_count + 1}'
    locals.append(cil.LocalNode(result))
    if not call.type:
        body.append(cil.VCAllNode(t, call.id, result))
    else:
        body.append(cil.VCAllNode(call.type, call.id, result))

    return CIL_block(locals, body, result)


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
    lp_ast.FuncCallNode: func_call_to_cil_visitor
}


class CIL_block:
    def __init__(self, locals, body, value):
        self.locals = locals
        self.body = body
        self.value = value
