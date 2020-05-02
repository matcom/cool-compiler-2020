import lexer_parser.ast as lp_ast


from types import TypesByName
import code_generation.ast as cil

def program_to_cil_visitor(program):
    types=[]
    data=[]
    code=[]
    #build program node with each section
    return cil.ProgramNode(types, data, code)
                
def func_to_cil_visitor(type_name, func):    
    name=f'{type_name}_{func.id}'
    params=[cil.ParamNode(id) for (id, t) in func.params]
    locals=[]
    body=[]
    locals_count=0
    for exp in func.expressions:
        instruction=expression_to_cil_visitor(exp, locals_count)
        locals.append(instruction.locals)
        body.append(instruction.body)
        locals_count+=len(instruction.locals)
        
    return cil.FuncNode(name, params, locals, body)
              
def expression_to_cil_visitor(expression, locals_count):
    try:
        return __visitor__[type(expression)](expression, locals_count)
    except:
        raise Exception(f'There is no visitor for {type(expression)}')

def assign_to_cil_visitor(assign, locals_count):
    expr=expression_to_cil_visitor(assign.expr, locals_count)
    locals_count+=len(expr.locals)
    value=[f'local_{locals_count}']
    locals=expr.locals+[cil.LocalNode(value)]
    body=expr.body+[cil.AssignNode(assign.id, expr.value)]
    return CIL_block(locals, body, value, expr.data)

def arith_to_cil_visitor(arith, locals_count):
    
    l=expression_to_cil_visitor(arith.lvalue, locals_count)
    r=expression_to_cil_visitor(arith.rvalue, locals_count)
    locals_count+=len(l.locals)+len(r.locals)
    
    cil_result=f'local_{locals_count}'
    
    locals=l.locals+r.locals+[cil.LocalNode(cil_result)]
    body=l.body+r.body
    data=l.data+r.data
    
    if type(arith)==lp_ast.PlusNode:
        body.append(cil.PlusNode(l.value, r.value, cil_result))
    elif type(arith)==lp_ast.MinusNode:
        body.append(cil.MinusNode(l.value, r.value, cil_result))
    elif type(arith)==lp_ast.StarNode:
        body.append(cil.StarNode(l.value, r.value, cil_result))
    elif type(arith)==lp_ast.DivNode:
        body.append(cil.DivNode(l.value, r.value, cil_result))
      
    return CIL_block(locals, body, cil_result, data)
    
def if_to_cil_visitor(_if, locals_count):
    predicate=expression_to_cil_visitor(_if.if_expr, locals_count)
    locals_count+=len(predicate.locals)
    
    then=expression_to_cil_visitor(_if.then_expr, locals_count)
    locals_count+=len(then.locals)
    
    else_expression=expression_to_cil_visitor(_if.else_expr, locals_count)
    locals_count+=len(else_expression.locals)
        
    label_1=f'local_{locals_count}'
    label_2=f'local_{locals_count+1}'
    value=f'local_{locals_count+2}'

    locals=predicate.locals+then.locals+else_expression.locals+[cil.LocalNode(value)]
    body=[cil.ConditionalGotoNode(predicate.value, label_1)]+else_expression.body+[cil.AssignNode(value, else_expression.value),cil.GotoNode(label_2),cil.LabelNode(label_1)]+then.body+[cil.AssignNode(value, then.value),cil.LabelNode(label_2)]
    data=predicate.data+then.data+else_expression.data
    
    return CIL_block(locals, body, value, data)
    
def loop_to_cil_visitor(loop, locals_count):
    predicate=expression_to_cil_visitor(loop.cond, locals_count)
    locals_count+=len(predicate.locals)
    
    loop_block=expression_to_cil_visitor(loop.body, locals_count)
    locals_count+=len(loop_block.locals)
    
    value=f'local_{locals_count}'

    locals=predicate.locals+loop_block.locals+[cil.LocalNode(value)]
    
    loop_label=f'local_{locals_count+1}'
    end_label=f'local_{locals_count+2}'
    
    body=[cil.ConditionalGotoNode(predicate.value, loop_label), cil.GotoNode(end_label), cil.LabelNode(loop_label)]+loop_block.body+[cil.AssignNode(value, loop_block.value) ,cil.LabelNode(end_label)]
    data=predicate.data+loop_block.data
    
    return CIL_block(locals, body, value, data)

