from coolgrammar import grammar
from parserr.lr import LALRParser
from comments import find_comments

GRAMMAR, LEXER = grammar.build_cool_grammar()
PARSER = LALRParser(GRAMMAR, verbose=True)
prog = r"""
class Main inherits IO {
    main() : Object {
            {
                    out_string("Enter number of numbers to multiply\n");
                    out_int(prod(in_int()));
                    out_string("\n");
            }
    };

    prod(i : Int) : Int {
        let y : Int <- 1 in {
                while (not (i = 0) ) loop {
                        out_string("Enter Number: ");
                        y <- y * in_int(Main : Int);    -- the parser correctly catches the error here
                        i <- i - 1;
                }
                    pool;
                y;
        }
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
