import ast as ast
from type_defined import *
from string_data_visitor import *
from cil_ast import *
from semantic import *

TYPES = {}
DATA = {}
CODE = []
MAX_PARAM_COUNT = 0
MAX_LOCAL_COUNT = 2
STRINGCODE = ""
MAIN_LOCAL = None

def generate_cil(ast):
    global TYPES, DATA, CODE, T_LOCALS, CILCODE
    CILCODE = generate_all(ast)
    return [TYPES, DATA, CODE, MAX_LOCAL_COUNT, MAX_PARAM_COUNT, CILCODE]


def generate_all(ast):
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

    global TYPES

    for key in ast.keys():
        if key == "SELF_TYPE":
            continue

        attributes_owner = ast[key].get_attribute_owner()
        attributes = ast[key].get_attributes_as_dict()
        methods_owner = ast[key].get_method_owner()
        new_type = TypeNode(key, attributes_owner, attributes, methods_owner)
        TYPES[key] = new_type

        result += new_type.GetCode() + "\n\n"

    return result


def generate_cil_data(ast):
    global DATA

    result = ""
    vis = FormatVisitorS()
    data = {}

    for val in ast.values():
        for attr in val.attributes.values():
            if attr.attribute_name != "self" and attr.expression:
                for s in vis.visit(attr.expression):
                    data[s] = s.lex
        for method in val.methods.values():
            if method.expression:
                for s in vis.visit(method.expression):
                    data[s] = s.lex

    i = 0
    for s in data.values():
        new_data = DataNode("data_" + str(i), s)
        DATA[s] = new_data
        result += new_data.GetCode() + "\n"
        i += 1

    result += "\n"
    return result


def generate_cil_code(ast):
    result = ""

    Main_class_attributes = []

    result += generate_built_in_functions()

    for types in ast.values():
        if types.name == "Object" or types.name == "IO" or types.name == "String":
            continue
        if types.name == "Main":
            for a in types.attributes.values():
                if a.attribute_name == "self":
                    continue
                Main_class_attributes += [[a.attribute_type.name, a.attribute_name, a.expression]]
        for method in types.methods.values():
            result += generate_function(types.name, method)

    global F_PARAM, F_LOCALS, LABEL_COUNTER, D_LOCALS, V_TYPE, CURR_TYPE, C_ATTRIBUTES, LET_LOCALS, MAIN_LOCAL
    C_ATTRIBUTES = {}
    F_LOCALS = {}
    D_LOCALS = {}
    V_TYPE = {}
    LET_LOCALS = {}
    CURR_TYPE = ""
    statements = []
    F_PARAM = {}

    Main_instance = get_local()
    MAIN_LOCAL = Main_instance
    result_local = get_local()

    main_func = FunctionNode('main', [], [], 
                [AllocateNode("Main", Main_instance.id)])

    F_LOCALS["self"] = Main_instance

    for a in Main_class_attributes:
        res = get_local()
        if a[0] == "String":

            if a[2] != None:
                inst = convert_expression(a[2])
                main_func.body += inst.node
                main_func.body += [SetAttributeNode("Main", Main_instance.id, a[1], inst.result.id)]
            else:
                main_func.body += [AllocateNode("String", res.id), 
                                   SetStringNode(res.id, ""),
                                   SetAttributeNode("Main", Main_instance.id, a[1], res.id)]
        elif a[0] == "Int":
            if a[2] != None:
                inst = convert_expression(a[2])
                main_func.body += inst.node
                main_func.body += [SetAttributeNode("Main", Main_instance.id, a[1], inst.result.id)]
            else:
                main_func.body += [AllocateNode("Int", res.id), 
                                   SetAttributeNode("Main", Main_instance.id, a[1], res.id)]
        elif a[0] == "Bool":
            if a[2] != None:
                inst = convert_expression(a[2])
                main_func.body += inst.node
                main_func.body += [SetAttributeNode("Main", Main_instance.id, a[1], inst.result.id)]
            else:
                main_func.body += [AllocateNode("Bool", res.id), 
                                   SetAttributeNode("Main", Main_instance.id, a[1], res.id)]
        else:
            if a[2] != None:
                inst = convert_expression(a[2])
                main_func.body += inst.node
                main_func.body += [SetAttributeNode("Main", Main_instance.id, a[1], inst.result.id)]
            else:
                main_func.body += [AllocateNode(a[0], res.id), 
                                   SetAttributeNode("Main", Main_instance.id, a[1], res.id)]
    
    Main_type_local = get_local()


    main_func.body += [LocalSaveNode(), ArgNode(Main_instance.id), 
                       AllocateNode("Int", Main_type_local.id),
                       TypeOfNode(Main_type_local.id, Main_instance.id),
                       DispatchCallNode(Main_type_local.id, "main", result_local.id)]

    global MAX_LOCAL_COUNT
    MAX_LOCAL_COUNT = max(len(F_LOCALS), MAX_LOCAL_COUNT)

    _locals = F_LOCALS.copy()
    locals_aux = []
    for key in _locals.keys():
        locals_aux += [_locals[key]]

    main_func.locals = locals_aux

    global CODE

    CODE.append(main_func)

    result += main_func.GetCode() + "\n\n"

    return result


