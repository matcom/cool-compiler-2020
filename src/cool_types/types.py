"""
Copyright (c) 2020 School of Math and Computer Science, University of Havana

COOL compiler project
"""

from errors import *


class CoolType:
    def __init__(self, name, parent_type, inherit=True):
        self.name = name
        self.parent = parent_type
        self.attributes = {}
        self.methods = {}
        self.inherit = inherit
        self.childs = []

    def __can_be_define__(self, id):
        if id in self.methods.keys():
            return False, f'method {id} already declared in class {self.name}'
        return True, None

    def add_method(self, id, arg_types_name, returned_type):
        ok, msg = self.__can_be_define__(id)
        if ok:
            arg_types = []
            for arg in arg_types_name:
                arg_type = type_by_name(arg)
                if arg_type is None:
                    return False, f'{ERR_TYPE}: Class {arg} of formal parameter is undefined.'
                arg_types.append(arg_type)
            _returned_type = type_by_name(returned_type)
            if _returned_type is None:
                return False, f'unknown type \'{returned_type}\''
            self.methods[id] = CoolTypeMethod(id, arg_types, _returned_type)
            return True, None
        else:
            return False, msg

    def get_all_attributes(self):
        t = self
        result = []
        while t:
            temp = []
            for attr in t.attributes.values():
                temp.append(attr)
            result.append(temp)
            t = t.parent
        return [elem for sublist in result[::-1] for elem in sublist]

    def get_all_self_methods(self):
        return self.methods

    def get_all_inherited_methods(self):
        t = self.parent
        result = []
        while t:
            temp = []
            for met in t.methods.values():
                met.owner = t.name
                temp.append(met)
            result.append(temp)
            t = t.parent
        return [elem for sublist in result[::-1] for elem in sublist]

    def get_method(self, id, args_types):
        try:
            return self.get_method_without_hierarchy(id, args_types)
        except Exception:
            if self.parent:
                return self.parent.get_method(id, args_types)
            else:
                return None, f'{ERR_ATTRIBUTE}: Dispatch to undefined method {id}.'

    def get_method_without_hierarchy(self, id, args_types):
        try:
            method = self.methods[id]
            if len(args_types) != len(method.args):
                return None, f'{ERR_SEMANTIC}: Method {id} called with wrong number of arguments.'
            for i, a in enumerate(args_types):
                if not check_inherits(a, method.args[i]):
                    return None, f'{ERR_TYPE}: In call of method {id}, type {a} does not conform to declared type {method.args[i]}.'
            return method, None
        except KeyError:
            raise Exception(f'type {self.name} don\'t have a method {id}')

    def add_attr(self, id, attr_type, expression):
        attribute, owner_type = get_attribute(self, id)
        if attribute is not None:
            return False, f'{ERR_SEMANTIC}: Attribute {id} is an attribute of an inherited class.'
        try:
            _ = self.attributes[id]
            return False, f'{ERR_SEMANTIC}: Attribute {id} is an attribute of an inherited class.'
        except KeyError:
            _attr_type = type_by_name(attr_type)
            if _attr_type is None:
                return False, f'unknown type \'{attr_type}\''
            self.attributes[id] = CoolTypeAttribute(id, _attr_type, expression)
            return True, None

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


def get_attribute(type_c: CoolType, id: str):
    while type_c is not None:
        try:
            return type_c.attributes[id], type_c
        except KeyError:
            type_c = type_c.parent
    return None, None


class CoolTypeAttribute:
    def __init__(self, id, attr_type, expression=None):
        self.id = id
        self.attrType = attr_type
        self.expression = expression


class CoolTypeMethod:
    def __init__(self, id, args, returned_type):
        self.returnedType = returned_type
        self.id = id
        self.args = args

    def __repr__(self):
        return f'{self.id}{self.args}:{self.returnedType}'


def type_by_name(type_name):
    try:
        return TypesByName[type_name]
    except KeyError:
        return None


def check_inherits(type_a: CoolType, type_b: CoolType):
    """
    Return True if type_a <= typeB
    """
    current = type_a
    while current != type_b:
        if current is None:
            return False
        current = current.parent
    return True


def check_type_declaration(node):
    for c in node.classes:
        try:
            _ = TypesByName[c.type]
            add_semantic_error(c.lineno, c.colno,
                               f'{ERR_SEMANTIC}: Redefinition of basic class {c.type}.')
            return False
        except KeyError:
            TypesByName[c.type] = CoolType(c.type, None)
    return True


def check_type_hierarchy(node):
    for c in node.classes:
        cType = TypesByName[c.type]
        if c.parent_type:
            try:
                parentType = TypesByName[c.parent_type]
                if parentType.inherit:
                    cType.parent = parentType
                    type_x = parentType
                    while type_x:
                        if type_x:
                            if type_x == cType:
                                add_semantic_error(
                                    c.lineno, c.colno, f'{ERR_SEMANTIC}: Class {cType.name}, or an ancestor of {cType.name}, is involved in an inheritance cycle.')
                                return False
                            type_x = type_x.parent
                else:
                    add_semantic_error(
                        c.lineno, c.colno, f'{ERR_SEMANTIC}: Class {cType} cannot inherit class {parentType.name}.')
                    return False
            except KeyError:
                add_semantic_error(c.lineno, c.colno,
                                   f'{ERR_TYPE}: Class {cType} inherits from an undefined class {c.parent_type}.')
                return False
        else:
            cType.parent = ObjectType
    return True


def __type_hierarchy__(type_x):
    h = []
    while type_x is not None:
        h.append(type_x)
        type_x = type_x.parent
    return h


def pronounced_join(type_a, type_b):
    h = __type_hierarchy__(type_b)
    while type_a is not None:
        if type_a in h:
            break
        type_a = type_a.parent
    return type_a


SelfType = CoolType('SELF_TYPE', None, False)
ObjectType = CoolType('Object', None)
IOType = CoolType('IO', ObjectType)
IntType = CoolType('Int', ObjectType, False)
StringType = CoolType('String', ObjectType, False)
BoolType = CoolType('Bool', ObjectType, False)

TypesByName = {
    'SELF_TYPE': SelfType,
    'Object': ObjectType,
    'IO': IOType,
    'Int': IntType,
    'String': StringType,
    'Bool': BoolType
}

ObjectType.childs = [IOType, IntType, StringType, BoolType]
ObjectType.add_method('abort', [], 'Object')
ObjectType.add_method('type_name', [], 'String')
ObjectType.add_method('copy', [], 'SELF_TYPE')
IOType.add_method('out_string', ['String'], 'SELF_TYPE')
IOType.add_method('out_int', ['Int'], 'SELF_TYPE')
IOType.add_method('in_string', [], 'String')
IOType.add_method('in_int', [], 'Int')
StringType.add_method('length', [], 'Int')
StringType.add_method('concat', ['String'], 'String')
StringType.add_method('substr', ['Int', 'Int'], 'String')
