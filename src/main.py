 #!/usr/bin/python3

from engine import *
import sys

args = sys.argv

if len(args) != 3:
    exit(1)

input_file = open(args[1], "r")

t = input_file.read()

output_file = args[2]

tokens, errors = tokenizer(t)

#print(tokens)
if len(errors):
    for e in errors:
        print(e)
    exit(1)

exit(0)

# parse, operations = CoolParser(tokens)

# if not operations:
#     print(f"Unexpected token: {parse.lex} at Ln: {parse.line}, Col {parse.column}\n")

# print(parse)