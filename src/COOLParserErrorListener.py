import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

class COOLParserErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        msg = offendingSymbol.text
        if msg == "<EOF>":
            msg = "EOF"
        else:
            msg = "\"" + msg + "\""
        print("(" + str(line) + ", " + str(column+1) + ") - SyntacticError: ERROR at or near " +msg, file=sys.stdout)