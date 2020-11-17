import ast
from type_defined import *
from data_visitor import *
from cil_ast import *
from semantic import *

TYPES = []
DATA = []
CODE = []

def generate_code(ast):
    cil = generate_cil(ast)
    #mips = generate_mips()
    #return cil, mips
    return cil

def generate_cil(ast):
    result = "TYPES -->\n\n"
    result += generate_cil_types(ast)
    result += "END <--\n\n"
    
    result += "DATA -->\n\n"
    result += generate_cil_data(ast)
    result += "END <--\n\n"
    
    result += "CODE -->\n\n"
    result += generate_cil_code(ast)
    result += "END <--"

    return result


def generate_cil_types(ast):
    result = ""

    for key in ast.keys():
        if key == "SELF_TYPE":
            continue
        
        attributes = ast[key].get_attribute_owner()
        methods = ast[key].get_method_owner()
        new_type = TypeNode(key, attributes, methods)
        TYPES.append(new_type)
        
        result += new_type.GetCode() + "\n\n"

    return result
        

def generate_cil_data(ast):
    result = ""
    vis = FormatVisitor()
    data = {}
    for val in ast.values():
        for attr in val.attributes.values():
            if attr.attribute_name != "self" and attr.expression:
                for s in vis.visit(attr.expression):
                    data[s] = s.lex
        for method in val.methods.values():
            if method.expression:
                for s in vis.visit(method.expression):
                    data[s] = s.lex[0:-1]

    i = 0
    for s in data.values():
        new_data = DataNode("data_" + str(i), s)
        DATA.append(new_data)
        result += new_data.GetCode() + "\n"
        i += 1

    result += "\n"  
    return result 


def generate_cil_code(ast):
    result = generate_built_in_functions()
    
    for types in ast.values():
        if types.name == "Object" or types.name == "IO" or types.name == "String":
            continue
        for method in types.methods.values():
            result += generate_function(types.name, method)

    return result

def generate_built_in_functions():
    code = [FunctionNode("IO_out_string", [ParamNode('self'), ParamNode('str')], [], [PrintNode('str'), 
                                                                                      ReturnNode('self')]),

            FunctionNode('IO_out_int', [ParamNode('self'), ParamNode('int')], [LocalNode('str')], [StrNode('int', 'str'), 
                                                                                                   PrintNode('str'), 
                                                                                                   ReturnNode('self')]),

            FunctionNode('IO_in_string', [ParamNode('self')], [LocalNode('str')], [ReadNode('str'), 
                                                                                   ReturnNode('str')]),

            FunctionNode('IO_in_int', [ParamNode('self')], [LocalNode('int')], [ReadIntNode('int'), 
                                                                                ReturnNode('int')]),

            FunctionNode('Object_type_name', [ParamNode('self')], [LocalNode('type'), LocalNode('str')], [TypeOfNode('type', 'self'), 
                                                                                                          StrNode('type', 'str'),
                                                                                                          ReturnNode('str')]),

            FunctionNode('Object_copy', [ParamNode('self')], [LocalNode('copy')], [CopyNode('self', 'copy'), 
                                                                                   ReturnNode('copy')]),

            FunctionNode('String_length', [ParamNode('self')], [LocalNode('result')], [LengthNode('self', 'result'), 
                                                                                       ReturnNode('result')]),

            FunctionNode('String_concat', [ParamNode('self'), ParamNode('str')], [LocalNode('result')], [ConcatNode('self', 'str', 'result'), 
                                                                                                       ReturnNode('result')]),

            FunctionNode('String_substr', [ParamNode('self'), ParamNode('from'), ParamNode('to')], [LocalNode('result')], [SubStringNode('self', 'from', 'to', 'result'), 
                                                                                                                           ReturnNode('result')])
            ]

    CODE = [] + code

    result = ""
    for f in code:
        result += f.GetCode() + "\n\n"
    
    return result


C_ATTRIBUTES = {}
F_LOCALS = {}
D_LOCALS = {}
V_TYPE = {}
CURR_TYPE = []
LABEL_COUNTER = 0


def create_local(id = None):
    if id is None:
        id = "local_" + len(F_LOCALS)

    local = LocalNode(id)
    F_LOCALS[id] = local
    return local

def create_label():
    LABEL_COUNTER += 1
    return "label_" + str(LABEL_COUNTER)

class Node_Result:
    def __init__(self, node, result):
        self.node = node
        self.result = result

def generate_function(type_name, method):
    result = ""

    f_name = type_name + "_" + method.name

    parameters = [ParamNode("self")]
    for p in method.args_names:
        parameters.append(ParamNode(p))

    result += "\t" + f_name + " {\n"
    for p in parameters:
        result += "\t\t" + p.GetCode() + "\n" 

    F_LOCALS = {}
    LABEL_COUNTER = 0
    D_LOCALS = {}
    V_TYPE = {}
    CURR_TYPE = [f_name]

    statements = []

    instruction = convert_expression(method.expression)
    statements += instruction.node

    statements.append(ReturnNode(instruction.value))

    _locals = F_LOCALS.copy()
    locals_aux = []
    for key in _locals.keys():
        locals_aux += _locals[key]

    CODE.append(FunctionNode(f_name, parameters, locals_aux, statements))

    return result

