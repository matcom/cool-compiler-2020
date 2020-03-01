import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

class COOLLexerErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("(" + str(line) + ", " + str(column+1) + ") - LexicographicError: " + msg, file=sys.stdout)