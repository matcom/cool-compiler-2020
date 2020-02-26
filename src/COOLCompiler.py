import sys
from antlr4 import *
from COOLLexer import COOLLexer
from COOLParser import COOLParser
from COOLListener import COOLListener

def main(argv):
    input = FileStream(argv[1])
    lexer = COOLLexer(input)
    stream = CommonTokenStream(lexer)
    parser = COOLParser(stream)
    tree = parser.program()

if __name__ == '__main__':
    main(sys.argv)
