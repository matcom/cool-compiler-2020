from .atomic_node import AtomicNode


class StringNode(AtomicNode):
    def __init__(self, token: str, line: int, column: int):
        super(StringNode, self).__init__(token, line, column)
