from .node_il import *

class AssignNodeIL(InstructionNodeIL):
    def __init__(self, dest, source, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source 
        
        self.in1 = source
        self.out = dest

    def __str__(self):
        return ("{} = {}".format(self.dest, self.source))