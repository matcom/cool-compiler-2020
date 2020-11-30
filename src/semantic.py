from ast import *
from graph import Graph
from type_defined import AllTypes, CoolType, object_type, BasicTypes


def check_type_declaration(ast: ProgramNode):
    for cls in ast.classes:
        if cls.typeName in BasicTypes:
            return f'({cls.getLineNumber()}, {cls.getColumnNumber()}) - SemanticError: Redefinition of basic class {cls.typeName}.'
        if cls.typeName in AllTypes:
            return f'({cls.getLineNumber()}, {cls.getColumnNumber()}) - SemanticError: Classes may not be redefined'

        AllTypes[cls.typeName] = CoolType(cls.typeName, None)
    return []


def check_type_inheritance(ast: ProgramNode):
    for cls in ast.classes:
        if cls.fatherTypeName:
            if cls.fatherTypeName in AllTypes:
                father_type = AllTypes[cls.fatherTypeName]
                if father_type.inherit:
                    if not (father_type.name == cls.typeName):
                        AllTypes[cls.typeName].parent_type = father_type
                    else:
                        return f"({cls.getLineNumber()}, {cls.getColumnNumber()}) - SemanticError: Class {cls.typeName}, " \
                               f"or an ancestor of {cls.typeName}, is involved in an inheritance cycle"
                else:
                    return f'({cls.getLineNumber()}, {cls.getColumnNumber()}) - SemanticError: Class {cls.typeName} ' \
                           f'cannot inherit class {father_type.name}.'
            else:
                return f"({cls.getLineNumber()}, {cls.getColumnNumber()}) - TypeError: Class {cls.typeName} " \
                       f"inherits from an undefined class {cls.fatherTypeName}. "
        else:
            AllTypes[cls.typeName].parent_type = object_type

    return []


def check_features(ast: ProgramNode):
    checked_types = [False for _ in ast.classes]
    created_types_names = [cls.typeName for cls in ast.classes]
    left_check = len(checked_types)

    while left_check > 0:
        for i, cls in enumerate(ast.classes):
            if checked_types[i]:
                continue

            if cls.fatherTypeName:
                # If father is in created types, then check if father is also checked
                if cls.fatherTypeName in created_types_names:
                    # If father not checked
                    if not checked_types[created_types_names.index(cls.fatherTypeName)]:
                        continue
                # Else is in Basic types. so can continue checking

            class_type = AllTypes[cls.typeName]
            class_type.add_attribute("self", class_type.name, "self")
            for feature in cls.features:
                if type(feature) is FunctionFeatureNode:
                    parameters_type = []
                    parameters_name = []
                    for arg in feature.parameters:
                        if arg.id == 'self':
                            return f'({arg.getLineNumber()}, {arg.getColumnNumber()}) - SemanticError: \'self\' ' \
                                   f'cannot be the name of a formal parameter.'
                        parameters_name.append(arg.id)
                        parameters_type.append(arg.typeName)
                    method_added = class_type.add_method(feature.id, parameters_type, parameters_name, feature.typeName,
                                                         feature.statement)
                    if len(method_added) == 2:
                        return f'({feature.parameters[method_added[1]].getLineNumber()}, ' \
                               f'{feature.parameters[method_added[1]].getColumnNumber()}) ' \
                               f'{method_added[0]}'
                    elif len(method_added) == 1:
                        return f'({feature.getLineNumber()}, ' \
                               f'{feature.getColumnNumber()}) ' \
                               f'{method_added[0]}'
                    continue
                if type(feature) is AttributeFeatureNode:
                    if feature.id == 'self':
                        return f'({feature.getLineNumber()}, {feature.getColumnNumber()}) - SemanticError: \'self\' ' \
                               f'cannot be the name of an attribute.'
                    feature_added_error = class_type.add_attribute(feature.id, feature.typeName, feature.expression)
                    if len(feature_added_error) == 1:
                        return f'({feature.getLineNumber()}, {feature.getColumnNumber()}) {feature_added_error[0]}'
                    elif len(feature_added_error) == 2:
                        # TODO Update column
                        return f'({feature.getLineNumber()}, {feature.getColumnNumber() + len(feature.id) + 2}) ' \
                               f'{feature_added_error[0]}'
                    continue
                return 'Unknown attribute or Method'

            class_methods = class_type.get_self_methods()
            class_inherited_methods = class_type.get_methods_inherited()

            for k in class_methods.keys():
                if k in class_inherited_methods:
                    if class_methods[k].return_type != class_inherited_methods[k].return_type:
                        return f'({feature.getLineNumber()}, {feature.getColumnNumber()}) - SemanticError: ' \
                               f'In redefined method {feature.id}, return type {class_methods[k].return_type.name} ' \
                               f'is different from original return type {class_inherited_methods[k].return_type.name}.'
                    if len(class_methods[k].args_types) != len(class_inherited_methods[k].args_types):
                        return f'({feature.getLineNumber()}, {feature.getColumnNumber()}) - SemanticError: ' \
                               f'Incompatible number of formal parameters in redefined method {feature.id}.'
                    for counter in range(0, len(class_methods[k].args_types)):
                        if (class_methods[k].args_types[counter]).name != \
                                (class_inherited_methods[k].args_types[counter]).name:
                            return f'({feature.getLineNumber()}, {feature.getColumnNumber()}) - SemanticError: ' \
                                   f'In redefined method {feature.id}, parameter type ' \
                                   f'{class_methods[k].args_types[counter].name} is different ' \
                                   f'from original type {class_inherited_methods[k].args_types[counter].name}.'

            left_check = left_check - 1
            checked_types[i] = True

    return []


