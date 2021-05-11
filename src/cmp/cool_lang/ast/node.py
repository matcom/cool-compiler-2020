from typing import Any


class Node:
    def __init__(self, line: int, column: int):
        self.line: int = line
        self.column: int = column
        self.static_type: Any = None  # type:ignore
