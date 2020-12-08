# Generated from COOL.g4 by ANTLR 4.7.2
from collections import deque
from antlr4 import *
# if __name__ is not None and "." in __name__:
#     from .COOL import COOL
# else:
#     from COOL import COOL

from COOL import *

from  src import COOLParser

# This class defines a complete generic visitor for a parse tree produced by COOL.
class COOLVisitor(ParseTreeVisitor):


    # Visit a parse tree produced by COOL#program.
    def visitProgram(self, ctx:COOL.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#classes.
    def visitClasses(self, ctx:COOL.ClassesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#classDefine.
    def visitClassDefine(self, ctx:COOL.ClassDefineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#method.
    def visitMethod(self, ctx:COOL.MethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#property.
    def visitProperty(self, ctx:COOL.PropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#formal.
    def visitFormal(self, ctx:COOL.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#letIn.
    def visitLetIn(self, ctx:COOL.LetInContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#minus.
    def visitMinus(self, ctx:COOL.MinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#string.
    def visitString(self, ctx:COOL.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#isvoid.
    def visitIsvoid(self, ctx:COOL.IsvoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#while.
    def visitWhile(self, ctx:COOL.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#division.
    def visitDivision(self, ctx:COOL.DivisionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#negative.
    def visitNegative(self, ctx:COOL.NegativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#boolNot.
    def visitBoolNot(self, ctx:COOL.BoolNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#lessThan.
    def visitLessThan(self, ctx:COOL.LessThanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#block.
    def visitBlock(self, ctx:COOL.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#id.
    def visitId(self, ctx:COOL.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#multiply.
    def visitMultiply(self, ctx:COOL.MultiplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#if.
    def visitIf(self, ctx:COOL.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#case.
    def visitCase(self, ctx:COOL.CaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#ownMethodCall.
    def visitOwnMethodCall(self, ctx:COOL.OwnMethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#add.
    def visitAdd(self, ctx:COOL.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#new.
    def visitNew(self, ctx:COOL.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#parentheses.
    def visitParentheses(self, ctx:COOL.ParenthesesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#assignment.
    def visitAssignment(self, ctx:COOL.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#false.
    def visitFalse(self, ctx:COOL.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#int.
    def visitInt(self, ctx:COOL.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#equal.
    def visitEqual(self, ctx:COOL.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#true.
    def visitTrue(self, ctx:COOL.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#lessEqual.
    def visitLessEqual(self, ctx:COOL.LessEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by COOL#methodCall.
    def visitMethodCall(self, ctx:COOL.MethodCallContext):
        return self.visitChildren(ctx)

class SemanticCOOLVisitor(ParseTreeVisitor):

    def join(self, class1: str, class2: str):
        if class1 == "None" or class2 == "None":
            return "None"
        if self.TypeTable[class1].Deep == self.TypeTable[class2].Deep:
            if self.TypeTable[class1].Name == self.TypeTable[class2].Name:
                return class1
            else:
                return self.join(self.TypeTable[class1].Parent, self.TypeTable[class2].Parent)
        elif self.TypeTable[class1].Deep > self.TypeTable[class2].Deep:
            return self.join(self.TypeTable[class1].Parent, class2)
        else:
            return self.join(class1, self.TypeTable[class2].Parent)

    def calculateDeep(self, coolClass: COOLClass):
        if self.TypeTable.keys().__contains__(coolClass.Parent):
            if self.TypeTable[coolClass.Parent].Deep != -1:
                coolClass.Deep = self.TypeTable[coolClass.Parent].Deep + 1
            else:
                self.calculateDeep(self.TypeTable[coolClass.Parent])
                coolClass.Deep = self.TypeTable[coolClass.Parent].Deep + 1
        elif coolClass.Name == "Object":
                coolClass.Deep = 0
        else:
            coolClass.Deep = 1
            coolClass.Parent = "Object"

    def searchMethod(self, coolClass: str, methodName: str):
        if coolClass == "None":
            return False
        elif self.TypeTable[coolClass].Methods.keys().__contains__(methodName):
            return True
        else:
            return self.searchMethod(self.TypeTable[coolClass].Parent, methodName)

    def searchAtribute(self, coolClass: str, atributeName: str):
        if coolClass == "None":
            return False
        elif self.TypeTable[coolClass].Atributes.keys().__contains__(atributeName):
            return True
        else:
            return self.searchAtribute(self.TypeTable[coolClass].Parent, atributeName)

    def searchMethodInfo(self, coolClass: str, methodName: str):
        for method in self.TypeTable[coolClass].Methods.keys():
            if method == methodName:
                return self.TypeTable[coolClass].Methods[method]
        return self.searchMethodInfo(self.TypeTable[coolClass].Parent, methodName)

    def searchAtributeInfo(self, coolClass: str, atributeName: str):
        for atribute in self.TypeTable[coolClass].Atributes.keys():
            if atribute == atributeName:
                return self.TypeTable[coolClass].Atributes[atribute]
        return self.searchAtributeInfo(self.TypeTable[coolClass].Parent, atributeName)


    def __init__(self, typeTable: dict):
        self.TypeTable = typeTable
        self.ScopeManager = COOLScopeManager()
        self.actualClass = "Object"

    # Visit a parse tree produced by COOL#program.
    def visitProgram(self, ctx:COOL.ProgramContext):
        for className in self.TypeTable.keys():
            self.calculateDeep(self.TypeTable[className])
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classes.
    def visitClasses(self, ctx:COOL.ClassesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classDefine.
    def visitClassDefine(self, ctx:COOL.ClassDefineContext):
        coolClass = ctx.getChild(1).symbol
        if(self.TypeTable[coolClass.text].Created):
            line = str(coolClass.line)
            column = str(coolClass.column)
            error = "(" + line + "," + column + "): this class name already exist"
            print(error)
        elif ctx.getChild(2).symbol.text == "inherits":
            classParent = ctx.getChild(3).symbol
            if (self.TypeTable.keys().__contains__(classParent.text)):
                if self.TypeTable[classParent.text].Sealed:
                    line = str(classParent.line)
                    column = str(classParent.column)
                    error = "(" + line + "," + column + "): this class is sealed"
                    print(error)
                else:
                    self.TypeTable[coolClass.text].Created = True
                    self.TypeTable[coolClass.text].Sealed = False
                    self.ScopeManager.addScope()
                    self.ScopeManager.addIdentifier("self", coolClass.text)
                    self.actualClass = coolClass.text
                    self.visitChildren(ctx)
                    self.ScopeManager.deleteScope()
                    return
            else:
                line = str(classParent.line)
                column = str(classParent.column)
                error = "(" + line + "," + column + "): this class doesn't exist"
                print(error)
        else:
            self.TypeTable[coolClass.text].Created = True
            self.TypeTable[coolClass.text].Sealed = False
            self.ScopeManager.addScope()
            self.actualClass = coolClass.text
            self.ScopeManager.addIdentifier("self", coolClass.text)
            self.visitChildren(ctx)
            self.ScopeManager.deleteScope()
            return

    # Visit a parse tree produced by COOL#method.
    def visitMethod(self, ctx:COOL.MethodContext):
        coolClass = ctx.parentCtx.getChild(1).symbol.text
        methodName = ctx.getChild(0).symbol.text
        methodType =  ctx.getChild(len(ctx.children) - 4).symbol
        if self.ScopeManager.searchScope(methodName):
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column)
            error = "(" + line + "," + column + "): this method name already exist"
            print(error)
        elif self.TypeTable.keys().__contains__(self.TypeTable[coolClass].Methods[methodName].Type) or methodType.text == "SELF_TYPE":
            self.ScopeManager.addIdentifier(methodName, methodType.text)
            self.ScopeManager.addScope()
            self.visitChildren(ctx)
            self.ScopeManager.deleteScope()
            return
        else:
            line = str(methodType.line)
            column = str(methodType.column)
            error = "(" + line + "," + column + "): this type doesn't exist"
            print(error)

    # Visit a parse tree produced by COOL#property.
    def visitProperty(self, ctx:COOL.PropertyContext):
        atributeType = ctx.getChild(2).symbol.text
        atributeName = ctx.getChild(0).symbol.text
        if self.ScopeManager.searchScope(atributeName):
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column)
            error = "(" + line + "," + column + "): this atribute name already exist"
            print(error)
            return "None"
        elif not(self.TypeTable.keys().__contains__(atributeType) or atributeType == "SELF_TYPE"):
            line = str(ctx.getChild(2).symbol.line)
            column = str(ctx.getChild(2).symbol.column)
            error = "(" + line + "," + column + "): this type doesn't exist"
            print(error)
            return "None"
        elif len(ctx.children) == 5:
            atributeValue = ctx.getChild(4).accept(self)
            if self.join(atributeType, atributeValue) != atributeType:
                line = str(ctx.getChild(4).start.line)
                column = str(ctx.getChild(4).start.column)
                error = "(" + line + "," + column + "): the type of the expression is diferent of the type of the atribute"
                print(error)
                return "None"
            else:
                self.ScopeManager.addIdentifier(atributeName, atributeType)
                return atributeType
        else:
            self.ScopeManager.addIdentifier(atributeName, atributeType)
            return atributeType

    # Visit a parse tree produced by COOL#formal.
    def visitFormal(self, ctx:COOL.FormalContext):
        paramName = ctx.getChild(0).symbol.text
        paramType = ctx.getChild(2).symbol.text
        if self.ScopeManager.searchScope(paramName):
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column)
            error = "(" + line + "," + column + "): this param name already exist"
            print(error)
        elif self.TypeTable.keys().__contains__(paramType):
            self.ScopeManager.addIdentifier(paramName, paramType)
            return self.visitChildren(ctx)
        else:
            line = str(ctx.getChild(2).symbol.line)
            column = str(ctx.getChild(2).symbol.column)
            error = "(" + line + "," + column + "): this type doesn't exist"
            print(error)

    # Visit a parse tree produced by COOL#int.
    def visitInt(self, ctx: COOL.IntContext):
        return "Int"

    # Visit a parse tree produced by COOL#string.
    def visitString(self, ctx: COOL.StringContext):
        return "String"

    # Visit a parse tree produced by COOL#false.
    def visitFalse(self, ctx: COOL.FalseContext):
        return "Bool"

    # Visit a parse tree produced by COOL#true.
    def visitTrue(self, ctx: COOL.TrueContext):
        return "Bool"

    # Visit a parse tree produced by COOL#add.
    def visitAdd(self, ctx: COOL.AddContext):
        addValue = "Int"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int":
            line = str(ctx.getChild(0).start.line)
            column = str(ctx.getChild(0).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            addValue = "None"
        if rightValue != "Int":
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            addValue = "None"
        return addValue

    # Visit a parse tree produced by COOL#minus.
    def visitMinus(self, ctx:COOL.MinusContext):
        minusValue = "Int"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int":
            line = str(ctx.getChild(0).start.line)
            column = str(ctx.getChild(0).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            minusValue = "None"
        if rightValue != "Int":
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            minusValue = "None"
        return minusValue

     # Visit a parse tree produced by COOL#multiply.
    def visitMultiply(self, ctx: COOL.MultiplyContext):
        mulValue = "Int"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int":
            line = str(ctx.getChild(0).start.line)
            column = str(ctx.getChild(0).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            mulValue = "None"
        if rightValue != "Int":
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            mulValue = "None"
        return mulValue

    # Visit a parse tree produced by COOL#division.
    def visitDivision(self, ctx: COOL.DivisionContext):
        divValue = "Int"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int":
            line = str(ctx.getChild(0).start.line)
            column = str(ctx.getChild(0).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            divValue = "None"
        if rightValue != "Int":
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            divValue = "None"
        return divValue

    # Visit a parse tree produced by COOL#negative.
    def visitNegative(self, ctx: COOL.NegativeContext):
        expressValue = ctx.getChild(1).accept(self)
        if expressValue == "Int":
            return "Int"
        return "None"

    # Visit a parse tree produced by COOL#isvoid.
    def visitIsvoid(self, ctx:COOL.IsvoidContext):
        self.visitChildren(ctx)
        return "Bool"

    # Visit a parse tree produced by COOL#boolNot.
    def visitBoolNot(self, ctx: COOL.BoolNotContext):
        expressValue = ctx.getChild(1).accept(self)
        if expressValue == "Bool":
            return "Bool"
        return "None"

    # Visit a parse tree produced by COOL#lessThan.
    def visitLessThan(self, ctx:COOL.LessThanContext):
        lessValue = "Bool"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int":
            line = str(ctx.getChild(0).start.line)
            column = str(ctx.getChild(0).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            lessValue = "None"
        if rightValue != "Int":
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            lessValue = "None"
        return lessValue

    # Visit a parse tree produced by COOL#lessEqual.
    def visitLessEqual(self, ctx:COOL.LessEqualContext):
        lessEqualValue = "Bool"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int":
            line = str(ctx.getChild(0).start.line)
            column = str(ctx.getChild(0).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            lessEqualValue = "None"
        if rightValue != "Int":
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is not integer"
            print(error)
            lessEqualValue = "None"
        return lessEqualValue

    # Visit a parse tree produced by COOL#equal.
    def visitEqual(self, ctx: COOL.EqualContext):
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue == "None" or rightValue == "None":
            return "None"
        if leftValue == rightValue:
            return "Bool"
        if leftValue == "String" or leftValue == "Int" or leftValue == "Bool":
            line = str(ctx.getChild(0).start.line)
            column = str(ctx.getChild(0).start.column)
            error = "(" + line + "," + column + "): the type of the expression is incorrect"
            print(error)
            return "None"
        if rightValue == "String" or rightValue == "Int" or rightValue == "Bool":
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is incorrect"
            print(error)
            return "None"
        return "Bool"

    # Visit a parse tree produced by COOL#assignment.
    def visitAssignment(self, ctx: COOL.AssignmentContext):
        variableName = ctx.getChild(0).symbol.text
        asignValue = ctx.getChild(2).accept(self)
        variableType = self.ScopeManager.searchforType(variableName)
        if variableType == "None":
            if self.searchAtribute(self.actualClass, variableName):
                variableType = self.searchAtributeInfo(self.actualClass, variableName)
            else:
                line = str(ctx.getChild(0).symbol.line)
                column = str(ctx.getChild(0).symbol.column)
                error = "(" + line + "," + column + "): this identifier does not exist"
                print(error)
                return "None"
        if variableType == "SELF_TYPE":
            variableType = self.actualClass
        if  self.join(asignValue, variableType) != variableType:
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column)
            error = "(" + line + "," + column + "): the type of the expression is diferent that the identifier"
            print(error)
            return "None"
        return variableType

    # Visit a parse tree produced by COOL#parentheses.
    def visitParentheses(self, ctx: COOL.ParenthesesContext):
        return ctx.getChild(1).accept(self)

    # Visit a parse tree produced by COOL#id.
    def visitId(self, ctx: COOL.IdContext):
        IdValue = ctx.getChild(0).symbol.text
        if self.ScopeManager.searchIdentifier(IdValue):
            return self.ScopeManager.searchforType(IdValue)
        elif self.searchAtribute(self.actualClass, IdValue):
            return self.searchAtributeInfo(self.actualClass, IdValue)
        line = str(ctx.getChild(0).symbol.line)
        column = str(ctx.getChild(0).symbol.column)
        error = "(" + line + "," + column + "): this identifier does not exist"
        print(error)
        return "None"

    # Visit a parse tree produced by COOL#if.
    def visitIf(self, ctx:COOL.IfContext):
        ifValue = ctx.getChild(1).accept(self)
        thenValue = ctx.getChild(3).accept(self)
        elseValue = ctx.getChild(5).accept(self)
        if ifValue == "None" or ifValue == "Bool":
            return self.join(thenValue, elseValue)
        else:
            line = str(ctx.getChild(1).start.line)
            column = str(ctx.getChild(1).start.column)
            error = "(" + line + "," + column + "): this expression is not boolean"
            print(error)
            return self.join(thenValue, elseValue)

    # Visit a parse tree produced by COOL#while.
    def visitWhile(self, ctx: COOL.WhileContext):
        whileValue = ctx.getChild(3).accept(self)
        whileValue = ctx.getChild(1).accept(self)
        if whileValue == "None" or whileValue == "Bool":
            return "Object"
        else:
            line = str(ctx.getChild(1).start.line)
            column = str(ctx.getChild(1).start.column)
            error = "(" + line + "," + column + "): this expression is not boolean"
            print(error)
            return "Object"

    # Visit a parse tree produced by COOL#block.
    def visitBlock(self, ctx:COOL.BlockContext):
        blockValue = "None"
        count = 1
        lengt = len(ctx.children) - 1
        while lengt > count:
            blockValue = ctx.getChild(count).accept(self)
            count = count + 2
        return blockValue

    # Visit a parse tree produced by COOL#case.
    def visitCase(self, ctx:COOL.CaseContext):
        ctx.getChild(1).accept(self)
        lengt = len(ctx.children) - 1
        count = 3
        caseValue = "None"
        while lengt > count:
            idName = ctx.getChild(count).symbol.text
            count = count + 2
            idType = ctx.getChild(count).symbol.text
            count = count + 2
            self.ScopeManager.addScope()
            self.ScopeManager.addIdentifier(idName, idType)
            if (caseValue == "None"):
                caseValue = ctx.getChild(count).accept(self)
            else:
                caseValue = self.join(caseValue, ctx.getChild(count).accept(self))
            count = count + 2
            self.ScopeManager.deleteScope()
        return caseValue

    # Visit a parse tree produced by COOL#new.
    def visitNew(self, ctx: COOL.NewContext):
        return ctx.getChild(1).symbol.text

    # Visit a parse tree produced by COOL#ownMethodCall.
    def visitOwnMethodCall(self, ctx:COOL.OwnMethodCallContext):
        methodType = "None"
        if self.searchMethod(self.actualClass, ctx.getChild(0).symbol.text):
            methodInfo = self.searchMethodInfo(self.actualClass, ctx.getChild(0).symbol.text)
            if(methodInfo.Type == "SELF_TYPE"):
                methodType = self.actualClass
            else:
                methodType = methodInfo.Type
            if methodInfo.ParamsNumber == 0 and len(ctx.children) != 3:
                line = str(ctx.getChild(1).symbol.line)
                column = str(ctx.getChild(1).symbol.column)
                error = "(" + line + "," + column + "): the number of params in the call is incorrect"
                print(error)
                methodType = "None"
            elif len(ctx.children) != methodInfo.ParamsNumber * 2 + 2 and methodInfo.ParamsNumber != 0:
                line = str(ctx.getChild(1).symbol.line)
                column = str(ctx.getChild(1).symbol.column)
                error = "(" + line + "," + column + "): the number of params in the call is incorrect"
                print(error)
                methodType = "None"
            else:
                count = 2
                for param in methodInfo.Params:
                    (_,paramType) = param
                    requestType = ctx.getChild(count).accept(self)
                    if (self.join(requestType, paramType) != paramType):
                        line = str(ctx.getChild(count).start.line)
                        column = str(ctx.getChild(count).start.column)
                        error = "(" + line + "," + column + "): the type of this param in the call is incorrect"
                        print(error)
                        methodType = "None"
                    count = count + 2
        else:
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column)
            error = "(" + line + "," + column + "): this method not exist in " + self.actualClass
            print(error)
        return methodType

    # Visit a parse tree produced by COOL#methodCall.
    def visitMethodCall(self, ctx:COOL.MethodCallContext):
        methodType = "None"
        length = 5
        currentClass = ctx.getChild(0).accept(self)
        if (ctx.getChild(1).symbol.text == "@"):
            length = length + 2
            parent = ctx.getChild(2).symbol.text
            if self.join(currentClass, parent) == parent:
                currentClass = parent
            else:
                line = str(ctx.getChild(2).symbol.line)
                column = str(ctx.getChild(2).symbol.column)
                error = "(" + line + "," + column + "): this class is not parent of " + currentClass
                print(error)
                return methodType
        if self.searchMethod(currentClass, ctx.getChild(length - 3).symbol.text):
            methodInfo = self.searchMethodInfo(currentClass, ctx.getChild(length - 3).symbol.text)
            if (methodInfo.Type == "SELF_TYPE"):
                methodType = currentClass
            else:
                methodType = methodInfo.Type
            if (methodInfo.ParamsNumber == 0 and len(ctx.children) != length):
                line = str(ctx.getChild(length - 3).start.line)
                column = str(ctx.getChild(length - 3).start.column)
                error = "(" + line + "," + column + "): the number of params in the call is incorrect"
                print(error)
                methodType = "None"
            elif (len(ctx.children) != methodInfo.ParamsNumber * 2 + length - 1) and methodInfo.ParamsNumber > 0:
                line = str(ctx.getChild(length - 3).start.line)
                column = str(ctx.getChild(length - 3).start.column)
                error = "(" + line + "," + column + "): the number of params in the call is incorrect"
                print(error)
                methodType = "None"
            else:
                count = length - 1
                for param in methodInfo.Params:
                    (_, paramType) = param
                    requestType = ctx.getChild(count).accept(self)
                    if (self.join(requestType, paramType) != paramType):
                        line = str(ctx.getChild(count).start.line)
                        column = str(ctx.getChild(count).start.column)
                        error = "(" + line + "," + column + "): the type of this param in the call is incorrect"
                        print(error)
                        methodType = "None"
                    count = count + 2
        else:
            line = str(ctx.getChild(length - 3).symbol.line)
            column = str(ctx.getChild(length - 3).symbol.column)
            error = "(" + line + "," + column + "): this method not exist in " + currentClass
            print(error)
        return methodType

    # Visit a parse tree produced by COOL#letIn.
    def visitLetIn(self, ctx: COOL.LetInContext):
        self.ScopeManager.addScope()
        count = 0
        while(ctx.getChild(count).symbol.text != "in"):
            idName = ctx.getChild(count + 1).symbol.text
            count = count + 2
            idType = ctx.getChild(count + 1).symbol.text
            if not(self.TypeTable.keys().__contains__(idType)) and idType != "SELF_TYPE":
                self.ScopeManager.deleteScope()
                line = str(ctx.getChild(count + 1).symbol.line)
                column = str(ctx.getChild(count + 1).symbol.column)
                error = "(" + line + "," + column + "): this class does not exist "
                print(error)
                return "None"
            self.ScopeManager.addIdentifier(idName, idType)
            count = count + 2
            if ctx.getChild(count).symbol.text == "<-":
                idValue = ctx.getChild(count + 1).accept(self)
                count = count + 2
                if self.join(idType, idValue) != idType:
                    self.ScopeManager.deleteScope()
                    line = str(ctx.getChild(count -1).start.line)
                    column = str(ctx.getChild(count - 1).start.column)
                    error = "(" + line + "," + column + "): the type of the expression is diferent of the type of the identifier"
                    print(error)
                    return "None"

        return ctx.getChild(count + 1).accept(self)

class TypeCOOLVisitor(ParseTreeVisitor):

    TypeTable = {}

    Counter = 0

    ConstantTable = list()

    # Visit a parse tree produced by COOL#program.
    def visitProgram(self, ctx: COOL.ProgramContext):
        self.TypeTable["Object"] = COOLClass("Object", "None", True, False)
        self.TypeTable["Object"].Methods["abort"] = COOLMethod("abort", "Object", 0, None)
        self.TypeTable["Object"].Methods["type_name"] = COOLMethod("type_name", "String", 0, None)
        self.TypeTable["Object"].Methods["copy"] = COOLMethod("copy", "SELF_TYPE", 0, None)
        self.TypeTable["String"] = COOLClass("String", "Object", True, True)
        self.TypeTable["String"].Methods["length"] = COOLMethod("length", "Int", 0, None)
        self.TypeTable["String"].Methods["concat"] = COOLMethod("concat", "String", 1, None)
        self.TypeTable["String"].Methods["concat"].Params.append(("s", "String"))
        self.TypeTable["String"].Methods["substr"] = COOLMethod("substr", "String", 2, None)
        self.TypeTable["String"].Methods["substr"].Params.append(("i", "Int"))
        self.TypeTable["String"].Methods["substr"].Params.append(("l", "Int"))
        self.TypeTable["Int"] = COOLClass("Int", "Object", True, True)
        self.TypeTable["Bool"] = COOLClass("Bool", "Object", True, True)
        self.TypeTable["IO"] = COOLClass("IO", "Object", True, False)
        self.TypeTable["IO"].Methods["in_string"] = COOLMethod("in_string", "String", 0, None)
        self.TypeTable["IO"].Methods["in_int"] = COOLMethod("in_int", "Int", 0, None)
        self.TypeTable["IO"].Methods["out_string"] = COOLMethod("out_string", "SELF_TYPE", 1, None)
        self.TypeTable["IO"].Methods["out_string"].Params.append(("x", "String"))
        self.TypeTable["IO"].Methods["out_int"] = COOLMethod("out_int", "SELF_TYPE", 1, None)
        self.TypeTable["IO"].Methods["out_int"].Params.append(("x", "Int"))
        self.ConstantTable.append(("", "String", "string_const0"))
        self.Counter = 1
        self.ConstantTable.append((0, "Int", "int_const0"))
        self.ConstantTable.append(("false", "Bool", "bool_const0"))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classes.
    def visitClasses(self, ctx: COOL.ClassesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classDefine.
    def visitClassDefine(self, ctx: COOL.ClassDefineContext):
        coolClass = ctx.getChild(1).symbol
        if self.TypeTable.keys().__contains__(coolClass.text):
            return
        if ctx.getChild(2).symbol.text == "inherits":
            classParent = ctx.getChild(3).symbol
            self.TypeTable[coolClass.text] = COOLClass(coolClass.text, classParent.text, False, False)
            return self.visitChildren(ctx)
        else:
            self.TypeTable[coolClass.text] = COOLClass(coolClass.text, "Object", False, False)
            return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#method.
    def visitMethod(self, ctx: COOL.MethodContext):
        name = ctx.getChild(0).symbol.text
        cclass = ctx.parentCtx.getChild(1).symbol.text
        if self.TypeTable[cclass].Methods.keys().__contains__(name):
            return
        n = len(ctx.children) - 4
        if ctx.getChild(n).symbol.text == ":":
            n = n + 1
        type = ctx.getChild(n).symbol.text
        lengt = len(ctx.children) - 8
        paramsNumber = 0
        if lengt > 0:
            paramsNumber = 1
            while lengt > 1:
                lengt = lengt - 2
                paramsNumber = paramsNumber + 1
        self.TypeTable[cclass].Methods[name] = COOLMethod(name, type, paramsNumber, ctx.getChild(len(ctx.children) - 2))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#property.
    def visitProperty(self, ctx: COOL.PropertyContext):
        cclass = ctx.parentCtx.getChild(1).symbol.text
        name = ctx.getChild(0).symbol.text
        if self.TypeTable[cclass].Atributes.keys().__contains__(name):
            return
        type = ctx.getChild(2).symbol.text
        self.TypeTable[cclass].Atributes[name] = type
        if len(ctx.children) == 4:
            self.TypeTable[cclass].AtributeAsign[name] = ctx.getChild(4)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#formal.
    def visitFormal(self, ctx: COOL.FormalContext):
        parent = ctx.parentCtx

        className = parent.parentCtx.getChild(1).symbol.text
        methodName = parent.getChild(0).symbol.text
        method = self.TypeTable[className].Methods[methodName]
        for param in method.Params:
            (paramName, paramType) = param
            if (paramName == ctx.getChild(0).symbol.text):
                return
        method.Params.append((ctx.getChild(0).symbol.text, ctx.getChild(2).symbol.text))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#letIn.
    def visitLetIn(self, ctx: COOL.LetInContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#minus.
    def visitMinus(self, ctx: COOL.MinusContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#string.
    def visitString(self, ctx: COOL.StringContext):
        constantName = ctx.getChild(0).symbol.text[1:-1]
        for cons in self.ConstantTable:
            (consName, consType,_) = cons
            if consName == constantName and consType == "String":
                return self.visitChildren(ctx)

        self.ConstantTable.append((constantName, "String", f"str_const{self.Counter}"))
        self.Counter = self.Counter + 1
        length = len(constantName)
        for cons in self.ConstantTable:
            (consName, consType,_) = cons
            if consName == length and consType == "Int":
                return self.visitChildren(ctx)
        self.ConstantTable.append((length, "Int", f"int_const{length}"))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#isvoid.
    def visitIsvoid(self, ctx: COOL.IsvoidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#while.
    def visitWhile(self, ctx: COOL.WhileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#division.
    def visitDivision(self, ctx: COOL.DivisionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#negative.
    def visitNegative(self, ctx: COOL.NegativeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#boolNot.
    def visitBoolNot(self, ctx: COOL.BoolNotContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#lessThan.
    def visitLessThan(self, ctx: COOL.LessThanContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#block.
    def visitBlock(self, ctx: COOL.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#id.
    def visitId(self, ctx: COOL.IdContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#multiply.
    def visitMultiply(self, ctx: COOL.MultiplyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#if.
    def visitIf(self, ctx: COOL.IfContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#case.
    def visitCase(self, ctx: COOL.CaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#ownMethodCall.
    def visitOwnMethodCall(self, ctx: COOL.OwnMethodCallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#add.
    def visitAdd(self, ctx: COOL.AddContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#new.
    def visitNew(self, ctx: COOL.NewContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#parentheses.
    def visitParentheses(self, ctx: COOL.ParenthesesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#assignment.
    def visitAssignment(self, ctx: COOL.AssignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#false.
    def visitFalse(self, ctx: COOL.FalseContext):
        for cons in self.ConstantTable:
            (consName, consType, _) = cons
            if consName == "false" and consType == "Bool":
                return self.visitChildren(ctx)

        self.ConstantTable.append(("false", "Bool", "bool_const0"))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#int.
    def visitInt(self, ctx: COOL.IntContext):
        constantName = int(ctx.getChild(0).symbol.text)
        for cons in self.ConstantTable:
            (consName, consType,_) = cons
            if consName == constantName and consType == "Int":
                return self.visitChildren(ctx)

        self.ConstantTable.append((constantName, "Int", f"int_const{constantName}"))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#equal.
    def visitEqual(self, ctx: COOL.EqualContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#true.
    def visitTrue(self, ctx: COOL.TrueContext):
        for cons in self.ConstantTable:
            (consName, consType,_) = cons
            if consName == "true" and consType == "Bool":
                return self.visitChildren(ctx)

        self.ConstantTable.append(("true", "Bool","bool_const1"))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#lessEqual.
    def visitLessEqual(self, ctx: COOL.LessEqualContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#methodCall.
    def visitMethodCall(self, ctx: COOL.MethodCallContext):
        return self.visitChildren(ctx)

class CodegenVisitor(ParseTreeVisitor):

    def __init__(self, typeTable: dict, constantTable: list, counter: int):
        self.TypeTable = typeTable
        self.ConstantTable = constantTable
        self.Counter = counter


    def genGlobalClases(self):
        sol = "\t.data\n\t.align 2\n\t.global class_nameTab\n"
        for clasName in self.TypeTable.keys():
            protoName = "\t.global " + clasName + "_protoObj\n"
            sol = sol + protoName
        sol = sol + "_string_tag:\n\t.word	1\n_int_tag:\n\t.word	2\n_bool_tag :\n\t.word	3\n"
        return sol

    def genConstant(self, sol: str):
        for const in self.ConstantTable:
            (constName, constType, constLabel) = const
            if constType == "Bool":
                sol = sol + \
                    f"\t.word   -1\n" \
                    f"{constLabel}:\n" \
                    f"\t.word   5\n" \
                    f"\t.word   4\n" \
                    f"\t.word   Bool_dispTab\n" \
                    f"\t.word   {constLabel[-1:-1]}\n"
            elif constType == "Int":
                sol = sol + \
                    f"\t.word   -1\n{constLabel}:\n" \
                    f"\t.word   3\n\t.word   4\n" \
                    f"\t.word   Int_dispTab\n" \
                    f"\t.word   {constName}\n"
            else:
                length = int(len(constName) / 4) + 3
                if len(constName) % 4 != 0:
                    length = length + 1
                sol = sol + \
                      f"\t.word   -1\n{constLabel}:\n" \
                      f"\t.word   4\n\t.word   {length}\n" \
                      f"\t.word   String_dispTab\n" \
                      f"\t.word   int_const{len(constName)}\n" \
                      f"\t.ascii  {constName}\n" \
                      f"\t.byte   0\n" \
                      f"\t.align  2\n"
        return sol

    def findLabel(self, name: str):
        for const in self.ConstantTable:
            (constName, constType, constLabel) = const
            if constName == name and constType == "String":
                return constLabel

    def genMethodNames(self, coolClass: str, coolMethods: list, className: str):
        if coolClass == "None":
            return ""
        temp = ""
        for method in self.TypeTable[coolClass].Methods:
            if not (coolMethods.__contains__(method)):
                temp = temp + f"\t.word   {coolClass}.{method}\n"
                coolMethods.append(method)

        code = self.genMethodNames(self.TypeTable[coolClass].Parent, coolMethods, className)
        return code + temp



    def genAtributeNames(self, coolClass: str, coolAtributes: list):
        if coolClass == "None":
            return ""
        temp = ""
        listAtributes = list()
        for atribute in self.TypeTable[coolClass].Atributes:
            listAtributes.append(atribute)
            if not (coolAtributes.__contains__(atribute)):
                value = self.TypeTable[coolClass].Atributes[atribute]
                if value == "Int" or  value == "String" or value == "Bool":
                    temp = temp + f"\t.word   {value.lower()}_constant0\n"
                else:
                    temp = temp + f"\t.word   0\n"
                coolAtributes.append(atribute)

        code = self.genAtributeNames(self.TypeTable[coolClass].Parent, coolAtributes)
        if coolClass != "Object":
            self.TypeTable[coolClass].TagAtributes = self.TypeTable[self.TypeTable[coolClass].Parent].TagAtributes + listAtributes
        return code + temp

    def genClassTable(self):
        classNameTab = "class_nameTab:\n"
        class_objTab = "class_objTab:\n"
        methods = ""
        atributes = ""
        counter = 0
        for className in self.TypeTable:
            classNameTab = classNameTab + f"\t.word   {self.findLabel(className)}\n"
            temp = self.genMethodNames(className, list(), className)
            class_objTab = class_objTab + \
                           f"\t.word   {className}_protObj\n" \
                           f"\t.word   {className}_init\n"
            methods = methods + f"{className}_dispTab:\n" + temp
            if className == "Int" or className == "Bool":
                atributes = atributes + \
                            f"\t.word   -1\n" \
                            f"{className}_protObj:\n" \
                            f"\t.word   {counter}\n" \
                            f"\t.word   4\n" \
                            f"\t.word   {className}_dispTab\n" \
                            f"\t.word   0\n"
            elif className == "String":
                atributes = atributes + \
                            f"\t.word   -1\n" \
                            f"{className}_protObj:\n" \
                            f"\t.word   {counter}\n" \
                            f"\t.word   5\n" \
                            f"\t.word   {className}_dispTab\n" \
                            f"\t.word   int_constant0\n" \
                            f"\t.word   0\n"
            else:
                atributeList = list()
                temp = self.genAtributeNames(className, atributeList)
                atributes = atributes + \
                            f"\t.word   -1\n" \
                            f"{className}_protObj:\n" \
                            f"\t.word   {counter}\n" \
                            f"\t.word   {len(atributeList) + 3}\n" \
                            f"\t.word   {className}_dispTab\n" \
                            f"" + temp
            self.TypeTable[className].Tag = counter
            counter = counter + 1
        return classNameTab + class_objTab + methods + atributes

    def genClassAtributes(self, className: str):
        if className == "None":
            return ""
        code = self.genClassAtributes(self.TypeTable[className].Parent)
        for atribute in self.TypeTable[className].AtributeAsign:
            code = code + self.TypeTable[className].AtributeAsign[atribute].accept(self)
        return code

    # Visit a parse tree produced by COOL#program.
    def visitProgram(self, ctx: COOL.ProgramContext):
        for className in self.TypeTable:
            constantName = className
            self.ConstantTable.append((constantName, "String", f"str_const{self.Counter}"))
            self.Counter = self.Counter + 1
            length = len(constantName)
            contain = True
            for cons in self.ConstantTable:
                (consName, consType, _) = cons
                if consName == length and consType == "Int":
                    contain = False
            if contain:
                self.ConstantTable.append((length, "Int", f"int_const{length}"))
        self.ConstantTable.append(("SELF_TYPE", "String", f"str_const{self.Counter}"))
        contain = True
        length = len("SELF_TYPE")
        for cons in self.ConstantTable:
            (consName, consType, _) = cons
            if consName == length and consType == "Int":
                contain = False
        if contain:
            self.ConstantTable.append((length, "Int", f"int_const{length}"))
        code = self.genGlobalClases()
        code = self.genConstant(code)
        code = code + self.genClassTable()
        code = code + \
               "\t.global  heap_start\n" \
               "heap_start:\n" \
               "\t.word   0\n" \
               "\t.text\n" \
               "\t.global  Main_init\n" \
               "\t.global  Int_init\n" \
               "\t.global  String_init\n" \
               "\t.global  Bool_init\n" \
               "\t.global  Main.main\n"
        for className in self.TypeTable:
            code = code + f"{className}_init:\n"
            temp = self.genClassAtributes(className)
            if len(temp) != 0:
                code = code + \
                       "\taddiu  $sp $sp -12\n" \
                       "\tsw     $fp 12($sp)\n" \
                       "\tsw     $s0 8($sp)\n" \
                       "\tsw     $ra 4($sp)\n" \
                       "\taddiu  $fp $sp 4\n" \
                       "\tmove	 $s0 $a0\n"
                code = code + temp
                code = code + \
                       "\tmove   $a0 $s0\n" \
                       "\tlw     $fp 12($sp)\n" \
                       "\tlw     $s0 8($sp)\n" \
                       "\tlw     $ra 4($sp)\n" \
                       "\taddiu  $sp $sp 12\n"
            code = code + "\tjr  $ra\n"
        for className in self.TypeTable:
            if  not(className == "Object" or className == "String" or className == "Int" or className == "Bool" or className == "IO"):
                for methodName in self.TypeTable[className].Methods:
                    code = code + f"{className}.{methodName}:\n"
                    code = code + \
                           "\taddiu  $sp $sp -12\n" \
                           "\tsw     $fp 12($sp)\n" \
                           "\tsw     $s0 8($sp)\n" \
                           "\tsw     $ra 4($sp)\n" \
                           "\taddiu  $fp $sp 4\n" \
                           "\tmove	 $s0 $a0\n"
                    code = code + self.TypeTable[className].Methods[methodName].InstructionSet.accept(self)
                    code = code + \
                           "\tmove	 $a0 $s0\n" \
                           "\tlw     $fp 12($sp)\n" \
                           "\tlw     $s0 8($sp)\n" \
                           "\tlw     $ra 4($sp)\n" \
                           "\taddiu  $sp $sp 12\n"
                    code = code + "\tjr  $ra\n"
        print(code)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classes.
    def visitClasses(self, ctx: COOL.ClassesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classDefine.
    def visitClassDefine(self, ctx: COOL.ClassDefineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#method.
    def visitMethod(self, ctx: COOL.MethodContext):
        return ""

    # Visit a parse tree produced by COOL#property.
    def visitProperty(self, ctx: COOL.PropertyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#formal.
    def visitFormal(self, ctx: COOL.FormalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#letIn.
    def visitLetIn(self, ctx: COOL.LetInContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#minus.
    def visitMinus(self, ctx: COOL.MinusContext):
        code = ctx.getChild(0).accept(self)
        code = code + \
               "\tsw	$a0 0 ($sp)\n" + \
               "\taddiu	$sp $sp -4\n"
        code = code + ctx.getChild(2).accept(self)
        code = code + \
               "\tjal Object.copy" + \
               "\tlw    $t1 4($sp)\n" + \
               "\tlw    $t1 12($t1)\n" + \
               "\tlw    $t2 12($a0)\n" + \
               "\tsub   $t1 $t1 $t2\n" + \
               "\tsw    $t1 12($a0)\n" + \
               "\taddiu $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#string.
    def visitString(self, ctx: COOL.StringContext):
        name = ctx.getChild(0).symbol.text[1:-1]
        for const in self.ConstantTable:
            (constName, constType, constTag) = const
            if constType == "String" and constName == name:
                return f"\tla    $a0 {constTag}\n"

    # Visit a parse tree produced by COOL#isvoid.
    def visitIsvoid(self, ctx: COOL.IsvoidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#while.
    def visitWhile(self, ctx: COOL.WhileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#division.
    def visitDivision(self, ctx: COOL.DivisionContext):
        code = ctx.getChild(0).accept(self)
        code = code + \
               "\tsw	$a0 0 ($sp)\n" + \
               "\taddiu	$sp $sp -4\n"
        code = code + ctx.getChild(2).accept(self)
        code = code + \
               "\tjal Object.copy" \
               "\tlw    $t1 4($sp)\n" \
               "\tlw    $t1 12($t1)\n" \
               "\tlw    $t2 12($a0)\n" \
               "\tdiv   $t1 $t2\n" \
               "\tmflo  $t1" \
               "\tsw    $t1 12($a0)\n" \
               "\taddiu   $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#negative.
    def visitNegative(self, ctx: COOL.NegativeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#boolNot.
    def visitBoolNot(self, ctx: COOL.BoolNotContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#lessThan.
    def visitLessThan(self, ctx: COOL.LessThanContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#block.
    def visitBlock(self, ctx: COOL.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#id.
    def visitId(self, ctx: COOL.IdContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#multiply.
    def visitMultiply(self, ctx: COOL.MultiplyContext):
        code = ctx.getChild(0).accept(self)
        code = code + \
               "\tsw	$a0 0 ($sp)\n" + \
               "\taddiu	$sp $sp -4\n"
        code = code + ctx.getChild(2).accept(self)
        code = code + \
               "\tjal Object.copy" + \
               "\tlw    $t1 4($sp)\n" + \
               "\tlw    $t1 12($t1)\n" + \
               "\tlw    $t2 12($a0)\n" + \
               "\tmul   $t1 $t1 $t2\n" + \
               "\tsw    $t1 12($a0)\n" + \
               "\taddiu $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#if.
    def visitIf(self, ctx: COOL.IfContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#case.
    def visitCase(self, ctx: COOL.CaseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#ownMethodCall.
    def visitOwnMethodCall(self, ctx: COOL.OwnMethodCallContext):
        length = len(ctx.children)
        code = ""
        if length > 3:
            count = 2
            while length != count:
                param = ctx.getChild(count).accept(self)
                code = code + param + f"\tsw	$a0 0($sp)\n\taddiu	 $sp $sp -4\n"
                count = count + 2
            code = code + "\tmove	  $a0 $s0\n"
        return code

    # Visit a parse tree produced by COOL#add.
    def visitAdd(self, ctx: COOL.AddContext):
        code = ctx.getChild(0).accept(self)
        code = code + \
               "\tsw	$a0 0 ($sp)\n"+ \
               "\taddiu	$sp $sp -4\n"
        code = code + ctx.getChild(2).accept(self)
        code = code + \
                "\tjal Object.copy"+ \
                "\tlw    $t1 4($sp)\n"+ \
                "\tlw    $t1 12($t1)\n"+ \
                "\tlw    $t2 12($a0)\n"+ \
                "\tadd   $t1 $t1 $t2\n"+ \
                "\tsw    $t1 12($a0)\n"+ \
                "\taddiu $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#new.
    def visitNew(self, ctx: COOL.NewContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#parentheses.
    def visitParentheses(self, ctx: COOL.ParenthesesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#assignment.
    def visitAssignment(self, ctx: COOL.AssignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#false.
    def visitFalse(self, ctx: COOL.FalseContext):
        return f"\tla    $a0 {bool_const0}\n"

    # Visit a parse tree produced by COOL#int.
    def visitInt(self, ctx: COOL.IntContext):
        name = ctx.getChild(0).symbol.text[1:-1]
        for const in self.ConstantTable:
            (constName, constType, constTag) = const
            if constType == "Int" and constName == name:
                return f"\tla    $a0 {constTag}\n"

    # Visit a parse tree produced by COOL#equal.
    def visitEqual(self, ctx: COOL.EqualContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#true.
    def visitTrue(self, ctx: COOL.TrueContext):
        return f"\tla    $a0 {bool_const1}\n"

    # Visit a parse tree produced by COOL#lessEqual.
    def visitLessEqual(self, ctx: COOL.LessEqualContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#methodCall.
    def visitMethodCall(self, ctx: COOL.MethodCallContext):
        return self.visitChildren(ctx)
