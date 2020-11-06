from .node_il import NodeIL

class AllocateIL(NodeIL):
    
    def __init__(self, var, size, type):
        self.var = var
        self.size = size
        self.type = type

    def __str__(self):
        pass
