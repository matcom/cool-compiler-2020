import sys, fileinput, os
from argparse import ArgumentParser
from compiler.components.lexer.lexer_analyzer import tokenizer, tokens
from compiler.components.parser.syntax_analyzer import run_parser
from compiler.components.semantic.semantic_analyzer import semanticAnalyzer
from compiler.components.semantic.context import programContext
from compiler.components.generation.CIL_generator import CILVisitor
#from compiler.utils.basics_AST import build_basic_ast
from compiler.utils.preprocess_input import replace_tabs
from compiler.components.generation.MIPS_generator import MipsVisitor
import compiler.components.semantic.AST_definitions as ast
import subprocess as sp

def build_basic_ast():
    fpath = "./compiler/utils/basics_classes.cl"
    with open(fpath, encoding="utf-8") as file:
        code = file.read()
        _, _, real_col_basic= tokenizer(code)
        ast_basic,_= run_parser(tokens= tokens, 
                            source_program= code, 
                            real_col= real_col_basic)
        for _class in ast_basic.class_list:
            if _class.idName == 'Int' or _class.idName == 'Bool' or _class.idName == 'String':
                _class.attributes.append(ast.NodeAttr(idName = '_val',
                                                      _type= '__prim_zero_slot',
                                                      line= 0, column= 0))
            if _class.idName== 'String':
                _class.attributes.append(ast.NodeAttr(idName = '_str_field',
                                                      _type= '__prim_empty_slot',
                                                      line= 0, column= 0))
        return ast_basic

parser_input =  ArgumentParser(description= 'This is the Diaz-Horrach cool compiler, an school project.\nRead this help and see the ofitial repo')
parser_input.add_argument('files_for_compile', help = 'The file(s) to be compiled', nargs= '+')
parser_input.add_argument('--test', help = 'Indicates if the compiling is for test', action="store_true")
""" parser_input.add_argument("--lexer", help = 'Select the lexer that you could use from avialable options', choices = component_injector['lexer_options'].keys(),
                            default='cool')
parser_input.add_argument("--parser", help = 'Select the lexer that you could use from avialable options', choices = component_injector['parser_options'].keys())
parser_input.add_argument("--output", help = 'Put the info of the selected components in the standard output.', choices = ['l','p','t'])
 """



args= parser_input.parse_args()
file= open(args.files_for_compile[0])
working_input= file.read()
working_input_with_no_tabs = replace_tabs(working_input)


all_errors= []
token_errors, tokens_for_input, real_col= tokenizer(working_input_with_no_tabs)

if token_errors:
    for error in token_errors:
        print(error)
    exit(1)


ast_result, parser_errors= run_parser(tokens,
                                      working_input_with_no_tabs,
                                      real_col)

if parser_errors:
    for error in parser_errors:
        print(error)
    exit(1)


basic_ast= build_basic_ast()
# Adding the builtIn classes
ast_result.class_list= basic_ast.class_list + ast_result.class_list

# Running semantic analyzer
sa = semanticAnalyzer(ast_result, programContext)
sa.run_visits()


all_errors += token_errors + parser_errors + sa.errors

if all_errors:
    for error in all_errors:
        print(error)
    exit(1)


# Running code generation

cilGen= CILVisitor(programContext, mapExpr= sa.mapExprWithResult)
programResult= cilGen.visit(sa.ast)

mipsGen= MipsVisitor(programContext)

mipsCode= mipsGen.visit(programResult)


# Saving the compiling
filePath= args.files_for_compile[0]

fileToWritePath= filePath[:filePath.rfind('.') + 1] + 'mips'

with open(fileToWritePath, 'w', encoding="utf-8") as file:
    stream = '#Compiled by DiazRock COOL compiler\n'
    for line in mipsCode:
        stream += line

    file.write(stream)
    if args.test:
        pathTest= filePath[ :filePath.rfind('.') ] + '_input.txt'
        spim= 'spim -f ' + fileToWritePath
        os.system('cat "{}"|{} '.format(pathTest, spim) )
    
