import sys, fileinput
from argparse import ArgumentParser
from compiler.components.lexer_analyzer import tokenizer, tokens
from compiler.components.syntax_analyzer import run_parser
from compiler.components.semantic_analyzer import semanticAnalyzer
from compiler.utils.context import programContext
from compiler.utils.preprocess_input import replace_tabs


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
#if parser_errors: print("In the parser_errors ", parser_errors)

sa = semanticAnalyzer(ast_result)
sa.run_visits()


#print('errors %s' %sa.errors)
all_errors += token_errors + parser_errors + sa.errors

if all_errors:
    for error in all_errors:
        print(error)
    exit(1)
