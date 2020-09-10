from build.compiler_struct import LEXER, PARSER
from cil.nodes import CilProgramNode
from travels.ciltomips import MipsCodeGenerator
from typecheck.evaluator import evaluate_right_parse
from comments import find_comments
from travels.ctcill import CilDisplayFormatter, CoolToCILVisitor
import sys


def report(errors: list):
    for error in errors:
        print(error)


def pipeline(program: str, deep: int) -> None:
    try:
        program = find_comments(program)
    except AssertionError as e:
        print(e)
        sys.exit(1)

    # Right now, program has no comments, so is safe to pass it to the LEXER
    try:
        tokens = LEXER(program)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Parse the tokens to obtain a derivation tree
    try:
        parse = PARSER(tokens)
    except Exception as e:
        print(e)
        sys.exit(1)
    # build the AST from the obtained parse
    # try:
    ast = evaluate_right_parse(parse, tokens[:-1])
    # except Exception as e:
    #     print(e)
    #     sys.exit(1)
    #####################
    # Start the visitors #
    ######################

    # Run type checker visitor
    errors, context, scope = ast.check_semantics(deep)
    if errors:
        report(errors)
        sys.exit(1)

    print(scope)

    cil_travel = CoolToCILVisitor(context)
    cil_program_node = cil_travel.visit(ast, scope)
    # formatter = CilDisplayFormatter()
    # print(formatter(cil_program_node))

    mips_gen = MipsCodeGenerator()
    assert isinstance(cil_program_node, CilProgramNode)
    source = mips_gen(cil_program_node)
    print(source)


text = """
class A {
    a : Int ;
    suma ( a : AUTO_TYPE , b : Int ) : AUTO_TYPE {
        a + b
    };
    b : Int ;
};

class B inherits A {
    c : Int ;
    f ( d : Int , a : A ) : AUTO_TYPE { {
        let f : AUTO_TYPE <- 10 in 8 ;
        let c : AUTO_TYPE <- a. suma ( 5 , f ) in c ;
        c;
    } };
};

class Main {

    main(): Object {
        {
            (new B).f(5, (new A));
        }
    };
};
"""
pipeline(text, 5)
