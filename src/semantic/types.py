from lexer_parser.ast import *
from errors import add_semantic_error


class CoolType:
    def __init__(self, name, parent_type):
        self.name = name
        self.parent = parent_type
        self.attributes = {}
        self.methods = {}

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class CoolTypeAttribute:
    def __init__(self, id, attr_type):
        self.id = id
        self.attrType = attr_type


class CoolTypeMethod:
    def __init__(self, id, args, returned_type):
        self.returnedType = returned_type
        self.id = id
        self.args = args

    def __repr__(self):
        return f'{self.id}{self.args}:{self.returnedType}'


ObjectType = CoolType('Object', None)
IOType = CoolType('IO', ObjectType)
IntType = CoolType('Int', ObjectType)
StringType = CoolType('String', ObjectType)
BoolType = CoolType('Bool', ObjectType)

TypesByName = {
    'Object': ObjectType,
    'IO': IOType,
    'Int': IntType,
    'String': StringType,
    'Bool': BoolType
}


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


def check_type_declaration(node: ProgramNode):
    for c in node.classes:
        try:
            _ = TypesByName[c.type]
            add_semantic_error(0, 0, f'duplicated declaration of type {c.type}')
            return False
        except KeyError:
            TypesByName[c.type] = CoolType(c.type, None)
    return True


def check_type_hierarchy(node: ProgramNode):
    for c in node.classes:
        cType = TypesByName[c.type]
        if c.parent_type:
            try:
                cType.parent = TypesByName[c.parent_type]
            except KeyError:
                add_semantic_error(0, 0, f'unknown parent type {c.parent_type}')
                return False
        else:
            cType.parent = ObjectType
    return True
