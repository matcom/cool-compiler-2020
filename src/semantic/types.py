ObjectType = 'Object'
IOType = 'IO'
IntType = 'Int'
StringType = 'String'
BoolType = 'Bool'

Types = [ObjectType, IOType, IntType, StringType, BoolType]

TypesHierarchy = {
    ObjectType: None,
    IOType: ObjectType,
    IntType: ObjectType,
    StringType: ObjectType,
    BoolType: ObjectType
}