def get_local():
    
    global F_LOCALS, F_PARAM, MAX_LOCAL_COUNT

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


def generate_built_in_functions():
    code = [FunctionNode("IO_out_string", [ParamNode('self'), ParamNode('str')], [], 
                [PrintNode('str'),
                ReturnNode('self')]),

            FunctionNode('IO_out_int', [ParamNode('self'), ParamNode('int')], [],
                [PrintIntNode('int'),
                ReturnNode('self')]),

            FunctionNode('IO_in_string', [ParamNode('self')], [get_local()], 
                [AllocateNode("String", 'local_0'),
                ReadNode('local_0'),
                ReturnNode('local_0')]),

            FunctionNode('IO_in_int', [ParamNode('self')], [get_local()], 
                [AllocateNode("Int", "local_0"),
                ReadIntNode('local_0'),
                ReturnNode('local_0')]),

            FunctionNode('Object_type_name', [ParamNode('self')], [get_local(), get_local()],
                [AllocateNode("Int", "local_0"),
                AllocateNode("String", "local_1"),
                TypeOfNode('local_0', 'self'),
                TypeNameNode("local_1", "local_0"),
                ReturnNode("local_1")]),

            # en el CopyNode no hace falta hacer allocate en memoria
            # para local_4 ya que esto se hace en ejecucion y depende
            # del tipo de self
            FunctionNode('Object_copy', [ParamNode('self')], [get_local()], 
                [CopyNode('self', 'local_0'),
                ReturnNode('local_0')]),

            FunctionNode('String_length', [ParamNode('self')], [get_local()], 
                [AllocateNode("Int", "local_0"),
                StrlenNode('self', 'local_0'),
                ReturnNode('local_0')]),

            FunctionNode('String_concat', [ParamNode('self'), ParamNode('str')], [get_local()],
                [AllocateNode("String", "local_0"),
                StrcatNode('self', 'str', 'local_0'),
                ReturnNode('local_0')]),

            FunctionNode('String_substr', [ParamNode('self'), ParamNode('from'), ParamNode('to')], [get_local()], 
                [AllocateNode("String", "local_0"),
                StrsubNode('self', 'from', 'to', 'local_0'),
                ReturnNode('local_0')]),

            FunctionNode("Object_abort", [ParamNode('self')], [get_local()], 
                [AllocateNode("Int", 'local_0'), 
                TypeOfNode('local_0', 'self'), 
                AbortNode('local_0')])]

    global MAX_PARAM_COUNT
    MAX_PARAM_COUNT += 18

    global CODE
    CODE = CODE + code

    result = ""
    for f in code:
        result += f.GetCode() + "\n\n"

    return result



C_ATTRIBUTES = {}
F_PARAM = {}
F_LOCALS = {}
LET_LOCALS = {}
CASE_LOCALS = {}
D_LOCALS = {}
V_TYPE = {}
CURR_TYPE = ""
LABEL_COUNTER = 0


class Node_Result:
    def __init__(self, node, result):
        self.node = node
        self.result = result


