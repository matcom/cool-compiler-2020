from ..semantics.semantic_utils import Type


class Node:
    def __init__(self, line: int, column: int):
        self.line: int = line
        self.column: int = column
        self.static_type: Type = Type("")
