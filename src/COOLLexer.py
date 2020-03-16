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
        self._currentToken = None;

    def notifyListeners(self, e:LexerNoViableAltException):
        self._hasErrors = True

        start = self._tokenStartCharIndex
        stop = self._input.index
        text = self._input.getText(start, stop)
        if self._currentToken.type in [COOL_LEX.STRING, COOL_LEX.STRING_FIRSTLINE, COOL_LEX.STRING_INNERLINE, COOL_LEX.STRING_SIMPLE_START, COOL_LEX.STRING_SIMPLE_CONTENT ] or text[0] == '"':
            if self._input.data[start] == 0:
                msg = "String contains null character"
            elif self.inputStream.size == self.inputStream.index:
                msg = "EOF in string constant"
            else:
                msg = "Unterminated string constant"
        else:
            msg = "'" + self.getErrorDisplay(text) + "'"
        if self._token == None:
            line = self.line
            col= self.column
        else:
            line = self._tokenStartLine
            col = self._tokenStartColumn
        listener = self.getErrorListenerDispatch()
        listener.syntaxError(self, self._token, line, col, msg, e)

    def nextToken(self):
        while (True):
            lastToken = self._currentToken
            self._currentToken = super().nextToken()
            if self._currentToken.type in [COOL_LEX.OPEN_COMMENT, COOL_LEX.CLOSE_COMMENT]:
                continue
            elif self._currentToken.type == COOL_LEX.STRING_FIRSTLINE:
                continue
            elif self._currentToken.type == COOL_LEX.STRING_INNERLINE:
                continue
            else:
                 break

        if self._currentToken.type == Token.EOF:
            if lastToken != None and lastToken.type == COOL_LEX.OPEN_COMMENT:
                self._hasErrors = True
                listener = self.getErrorListenerDispatch()
                listener.syntaxError(self, self._currentToken, self._currentToken.line, self._currentToken.column,
                                     "EOF in comment", None)
        return self._currentToken;

    def reset(self):
        super().reset()
        self._hasErrors = False
        self._currentToken = None;

    @property
    def hasErrors(self):
        return self._hasErrors