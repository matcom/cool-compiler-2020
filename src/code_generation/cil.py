import lexer_parser.ast as lp_ast
from semantic.types import *
import code_generation.ast as cil


def ast_to_cil(ast):
    if type(ast) == lp_ast.ProgramNode:
        return program_to_cil_visitor(ast)
    raise Exception(f'AST root must be program')


def program_to_cil_visitor(program):
    types = []
    data = []
    code = []

    # completing .TYPE section
    for t in TypesByName:
        _type = cil.TypeNode(t)
        value = TypesByName[t]
        for attr in value.get_all_attributes():
            _type.attributes.append(attr.id)

        for met in value.get_all_inherited_methods():
            _type.methods[met.id] = met.owner

        for met in value.get_all_self_methods():
            _type.methods[met.id] = t

        types.append(_type)

        # completing .CODE and .DATA sections
    for c in program.classes:
        for f in c.features:
            if type(f) == DefFuncNode:
                if f.id == 'main' and c.name == 'Main':
                    fun = func_to_cil_visitor(c.name, f)
                    code.insert(0, fun[0])
                    data.append(fun[1])
                else:
                    fun = func_to_cil_visitor(c.name, f)
                    code.append(fun[0])
                    data.append(fun[1])

    return cil.ProgramNode(types, data, code)


def func_to_cil_visitor(type_name, func):
    name = f'{type_name}_{func.id}'
    params = [cil.ParamNode('self')]
    params += [cil.ParamNode(id) for (id, t) in func.params]
    locals = []
    body = []
    data = []
    locals_count = 0

    if type_name == 'Main' and func.id == 'main':
        instance = '__main__'
        locals.append(cil.LocalNode(instance))
        body.append(cil.AllocateNode('Main', instance))

        init_attr = TypesByName['Main'].get_all_attributes()
        for attr in init_attr:
            if attr.expression:
                attr_cil = expression_to_cil_visitor(attr.expression, locals_count)
                locals_count += len(attr_cil.locals)
                locals.append(attr_cil.locals)
                body.append(attr_cil.body)
                data.append(attr_cil.data)
                body.append(cil.SetAttrNode(instance, attr.id, attr_cil.value))

    for exp in func.expressions:
        instruction = expression_to_cil_visitor(exp, locals_count)
        locals += instruction.locals
        body += instruction.body
        data += instruction.data
        locals_count += len(instruction.locals)

    return cil.FuncNode(name, params, locals, body), data


def expression_to_cil_visitor(expression, locals_count):
    try:
        return __visitor__[type(expression)](expression, locals_count)
    except:
        raise Exception(f'There is no visitor for {type(expression)}')
    
def case_to_cil_visitor(case, locals_count):
    locals=[]
    body=[]
    data=[]
    expr_cil=expression_to_cil_visitor(case.expr, locals_count)
    locals_count+=len(expr_cil.locals)
    locals+=expr_cil.locals
    body+=expr_cil.body
    data+=expr_cil.data
    t=f'local_{locals_count}'
    locals_count+=1
    locals.append(cil.LocalNode(t))
    body.append(cil.TypeOfNode(t, expr_cil.value))
    types=[]
    labels=[]
    for c in case.case_list:
        types.append(c.type)
        
    for l in range(len(case.case_list)):
        labels.append(f'local_{locals_count}')
        locals_count+=1
              
    value=None
    
    for i, branch in enumerate(case.case_list):
        predicate=f'local_{locals_count}'
        locals_count+=1
        locals+=[cil.LocalNode(predicate), cil.LocalNode(branch.id)]
        body.append(cil.MinusNode(t, branch.type, predicate))
        body.append(cil.ConditionalGotoNode(predicate, labels[i]))
        body.append(cil.AssignNode(branch.id, expr_cil.value))
        branch_cil=expression_to_cil_visitor(branch.expr, locals_count)
        locals+=branch_cil.locals
        body+=branch_cil.body
        data+=branch_cil.data
        locals_count+=len(branch_cil.locals)
        value=branch_cil.value
        body.append(cil.LabelNode(labels[i]))
        
    return CIL_block(locals, body, value, data)
        
        
        


def assign_to_cil_visitor(assign, locals_count):
    expr = expression_to_cil_visitor(assign.expr, locals_count)
    locals_count += len(expr.locals)
    value = [f'local_{locals_count}']
    locals = expr.locals + [cil.LocalNode(value)]
    body = expr.body + [cil.AssignNode(assign.id, expr.value)]
    return CIL_block(locals, body, value, expr.data)


