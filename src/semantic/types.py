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