CURR_TYPE = ""

def check_expressions(ast: ProgramNode):
    global CURR_TYPE, TYPE_CHANGES

    change = False

    for cls in ast.classes:
        attrs = {}
        cls_type = AllTypes[cls.typeName]
        CURR_TYPE = cls_type.name
        attrs_type = cls_type.get_attributes()

        for attr in attrs_type:
                attrs[attr.attribute_name] = attr.attribute_type.name
        attrs["self"] = cls.typeName

        for feature in cls.features:
            if type(feature) is AttributeFeatureNode:
                feature_type = feature.typeName
                if feature.expression:
                    error, expression_type = get_expression_return_type(feature.expression, False, attrs, {}, {}, False,
                                                                            {})
                    if len(error) > 0:
                        return error
                    if expression_type != feature.typeName and not is_ancestor(AllTypes[feature_type], AllTypes[expression_type]):
                        return f'({feature.getLineNumber()}, {feature.getColumnNumber()}) - TypeError: Inferred type ' \
                                f'{expression_type} of initialization of attribute test ' \
                                f'does not conform to declared type {feature_type}.'
                        

        functions = AllTypes[cls.typeName].get_methods()

        for feature in cls.features:
            if type(feature) is FunctionFeatureNode:
                feature_type = feature.typeName

                params = { "self" : cls.typeName }
                for parameter in feature.parameters:
                    params[parameter.id] = parameter.typeName
                error, expression_type = get_expression_return_type(feature.statement, True, attrs, functions,
                                                                        params,
                                                                        False, {})

                if len(error) > 0:
                    return error
                if feature_type not in AllTypes:
                    return f'({feature.statement.getLineNumber()}, {feature.statement.getColumnNumber()}) - TypeError: ' \
                            f'Undefined return type {feature_type} in method test.'
                if not is_ancestor(AllTypes[feature_type], AllTypes[expression_type]):
                    return f'({feature.statement.getLineNumber()}, {feature.statement.getColumnNumber()}) - TypeError: ' \
                            f'Inferred return type {expression_type} of method {feature.id} does not conform to declared ' \
                            f'return type {feature_type}.'

    return []


def GetFirstCommonAncestor(types):
    result = types[0]
    for i in range(1, len(types)):
        result = AllTypes[get_first_common_ancestor(result, types[i])]

    return result.name


