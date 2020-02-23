from .node import Node


class ProgramNode(Node):
    def __init__(self, declarations, line, column):
        self.declarations = declarations
        self.line = line
        self.column = column
