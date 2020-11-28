from .cil_ast import *
from ..cp import visitor

class CIL_TO_MIPS:

    @visitor.on('node')
    def visit(self,node):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node):
        pass

    @visitor.when(FunctionNode)
    def visit(self,node):
        pass

    @visitor.when(TypeNode)
    def visit(self,node):
        pass

    @visitor.when(DataNode)
    def visit(self,node):
        pass

    @visitor.when(ParamNode)
    def visit(self,node):
        pass

    @visitor.when(LocalNode)
    def visit(self,node):
        pass

    @visitor.when(GetAttribNode)
    def visit(self,node):
        pass

    @visitor.when(SetAttribNode)
    def visit(self,node):
        pass

    @visitor.when(AssignNode)
    def visit(self,node):
        pass

    @visitor.when(ComplementNode)
    def visit(self,node):
        pass

    @visitor.when(NotNode)
    def visit(self,node):
        pass

    @visitor.when(PlusNode)
    def visit(self,node):
        pass

    @visitor.when(MinusNode)
    def visit(self,node):
        pass

    @visitor.when(StarNode)
    def visit(self,node):
        pass

    @visitor.when(DivNode)
    def visit(self,node):
        pass

    @visitor.when(EqualNode)
    def visit(self,node):
        pass

    @visitor.when(LessEqNode)
    def visit(self,node):
        pass

    @visitor.when(LessNode)
    def visit(self,node):
        pass

    @visitor.when(AllocateNode)
    def visit(self,node):
        pass

    @visitor.when(TypeOfNode)
    def visit(self,node):
        pass

    @visitor.when(LabelNode)
    def visit(self,node):
        pass

    @visitor.when(GotoNode)
    def visit(self,node):
        pass

    @visitor.when(IfGotoNode)
    def visit(self,node):
        pass

    @visitor.when(StaticCallNode)
    def visit(self,node):
        pass

    @visitor.when(DynamicCallNode)
    def visit(self,node):
        pass

    @visitor.when(ArgNode)
    def visit(self,node):
        pass

    @visitor.when(ErrorNode)
    def visit(self,node):
        pass

    @visitor.when(CopyNode)
    def visit(self,node):
        pass

    @visitor.when(TypeNameNode)
    def visit(self,node):
        pass

    @visitor.when(LengthNode)
    def visit(self,node):
        pass

    @visitor.when(ConcatNode)
    def visit(self,node):
        pass

    @visitor.when(StringEqualNode)
    def visit(self,node):
        pass

    @visitor.when(ConcatNode)
    def visit(self,node):
        pass

    @visitor.when(LoadNode)
    def visit(self,node):
        pass

    @visitor.when(SubstringNode)
    def visit(self,node):
        pass

    @visitor.when(ToStrNode)
    def visit(self,node):
        pass

    @visitor.when(ToIntNode)
    def visit(self,node):
        pass

    @visitor.when(ReadNode)
    def visit(self,node):
        pass

    @visitor.when(PrintNode)
    def visit(self,node):
        pass

    @visitor.when(ReturnNode)
    def visit(self,node):
        pass
    