def equal_to_cil_visitor(less_than, locals_count):
    l=expression_to_cil_visitor(arith.lvalue, locals_count)
    r=expression_to_cil_visitor(arith.rvalue, locals_count)
    locals_count+=len(l.locals)+len(r.locals)
    
    cil_result=f'local_{locals_count}'
    end_label=f'local_{locals_count+1}'
    value=f'local_{locals_count+2}'
    
    locals=l.locals+r.locals+[cil.LocalNode(cil_result), cil.LocalNode(value)]
    body=l.body+r.body+[cil.MinusNode(l.value, r.value, cil_result), cil.AssignNode(value, 0),cil.ConditionalGotoNode(cil_result, end_label), cil.AssignNode(value, 1), cil.LabelNode(end_label)]
    data=l.data+r.data
    
    return CIL_block(locals, body, value, data)
       
def integer_to_cil_visitor(integer, locals_count):
    return CIL_block([], [], integer.value)

def bool_to_cil_visitor(bool, locals_count):
    return CIL_block([], [], 1) if bool=='true' else CIL_block([], [], 0)

def id_to_cil_visitor(id, locals_count):
    return CIL_block([], [], id.id)

def new_to_cil_visitor(new_node, locals_count):
    value=f'local_{locals_count}'
    body=[cil.AllocateNode(new_node.type, value)]
    locals=[cil.LocalNode(value)]
    return CIL_block(locals, body, value)

def string_to_cil_visitor(str, locals_count):
    str_addr=f'local_{locals_count}'
    str_id=f'local_{locals_count+1}'
    
    locals=[cil.LocalNode(str_id)]
    data=[cil.DataNode(str_addr, str.value)]
    body=[cil.LoadNode(str_addr, str_id)]
    
    return CIL_block(locals, body, str_id, data)

def let_to_cil_visitor(let, locals_count):
    body=[]
    locals=[]
    data=[]
    for attr in let.let_attr:
        attr_cil=expression_to_cil_visitor(attr, locals_count)
        locals_count+=len(attr_cil.locals)
        body.append(cil.AssignNode(attr.id, attr_cil.value))
        body+=attr_cil.body
        locals+=attr_cil.locals
        data+=attr_cil.data
    
    expr_cil=expression_to_cil_visitor(let.expr, locals_count)
    locals+=expr_cil.locals
    body+=expr_cil.locals
    data+=expr_cil.data
    
    return CIL_block(locals, body, expr_cil.value, data)
        
def logic_not_to_cil_visitor(not_node, locals_count):
    expr_cil=expression_to_cil_visitor(not_node.val, locals_count)
    locals_count+=len(expr_cil.locals)
    
    value=f'local_{locals_count}'
    end_label=f'local_{locals_count + 1}'
    
    
    locals=expr_cil.locals+[cil.LocalNode(value)]
    body=expr_cil.body+[cil.AssignNode(value, 0), cil.ConditionalGotoNode(expr_cil.value, end_label), cil.AssignNode(value, 1), cil.LabelNode(end_label)]
    
    return CIL_block(locals, body, value, expr_cil.data)

def block_to_cil_visitor(block, locals_count):
    locals=[]
    body=[]
    data=[]
    value=None
    
    for expr in block.expressions:
        expr_cil=expression_to_cil_visitor(expr, locals_count)
        locals_count+=len(expr_cil.locals)
        locals+=expr_cil.locals
        body+=expr_cil.body
        data+=expr_cil.data
        value=expr_cil.value
    
    return CIL_block(locals, body, value, data)
            
class CIL_block:
    def __init__(self, locals, body, value, data=[]):
        self.locals=locals
        self.body=body
        self.value=value
        self.data=data
  
  
__visitor__={
    lp_ast.AssignNode:assign_to_cil_visitor,
    lp_ast.BlockNode:block_to_cil_visitor,
    lp_ast.BoolNode:bool_to_cil_visitor,
    lp_ast.IfNode:if_to_cil_visitor,
    lp_ast.WhileNode:loop_to_cil_visitor,
    lp_ast.EqNode:equal_to_cil_visitor,
    lp_ast.LogicNegationNode:logic_not_to_cil_visitor,
    lp_ast.LetNode:let_to_cil_visitor,
    lp_ast.NewNode:new_to_cil_visitor,
    lp_ast.IntNode:integer_to_cil_visitor,
    lp_ast.StringNode:string_to_cil_visitor,
    lp_ast.PlusNode:arith_to_cil_visitor,
    lp_ast.MinusNode:arith_to_cil_visitor,
    lp_ast.StarNode:arith_to_cil_visitor,
    lp_ast.DivNode:arith_to_cil_visitor, 
    lp_ast.VarNode:id_to_cil_visitor   
}      
    
    
    
            
            
            
        
        
        
        
    


    