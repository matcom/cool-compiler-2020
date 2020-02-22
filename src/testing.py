from coolgrammar import grammar
from parserr.lr import LALRParser
from comments import find_comments

GRAMMAR, LEXER = grammar.build_cool_grammar()
PARSER = LALRParser(GRAMMAR, verbose=True)
prog = r"""
class Test {
    testing4(): Int {
        test1 <-- ~(1 + 2 + 3 + 4 + 5) -- The left side must be an expression
    };
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};
"""

# First Round of tests
TOKS = None
try:
    program = find_comments(prog)
    TOKS = LEXER(program)
    parse = PARSER(TOKS)
    # Try to save the parser and then reuse it
    # with open('.parser.dmp','wb') as file:
    # cloudpickle.dump(PARSER, file)

    #with open('.parser.dmp', 'rb') as file:
    # parser = cloudpickle.load(file)
    print(parse)
except Exception as e:
    print(e)
