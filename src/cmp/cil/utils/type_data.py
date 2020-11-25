from ..ast import TypeNode


class TypeData:
    def __init__(self, type_number: int, typex: TypeNode):
        self.type: int = type_number
        self.str: str = typex.name_dir
        self.attr_offsets = dict()
        self.func_offsets = dict()

        # Calculate offsets for attributes and functions
        for idx, feature in enumerate(typex.features):
            if isinstance(feature, str):
                # The plus 2 is because the two first elementes in the instance
                #  are the type_int and the type_str_dir
                # Also enumerate starts with 0
                self.attr_offsets[feature] = idx + 2
            else:
                func_name, _ = feature
                self.func_offsets[func_name] = idx + 2
