class AllocateNodeIL(InstructionNodeIL):
    def __init__(self, itype, dest, idx=None):
        super().__init__(idx)
        self.type = itype
        self.dest = dest

        self.out = dest

    def __str__():
        return ("{} = ALLOCATE {}".format(self.dest, self.type))