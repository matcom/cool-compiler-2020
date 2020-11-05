from .atomic_node import AtomicNode


class IntegerNode(AtomicNode):
    def __init__(self, token: str, line: int, column: int):
        super(IntegerNode, self).__init__(token, line, column)
