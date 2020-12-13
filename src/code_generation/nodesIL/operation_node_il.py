from .node_il import *

class BinaryNodeIL(InstructionNodeIL):
    def __init__(self, dest, left, right, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.left = left
        self.right = right 
        self.op = idx
        self.in1 = left
        self.in2 = right
        self.out = dest

class UnaryNodeIL(InstructionNodeIL):
    def __init__(self, dest, expr, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.op = idx
        self.expr = expr

        self.in1 = expr
        self.out = dest