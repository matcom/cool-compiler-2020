from build.compiler_struct import LEXER, PARSER
from cil.nodes import CilProgramNode
from travels.ciltomips import MipsCodeGenerator
from typecheck.evaluator import evaluate_right_parse
from comments import find_comments
from travels.ctcill import CilDisplayFormatter, CoolToCILVisitor
import sys


def report(errors: list):
    for error in set(errors):
        print(error)


def pipeline(program: str, deep: int) -> None:
    try:
        program = find_comments(program)
        program = program.replace('\t', ' ' * 4)
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

    cil_travel = CoolToCILVisitor(context)
    cil_program_node = cil_travel.visit(ast, scope)
    # formatter = CilDisplayFormatter()
    # print(formatter(cil_program_node))

    mips_gen = MipsCodeGenerator()
    assert isinstance(cil_program_node, CilProgramNode)
    source = mips_gen(cil_program_node)
    print(source)


text = r"""(*
e@B.f() invokes the method
f in class B on the object that is the value of e. For this form of dispatch, the static type to the left of
“@”must conform to the type specified to the right of “@”.
*)

class A {
	f(x: Int, y: Int): Int { x + y };
	g(x: Int): Int { x + x };
};
class B inherits A {
	f(a: Int, b: Int): Int { a - b };
	sum(m: Int, n: Int, p: Int): Int { m + n + p };
};
class C inherits B {
	ident(m: Int): Int { m };
	f(m: Int, n: Int): Int { m * n };
};
class D inherits B { 
	ident(v: String): IO { new IO.out_string(v) };
	f(v: Int, w: Int): Int { v / w };
	g(v: Int): Int { v + v + v };
	sum(v: Int, w: Int, z: Int): Int { v - w - z };
};

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	a: A <- new D;
	b: Int <- new D@B.sum(1, 2, 3);
	test: Int <- a@B.sum(1, 2, 3);
}; 

"""
pipeline(text, 5)
