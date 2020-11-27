from typing import Dict

from ..ast import TypeNode


class TypeData:
    def __init__(self, type_number: int, typex: TypeNode):
        self.type: int = type_number
        self.str: str = typex.name_dir
        self.attr_offsets: Dict[str, int] = dict()
        self.func_offsets: Dict[str, int] = dict()
        self.func_names: Dict[str, str] = dict()

        # Calculate offsets for attributes and functions
        for idx, feature in enumerate(typex.features):
            if isinstance(feature, str):
                # The plus 2 is because the two first elementes
                # in the instance are the type_int and the type_str_dir.
                # Also enumerate starts with 0
                self.attr_offsets[feature] = idx + 2
            else:
                func_name, long_name = feature
                self.func_offsets[func_name] = idx + 2
                self.func_names[func_name] = long_name

    def __str__(self) -> str:
        return (
            f"TypeData-> type: {self.type}, str: {self.str}, "
            + f"attr_offsets: {self.attr_offsets}, "
            + f"func_offsets: {self.func_offsets}, "
            + f"func_names: {self.func_names}"
        )
