from ..ast import TypeNode


class TypeData:
    def __init__(self, type_number:int, typex:TypeNode):
        self.type: int = type_number
        self.str: str = typex.name_dir
        self.attr_offsets = dict()
        self.func_offsets = dict()

        for idx, feature in enumerate(typex.features): # Calculate offsets for attributes and functions
            if isinstance(feature, str):
                self.attr_offsets[feature] = idx + 2 # The plus 2 is because the two first elementes in the instance are the type_int and the type_str_dir. Also enumerate starts with 0
            else:
                func_name, _ = feature
                self.func_offsets[func_name] = idx + 2
