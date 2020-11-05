from typing import List
from .declaration_node import DeclarationNode
from .feature_declaration_node import FeatureDeclarationNode


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx: str, features: List[FeatureDeclarationNode], parent: 'ClassDeclarationNode', line: int, column: int):
        super(ClassDeclarationNode, self).__init__(idx, line, column)
        self.parent: 'ClassDeclarationNode' = parent
        self.features: List[FeatureDeclarationNode] = features
