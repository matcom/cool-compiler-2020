import sys
sys.path.append('/..')
from nodesIL import *
from virtual_table import VirtualTable
from variables import Variables
import visitor
from ..cl_ast import *

class codeVisitor:

    def __init__(self):
        #code IL
        self.code = []
        self.data = []

        self.count = 0
        self.current_class = 'Main'

        self.virtual_table = VirtualTable()

    def getInt(self):
        self.count = self.count + 1
        return self.count 

    def collectTypes(self):
        pass

    def setInitialCode(self):
        self.code.append(CommentIL('--------------Initial Code---------------'))
        self.code.append(LabelIL("main", ""))
        
        self.append(PushIL())
        self.append(PushIL())
        self.append(PushIL())

        self.code.append(AllocateIL(1, self.vt.get_index('Main'), 'Main'))
        self.code.append(DispatchParentIL(2, 1, 'Main.Constructor'))

        self.code.append(DispatchIL(3,1,self.virtual_table.get_method_id('Main', 'main')))

        self.code.append(GotoIL("Object.abort"))

    def setBuiltInTypes(self):
        built_in = ['Object', 'IO', 'Bool', 'String']
        for t in built_in:
            self.code.append(LabelIL(t, 'Constructor', True))
            self.code.append(PushIL())
            self.append(ReturnIL())

    def setClassConstructor(self, attributes):
        self.code.append(LabelIL(self.current_class, 'Constructor', True))

        vars = Variables()
        vars.add_var('self')
        vars.add_temp()

        for node in attributes:
            if node.value == None:
                continue
            self.visit(node.value, vars)
            p = vars.peek_last()
            index = self.virtual_table.get_attributes_id(self.current_class, node.name.value)
            self.code.append(VarToMemoIL(vars.id('self'), vars.id(p), index)))

        self.code.append(PushIL())
        self.code.append(ReturnIL())


    def handleBinaryOps(self, node, variables, symbol):
        self.code.append(CommentIL('Binary'))
        self.code.append(PushIL())
        res = variables.add_temp()

        self.visit(node.left, variables)
        left = variables.peek_last()
        self.visit(node.right, variables)
        right = variables.peek_last()

        self.code.append(BinaryOperationIL(variables.id(res), variables.id(left), variables.id(right), symbol))

        variables.pop_var()
        variables.pop_var()
        self.code.append(PopIL(2))

    def handleUnaryOps(self, node, variables, symbol):
        self.code.append(CommentIL('Unary'))
        res = variables.add_tmp()
        self.code.append(PushIL())

        self.visit(node.expr, variables)
        v = variables.peek_last()

        self.code.append(UnaryOperationIL(variables.id(res), variables.id(v), symbol))
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    #program
    @visitor.on(ProgramNode)
    def visit(self, node):
        self.visit(node.declarations)
    
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


    




