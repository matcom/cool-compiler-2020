from coolcmp.cmp_utils.my_ast import *

native_classes = [
    Class(Type('Object'), None),
    Class(Type('Int'), None, can_inherit=False),
    Class(Type('String'), None, can_inherit=False),
    Class(Type('Bool'), None, can_inherit=False),
    Class(Type('IO'), None)
]