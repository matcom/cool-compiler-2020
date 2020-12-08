from argparse import ArgumentParser
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


def pipeline(program: str, deep: int, file_name) -> None:
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

    with open(f"{file_name[: len(file_name) - 3]}.mips", "w+") as f:
        f.write(source)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str, help="Cool source file.")
    parser.add_argument("--deep", type=int)
    args = parser.parse_args()
    deep = 1 if args.deep is None else args.deep
    with open(args.file, "r") as f:
        program = f.read()
        pipeline(program, deep, args.file)
        sys.exit(0)