def get_first_common_ancestor(typeA, typeB):
    if is_ancestor(typeA, typeB):
        return typeA.name
    if is_ancestor(typeB, typeA):
        return typeB.name
    return get_first_common_ancestor(typeA.parent_type, typeB.parent_type)


def is_ancestor(olderNode, youngerNode):
    if olderNode is None or youngerNode is None:
        return False
    if olderNode.name == youngerNode.name:
        return True
    return is_ancestor(olderNode, youngerNode.parent_type)


def get_expression_return_type(expression, insideFunction, attributes, functions, parameters, insideLet, letVars,
                               insideCase=False, caseVar={}, inside_loop=False):
    if type(expression) is AssignStatementNode:
        if expression.id == 'self':
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - SemanticError: ' \
                   f'Cannot assign to \'self\'.', ''

        error1, type1 = get_expression_return_type(expression.expression, insideFunction, attributes, functions,
                                                   parameters, insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""

        if insideLet:
            if expression.id in letVars and not is_ancestor(AllTypes[letVars[expression.id]], AllTypes[type1]):
                return "Errorrrrrrrr asigning another type to a let variable"


        if insideCase:
            if expression.id in caseVar and not is_ancestor(AllTypes[caseVar[expression.id]], AllTypes[type1]):
                return "Errorrrrrrrr asigning another type to a case variable"


        if insideFunction:
            if expression.id in parameters and not is_ancestor(AllTypes[parameters[expression.id]], AllTypes[type1]):
                return "Errorrrrrrrr asigning another type to a parameter"
            if expression.id in attributes and not is_ancestor(AllTypes[attributes[expression.id]], AllTypes[type1]):
                return "Errorrrrrrrr asigning another type to an attribute"

        return [], type1


    elif type(expression) is ConditionalStatementNode:
        error1, type1 = get_expression_return_type(expression.evalExpr, insideFunction, attributes, functions,
                                                   parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: Predicate of \'if\' ' \
                   f'does not have type Bool.', ""

        error2, type2 = get_expression_return_type(expression.ifExpr, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        error3, type3 = get_expression_return_type(expression.elseExpr, insideFunction, attributes, functions,
                                                   parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error3) > 0:
            return error3, ""

        thenType = AllTypes[type2]
        elseType = AllTypes[type3]
        return [], get_first_common_ancestor(thenType, elseType)

    elif type(expression) is LoopStatementNode:
        error1, type1 = get_expression_return_type(expression.evalExpr, insideFunction, attributes, functions,
                                                   parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop=True)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return f'({expression.loopExpr.getLineNumber()}, {expression.loopExpr.getColumnNumber()}) - ' \
                   f'TypeError: Loop condition does not have type Bool.', ''
        error2, type2 = get_expression_return_type(expression.loopExpr, insideFunction, attributes, functions,
                                                   parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop=True)
        if len(error2) > 0:
            return error2, ""
        return [], "Object"

    elif type(expression) is BlockStatementNode:
        lastType = ""
        for expr in expression.expressions:
            eError, eType = get_expression_return_type(expr, insideFunction, attributes, functions, parameters,
                                                       insideLet,
                                                       letVars, insideCase, caseVar, inside_loop)
            if len(eError) > 0:
                return eError, ""
            lastType = eType

        return [], lastType

    elif type(expression) is LetStatementNode:
        letVariables = letVars
        for item in attributes.keys():
            letVars[item] = attributes[item]
        for variable in expression.variables:
            if variable.id == 'self':
                return f'({variable.getLineNumber()}, {variable.getColumnNumber()}) - SemanticError: \'self\' cannot ' \
                       f'be bound in a \'let\' expression.', ''
            if not (variable.typeName in AllTypes):
                return f"({variable.getLineNumber()}, {variable.getColumnNumber()}) - TypeError: Class " \
                       f"{variable.typeName} of let-bound identifier {variable.id} is undefined.", ""
            if variable.expression is not None:
                error0, type0 = get_expression_return_type(variable.expression, insideFunction, attributes, functions,
                                                           parameters, True, letVariables, insideCase, caseVar,
                                                           inside_loop)
                if len(error0) > 0:
                    return "Error in let variable initialization expression", ""
                if not is_ancestor(AllTypes[variable.typeName], AllTypes[type0]):
                    return f'({variable.getLineNumber()}, {variable.getColumnNumber()}) - TypeError: ' \
                           f'Inferred type {type0} of initialization of {variable.id} does not conform to ' \
                           f'identifier\'s declared type {variable.typeName}. ', ''
            letVariables[variable.id] = variable.typeName
        errorLet, typeLet = get_expression_return_type(expression.expression, insideFunction, attributes, functions,
                                                       parameters, True, letVariables, insideCase, caseVar, inside_loop)
        if len(errorLet) > 0:
            return errorLet, ""
        return [], typeLet

    elif type(expression) is CaseStatementNode:
        eError, eType = get_expression_return_type(expression.expression, insideFunction, attributes, functions,
                                                   parameters, insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(eError) > 0:
            return eError, ""
        caseBranchesTypes = []
        case_types = []
        for caseBranch in expression.body:
            for s in case_types:
                if s == caseBranch.typeName:
                    return f'({caseBranch.getLineNumber()}, {caseBranch.getColumnNumber()}) - SemanticError: Duplicate branch {caseBranch.typeName} in case statement', ""
            
            case_types.append(caseBranch.typeName)
            error0, type0 = get_expression_return_type(caseBranch, insideFunction, attributes, functions, parameters,
                                                       insideLet, letVars, insideCase, caseVar, inside_loop)
            if len(error0) > 0:
                return f'({caseBranch.getLineNumber()}, {caseBranch.getColumnNumber()}) - {error0}', ""
            
            duplicated_type = False
            for t in caseBranchesTypes:
                if t.name == type0:
                    duplicated_type = True
                    break

            if not duplicated_type:
                caseBranchesTypes.append(AllTypes[type0])

        return [], GetFirstCommonAncestor(caseBranchesTypes)

    elif type(expression) is CaseBranchNode:
        if not (expression.typeName in AllTypes):
            return f"TypeError: Class {expression.typeName} of case branch is undefined.", ""
        error0, type0 = get_expression_return_type(expression.expression, insideFunction, attributes, functions,
                                                   parameters, insideLet, letVars, True,
                                                   {expression.id: expression.typeName})
        if len(error0) > 0:
            return error0, ""

        return [], type0

    elif type(expression) is NewStatementNode:
        if expression.typeName in AllTypes:
            return [], AllTypes[expression.typeName].name
        else:
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: \'new\' used ' \
                   f'with undefined class {expression.typeName}.', ''

    elif type(expression) is FunctionCallStatement:

        e, t = get_expression_return_type(expression.instance, insideFunction, attributes, functions, parameters,
                                          insideLet, letVars, insideCase, caseVar, inside_loop)
        
        if len(e) > 0:
            return e, ""
        if expression.dispatchType is not None:
            if not (expression.dispatchType in AllTypes):
                return "Ancestor class type not defined", ""
            expType = AllTypes[t]
            ancType = AllTypes[expression.dispatchType]
            if is_ancestor(ancType, expType):
                methods = ancType.get_methods()
                if expression.function in methods:
                    if len(methods[expression.function].args_names) != len(expression.args):
                        return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - SemanticError: ' \
                               f'Method {expression.function} called with wrong number of arguments.', ''
                    i = 0
                    for arg in expression.args:
                        aError, aType = get_expression_return_type(arg, insideFunction, attributes, functions,
                                                                   parameters,
                                                                   insideLet, insideCase, caseVar, inside_loop)

                        if len(aError) > 0:
                            return aError, ""
                        if aType != ((methods[expression.function]).args_types[i]).name:
                            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: ' \
                                   f'In call of method {expression.function}, type {((methods[expression.function]).args_types[i]).name} of parameter {((methods[expression.function]).args_names[i])} ' \
                                   f'does not conform to declared type {aType}. ', ''
                        i = i + 1
                    return [], methods[expression.function].return_type.name
                else:
                    return f'({1}, {1}) - AttributeError: Dispatch to undefined method {1}.', ''

            else:
                return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: ' \
                       f'Expression type {expType.name} does not conform to declared static dispatch type ' \
                       f'{ancType.name}. ', ''


        methods = AllTypes[t].get_methods()
        if expression.function in methods:
            if len(methods[expression.function].args_names) != len(expression.args):
                return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - SemanticError: ' \
                       f'Method {expression.function} called with wrong number of arguments.', ''
            i = 0
            for arg in expression.args:
                aError, aType = get_expression_return_type(arg, insideFunction, attributes, functions, parameters,
                                                           insideLet, letVars, insideCase, caseVar, inside_loop)
                if len(aError) > 0:
                    return aError, ""
                if not is_ancestor(AllTypes[((methods[expression.function]).args_types[i]).name], AllTypes[aType]):
                    return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: ' \
                           f'In call of method {expression.function}, type {((methods[expression.function]).args_types[i]).name} of parameter {(methods[expression.function]).args_names[i]} ' \
                           f'does not conform to declared type {aType}. ', ''
                i = i + 1

            return [], methods[expression.function].return_type.name
        else:
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - AttributeError: ' \
                   f'Dispatch to undefined method {expression.function}.', ''

    elif type(expression) is ConstantNumericNode:
        return [], "Int"
    elif type(expression) is ConstantStringNode:
        return [], "String"
    elif type(expression) is ConstantBoolNode:
        return [], "Bool"

    elif type(expression) is VariableNode:
        if insideLet:
            if expression.lex in letVars:
                return [], letVars[expression.lex]
        if insideCase:
            if expression.lex in caseVar:
                return [], caseVar[expression.lex]
        if insideFunction or inside_loop:
            if expression.lex in parameters:
                return [], parameters[expression.lex]
        if expression.lex in attributes:
            return [], attributes[expression.lex]
        return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - NameError: ' \
               f'Undeclared identifier {expression.lex}.', ''

    elif type(expression) is NotNode:
        error1, type1 = get_expression_return_type(expression.expression, insideFunction, attributes, functions,
                                                   parameters, insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return f'({expression.expression.getLineNumber()}, {expression.expression.getColumnNumber()}) - TypeError: ' \
                   f'Argument of \'not\' has type {type1} instead of Bool', ''
        return [], "Bool"

    elif type(expression) is IsVoidNode:
        error1, type1 = get_expression_return_type(expression.expression, insideFunction, attributes, functions,
                                                   parameters, insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""

        return [], "Bool"

    elif type(expression) is ComplementNode:
        error1, type1 = get_expression_return_type(expression.expression, insideFunction, attributes, functions,
                                                   parameters, insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Int":
            return f'({expression.expression.getLineNumber()}, {expression.expression.getColumnNumber()}) - TypeError: Argument of \'~\' ' \
                   f'has type {type1} instead of Int', ''
        return [], "Int"

    elif type(expression) is LessEqualNode:
        error1, type1 = get_expression_return_type(expression.left, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = get_expression_return_type(expression.right, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: non-Int arguments: ' \
                   f'{type1} <= {type2}', ''
        return [], "Bool"

    elif type(expression) is LessNode:
        error1, type1 = get_expression_return_type(expression.left, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = get_expression_return_type(expression.right, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: non-Int arguments: ' \
                   f'{type1} < {type2}', ''
        return [], "Bool"

    elif type(expression) is EqualNode:
        error1, type1 = get_expression_return_type(expression.left, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = get_expression_return_type(expression.right, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        
        if type1 not in BasicTypes and type2 not in BasicTypes:
            return [], 'Bool'
        if type1 != type2:
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: ' \
                   f'Illegal comparison with a basic type.', ''
        return [], "Bool"

    elif type(expression) is PlusNode:
        error1, type1 = get_expression_return_type(expression.left, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = get_expression_return_type(expression.right, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: non-Int arguments: ' \
                   f'{type1} + {type2} ', ''
        return [], "Int"

    elif type(expression) is MinusNode:
        error1, type1 = get_expression_return_type(expression.left, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = get_expression_return_type(expression.right, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: non-Int arguments: ' \
                   f'{type1} - {type2}', ''
        return [], "Int"

    elif type(expression) is TimesNode:
        error1, type1 = get_expression_return_type(expression.left, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = get_expression_return_type(expression.right, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: non-Int arguments: ' \
                   f'{type1} * {type2}', ''
        return [], "Int"

    elif type(expression) is DivideNode:
        error1, type1 = get_expression_return_type(expression.left, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = get_expression_return_type(expression.right, insideFunction, attributes, functions, parameters,
                                                   insideLet, letVars, insideCase, caseVar, inside_loop)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return f'({expression.getLineNumber()}, {expression.getColumnNumber()}) - TypeError: non-Int arguments: ' \
                   f'{type1} / {type2}', ''
        return [], "Int"


def get_cyclic_class(graph: Graph, ast: ProgramNode):
    for cls in ast.classes:
        if not graph.visited[graph.vertex_id.index(cls.typeName)]:
            nodes = graph.graph[cls.typeName]
            for cls2 in ast.classes:
                if cls2.typeName == nodes[0]:
                    return f"({cls2.getLineNumber()}, {cls2.getColumnNumber()}) - SemanticError: Class {cls2.typeName}, " \
                           f"or an ancestor of {cls2.typeName}, is involved in an inheritance cycle"
            return f"({cls.getLineNumber()}, {cls.getColumnNumber()}) - SemanticError: Class {cls.typeName}, " \
                   f"or an ancestor of {cls.typeName}, is involved in an inheritance cycle"
    return []


def check_cyclic_inheritance(ast):
    graph = Graph(len(AllTypes.keys()))

    for cool_type_name in AllTypes.keys():
        graph.addNewEdge(cool_type_name)

    for cool_type in AllTypes.values():
        if cool_type.parent_type is not None:
            graph.addEdge(cool_type.parent_type.name, cool_type.name)
        elif cool_type.name != 'Object':
            graph.addEdge('Object', cool_type.name)

    return [] if graph.dfs('Object') else get_cyclic_class(graph, ast)





def check_methods_params(ast):
    for cls in ast.classes:
        cls_type = AllTypes[cls.typeName]
        attrs = cls_type.get_attributtes()
        for feature in enumerate(cls.features):
            if type(feature) is FunctionFeatureNode:
                for param in feature.parameters:
                    if param.id in attrs:
                        return f'({param.getLineNumber()}, {param.getColumnNumber()}) - '
    return []


def check_semantic(ast: ProgramNode):
    errors = []

    # Checking semantic errors

    # Checking duplicated types declaration
    type_declaration_output = check_type_declaration(ast)
    if len(type_declaration_output) > 0:
        errors.append(type_declaration_output)
        return errors, AllTypes

    # Checking inheritance in declared types
    inheritance_check_output = check_type_inheritance(ast)
    if len(inheritance_check_output) > 0:
        errors.append(inheritance_check_output)
        return errors, AllTypes

    # Check cyclic inheritance
    cyclic_inheritance_check = check_cyclic_inheritance(ast)
    if len(cyclic_inheritance_check) > 0:
        errors.append(cyclic_inheritance_check)
        return errors, AllTypes

    # Check feature class list
    feature_check_output = check_features(ast)
    if len(feature_check_output) > 0:
        errors.append(feature_check_output)
        return errors, AllTypes

    # Check expressions types
    expressions_check_output = check_expressions(ast)
    if len(expressions_check_output) > 0:
        errors.append(expressions_check_output)
        return errors, AllTypes

    # Check Main unity
    if 'Main' not in AllTypes:
        # Update Error message
        errors.append('Main not declared')
        return errors, AllTypes

    if 'main' not in AllTypes["Main"].methods:
        # Update Error message
        errors.append('main method not declared')
        return errors, AllTypes

    return [], AllTypes
