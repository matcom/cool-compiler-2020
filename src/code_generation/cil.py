import code_generation.ast as cil
import lexer_parser.ast as lp_ast
from semantic.types import *

__DATA__ = {}


def add_str_data(data: str):
    try:
        return __DATA__[data]
    except KeyError:
        data_count = len(__DATA__) + 1
        __DATA__[data] = f'data_{data_count}'
        return __DATA__[data]


locals_count = 0


def add_local():
    global locals_count
    locals_count += 1
    return f'local_{locals_count}'


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
                
    code += built_in_to_cil()

    data = [cil.DataNode(__DATA__[data_value], data_value)
            for data_value in __DATA__.keys()]

    return cil.ProgramNode(types, data, code)

def built_in_to_cil():
    return [out_int_to_cil(), out_string_to_cil(), in_string_to_cil()]
    
def out_string_to_cil():
    return cil.FuncNode('IO_out_string', [cil.ParamNode('self'),cil.ParamNode('str')], [], [cil.PrintNode('str'), cil.ReturnNode('self')])

def out_int_to_cil():
    return cil.FuncNode('IO_out_int', [cil.ParamNode('self'),cil.ParamNode('int')], [cil.LocalNode('str')], [cil.StrNode('int', 'str'), cil.PrintNode('int'), cil.ReturnNode('self')])

def in_string_to_cil():
    return cil.FuncNode('IO_in_string', [cil.ParamNode('self')], [cil.LocalNode('str')], [cil.ReadNode('str'), cil.ReturnNode('str')])

def in_int_to_cil():
    pass

def type_name_to_cil():
    pass

def copy_to_cil():
    pass

def length_to_cil():
    return cil.FuncNode('length_String', [cil.ParamNode('self')], [cil.LocalNode('result')], [cil.LengthNode('self', 'result'), cil.ReturnNode('result')])

def concat_to_cil():
    return cil.FuncNode('concat_String', [cil.ParamNode('self'), cil.ParamNode('x')], [cil.LocalNode('result')], [cil.ConcatNode('self', 'x', 'result'), cil.ReturnNode('result')])

def substring_to_cil():
    return cil.FuncNode('substr_String', [cil.ParamNode('self'), cil.ParamNode('i'),cil.ParamNode('l')], [cil.LocalNode('result')], [cil.SubStringNode('self', 'i', 'l','result'), cil.ReturnNode('result')])

def func_to_cil_visitor(type_name, func):
    global locals_count, __DATA_LOCALS__, __TYPEOF__
    name = f'{type_name}_{func.id}'
    params = [cil.ParamNode('self')]
    params += [cil.ParamNode(id) for (id, t) in func.params]
    locals_count = 0
    __DATA_LOCALS__ = {}
    __TYPEOF__ = {}
    body = []

    instruction = expression_to_cil_visitor(
        func.expressions)
    body += instruction.body
    
    body.append(cil.ReturnNode(instruction.value))

    _locals = [cil.LocalNode(f'local_{i + 1}') for i in range(locals_count)]
    return cil.FuncNode(name, params, _locals, body)


def expression_to_cil_visitor(expression):
    #try:
    return __visitor__[type(expression)](expression)
    #except:
        #raise Exception(f'There is no visitor for {type(expression)}')


def case_to_cil_visitor(case):
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
        labels.append(add_local())

    value = None

    for i, branch in enumerate(case.case_list):
        predicate = add_local()
        body.append(cil.MinusNode(t, branch.type, predicate))
        body.append(cil.ConditionalGotoNode(predicate, labels[i]))
        body.append(cil.AssignNode(branch.id, expr_cil.value))
        branch_cil = expression_to_cil_visitor(
            branch.expr)
        body += branch_cil.body
        value = branch_cil.value
        body.append(cil.LabelNode(labels[i]))

    return CIL_block(body, value)


