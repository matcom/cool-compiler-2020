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


text = r"""
class Main inherits IO {
	-- the class has features. Only methods in this case.
	main(): Object {
		{
			out_string("Enter n to find nth fibonacci number!\n");
			out_int(fib(in_int()));
			out_string("\n");
		}
	};

	fib(i : Int) : Int {	-- list of formals. And the return type of the method.
			let a : Int <- 1,
					b : Int <- 0,
					c : Int <- 0
			in
			{
			while (not (i = 0)) loop	-- expressions are nested.
			{
				c <- a + b;
				i <- i - 1;
				b <- a;
				a <- c;
			}
			pool;
			c;
			}
	};

};

"""
pipeline(text, 5)
