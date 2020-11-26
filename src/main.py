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

collect_errors = []
collect = Collector(collect_errors)
collect.visit(ast)
context = collect.context
builder_errors = []
#builder = Builder(context, builder_errors)
#builder.visit(ast)
#context = builder.context
#checker_errors = []
#checker = Checker(context, checker_errors)
#scope = checker.visit(ast)


# cil = COOL_TO_CIL(checker.context)
# # cil = COOL_TO_CIL_VISITOR(checker.context)
# # sc = Scope()
# cil_ast = cil.visit(ast,scope)
# # f_ast = Format().visit(ast)
# f_ast = CIL_FORMATTER().visit(cil_ast)
# string_formatted = str(f_ast)
#output_file.write(string_formatted)
output_file.write(str(collect_errors))
#print(str(collect_errors))
#output_file.write(str(builder_errors))
#output_file.write(str(checker_errors))
#output_file.write(collect_errors)
output_file.close()


if not operations:
    message = f'ERROR at or near "{parse.lex}"'
    print(SyntacticError(parse.line,parse.column, message))
    exit(1)
#print(parse)


if len(collect_errors):
    for e in collect_errors:
        print(e)
    print('/n')
    exit(1)

exit(0)