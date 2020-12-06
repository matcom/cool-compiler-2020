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


text = r"""class Main inherits IO {
    main() : IO {
	(let c : Complex <- (new Complex).init(1, 1) in
	    {
	        -- trivially equal (see CoolAid)
	        if c.reflect_X() = c.reflect_0()
	        then out_string("=)\n")
	        else out_string("=(\n")
	        fi;
		-- equal
	        if c.reflect_X().reflect_Y().equal(c.reflect_0())
	        then out_string("=)\n")
	        else out_string("=(\n")
	        fi;
	    }
	)
    };
};

class Complex inherits IO {
    x : Int;
    y : Int;

    init(a : Int, b : Int) : Complex {
	{
	    x = a;
	    y = b;
	    self;
	}
    };

    print() : Object {
	if y = 0
	then out_int(x)
	else out_int(x).out_string("+").out_int(y).out_string("I")
	fi
    };

    reflect_0() : Complex {
	{
	    x = ~x;
	    y = ~y;
	    self;
	}
    };

    reflect_X() : Complex {
	{
	    y = ~y;
	    self;
	}
    };

    reflect_Y() : Complex {
	{
	    x = ~x;
	    self;
	}
    };

    equal(d : Complex) : Bool {
	if x = d.x_value()
	then
	    if y = d.y_value()
	    then true
	    else false
	    fi
	else false
	fi
    };

    x_value() : Int {
	x
    };

    y_value() : Int {
	y
    };
};

"""
pipeline(text, 5)
