from collections import deque
from antlr4 import *
from COOL import *
from  src import COOLParser

class COOLClass:
    def __init__(self, name: str, parent: str, created: bool, sealed: bool):
        self.Name = name
        self.Parent = parent
        self.Created = created
        self.Sealed = sealed
        self.Deep = -1
        self.Methods = {}
        self.VisitedMethods = list()
        self.VisitedAtributes = list()
        self.TagMethods = list()
        self.Atributes = {}
        self.Tag = 0
        self.TagAtributes = list()
        self.AtributeAsign = {}

class COOLMethod:
    def __init__(self, name: str, type: str, paramNumber: int, instructionSet):
        self.Name = name
        self.Type = type
        self.Params = list()
        self.ParamsNumber= paramNumber
        self.InstructionSet = instructionSet

class SemanticScopeManager:
    def __init__(self):
        self.Stack = deque()

    def addScope(self):
        self.Stack.append({})

    def addIdentifier(self, name: str, type: str):
        scope = self.Stack.pop()
        scope[name] = type
        self.Stack.append(scope)

    def deleteScope(self):
        self.Stack.pop()

    def searchScope(self, identifier: str):
        scope = self.Stack.pop()
        self.Stack.append(scope)
        return scope.keys().__contains__(identifier)

    def searchIdentifier(self, identifier: str):
        for scope in reversed(self.Stack):
            if(scope.keys().__contains__(identifier)):
                return True
        return False

    def searchforType(self, identifier: str):
        for scope in reversed(self.Stack):
            if(scope.keys().__contains__(identifier)):
                return scope[identifier]
        return "None"

