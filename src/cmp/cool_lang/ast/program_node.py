from typing import List
from .class_declaration_node import ClassDeclarationNode
from .node import Node


class ProgramNode(Node):
    def __init__(self, classes: List[ClassDeclarationNode], line: int, column: int):
        super(ProgramNode, self).__init__(line, column)
        self.classes: List[ClassDeclarationNode] = classes
