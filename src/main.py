#!/usr/bin/python3

from engine import *
import sys

args = sys.argv

input_file = open(args[1], "r")
output_file = open(args[2], 'w')

t = input_file.read()

lexer = CoolLexer()
tokens, errors = lexer.tokenize(t)

if len(errors):
    for e in errors:
        print(e)
    exit(1)

if not tokens:
    print(SyntacticError(0, 0, 'ERROR at or near "%s"' % 'EOF'))
    exit(1)

lexer = CoolLexer()
parser = CoolParser(lexer)
ast, errors = parser.parse(t)

if errors:
    for error in errors:
        print(error)
    exit(1)
# print(ast)

# fmatter = Format()
# tree = fmatter.visit(ast, 0)

# print(tree)

collect_errors = []
collect = Collector(collect_errors)
collect.visit(ast)

if len(collect_errors):
    for e in collect_errors[::-1]:
        print(e)
    exit(1)

context = collect.context
builder_errors = []
builder = Builder(context, builder_errors)


builder.visit(ast)

if len(builder_errors):
    for e in builder_errors:
        print(e)
    exit(1)

context = builder.context
checker_errors = []
checker = Checker(context, checker_errors)
scope = checker.visit(ast)

if len(checker_errors):
    for e in checker_errors:
        print(e)
    exit(1)


cil = COOL_TO_CIL(checker.context)
cil_ast = cil.visit(ast)

emsamb = CIL_TO_MIPS()
emsamb.visit(cil_ast)

f_ast = emsamb.mips.compile()
# f_ast = CIL_FORMATTER().visit(cil_ast)

string_formatted = str(f_ast)
output_file.write(string_formatted)

input_file.close()
output_file.close()

exit(0)
