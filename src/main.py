import sys, fileinput
from argparse import ArgumentParser
from compiler.utils.compiler_containers import container_dict

parser_input =  ArgumentParser(description= 'This is the Diaz-Horrach cool compiler, an school project.\nRead this help and see the ofitial repo')
parser_input.add_argument('files_for_compile', help = 'The file(s) to be compiled', nargs= '+')
parser_input.add_argument("--lexer", help = 'Select the lexer that you could use from avialable options', choices = container_dict['lexer_options'].keys())
parser_input.add_argument("--parser", help = 'Select the lexer that you could use from avialable options', choices = container_dict['parser_options'].keys())
parser_input.add_argument("--output", help = 'Put the info of the selected components in the standard output.', choices = ['l','p','t'])

args = parser_input.parse_args()
working_input = fileinput.input(files = args.files_for_compile)


