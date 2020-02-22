from .expresion_node import ExpressionNode


class FunctionCallNode(ExpressionNode):
    def __init__(self, obj, idx, args, typex=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex
        self.line = idx.line
        self.column = idx.column
