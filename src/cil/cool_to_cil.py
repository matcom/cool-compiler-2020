from ..cool_lang import ast as cool

from .ast import ProgramNode, TypeNode, FunctionNode, ParamNode, LocalNode, AssignNode, PlusNode \
    , MinusNode, StarNode, DivNode, AllocateNode, TypeOfNode, StaticCallNode, DynamicCallNode    \
    , ArgNode, ReturnNode, ReadNode, PrintNode, LoadNode, LengthNode, ConcatNode, PrefixNode     \
    , SubstringNode, ToStrNode, GetAttribNode, SetAttribNode, LabelNode, GotoNode, GotoIfNode    \
    , DataNode

from .basic_transform import BASE_COOL_CIL_TRANSFORM, VariableInfo
from .utils import when, on


class COOL_TO_CIL_VISITOR(BASE_COOL_CIL_TRANSFORM):
    @on('node')
    def visit(self, node):
        pass

    @when(cool.cool.ProgramNode)
    def visit(self, node:cool.ProgramNode=None):
        pass
        
    @when(cool.cool.ClassDeclarationNode)
    def visit(self, node:cool.ClassDeclarationNode):
        pass

    @when(cool.cool.AttrDeclarationNode)
    def visit(self, node:cool.AttrDeclarationNode):
        pass

    @when(cool.cool.FuncDeclarationNode)
    def visit(self, node:cool.FuncDeclarationNode):
        pass


    @when(cool.cool.IfThenElseNode)
    def visit(self, node:cool.IfThenElseNode):
        pass

    @when(cool.cool.WhileLoopNode)
    def visit(self, node:cool.WhileLoopNode):
        pass

    @when(cool.cool.BlockNode)
    def visit(self, node:cool.BlockNode):
        pass

    @when(cool.cool.LetNode)
    def visit(self, node:cool.LetNode):
        pass
        
    @when(cool.LetInNode)
    def visit(self, node:cool.LetInNode):
        pass

    @when(cool.CaseNode)
    def visit(self, node:cool.CaseNode):
        pass

    @when(cool.CaseOfNode)
    def visit(self, node:cool.CaseOfNode):
        pass

    @when(cool.AssignNode)
    def visit(self, node:cool.AssignNode):
        pass
    
    @when(cool.MemberCallNode)
    def visit(self, node:cool.MemberCallNode):
        pass

    @when(cool.FunctionCallNode)
    def visit(self, node:cool.FunctionCallNode):
        pass

    @when(cool.NewNode)
    def visit(self, node:cool.NewNode):
        pass

    @when(cool.IsVoidNode)
    def visit(self, node:cool.IsVoidNode):
        pass

    @when(cool.NotNode)
    def visit(self, node:cool.NotNode):
        pass

    @when(cool.ComplementNode)
    def visit(self, node:cool.ComplementNode):
        pass

    @when(cool.ArithmeticNode)
    def visit(self, node:cool.ArithmeticNode):
        pass

    @when(cool.EqualNode)
    def visit(self, node:cool.EqualNode):
        pass

    @when(cool.LessEqualNode)
    def visit(self, node:cool.LessEqualNode):
        pass

    @when(cool.LessNode)
    def visit(self, node:cool.LessNode):
        pass
        
    @when(cool.IdNode)
    def visit(self, node:cool.IdNode):
        pass

    @when(cool.BoolNode)
    def visit(self, node:cool.BoolNode):
        pass

    @when(cool.IntegerNode)
    def visit(self, node:cool.IntegerNode):
        pass

    @when(cool.StringNode)
    def visit(self, node:cool.StringNode):
        pass
