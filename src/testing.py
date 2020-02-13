from coolgrammar import grammar
from lexer import tokenizer
from parserr.lr import LALRParser
from parserr.shiftreduce import ShiftReduceParser
import cloudpickle

GRAMMAR, LEXER = grammar.build_cool_grammar()
PARSER = LALRParser(GRAMMAR, verbose=True)

SIMPLE_PROGRAM = """
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
  TOKS = LEXER(SIMPLE_PROGRAM)
  parse = PARSER(TOKS)
  # Try to save the parser and then reuse it
  # with open('.parser.dmp','wb') as file:
  #   cloudpickle.dump(PARSER, file)

  with open('.parser.dmp', 'rb') as file:
    parser = cloudpickle.load(file)
    print(parser(TOKS))
except Exception as e:
  print(e)
