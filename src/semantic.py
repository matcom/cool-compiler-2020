from ast import *
from graph import Graph
from type_defined import AllTypes, CoolType, object_type, BasicTypes


def check_type_declaration(ast: ProgramNode):
    for cls in ast.classes:
        if cls.typeName in BasicTypes:
            return f'({cls.getLineNumber()}, {cls.getColumnNumber()}) - SemanticError: Redefinition of basic class {cls.typeName}.'
        if cls.typeName in AllTypes:
            # TODO Update return error message
            return 'Re-declaring class'

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
                        parameters_name.append(arg.id)
                        parameters_type.append(arg.typeName)
                    method_added = class_type.add_method(feature.id, parameters_type, parameters_name, feature.typeName, feature.statement)
                    if len(method_added) > 0:
                        return f'({feature.parameters[method_added[1]].getLineNumber()}, ' \
                               f'{feature.parameters[method_added[1]].getColumnNumber()}) ' \
                               f'{method_added[0]}'
                    continue
                if type(feature) is AttributeFeatureNode:
                    feature_added_error = class_type.add_attribute(feature.id, feature.typeName, feature.expression)
                    if len(feature_added_error) > 0:
                        return f'({feature.getLineNumber()}, {feature.getColumnNumber()}) {feature_added_error}'
                    continue
                return 'Unknown attribute or Method'

            class_methods = class_type.get_self_methods()
            class_inherited_methods = class_type.get_methods_inherited()

            for k in class_methods.keys():
                if k in class_inherited_methods:
                    if class_methods[k].return_type != class_inherited_methods[k].return_type:
                        return "Child overriding function must have the same return type as father overrided function"
                    if len(class_methods[k].args) != len(class_inherited_methods[k].args):
                        return "Child overriding function must have the same params count as father overrided function"
                    for counter in range(0, len(class_methods[k].args)):
                        if (class_methods[k].args[counter])[1].name != (class_inherited_methods[k].args[counter])[
                            1].name:
                            return "Child overriding function's params must have same type as father overrided function's params"

            left_check = left_check - 1
            checked_types[i] = True

    return []


def check_expressions(ast: ProgramNode):
    for cls in ast.classes:
        for feature in cls.features:
            if type(feature) is AttributeFeatureNode:
                feature_type = feature.typeName
                if feature.expression:
                    error, expression_type = GetExpressionReturnType(feature.expression, False, {}, {}, {}, False, {})
                    if len(error) > 0:
                        return error
                    if feature_type != expression_type:
                        return "Invalid expression returning type"
            
        attributes = AllTypes[cls.typeName].get_attributes()
        functions = AllTypes[cls.typeName].get_methods()

        for feature in cls.features:
            if type(feature) is FunctionFeatureNode:
                feature_type = feature.typeName
                params = {}
                for parameter in feature.parameters:
                    params[parameter.id] = parameter.typeName
                error, expression_type = GetExpressionReturnType(feature.statement, True, attributes, functions,
                                                                 params,
                                                                 False, {})
                if len(error) > 0:
                    return error
                if feature_type != expression_type:
                    return "Invalid expression returning type"

    return []


def GetFirstCommonAncestor(types):
    result = types[0].name
    for i in range(1, len(types)):
        result = GetFirstCommonAncestor(result, types[i])

    return result


def GetFirstCommonAncestor(typeA, typeB):
    if IsAncestor(typeA, typeB):
        return typeA.name
    if IsAncestor(typeB, typeA):
        return typeB.name
    return GetFirstCommonAncestor(typeA.parent_type, typeB.parent_type)


def IsAncestor(olderNode, youngerNode):
    if olderNode.name == youngerNode.name:
        return True
    return IsAncestor(olderNode, youngerNode.parent_type)