def convert_expression(expression):
    if type(expression) is AssignStatementNode:
        convert_assign(expression)

    elif type(expression) is ConditionalStatementNode:
        convert_conditional(expression)

    elif type(expression) is LoopStatementNode:
        convert_loop(expression)

    elif type(expression) is BlockStatementNode:
        convert_block(expression)

    elif type(expression) is LetStatementNode:
        convert_let(expression)

    elif type(expression) is CaseStatementNode:
        convert_case(expression)

    elif type(expression) is CaseBranchNode:
        convert_case_branch(expression)

    elif type(expression) is NewStatementNode:
        convert_new(expression)

    elif type(expression) is FunctionCallStatement:
        convert_function_call(expression)

    elif type(expression) is ConstantNumericNode:
        convert_integer(expression)

    elif type(expression) is ConstantStringNode:
        convert_string(expression)

    elif type(expression) is ConstantBoolNode:
        convert_bool(expression)

    elif type(expression) is VariableNode:
        convert_variable(expression)

    elif type(expression) is NotNode:
        convert_not(expression)

    elif type(expression) is IsVoidNode:
        convert_is_void(expression)

    elif type(expression) is ComplementNode:
        convert_complement(expression)

    elif type(expression) is LessEqualNode:
        convert_less_equal(expression)

    elif type(expression) is LessNode:
        convert_less(expression)

    elif type(expression) is EqualNode:
        convert_equal(expression)

    elif type(expression) is PlusNode:
        convert_binary_arithmetic_operation(expression)

    elif type(expression) is MinusNode:
        convert_binary_arithmetic_operation(expression)

    elif type(expression) is TimesNode:
        convert_binary_arithmetic_operation(expression)

    elif type(expression) is DivideNode:
        convert_binary_arithmetic_operation(expression)

def convert_case(case):
    nodes = []
    expr = convert_expression(case.expr)
    nodes += expr.node
    aux_local = create_local()
    nodes.append(TypeOfNode(aux_local, expr.result))
    expr_type_local = create_local()
    nodes.append(StrNode(aux_local, expr_type_local))
    
    case_types = []
    case_labels = []
    
    for c in case.body:
        case_types.append(create_local())
        case_labels.append(create_label())
        
    result = None

    for i, case_branch in enumerate(case.body):
        predicate = create_local()
        nodes.append(MinusNode(expr_type_local, case_types[i], predicate))
        nodes.append(ConditionalGotoNode(predicate, case_labels[i]))
        case_local = create_local(case_branch.id)
        nodes.append(AssignNode(case_local, expr.result))
        branch = convert_expression(case_branch.expr)
        nodes += branch.node
        result = branch.result
        nodes.append(LabelNode(case_labels[i]))

    return Node_Result(nodes, result)


def convert_assign(assign):        
    expr = convert_expression(assign.expression)

    if assign.id in C_ATTRIBUTES[CURR_TYPE[-1]]:
        node = expr.node + [SetAttrNode("self", assign.id, expr.result)]
        return Node_Result(node, expr.result)

    else:
        result = create_local(assign.id)
        node = node.node + [AssignNode(result, expr.result)]
        return Node_Result(node, result)


def convert_binary_arithmetic_operation(op):
    left = convert_expression(op.left)
    right = convert_expression(op.right)

    result = create_local()

    node = left.node + right.node

    if type(op) == ast.PlusNode:
        node.append(PlusNode(left.result, right.result, result))

    elif type(op) == ast.MinusNode:
        node.append(MinusNode(left.result, right.result, result))

    elif type(op) == ast.StarNode:
        node.append(StarNode(left.result, right.result, result))

    elif type(op) == ast.DivNode:
        node.append(DivNode(left.result, right.result, result))

    return Node_Result(node, result)


def convert_conditional(expression):
    predicate = convert_expression(expression.evalExpr)

    if_expr = convert_expression(expression.ifExpr)

    else_expr = convert_expression(expression.elseExpr)

    label_if = create_label()
    label_else = create_label()
    result = create_local()

    node = predicate.node + [
           ConditionalGotoNode(predicate.result, label_if)] + 
           else_expr.node + [
           AssignNode(result, else_expr.result), 
           GotoNode(label_else), 
           LabelNode(label_if)] + 
           if_expr.node + [
           AssignNode(result, if_expr.result), cil.LabelNode(label_else)]

    return Node_Result(node, result)


def convert_loop(loop):
    predicate = convert_expression(loop.evalExpr)

    expr = convert_expression(loop.loopExpr)

    result = add_local()

    predicate_label = create_label()
    expr_label = create_label()
    end_label = create_label()

    node = [LabelNode(predicate_label)] + 
            predicate.node + 
            [ConditionalGotoNode(predicate.result, expr_label), 
            GotoNode(end_label),
            LabelNode(expr_label)] + 
            expr.node + [
            GotoNode(predicate_label),
            LabelNode(end_label), 
            AssignNode(result, 0)]

    return Node_Result(node, result)


