from .expresion_node import ExpressionNode
from .feature_declaration_node import FeatureDeclarationNode


class AttrDeclarationNode(FeatureDeclarationNode):
    def __init__(self, idx: str, typex: str, expression: ExpressionNode, line: int, column: int):
        super(AttrDeclarationNode, self).__init__(idx, typex, expression, line, column)
