from ast import *
from type_defined import AllTypes, CoolType, object_type, BasicTypes


def check_type_declaration(ast: ProgramNode):
    for cls in ast.classes:
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
                        # TODO Update error message
                        return "Can't inherit from same class"
                else:
                    # TODO Update error message
                    return f'Error inherit from {cls.fatherTypeName}'
            else:
                # TODO Update error message
                return f'Error getting {cls.fatherTypeName}'
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
            for feature in cls.features:
                if type(feature) is FunctionFeatureNode:
                    parameters_name = []
                    for arg in feature.parameters:
                        parameters_name.append([arg.id, arg.typeName])
                    method_added = class_type.add_method(feature.id, parameters_name, feature.typeName)
                    if not method_added:
                        return 'Couldn\'t add method'
                    continue
                if type(feature) is AttributeFeatureNode:
                    feature_added = class_type.add_attribute(feature.id, feature.typeName, feature.expression)
                    if not feature_added:
                        return 'Couldn\'t add attribute'
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
                    for i in range(0, len(class_methods[k].args)):
                        if (class_methods[k].args[i])[1].name != (class_inherited_methods[k].args[i])[1].name:
                            return "Child overriding function's params must have same type as father overrided function's params"

            left_check = left_check - 1
            print(i)
            checked_types[i] = True

    return []

def check_expressions(ast: ProgramNode):
    for cls in ast.classes:
        for feature in cls.features:
            if type(feature) is AttributeFeatureNode:
                feature_type = feature.typeName
                error, expression_type = GetExpressionReturnType(feature.expression)
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
                
                error, expression_type = GetExpressionReturnType(feature.expression, attributes, functions, params, True)
                if len(error) > 0:
                    return error
                if feature_type != expression_type:
                    return "Invalid expression returning type"
    
    return []

def GetExpressionReturnType(expression, attributes = {}, functions = {}, parameters = {}, isFunction = False):

    if type(expression) is AssignStatementNode:
        error1, type1 = GetExpressionReturnType(expression.expression)
        if len(error1) > 0:
            return error1, ""
        return [], type1

    elif type(expression) is ConditionalStatementNode:
        error1, type1 = GetExpressionReturnType(expression.evalExpr)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return "Conditional predicate must be boolean", ""
        error2, type2 = GetExpressionReturnType(expression.ifExpr)
        if len(error2) > 0:
            return error2, ""
        error3, type3 = GetExpressionReturnType(expression.elseExpr)
        if len(error3) > 0:
            return error3, ""
        # Aqui ver como es que se comprueban los dos tipos de retorno del
        # then y del else con el del feature en cuestion
        # return [], type2 + " " + type3 ???

    elif type(expression) is LoopStatementNode:
        error1, type1 = GetExpressionReturnType(expression.evalExpr)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return "Loop predicate must be boolean", ""
        error2, type2 = GetExpressionReturnType(expression.loopExpr)
        if len(error2) > 0:
            return error2, ""
        return [], "Object"

    elif type(expression) is BlockStatementNode:
        lastType = ""
        for expr in expression.expressions:
            eError, eType = GetExpressionReturnType(expr)
            if len(eError) > 0:
                return "Error in block expression: " + eError, ""
            lastType = eType

        return [], lastType

    elif type(expression) is LetStatementNode:
        pass

    elif type(expression) is CaseStatementNode:
        pass

    elif type(expression) is CaseBranchNode:
        pass

    elif type(expression) is NewStatementNode:
        # Aqui hay que comprobar si el tipo que me dan esta definido
        pass

    elif type(expression) is FunctionCallStatement:
        # Aqui hay que chequear que el tipo de la expresion de la izquierda
        # contenga la funcion que se le llama
        pass

    elif type(expression) is ConstantNumericNode:
        return [], "Int"
    elif type(expression) is ConstantStringNode:
        return [], "String"
    elif type(expression) is ConstantBoolNode:
        return [], "Bool"

    elif type(expression) is VariableNode:
        # Aqui hay que comprobar los casos de si estamos en una funcion o un atributos
        # y en el primer caso buscar que se encuentre en alguno de los diccionarios de entrada
        pass

    elif type(expression) is NotNode:
        error1, type1 = GetExpressionReturnType(expression.expression)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Bool":
            return "Expressions for not operator must be boolean", ""
        return [], "Bool"

    elif type(expression) is IsVoidNode:
        error1, type1 = GetExpressionReturnType(expression.expression)
        if len(error1) > 0:
            return error1, ""
        return [], "Bool"

    elif type(expression) is ComplementNode:
        error1, type1 = GetExpressionReturnType(expression.expression)
        if len(error1) > 0:
            return error1, ""
        if type1 != "Int":
            return "Expressions for complement must be an integer", ""
        return [], "Int"

    elif type(expression) is LessEqualNode:
        error1, type1 = GetExpressionReturnType(expression.left)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be compared with <=", ""
        return [], "Int"

    elif type(expression) is LessNode:
        error1, type1 = GetExpressionReturnType(expression.left)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be compared with <", ""
        return [], "Int"

    elif type(expression) is EqualNode:
        error1, type1 = GetExpressionReturnType(expression.left)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right)
        if len(error2) > 0:
            return error2, ""
        if type1 != type2:
            return "Expressions must be of same type", ""
        return [], type1

    elif type(expression) is PlusNode:
        error1, type1 = GetExpressionReturnType(expression.left)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be added", ""
        return [], "Int"

    elif type(expression) is MinusNode:
        error1, type1 = GetExpressionReturnType(expression.left)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be substracted", ""
        return [], "Int"

    elif type(expression) is TimesNode:
        error1, type1 = GetExpressionReturnType(expression.left)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be multiplied", ""
        return [], "Int"

    elif type(expression) is DivideNode:
        error1, type1 = GetExpressionReturnType(expression.left)
        if len(error1) > 0:
            return error1, ""
        error2, type2 = GetExpressionReturnType(expression.right)
        if len(error2) > 0:
            return error2, ""
        if type1 != "Int" or type2 != "Int":
            return "Only integers can be divided", ""
        return [], "Int"

def check_semantic(ast: ProgramNode):
    errors = []

    # Checking semantic errors

    # Checking duplicated types declaration
    type_declaration_output = check_type_declaration(ast)
    if len(type_declaration_output) > 0:
        errors.append(type_declaration_output)
        return errors

    # Checking inheritance in declared types
    inheritance_check_output = check_type_inheritance(ast)
    if len(inheritance_check_output) > 0:
        errors.append(inheritance_check_output)
        return errors

    # Check feature class list
    feature_check_output = check_features(ast)
    if len(feature_check_output) > 0:
        errors.append(feature_check_output)
        return errors

    # Check expressions types
    #expressions_check_output = check_expressions(ast)
    #if len(expressions_check_output) > 0:
    #    errors.append(expressions_check_output)
    #    return errors

    # Check Main unity
    #if 'Main' not in AllTypes:
    #    # Update Error message
    #    errors.append('Main not declared')
    #    return errors
    
    return []

