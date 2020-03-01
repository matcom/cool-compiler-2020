import sys
from io import StringIO
from typing.io import TextIO
from antlr4 import *
from COOL import COOL
from antlr4.CommonTokenFactory import CommonTokenFactory
from antlr4.atn.LexerATNSimulator import LexerATNSimulator
from antlr4.InputStream import InputStream
from antlr4.Recognizer import Recognizer
from antlr4.Token import Token
from antlr4.error.Errors import IllegalStateException, LexerNoViableAltException, RecognitionException

class COOLParser(COOL):
    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)

    def notifyErrorListeners(self, msg:str, offendingToken:Token = None, e:RecognitionException = None):
        if offendingToken is None:
            offendingToken = self.getCurrentToken()
        self._syntaxErrors += 1
        line = offendingToken.line
        column = offendingToken.column
        listener = self.getErrorListenerDispatch()
        listener.syntaxError(self, offendingToken, line, column, msg, e)