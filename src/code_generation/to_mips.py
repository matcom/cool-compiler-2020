import os
from nodesIL import *
import visitor

class MIPS:
    def __init__(self, il_code, il_data):
        self.code = []
        self.data = []
        self.il_code = il_code
        self.il_data = il_data
        self.path = path

    def _loadfrom(self, file):
        fd = open(file)
        return fd.read()

    def start(self):
        code = ""
        code += ".data\n"
        code += "buffer:\n"
        code += ".space 65536\n"
        code += "\n"

        for node in il_data:
            self.visit(node)

        code += "\n.globl main\n"
        code+= ".text\n"

        code += _loadfrom(path.join('code_generation/statics', 'IO.s'))
        code += _loadfrom(path.join('code_generation/statics', 'Object.s'))
        code += _loadfrom(path.join('code_generation/statics', 'String.s'))
        code += _loadfrom(path.join('code_generation/statics', 'inherit.s'))

        for c in self.code:
            code += (c + "\n")

        code += "li $v0, 10\n"
        code += "syscall\n"

        return code

    @visitor.on('node')
    def visit(self, node):
        pass

    #operations

    @visitor.on(BinaryOperationIL)
    def visit(self, node):
        pass

    @visitor.on(UnaryOperationIL)
    def visit(self, node):
        pass

    #allocate

    @visitor.on(AllocateIL)
    def visit(self, node):
        pass

    #assignment
    @visitor.on(VarToVarIL)
    def visit(self, node):
        pass

    @visitor.on(VarToMemoIL)
    def visit(self, node):
        pass

    @visitor.on(MemoToVarIL)
    def visit(self, node):
        pass

    @visitor.on(ConstToMemoIL)
    def visit(self, node):
        pass

    #methods
    @visitor.on(LabelIL)
    def visit(self, node):
        pass

    @visitor.on(GotoIL)
    def visit(self, node):
        pass

    @visitor.on(CommentIL)
    def visit(self, node):
        pass

    @visitor.on(IfJumpIL)
    def visit(self, node):
        pass

    @visitor.on(HierarchyIL)
    def visit(self, node):
        pass

    @visitor.on(VirtualTableIL)
    def visit(self, node):
        pass

    @visitor.on(PushIL)
    def visit(self, node):
        pass

    @visitor.on(PopIL)
    def visit(self, node):
        pass

    @visitor.on(ReturnIL)
    def visit(self, node):
        pass

    @visitor.on(DispatchIL)
    def visit(self, node):
        pass

    @visitor.on(DispatchParentIL)
    def visit(self, node):
        pass

    @visitor.on(InheritIL)
    def visit(self, node):
        pass

    @visitor.on(StringIL)
    def visit(self, node):
        pass

    @visitor.on(PrintIL)
    def visit(self, node):
        pass

    @visitor.on(LoadLabelIL)
    def visit(self, node):
        pass