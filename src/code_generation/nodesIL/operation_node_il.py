from .node_il import NodeIL

class BinaryOperationIL(NodeIL):
    
    def __init__(self, var, leftOp, rightOp, symbol):
        self.var = var
        self.leftOp = leftOp
        self.rightOp = rightOp
        self.symbol = symbol
    
    def __str__(self):
        return "var {} = var {} {} var {}\n".format(self.var, self.leftOp, self.symbol, self.rightOp)

class UnaryOperationIL(NodeIL):
    
    def __init__(self, var, op, symbol):
        self.var = var
        self.op = op
        self.symbol = symbol
    
    def __str__(self):
        return "var {} = {} var {}".format(self.var, self.symbol, self.op)
