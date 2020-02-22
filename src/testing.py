from coolgrammar import grammar
from lexer import tokenizer
from parserr.lr import LALRParser, LR1Parser
from parserr.shiftreduce import ShiftReduceParser
import cloudpickle
from comments import find_comments

GRAMMAR, LEXER = grammar.build_cool_grammar()
PARSER = LALRParser(GRAMMAR, verbose=True)
prog = r"""
(* Case expressions provide runtime type tests on objects *)

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

    testing4(x: Int, y: Int): Test {
        self
    };

    testing5(a: String, b: String): IO {
        If a.length() < b.length() THeN
            new IO.out_string("La cadena \"".concat(b).concat("\" es mas larga que la cadena \"").concat(a).concat("\"."))
        eLSe
            if a.length() = b.length() THeN
                new IO.out_string("La cadena \"".concat(a).concat("\" mide igual que la cadena \"").concat(b).concat("\"."))
            ElsE
                new IO.out_string("La cadena \"".concat(a).concat("\" es mas larga que la cadena \"").concat(b).concat("\"."))
            fI
        Fi
    };

    testing6(a: Int): IO {
        let count: Int <- 0, pow: Int 
        in {
            -- count <- 0;
            pow <- 1;
            while pow < a 
            loop 
                {
                    count <- count + 1;
                    pow <- pow * 2;
                } 
            pool;
            new IO.out_string("El logaritmo en base 2 de ").out_int(a).out_string(" es ").out_int(count);
        }
    };

    testing7(): Object {
        case true of
            x: Int => new IO.out_string("Es un entero!");
            y: String => new IO.out_string("Es una cadena!"); 
            Mazinger_Z: Bool => new IO.out_string("Es un booleano!"); -- Identifiers starts with a lowercase letter
        esac
    };
};

class Test2 {
    test1: Test <- new Test;

    testing1(): Test {
        test1.testing4(1 + 1, 1 + 2).testing4(2 + 3, 3 + 5).testing4(5 + 8, 8 + 13)
    };

    testing2(x: Int, y: Int): Test2 {
        self
    };

    testing3(): Test2 {
        testing2(1 + 1, 1 + 2).testing2(2 + 3, 3 + 5).testing2(5 + 8, true + fALSE)
    };

    testing4(): Object {
        test1@Object.copy()
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
