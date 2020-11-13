import os
from nodesIL import *
import visitor

class MIPS:
    def __init__(self):
        pass

    def start(self):
        pass
    
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