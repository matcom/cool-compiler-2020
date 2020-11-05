from .atomic_node import AtomicNode


class IdNode(AtomicNode):
    def __init__(self, token: str, line: int, column: int):
        super(IdNode, self).__init__(token, line, column)
