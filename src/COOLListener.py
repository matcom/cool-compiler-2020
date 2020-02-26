# Generated from C:\Software\ANTLR\cool\COOL.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .COOLParser import COOLParser
else:
    from COOLParser import COOLParser

# This class defines a complete listener for a parse tree produced by COOLParser.
class COOLListener(ParseTreeListener):

    # Enter a parse tree produced by COOLParser#program.
    def enterProgram(self, ctx:COOLParser.ProgramContext):
        pass

    # Exit a parse tree produced by COOLParser#program.
    def exitProgram(self, ctx:COOLParser.ProgramContext):
        pass


    # Enter a parse tree produced by COOLParser#classes.
    def enterClasses(self, ctx:COOLParser.ClassesContext):
        pass

    # Exit a parse tree produced by COOLParser#classes.
    def exitClasses(self, ctx:COOLParser.ClassesContext):
        pass


    # Enter a parse tree produced by COOLParser#eof.
    def enterEof(self, ctx:COOLParser.EofContext):
        pass

    # Exit a parse tree produced by COOLParser#eof.
    def exitEof(self, ctx:COOLParser.EofContext):
        pass


    # Enter a parse tree produced by COOLParser#classDefine.
    def enterClassDefine(self, ctx:COOLParser.ClassDefineContext):
        pass

    # Exit a parse tree produced by COOLParser#classDefine.
    def exitClassDefine(self, ctx:COOLParser.ClassDefineContext):
        pass


    # Enter a parse tree produced by COOLParser#method.
    def enterMethod(self, ctx:COOLParser.MethodContext):
        pass

    # Exit a parse tree produced by COOLParser#method.
    def exitMethod(self, ctx:COOLParser.MethodContext):
        pass


    # Enter a parse tree produced by COOLParser#property.
    def enterProperty(self, ctx:COOLParser.PropertyContext):
        pass

    # Exit a parse tree produced by COOLParser#property.
    def exitProperty(self, ctx:COOLParser.PropertyContext):
        pass


    # Enter a parse tree produced by COOLParser#formal.
    def enterFormal(self, ctx:COOLParser.FormalContext):
        pass

    # Exit a parse tree produced by COOLParser#formal.
    def exitFormal(self, ctx:COOLParser.FormalContext):
        pass


    # Enter a parse tree produced by COOLParser#letIn.
    def enterLetIn(self, ctx:COOLParser.LetInContext):
        pass

    # Exit a parse tree produced by COOLParser#letIn.
    def exitLetIn(self, ctx:COOLParser.LetInContext):
        pass


    # Enter a parse tree produced by COOLParser#minus.
    def enterMinus(self, ctx:COOLParser.MinusContext):
        pass

    # Exit a parse tree produced by COOLParser#minus.
    def exitMinus(self, ctx:COOLParser.MinusContext):
        pass


    # Enter a parse tree produced by COOLParser#string.
    def enterString(self, ctx:COOLParser.StringContext):
        pass

    # Exit a parse tree produced by COOLParser#string.
    def exitString(self, ctx:COOLParser.StringContext):
        pass


    # Enter a parse tree produced by COOLParser#isvoid.
    def enterIsvoid(self, ctx:COOLParser.IsvoidContext):
        pass

    # Exit a parse tree produced by COOLParser#isvoid.
    def exitIsvoid(self, ctx:COOLParser.IsvoidContext):
        pass


    # Enter a parse tree produced by COOLParser#while.
    def enterWhile(self, ctx:COOLParser.WhileContext):
        pass

    # Exit a parse tree produced by COOLParser#while.
    def exitWhile(self, ctx:COOLParser.WhileContext):
        pass


    # Enter a parse tree produced by COOLParser#division.
    def enterDivision(self, ctx:COOLParser.DivisionContext):
        pass

    # Exit a parse tree produced by COOLParser#division.
    def exitDivision(self, ctx:COOLParser.DivisionContext):
        pass


    # Enter a parse tree produced by COOLParser#negative.
    def enterNegative(self, ctx:COOLParser.NegativeContext):
        pass

    # Exit a parse tree produced by COOLParser#negative.
    def exitNegative(self, ctx:COOLParser.NegativeContext):
        pass


    # Enter a parse tree produced by COOLParser#boolNot.
    def enterBoolNot(self, ctx:COOLParser.BoolNotContext):
        pass

    # Exit a parse tree produced by COOLParser#boolNot.
    def exitBoolNot(self, ctx:COOLParser.BoolNotContext):
        pass


    # Enter a parse tree produced by COOLParser#lessThan.
    def enterLessThan(self, ctx:COOLParser.LessThanContext):
        pass

    # Exit a parse tree produced by COOLParser#lessThan.
    def exitLessThan(self, ctx:COOLParser.LessThanContext):
        pass


    # Enter a parse tree produced by COOLParser#block.
    def enterBlock(self, ctx:COOLParser.BlockContext):
        pass

    # Exit a parse tree produced by COOLParser#block.
    def exitBlock(self, ctx:COOLParser.BlockContext):
        pass


    # Enter a parse tree produced by COOLParser#id.
    def enterId(self, ctx:COOLParser.IdContext):
        pass

    # Exit a parse tree produced by COOLParser#id.
    def exitId(self, ctx:COOLParser.IdContext):
        pass


    # Enter a parse tree produced by COOLParser#multiply.
    def enterMultiply(self, ctx:COOLParser.MultiplyContext):
        pass

    # Exit a parse tree produced by COOLParser#multiply.
    def exitMultiply(self, ctx:COOLParser.MultiplyContext):
        pass


    # Enter a parse tree produced by COOLParser#if.
    def enterIf(self, ctx:COOLParser.IfContext):
        pass

    # Exit a parse tree produced by COOLParser#if.
    def exitIf(self, ctx:COOLParser.IfContext):
        pass


    # Enter a parse tree produced by COOLParser#case.
    def enterCase(self, ctx:COOLParser.CaseContext):
        pass

    # Exit a parse tree produced by COOLParser#case.
    def exitCase(self, ctx:COOLParser.CaseContext):
        pass


    # Enter a parse tree produced by COOLParser#ownMethodCall.
    def enterOwnMethodCall(self, ctx:COOLParser.OwnMethodCallContext):
        pass

    # Exit a parse tree produced by COOLParser#ownMethodCall.
    def exitOwnMethodCall(self, ctx:COOLParser.OwnMethodCallContext):
        pass


    # Enter a parse tree produced by COOLParser#add.
    def enterAdd(self, ctx:COOLParser.AddContext):
        pass

    # Exit a parse tree produced by COOLParser#add.
    def exitAdd(self, ctx:COOLParser.AddContext):
        pass


    # Enter a parse tree produced by COOLParser#new.
    def enterNew(self, ctx:COOLParser.NewContext):
        pass

    # Exit a parse tree produced by COOLParser#new.
    def exitNew(self, ctx:COOLParser.NewContext):
        pass


    # Enter a parse tree produced by COOLParser#parentheses.
    def enterParentheses(self, ctx:COOLParser.ParenthesesContext):
        pass

    # Exit a parse tree produced by COOLParser#parentheses.
    def exitParentheses(self, ctx:COOLParser.ParenthesesContext):
        pass


    # Enter a parse tree produced by COOLParser#assignment.
    def enterAssignment(self, ctx:COOLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by COOLParser#assignment.
    def exitAssignment(self, ctx:COOLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by COOLParser#false.
    def enterFalse(self, ctx:COOLParser.FalseContext):
        pass

    # Exit a parse tree produced by COOLParser#false.
    def exitFalse(self, ctx:COOLParser.FalseContext):
        pass


    # Enter a parse tree produced by COOLParser#int.
    def enterInt(self, ctx:COOLParser.IntContext):
        pass

    # Exit a parse tree produced by COOLParser#int.
    def exitInt(self, ctx:COOLParser.IntContext):
        pass


    # Enter a parse tree produced by COOLParser#equal.
    def enterEqual(self, ctx:COOLParser.EqualContext):
        pass

    # Exit a parse tree produced by COOLParser#equal.
    def exitEqual(self, ctx:COOLParser.EqualContext):
        pass


    # Enter a parse tree produced by COOLParser#true.
    def enterTrue(self, ctx:COOLParser.TrueContext):
        pass

    # Exit a parse tree produced by COOLParser#true.
    def exitTrue(self, ctx:COOLParser.TrueContext):
        pass


    # Enter a parse tree produced by COOLParser#lessEqual.
    def enterLessEqual(self, ctx:COOLParser.LessEqualContext):
        pass

    # Exit a parse tree produced by COOLParser#lessEqual.
    def exitLessEqual(self, ctx:COOLParser.LessEqualContext):
        pass


    # Enter a parse tree produced by COOLParser#methodCall.
    def enterMethodCall(self, ctx:COOLParser.MethodCallContext):
        pass

    # Exit a parse tree produced by COOLParser#methodCall.
    def exitMethodCall(self, ctx:COOLParser.MethodCallContext):
        pass


