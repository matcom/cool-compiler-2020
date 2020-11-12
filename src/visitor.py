from visitor_helper import *
from ast import *


class FormatVisitor(object):
    @on('node')
    def visit(self, node, tabs):
        pass
    
    @when(ProgramNode)
    def visit(self, node, tabs=0):  
        buff = ""
        buff += "ProgramNode"
        for child in node.classes:
            buff += "\n"
            buff += self.visit(child, tabs + 1)
        
        return buff
    
    @when(ClassNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ClassNode"
        buff += " " + node.typeName
        
        for feature in node.features:
            buff += "\n"
            buff += self.visit(feature, tabs + 1)
        
        return buff
    
    @when(AttributeFeatureNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "AttributeFeatureNode " + node.id
        if node.expression != None:
            buff += "\n"
            buff += self.visit(node.expression, tabs + 1)

        return buff

    @when(FunctionFeatureNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "FunctionFeatureNode " + node.id
        for parameter in node.parameters:
            buff += "\n"
            buff += self.visit(parameter, tabs + 1)
        buff += "\n"
        buff += self.visit(node.statement, tabs + 1)

        return buff

    @when(ParameterNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ParameterNode " + node.id

        return buff

    @when(AssignStatementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "AssignStatementNode"
        if node.expression != None:
            buff += "\n"
            buff += self.visit(node.expression, tabs + 1)

        return buff

    @when(ConditionalStatementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ConditionalStatementNode"
        if node.evalExpr != None:
            buff += "\n"
            buff += self.visit(node.evalExpr, tabs + 1)
        if node.ifExpr != None:
            buff += "\n"
            buff += self.visit(node.ifExpr, tabs + 1)
        if node.elseExpr != None:
            buff += "\n"
            buff += self.visit(node.elseExpr, tabs + 1)

        return buff

    @when(LoopStatementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "LoopStatementNode"

        if node.evalExpr != None:
            buff += "\n"
            buff += self.visit(node.evalExpr, tabs + 1)
        if node.loopExpr != None:
            buff += "\n"
            buff += self.visit(node.loopExpr, tabs + 1)

        return buff

    @when(BlockStatementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "BlockStatementNode"

        for expression in node.expressions:
            buff += "\n"
            buff += self.visit(expression, tabs + 1)

        return buff
    
    @when(LetStatementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "LetStatementNode"

        for variable in node.variables:
            buff += "\n"
            buff += self.visit(variable, tabs + 1)
        
        if node.expression != None:
            buff += "\n"
            buff += self.visit(node.expression, tabs + 1)

        return buff

    @when(CaseStatementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "CaseStatementNode"

        if node.expression != None:
            buff += "\n"
            buff += self.visit(node.expression, tabs + 1)

        for case in node.cases:
            buff += "\n"
            buff += self.visit(case, tabs + 1)

        return buff

    @when(CaseBranchNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "CaseBranchNode"

        if node.expression != None:
            buff += "\n"
            buff += self.visit(node.expression, tabs + 1)

        return buff

    @when(NewStatementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "NewStatementNode"

        return buff

    @when(FunctionCallStatement)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "FunctionCallStatement"

        if node.instance != None:
            buff += "\n"
            buff += self.visit(node.instance, tabs + 1)

        return buff

    @when(ConstantNumericNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ConstantNumericNode"

        return buff

    @when(ConstantStringNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ConstantStringNode"

        return buff

    @when(ConstantBoolNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ConstantBoolNode"

        return buff

    @when(VariableNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "VariableNode"

        return buff

    @when(NotNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "NotNode"

        buff += "\n"
        buff += self.visit(node.expression, tabs + 1)

        return buff
    
    @when(IsVoidNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "IsVoidNode"

        buff += "\n"
        buff += self.visit(node.expression, tabs + 1)

        return buff

    @when(ComplementNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ComplementNode"

        buff += "\n"
        buff += self.visit(node.expression, tabs + 1)

        return buff

    @when(LessEqualNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "LessEqualNode"

        buff += "\n"
        buff += self.visit(node.left, tabs + 1)

        buff += "\n"
        buff += self.visit(node.right, tabs + 1)

        return buff

    @when(LessNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "LessNode"

        buff += "\n"
        buff += self.visit(node.left, tabs + 1)

        buff += "\n"
        buff += self.visit(node.right, tabs + 1)

        return buff
    
    @when(EqualNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "EqualNode"

        buff += "\n"
        buff += self.visit(node.left, tabs + 1)

        buff += "\n"
        buff += self.visit(node.right, tabs + 1)

        return buff

    @when(PlusNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "PlusNode"

        buff += "\n"
        buff += self.visit(node.left, tabs + 1)

        buff += "\n"
        buff += self.visit(node.right, tabs + 1)

        return buff

    @when(MinusNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "MinusNode"

        buff += "\n"
        buff += self.visit(node.left, tabs + 1)

        buff += "\n"
        buff += self.visit(node.right, tabs + 1)

        return buff

    @when(TimesNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "TimesNode"

        buff += "\n"
        buff += self.visit(node.left, tabs + 1)

        buff += "\n"
        buff += self.visit(node.right, tabs + 1)

        return buff

    @when(DivideNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "DivideNode"

        buff += "\n"
        buff += self.visit(node.left, tabs + 1)

        buff += "\n"
        buff += self.visit(node.right, tabs + 1)

        return buff