def arith_to_cil_visitor(arith, locals_count):
    l = expression_to_cil_visitor(arith.lvalue, locals_count)
    r = expression_to_cil_visitor(arith.rvalue, locals_count)
    locals_count += len(l.locals) + len(r.locals)

    cil_result = f'local_{locals_count}'

    locals = l.locals + r.locals + [cil.LocalNode(cil_result)]
    body = l.body + r.body
    data = l.data + r.data

    if type(arith) == lp_ast.PlusNode:
        body.append(cil.PlusNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.MinusNode:
        body.append(cil.MinusNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.StarNode:
        body.append(cil.StarNode(l.value, r.value, cil_result))
    elif type(arith) == lp_ast.DivNode:
        body.append(cil.DivNode(l.value, r.value, cil_result))

    return CIL_block(locals, body, cil_result, data)


def if_to_cil_visitor(_if, locals_count):
    predicate = expression_to_cil_visitor(_if.if_expr, locals_count)
    locals_count += len(predicate.locals)

    then = expression_to_cil_visitor(_if.then_expr, locals_count)
    locals_count += len(then.locals)

    else_expression = expression_to_cil_visitor(_if.else_expr, locals_count)
    locals_count += len(else_expression.locals)

    label_1 = f'local_{locals_count}'
    label_2 = f'local_{locals_count + 1}'
    value = f'local_{locals_count + 2}'

    locals = predicate.locals + then.locals + else_expression.locals + [cil.LocalNode(value)]
    body = [cil.ConditionalGotoNode(predicate.value, label_1)] + else_expression.body + [
        cil.AssignNode(value, else_expression.value), cil.GotoNode(label_2), cil.LabelNode(label_1)] + then.body + [
               cil.AssignNode(value, then.value), cil.LabelNode(label_2)]
    data = predicate.data + then.data + else_expression.data

    return CIL_block(locals, body, value, data)


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
            cil.LabelNode(loop_label)] + loop_block.body + [cil.AssignNode(value, loop_block.value),
                                                            cil.LabelNode(end_label)]
    data = predicate.data + loop_block.data

    return CIL_block(locals, body, value, data)


def equal_to_cil_visitor(equal, locals_count):
    l = expression_to_cil_visitor(equal.lvalue, locals_count)
    r = expression_to_cil_visitor(equal.rvalue, locals_count)
    locals_count += len(l.locals) + len(r.locals)

    cil_result = f'local_{locals_count}'
    end_label = f'local_{locals_count + 1}'
    value = f'local_{locals_count + 2}'

    locals = l.locals + r.locals + [cil.LocalNode(cil_result), cil.LocalNode(value)]
    body = l.body + r.body + [cil.MinusNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(cil_result, end_label), cil.AssignNode(value, 1),
                              cil.LabelNode(end_label)]
    data = l.data + r.data

    return CIL_block(locals, body, value, data)


def lessthan_to_cil_visitor(lessthan, locals_count):
    l = expression_to_cil_visitor(lessthan.lvalue, locals_count)
    r = expression_to_cil_visitor(lessthan.rvalue, locals_count)
    locals_count += len(l.locals) + len(r.locals)

    cil_result = f'local_{locals_count}'
    end_label = f'local_{locals_count + 1}'
    value = f'local_{locals_count + 2}'

    locals = l.locals + r.locals + [cil.LocalNode(cil_result), cil.LocalNode(value)]
    body = l.body + r.body + [cil.DivNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(cil_result, end_label), cil.AssignNode(value, 1),
                              cil.LabelNode(end_label)]
    data = l.data + r.data

    return CIL_block(locals, body, value, data)


def lesseqthan_to_cil_visitor(lessthan, locals_count):
    l = expression_to_cil_visitor(lessthan.lvalue, locals_count)
    r = expression_to_cil_visitor(lessthan.rvalue, locals_count)
    locals_count += len(l.locals) + len(r.locals)

    cil_less = f'local_{locals_count}'
    cil_equal = f'local_{locals_count + 1}'
    eq_label = f'local_{locals_count + 2}'
    end_label = f'local_{locals_count + 3}'
    value = f'local_{locals_count + 4}'

    locals = l.locals + r.locals + [cil.LocalNode(cil_less), cil.LocalNode(cil_equal), cil.LocalNode(value)]
    body = l.body + r.body + [cil.DivNode(l.value, r.value, cil_less), cil.AssignNode(value, 0),
                              cil.ConditionalGotoNode(cil_less, eq_label), cil.AssignNode(value, 1),
                              cil.GotoNode(end_label), cil.LabelNode(eq_label),
                              cil.MinusNode(l.value, r.value, cil_equal), cil.ConditionalGotoNode(cil_equal, end_label),
                              cil.AssignNode(value, 1), cil.LabelNode(end_label)]
    data = l.data + r.data

    return CIL_block(locals, body, value, data)


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
    data = []
    init_attr = TypesByName[new_node.type].get_all_attributes()

    for attr in init_attr:
        if attr.expression:
            attr_cil = expression_to_cil_visitor(attr.expression, locals_count)
            locals_count += len(attr_cil.locals)
            locals.append(attr_cil.locals)
            body.append(attr_cil.body)
            data.append(attr_cil.data)
            body.append(cil.SetAttrNode(value, attr.id, attr_cil.value))

    return CIL_block(locals, body, value, data)


def string_to_cil_visitor(str, locals_count):
    str_addr = f'local_{locals_count}'
    str_id = f'local_{locals_count + 1}'

    locals = [cil.LocalNode(str_id)]
    data = [cil.DataNode(str_addr, str.value)]
    body = [cil.LoadNode(str_addr, str_id)]

    return CIL_block(locals, body, str_id, data)


def let_to_cil_visitor(let, locals_count):
    body = []
    locals = []
    data = []
    for attr in let.let_attr:
        attr_cil = expression_to_cil_visitor(attr, locals_count)
        locals_count += len(attr_cil.locals)
        body.append(cil.AssignNode(attr.id, attr_cil.value))
        body += attr_cil.body
        locals += attr_cil.locals
        data += attr_cil.data

    expr_cil = expression_to_cil_visitor(let.expr, locals_count)
    locals += expr_cil.locals
    body += expr_cil.locals
    data += expr_cil.data

    return CIL_block(locals, body, expr_cil.value, data)


def logic_not_to_cil_visitor(not_node, locals_count):
    expr_cil = expression_to_cil_visitor(not_node.val, locals_count)
    locals_count += len(expr_cil.locals)

    value = f'local_{locals_count}'
    end_label = f'local_{locals_count + 1}'

    locals = expr_cil.locals + [cil.LocalNode(value)]
    body = expr_cil.body + [cil.AssignNode(value, 0), cil.ConditionalGotoNode(expr_cil.value, end_label),
                            cil.AssignNode(value, 1), cil.LabelNode(end_label)]

    return CIL_block(locals, body, value, expr_cil.data)


def block_to_cil_visitor(block, locals_count):
    locals = []
    body = []
    data = []
    value = None

    for expr in block.expressions:
        expr_cil = expression_to_cil_visitor(expr, locals_count)
        locals_count += len(expr_cil.locals)
        locals += expr_cil.locals
        body += expr_cil.body
        data += expr_cil.data
        value = expr_cil.value

    return CIL_block(locals, body, value, data)

def case_to_cil_visitor(case, locals_count):
    pass

def func_call_to_cil_visitor(call, locals_count):
    locals = []
    body = []
    data = []
    if call.object:
        obj_cil = expression_to_cil_visitor(call.object, locals_count)
        locals_count += len(obj_cil.locals)
        locals += obj_cil.locals
        body += obj_cil.body
        data += obj_cil.data
        obj=obj_cil.value
    else:
        obj='self'

    arg_values = []

    for arg in call.args:
        arg_cil = expression_to_cil_visitor(arg, locals_count)
        locals_count += len(arg_cil.locals)
        locals += arg_cil.locals
        body += arg_cil.body
        data += arg_cil.data
        arg_values.append(arg_cil.value)
        
    t=f'local_{locals_count}'
    locals.append(cil.LocalNode(t))
    body.append(cil.TypeOfNode(t, obj))

    body.append(cil.ArgNode(obj))

    for arg in arg_values:
        body.append(cil.ArgNode(arg))

    result = f'local_{locals_count+1}'
    locals.append(cil.LocalNode(result))
    if not call.type:
        body.append(cil.VCAllNode(t, call.id, result))
    else:
        body.append(cil.VCAllNode(call.type, call.id, result))

    return CIL_block(locals, body, result, data)   
    


class CIL_block:
    def __init__(self, locals, body, value, data=[]):
        self.locals = locals
        self.body = body
        self.value = value
        self.data = data

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
    def __init__(self, locals, body, value, data=[]):
        self.locals = locals
        self.body = body
        self.value = value
        self.data = data
