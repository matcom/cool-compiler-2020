import ast as ast
from type_defined import *
from data_visitor import *
from cil_ast import *
from semantic import *

TYPES = []
DATA = {}
CODE = []
CILCODE = ""




def generate_code(ast):
    cil = generate_cil(ast)
    # mips = generate_mips()
    # return cil, mips
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
    global DATA
    result = ""
    vis = FormatVisitor()
    data = {}
    for val in ast.values():
        for attr in val.attributes.values():
            if attr.attribute_name != "self" and attr.expression:
                for s in vis.visit(attr.expression):
                    if len(s.lex) == 1:
                        s.lex = "\\n\n"
                    data[s] = s.lex[0:-1]
        for method in val.methods.values():
            if method.expression:
                for s in vis.visit(method.expression):
                    if len(s.lex) == 1:
                        s.lex = "\\n\n"
                    data[s] = s.lex[0:-1]

    i = 0
    for s in data.values():
        new_data = DataNode("data_" + str(i), s)
        DATA[s] = new_data
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
    main_instance = "local_0"
    main_result = "local_1"
    code = [FunctionNode("IO_out_string", [ParamNode('self'), ParamNode('str')], [], [PrintNode('str'),
                                                                                      ReturnNode('self')]),

            FunctionNode('IO_out_int', [ParamNode('self'), ParamNode('int')], [LocalNode('str')],
                         [ToStrNode('int', 'str'),
                          PrintNode('str'),
                          ReturnNode('self')]),

            FunctionNode('IO_in_string', [ParamNode('self')], [LocalNode('str')], [ReadNode('str'),
                                                                                   ReturnNode('str')]),

            FunctionNode('IO_in_int', [ParamNode('self')], [LocalNode('int')], [ReadIntNode('int'),
                                                                                ReturnNode('int')]),

            FunctionNode('Object_type_name', [ParamNode('self')], [LocalNode('type'), LocalNode('str')],
                         [TypeOfNode('type', 'self'),
                          ToStrNode('type', 'str'),
                          ReturnNode('str')]),

            FunctionNode('Object_copy', [ParamNode('self')], [LocalNode('copy')], [CopyNode('self', 'copy'),
                                                                                   ReturnNode('copy')]),

            FunctionNode('String_length', [ParamNode('self')], [LocalNode('result')], [StrlenNode('self', 'result'),
                                                                                       ReturnNode('result')]),

            FunctionNode('String_concat', [ParamNode('self'), ParamNode('str')], [LocalNode('result')],
                         [StrcatNode('self', 'str', 'result'),
                          ReturnNode('result')]),

            FunctionNode('String_substr', [ParamNode('self'), ParamNode('from'), ParamNode('to')],
                         [LocalNode('result')], [StrsubNode('self', 'from', 'to', 'result'),
                                                 ReturnNode('result')]),
            FunctionNode('Program_entry', [], [LocalNode("local_0"), LocalNode("local_1")],
                         [AllocateNode('Main', "local_0"),
                          ArgNode("local_0"),
                          DispatchCallNode('Main', 'main', "local_1")])
            ]

    CODE = [] + code

    result = ""
    for f in code:
        result += f.GetCode() + "\n\n"

    return result


C_ATTRIBUTES = {}
F_PARAM = {}
F_LOCALS = {}
LET_LOCALS = {}
D_LOCALS = {}
V_TYPE = {}
CURR_TYPE = ""
LABEL_COUNTER = 0


def get_local(id=None):
    global F_LOCALS
    if id is None:
        id = "local_" + str(len(F_LOCALS))

    if id in F_PARAM:
        return F_PARAM[id]

    local = LocalNode(id)
    F_LOCALS[id] = local
    return local


def get_label():
    global LABEL_COUNTER
    LABEL_COUNTER += 1
    return "label_" + str(LABEL_COUNTER)


class Node_Result:
    def __init__(self, node, result):
        self.node = node
        self.result = result


def generate_function(type_name, method):
    result = ""

    f_name = type_name + "_" + method.name

    global F_PARAM, F_LOCALS, LABEL_COUNTER, D_LOCALS, V_TYPE, CURR_TYPE, C_ATTRIBUTES, LET_LOCALS
    C_ATTRIBUTES = {}
    F_LOCALS = {}
    LABEL_COUNTER = 0
    D_LOCALS = {}
    V_TYPE = {}
    LET_LOCALS = {}
    CURR_TYPE = f_name
    statements = []
    F_PARAM = {}

    parameters = [ParamNode("self")]
    F_PARAM["self"] = ParamNode("self")
    for p in method.args_names:
        node = ParamNode(p)
        parameters.append(node)
        F_PARAM[node.id] = node

    for attr in AllTypes[type_name].get_attributes_as_dict().values():
        C_ATTRIBUTES[attr.attribute_name] = attr.attribute_name

    instruction = convert_expression(method.expression)
    statements += instruction.node

    statements.append(ReturnNode(instruction.result))

    _locals = F_LOCALS.copy()
    locals_aux = []
    for key in _locals.keys():
        locals_aux += [_locals[key]]

    CODE.append(FunctionNode(f_name, parameters, locals_aux, statements))

    result += CODE[-1].GetCode() + "\n\n"

    return result