def generate_function(type_name, method):
    result = ""

    f_name = type_name + "_" + method.name

    global MAX_LOCAL_COUNT, F_PARAM, F_LOCALS, LABEL_COUNTER, D_LOCALS, V_TYPE, CURR_TYPE, C_ATTRIBUTES, LET_LOCALS
    C_ATTRIBUTES = {}
    F_LOCALS = {}
    D_LOCALS = {}
    V_TYPE = {}
    LET_LOCALS = {}
    CURR_TYPE = type_name
    statements = []
    F_PARAM = {}
    CASE_LOCALS = {}

    parameters = [ParamNode("self")]
    F_PARAM["self"] = ParamNode("self")
    for p in method.args_names:
        node = ParamNode(p)
        parameters.append(node)
        F_PARAM[node.id] = node

    for attr in AllTypes[type_name].get_attributes_as_dict().values():
        C_ATTRIBUTES[attr.attribute_name] = attr

    instruction = convert_expression(method.expression)
    statements += instruction.node

    statements.append(ReturnNode(instruction.result.id))

    MAX_LOCAL_COUNT = max(len(F_LOCALS), MAX_LOCAL_COUNT)

    _locals = F_LOCALS.copy()
    locals_aux = []
    for key in _locals.keys():
        locals_aux += [_locals[key]]

    global MAX_PARAM_COUNT
    MAX_PARAM_COUNT += len(parameters)

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


################################### PENDIENTE ##############################################
def convert_case(case):
    nodes = []
    expr = convert_expression(case.expression)
    nodes += expr.node
    expr_type_local = get_local()
    nodes += [AllocateNode("String", expr_type_local.id), TypeOfNode(expr_type_local.id, expr.result.id)]

    case_types = []
    case_labels = []

    for c in case.body:
        lcl = get_local()
        nodes += [AllocateNode("String", lcl.id), SetStringNode(lcl.id, c.typeName)]
        case_types.append(lcl)
        case_labels.append(get_label())

    result = get_local()

    for i, case_branch in enumerate(case.body):
        predicate = get_local()
        nodes.append(AllocateNode("Bool", predicate.id))
        nodes.append(IsSonNode(expr_type_local.id, case_types[i].id, predicate.id))
        nodes.append(IfGotoNode(predicate.id, case_labels[i]))
    
    end_label = get_label()
    nodes.append(GotoNode(end_label))

    global CASE_LOCALS

    for i, case_branch in enumerate(case.body):
        nodes.append(LabelNode(case_labels[i]))
        CASE_LOCALS[case_branch.id] = expr.result
        branch = convert_expression(case_branch.expression)
        nodes += branch.node
        nodes.append(CopyNode(branch.result.id, result.id))
        nodes.append(GotoNode(end_label))

    # Aqui iria el error por no irse por ninguna rama

    nodes.append(LabelNode(end_label))

    return Node_Result(nodes, result)

############################################################################################

def convert_assign(assign):
    global C_ATTRIBUTES, CURR_TYPE, MAIN_LOCAL, LET_LOCALS, F_PARAM

    expr = convert_expression(assign.expression)

    if assign.id in LET_LOCALS:
        node = expr.node + [MovNode(LET_LOCALS[assign.id].id, expr.result.id)]

        return Node_Result(node, LET_LOCALS[assign.id])

    if assign.id in F_PARAM:
        node = expr.node + [MovNode(F_PARAM[assign.id].id, expr.result.id)]

        return Node_Result(node, F_PARAM[assign.id])

    if CURR_TYPE == "":
        node = expr.node + [SetAttributeNode("Main", MAIN_LOCAL.id, assign.id, expr.result.id)]
        return Node_Result(node, expr.result)

    if assign.id in C_ATTRIBUTES:
        node = expr.node + [SetAttributeNode(CURR_TYPE, "self", assign.id, expr.result.id)]
        return Node_Result(node, expr.result)
    else:
        node = expr.node
        return Node_Result(node, expr.result)