def GetExpressionReturnType(expression, insideFunction, attributes, functions, parameters, insideLet, letVars,
                            insideCase=False, caseVar={}):
    if type(expression) is AssignStatementNode:
        error1, type1 = GetExpressionReturnType(expression.expression, insideFunction, attributes, functions,
                                                parameters, insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        return [], type1

    elif type(expression) is ConditionalStatementNode:
        error1, type1 = GetExpressionReturnType(expression.evalExpr, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return "Conditional predicate must be boolean", ""
        
        error2, type2 = GetExpressionReturnType(expression.ifExpr, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        error3, type3 = GetExpressionReturnType(expression.elseExpr, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error3) > 0:
            return error3, ""

        thenType = AllTypes[type2]
        elseType = AllTypes[type3]
        return [], GetFirstCommonAncestor(thenType, elseType)

    elif type(expression) is LoopStatementNode:
        error1, type1 = GetExpressionReturnType(expression.evalExpr, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return "Loop predicate must be boolean", ""
        error2, type2 = GetExpressionReturnType(expression.loopExpr, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        return [], "Object"

    elif type(expression) is BlockStatementNode:
        lastType = ""
        for expr in expression.expressions:
            eError, eType = GetExpressionReturnType(expr, insideFunction, attributes, functions, parameters, insideLet,
                                                    letVars, insideCase, caseVar)
            if len(eError) > 0:
                return "Error in block expression: " + eError, ""
            lastType = eType

        return [], lastType


    elif type(expression) is LetStatementNode:
        letVariables = letVars
        for variable in expression.variables:
            if not (variable.typeName in AllTypes):
                return "Self variable type not defined", ""
            if variable.expression != None:
                error0, type0 = GetExpressionReturnType(variable.expression, insideFunction, attributes, functions,
                                                        parameters, True, letVariables, insideCase, caseVar)
                if len(error0) > 0:
                    return "Error in let variable initialization expression", ""
                if type0 != variable.typeName:
                    return "Let variables types and corresponding initialization expressions types must match", ""
            letVariables[variable.id] = variable.typeName

        errorLet, typeLet = GetExpressionReturnType(expression.expression, insideFunction, attributes, functions,
                                                    parameters, True, letVariables, insideCase, caseVar)
        if len(errorLet) > 0:
            return errorLet, ""
        return [], typeLet


    elif type(expression) is CaseStatementNode:
        eError, eType = GetExpressionReturnType(expression.expression, insideFunction, attributes, functions,
                                                parameters, insideLet, letVars, insideCase, caseVar)
        if len(eError) > 0:
            return eError, ""
        caseBranchesTypes = []
        for caseBranch in expression.body:
            error0, type0 = GetExpressionReturnType(caseBranch, insideFunction, attributes, functions, parameters,
                                                    insideLet, letVars, insideCase, caseVar)
            if len(error0) > 0:
                return error0, ""
            inList = False
            for t in caseBranchesTypes:
                if t.name == type0:
                    inList = True
                    break
            if not inList:
                inList.append(AllTypes[type0])

        return [], GetFirstCommonAncestor(caseBranchesTypes)


    elif type(expression) is CaseBranchNode:
        if not (expression.typeName in AllTypes):
            return "Case branch type not defined", ""
        error0, type0 = GetExpressionReturnType(expression.expression, insideFunction, attributes, functions,
                                                parameters, insideLet, letVars, True,
                                                {expression.id: expression.typeName})
        if len(error0) > 0:
            return error0, ""

        return [], type0

    elif type(expression) is NewStatementNode:
        if expression.typeName in AllTypes:
            return [], AllTypes[expression.typeName].name
        else:
            return "New statement type not defined", ""

    elif type(expression) is FunctionCallStatement:
        
        e, t = GetExpressionReturnType(expression.instance, insideFunction, attributes, functions, parameters,
                                       insideLet, insideCase, caseVar)
        if len(e) > 0:
            return e, ""
        if expression.dispatchType != None:
            if not (expression.dispatchType in AllTypes):
                return "Ancestor class type not defined", ""
            expType = AllTypes[t]
            ancType = AllTypes[expression.dispatchType]
            if IsAncestor(ancType, expType):
                methods = ancType.get_methods()
                if expression.function in methods:
                    if len(methods[expression.function].args_names) != len(expression.args):
                        return "Argument count does not match in function call", ""
                    i = 0
                    for arg in expression.args:
                        aError, aType = GetExpressionReturnType(arg, insideFunction, attributes, functions, parameters,
                                                                insideLet, insideCase, caseVar)
                        
                        if len(aError) > 0:
                            return aError, ""
                        if aType != ((methods[expression.function]).args_types[i]).name:
                            return "Some argument type in function call doesn't match with functions argument type", ""
                        i = i + 1
                    return [], methods[expression.function].return_type.name
                else:
                    return "Function not defined", ""

            else:
                return "Type " + aType.name + " is not ancestor of type " + eType.name, ""

        methods = AllTypes[t].get_methods()
        if expression.function in methods:
            if len(methods[expression.function].args_names) != len(expression.args):
                return "Argument count does not match in function call", ""
            i = 0
            for arg in expression.args:
                aError, aType = GetExpressionReturnType(arg, insideFunction, attributes, functions, parameters,
                                                        insideLet, insideCase, caseVar)
                if len(aError) > 0:
                    return aError, ""
                if aType != ((methods[expression.function]).args_types[i]).name:
                    return "Some argument type in function call doesn't match with functions argument type", ""
                i = i + 1

            return [], methods[expression.function].return_type.name
        else:
            return "Function not defined", ""


    elif type(expression) is ConstantNumericNode:
        return [], "Int"
    elif type(expression) is ConstantStringNode:
        return [], "String"
    elif type(expression) is ConstantBoolNode:
        return [], "Bool"

    elif type(expression) is VariableNode:
        if insideFunction:
            if insideLet:
                if expression.lex in letVars:
                    return [], letVars[expression.lex]
            if insideCase:
                if expression.lex in caseVar:
                    return [], caseVar[expression.lex]
            if expression.lex in parameters:
                return [], parameters[expression.lex]
            if expression.lex in attributes:
                return [], (attributes[expression.lex].attribute_type).name

        return "Variable " + expression.lex + "not defined"

    elif type(expression) is NotNode:
        error1, type1 = GetExpressionReturnType(expression.expression, insideFunction, attributes, functions,
                                                parameters, insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return "Expressions for not operator must be boolean", ""
        return [], "Bool"

    elif type(expression) is IsVoidNode:
        error1, type1 = GetExpressionReturnType(expression.expression, insideFunction, attributes, functions,
                                                parameters, insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        return [], "Bool"

    elif type(expression) is ComplementNode:
        error1, type1 = GetExpressionReturnType(expression.expression, insideFunction, attributes, functions,
                                                parameters, insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Int":
            return "Expressions for complement must be an integer", ""
        return [], "Int"

    elif type(expression) is LessEqualNode:
        error1, type1 = GetExpressionReturnType(expression.left, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be compared with <=", ""
        return [], "Bool"

    elif type(expression) is LessNode:
        error1, type1 = GetExpressionReturnType(expression.left, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be compared with <", ""
        return [], "Bool"

    elif type(expression) is EqualNode:
        error1, type1 = GetExpressionReturnType(expression.left, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        if type1 != type2:
            return "Expressions must be of same type", ""
        return [], "Bool"

    elif type(expression) is PlusNode:
        error1, type1 = GetExpressionReturnType(expression.left, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be added", ""
        return [], "Int"

    elif type(expression) is MinusNode:
        error1, type1 = GetExpressionReturnType(expression.left, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be substracted", ""
        return [], "Int"

    elif type(expression) is TimesNode:
        error1, type1 = GetExpressionReturnType(expression.left, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be multiplied", ""
        return [], "Int"

    elif type(expression) is DivideNode:
        error1, type1 = GetExpressionReturnType(expression.left, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right, insideFunction, attributes, functions, parameters,
                                                insideLet, letVars, insideCase, caseVar)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be divided", ""
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


def check_attributes_inheritance(ast):
    for cls in ast.classes:
        type_cls = AllTypes[cls.typeName]
        attr_inherited = type_cls.get_attributes()
        for attr in cls.features:
            if type(attr) is AttributeFeatureNode:
                if attr.id in attr_inherited:
                    print(attr)
        return ''
    return []


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

    # Check illegal redefinition of methods
    attr_inheritance_redefinition = check_attributes_inheritance(ast)
    if len(attr_inheritance_redefinition) > 0:
        errors.append(attr_inheritance_redefinition)
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
