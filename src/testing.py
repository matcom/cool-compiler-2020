from coolgrammar import grammar
from lexer import tokenizer
from parserr.lr import LALRParser
from parserr.shiftreduce import ShiftReduceParser
import cloudpickle
from comments import find_comments

GRAMMAR, LEXER = grammar.build_cool_grammar()
#PARSER = LALRParser(GRAMMAR, verbose=True)
TEST = r"""

"This \
is OK"
"This is not
OK"
"""

string2 = r"""
"               May the Triforce              \
                      0                       \
                     0v0                      \
                    0vvv0                     \
                   0vvvvv0                    \
                  0vvvvvvv0                   \
                 0vvvvvvvvv0                  \
                0vvvvvvvvvvv0                 \
               000000000000000                \
              0v0           0v0               \
             0vvv0         0vvv0              \
            0vvvvv0       0vvvvv0             \
           0vvvvvvv0     0vvvvvvv0            \
          0vvvvvvvvv0   0vvvvvvvvv0           \
         0vvvvvvvvvvv0 0vvvvvvvvvvv0          \
        00000000000000000000000000000         \
                be with you!"""

TEST_PROGRAM = r"""
"lkjdsafkljdsalfj\u0000dsafdsaf\u0000djafslkjdsalf\nsdajf\" lkjfdsasdkjfl"123
adsfasklj#
LKldsajf iNhERITS
"lkdsajf"

(*
#1 STR_CONST "lkjdsafkljdsalfju0000dsafdsafu0000djafslkjdsalf\nsdajf\" lkjfdsasdkjfl"
#1 INT_CONST 123
#2 OBJECTID adsfasklj
#2 ERROR "#"
#3 TYPEID LKldsajf
#3 INHERITS
#4 STR_CONST "lkdsajf"
*)
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

space_test = r"t t t t ?"
# First Round of tests
TOKS = None
try:
    program = find_comments(space_test)
    TOKS = LEXER(program)
    # parse = PARSER(TOKS)
    # Try to save the parser and then reuse it
    # with open('.parser.dmp','wb') as file:
    # cloudpickle.dump(PARSER, file)

    #with open('.parser.dmp', 'rb') as file:
    # parser = cloudpickle.load(file)
    print(TOKS)
except Exception as e:
    print(e)
