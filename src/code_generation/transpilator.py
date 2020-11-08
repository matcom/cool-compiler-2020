import sys
sys.path.append('/..')
from .nodesIL import *
from .virtual_table import VirtualTable
from ..visitors import visitor
from ..cl_ast import *

class codeVisitor:

    def __init__(self):
        #code IL
        self.code = []
        self.data = []

        self.count = 0

        self.virtual_table = VirtualTable()

    def getInt(self):
        self.count = self.count + 1
        return self.count 

    def collectTypes(self):
        pass

    def setInitialCode(self):
        pass
    
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    #program
    @visitor.on(ProgramNode)
    def visit(self, node):
        pass
    
    #declarations
    @visitor.on(ClassDeclarationNode)
    def visit(self, node):
        pass

    @visitor.on(AttrDeclarationNode)
    def visit(self, node):
        pass

    @visitor.on(FuncDeclarationNode)
    def visit(self, node):
        pass

    @visitor.on(VarDeclarationNode)
    def visit(self, node):
        pass

    #operations: binary
    @visitor.on(SumNode)
    def visit(self, node):
        pass

    @visitor.on(DiffNode)
    def visit(self, node):
        pass

    @visitor.on(StarNode)
    def visit(self, node):
        pass

    @visitor.on(DivNode)
    def visit(self, node):
        pass

    @visitor.on(LessNode)
    def visit(self, node):
        pass

    @visitor.on(LessEqualNode)
    def visit(self, node):
        pass

    @visitor.on(EqualNode)
    def visit(self, node):
        pass

    #operations: unary

    @visitor.on(BitNotNode)
    def visit(self, node):
        pass

    @visitor.on(NotNode)
    def visit(self, node):
        pass

    #expressions: atomics
    @visitor.on(VariableNode)
    def visit(self, node):
        pass

    @visitor.on(NewNode)
    def visit(self, node):
        pass

    #expressions: complex
    @visitor.on(ConditionalNode)
    def visit(self, node):
        pass

    @visitor.on(WhileNode)
    def visit(self, node):
        pass

    @visitor.on(LetNode)
    def visit(self, node):
        pass

    @visitor.on(LetDeclarationNode)
    def visit(self, node):
        pass

    @visitor.on(BlockNode)
    def visit(self, node):
        pass

    @visitor.on(CaseNode)
    def visit(self, node):
        pass

    @visitor.on(OptionNode)
    def visit(self, node):
        pass

    @visitor.on(AssignNode)
    def visit(self, node):
        pass

    @visitor.on(IsVoidNode)
    def visit(self, node):
        pass

    #expression: complex->dispatch
    @visitor.on(ExprCallNode)
    def visit(self, node):
        pass

    @visitor.on(SelfCallNode)
    def visit(self, node):
        pass

    @visitor.on(ParentCallNode)
    def visit(self, node):
        pass

    #constants
    @visitor.on(IntegerNode)
    def visit(self, node):
        pass

    @visitor.on(StringNode)
    def visit(self, node):
        pass

    @visitor.on(BoolNode)
    def visit(self, node):
        pass


    




