import sys
from cmp.parser import Parser

p = Parser()
p.build()

with open(sys.argv[1]) as f:
    p.parser.parse("".join(f))
