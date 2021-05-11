from typing import List
from .expresion_node import ExpressionNode
from .feature_declaration_node import FeatureDeclarationNode
from .param_declaration_node import ParamDeclarationNode


class FuncDeclarationNode(FeatureDeclarationNode):
    def __init__(self, idx: str, params: List[ParamDeclarationNode], typex: str, expression: ExpressionNode, line: int, column: int):
        super(FuncDeclarationNode, self).__init__(idx, typex, expression, line, column)
        self.params: List[ParamDeclarationNode] = params