class GenScopeManager:
    def __init__(self):
        self.Stack = deque()

    def addScope(self):
        self.Stack.append({})

    def addIdentifier(self, name: str, type: str):
        scope = self.Stack.pop()
        scope[name] = type
        self.Stack.append(scope)

    def deleteScope(self):
        self.Stack.pop()

    def searchScope(self, identifier: str):
        scope = self.Stack.pop()
        self.Stack.append(scope)
        return scope.keys().__contains__(identifier)

    def searchIdentifier(self, identifier: str):
        index = len(self.Stack) - 1
        for scope in reversed(self.Stack):
            if (len(scope) != 0):
                if(scope.keys().__contains__(identifier)):
                    return index
            index -= 1
        return index

    def searchType(self, identifier: str):
        for scope in reversed(self.Stack):
            if (len(scope) != 0):
                if(scope.keys().__contains__(identifier)):
                    return scope[identifier]
        return "None"

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

    def calculateDeep(self, coolClass: COOLClass, classList: list):
        if coolClass.Deep != -1:
            return
        elif self.TypeTable.keys().__contains__(coolClass.Parent):
            if self.TypeTable[coolClass.Parent].Deep != -1:
                coolClass.Deep = self.TypeTable[coolClass.Parent].Deep + 1
            elif classList.__contains__(coolClass.Parent):
                coolClass.Deep = 1
            else:
                classList.append(coolClass.Name)
                self.calculateDeep(self.TypeTable[coolClass.Parent], classList)
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
        self.ScopeManager = SemanticScopeManager()
        self.actualClass = "Object"
        self.hasNoError = True

    # Visit a parse tree produced by COOL#program.
    def visitProgram(self, ctx:COOL.ProgramContext):
        for className in self.TypeTable.keys():
            self.calculateDeep(self.TypeTable[className], list())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classes.
    def visitClasses(self, ctx:COOL.ClassesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by COOL#classDefine.
    def visitClassDefine(self, ctx:COOL.ClassDefineContext):
        coolClass = ctx.getChild(1).symbol
        if(self.TypeTable[coolClass.text].Created):
            line = str(coolClass.line)
            column = str(coolClass.column + 1)
            if coolClass.text == "Bool" or coolClass.text == "Int" or coolClass.text == "String" or coolClass.text == "IO" or coolClass.text == "Object":
                error = f"({line}, {column}) - SemanticError: Redefinition of basic class {coolClass.text}"
            else:
                error = f"({line}, {column}) - SemanticError: Classes may not be redefined"
            print(error)
            self.hasNoError = False
        elif ctx.getChild(2).symbol.text == "inherits":
            classParent = ctx.getChild(3).symbol
            if (self.TypeTable.keys().__contains__(classParent.text)):
                if self.TypeTable[classParent.text].Sealed:
                    line = str(classParent.line)
                    column = str(classParent.column + 1)
                    error = f"({line}, {column}) - SemanticError: Class {coolClass.text} cannot inherit class {classParent.text}"
                    print(error)
                    self.hasNoError = False
                elif not (self.TypeTable[coolClass.text].Deep > self.TypeTable[classParent.text].Deep):
                    line = str(classParent.line)
                    column = str(classParent.column + 1)
                    error = f"({line}, {column}) - SemanticError: Class {coolClass.text}, or an ancestor of {coolClass.text}, is involved in an inheritance cycle."
                    print(error)
                    self.hasNoError = False
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
                column = str(classParent.column + 1)
                error = f"({line}, {column}) - TypeError: Class {coolClass.text} inherits from an undefined class {classParent.text}."
                print(error)
                self.hasNoError = False
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
        methodType = ctx.getChild(len(ctx.children) - 4).symbol
        if self.TypeTable[coolClass].VisitedMethods.__contains__(methodName):
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column + 1)
            error = f"({line}, {column}) - SemanticError: Method {methodName} is multiply defined."
            print(error)
            self.hasNoError = False
            return
        if self.searchMethod(self.TypeTable[coolClass].Parent, methodName):
            ancestorMethod = self.searchMethodInfo(self.TypeTable[coolClass].Parent,methodName)
            if ancestorMethod.ParamsNumber != self.TypeTable[coolClass].Methods[methodName].ParamsNumber:
                line = str(ctx.getChild(0).symbol.line)
                column = str(ctx.getChild(0).symbol.column + 1)
                error = f"({line}, {column}) SemanticError: Incompatible number of formal parameters in redefined method {methodName}."
                print(error)
                self.hasNoError = False
                return
            if ancestorMethod.Type != methodType.text:
                line = str(methodType.line)
                column = str(methodType.column + 1)
                error = f"({line}, {column}) SemanticError: In redefined method {methodName}, return type {methodType.text} is different from original return type {ancestorMethod.Type}."
                print(error)
                self.hasNoError = False
                return
        if self.TypeTable.keys().__contains__(self.TypeTable[coolClass].Methods[methodName].Type) or methodType.text == "SELF_TYPE":
            self.ScopeManager.addIdentifier(methodName, methodType.text)
            self.TypeTable[coolClass].VisitedMethods.append(methodName)
            self.ScopeManager.addScope()
            i = 2
            while(i < len(ctx.children) - 4):
                ctx.getChild(i).accept(self)
                i += 2
            methodValue = ctx.getChild(len(ctx.children) - 2).accept(self)
            if self.join(methodType.text, methodValue) != methodType.text:
                line = str(ctx.getChild(len(ctx.children) - 2).start.line)
                column = str(ctx.getChild(len(ctx.children) - 2).start.column + 1)
                error =  f"({line}, {column}) - TypeError: Inferred return type {methodValue} of method {methodName} does not conform to declared return type {methodType.text}."
                print(error)
                self.hasNoError = False
            self.ScopeManager.deleteScope()
            return
        else:
            line = str(methodType.line)
            column = str(methodType.column + 1)
            error = f"({line}, {column}) - TypeError: Undefined return type {methodType.text} in method {methodName}."
            print(error)
            self.hasNoError = False

    # Visit a parse tree produced by COOL#property.
    def visitProperty(self, ctx:COOL.PropertyContext):
        atributeType = ctx.getChild(2).symbol.text
        coolClass = ctx.parentCtx.getChild(1).symbol.text
        atributeName = ctx.getChild(0).symbol.text
        if self.TypeTable[coolClass].VisitedAtributes.__contains__(atributeName):
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column + 1)
            error = f"({line}, {column}) - SemanticError: Attribute {atributeName} is multiply defined in class."
            print(error)
            self.hasNoError = False
            return "None"
        elif atributeName == "self":
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column + 1)
            error = f"({line}, {column}) - SemanticError: 'self' cannot be the name of an atribute."
            print(error)
            self.hasNoError = False
            return
        elif not(self.TypeTable.keys().__contains__(atributeType) or atributeType == "SELF_TYPE"):
            line = str(ctx.getChild(2).symbol.line)
            column = str(ctx.getChild(2).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: Class {atributeType} of attribute {atributeName} is undefined."
            print(error)
            self.hasNoError = False
            return "None"
        elif self.TypeTable[self.TypeTable[coolClass].Parent].Atributes.keys().__contains__(atributeName):
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column + 1)
            error = f"({line}, {column}) - SemanticError: Attribute {atributeName} is an attribute of an inherited class."
            print(error)
            self.hasNoError = False
            return "None"
        elif len(ctx.children) == 5:
            atributeValue = ctx.getChild(4).accept(self)
            if self.join(atributeType, atributeValue) != atributeType:
                line = str(ctx.getChild(4).start.line)
                column = str(ctx.getChild(4).start.column + 1)
                error =  f"({line}, {column}) - TypeError: Inferred type {atributeValue} of initialization of attribute {atributeName} does not conform to declared type {atributeType}."
                print(error)
                self.hasNoError = False
                return "None"
            else:
                self.ScopeManager.addIdentifier(atributeName, atributeType)
                self.TypeTable[coolClass].VisitedAtributes.append(atributeName)
                return atributeType
        else:
            self.ScopeManager.addIdentifier(atributeName, atributeType)
            self.TypeTable[coolClass].VisitedAtributes.append(atributeName)
            return atributeType

    # Visit a parse tree produced by COOL#formal.
    def visitFormal(self, ctx:COOL.FormalContext):
        paramName = ctx.getChild(0).symbol.text
        paramType = ctx.getChild(2).symbol.text
        method = ctx.parentCtx
        coolClass = method.parentCtx.getChild(1).symbol.text
        methodName = method.getChild(0).symbol.text
        if paramName == "self":
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column + 1)
            error = f"({line}, {column}) - SemanticError: 'self' cannot be the name of a formal parameter."
            print(error)
            self.hasNoError = False
            return
        if self.ScopeManager.searchScope(paramName):
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column + 1)
            error = f"({line}, {column}) - SemanticError: Formal parameter {paramName} is multiply defined."
            print(error)
            self.hasNoError = False
            return
        if self.searchMethod(self.TypeTable[coolClass].Parent, methodName):
            ancestorMethod = self.searchMethodInfo(self.TypeTable[coolClass].Parent,methodName)
            exist = False
            i = 0
            for param in self.TypeTable[coolClass].Methods[methodName].Params:
                (pName, pType) = param
                if pName == paramName:
                    exist = True
                    (_, acType) = ancestorMethod.Params.__getitem__(i)
                    if paramType != acType:
                        line = str(ctx.getChild(0).symbol.line)
                        column = str(ctx.getChild(0).symbol.column + 1)
                        error = f"({line}, {column}) - SemanticError: In redefined method {methodName}, parameter type {paramType} is different from original type {acType}."
                        print(error)
                        self.hasNoError = False
                        return
                    i += 1
            if not exist:
                line = str(ctx.getChild(0).symbol.line)
                column = str(ctx.getChild(0).symbol.column + 1)
                error = f"({line}, {column}) - SemanticError: In ancestor method {methodName}, dont exist param {paramName}."
                print(error)
                self.hasNoError = False
                return
        if self.TypeTable.keys().__contains__(paramType):
             self.ScopeManager.addIdentifier(paramName, paramType)
             return self.visitChildren(ctx)
        else:
            line = str(ctx.getChild(2).symbol.line)
            column = str(ctx.getChild(2).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: Class {paramType} of formal parameter {paramName} is undefined."
            print(error)
            self.hasNoError = False

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
        if leftValue != "Int" or rightValue != "Int":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: non-Int arguments: {leftValue} + {rightValue}"
            print(error)
            self.hasNoError = False
            addValue = "None"
        return addValue

    # Visit a parse tree produced by COOL#minus.
    def visitMinus(self, ctx:COOL.MinusContext):
        minusValue = "Int"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int" or rightValue != "Int":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: non-Int arguments: {leftValue} - {rightValue}"
            print(error)
            self.hasNoError = False
            minusValue = "None"
        return minusValue

     # Visit a parse tree produced by COOL#multiply.
    def visitMultiply(self, ctx: COOL.MultiplyContext):
        mulValue = "Int"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int" or rightValue != "Int":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: non-Int arguments: {leftValue} * {rightValue}"
            print(error)
            self.hasNoError = False
            mulValue = "None"
        return mulValue

    # Visit a parse tree produced by COOL#division.
    def visitDivision(self, ctx: COOL.DivisionContext):
        divValue = "Int"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int" or rightValue != "Int":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: non-Int arguments: {leftValue} / {rightValue}"
            print(error)
            self.hasNoError = False
            divValue = "None"
        return divValue

    # Visit a parse tree produced by COOL#negative.
    def visitNegative(self, ctx: COOL.NegativeContext):
        expressValue = ctx.getChild(1).accept(self)
        if expressValue == "Int":
            return "Int"
        else:
            line = str(ctx.getChild(1).start.line)
            column = str(ctx.getChild(1).start.column + 1)
            error = f"({line}, {column}) - TypeError: Argument of '~' has type {expressValue} instead of Int."
            print(error)
            self.hasNoError = False
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
        else:
            line = str(ctx.getChild(1).start.line)
            column = str(ctx.getChild(1).start.column + 1)
            error = f"({line}, {column}) - TypeError: Argument of 'not' has type {expressValue} instead of Bool."
            print(error)
            self.hasNoError = False
            return "None"

    # Visit a parse tree produced by COOL#lessThan.
    def visitLessThan(self, ctx:COOL.LessThanContext):
        lessValue = "Bool"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int" or rightValue != "Int":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: non-Int arguments: {leftValue} < {rightValue}"
            print(error)
            self.hasNoError = False
            lessValue = "None"
        return lessValue

    # Visit a parse tree produced by COOL#lessEqual.
    def visitLessEqual(self, ctx:COOL.LessEqualContext):
        lessEqualValue = "Bool"
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue != "Int" or rightValue != "Int":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: non-Int arguments: {leftValue} <= {rightValue}"
            print(error)
            self.hasNoError = False
            lessEqualValue = "None"
        return lessEqualValue

    # Visit a parse tree produced by COOL#equal.
    def visitEqual(self, ctx: COOL.EqualContext):
        leftValue = ctx.getChild(0).accept(self)
        rightValue = ctx.getChild(2).accept(self)
        if leftValue == "None" or rightValue == "None":
            return "None"
        elif leftValue == rightValue:
            return "Bool"
        elif leftValue == "String" or leftValue == "Int" or leftValue == "Bool":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: Illegal comparison with a basic type."
            print(error)
            self.hasNoError = False
            return "None"
        elif rightValue == "String" or rightValue == "Int" or rightValue == "Bool":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: Illegal comparison with a basic type."
            print(error)
            self.hasNoError = False
            return "None"
        else:
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
                column = str(ctx.getChild(0).symbol.column + 1)
                error = f"({line}, {column}) - NameError: Undeclared identifier {variableName}."
                print(error)
                self.hasNoError = False
                return "None"
        if variableType == "SELF_TYPE":
            variableType = self.actualClass
        if  self.join(asignValue, variableType) != variableType:
            line = str(ctx.getChild(2).start.line)
            column = str(ctx.getChild(2).start.column + 1)
            error = f"({line}, {column}) - TypeError: Cannot assign {asignValue} expression to {variableType} identifier."
            print(error)
            self.hasNoError = False
            return "None"
        if variableName == "self":
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - SemanticError: Cannot assign to 'self'."
            print(error)
            self.hasNoError = False
            return "None"
        return asignValue

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
        column = str(ctx.getChild(0).symbol.column + 1)
        error = f"({line}, {column}) - NameError: Undeclared identifier {IdValue}."
        print(error)
        self.hasNoError = False
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
            column = str(ctx.getChild(1).start.column + 1)
            error = f"({line}, {column}) - TypeError: Predicate of 'if' does not have type Bool."
            print(error)
            self.hasNoError = False
            return self.join(thenValue, elseValue)

    # Visit a parse tree produced by COOL#while.
    def visitWhile(self, ctx: COOL.WhileContext):
        ctx.getChild(3).accept(self) #chequea semanticamente el cuerpo
        whileValue = ctx.getChild(1).accept(self)
        if whileValue == "None" or whileValue == "Bool":
            return "Object"
        else:
            line = str(ctx.getChild(1).start.line)
            column = str(ctx.getChild(1).start.column + 1)
            error = f"({line}, {column}) - TypeError: Loop condition does not have type Bool."
            print(error)
            self.hasNoError = False
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
        typeList = []
        while lengt > count:
            idName = ctx.getChild(count).symbol.text
            count = count + 2
            idType = ctx.getChild(count).symbol.text
            if not (self.TypeTable.keys().__contains__(idType)):
                line = str(ctx.getChild(count).symbol.line)
                column = str(ctx.getChild(count).symbol.column + 1)
                error = f"({line}, {column}) - TypeError: Class {idType} of case branch is undefined."
                print(error)
                self.hasNoError = False
            if typeList.__contains__(idType):
                line = str(ctx.getChild(count).symbol.line)
                column = str(ctx.getChild(count).symbol.column + 1)
                error = f"({line}, {column}) - SemanticError: Duplicate branch {idType} in case statement."
                print(error)
                self.hasNoError = False
            count = count + 2
            typeList.append(idType)
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
        typeName = ctx.getChild(1).symbol.text
        if not self.TypeTable.keys().__contains__(typeName):
            line = str(ctx.getChild(1).symbol.line)
            column = str(ctx.getChild(1).symbol.column + 1)
            error = f"({line}, {column}) - TypeError: 'new' used with undefined class {typeName}."
            print(error)
            self.hasNoError = False
        return typeName

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
                column = str(ctx.getChild(1).symbol.column + 1)
                error = f"({line}, {column}) - SemanticError: Method {ctx.getChild(1).symbol.text} called with wrong number of arguments."
                print(error)
                self.hasNoError = False
                methodType = "None"
            elif len(ctx.children) != methodInfo.ParamsNumber * 2 + 2 and methodInfo.ParamsNumber != 0:
                line = str(ctx.getChild(1).symbol.line)
                column = str(ctx.getChild(1).symbol.column + 1)
                error = f"({line}, {column}) - SemanticError: Method {ctx.getChild(1).symbol.text} called with wrong number of arguments."
                print(error)
                self.hasNoError = False
                methodType = "None"
            else:
                count = 2
                for param in methodInfo.Params:
                    (paramName,paramType) = param
                    requestType = ctx.getChild(count).accept(self)
                    if (self.join(requestType, paramType) != paramType):
                        line = str(ctx.getChild(count).start.line)
                        column = str(ctx.getChild(count).start.column + 1)
                        error = f"({line}, {column}) - TypeError: In call of method {ctx.getChild(1).symbol.text}, type {requestType} of parameter {paramName} does not conform to declared type {paramType}."
                        print(error)
                        self.hasNoError = False
                        methodType = "None"
                    count = count + 2
        else:
            line = str(ctx.getChild(0).symbol.line)
            column = str(ctx.getChild(0).symbol.column + 1)
            error = f"({line}, {column}) AttributeError: Dispatch to undefined method {ctx.getChild(0).symbol.text}."
            print(error)
            self.hasNoError = False
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
                line = str(ctx.getChild(1).symbol.line)
                column = str(ctx.getChild(1).symbol.column)
                error = f"({line}, {column}) - SemanticError: Expression type {currentClass} does not conform to declared static dispatch type {parent}."
                print(error)
                self.hasNoError = False
                return methodType
        if self.searchMethod(currentClass, ctx.getChild(length - 3).symbol.text):
            methodInfo = self.searchMethodInfo(currentClass, ctx.getChild(length - 3).symbol.text)
            if (methodInfo.Type == "SELF_TYPE"):
                methodType = currentClass
            else:
                methodType = methodInfo.Type
            if (methodInfo.ParamsNumber == 0 and len(ctx.children) != length):
                line = str(ctx.getChild(2).symbol.line)
                column = str(ctx.getChild(2).symbol.column + 1)
                error = f"({line}, {column}) - SemanticError: Method {ctx.getChild(2).symbol.text} called with wrong number of arguments."
                print(error)
                self.hasNoError = False
                methodType = "None"
            elif (len(ctx.children) != methodInfo.ParamsNumber * 2 + length - 1) and methodInfo.ParamsNumber > 0:
                line = str(ctx.getChild(2).symbol.line)
                column = str(ctx.getChild(2).symbol.column + 1)
                error = f"({line}, {column}) - SemanticError: Method {ctx.getChild(2).symbol.text} called with wrong number of arguments."
                print(error)
                self.hasNoError = False
                methodType = "None"
            else:
                count = length - 1
                for param in methodInfo.Params:
                    (paramName, paramType) = param
                    requestType = ctx.getChild(count).accept(self)
                    if (self.join(requestType, paramType) != paramType):
                        line = str(ctx.getChild(count).start.line)
                        column = str(ctx.getChild(count).start.column + 1)
                        error = f"({line}, {column}) - TypeError: In call of method {ctx.getChild(2).symbol.text}, type {requestType} of parameter {paramName} does not conform to declared type {paramType}."
                        print(error)
                        self.hasNoError = False
                        methodType = "None"
                    count = count + 2
        else:
            line = str(ctx.getChild(length - 3).symbol.line)
            column = str(ctx.getChild(length - 3).symbol.column + 1)
            error = f"({line}, {column}) AttributeError: Dispatch to undefined method {ctx.getChild(length - 3).symbol.text}."
            print(error)
            self.hasNoError = False
        return methodType

    # Visit a parse tree produced by COOL#letIn.
    def visitLetIn(self, ctx: COOL.LetInContext):
        self.ScopeManager.addScope()
        count = 0
        while(ctx.getChild(count).symbol.text != "in"):
            idName = ctx.getChild(count + 1).symbol.text
            if idName == "self":
                self.ScopeManager.deleteScope()
                line = str(ctx.getChild(count + 1).symbol.line)
                column = str(ctx.getChild(count + 1).symbol.column + 1)
                error = f"({line}, {column}) - SemanticError: 'self' cannot be bound in a 'let' expression."
                print(error)
                self.hasNoError = False
                return "None"
            count = count + 2
            idType = ctx.getChild(count + 1).symbol.text
            if not(self.TypeTable.keys().__contains__(idType)) and idType != "SELF_TYPE":
                self.ScopeManager.deleteScope()
                line = str(ctx.getChild(count + 1).symbol.line)
                column = str(ctx.getChild(count + 1).symbol.column + 1)
                error = f"({line}, {column}) - TypeError: Class {idType} of let-bound identifier {idName} is undefined."
                print(error)
                self.hasNoError = False
                return "None"
            self.ScopeManager.addIdentifier(idName, idType)
            count = count + 2
            if ctx.getChild(count).symbol.text == "<-":
                idValue = ctx.getChild(count + 1).accept(self)
                count = count + 2
                if self.join(idType, idValue) != idType:
                    self.ScopeManager.deleteScope()
                    line = str(ctx.getChild(count -1).start.line)
                    column = str(ctx.getChild(count - 1).start.column + 1)
                    error = f"({line}, {column}) - TypeError: Inferred type of {idValue} initialization of {idName} does not conform to identifier's declared type {idType}."
                    print(error)
                    self.hasNoError = False
                    return "None"

        temp = ctx.getChild(count + 1).accept(self)
        self.ScopeManager.deleteScope()
        return temp

class TypeCOOLVisitor(ParseTreeVisitor):

    TypeTable = {}

    Counter = 0

    ConstantTable = list()

    # Visit a parse tree produced by COOL#program.
    def visitProgram(self, ctx: COOL.ProgramContext, fileName: str):
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
        self.ConstantTable.append(("", "String", "str_const0"))
        self.ConstantTable.append((0, "Int", "int_const0"))
        self.ConstantTable.append(("false", "Bool", "bool_const0"))
        self.ConstantTable.append(("true", "Bool", "bool_const1"))
        self.ConstantTable.append((fileName, "String", "str_const1"))
        self.ConstantTable.append((len(fileName), "Int", F"int_const{len(fileName)}"))
        self.Counter = 2
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
        if len(ctx.children) == 5:
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

    CurrentClass : COOLClass

    CurrentMethod: COOLMethod

    CurrentType: str

    def join(self, class1: str, class2: str):
        if class1 == "None" or class2 == "None":
            return "None"
        if class1 == "SELF_TYPE":
            class1 = self.CurrentClass.Name
        if class2 == "SELF_TYPE":
            class2 = self.CurrentClass.Name
        if self.TypeTable[class1].Deep == self.TypeTable[class2].Deep:
            if self.TypeTable[class1].Name == self.TypeTable[class2].Name:
                return class1
            else:
                return self.join(self.TypeTable[class1].Parent, self.TypeTable[class2].Parent)
        elif self.TypeTable[class1].Deep > self.TypeTable[class2].Deep:
            return self.join(self.TypeTable[class1].Parent, class2)
        else:
            return self.join(class1, self.TypeTable[class2].Parent)

    def searchAtributeInfo(self, coolClass: str, atributeName: str):
        for atribute in self.TypeTable[coolClass].Atributes.keys():
            if atribute == atributeName:
                return self.TypeTable[coolClass].Atributes[atribute]
        return self.searchAtributeInfo(self.TypeTable[coolClass].Parent, atributeName)

    def searchMethodInfo(self, coolClass: str, methodName: str):
        for method in self.TypeTable[coolClass].Methods.keys():
            if method == methodName:
                return self.TypeTable[coolClass].Methods[method].Type
        return self.searchMethodInfo(self.TypeTable[coolClass].Parent, methodName)

    def __init__(self, typeTable: dict, constantTable: list, counter: int):
        self.TypeTable = typeTable
        self.ConstantTable = constantTable
        self.Counter = counter
        self.LabelCounter = 0
        self.ScopeManager = GenScopeManager()

    def genGlobalClases(self):
        sol = "\t.data\n\t.align 2\n\t.globl class_nameTab\n"
        for clasName in self.TypeTable.keys():
            protoName = "\t.globl " + clasName + "_protObj\n"
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
                    f"\t.word   3\n" \
                    f"\t.word   4\n" \
                    f"\t.word   Bool_dispTab\n" \
                    f"\t.word   {constLabel[-1]}\n"
            elif constType == "Int":
                sol = sol + \
                    f"\t.word   -1\n{constLabel}:\n" \
                    f"\t.word   2\n\t.word   4\n" \
                    f"\t.word   Int_dispTab\n" \
                    f"\t.word   {constName}\n"
            else:
                length = int(len(constName) / 4) + 3
                if len(constName) % 4 != 0:
                    length = length + 1
                sol = sol + \
                      f"\t.word   -1\n{constLabel}:\n" \
                      f"\t.word   1\n\t.word   {length}\n" \
                      f"\t.word   String_dispTab\n" \
                      f"\t.word   int_const{len(constName)}\n" \
                      f"\t.ascii  \"{constName}\"\n" \
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

    def genMethodTags(self, coolClass: str, coolMethods: list, className: str):
        if coolClass == "None":
            return coolMethods
        coolMethods = self.genMethodTags(self.TypeTable[coolClass].Parent, coolMethods, className)
        for method in self.TypeTable[coolClass].Methods:
            if not (coolMethods.__contains__(method)):
                coolMethods.append(method)
        return coolMethods

    def genAtributeNames(self, coolClass: str, coolAtributes: list):
        if coolClass == "None":
            return ""
        temp = ""
        listAtributes = list()
        for atribute in self.TypeTable[coolClass].Atributes:
            if not (coolAtributes.__contains__(atribute)):
                listAtributes.append(atribute)
                value = self.TypeTable[coolClass].Atributes[atribute]
                if value == "Int" or  value == "String" or value == "Bool":
                    temp = temp + f"\t.word   {value.lower()}_const0\n"
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
                            f"\t.word   int_const0\n" \
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
            code = code + (self.TypeTable[className].AtributeAsign[atribute].accept(self) or "")
            pos = self.CurrentClass.TagAtributes.index(atribute)
            code = code + f"\tsw     $a0 {pos * 4 + 12}($s0)\n"
        return code

    # Visit a parse tree produced by COOL#program.
    def visitProgram(self, ctx: COOL.ProgramContext, outFilename: str):
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
            self.TypeTable[className].TagMethods = self.genMethodTags(className,list(),className)
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
               "\t.globl  heap_start\n" \
               "heap_start:\n" \
               "\t.word   0\n" \
               "\t.text\n" \
               "\t.globl  Main_init\n" \
               "\t.globl  Int_init\n" \
               "\t.globl  String_init\n" \
               "\t.globl  Bool_init\n" \
               "\t.globl  Main.main\n"
        for className in self.TypeTable:
            self.CurrentClass = self.TypeTable[className]
            self.CurrentType = className
            self.CurrentMethod = "None"
            code = code + f"{className}_init:\n"
            temp = self.genClassAtributes(className)
            if len(temp) != 0:
                code = code + \
                       "\taddiu  $sp $sp -12\n" \
                       "\tsw     $fp 12($sp)\n" \
                       "\tsw     $s0 8($sp)\n" \
                       "\tsw     $ra 4($sp)\n" \
                       "\taddiu  $fp $sp 4\n" \
                       "\tmove   $s0 $a0\n"
                code = code + temp
                code = code + \
                       "\tmove   $a0 $s0\n" \
                       "\tlw     $fp 12($sp)\n" \
                       "\tlw     $s0 8($sp)\n" \
                       "\tlw     $ra 4($sp)\n" \
                       "\taddiu  $sp $sp 12\n"
            code = code + "\tjr     $ra\n"
        for className in self.TypeTable:
            if not(className == "Object" or className == "String" or className == "Int" or className == "Bool" or className == "IO"):
                self.CurrentClass = self.TypeTable[className]
                self.ScopeManager.addScope()
                for atribute in self.CurrentClass.TagAtributes:
                    self.ScopeManager.addIdentifier(atribute,self.searchAtributeInfo(className, atribute))
                for methodName in self.CurrentClass.Methods:
                    self.CurrentMethod = self.CurrentClass.Methods[methodName]
                    self.CurrentType = self.CurrentMethod.Type
                    self.ScopeManager.addScope()
                    for param in self.CurrentClass.Methods[methodName].Params:
                        (paramName, paramType) = param
                        self.ScopeManager.addIdentifier(paramName, paramType)
                    code = code + f"{className}.{methodName}:\n"
                    code = code + \
                           "\taddiu  $sp $sp -12\n" \
                           "\tsw     $fp 12($sp)\n" \
                           "\tsw     $s0 8($sp)\n" \
                           "\tsw     $ra 4($sp)\n" \
                           "\taddiu  $fp $sp 4\n" \
                           "\tmove   $s0 $a0\n"
                    code = code + (self.TypeTable[className].Methods[methodName].InstructionSet.accept(self) or "")
                    # "\tmove   $a0 $s0\n" \
                    code = code + \
                           "\tlw     $fp 12($sp)\n" \
                           "\tlw     $s0 8($sp)\n" \
                           "\tlw     $ra 4($sp)\n" \
                           f"\taddiu  $sp $sp {12+4*self.CurrentClass.Methods[methodName].ParamsNumber}\n"
                    code = code + "\tjr     $ra\n"
                    self.ScopeManager.deleteScope()

                self.ScopeManager.deleteScope()

        code =  self.RuntimeMessages + \
                "\n" + \
                self.MemManagerNoGCInit + \
                "\n" + \
                code + \
                "\n" + \
                self.RuntimeCode + \
                "\n" + \
                self.MemManagerNoGC

        outFile = open(outFilename, "w");
        outFile.write(code)
        #print(code)

        return

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
        self.ScopeManager.addScope()
        count = 0
        varNumber = 0
        code = ""
        while (ctx.getChild(count).symbol.text != "in"):
            idName = ctx.getChild(count + 1).symbol.text
            varNumber += 1
            count = count + 2
            idType = ctx.getChild(count + 1).symbol.text
            count = count + 2
            if ctx.getChild(count).symbol.text == "<-":
                code += ctx.getChild(count + 1).accept(self)
                count = count + 2
            else:
                if idType == "String" or idType == "Int" or idType == "Bool":
                    code += f"\tla     $a0 {idType.lower()}_const0\n"
                else:
                    code += "li      $a0 0\n"
            code += f"\tsw     $a0 0($sp)\n" \
                    f"\taddiu  $sp $sp -4\n"
            self.ScopeManager.addIdentifier(idName, idType)
        code += ctx.getChild(count + 1).accept(self)
        code += f"\taddiu  $sp $sp {varNumber * 4}\n"
        self.ScopeManager.deleteScope()
        return code

    # Visit a parse tree produced by COOL#minus.
    def visitMinus(self, ctx: COOL.MinusContext):
        code = ctx.getChild(0).accept(self)
        code = code + \
                "\tsw     $a0 0 ($sp)\n" + \
                "\taddiu $sp $sp -4\n"
        code = code + ctx.getChild(2).accept(self)
        code = code + \
                "\tjal    Object.copy\n" + \
                "\tlw     $t1 4($sp)\n" + \
                "\tlw     $t1 12($t1)\n" + \
                "\tlw     $t2 12($a0)\n" + \
                "\tsub    $t1 $t1 $t2\n" + \
                "\tsw     $t1 12($a0)\n" + \
                "\taddiu  $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#string.
    def visitString(self, ctx: COOL.StringContext):
        name = ctx.getChild(0).symbol.text[1:-1]
        self.CurrentType = "String"
        for const in self.ConstantTable:
            (constName, constType, constTag) = const
            if constType == "String" and constName == name:
                return f"\tla     $a0 {constTag}\n"

    # Visit a parse tree produced by COOL#isvoid.
    def visitIsvoid(self, ctx: COOL.IsvoidContext):
        code = ctx.getChild(1).accept(self)
        code += \
            "\tla   $t1 bool_const0\n" \
            "\tla   $t2 bool_const1\n" \
            "\tmovz $t1 $t2 $a0\n" \
            "\tmove $a0 $t1\n"
        self.CurrentType = "Bool"
        return code

    # Visit a parse tree produced by COOL#while.
    def visitWhile(self, ctx: COOL.WhileContext):
        code = f"while_label{self.Counter}:\n"
        code += ctx.getChild(1).accept(self)
        code += "\tlw     $t1 12($a0)\n" + \
               f"\tbgtz   $t1 loop_label{self.Counter}\n" + \
               f"\tb      pool_label{self.Counter}\n" + \
               f"loop_label{self.Counter}:\n"
        code += ctx.getChild(3).accept(self)
        code += f"\tb      while_label{self.Counter}\n" + \
                f"pool_label{self.Counter}:\n"
        self.CurrentType = "None"
        self.Counter += 1
        return code

    # Visit a parse tree produced by COOL#division.
    def visitDivision(self, ctx: COOL.DivisionContext):
        code = ctx.getChild(0).accept(self)
        code += \
                "\tsw     $a0 0($sp)\n" + \
                "\taddiu  $sp $sp -4\n"
        code += ctx.getChild(2).accept(self)
        code += \
                "\tjal    Object.copy\n" \
                "\tlw     $t1 4($sp)\n" \
                "\tlw     $t1 12($t1)\n" \
                "\tlw     $t2 12($a0)\n" \
                "\tdiv    $t1 $t2\n" \
                "\tmflo   $t1\n" \
                "\tsw     $t1 12($a0)\n" \
                "\taddiu  $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#negative.
    def visitNegative(self, ctx: COOL.NegativeContext):
        self.CurrentType = "Int"
        code = ctx.getChild(1).accept(self)
        code += \
            "\tjal    Object.copy\n" \
            "\tlw     $t1 12($a0)\n" \
            "\tnegu   $t1 $t1\n" \
            "\tsw     $t1 12($a0)\n" \
            "\tsw     $a0 0($sp)\n"
        return code

    # Visit a parse tree produced by COOL#boolNot.
    def visitBoolNot(self, ctx: COOL.BoolNotContext):
        self.CurrentType = "Bool"
        code = ctx.getChild(1).accept(self)
        code += \
            "\tjal    Object.copy\n" \
            "\tlw     $t1 12($a0)\n" \
            "\tnegu   $t2 $t1\n" \
            "\taddiu  $t3 $t2 1\n"\
            "\tsw     $t3 12($a0)\n" \
            "\tsw     $a0 0($sp)\n"
        return code

    # Visit a parse tree produced by COOL#lessThan.
    def visitLessThan(self, ctx: COOL.LessThanContext):
        self.CurrentType = "Bool"
        code = ctx.getChild(0).accept(self)
        code += \
            "\tsw     $a0 0($sp)\n" + \
            "\taddiu  $sp $sp -4\n"
        code += ctx.getChild(2).accept(self)
        code += \
            "\tjal    Object.copy\n" \
            "\tlw     $t0 4($sp)\n" \
            "\tlw     $t1 12($t0)\n" \
            "\tlw     $t2 12($a0)\n" \
            "\tslt    $t3 $t1 $t2\n" \
            "\tla     $a0 bool_const0\n" \
            "\tjal    Object.copy\n" \
            "\tsw     $t3 12($a0)\n" \
            "\taddiu  $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#block.
    def visitBlock(self, ctx: COOL.BlockContext):
        counter = 1
        length = len(ctx.children) - 1
        code = ""
        while(counter < length ):
            code += (ctx.getChild(counter).accept(self))
            counter += 2
        return code

    # Visit a parse tree produced by COOL#id.
    def visitId(self, ctx: COOL.IdContext):
        varName = ctx.getChild(0).symbol.text
        if varName == "self":
            self.CurrentType = self.CurrentClass.Name
            return "\tlw     $a0 ($s0)\n"
        self.CurrentType = self.ScopeManager.searchType(varName)
        option = self.ScopeManager.searchIdentifier(varName)
        if option == 0 and self.CurrentMethod != "None":
            return self.propertyId(ctx)
        elif option == 1 and self.CurrentMethod != "None":
            return self.formalId(ctx)
        else:
            return self.variableId(ctx)

    def propertyId(self, ctx: COOL.AssignmentContext):
        varName = ctx.getChild(0).symbol.text
        pos = self.CurrentClass.TagAtributes.index(varName)
        code = f"\tlw     $a0 {pos * 4 + 12}($s0)\n"
        return code

    def formalId(self, ctx: COOL.AssignmentContext):
        varName = ctx.getChild(0).symbol.text
        varType = self.ScopeManager.Stack[1][varName]
        pos = self.CurrentMethod.Params.index((varName,varType))
        total = self.CurrentMethod.ParamsNumber
        code = f"\tlw     $a0 {((total + 2) - pos) * 4}($fp)\n"
        return code

    def variableId(self, ctx: COOL.AssignmentContext):
        varName = ctx.getChild(0).symbol.text
        scope = self.ScopeManager.searchIdentifier(varName)
        pos = list(self.ScopeManager.Stack[scope].keys()).index(varName) + 1
        init = 2
        if self.CurrentMethod == "None":
            init = 0
        for scope in list(self.ScopeManager.Stack)[init : scope]:
            pos += len(list(scope.keys()))
        code = f"\tlw     $a0 {-(pos * 4)}($fp)\n"
        return code

    # Visit a parse tree produced by COOL#multiply.
    def visitMultiply(self, ctx: COOL.MultiplyContext):
        code = ctx.getChild(0).accept(self)
        code = code + \
                "\tsw     $a0 0 ($sp)\n" + \
                "\taddiu  $sp $sp -4\n"
        code = code + ctx.getChild(2).accept(self)
        code = code + \
                "\tjal    Object.copy\n" + \
                "\tlw     $t1 4($sp)\n" + \
                "\tlw     $t1 12($t1)\n" + \
                "\tlw     $t2 12($a0)\n" + \
                "\tmul    $t1 $t1 $t2\n" + \
                "\tsw     $t1 12($a0)\n" + \
                "\taddiu  $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#if.
    def visitIf(self, ctx: COOL.IfContext):
        code = ctx.getChild(1).accept(self)
        counter = self.Counter
        self.Counter += 1
        code = code + \
               "\tlw     $t1 12($a0)\n" + \
               f"\tbgtz   $t1 then_label{counter}\n" + \
               f"\tb      else_label{counter}\n" + \
               f"then_label{counter}:\n"
        code = code +\
               ctx.getChild(3).accept(self) + \
               f"\tb      fi_label{counter}\n" + \
               f"else_label{counter}:\n"
        tempType = self.CurrentType
        code = code +\
               ctx.getChild(5).accept(self) + \
               f"\tb      fi_label{counter}\n" + \
               f"fi_label{counter}:\n"
        self.CurrentType = self.join(tempType, self.CurrentType)
        return code

    # Visit a parse tree produced by COOL#case.
    def visitCase(self, ctx: COOL.CaseContext):
        counter = self.Counter
        self.Counter += 1
        code = ctx.getChild(1).accept(self) +\
                "\tli    $t1 0\n" \
                f"\tbeq    $a0 $t1 abort{counter}\n"
        lengt = len(ctx.children) - 1
        tempCode = f"abort{counter}:\n" \
                "\tjal    _case_abort2\n"
        count = 3
        while lengt > count:
            idName = ctx.getChild(count).symbol.text
            count = count + 2
            idType = ctx.getChild(count).symbol.text
            count = count + 2
            self.ScopeManager.addScope()
            self.ScopeManager.addIdentifier(idName, idType)
            code += \
                f"\tlw     $t1 0($a0)\n" \
                f"\tli     $t2 {self.TypeTable[idType].Tag}\n" \
                f"\tbeq    $t1 $t2 {idType}_case{counter}\n"
            scope = self.ScopeManager.searchIdentifier(idName)
            pos = list(self.ScopeManager.Stack[scope].keys()).index(idName) + 1
            init = 2
            if self.CurrentMethod == "None":
                init = 0
            for scope in list(self.ScopeManager.Stack)[init: scope]:
                pos += len(list(scope.keys()))
            tempCode +=\
                f"{idType}_case{counter}:\n" \
                f"\tsw     $a0 -{pos * 4}($fp)\n"
            tempCode += ctx.getChild(count).accept(self)
            tempCode += f"\tb      esac{counter}\n"
            self.ScopeManager.deleteScope()
            count = count + 2
        code = code + \
               "\tjal    _case_abort\n"
        code += tempCode +\
               f"esac{counter}:\n"
        return code

    # Visit a parse tree produced by COOL#ownMethodCall.
    def visitOwnMethodCall(self, ctx: COOL.OwnMethodCallContext):
        length = len(ctx.children)
        code = ""
        if length > 3:
            count = 2
            while length != count:
                param = (ctx.getChild(count).accept(self) or "")
                code += param + \
                       f"\tsw     $a0 0($sp)\n" \
                       f"\taddiu  $sp $sp -4\n"
                count = count + 2
        methodIdx = self.CurrentClass.TagMethods.index(ctx.getChild(0).symbol.text)
        self.CurrentType = self.searchMethodInfo(self.CurrentClass.Name, ctx.getChild(0).symbol.text)
        code += "\tmove   $a0 $s0\n" \
                "\tlw     $t1 8($a0)\n" \
                f"\tlw     $t1 {methodIdx * 4}($t1)\n" \
                "\tjalr   $t1\n"
        return code

    # Visit a parse tree produced by COOL#add.
    def visitAdd(self, ctx: COOL.AddContext):
        code = ctx.getChild(0).accept(self) or ""
        code = code + \
                "\tsw     $a0 0 ($sp)\n"+ \
                "\taddiu  $sp $sp -4\n"
        code = code + ctx.getChild(2).accept(self)
        code = code + \
                "\tjal    Object.copy\n"+ \
                "\tlw     $t1 4($sp)\n"+ \
                "\tlw     $t1 12($t1)\n"+ \
                "\tlw     $t2 12($a0)\n"+ \
                "\tadd    $t1 $t1 $t2\n"+ \
                "\tsw     $t1 12($a0)\n"+ \
                "\taddiu  $sp $sp 4\n"
        return code

    # Visit a parse tree produced by COOL#new.
    def visitNew(self, ctx: COOL.NewContext):
        self.CurrentType = ctx.getChild(1).symbol.text
        return f"\tla     $a0 {self.CurrentType}_protObj\n"\
                "\tjal    Object.copy\n" \
               f"\tjal    {self.CurrentType}_init\n"

    # Visit a parse tree produced by COOL#parentheses.
    def visitParentheses(self, ctx: COOL.ParenthesesContext):
        return ctx.getChild(1).accept(self)

    # Visit a parse tree produced by COOL#assignment.
    def visitAssignment(self, ctx: COOL.AssignmentContext):
        varName = ctx.getChild(0).symbol.text
        option = self.ScopeManager.searchIdentifier(varName)
        if option == 0 and self.CurrentMethod != "None":
            return self.propertyAssignament(ctx)
        elif option == 1 and self.CurrentMethod != "None":
            return self.formalAssignament(ctx)
        else:
            return self.variableAssignament(ctx)

    def propertyAssignament(self, ctx: COOL.AssignmentContext):
        varName = ctx.getChild(0).symbol.text
        code = ctx.getChild(2).accept(self)
        pos = self.CurrentClass.TagAtributes.index(varName)
        code = code + f"\tsw     $a0 {pos * 4 + 12}($s0)\n"
        return code

    def formalAssignament(self, ctx: COOL.AssignmentContext):
        varName = ctx.getChild(0).symbol.text
        code = ctx.getChild(2).accept(self)
        varType = self.ScopeManager.Stack[1][varName]
        pos = self.CurrentMethod.Params.index((varName, varType))
        total = self.CurrentMethod.ParamsNumber
        code = code + f"\tsw     $a0 {(pos - (total + 2)) * 4}($fp)\n"
        return code

    def variableAssignament(self, ctx: COOL.AssignmentContext):
        varName = ctx.getChild(0).symbol.text
        scope = self.ScopeManager.searchIdentifier(varName)
        pos = list(self.ScopeManager.Stack[scope].keys()).index(varName) + 1
        init = 2
        if self.CurrentMethod == "None":
            init = 0
        for scope in list(self.ScopeManager.Stack)[init: scope]:
            pos += len(list(scope.keys()))
        code = ctx.getChild(2).accept(self)
        code += f"\tsw     $a0 -{pos * 4}($fp)\n"
        return code

    # Visit a parse tree produced by COOL#false.
    def visitFalse(self, ctx: COOL.FalseContext):
        self.CurrentType = "Bool"
        return "\tla     $a0 bool_const0\n"

    # Visit a parse tree produced by COOL#int.
    def visitInt(self, ctx: COOL.IntContext):
        val = int(ctx.getChild(0).symbol.text)
        self.CurrentType = "Int"
        for const in self.ConstantTable:
            (constVal, constType, constTag) = const
            if constType == "Int" and constVal == val:
                return f"\tla     $a0 {constTag}\n"

    # Visit a parse tree produced by COOL#equal.
    def visitEqual(self, ctx: COOL.EqualContext):
        code = ctx.getChild(0).accept(self)
        code += \
            "\tsw     $a0 0($sp)\n" + \
            "\taddiu  $sp $sp -4\n"
        code += ctx.getChild(2).accept(self)
        code += \
            "\tmove    $t2 $a0\n" \
            "\tlw     $t1 4($sp)\n" \
            "\taddiu  $sp $sp 4\n" \
            "\tla     $a0 bool_const1\n" \
            "\tla     $a1 bool_const0\n" \
            "\tjal    equality_test\n"
        self.CurrentType = "Bool"
        return code

    # Visit a parse tree produced by COOL#true.
    def visitTrue(self, ctx: COOL.TrueContext):
        self.CurrentType = "Bool"
        return "\tla     $a0 bool_const1\n"

    # Visit a parse tree produced by COOL#lessEqual.
    def visitLessEqual(self, ctx: COOL.LessEqualContext):
        code = ctx.getChild(0).accept(self)
        code += \
            "\tsw     $a0 0($sp)\n" + \
            "\taddiu  $sp $sp -4\n"
        code += ctx.getChild(2).accept(self)
        code += \
            "\tjal    Object.copy\n" \
            "\tlw     $t0 4($sp)\n" \
            "\tlw     $t1 12($t0)\n" \
            "\tlw     $t2 12($a0)\n" \
            "\tslt    $t3 $t2 $t1\n" \
            "\tnegu   $t4 $t3\n" \
            "\taddiu  $t5 $t4 1\n" \
            "\tla     $a0 bool_const0\n" \
            "\tjal    Object.copy\n" \
            "\tsw     $t5 12($a0)\n" \
            "\taddiu  $sp $sp 4\n"
        self.CurrentType = "Bool"
        return code

    # Visit a parse tree produced by COOL#methodCall.
    def visitMethodCall(self, ctx: COOL.MethodCallContext):
        length = 5
        methodPos = 2
        objCode = ctx.getChild(0).accept(self)
        code = ""
        classId = self.CurrentType
        if ctx.getChild(1).symbol.text == "@":
            length += 2
            methodPos += 2
            classId = ctx.getChild(2).symbol.text
        count = methodPos + 2
        if len(ctx.children) > length:
            length = len(ctx.children)
            while length != count:
                param = (ctx.getChild(count).accept(self) or "")
                code += param + \
                        f"\tsw     $a0 0($sp)\n" \
                        f"\taddiu  $sp $sp -4\n"
                count = count + 2
        methodIdx = self.TypeTable[classId].TagMethods.index(ctx.getChild(methodPos).symbol.text)
        self.CurrentType = self.searchMethodInfo(classId, ctx.getChild(methodPos).symbol.text)
        code += objCode + \
                "\tlw     $t1 8($a0)\n" \
                f"\tlw     $t1 {methodIdx * 4}($t1)\n" \
                "\tjalr   $t1\n"
        return code

    RuntimeMessages = """
#
# Messages for the Runtime
#
	.data

_abort_msg:	.asciiz "Abort called from class "
_colon_msg:	.asciiz ":"
_dispatch_msg:  .asciiz ": Dispatch to void.\\n"
_cabort_msg:	.asciiz "No match in case statement for Class "
_cabort_msg2:   .asciiz "Match on void in case statement.\\n"
_nl:		.asciiz "\\n"
_term_msg:	.asciiz "\nCOOL program successfully executed\\n"
_sabort_msg1:	.asciiz	"Index to substr is negative\\n"
_sabort_msg2:	.asciiz	"Index to substr is too big\\n"
_sabort_msg3:	.asciiz	"Length to substr too long\\n"
_sabort_msg4:	.asciiz	"Length to substr is negative\\n"
_sabort_msg:	.asciiz "Execution aborted.\\n"
_objcopy_msg:	.asciiz "Object.copy: Invalid object size.\\n"
_gc_abort_msg:	.asciiz "GC bug!\\n"

#
# Messages for the GenGC garabge collector
#

_GenGC_INITERROR:	.asciiz "GenGC: Unable to initialize the garbage collector.\\n"
_GenGC_COLLECT:		.asciiz "Garbage collecting ...\\n"
_GenGC_Major:		.asciiz "Major ...\\n"
_GenGC_Minor:		.asciiz "Minor ...\\n"
#_GenGC_COLLECT:		.asciiz ""
_GenGC_MINORERROR:	.asciiz "GenGC: Error during minor garbage collection.\\n"
_GenGC_MAJORERROR:	.asciiz "GenGC: Error during major garbage collection.\\n"

#
# Messages for the NoGC garabge collector
#

_NoGC_COLLECT:		.asciiz "Increasing heap...\\n"
#_NoGC_COLLECT:		.asciiz ""    
"""

    MemManagerNoGCInit = """
	.data
	.align 2

	.globl	_MemMgr_INITIALIZER
_MemMgr_INITIALIZER:
	.word	_NoGC_Init
	.globl	_MemMgr_COLLECTOR
_MemMgr_COLLECTOR:
	.word	_NoGC_Collect
	.globl	_MemMgr_TEST
_MemMgr_TEST:
	.word	0
"""

    MemManagerGenGCInit = """
    	.data
    	.align 2

    	.globl	_MemMgr_INITIALIZER
    _MemMgr_INITIALIZER:
    	.word	_GenGC_Init
    	.globl	_MemMgr_COLLECTOR
    _MemMgr_COLLECTOR:
    	.word	_GenGC_Collect
    	.globl	_MemMgr_TEST
    _MemMgr_TEST:
    	.word	0
    """

    RuntimeCode = """
#
# Define some constants
#

obj_eyecatch=-4	# Unique id to verify any object
obj_tag=0
obj_size=4
obj_disp=8
obj_attr=12
int_slot=12
bool_slot=12
str_size=12	# This is a pointer to an Int object!!!
str_field=16	# The beginning of the ascii sequence
str_maxsize=1026	# the maximum string length

#
# The REG mask tells the garbage collector which register(s) it
# should automatically update on a garbage collection.  Note that
# this is (ANDed) with the ARU mask before the garbage collector
# reads it.  Only the registers specified in the garbage collector's
# ARU mask can be automatically updated.
#
# BITS----------------------------
# 3 2         1         0
# 10987654321098765432109876543210
# --------------------------------
#
# 00000000011111110000000000000000  <-  initial Register (REG) mask
# +--++--++--++--++--++--++--++--+      $s0-$s6
#    0   0   7   F   0   0   0   0     ($16-$22)
#

MemMgr_REG_MASK=0x007F0000

	.text
	.globl main
main:
	li	$v0 9
	move	$a0 $zero
	syscall				# sbrk
	move	$a0 $sp			# initialize the garbage collector
	li	$a1 MemMgr_REG_MASK
	move	$a2 $v0
	jal	_MemMgr_Init		# sets $gp and $s7 (limit)
	la	$a0 Main_protObj	# create the Main object
	jal	Object.copy		# Call copy
	addiu	$sp $sp -4
	sw	$a0 4($sp)		# save the Main object on the stack
	move	$s0 $a0			# set $s0 to point to self
	jal	Main_init		# initialize the Main object
	jal	Main.main		# Invoke main method
	addiu	$sp $sp 4		# restore the stack
	la	$a0 _term_msg		# show terminal message
	li	$v0 4
	syscall
	li $v0 10
	syscall				# syscall 10 (exit)

#
#  Polymorphic equality testing function:
#  Two objects are equal if they are
#    - identical (pointer equality, inlined in code)
#    - have same tag and are of type BOOL,STRING,INT and contain the
#      same data
#
#  INPUT: The two objects are passed in $t1 and $t2
#  OUTPUT: Initial value of $a0, if the objects are equal
#          Initial value of $a1, otherwise
#
#  The tags for Int,Bool,String are found in the global locations
#  _int_tag, _bool_tag, _string_tag, which are initialized by the
#  data part of the generated code. This removes a consistency problem
#  between this file and the generated code.
#

	.globl	equality_test
equality_test:			# ops in $t1 $t2
				# true in A0, false in A1
				# assume $t1, $t2 are not equal
	beq	$t1 $zero _eq_false # $t2 can't also be void   
	beq     $t2 $zero _eq_false # $t1 can't also be void   
	lw	$v0 obj_tag($t1)	# get tags
	lw	$v1 obj_tag($t2)
	bne	$v1 $v0 _eq_false	# compare tags
	lw	$a2 _int_tag	# load int tag
	beq	$v1 $a2 _eq_int	# Integers
	lw	$a2 _bool_tag	# load bool tag
	beq	$v1 $a2 _eq_int	# Booleans
	lw	$a2 _string_tag # load string tag
	bne	$v1 $a2 _eq_false  # Not a primitive type
_eq_str: # handle strings
	lw	$v0, str_size($t1)	# get string size objs
	lw	$v1, str_size($t2)
	lw	$v0, int_slot($v0)	# get string sizes
	lw	$v1, int_slot($v1)
	bne	$v1 $v0 _eq_false
	beqz	$v1 _eq_true		# 0 length strings are equal
	add	$t1 str_field		# Point to start of string
	add	$t2 str_field
	move	$t0 $v0		# Keep string length as counter
_eq_l1:
	lbu	$v0,0($t1)	# get char
	add	$t1 1
	lbu	$v1,0($t2)
	add	$t2 1
	bne	$v1 $v0 _eq_false
	addiu	$t0 $t0 -1	# Decrement counter
	bnez	$t0 _eq_l1
	b	_eq_true		# end of strings
		
_eq_int:	# handles booleans and ints
	lw	$v0,int_slot($t1)	# load values
	lw	$v1,int_slot($t2)
	bne	$v1 $v0 _eq_false
_eq_true:
	jr	$ra		# return true
_eq_false:
	move	$a0 $a1		# move false into accumulator
	jr	$ra

#
#  _dispatch_abort
#
#      filename in $a0
#      line number in $t1
#  
#  Prints error message and exits.
#  Called on dispatch to void.
#
	.globl	_dispatch_abort
_dispatch_abort:		 
        sw      $t1 0($sp)       # save line number
        addiu   $sp $sp -4
	addiu   $a0 $a0 str_field # adjust to beginning of string
	li      $v0 4
	syscall                  # print file name
	la      $a0 _colon_msg
	li	$v0 4
	syscall                  # print ":"
	lw      $a0 4($sp)       # 
	li	$v0 1
	syscall			 # print line number
	li 	$v0 4
	la	$a0 _dispatch_msg
	syscall			 # print dispatch-to-void message
	li   	$v0 10
        syscall			 # exit


#
#  _case_abort2
#
#      filename in $a0
#      line number in $t1
#  
#  Prints error message and exits.
#  Called on case on void.
#
	.globl	_case_abort2
_case_abort2:		 
        sw      $t1 0($sp)       # save line number
        addiu   $sp $sp -4
	addiu   $a0 $a0 str_field # adjust to beginning of string
	li      $v0 4
	syscall                  # print file name
	la      $a0 _colon_msg
	li	$v0 4
	syscall                  # print ":"
	lw      $a0 4($sp)       # 
	li	$v0 1
	syscall			 # print line number
	li 	$v0 4
	la	$a0 _cabort_msg2
	syscall			 # print case-on-void message
	li   	$v0 10
        syscall			 # exit
	
#
#
#  _case_abort
#		Is called when a case statement has no match
#
#   INPUT:	$a0 contains the object on which the case was
#		performed
#
#   Does not return!
#
	.globl	_case_abort
_case_abort:			# $a0 contains case expression obj.
	move	$s0 $a0		# save the expression object
	la	$a0 _cabort_msg
	li	$v0 4
	syscall			# print_str
	la	$t1 class_nameTab
	lw	$v0 obj_tag($s0)	# Get object tag
	sll	$v0 $v0 2	# *4
	addu	$t1 $t1 $v0
	lw	$t1 0($t1)	# Load class name string obj.
	addiu	$a0 $t1 str_field # Adjust to beginning of str
	li	$v0 4		# print_str
	syscall
	la	$a0 _nl
	li	$v0 4		# print_str
	syscall
	li	$v0 10
	syscall			# Exit
	

#
# Copy method
#
#   Copies an object and returns a pointer to a new object in
#   the heap.  Note that to increase performance, the stack frame
#   is not set up unless it is absolutely needed.  As a result,
#   the frame is setup just before the call to "_MemMgr_Alloc" and
#   is destroyed just after it.  The increase in performance
#   occurs becuase the calls to "_MemMgr_Alloc" happen very
#   infrequently when the heap needs to be garbage collected.
#
#   INPUT:	$a0: object to be copied to free space in heap
#
#   OUTPUT:	$a0: points to the newly created copy.
#
#   Registers modified:
#	$t0, $t1, $t2, $v0, $v1, $a0, $a1, $a2, $gp, $s7
#

	.globl	Object.copy
Object.copy:
	addiu	$sp $sp -8			# create stack frame
	sw	$ra 8($sp)
	sw	$a0 4($sp)

	jal	_MemMgr_Test			# test GC area

	lw	$a0 4($sp)			# get object size
	lw	$a0 obj_size($a0)
	blez	$a0 _objcopy_error		# check for invalid size
	sll	$a0 $a0 2			# convert words to bytes
	addiu	$a0 $a0 4			# account for eyecatcher
	jal	_MemMgr_Alloc			# allocate storage
	addiu	$a1 $a0 4			# pointer to new object

	lw	$a0 4($sp)			# the self object
	lw	$ra 8($sp)			# restore return address
	addiu	$sp $sp 8			# remove frame
	lw	$t0 obj_size($a0)		# get size of object
	sll	$t0 $t0 2			# convert words to bytes
	b	_objcopy_allocated		# get on with the copy

# A faster version of Object.copy, for internal use (does not call
# _MemMgr_Test, and if possible not _MemMgr_Alloc)

_quick_copy:
	lw	$t0 obj_size($a0)		# get size of object to copy
	blez	$t0 _objcopy_error		# check for invalid size
	sll	$t0 $t0 2			# convert words to bytes
	addiu	$t1 $t0 4			# account for eyecatcher
	add	$gp $gp $t1			# allocate memory
	sub	$a1 $gp $t0			# pointer to new object
	blt	$gp $s7 _objcopy_allocated	# check allocation
_objcopy_allocate:
	sub	$gp $a1 4			# restore the original $gp
	addiu	$sp $sp -8			# frame size
	sw	$ra 8($sp)			# save return address
	sw	$a0 4($sp)			# save self
	move	$a0 $t1				# put bytes to allocate in $a0
	jal	_MemMgr_Alloc			# allocate storage
	addiu	$a1 $a0 4			# pointer to new object
	lw	$a0 4($sp)			# the self object
	lw	$ra 8($sp)			# restore return address
	addiu	$sp $sp 8			# remove frame
	lw	$t0 obj_size($a0)		# get size of object
	sll	$t0 $t0 2			# convert words to bytes
_objcopy_allocated:
	addiu	$t1 $0 -1
	sw	$t1 obj_eyecatch($a1)		# store eyecatcher
	add	$t0 $t0 $a0			# find limit of copy
	move	$t1 $a1				# save source
_objcopy_loop:
	lw	$v0 0($a0)			# copy word
	sw	$v0 0($t1)
	addiu	$a0 $a0 4			# update source
	addiu	$t1 $t1 4			# update destination
	bne	$a0 $t0 _objcopy_loop		# loop
_objcopy_end:
	move	$a0 $a1				# put new object in $a0
	jr	$ra				# return
_objcopy_error:
	la	$a0 _objcopy_msg		# show error message
	li	$v0 4
	syscall
	li	$v0 10				# exit
	syscall

#
#
# Object.abort
#
#	The abort method for the object class (usually inherited by
#	all other classes)
#
#   INPUT:	$a0 contains the object on which abort() was dispatched.
#

	.globl	Object.abort
Object.abort:
	move	$s0 $a0		# save self
	li	$v0 4
	la	$a0 _abort_msg
	syscall			# print_str
	la	$t1 class_nameTab
	lw	$v0 obj_tag($s0)	# Get object tag
	sll	$v0 $v0 2	# *4
	addu	$t1 $t1 $v0
	lw	$t1 0($t1)	# Load class name string obj.
	addiu	$a0 $t1 str_field	# Adjust to beginning of str
	li	$v0 4		# print_str
	syscall
	la	$a0 _nl
	li	$v0 4
	syscall			# print new line
	li	$v0 10
	syscall			# Exit

#
#
# Object.type_name	
#
#   	INPUT:	$a0 object who's class name is desired
#	OUTPUT:	$a0 reference to class name string object
#

	.globl	Object.type_name
Object.type_name:
	la	$t1 class_nameTab
	lw	$v0 obj_tag($a0)	# Get object tag
	sll	$v0 $v0 2	# *4
	addu	$t1 $t1 $v0	# index table
	lw	$a0 0($t1)	# Load class name string obj.
	jr	$ra

#
#
# IO.out_string
#
#	Prints out the contents of a string object argument
#	which is on top of the stack.
#
#	$a0 is preserved!
#

	.globl	IO.out_string
IO.out_string:
	addiu	$sp $sp -4
	sw	$a0 4($sp)	# save self
	lw	$a0 8($sp)	# get arg
	addiu	$a0 $a0 str_field	# Adjust to beginning of str
	li	$v0 4		# print_str
	syscall
	lw	$a0 4($sp)	# return self
	addiu	$sp $sp 8	# pop argument
	jr	$ra

#
#
# IO.out_int
#
#	Prints out the contents of an integer object on top of the
#	stack.
#
#	$a0 is preserved!
#

	.globl	IO.out_int
IO.out_int:
	addiu	$sp $sp -4
	sw	$a0 4($sp)	# save self
	lw	$a0 8($sp)	# get arg
	lw	$a0 int_slot($a0)	# Fetch int
	li	$v0 1		# print_int
	syscall	
	lw	$a0 4($sp)	# return self
	addiu	$sp $sp 8	# pop argument
	jr	$ra

#
#
# IO.in_int
#
#	Returns an integer object read from the terminal in $a0
#

	.globl	IO.in_int
IO.in_int:
	addiu	$sp $sp -4
	sw	$ra 4($sp)	# save return address

        la      $a0 Int_protObj
        jal     _quick_copy	# Call copy
        jal     Int_init

	addiu	$sp $sp -4
	sw	$a0 4($sp)	# save new object

	li	$v0, 5		# read int
	syscall

	lw	$a0 4($sp)
	addiu	$sp $sp 4


	sw	$v0 int_slot($a0)	# store int read into obj
	lw	$ra 4($sp)
	addiu	$sp $sp 4
	jr	$ra

#
#
# IO.in_string
#
#	Returns a string object read from the terminal, removing the
#	'\\n'
#
#	OUTPUT:	$a0 the read string object
#

	.globl	IO.in_string
IO.in_string:
	addiu	$sp $sp -8
	sw	$ra 8($sp)			# save return address
	sw	$0 4($sp)			# init GC area

	jal	_MemMgr_Test			# test GC area

	la	$a0 Int_protObj			# Int object for string size
	jal	_quick_copy
	jal	Int_init
	sw	$a0 4($sp)			# save it

	li	$a0 str_field			# size of string obj. header
	addiu	$a0 $a0 str_maxsize		# max size of string data
	jal	_MemMgr_QAlloc			# make sure enough room

	la	$a0 String_protObj		# make string object
	jal	_quick_copy
	jal	String_init
	lw	$t0 4($sp)			# get size object
	sw	$t0 str_size($a0)		# store size object in string
	sw	$a0 4($sp)			# save string object

	addiu	$gp $gp -4			# overwrite last word

_instr_ok:
	li	$a1 str_maxsize			# largest string to read
	move	$a0 $gp	
	li	$v0, 8				# read string
	syscall

	move	$t0 $gp				# t0 to beginning of string
_instr_find_end:
	lb	$v0 0($gp)
	addiu	$gp $gp 1
	bnez	$v0 _instr_find_end

	# $gp points just after the null byte
	lb	$v0 0($t0)			# is first byte '\\0'?
	bnez	$v0 _instr_noteof

	# we read nothing. Return '\\n' (we don't have '\\0'!!!)
	add	$v0 $zero 10			# load '\\n' into $v0
	sb	$v0 -1($gp)
	sb	$zero 0($gp)			# terminate
	addiu	$gp $gp 1
	b	_instr_nonl

_instr_noteof:
	# Check if there really is a '\\n'
	lb	$v0 -2($gp)
	bne	$v0 10 _instr_nonl

	# Write '\\0' over '\\n'
	sb	$zero -2($gp)			# Set end of string where '\\n' was
	addiu	$gp $gp -1			# adjust for '\\n'

_instr_nonl:
	lw	$a0 4($sp)			# get pointer to new str obj
	lw	$t1 str_size($a0)		# get pointer to int obj

	sub	$t0 $gp $a0
	subu	$t0 str_field			# calc actual str size
	addiu	$t0  -1				# adjust for '\\0'
	sw	$t0 int_slot($t1)		# store string size in int obj
	addi	$gp $gp 3			# was already 1 past '\\0'
	and	$gp $gp 0xfffffffc		# word align $gp

	sub	$t0 $gp $a0			# calc length
	srl	$t0 $t0 2			# divide by 4
	sw	$t0 obj_size($a0)		# set size field of obj

	lw	$ra 8($sp)			# restore return address
	addiu	$sp $sp 8
	jr	$ra				# return

#
#
# String.length
#		Returns Int Obj with string length of self
#
#	INPUT:	$a0 the string object
#	OUTPUT:	$a0 the int object which is the size of the string
#

	.globl	String.length
String.length:
	lw	$a0 str_size($a0)	# fetch attr
	jr	$ra	# Return

#
# String.concat
#
#   Concatenates arg1 onto the end of self and returns a pointer
#   to the new object.
#
#	INPUT:	$a0: the first string object (self)
#		Top of stack: the second string object (arg1)
#
#	OUTPUT:	$a0 the new string object
#

	.globl	String.concat
String.concat:

	addiu	$sp $sp -16
	sw	$ra 16($sp)			# save return address
	sw	$a0 12($sp)			# save self arg.
	sw	$0 8($sp)			# init GC area
	sw	$0 4($sp)			# init GC area

	jal	_MemMgr_Test			# test GC area

	lw	$a0 12($sp)
	lw	$a0 str_size($a0)
	jal     _quick_copy			# Call copy
	sw	$a0 8($sp)			# save new size object

	lw	$t1 20($sp)			# load arg object
	lw	$t1 str_size($t1)		# get size object
	lw	$t1 int_slot($t1)		# arg string size
	blez	$t1 _strcat_argempty		# nothing to add
	lw	$t0 12($sp)			# load self object
	lw	$t0 str_size($t0)		# get size object
	lw	$t0 int_slot($t0)		# self string size
	addu	$t0 $t0 $t1			# new size
	sw	$t0 int_slot($a0)		# store new size

	addiu	$a0 $t0 str_field		# size to allocate
	addiu	$a0 $a0 4			# include '\\0', +3 to align
	and	$a0 $a0 0xFFFFFFFC		# align on word boundary
	addiu   $a0 $a0 1                       # make size odd for GC <-|
	sw	$a0 4($sp)			# save size in bytes     |
	addiu	$a0 $a0 3			# include eyecatcher(4) -1
	jal	_MemMgr_QAlloc			# check memory

	lw	$a0 12($sp)			# copy self
	jal	_quick_copy			# Call copy
	lw	$t0 8($sp)			# get the Int object
	sw	$t0 str_size($a0)		# store it in the str obj.

	sub	$t1 $gp $a0			# bytes allocated by _quick_copy
	lw	$t0 4($sp)			# get size in bytes (no eyecatcher)
	sub     $t0 $t0 1                       # Remove extra 1 (was for GC)
	sub	$t1 $t0 $t1			# more memory needed
	addu	$gp $gp $t1			# allocate rest
	srl	$t0 $t0 2			# convert to words
	sw	$t0 obj_size($a0)		# save new object size

	lw	$t0 12($sp)			# get original self object
	lw	$t0 str_size($t0)		# get size object
	lw	$t0 int_slot($t0)		# self string size
	addiu	$t1 $a0 str_field		# points to start of string data
	addu	$t1 $t1 $t0			# points to end: '\\0'
	lw	$t0 20($sp)			# load arg object
	addiu	$t2 $t0 str_field		# points to start of arg data
	lw	$t0 str_size($t0)		# get arg size
	lw	$t0 int_slot($t0)
	addu	$t0 $t0 $t2			# find limit of copy

_strcat_copy:
	lb	$v0 0($t2)			# load from source
	sb	$v0 0($t1)			# save in destination
	addiu	$t2 $t2 1			# advance each index
	addiu	$t1 $t1 1
	bne	$t2 $t0 _strcat_copy		# check limit
	sb	$0 0($t1)			# add '\\0'

	lw	$ra 16($sp)			# restore return address
	addiu	$sp $sp 20			# pop argument
	jr	$ra				# return

_strcat_argempty:
	lw	$a0 12($sp)			# load original self
	lw	$ra 16($sp)			# restore return address
	addiu	$sp $sp 20			# pop argument
	jr	$ra				# return

#
#
# String.substr(i,l)
#		Returns the sub string of self from i with length l
#		Offset starts at 0.
#
#	INPUT:	$a0 the string
#		length int object on top of stack (-4)
#		index int object below length on stack (-8)
#	OUTPUT:	The substring object in $a0
#

	.globl	String.substr
String.substr:
	addiu	$sp $sp -12		# frame
	sw	$ra 4($sp)		# save return
	sw	$a0 12($sp)		# save self
	sw	$0 8($sp)		# init GC area

	jal	_MemMgr_Test		# test GC area

	lw	$a0 12($sp)
	lw	$v0 obj_size($a0)
        la      $a0 Int_protObj		# ask if enough room to allocate
	lw	$a0 obj_size($a0)	#   a string object, an int object,
	add	$a0 $a0 $v0		#   and the string data
	addiu	$a0 $a0 2		# include 2 eyecatchers
	sll	$a0 $a0 2
	addi	$a0 $a0 str_maxsize
	jal	_MemMgr_QAlloc

_ss_ok:
	la	$a0 Int_protObj
	jal	_quick_copy
	jal	Int_init
	sw	$a0 8($sp)	# save new length obj
	la	$a0 String_protObj
	jal	_quick_copy
	jal	String_init	# new obj ptr in $a0
	move	$a2 $a0		# use a2 to make copy
	addiu	$gp $gp -4	# backup alloc ptr
	lw	$a1 12($sp)	# load orig
	lw	$t1 20($sp)	# index obj
	lw	$t2 16($sp)	# length obj
	lw	$t0 str_size($a1)
	lw	$v1 int_slot($t1) # index
	lw	$v0 int_slot($t0) # size of orig
	bltz	$v1 _ss_abort1	# index is smaller than 0
	bgt	$v1 $v0 _ss_abort2	# index > orig
	lw	$t3 int_slot($t2) # sub length
	add	$v1 $v1 $t3	# index+sublength
	bgt	$v1 $v0 _ss_abort3
	bltz	$t3 _ss_abort4
	lw	$t4 8($sp)	# load new length obj
	sw	$t3 int_slot($t4) # save new size
	sw	$t4 str_size($a0) # store size in string
	lw	$v1 int_slot($t1) # index
	addiu	$a1 $a1 str_field # advance src to str
	add	$a1 $a1 $v1	  # advance to indexed char
	addiu	$a2 $a2 str_field # advance dst to str
	beqz	$t3 _ss_end	  # empty length
_ss_loop:
	lb	$v0 0($a1)
	addiu	$a1 $a1 1	# inc src
	sb	$v0 0($a2)
	addiu	$a2 $a2 1	# inc dst
	addiu	$t3 $t3 -1	# dec ctr
	bnez	$t3 _ss_loop
_ss_end:
	sb	$zero 0($a2)	# null terminate
	move	$gp $a2
	addiu	$gp $gp 4	# realign the heap ptr
	and	$gp $gp 0xfffffffc

	sub	$t0 $gp $a0	# calc object size
	srl	$t0 $t0 2	# div by 4
	sw	$t0 obj_size($a0)

	lw	$ra 4($sp)
	addiu	$sp $sp 20	# pop arguments
	jr	$ra

_ss_abort1:
	la	$a0 _sabort_msg1
	b	_ss_abort
_ss_abort2:
	la	$a0 _sabort_msg2
	b	_ss_abort
_ss_abort3:
	la	$a0 _sabort_msg3
	b	_ss_abort
_ss_abort4:
	la	$a0 _sabort_msg4
_ss_abort:
	li	$v0 4
	syscall
	la	$a0 _sabort_msg
	li	$v0 4
	syscall
	li	$v0 10		# exit
	syscall

#
# MemMgr Memory Manager
#
#   The MemMgr functions give a consistent view of the garbage collectors.
#   This allows multiple collectors to exist in one file and the easy
#   selection of different collectors.  It includes functions to initialize
#   the collector and to reserve memory and query its status.
#
#   The following assumptions are made:
#
#     1) The allocation of memory involves incrementing the $gp pointer.
#        The $s7 pointer serves as a limit.  The collector function is
#        called before $s7 is exceeded by $gp.
#
#     2) The initialization functions all take the same arguments as
#        defined in "_MemMgr_Init".
#
#     3) The garbage collector functions all take the arguments.  "$a0"
#        contains the end of the stack to check for pointers.  "$a1"
#        contains the size in bytes needed by the program and must be
#        preserved across the function call.
#

#
# Initialize the Memory Manager
#
#   Call the initialization routine for the garbage collector.
#
#   INPUT:
#	$a0: start of stack
#	$a1: initial Register mask
#	$a2: end of heap
#	heap_start: start of the heap
#
#   OUTPUT:
#	$gp: lower bound of the work area
#	$s7: upper bound of the work area
#
#   Registers modified:
#	$t0, initializer function
#

	.globl _MemMgr_Init
_MemMgr_Init:
	addiu	$sp $sp -4
	sw	$ra 4($sp)			# save return address
	la	$t0 _MemMgr_INITIALIZER		# pointer to initialization
	lw	$t0 0($t0)
	jalr	$t0				# initialize
	lw	$ra 4($sp)			# restore return address
	addiu	$sp $sp 4
	jr	$ra				# return

#
# Memory Allocation
#
#   Allocates the requested amount of memory and returns a pointer
#   to the start of the block.
#
#   INPUT:
#	$a0: size of allocation in bytes
#	$s7: limit pointer of the work area
#	$gp: current allocation pointer
#	heap_start: start of heap
#
#   OUTPUT:
#	$a0: pointer to new memory block
#
#   Registers modified:
#	$t0, $a1, collector function
#

	.globl _MemMgr_Alloc
_MemMgr_Alloc:
	add	$gp $gp $a0			# attempt to allocate storage
	blt	$gp $s7 _MemMgr_Alloc_end	# check allocation
	sub	$gp $gp $a0			# restore $gp
	addiu	$sp $sp -4
	sw	$ra 4($sp)			# save return address
	move	$a1 $a0				# size
	addiu	$a0 $sp 4			# end of stack to collect
	la	$t0 _MemMgr_COLLECTOR		# pointer to collector function
	lw	$t0 0($t0)
	jalr	$t0				# garbage collect
	lw	$ra 4($sp)			# restore return address
	addiu	$sp $sp 4
	move	$a0 $a1				# put size into $a0
	add	$gp $gp $a0			# allocate storage
_MemMgr_Alloc_end:
	sub	$a0 $gp $a0
	jr	$ra				# return

#
# Query Memory Allocation
#
#   Verifies that the requested amount of memory can be allocated
#   within the work area.
#
#   INPUT:
#	$a0: size of allocation in bytes
#	$s7: limit pointer of the work area
#	$gp: current allocation pointer
#	heap_start: start of heap
#
#   OUTPUT:
#	$a0: size of allocation in bytes (unchanged)
#
#   Registers modified:
#	$t0, $a1, collector function
#

	.globl _MemMgr_QAlloc
_MemMgr_QAlloc:
	add	$t0 $gp $a0			# attempt to allocate storage
	blt	$t0 $s7 _MemMgr_QAlloc_end	# check allocation
	addiu	$sp $sp -4
	sw	$ra 4($sp)			# save return address
	move	$a1 $a0				# size
	addiu	$a0 $sp 4			# end of stack to collect
	la	$t0 _MemMgr_COLLECTOR		# pointer to collector function
	lw	$t0 0($t0)
	jalr	$t0				# garbage collect
	lw	$ra 4($sp)			# restore return address
	addiu	$sp $sp 4
	move	$a0 $a1				# put size into $a0
_MemMgr_QAlloc_end:
	jr	$ra				# return

#
# Test heap consistency
#
#   Runs the garbage collector in the hope that this will help detect
#   garbage collection bugs earlier.
#
#   INPUT: (the usual GC stuff)
#	$s7: limit pointer of the work area
#	$gp: current allocation pointer
#	heap_start: start of heap
#
#   OUTPUT:
#	none
#
#   Registers modified:
#	$t0, $a1, collector function

	.globl	_MemMgr_Test
_MemMgr_Test:
	la	$t0 _MemMgr_TEST		# Check if testing enabled
	lw	$t0 0($t0)
	beqz	$t0 _MemMgr_Test_end

# Allocate 0 bytes
	addiu	$sp $sp -4			# Save return address
	sw	$ra 4($sp)
	li	$a1 0				# size = 0
	addiu	$a0 $sp 4			# end of stack to collect
	la	$t0 _MemMgr_COLLECTOR		# pointer to collector function
	lw	$t0 0($t0)
	jalr	$t0				# garbage collect
	lw	$ra 4($sp)			# restore return address
	addiu	$sp $sp 4

_MemMgr_Test_end:
	jr	$ra
"""

    MemManagerNoGC = """
#
# NoGC Garbage Collector
#
#   NoGC does not attempt to do any garbage collection.
#   It simply expands the heap if more memory is needed.
#

#
# Some constants
#

NoGC_EXPANDSIZE=0x10000				# size to expand heap

#
# Initialization
#
#   INPUT:
#	none
#
#   OUTPUT:
#	$gp: lower bound of the work area
#	$s7: upper bound of the work area
#
#   Registers modified:
#	$a0, $v0
#
	.globl _NoGC_Init
_NoGC_Init:
	la	$gp heap_start			# set $gp to the start of the heap
	li	$v0 9				# get heap end
	move	$a0 $zero
	syscall					# sbrk
	move	$s7 $v0				# set limit pointer
	jr	$ra

#
# Collection
#
#   Expand the heap as necessary.
#
#   INPUT:
#	$a1: size will need to allocate in bytes
#	$s7: limit pointer of thw work area
#	$gp: current allocation pointer
#
#   OUTPUT:
#	$a1: size will need to allocate in bytes (unchanged)
#
#   Registers modified:
#	$t0, $a0, $v0, $gp, $s7
#

	.globl _NoGC_Collect
_NoGC_Collect:
	la	$a0 _NoGC_COLLECT		# show collection message
	li	$v0 4
	syscall
_NoGC_Collect_loop:
	add	$t0 $gp $a1			# test allocation
	blt	$t0 $s7 _NoGC_Collect_ok	# stop if enough
	li	$v0 9				# expand heap
	li	$a0 NoGC_EXPANDSIZE		# set the size to expand the heap
	syscall					# sbrk
	li	$v0 9				# get heap end
	move	$a0 $zero
	syscall					# sbrk
	move	$s7 $v0				# set limit pointer
	b	_NoGC_Collect_loop		# loop
_NoGC_Collect_ok:
	jr	$ra				# return
"""

    MemManagerGenGC = """
#
# GenGC Generational Garbage Collector
#
#   This is an implementation of a generational garbage collector
#   as described in "Simple Generational Garbage Collection and Fast
#   Allocation" by Andrew W. Appel [Princeton University, March 1988].
#   This is a two generation scheme which uses an assignment table
#   to handle root pointers located in the older generation objects.
#
#   When the work area is filled, a minor garbage collection takes place
#   which moves all live objects into the reserve area.  These objects
#   are then incorporated into the old area.  New reserve and work areas
#   are setup and allocation can continue in the work area.  If a break-
#   point is reached in the size of the old area just after a minor
#   collection, a major collection then takes place.  All live objects in
#   the old area are then copied into the new area, expanding the heap if
#   necessary.  The X and new areas are then block copied back L1-L0
#   bytes to form the next old area.
#
#   The assignment table is implemented as a stack growing towards the
#   allocation pointer ($gp) in the work area.  If they cross, a minor
#   collection is then carried out.  This allows the garbage collector to
#   to have to keep a fixed table of assignments.  As a result, programs
#   with many assignments will tend not to be bogged down with extra
#   garbage collections.
#
#   The unused area was implemented to help keep the garbage collector
#   from continually expanding the heap.  This buffer zone allows major
#   garbage collections to happen earlier, reducing the risk of expansions
#   due to too many live objects in the old area.  The histories kept by
#   the garbage collector in MAJOR0, MAJOR1, MINOR0, and MINOR1 also help
#   to prevent unnecessary expansions of the heap.  If many live objects
#   were recently collected, the garbage collections will start to occur
#   sooner.
#
#   Note that during a minor collection, the work area is guaranteed to
#   fit within the reserve area.  However, during a major collection, the
#   old area will not necessarily fit in the new area.  If the latter occurs,
#   "_GenGC_OfsCopy" will detect this and expand the heap.
#
#   The heap is expanded on two different occasions:
#
#     1) After a major collection, the old area is set to be at most
#        1/(2^GenGC_OLDRATIO) of the usable heap (L0 to L3).  Note that
#        first L4 is checked to see if any of the unused memory between L3
#        and L4 is enough to satisfy this requirement.  If not, then the
#        heap will be expanded.  If it is, the appropriate amount will be
#        transfered from the unused area to the work/reserve area.
#
#     2) During a major collection, if the live objects in the old area
#        do not fit within the new area, the heap is expanded and $s7
#        is updated to reflact this.  This value later gets stored back
#        into L4.
#
#   During a normal allocation and minor collections, the heap has the
#   following form:
#
#      Header
#       |
#       |   Older generation objects
#       |    |
#       |    |             Minor garbage collection area
#       |    |              |
#       |    |              |                Allocation area
#       |    |              |                 |
#       |    |              |                 |           Assignment table
#       |    |              |                 |            |
#       |    |              |                 |            |   Unused
#       |    |              |                 |            |    |
#       v    v              v                 v            v    v
#     +----+--------------+-----------------+-------------+---+---------+
#     |XXXX| Old Area     | Reserve Area    | Work Area   |XXX| Unused  |
#     +----+--------------+-----------------+-------------+---+---------+
#      ^    ^              ^                 ^    ^        ^   ^         ^
#      |    |              |                 |    |-->  <--|   |         |
#      |    L0             L1                L2  $gp      $s7  L3        L4
#      |
#     heap_start
#
#     $gp (allocation pointer): points to the next free word in the work
#         area during normal allocation.  During a minor garbage collection,
#         it points to the next free work in the reserve area.
#
#     $s7 (limit pointer): points to the limit that $gp can traverse.  Between
#         it and L3 sits the assignment table which grows towards $gp.
#
#   During a Major collection, the heap has the following form:
#
#      Header
#       |
#       |   Older generation objects
#       |    |
#       |    |                 Objects surviving last minor garbage collection
#       |    |                  |
#       |    |                  |         Major garbage collection area
#       |    |                  |          |
#       v    v                  v          v
#     +----+------------------+----------+------------------------------+
#     |XXXX| Old Area         | X        | New Area                     |
#     +----+------------------+----------+------------------------------+
#      ^    ^                  ^      ^   ^      ^                       ^
#      |    |                  |      |   |      |-->                    |
#      |    L0                 L1     |   L2    $gp                   L4, $s7
#      |                              |
#     heap_start                     breakpoint
#
#     $gp (allocation pointer): During a major collection, this points
#         into the next free word in the new area.
#
#     $s7 (limit pointer): During a major collection, the points to the
#         limit of heap memory.  $gp is not allowed to pass this value.
#         If the objects in the live old area cannot fit in the new area,
#         more memory is allocated and $s7 is adjusted accordingly.
#
#     breakpoint: Point where a major collection will occur.  It is
#         calculated by the following formula:
#
#         breakpoint = MIN(L3-MAX(MAJOR0,MAJOR1)-MAX(MINOR0,MINOR1),
#                          L3-(L3-L0)/2)
#
#         where (variables stored in the header):
#           MAJOR0 = total size of objects in the new area after last major
#                    collection.
#           MAJOR1 = (MAJOR0+MAJOR1)/2
#           MINOR0 = total size of objects in the reserve area after last
#                    minor collection.
#           MINOR1 = (MINOR0+MINOR1)/2
#
#   The following assumptions are made in the garbage collection
#   process:
#
#     1) Pointers on the Stack:
#        Every word on the stack that ends in 0 (i.e., is even) and is
#	 a valid address in the heap is assumed to point to an object
#        in the heap.  Even heap addresses on the stack that are actually
#	 something else (e.g., raw integers) will probably cause an
#        garbage collection error.
#
#     2) Object Layout:
#        Besides the Int, String, and Bool objects (which are handled
#        separately), the garbage collector assumes that each attribute
#        in an object is a pointer to another object.  It, however,
#        still does as much as possible to verify this before actually
#        updating any fields.
#
#     3) Pointer tests:
#        In order to be verified as an object, a pointer must undergo
#        certain tests:
#
#          a) The pointer must point within the correct storage area.
#          b) The word before the pointer (obj_eyecatch) must be the
#             word 0xFFFF FFFF
#          c) The word at the pointer must not be 0xFFFF FFFF (i.e.
#             -1 cannot be a class tag)
#
#        These tests are performed whenever any data could be a pointer
#        to keep any non-pointers from being updated accidentally.  The
#        functions "_GenGC_ChkCopy" and "_GenGC_OfsCopy" are responsible
#        for these checks.
#
#     4) The size stored in the object does not include the word required
#        to store the eyecatcher for the object in the heap.  This allows
#        the prototype objects to not require its own eyecatcher.  Also,
#        a size of 0 is invalid because it is used as a flag by the garbage
#        collector to indicate a forwarding pointer in the "obj_disp" field.
#
#     5) Roots are contained in the following areas: the stack, registers
#        specified in the REG mask, and the assignment table.
#

#
# Constants
#

#
# GenGC header offsets from "heap_start"
#

GenGC_HDRSIZE=44				# size of GenGC header
GenGC_HDRL0=0					# pointers to GenGC areas
GenGC_HDRL1=4
GenGC_HDRL2=8
GenGC_HDRL3=12
GenGC_HDRL4=16
GenGC_HDRMAJOR0=20				# history of major collections
GenGC_HDRMAJOR1=24
GenGC_HDRMINOR0=28				# history of minor collections
GenGC_HDRMINOR1=32
GenGC_HDRSTK=36					# start of stack
GenGC_HDRREG=40					# current REG mask

#
# Granularity of heap expansion
#
#   The heap is always expanded in multiples of 2^k, where
#   k is the granularity.
#

GenGC_HEAPEXPGRAN=14				# 2^14=16K

#
# Old to usable heap size ratio
#
#   After a major collection, the ratio of size of old area to the usable
#   size of the heap is at most 1/(2^k) where k is the value provided.
#

GenGC_OLDRATIO=2				# 1/(2^2)=.25=25%

#
# Mask to speficy which registers can be automatically updated
# when a garbage collection occurs.  The Automatic Register Update
# (ARU) mask has a bit set for all possible registers the
# garbage collector is able to handle.  The Register (REG) mask
# determines which register(s) are actually updated.
#
# BITS----------------------------
# 3 2         1         0
# 10987654321098765432109876543210
# --------------------------------
#
# 11000011011111110000000000000000  <-  Auto Register Update (ARU) mask
# +--++--++--++--++--++--++--++--+      $s0-$s6, $t8-$t9, $fp, $ra
#    C   3   7   F   0   0   0   0     ($16-$22, $24-$25, $30, $31)
#

GenGC_ARU_MASK=0xC37F0000

#
# Functions
#

#
# Initialization
#
#   Sets up the header information block for the garbage collector.
#   This block is located at the start of the heap ("heap_start")
#   and includes information needed by the garbage collector.  It
#   also calculates the barrier for the reserve and work areas and
#   sets the L2 pointer accordingly, rounding off in favor of the
#   reserve area.
#
#   INPUT:
#	$a0: start of stack
#	$a1: initial Register mask
#	$a2: end of heap
#	heap_start: start of the heap
#
#   OUTPUT:
#	$gp: lower bound of the work area
#	$s7: upper bound of the work area
#
#   Registers modified:
#	$t0, $t1, $v0, $a0
#

	.globl _GenGC_Init
_GenGC_Init:
	la	$t0 heap_start
	addiu	$t1 $t0 GenGC_HDRSIZE
	sw	$t1 GenGC_HDRL0($t0)		# save start of old area
	sw	$t1 GenGC_HDRL1($t0)		# save start of reserve area
	sub	$t1 $a2 $t1			# find reserve/work area barrier
	srl	$t1 $t1 1
	and	$t1 $t1 0xFFFFFFFC
	blez	$t1 _GenGC_Init_error		# heap initially to small
	sub	$gp $a2 $t1
	sw	$gp GenGC_HDRL2($t0)		# save start of work area	
	sw	$a2 GenGC_HDRL3($t0)		# save end of work area
	move	$s7 $a2				# set limit pointer
	sw	$0 GenGC_HDRMAJOR0($t0)		# clear histories
	sw	$0 GenGC_HDRMAJOR1($t0)
	sw	$0 GenGC_HDRMINOR0($t0)
	sw	$0 GenGC_HDRMINOR1($t0)
	sw	$a0 GenGC_HDRSTK($t0)		# save stack start
	sw	$a1 GenGC_HDRREG($t0)		# save register mask
	li	$v0 9				# get heap end
	move	$a0 $zero
	syscall					# sbrk
	sw	$v0 GenGC_HDRL4($t0)		# save heap limit
	jr	$ra				# return
_GenGC_Init_error:
	la	$a0 _GenGC_INITERROR		# show error message
	li	$v0 4
	syscall
	li	$v0 10				# exit
	syscall

#
# Record Assignment
#
#   Records an assignment in the assignment table.  Note that because
#   $s7 is always greater than $gp, an assignment can always be
#   recorded.
#
#   INPUT:
#	$a1: pointer to the pointer being modified
#	$s7: limit pointer of the work area
#	$gp: current allocation pointer
#	heap_start: start of heap
#
#   Registers modified:
#	$t0, $t1, $t2, $v0, $v1, $a0, $a1, $a2, $gp, $s7
#

	.globl _GenGC_Assign
_GenGC_Assign:
	addiu	$s7 $s7 -4
	sw	$a1 0($s7)			# save pointer to assignment
	bgt	$s7 $gp _GenGC_Assign_done
	addiu	$sp $sp -4
	sw	$ra 4($sp)			# save return address
	move	$a1 $0				# size
	addiu	$a0 $sp 4			# end of stack to collect
	jal	_GenGC_Collect
	lw	$ra 4($sp)			# restore return address
	addiu	$sp $sp 4
_GenGC_Assign_done:
	jr	$ra				# return

	.globl	_gc_check
_gc_check:
	beqz	$a1, _gc_ok			# void is ok
	lw	$a2 obj_eyecatch($a1)		# and check if it is valid
	addiu	$a2 $a2 1
	bnez	$a2 _gc_abort
_gc_ok:
	jr	$ra

_gc_abort:		 
	la      $a0 _gc_abort_msg
	li	$v0 4
	syscall                  # print gc message
	li   	$v0 10
        syscall			 # exit


#
# Generational Garbage Collection
#
#   This function implements the generational garbage collection.
#   It first calls the minor collector, "_GenGC_MinorC", and then
#   updates its history in the header.  The breakpoint is then
#   calculated.  If the breakpoint is reached or there is still not
#   enough room to allocate the requested size, a major garbage
#   collection then takes place by calling "_GenGC_MajorC".  After
#   the major collection, the size of the old area is analyzed.  If
#   it is greater than 1/(2^GenGC_OLDRATIO) of the total usable heap
#   size (L0 to L3), the heap is expanded.  Also, if there is still not
#   enough room to allocate the requested size, the heap is expanded
#   further to make sure that the specified amount of memory can be
#   allocated. If there is enough room in the unused area (L3 to L4),
#   this memory is used and the heap is not expanded.  The $s7 and $gp
#   pointers are then set as well as the L2 pointer.  If a major collection
#   is not done, the X area is incorporated into the old area
#   (i.e. the L2 pointer is moved into L1) and $s7, $gp, and L2 are
#   then set.
#
#   INPUT:
#	$a0: end of stack
#	$a1: size will need to allocate in bytes
#	$s7: limit pointer of thw work area
#	$gp: current allocation pointer
#	heap_start: start of heap
#
#   OUTPUT:
#	$a1: size will need to allocate in bytes (unchanged)
#
#   Registers modified:
#	$t0, $t1, $t2, $t3, $t4, $v0, $v1, $a0, $a2, $gp, $s7
#

	.globl _GenGC_Collect
_GenGC_Collect:
	addiu	$sp $sp -12
	sw	$ra 12($sp)			# save return address
	sw	$a0 8($sp)			# save stack end
	sw	$a1 4($sp)			# save size
	la	$a0 _GenGC_COLLECT		# print collection message
	li	$v0 4
	syscall
	lw	$a0 8($sp)			# restore stack end
	jal	_GenGC_MinorC			# minor collection
	la	$a1 heap_start
	lw	$t1 GenGC_HDRMINOR1($a1)
	addu	$t1 $t1 $a0
	srl	$t1 $t1 1
	sw	$t1 GenGC_HDRMINOR1($a1)	# update histories
	sw	$a0 GenGC_HDRMINOR0($a1)
	move	$t0 $t1				# set $t0 to max of minor
	bgt	$t1 $a0 _GenGC_Collect_maxmaj
	move	$t0 $a0
_GenGC_Collect_maxmaj:
	lw	$t1 GenGC_HDRMAJOR0($a1)	# set $t1 to max of major
	lw	$t2 GenGC_HDRMAJOR1($a1)
	bgt	$t1 $t2 _GenGC_Collect_maxdef
	move	$t1 $t2
_GenGC_Collect_maxdef:
	lw	$t2 GenGC_HDRL3($a1)
	sub	$t0 $t2 $t0			# set $t0 to L3-$t0-$t1
	sub	$t0 $t0 $t1
	lw	$t1 GenGC_HDRL0($a1)		# set $t1 to L3-(L3-L0)/2
	sub	$t1 $t2 $t1
	srl	$t1 $t1 1
	sub	$t1 $t2 $t1
	blt	$t0 $t1 _GenGC_Collect_breakpt	# set $t0 to minimum of above
	move	$t0 $t1
_GenGC_Collect_breakpt:
	lw	$t1 GenGC_HDRL1($a1)		# get end of old area
	bge	$t1 $t0 _GenGC_Collect_major
	lw	$t0 GenGC_HDRL2($a1)
	lw	$t1 GenGC_HDRL3($a1)
	lw	$t2 4($sp)			# load requested size into $t2
	sub	$t0 $t1 $t0			# find reserve/work area barrier
	srl	$t0 $t0 1
	and	$t0 $t0 0xFFFFFFFC
	sub	$t0 $t1 $t0			# reserve/work barrier
	addu	$t2 $t0 $t2			# test allocation
	bge	$t2 $t1 _GenGC_Collect_major	# check if work area too small
_GenGC_Collect_nomajor:
	lw	$t1 GenGC_HDRL2($a1)
	sw	$t1 GenGC_HDRL1($a1)		# expand old area
	sw	$t0 GenGC_HDRL2($a1)		# set new reserve/work barrier
	move	$gp $t0				# set $gp
	lw	$s7 GenGC_HDRL3($a1)		# load limit into $s7
	b	_GenGC_Collect_done
_GenGC_Collect_major:
	la	$a0 _GenGC_Major		# print collection message
	li	$v0 4
	syscall
	lw	$a0 8($sp)			# restore stack end
	jal	_GenGC_MajorC			# major collection
	la	$a1 heap_start
	lw	$t1 GenGC_HDRMAJOR1($a1)
	addu	$t1 $t1 $a0
	srl	$t1 $t1 1
	sw	$t1 GenGC_HDRMAJOR1($a1)	# update histories
	sw	$a0 GenGC_HDRMAJOR0($a1)
	lw	$t1 GenGC_HDRL3($a1)		# find ratio of the old area
	lw	$t0 GenGC_HDRL0($a1)
	sub	$t1 $t1 $t0
	srl	$t1 $t1 GenGC_OLDRATIO
	addu	$t1 $t0 $t1
	lw	$t0 GenGC_HDRL1($a1)
	sub	$t0 $t0 $t1
	sll	$t0 $t0 GenGC_OLDRATIO		# amount to expand in $t0
	lw	$t1 GenGC_HDRL3($a1)		# load L3
	lw	$t2 GenGC_HDRL1($a1)		# load L1
	sub	$t2 $t1 $t2
	srl	$t2 $t2 1
	and	$t2 $t2 0xFFFFFFFC
	sub	$t1 $t1 $t2			# reserve/work barrier
	lw	$t2 4($sp)			# restore size
	addu	$t1 $t1 $t2
	lw	$t2 GenGC_HDRL3($a1)		# load L3
	sub	$t1 $t1 $t2			# test allocation
	addiu	$t1 $t1 4			# adjust for round off errors
	sll	$t1 $t1 1			# need to allocate $t1 memory
	blt	$t1 $t0 _GenGC_Collect_enough	# put max of $t0, $t1 in $t0
	move	$t0 $t1
_GenGC_Collect_enough:
	blez	$t0 _GenGC_Collect_setL2	# no need to expand
	addiu	$t1 $0 1			# put 1 in $t1
	sll	$t1 $t1 GenGC_HEAPEXPGRAN	# get granularity of expansion
	addiu	$t1 $t1 -1			# align to granularity
	addu	$t0 $t0 $t1
	nor	$t1 $t1 $t1
	and	$t0 $t0 $t1			# total memory needed
	lw	$t1 GenGC_HDRL3($a1)		# load L3
	lw	$t2 GenGC_HDRL4($a1)		# load L4
	sub	$t1 $t2 $t1
	sub	$t2 $t0 $t1			# actual amount to allocate
	bgtz	$t2 _GenGC_Collect_getmem	# check if really need to allocate
_GenGC_Collect_xfermem:
	lw	$s7 GenGC_HDRL3($a1)		# load L3
	addu	$s7 $s7 $t0			# expand by $t0, set $s7
	sw	$s7 GenGC_HDRL3($a1)		# save L3
	b	_GenGC_Collect_findL2
_GenGC_Collect_getmem:
	li	$v0 9				# sbrk
	move	$a0 $t2				# set the size to expand the heap
	syscall
	li	$v0 9
	move	$a0 $zero
	syscall					# get new end of heap in $v0
	sw	$v0 GenGC_HDRL4($a1)		# save L4
	sw	$v0 GenGC_HDRL3($a1)		# save L3
	move	$s7 $v0				# set $s7
	b	_GenGC_Collect_findL2
_GenGC_Collect_setL2:
	lw	$s7 GenGC_HDRL3($a1)		# load L3
_GenGC_Collect_findL2:
	lw	$t1 GenGC_HDRL1($a1)		# load L1
	sub	$t1 $s7 $t1
	srl	$t1 $t1 1
	and	$t1 $t1 0xFFFFFFFC
	sub	$gp $s7 $t1			# reserve/work barrier
	sw	$gp GenGC_HDRL2($a1)		# save L2
_GenGC_Collect_done:

# Clear new generation to catch missing pointers
	move	$t0 $gp
_GenGC_Clear_loop:
	sw	$zero 0($t0)
	addiu	$t0 $t0 4
	blt	$t0 $s7 _GenGC_Clear_loop

	lw	$a1 4($sp)			# restore size
	lw	$ra 12($sp)			# restore return address
	addiu	$sp $sp 12
	jr	$ra				# return

#
# Check and Copy an Object
#
#   Checks that the input pointer points to an object is a heap
#   object.  If so, it then checks for a forwarding pointer by
#   checking for an object size of 0.  If found, the forwarding
#   pointer is returned.  If not found, the object is copied to $gp
#   and a pointer to it is returned.  The following tests are done to
#   determine if the object is a heap object:
#
#     1) The pointer is within the specified limits
#     2) The pointer is even
#     3) The word before the pointer is the eye catcher 0xFFFF FFFF
#     4) The word at the pointer is a valid tag (i.e. not equal to
#        0xFFFF FFFF)
#
#   INPUT:
#	$a0: pointer to check and copy
#	$a1: lower bound object should be within.
#	$a2: upper bound object should be within.
#	$gp: current allocation pointer
#
#   OUTPUT:
#	$a0: if input points to a heap object then it is set to the
#            new location of object.  If not, it is unchanged.
#	$a1: lower bound object should be within. (unchanged)
#	$a2: upper bound object should be within. (unchanged)
#
#   Registers modified:
#	$t0, $t1, $t2, $v0, $a0, $gp
#

	.globl _GenGC_ChkCopy
_GenGC_ChkCopy:
	blt	$a0 $a1 _GenGC_ChkCopy_done	# check bounds
	bge	$a0 $a2 _GenGC_ChkCopy_done
	andi	$t2 $a0 1			# check if odd
	bnez	$t2 _GenGC_ChkCopy_done
	addiu	$t2 $0 -1
	lw	$t1 obj_eyecatch($a0)		# check eyecatcher
	bne	$t2 $t1 _gc_abort
	lw	$t1 obj_tag($a0)		# check object tag
	beq	$t2 $t1 _GenGC_ChkCopy_done
	lw	$t1 obj_size($a0)		# get size of object
	beqz	$t1 _GenGC_ChkCopy_forward	# if size = 0, get forwarding pointer
	move	$t0 $a0				# save pointer to old object in $t0
	addiu	$gp $gp 4			# allocate memory for eyecatcher
	move	$a0 $gp				# get address of new object
	sw	$t2 obj_eyecatch($a0)		# save eye catcher
	sll	$t1 $t1 2			# convert words to bytes
	addu	$t1 $t0 $t1			# set $t1 to limit of copy
	move	$t2 $t0				# set $t2 to old object
_GenGC_ChkCopy_loop:
	lw	$v0 0($t0)			# copy
	sw	$v0 0($gp)
	addiu	$t0 $t0 4			# update each index
	addiu	$gp $gp 4
	bne	$t0 $t1 _GenGC_ChkCopy_loop	# check for limit of copy
	sw	$0 obj_size($t2)		# set size to 0
	sw	$a0 obj_disp($t2)		# save forwarding pointer
_GenGC_ChkCopy_done:
	jr	$ra				# return
_GenGC_ChkCopy_forward:
	lw	$a0 obj_disp($a0)		# get forwarding pointer
	jr	$ra				# return


#
# Minor Garbage Collection
#
#   This garbage collector is run when ever the space in the work
#   area is used up by objects and the assignment table.  The live
#   objects are found and copied to the reserve area.  The L2 pointer
#   is then set to the end of the live objects.  The collector consists
#   of six phases:
#
#     1) Set $gp into the reserve area and set the inputs for ChkCopy
#
#     2) Scan the stack for root pointers into the heap.  The beginning
#        of the stack is in the header and the end is an input to this
#        function.  Look for the appropriate stack flags and act
#        accordingly.  Use "_GenGC_ChkCopy" to validate the pointer and
#        get the new pointer, and then update the stack entry.
#
#     3) Check the registers specified in the Register (REG) mask to
#        automatically update.  This mask is stored in the header.  If
#        bit #n in the mask is set, register #n will be passed to
#        "_GenGC_ChkCopy" and updated with its result.  "_GenGC_SetRegMask"
#        can be used to update this mask.
#
#     4) The assignemnt table is now checked.  $s7 is moved from its
#        current position until it hits the L3 pointer.  Each entry is a
#        pointer to the pointer that must be checked.  Again,
#        "_GenGC_ChkCopy" is used and the pointer updated.
#
#     5) At this point, all root objects are in the reserve area.  This
#        area is now traversed object by object (from L1 to $gp).  It
#        results in a breadth first search of the live objects collected.
#        All attributes of objects are treated as pointers except the
#        "Int", "Bool", and "String" objects.  The first two are skipped
#        completely, and the first attribute of the string object is
#        analyzed (should be a pointer to an "Int" object).
#
#     6) At this point, L2 is set to the end of the live objects in the
#        reserve area.  This is in preparation for a major collection.
#        The size of all the live objects collected is then computed and
#        returned.
#
#   INPUT:
#	$a0: end of stack
#	$s7: limit pointer of this area of storage
#	$gp: current allocation pointer
#	heap_start: start of heap
#
#   OUTPUT:
#	$a0: size of all live objects collected
#
#   Registers modified:
#	$t0, $t1, $t2, $t3, $t4, $v0, $v1, $a0, $a1, $a2, $gp, $s7
#

	.globl _GenGC_MinorC
_GenGC_MinorC:
	addiu	$sp $sp -20
	sw	$ra 20($sp)			# save return address
	la	$t0 heap_start
	lw	$a1 GenGC_HDRL2($t0)		# set lower bound to work area
	move	$a2 $s7				# set upper bound for ChkCopy
	lw	$gp GenGC_HDRL1($t0)		# set $gp into reserve area
	sw	$a0 16($sp)			# save stack end
	lw	$t0 GenGC_HDRSTK($t0)		# set $t0 to stack start
	move	$t1 $a0				# set $t1 to stack end
	ble	$t0 $t1 _GenGC_MinorC_stackend	# check for empty stack
_GenGC_MinorC_stackloop: 			# $t1 stack end, $t0 index
	addiu	$t0 $t0 -4			# update index
	sw	$t0 12($sp)			# save stack index
	lw	$a0 4($t0)			# get stack item
	jal	_GenGC_ChkCopy			# check and copy
	lw	$t0 12($sp)			# load stack index
	sw	$a0 4($t0)
	lw	$t1 16($sp)			# restore stack end
	bgt	$t0 $t1 _GenGC_MinorC_stackloop	# loop
_GenGC_MinorC_stackend:
	la	$t0 heap_start
	lw	$t0 GenGC_HDRREG($t0)		# get Register mask
	sw	$t0 16($sp)			# save Register mask
_GenGC_MinorC_reg16:
	srl	$t0 $t0 16			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg17	# check if set
	move	$a0 $16				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$16 $a0				# update register
_GenGC_MinorC_reg17:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 17			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg18	# check if set
	move	$a0 $17				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$17 $a0				# update register
_GenGC_MinorC_reg18:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 18			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg19	# check if set
	move	$a0 $18				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$18 $a0				# update register
_GenGC_MinorC_reg19:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 19			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg20	# check if set
	move	$a0 $19				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$19 $a0				# update register
_GenGC_MinorC_reg20:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 20			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg21	# check if set
	move	$a0 $20				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$20 $a0				# update register
_GenGC_MinorC_reg21:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 21			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg22	# check if set
	move	$a0 $21				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$21 $a0				# update register
_GenGC_MinorC_reg22:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 22			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg24	# check if set
	move	$a0 $22				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$22 $a0				# update register
_GenGC_MinorC_reg24:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 24			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg25	# check if set
	move	$a0 $24				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$24 $a0				# update register
_GenGC_MinorC_reg25:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 25			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg30	# check if set
	move	$a0 $25				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$25 $a0				# update register
_GenGC_MinorC_reg30:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 30			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_reg31	# check if set
	move	$a0 $30				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$30 $a0				# update register
_GenGC_MinorC_reg31:
	lw	$t0 16($sp)			# restore mask
	srl	$t0 $t0 31			# shift to proper bit
	andi	$t1 $t0 1
	beq	$t1 $0 _GenGC_MinorC_regend	# check if set
	move	$a0 $31				# set test pointer
	jal	_GenGC_ChkCopy			# check and copy
	move	$31 $a0				# update register
_GenGC_MinorC_regend:
	la	$t0 heap_start
	lw	$t3 GenGC_HDRL0($t0)		# lower limit of old area
	lw	$t4 GenGC_HDRL1($t0)		# upper limit of old area
	lw	$t0 GenGC_HDRL3($t0)		# get L3
	sw	$t0 16($sp)			# save index limit
	bge	$s7 $t0 _GenGC_MinorC_assnend	# check for no assignments
_GenGC_MinorC_assnloop:				# $s7 index, $t0 limit
	lw	$a0 0($s7)			# get table entry
	blt	$a0 $t3 _GenGC_MinorC_assnnext	# must point into old area
	bge	$a0 $t4 _GenGC_MinorC_assnnext
	lw	$a0 0($a0)			# get pointer to check
	jal	_GenGC_ChkCopy			# check and copy
	lw	$t0 0($s7)
	sw	$a0 0($t0)			# update pointer
	lw	$t0 16($sp)			# restore index limit
_GenGC_MinorC_assnnext:
	addiu	$s7 $s7 4			# update index
	blt	$s7 $t0 _GenGC_MinorC_assnloop	# loop
_GenGC_MinorC_assnend:
	la	$t0 heap_start
	lw	$t0 GenGC_HDRL1($t0)		# start of reserve area
	bge	$t0 $gp _GenGC_MinorC_heapend	# check for no objects
_GenGC_MinorC_heaploop:				# $t0: index, $gp: limit
	addiu	$t0 $t0 4			# skip over eyecatcher
	addiu	$t1 $0 -1			# check for eyecatcher
	lw	$t2 obj_eyecatch($t0)
	bne	$t1 $t2 _GenGC_MinorC_error	# eyecatcher not found
	lw	$a0 obj_size($t0)		# get object size
	sll	$a0 $a0 2			# words to bytes
	lw	$t1 obj_tag($t0)		# get the object's tag
	lw	$t2 _int_tag			# test for int object
	beq	$t1 $t2 _GenGC_MinorC_int
	lw	$t2 _bool_tag			# test for bool object
	beq	$t1 $t2 _GenGC_MinorC_bool
	lw	$t2 _string_tag			# test for string object
	beq	$t1 $t2 _GenGC_MinorC_string
_GenGC_MinorC_other:
	addi	$t1 $t0 obj_attr		# start at first attribute
	add	$t2 $t0 $a0			# limit of attributes
	bge	$t1 $t2 _GenGC_MinorC_nextobj	# check for no attributes
	sw	$t0 16($sp)			# save pointer to object
	sw	$a0 12($sp)			# save object size
	sw	$t2 4($sp)			# save limit
_GenGC_MinorC_objloop:				# $t1: index, $t2: limit
	sw	$t1 8($sp)			# save index
	lw	$a0 0($t1)			# set pointer to check
	jal	_GenGC_ChkCopy
"""