def convert_binary_arithmetic_operation(op):
    left = convert_expression(op.left)
    right = convert_expression(op.right)

    node = []

    result = get_local()

    node = left.node + right.node + [AllocateNode("Int", result.id)]

    if type(op) == ast.PlusNode:
        node.append(AddNode(left.result.id, right.result.id, result.id))

    elif type(op) == ast.MinusNode:
        node.append(SubNode(left.result.id, right.result.id, result.id))

    elif type(op) == ast.TimesNode:
        node.append(MulNode(left.result.id, right.result.id, result.id))

    elif type(op) == ast.DivideNode:
        node.append(DivNode(left.result.id, right.result.id, result.id))

    return Node_Result(node, result)


def convert_conditional(expression):
    predicate = convert_expression(expression.evalExpr)

    if_expr = convert_expression(expression.ifExpr)

    else_expr = convert_expression(expression.elseExpr)

    label_if = get_label()
    label_else = get_label()

    result = get_local()

    node =  predicate.node + [
            IfGotoNode(predicate.result.id, label_if)] + else_expr.node + [
            MovNode(result.id, else_expr.result.id),
            GotoNode(label_else),
            LabelNode(label_if)] + if_expr.node + [
            MovNode(result.id, if_expr.result.id), LabelNode(label_else)]

    return Node_Result(node, result)


def convert_loop(loop):

    predicate = convert_expression(loop.evalExpr)

    expr = convert_expression(loop.loopExpr)

    predicate_label = get_label()
    expr_label = get_label()
    end_label = get_label()

    result = get_local()

    node = [AllocateNode("void", result.id), LabelNode(predicate_label)] + predicate.node + [
        IfGotoNode(predicate.result.id, expr_label),
        GotoNode(end_label),
        LabelNode(expr_label)] + expr.node + [
               GotoNode(predicate_label),
               LabelNode(end_label)]

    return Node_Result(node, result)


def convert_equal(equal):
    left = convert_expression(equal.left)
    right = convert_expression(equal.right)

    result = get_local()

    node = [AllocateNode("Bool", result.id)] + left.node + right.node + [ENode(left.result.id, right.result.id, result.id)]

    return Node_Result(node, result)


def convert_less(l):
    left = convert_expression(l.left)
    right = convert_expression(l.right)

    result = get_local()

    node = [AllocateNode("Bool", result.id)] + left.node + right.node + [LNode(left.result.id, right.result.id, result.id)]

    return Node_Result(node, result)


def convert_less_equal(le):
    left = convert_expression(le.left)
    right = convert_expression(le.right)

    result = get_local()

    node = [AllocateNode("Bool", result.id)] + left.node + right.node + [LENode(left.result.id, right.result.id, result.id)]

    return Node_Result(node, result)


def convert_integer(integer):
    result = get_local()
    
    nodes = [AllocateNode("Int", result.id), MovNode(result.id, int(integer.lex))]
    
    return Node_Result(nodes, result)


def convert_bool(bool):
    result = get_local()
    
    if bool.lex == "true":
        val = 1
    else:
        val = 0
    
    nodes = [AllocateNode("Bool", result.id), MovNode(result.id, val)]

    return Node_Result(nodes, result)


def convert_variable(id):
  
    global LET_LOCALS, F_PARAM, C_ATTRIBUTES, CURR_TYPE, MAIN_LOCAL, CASE_LOCALS

    if id.lex in CASE_LOCALS:
        return Node_Result([], CASE_LOCALS[id.lex])

    if id.lex in LET_LOCALS:
        return Node_Result([], LET_LOCALS[id.lex])

    if id.lex in F_PARAM:
        return Node_Result([], F_PARAM[id.lex])

    if CURR_TYPE == "":
        result = get_local()
        nodes = [AllocateNode(AllTypes["Main"].attributes[id.lex].attribute_type.name, result.id), GetAttributeNode("Main", MAIN_LOCAL.id, id.lex, result.id)]
        return Node_Result(nodes, result)

    if id.lex in C_ATTRIBUTES:
        result = get_local()
        return Node_Result([AllocateNode(C_ATTRIBUTES[id.lex].attribute_type.name, result.id), GetAttributeNode(CURR_TYPE, "self", id.lex, result.id)], result)
    
    result = get_local()
    
    return Node_Result([AllocateNode("void", result.id)], result)