def convert_expression(expression):
    if type(expression) is AssignStatementNode:
        return convert_assign(expression)

    elif type(expression) is ConditionalStatementNode:
        return convert_conditional(expression)

    elif type(expression) is LoopStatementNode:
        return convert_loop(expression)

    elif type(expression) is BlockStatementNode:
        return convert_block(expression)

    elif type(expression) is LetStatementNode:
        return convert_let(expression)

    elif type(expression) is CaseStatementNode:
        return convert_case(expression)

    elif type(expression) is CaseBranchNode:
        return convert_case_branch(expression)

    elif type(expression) is NewStatementNode:
        return convert_new(expression)

    elif type(expression) is FunctionCallStatement:
        return convert_function_call(expression)

    elif type(expression) is ConstantNumericNode:
        return convert_integer(expression)

    elif type(expression) is ConstantStringNode:
        return convert_string(expression)

    elif type(expression) is ConstantBoolNode:
        return convert_bool(expression)

    elif type(expression) is VariableNode:
        return convert_variable(expression)

    elif type(expression) is NotNode:
        return convert_not(expression)

    elif type(expression) is IsVoidNode:
        return convert_is_void(expression)

    elif type(expression) is ComplementNode:
        return convert_complement(expression)

    elif type(expression) is LessEqualNode:
        return convert_less_equal(expression)

    elif type(expression) is LessNode:
        return convert_less(expression)

    elif type(expression) is EqualNode:
        return convert_equal(expression)

    elif type(expression) is PlusNode:
        return convert_binary_arithmetic_operation(expression)

    elif type(expression) is MinusNode:
        return convert_binary_arithmetic_operation(expression)

    elif type(expression) is TimesNode:
        return convert_binary_arithmetic_operation(expression)

    elif type(expression) is DivideNode:
        return convert_binary_arithmetic_operation(expression)


def convert_case(case):
    nodes = []
    expr = convert_expression(case.expression)
    nodes += expr.node
    aux_local = get_local()
    nodes.append(TypeOfNode(aux_local, expr.result))
    expr_type_local = get_local()
    nodes.append(ToStrNode(aux_local, expr_type_local))

    case_types = []
    case_labels = []

    for c in case.body:
        case_types.append(get_local())
        case_labels.append(get_label())

    result = None

    for i, case_branch in enumerate(case.body):
        predicate = get_local()
        nodes.append(SusNode(expr_type_local, case_types[i], predicate))
        nodes.append(IfGotoNode(predicate, case_labels[i]))
        case_local = get_local(case_branch.id)
        nodes.append(MovNode(case_local, expr.result))
        branch = convert_expression(case_branch.expression)
        nodes += branch.node
        result = branch.result
        nodes.append(LabelNode(case_labels[i]))

    return Node_Result(nodes, result)


def convert_assign(assign):
    global C_ATTRIBUTES
    expr = convert_expression(assign.expression)

    if assign.id in C_ATTRIBUTES:
        node = expr.node + [SetAttributeNode("self", assign.id, expr.result)]
        return Node_Result(node, expr.result)

    else:
        result = get_local(assign.id)
        node = expr.node + [MovNode(result, expr.result)]
        return Node_Result(node, result)


def convert_binary_arithmetic_operation(op):
    left = convert_expression(op.left)
    right = convert_expression(op.right)

    if type(left.result) == LocalNode:
        result = left.result
    else:
        if type(right.result) == LocalNode:
            result = right.result
        else:
            result = get_local()

    node = left.node + right.node

    if type(op) == ast.PlusNode:
        node.append(AddNode(left.result, right.result, result))

    elif type(op) == ast.MinusNode:
        node.append(SusNode(left.result, right.result, result))

    elif type(op) == ast.TimesNode:
        node.append(MulNode(left.result, right.result, result))

    elif type(op) == ast.DivideNode:
        node.append(DivNode(left.result, right.result, result))

    return Node_Result(node, result)


def convert_conditional(expression):
    predicate = convert_expression(expression.evalExpr)

    if_expr = convert_expression(expression.ifExpr)

    else_expr = convert_expression(expression.elseExpr)

    label_if = get_label()
    label_else = get_label()
    result = get_local()

    node = predicate.node + [IfGotoNode(predicate.result, label_if)] + else_expr.node + [
        MovNode(result, else_expr.result),
        GotoNode(label_else),
        LabelNode(label_if)] + if_expr.node + [
               MovNode(result, if_expr.result), LabelNode(label_else)]

    return Node_Result(node, result)


def convert_loop(loop):
    predicate = convert_expression(loop.evalExpr)

    expr = convert_expression(loop.loopExpr)

    predicate_label = get_label()
    expr_label = get_label()
    end_label = get_label()

    node = [LabelNode(predicate_label)] + predicate.node + [
        IfGotoNode(predicate.result, expr_label),
        GotoNode(end_label),
        LabelNode(expr_label)] + expr.node + [
               GotoNode(predicate_label),
               LabelNode(end_label), ]

    return Node_Result(node, None)


