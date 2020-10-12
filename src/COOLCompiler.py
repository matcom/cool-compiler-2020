import sys
import os.path
import errno
from antlr4 import *
from COOLLexer import COOLLexer
from COOLLexerErrorListener import COOLLexerErrorListener
from COOLParser import COOLParser
from COOLParserErrorListener import COOLParserErrorListener
from COOLListener import COOLListener
from Visitors import  TypeCOOLVisitor
from Visitors import  SemanticCOOLVisitor
from Visitors import CodegenVisitor
from collections import deque

def main(argv):
    if not os.path.isfile(argv[1]):
        print("invalid input filename: " + argv[1])
        return sys.exit(errno.EPERM)

    input = FileStream(argv[1])

    lexer = COOLLexer(input)
    lexer.removeErrorListeners()
    lexer.addErrorListener(COOLLexerErrorListener())
    token = lexer.nextToken()
    while token.type != Token.EOF:
        #print(token.type)
        token = lexer.nextToken()
    if lexer.hasErrors:
        return sys.exit(errno.EPERM)
    lexer.reset();
    stream = CommonTokenStream(lexer)
    parser = COOLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(COOLParserErrorListener())
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() > 0:
        return sys.exit(errno.EPERM)
    visitor = TypeCOOLVisitor()
    visitor.visitProgram(tree, argv[1])
    typeTree = visitor.TypeTable
    consTble = visitor.ConstantTable
    semanticAnalizer = SemanticCOOLVisitor(typeTree)
    codegenerator = CodegenVisitor(typeTree, consTble, visitor.Counter)
    semanticAnalizer.visitProgram(tree)

    outFilename = os.path.splitext(argv[1])[0] + ".s"
    codegenerator.visitProgram(tree, outFilename)
    none = typeTree["Object"]




if __name__ == '__main__':
    main(sys.argv)
