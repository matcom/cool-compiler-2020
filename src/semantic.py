from ast import *
from types import *


def check_type_declaration(ast: ProgramNode):
    for cls in ast.classes:
        if cls in AllTypes:
            # TODO Update return error message
            return 'Re-declaring class'
        AllTypes[cls.type_name] = CoolType(cls.type_name, None)
    return []


def check_type_inheritance(ast: ProgramNode):
    for cls in ast.classes:
        if cls.father_type_name:
            if cls.father_type_name in AllTypes:
                father_type = AllTypes[cls.father_type_name]
                if father_type.inherit:
                    AllTypes[cls.type_name].parent_type = object_type
                else:
                    # TODO Update error message
                    return f'Error inherit from {cls.father_type_name}'
            else:
                # TODO Update error message
                return f'Error getting {cls.father_type_name}'
        else:
            AllTypes[cls.type_name].parent_type = object_type

    return []


def check_features(ast: ProgramNode):
    checked_types = [True if t in BasicTypes else False for t in AllTypes]
    left_check = checked_types.count(False)

    while left_check > 0:
        for i, cls in enumerate(ast.classes):
            if checked_types[i]:
                continue
            if cls.father_type_name and cls.father_type_name not in checked_types:
                continue
            class_type = AllTypes[cls.type_name]
            for feature in cls.features:
                if type(feature) is FunctionFeatureNode:
                    method_added = class_type.add_method(feature.id, feature.parameters, feature.typeName)
                    if not method_added:
                        return 'Couldn\'t add method'
                if type(feature) is AttributeFeatureNode:
                    feature_added = class_type.add_attribute(feature.id, feature.typeName, feature.expression)
                    if not feature_added:
                        return 'Couldn\'t add feature'
                return 'Unknow feature or Method'
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

    inheritance_check_output = check_type_inheritance(ast)
    # Checking inheritance in declared types
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
