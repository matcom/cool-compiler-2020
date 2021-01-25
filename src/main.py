import sys, fileinput
from argparse import ArgumentParser
from compiler.components.lexer_analyzer import tokenizer, tokens
from compiler.components.syntax_analyzer import run_parser

parser_input =  ArgumentParser(description= 'This is the Diaz-Horrach cool compiler, an school project.\nRead this help and see the ofitial repo')
parser_input.add_argument('files_for_compile', help = 'The file(s) to be compiled', nargs= '+')
""" parser_input.add_argument("--lexer", help = 'Select the lexer that you could use from avialable options', choices = component_injector['lexer_options'].keys(),
                            default='cool')
parser_input.add_argument("--parser", help = 'Select the lexer that you could use from avialable options', choices = component_injector['parser_options'].keys())
parser_input.add_argument("--output", help = 'Put the info of the selected components in the standard output.', choices = ['l','p','t'])
 """
args = parser_input.parse_args()
#print(args.files_for_compile)
file = open(args.files_for_compile[0])
working_input = file.read()

all_errors = []
token_errors, tokens_for_input, real_col = tokenizer(working_input)
if token_errors:
    print(token_errors[0])
    exit(1)
#print(tokens_for_input)

parser_errors = run_parser(tokens, working_input, real_col)

""" print('tokens for _input \n')
print(tokens_for_input)
print('---------------') """
if parser_errors:
    print(parser_errors[0])
    exit(1)


exit(0)