def assign_to_cil_visitor(assign):
    expr = expression_to_cil_visitor(assign.expr)
    value = [add_local()]
    body = expr.body + [cil.AssignNode(assign.id, expr.value)]
    return CIL_block(body, value)


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

    label_1 = add_local()
    label_2 = add_local()
    value = add_local()

    body = [cil.ConditionalGotoNode(predicate.value, label_1)] + else_expression.body + [
        cil.AssignNode(value, else_expression.value), cil.GotoNode(label_2), cil.LabelNode(label_1)] + then.body + [
        cil.AssignNode(value, then.value), cil.LabelNode(label_2)]

    return CIL_block(body, value)


def loop_to_cil_visitor(loop):
    predicate = expression_to_cil_visitor(loop.cond)

    loop_block = expression_to_cil_visitor(loop.body)

    value = add_local()

    loop_label = add_local()
    end_label = add_local()

    body = [cil.ConditionalGotoNode(predicate.value, loop_label), cil.GotoNode(end_label),
            cil.LabelNode(loop_label)] + loop_block.body + [cil.LabelNode(end_label), cil.AssignNode(value, 0)]

    return CIL_block(body, value)


def equal_to_cil_visitor(equal):
    l = expression_to_cil_visitor(equal.lvalue)
    r = expression_to_cil_visitor(equal.rvalue)

    cil_result = add_local()
    end_label = add_local()
    value = add_local()

    body = l.body + r.body + [cil.MinusNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(
                                  cil_result, end_label), cil.AssignNode(value, 1),
                              cil.LabelNode(end_label)]

    return CIL_block(body, value)


def lessthan_to_cil_visitor(lessthan):
    l = expression_to_cil_visitor(lessthan.lvalue)
    r = expression_to_cil_visitor(lessthan.rvalue)

    cil_result = add_local()
    end_label = add_local()
    value = add_local()

    body = l.body + r.body + [cil.DivNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(
                                  cil_result, end_label), cil.AssignNode(value, 1),
                              cil.LabelNode(end_label)]

    return CIL_block(body, value)


def lesseqthan_to_cil_visitor(lessthan):
    l = expression_to_cil_visitor(lessthan.lvalue)
    r = expression_to_cil_visitor(lessthan.rvalue)

    cil_less = add_local()
    cil_equal = add_local()
    eq_label = add_local()
    end_label = add_local()
    value = add_local()

    body = l.body + r.body + [cil.DivNode(l.value, r.value, cil_less), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(
                                  cil_less, eq_label), cil.AssignNode(value, 1),
                              cil.GotoNode(end_label), cil.LabelNode(eq_label),
                              cil.MinusNode(l.value, r.value, cil_equal), cil.ConditionalGotoNode(
                                  cil_equal, end_label),
                              cil.AssignNode(value, 1), cil.LabelNode(end_label)]

    return CIL_block(body, value)


def integer_to_cil_visitor(integer):
    return CIL_block([], integer.value)


def bool_to_cil_visitor(bool):
    return CIL_block([], 1) if bool.value == 'true' else CIL_block([], 0)


def id_to_cil_visitor(id):
    return CIL_block([], id.id)


def new_to_cil_visitor(new_node):
    value = add_local()
    t=new_node.type
    body=[]
    
    if t=='SELF_TYPE':
        t, need_typeof=get_typeof(t,'self')
        if need_typeof:
            body.append(cil.TypeOfNode(t,'self'))
            
    body.append(cil.AllocateNode(t, value))
    init_attr = TypesByName[t].get_all_attributes()
    

    for attr in init_attr:
        if attr.expression:
            attr_cil = expression_to_cil_visitor(
                attr.expression)
            body+=attr_cil.body
            body.append(cil.SetAttrNode(value, attr.id, attr_cil.value))

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
            body.append(cil.AssignNode(attr.id, attr_cil.value))

    expr_cil = expression_to_cil_visitor(let.expr)
    body += expr_cil.body

    return CIL_block(body, expr_cil.value)


def logic_not_to_cil_visitor(not_node):
    expr_cil = expression_to_cil_visitor(
        not_node.val)

    value = add_local()
    end_label = add_local()

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
    lp_ast.NegationNode: not_to_cil_visitor
}


class CIL_block:
    def __init__(self, body, value):
        self.body = body
        self.value = value