def convert_new(new_node):
    global CURR_TYPE

    result = get_local()
    nodes = []

    if new_node.typeName == "SELF_TYPE":
        if CURR_TYPE == "":
            new_node.typeName = "Main"
        else:
            new_node.typeName = CURR_TYPE

    nodes.append(AllocateNode(new_node.typeName, result.id))

    attr = AllTypes[new_node.typeName].get_attributes()
    for a in attr:
        if a.attribute_name == "self":
            continue
        if a.expression:
            expr = convert_expression(a.expression)
            nodes += expr.node
            nodes.append(SetAttributeNode(new_node.typeName, result.id, a.attribute_name, expr.result.id))
        else:
            res = get_local()
            if a.attribute_type.name == "String":
                nodes.append(AllocateNode("String", res.id))
                nodes.append(SetStringNode(res.id, ""))
                nodes.append(SetAttributeNode(new_node.typeName, result.id, a.attribute_name, res.id))
            elif a.attribute_type.name == "Int":
                nodes.append(AllocateNode("Int", res.id))
                nodes.append(SetAttributeNode(new_node.typeName, result.id, a.attribute_name, res.id))
            elif a.attribute_type.name == "Bool":
                nodes.append(AllocateNode("Bool", res.id))
                nodes.append(SetAttributeNode(new_node.typeName, result.id, a.attribute_name, res.id))
            else:
                nodes.append(AllocateNode(a.attribute_type.name, res.id))
                nodes.append(SetAttributeNode(new_node.typeName, result.id, a.attribute_name, res.id))

    return Node_Result(nodes, result)


def convert_string(s):
    global DATA
    in_data = DATA[s.lex]

    already_loaded = False
    result = None
    if in_data in D_LOCALS:
        already_loaded = True
        result = D_LOCALS[in_data]
    else:
        result = get_local()
        D_LOCALS[in_data] = result

    if not already_loaded:
        node = [AllocateNode("String", result.id), LoadDataNode(result.id, DATA[s.lex].id)]
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
            nodes.append(AllocateNode(attr.typeName, local.id))
            nodes.append(MovNode(local.id, a.result.id))
            LET_LOCALS[attr.id] = local
        else:
            local = get_local()
            nodes.append(AllocateNode(attr.typeName, local.id))
            LET_LOCALS[attr.id] = local

    expr = convert_expression(let.expression)
    nodes += expr.node

    return Node_Result(nodes, expr.result)


def convert_complement(complement_node):
    expr = convert_expression(complement_node.expression)

    result = get_local()

    node = [AllocateNode("Int", result.id)] + expr.node + [CmpNode(expr.result.id, result.id)]

    return Node_Result(node, result)


def convert_not(not_node):
    expr = convert_expression(not_node.expression)

    result = get_local()

    node = [AllocateNode("Bool", result.id)] + expr.node + [NtNode(expr.result.id, result.id)]

    return Node_Result(node, result)


def convert_is_void(isvoid):
    expr = convert_expression(isvoid.expression)

    result = get_local()

    node = expr.node + [AllocateNode("Bool", result.id), VDNode(expr.result.id, result.id)]

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
        instance = ins.result.id
    else:

        if CURR_TYPE == "":
            global MAIN_LOCAL
            instance = MAIN_LOCAL.id
        else:
            global F_PARAM
            instance = F_PARAM["self"].id

    arguments = []

    for a in call.args:
        arg = convert_expression(a)
        nodes += arg.node
        arguments.append(arg.result)

    nodes += [LocalSaveNode()]

    nodes.append(ArgNode(instance))

    for a in arguments:
        nodes.append(ArgNode(a.id))

    result = get_local()

    ins_type = get_local()
    nodes += [AllocateNode("Int", ins_type.id)]

    if not call.dispatchType: 
        nodes += [TypeOfNode(ins_type.id, instance)]
        nodes.append(DispatchCallNode(ins_type.id, call.function, result.id))
    else:
        nodes.append(TypeAddressNode(ins_type.id, call.dispatchType))
        nodes.append(DispatchCallNode(ins_type.id, call.function, result.id))

    return Node_Result(nodes, result)

