from .node_il import NodeIL

class BinaryOperationIL(NodeIL):
    
    def __init__(self, var, leftOp, rightOp, op):
        self.var = var
        self.leftOp = leftOp
        self.rightOp = rightOp
        self.op = op
    
    def __str__(self):
        return "{} = {} {} {}\n".format(self.var, self.leftOp, self.op, self.rightOp)

class UnaryOperationIL(NodeIL):
    
    def __init__(self, var, op, symb):
        self.var = var
        self.op = op
        self.symb = symb
    
    def __str__(self):
        return "{} = {} {}".format(self.var, self.symbol, self.op)
