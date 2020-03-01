import sys
from io import StringIO
from typing.io import TextIO
from antlr4 import *
from COOL_LEX import COOL_LEX
from antlr4.CommonTokenFactory import CommonTokenFactory
from antlr4.atn.LexerATNSimulator import LexerATNSimulator
from antlr4.InputStream import InputStream
from antlr4.Recognizer import Recognizer
from antlr4.Token import Token
from antlr4.error.Errors import IllegalStateException, LexerNoViableAltException, RecognitionException

class COOLLexer(COOL_LEX):
    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self._hasErrors = False

    def notifyListeners(self, e:LexerNoViableAltException):
        self._hasErrors = True

        start = self._tokenStartCharIndex
        stop = self._input.index
        text = self._input.getText(start, stop)
        msg = "'" + self.getErrorDisplay(text) + "'"
        listener = self.getErrorListenerDispatch()
        listener.syntaxError(self, self._token, self._tokenStartLine, self._tokenStartColumn, msg, e)

    def reset(self):
        super().reset()
        self._hasErrors = False

    @property
    def hasErrors(self):
        return self._hasErrors