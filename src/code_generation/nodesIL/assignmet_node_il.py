from .node_il import NodeIL

class AssignmentNodeIL(NodeIL):

    def __init__(self):
        pass

    def __str__(self):
        pass

class VarToVarIL(AssigmentNodeIL):

    def __init__(self):
        pass
    
    def __str__(self):
        pass

class MemoToVarIL(AssigmentNodeIL):
    
    def __init__(self, left, right, offset):
        pass
    
    def __str__(self):
        pass

class VarToMemoIL(AssigmentNodeIL):
    
    def __init__(self, left, right, offset):
        pass
    
    def __str__(self):
        pass

class ConstToMemoIL(AssigmentNodeIL):
    
    def __init__(self, left, right, offset):
        pass
    
    def __str__(self):
        pass