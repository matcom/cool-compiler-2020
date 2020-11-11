from ast import *
from types_defined import AllTypes, CoolType, object_type, BasicTypes

def check_type_declaration(ast: ProgramNode):
    for cls in ast.classes:
        if cls in AllTypes:
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
                    AllTypes[cls.typeName].parent_type = father_type
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
    created_types_names = [cls.fatherTypeName for cls in ast.classes]
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
                    method_added = class_type.add_method(feature.id, feature.parameters, feature.typeName)
                    if not method_added:
                        return 'Couldn\'t add method'
                if type(feature) is AttributeFeatureNode:
                    feature_added = class_type.add_attribute(feature.id, feature.typeName, feature.expression)
                    if not feature_added:
                        return 'Couldn\'t add feature'
                return 'Unknown feature or Method'
            left_check = left_check - 1
            checked_types[i] = True

    return []


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

    

    # Check Main unity
    if 'Main' not in AllTypes:
        # Update Error message
        errors.append('Main not declared')
        return errors

    return []
