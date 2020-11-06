from .node_il import NodeIL

class AllocateIL(NodeIL):
    
    def __init__(self, var, size, typ):
        self.var = var
        self.size = size
        self.typ = typ

    def __str__(self):
        return "alloc {} in {}".format(self.typ, self.var)
