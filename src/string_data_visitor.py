from visitor_helper import *
from ast import *

# se utiliza para encontrar cadenas de caracteres en el texto y devolverlas
class FormatVisitorS(object):
    @on('node')
    def visit(self, node, tabs):
        pass
    
    @when(ProgramNode)
    def visit(self, node, tabs=0):  
        result = []
        for c in node.classes:
            result += self.visit(c)
        return result
    
    @when(ClassNode)
    def visit(self, node, tabs=0):
        result = []
        for f in node.features:
            result += self.visit(f)
        return result
    
    @when(AttributeFeatureNode)
    def visit(self, node, tabs=0):
        return self.visit(node.expression)

    @when(FunctionFeatureNode)
    def visit(self, node, tabs=0):
        return self.visit(node.statement)

    @when(ParameterNode)
    def visit(self, node, tabs=0):
        return []

    @when(AssignStatementNode)
    def visit(self, node, tabs=0):
        return self.visit(node.expression)

    @when(ConditionalStatementNode)
    def visit(self, node, tabs=0):
        return self.visit(node.evalExpr) + self.visit(node.ifExpr) + self.visit(node.elseExpr)

    @when(LoopStatementNode)
    def visit(self, node, tabs=0):
        return self.visit(node.evalExpr) + self.visit(node.loopExpr)

    @when(BlockStatementNode)
    def visit(self, node, tabs=0):
        result = []
        for e in node.expressions:
            result += self.visit(e)
        return result
    
    @when(LetStatementNode)
    def visit(self, node, tabs=0):
        result = []
        for v in node.variables:
            result += self.visit(v)
        return result + self.visit(node.expression)

    @when(CaseStatementNode)
    def visit(self, node, tabs=0):
        result = []
        for cs in node.body:
            result += self.visit(cs)
        return self.visit(node.expression) + result

    @when(CaseBranchNode)
    def visit(self, node, tabs=0):
        return self.visit(node.expression)

    @when(NewStatementNode)
    def visit(self, node, tabs=0):
        return []

    @when(FunctionCallStatement)
    def visit(self, node, tabs=0):
        result = []
        for arg in node.args:
            result += self.visit(arg)
        return self.visit(node.instance) + result

    @when(ConstantNumericNode)
    def visit(self, node, tabs=0):
        return []

    @when(ConstantStringNode)
    def visit(self, node, tabs=0):
        return [node]

    @when(ConstantBoolNode)
    def visit(self, node, tabs=0):
        return []

    @when(VariableNode)
    def visit(self, node, tabs=0):
        return []

    @when(NotNode)
    def visit(self, node, tabs=0):
        return self.visit(node.expression)
    
    @when(IsVoidNode)
    def visit(self, node, tabs=0):
        return self.visit(node.expression)

    @when(ComplementNode)
    def visit(self, node, tabs=0):
        return self.visit(node.expression)

    @when(LessEqualNode)
    def visit(self, node, tabs=0):
        return self.visit(node.left) + self.visit(node.right)

    @when(LessNode)
    def visit(self, node, tabs=0):
        return self.visit(node.left) + self.visit(node.right)
    
    @when(EqualNode)
    def visit(self, node, tabs=0):
        return self.visit(node.left) + self.visit(node.right)

    @when(PlusNode)
    def visit(self, node, tabs=0):
        return self.visit(node.left) + self.visit(node.right)

    @when(MinusNode)
    def visit(self, node, tabs=0):
        return self.visit(node.left) + self.visit(node.right)

    @when(TimesNode)
    def visit(self, node, tabs=0):
        return self.visit(node.left) + self.visit(node.right)

    @when(DivideNode)
    def visit(self, node, tabs=0):
        return self.visit(node.left) + self.visit(node.right)
