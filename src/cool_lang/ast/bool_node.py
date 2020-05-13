from .atomic_node import AtomicNode


class BoolNode(AtomicNode):
    def __init__(self, token: str, line: int, column: int):
        super(BoolNode, self).__init__(token, line, column)
