import sys
import os.path
from antlr4 import *
from COOLLexer import COOLLexer
from COOLLexerErrorListener import COOLLexerErrorListener
from COOLParser import COOLParser
from COOLParserErrorListener import COOLParserErrorListener
from COOLListener import COOLListener

def main(argv):
    if not os.path.isfile(argv[1]):
        print("invalid input filename")
        return

    input = FileStream(argv[1])

    lexer = COOLLexer(input)
    lexer.removeErrorListeners()
    lexer.addErrorListener(COOLLexerErrorListener())
    token = lexer.nextToken()
    while token.type != Token.EOF:
        token = lexer.nextToken()

    if lexer.hasErrors:
        return

    lexer.reset();
    stream = CommonTokenStream(lexer)
    parser = COOLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(COOLParserErrorListener())

    tree = parser.program()

if __name__ == '__main__':
    main(sys.argv)
