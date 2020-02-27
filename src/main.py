import sys, fileinput
from argparse import ArgumentParser


parser_input =  ArgumentParser(description= 'This is the Diaz-Horrach cool compiler, an school project.\nRead this help and see the ofitial repo')
parser_input.add_argument('files_for_compile', help = 'The file(s) to be compiled', nargs= '*')
parser_input.add_argument("--lex", '-l', help = 'Output the lexer for the .cl file', action = 'store_true')
parser_input.add_argument("--ast", help = 'Output the abstract syntax tree (AST) for the .cl file', action = 'store_true')
parser_input.add_argument("--outputFile", '-oF', help = 'Put the info of the output options in the specified file.\n If no output option is specified the file creates empty.')
args = parser_input.parse_args()
working_input = fileinput.input(files = args.files_for_compile)
if args.outputFile:
    fd = open(mode= 'x', file = './output_files' + args.outputFile)