def convert_equal(equal):
    left = convert_expression(equal.left)
    right = convert_expression(equal.right)

    sus_result = create_local()
    end_label = create_label()
    result = create_local()

    node = left.node + right.node + [MinusNode(left.result, r.result, sus_result), 
                                     AssignNode(result, 0),
                                     ConditionalGotoNode(sus_result, end_label), 
                                     AssignNode(result, 1),
                                     LabelNode(end_label)]

    return Node_Result(node, result)


def convert_less(l):
    left = convert_expression(l.left)
    right = convert_expression(l.right)

    result = create_local()
    
    node = left.node + right.node + [LessNode(left.result, right.result, result)]
    
    return Node_Result(node, result)


def convert_less_equal(le):
    left = convert_expression(le.left)
    right = convert_expression(le.right)

    result = create_local()
    
    node = left.node + right.node + [LessEqualNode(left.result, right.result, result)]
    
    return Node_Result(node, result)


def convert_integer(integer):
    return Node_Result([], int(integer.lex))


def convert_bool(bool):
    if bool.lex == "True":
        return Node_Result([], 1)
    else:
        return Node_Result([], 0)


def convert_id(id):
    if id.lex in C_ATTRIBUTES[CURR_TYPE[-1]]:
        result = create_local()
        return Node_Result([GetAttributeNode("self", id.lex, result)], result)

    try:
        result = F_LOCALS[id.lex]
        return Node_Result([], result)

    except:
        return Node_Result([], id.lex)

def convert_new(new_node):
    result = create_local()
    nodes = []

    if new_node.typeName == "SELF_TYPE":
        if new_node.typeName not in V_TYPE:
            type_local = create_local()
            V_TYPE[new_node.typeName] = type_local
            if need_typeof:
                nodes.append(TypeOfNode(new_node.typeName, "self"))

    nodes.append(AllocateNode(new_node.typeName, result))
    
    attr = AllTypes[new_node.typeName].get_attributes()
    for a in attr:
        if a.expression:
            expr = convert_expression(a.expression)
            nodes += expr.node
            nodes.append(SetAttrNode(result, a.id, expr.result))

    return Node_Result(nodes, result)


def convert_is_void(isvoid):
    expr = convert_expression(isvoid.expression)

    node = expr.node

    if not expr.value:
        return Node_Result(node, 1)
    else:
        return Node_Result(node, 0)


def convert_string(s):
    in_data = DATA[s]

    already_loaded = False
    result = None
    if in_data in D_LOCALS:
        already_loaded = True
        result = D_LOCALS[in_data]
    else:
        result = create_local()
        D_LOCALS[in_data] = result

    if already_loaded:
        node = [LoadNode(in_data, result)]
    else:
        node = []

    return CIL_block(node, result)


def convert_let(let):
    nodes = []

    for attr in let.variables:
        if attr.expression:
            a = convert_expression(attr.expression)
            nodes += a.node
            local = create_local(attr.id)
            nodes.append(AssignNode(local, a.result))

    expr = convert_expression(let.expression)
    nodes += expr.node

    return Node_Result(nodes, expr.result)


def convert_complement(complement_node):
    expr = convert_expression(complement_node.expression)

    result = create_local()
    end_label = create_label()

    node = expr.node + [AssignNode(result, 0), 
                        ConditionalGotoNode(expr.result, end_label),
                        AssignNode(result, 1), LabelNode(end_label)]

    return Node_Result(node, result)


def convert_not(not_node):
    expr = convert_expression(not_node.expression)

    result = create_local()

    node = expr.body + [NotNode(expr.value, value)]

    return Node_Result(node, expr)


def convert_block(block):
    nodes = []
    result = None

    for e in block.expressions:
        expr = convert_expression(e)
        nodes += expr.body
        result = expr.value

    return Node_Result(nodes, result)


def convert_function_call(call):
    nodes = []

    if call.instance:
        ins = convert_expression(call.instance)
        nodes += ins.node
        instance = ins.result
    else:
        instance = "self"

    arguments = []

    for a in call.args:
        arg = convert_expression(a)
        nodes += a.node
        arguments.append(arg.result)

    def get_typeof(obj):
        try:
            return __TYPEOF__[obj], False
        except KeyError:
            type_local = add_local()
            __TYPEOF__[obj] = type_local
            return type_local, True

    t, need_typeof = get_typeof(instance)
    
    if instance in V_TYPE:
        ins_type = V_TYPE[instance]
    else:
        local = create_local()
        V_TYPE[instance] = local
        nodes.append(TypeOfNode(local, instance))

    nodes.append(ArgNode(instance))

    for a in arguments:
        nodes.append(ArgNode(a))

    result = create_local()
    if not call.dispatchType:
        nodes.append(VCAllNode(ins_type, call.function, result))
    else:
        nodes.append(VCAllNode(call.dispatchType, call.function, result))

    return Node_Result(nodes, result)


def generate_mips():
    pass