def convert_equal(equal):
    left = convert_expression(equal.left)
    right = convert_expression(equal.right)

    result = get_local()

    node = left.node + right.node + [ENode(left.result, right.result, result)]

    return Node_Result(node, result)


def convert_less(l):
    left = convert_expression(l.left)
    right = convert_expression(l.right)

    result = get_local()

    node = left.node + right.node + [LNode(left.result, right.result, result)]

    return Node_Result(node, result)


def convert_less_equal(le):
    left = convert_expression(le.left)
    right = convert_expression(le.right)

    result = get_local()

    node = left.node + right.node + [LENode(left.result, right.result, result)]

    return Node_Result(node, result)


def convert_integer(integer):
    return Node_Result([], int(integer.lex))


def convert_bool(bool):
    if bool.lex == "true":
        return Node_Result([], 1)
    else:
        return Node_Result([], 0)


def convert_variable(id):
    global F_LOCALS, C_ATTRIBUTES, LET_LOCALS, F_PARAM

    if id.lex in LET_LOCALS:
        return Node_Result([], LET_LOCALS[id.lex])

    if id.lex in F_PARAM:
        return Node_Result([], F_PARAM[id.lex])

    if id.lex in C_ATTRIBUTES:
        result = get_local()
        return Node_Result([GetAttributeNode("self", id.lex, result)], result)

    return Node_Result([], get_local(id.lex))


def convert_new(new_node):
    result = get_local()
    nodes = []

    if new_node.typeName == "SELF_TYPE":
        new_node.typeName = CURR_TYPE

    nodes.append(AllocateNode(new_node.typeName, result))

    attr = AllTypes[new_node.typeName].get_attributes()
    for a in attr:
        if a.attribute_name == "self":
            continue
        if a.expression:
            expr = convert_expression(a.expression)
            nodes += expr.node
            nodes.append(SetAttributeNode(result, a.attribute_name, expr.result))
        else:
            nodes.append(SetAttributeNode(result, a.attribute_name, 0))

    return Node_Result(nodes, result)


def convert_string(s):
    global DATA
    in_data = DATA[s.lex[0:-1]]

    already_loaded = False
    result = None
    if in_data in D_LOCALS:
        already_loaded = True
        result = D_LOCALS[in_data]
    else:
        result = get_local()
        D_LOCALS[in_data] = result

    if not already_loaded:
        node = [LoadNode(DATA[s.lex[0:-1]].id, result)]
    else:
        node = []

    return Node_Result(node, result)


def convert_let(let):
    global LET_LOCALS
    nodes = []

    for attr in let.variables:
        if attr.expression:
            a = convert_expression(attr.expression)
            nodes += a.node
            local = get_local()
            nodes.append(MovNode(local, a.result))
            LET_LOCALS[attr.id] = local

    expr = convert_expression(let.expression)
    nodes += expr.node

    return Node_Result(nodes, expr.result)


def convert_complement(complement_node):
    expr = convert_expression(complement_node.expression)

    result = get_local()

    node = expr.node + [CmpNode(expr.result, result)]

    return Node_Result(node, result)


def convert_not(not_node):
    expr = convert_expression(not_node.expression)

    result = get_local()

    node = expr.node + [NtNode(expr.result, result)]

    return Node_Result(node, result)


def convert_is_void(isvoid):
    expr = convert_expression(isvoid.expression)

    result = get_local()

    if type(expr.result == ParamNode):
        e = expr.result.id
    else:
        e = expr.result

    node = expr.node + [VDNode(e, result)]

    return Node_Result(node, result)


def convert_block(block):
    nodes = []
    result = None

    for e in block.expressions:
        expr = convert_expression(e)
        nodes += expr.node
        result = expr.result

    return Node_Result(nodes, result)


def convert_function_call(call):
    global V_TYPE, CURR_TYPE
    nodes = []

    instance_is_self = type(call.instance) == VariableNode and call.instance.lex == "self"

    if not instance_is_self:
        ins = convert_expression(call.instance)
        nodes += ins.node
        instance = ins.result
    else:
        instance = "self"

    if type(instance) == ParamNode or type(instance) == LocalNode:
        instance = instance.id

    arguments = []

    for a in call.args:
        arg = convert_expression(a)
        nodes += arg.node
        arguments.append(arg.result)

    if instance in V_TYPE:
        ins_type = V_TYPE[instance]
    else:
        type_local = get_local()
        V_TYPE[instance] = type_local
        ins_type = type_local
        nodes.append(TypeOfNode(type_local, instance))

    nodes.append(ArgNode(instance))

    for a in arguments:
        nodes.append(ArgNode(a))

    result = get_local()
    if not call.dispatchType:
        nodes.append(DispatchCallNode(ins_type, call.function, result))
    else:
        nodes.append(DispatchCallNode(call.dispatchType, call.function, result))

    return Node_Result(nodes, result)

