from coolgrammar import grammar
from lexer import tokenizer
from parserr.lr import LALRParser, LR1Parser
from parserr.shiftreduce import ShiftReduceParser
import cloudpickle
from comments import find_comments

GRAMMAR, LEXER = grammar.build_cool_grammar()
PARSER = LALRParser(GRAMMAR, verbose=True)

test_String = r"""
'Hello World'
"""

test_program = r"""
class Main {
    main(): Object {
        (new Alpha).print()
    };
};

class Test {
    test1: Object;
    
    testing1(): Int {
        2 + 2
    };

    test2: Int <- 1;

    test3: String <- "1";

    testing2(a: Alpha, b: Int): Int {
        2 + 2
    };

    testing3(): String {
        "2 + 2"
    };

    testing4(): String {
        Test1 <- 'Hello World' -- Identifiers begin with a lower case letter
    };
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};
"""
SIMPLE_PROGRAM = r"""
"kjsafkljd\saa\aa"
"helloworld"
class A inherits IO
{
    attribute : int <- 10;

    main(): SELF_TYPE
     {
           print("Hello There");
     };

    a(n :int) : int
    {
       n;
    };

    b (): int
    {
        let varj : int <- 10 in
        {
          varj;
        };

        let varl : int in
        {
          varh;
         };

         let varj :int, varu : string <- "Hello There" in
         {
            var;
         };

         case varj of
              x : int => x + 10 ;
              x : string => "Hi  there" ;
              x : object => varj;
           esac;


         a(10);
     };

};
"""

# First Round of tests
TOKS = None
try:
    program = find_comments(test_program)
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
