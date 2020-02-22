from .node import Node


class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
        self.line = declarations[0].line
        self.column = declarations[0].column
