from build.compiler_struct import LEXER, PARSER
from cil.nodes import CilProgramNode
from travels.ciltomips import MipsCodeGenerator
from travels.ctcill import CoolToCILVisitor
from typecheck.evaluator import evaluate_right_parse
from comments import find_comments
from argparse import ArgumentParser
import sys


def report(errors: list):
    for error in errors:
        print(error)


def pipeline(program: str, deep: int, file_name: str) -> None:
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
    try:
        ast = evaluate_right_parse(parse, tokens[:-1])
    except Exception as e:
        print(e)
        sys.exit(1)
    #####################
    # Start the visitors #
    ######################

    # Run type checker visitor
    errors, context, scope = ast.check_semantics(deep)
    if errors:
        report(errors)
        sys.exit(1)

    # Run Cool to CIL visitor
    cil_visitor = CoolToCILVisitor(context)
    try:
        cil_program = cil_visitor.visit(ast)
    except Exception as e:
        print(e)
        sys.exit(1)

    assert isinstance(cil_program, CilProgramNode)

    # Run CIL to MIPS visitor
    code_gen = MipsCodeGenerator()
    file_str = code_gen(cil_program)

    with open(f"{file_name}.mips", "w+") as f:
        f.write(file_str)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('file', type=str, help="Cool source file.")
    parser.add_argument('--deep', type=int)
    args = parser.parse_args()
    deep = 3 if args.deep is None else args.deep
    with open(args.file, "r") as f:
        program = f.read()
        pipeline(program, deep, args.file)
        sys.exit(0)
