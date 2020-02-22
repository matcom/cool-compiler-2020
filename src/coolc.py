from sys import argv
from cool_lang.lexer import COOL_LEXER
import cool_lang.utils as clutils


INPUT_FILE = argv[1]
OUTPUT_FILE = argv[2]

result = clutils.preprocessing.process(INPUT_FILE)
code, comments, errors = result.data, result.comments, result.errors

if errors: # Exiting if errors in the comments
    for error in errors:
        print(error)
    exit(1)

clexer = COOL_LEXER()
if not clexer.tokenize(code):
    for error in clexer.errors:
        print(error)
    exit(1)

for token in clexer.result:
    print(token)
