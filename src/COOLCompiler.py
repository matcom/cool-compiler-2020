import sys
import os.path
import errno
from antlr4 import *
from COOLLexer import COOLLexer
# from COOLLexerErrorListener import COOLLexerErrorListener
# from COOLParser import COOLParser
# from COOLParserErrorListener import COOLParserErrorListener
# from Visitors import  TypeCOOLVisitor
# from Visitors import  SemanticCOOLVisitor
# from Visitors import CodegenVisitor



def main(argv):
    print("COOLCompiler 1.0.3")
    print("Copyright (C) 2019-2020: Liset Silva Oropesa, Pablo A. de Armas Suárez, Yenli Gil Machado")

    if len(argv) < 2:
        print("ERROR: no input filename")
        return sys.exit(errno.EPERM)

    if not os.path.isfile(argv[1]):
        print("ERROR: invalid input filename: " + argv[1])
        return sys.exit(errno.EPERM)


    input = FileStream(argv[1], "utf-8")
    lexer = COOLLexer(input)
    # lexer.removeErrorListeners()
    # lexer.addErrorListener(COOLLexerErrorListener())
    # token = lexer.nextToken()
    # while token.type != Token.EOF:
    #     #print(token.type)
    #     token = lexer.nextToken()
    # if lexer.hasErrors:
    #     return sys.exit(errno.EPERM)
    # lexer.reset()
    # stream = CommonTokenStream(lexer)
    # parser = COOLParser(stream)
    # parser.removeErrorListeners()
    # parser.addErrorListener(COOLParserErrorListener())
    # tree = parser.program()
    # if parser.getNumberOfSyntaxErrors() > 0:
    #     return sys.exit(errno.EPERM)
    # visitor = TypeCOOLVisitor()
    # visitor.visitProgram(tree, argv[1])
    # typeTree = visitor.TypeTable
    # consTble = visitor.ConstantTable
    # semanticAnalizer = SemanticCOOLVisitor(typeTree)
    # codegenerator = CodegenVisitor(typeTree, consTble, visitor.Counter)
    # semanticAnalizer.visitProgram(tree)
    # if semanticAnalizer.hasNoError:
    #     if len(argv) > 2:
    #         outFilename = argv[2]
    #     else:
    #         outFilename = os.path.splitext(argv[1])[0] + ".s"
    #     codegenerator.visitProgram(tree, outFilename)
    # else:
    #     return sys.exit(errno.EPERM)

    return 0

if __name__ == '__main__':
    main(sys.argv)
