# Generated from COOL.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .COOL import COOL
else:
    from COOL import COOL

# This class defines a complete listener for a parse tree produced by COOL.
class COOLListener(ParseTreeListener):

    # Enter a parse tree produced by COOL#program.
    def enterProgram(self, ctx:COOL.ProgramContext):
        pass

    # Exit a parse tree produced by COOL#program.
    def exitProgram(self, ctx:COOL.ProgramContext):
        pass


    # Enter a parse tree produced by COOL#classes.
    def enterClasses(self, ctx:COOL.ClassesContext):
        pass

    # Exit a parse tree produced by COOL#classes.
    def exitClasses(self, ctx:COOL.ClassesContext):
        pass


    # Enter a parse tree produced by COOL#classDefine.
    def enterClassDefine(self, ctx:COOL.ClassDefineContext):
        pass

    # Exit a parse tree produced by COOL#classDefine.
    def exitClassDefine(self, ctx:COOL.ClassDefineContext):
        pass


    # Enter a parse tree produced by COOL#method.
    def enterMethod(self, ctx:COOL.MethodContext):
        pass

    # Exit a parse tree produced by COOL#method.
    def exitMethod(self, ctx:COOL.MethodContext):
        pass


    # Enter a parse tree produced by COOL#property.
    def enterProperty(self, ctx:COOL.PropertyContext):
        pass

    # Exit a parse tree produced by COOL#property.
    def exitProperty(self, ctx:COOL.PropertyContext):
        pass


    # Enter a parse tree produced by COOL#formal.
    def enterFormal(self, ctx:COOL.FormalContext):
        pass

    # Exit a parse tree produced by COOL#formal.
    def exitFormal(self, ctx:COOL.FormalContext):
        pass


    # Enter a parse tree produced by COOL#letIn.
    def enterLetIn(self, ctx:COOL.LetInContext):
        pass

    # Exit a parse tree produced by COOL#letIn.
    def exitLetIn(self, ctx:COOL.LetInContext):
        pass


    # Enter a parse tree produced by COOL#minus.
    def enterMinus(self, ctx:COOL.MinusContext):
        pass

    # Exit a parse tree produced by COOL#minus.
    def exitMinus(self, ctx:COOL.MinusContext):
        pass


    # Enter a parse tree produced by COOL#string.
    def enterString(self, ctx:COOL.StringContext):
        pass

    # Exit a parse tree produced by COOL#string.
    def exitString(self, ctx:COOL.StringContext):
        pass


    # Enter a parse tree produced by COOL#isvoid.
    def enterIsvoid(self, ctx:COOL.IsvoidContext):
        pass

    # Exit a parse tree produced by COOL#isvoid.
    def exitIsvoid(self, ctx:COOL.IsvoidContext):
        pass


    # Enter a parse tree produced by COOL#while.
    def enterWhile(self, ctx:COOL.WhileContext):
        pass

    # Exit a parse tree produced by COOL#while.
    def exitWhile(self, ctx:COOL.WhileContext):
        pass


    # Enter a parse tree produced by COOL#division.
    def enterDivision(self, ctx:COOL.DivisionContext):
        pass

    # Exit a parse tree produced by COOL#division.
    def exitDivision(self, ctx:COOL.DivisionContext):
        pass


    # Enter a parse tree produced by COOL#negative.
    def enterNegative(self, ctx:COOL.NegativeContext):
        pass

    # Exit a parse tree produced by COOL#negative.
    def exitNegative(self, ctx:COOL.NegativeContext):
        pass


    # Enter a parse tree produced by COOL#boolNot.
    def enterBoolNot(self, ctx:COOL.BoolNotContext):
        pass

    # Exit a parse tree produced by COOL#boolNot.
    def exitBoolNot(self, ctx:COOL.BoolNotContext):
        pass


    # Enter a parse tree produced by COOL#lessThan.
    def enterLessThan(self, ctx:COOL.LessThanContext):
        pass

    # Exit a parse tree produced by COOL#lessThan.
    def exitLessThan(self, ctx:COOL.LessThanContext):
        pass


    # Enter a parse tree produced by COOL#block.
    def enterBlock(self, ctx:COOL.BlockContext):
        pass

    # Exit a parse tree produced by COOL#block.
    def exitBlock(self, ctx:COOL.BlockContext):
        pass


    # Enter a parse tree produced by COOL#id.
    def enterId(self, ctx:COOL.IdContext):
        pass

    # Exit a parse tree produced by COOL#id.
    def exitId(self, ctx:COOL.IdContext):
        pass


    # Enter a parse tree produced by COOL#multiply.
    def enterMultiply(self, ctx:COOL.MultiplyContext):
        pass

    # Exit a parse tree produced by COOL#multiply.
    def exitMultiply(self, ctx:COOL.MultiplyContext):
        pass


    # Enter a parse tree produced by COOL#if.
    def enterIf(self, ctx:COOL.IfContext):
        pass

    # Exit a parse tree produced by COOL#if.
    def exitIf(self, ctx:COOL.IfContext):
        pass


    # Enter a parse tree produced by COOL#case.
    def enterCase(self, ctx:COOL.CaseContext):
        pass

    # Exit a parse tree produced by COOL#case.
    def exitCase(self, ctx:COOL.CaseContext):
        pass


    # Enter a parse tree produced by COOL#ownMethodCall.
    def enterOwnMethodCall(self, ctx:COOL.OwnMethodCallContext):
        pass

    # Exit a parse tree produced by COOL#ownMethodCall.
    def exitOwnMethodCall(self, ctx:COOL.OwnMethodCallContext):
        pass


    # Enter a parse tree produced by COOL#add.
    def enterAdd(self, ctx:COOL.AddContext):
        pass

    # Exit a parse tree produced by COOL#add.
    def exitAdd(self, ctx:COOL.AddContext):
        pass


    # Enter a parse tree produced by COOL#new.
    def enterNew(self, ctx:COOL.NewContext):
        pass

    # Exit a parse tree produced by COOL#new.
    def exitNew(self, ctx:COOL.NewContext):
        pass


    # Enter a parse tree produced by COOL#parentheses.
    def enterParentheses(self, ctx:COOL.ParenthesesContext):
        pass

    # Exit a parse tree produced by COOL#parentheses.
    def exitParentheses(self, ctx:COOL.ParenthesesContext):
        pass


    # Enter a parse tree produced by COOL#assignment.
    def enterAssignment(self, ctx:COOL.AssignmentContext):
        pass

    # Exit a parse tree produced by COOL#assignment.
    def exitAssignment(self, ctx:COOL.AssignmentContext):
        pass


    # Enter a parse tree produced by COOL#false.
    def enterFalse(self, ctx:COOL.FalseContext):
        pass

    # Exit a parse tree produced by COOL#false.
    def exitFalse(self, ctx:COOL.FalseContext):
        pass


    # Enter a parse tree produced by COOL#int.
    def enterInt(self, ctx:COOL.IntContext):
        pass

    # Exit a parse tree produced by COOL#int.
    def exitInt(self, ctx:COOL.IntContext):
        pass


    # Enter a parse tree produced by COOL#equal.
    def enterEqual(self, ctx:COOL.EqualContext):
        pass

    # Exit a parse tree produced by COOL#equal.
    def exitEqual(self, ctx:COOL.EqualContext):
        pass


    # Enter a parse tree produced by COOL#true.
    def enterTrue(self, ctx:COOL.TrueContext):
        pass

    # Exit a parse tree produced by COOL#true.
    def exitTrue(self, ctx:COOL.TrueContext):
        pass


    # Enter a parse tree produced by COOL#lessEqual.
    def enterLessEqual(self, ctx:COOL.LessEqualContext):
        pass

    # Exit a parse tree produced by COOL#lessEqual.
    def exitLessEqual(self, ctx:COOL.LessEqualContext):
        pass


    # Enter a parse tree produced by COOL#methodCall.
    def enterMethodCall(self, ctx:COOL.MethodCallContext):
        pass

    # Exit a parse tree produced by COOL#methodCall.
    def exitMethodCall(self, ctx:COOL.MethodCallContext):
        pass


