from .node_il import NodeIL

class AssignmentNodeIL(NodeIL):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "{} = {}".format(self.left, self.right)

class VarToVarIL(AssignmentNodeIL):

    def __init__(self, left, right):
        super().__init__(left, right)
    
    def __str__(self):
        return "var {} = var {}".format(self.left, self.right)

class MemoToVarIL(AssignmentNodeIL):
    
    def __init__(self, left, right, offset):
        super().__init__(left, right)
        self.offset = offset
    
    def __str__(self):
        return "var {} = memo [{}]".format(self.left, self.offset)

class VarToMemoIL(AssignmentNodeIL):
    
    def __init__(self, left, right, offset):
        super().__init__(left, right)
        self.offset = offset
    
    def __str__(self):
        return "memo [{}] = var {}".format(self.offset, self.right)

class ConstToMemoIL(AssignmentNodeIL):
    
    def __init__(self, left, right, offset):
        super().__init__(left, right)
        self.offset = offset
    
    def __str__(self):
        return "memo [{}] = {}\n".format(self.left + self.offset, self.right)