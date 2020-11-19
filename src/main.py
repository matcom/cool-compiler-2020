 #!/usr/bin/python3

from engine import *
import sys

args = sys.argv

if len(args) != 3:
    exit(1)

input_file = open(args[1], "r")
output_file = open(args[2], 'w')

t = input_file.read()

# output_file = args[2]

tokens, errors = tokenizer(t)

#print(tokens)
if len(errors):
    for e in errors:
        print(e)
    exit(1)


parse, operations = CoolParser(tokens)

ast = evaluate_reverse_parse(parse,operations,tokens)

collect = Collector()
collect.visit(ast)

context = collect.context
builder = Builder(context)
builder.visit(ast)
context = builder.context
checker = Checker(context)
checker.visit(ast)

# cil = COOL_TO_CIL_VISITOR(checker.context)

# cil_ast = cil.visit(ast)

# f_ast = CIL_FORMATTER().visit(cil_ast)
# string_formatted = str(f_ast)
# output_file.write(string_formatted)
# output_file.close()


if not operations:
    message = f'ERROR at or near "{parse.lex}"'
    print(SyntacticError(parse.line,parse.column, message))
    exit(1)
#print(parse)
exit(0)
