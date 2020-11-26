import sys, fileinput
from argparse import ArgumentParser
from compiler.components.lexer_analyzer import tokenizer, tokens
from compiler.components.syntax_analyzer import run_parser
from compiler.components.semantic_analyzer import semanticAnalyzer
from compiler.utils.context import programContext


parser_input =  ArgumentParser(description= 'This is the Diaz-Horrach cool compiler, an school project.\nRead this help and see the ofitial repo')
parser_input.add_argument('files_for_compile', help = 'The file(s) to be compiled', nargs= '+')
""" parser_input.add_argument("--lexer", help = 'Select the lexer that you could use from avialable options', choices = component_injector['lexer_options'].keys(),
                            default='cool')
parser_input.add_argument("--parser", help = 'Select the lexer that you could use from avialable options', choices = component_injector['parser_options'].keys())
parser_input.add_argument("--output", help = 'Put the info of the selected components in the standard output.', choices = ['l','p','t'])
 """

args= parser_input.parse_args()
file= open(args.files_for_compile[0])
working_input= file.read()

all_errors= []
token_errors, tokens_for_input, real_col= tokenizer(working_input)


ast_result, parser_errors= run_parser(tokens, working_input, real_col)
#if parser_errors: print("In the parser_errors ", parser_errors)

#sa = semanticAnalyzer(ast_result)

#sa.run_visits()
#print('context of the input %s' %programContext)
#print('errors %s' %sa.errors)
all_errors += token_errors + parser_errors
#+ sa.errors

if all_errors:
    for error in all_errors:
        print(error)
    exit(1)
