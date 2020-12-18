#!/usr/bin/python3

from engine import *
import sys


def compile_code(inFile, outFile, output_cil=False):
    input_file = open(inFile, "r")
    output_file = open(outFile, 'w')

    text_code = input_file.read()

    ast = parse(text_code)
    context = collect(ast)
    context = builder(ast, context)
    context = checker(ast, context)

    string_formatted = codegen(ast, context, output_cil)
    output_file.write(string_formatted)

    input_file.close()
    output_file.close()

    exit(0)


def parse(text_code):
    lexer = CoolLexer()
    tokens, errors = lexer.tokenize(text_code)

    if len(errors):
        for e in errors:
            print(e)
        exit(1)

    if not tokens:
        print(SyntacticError(0, 0, 'ERROR at or near "%s"' % 'EOF'))
        exit(1)

    lexer = CoolLexer()
    parser = CoolParser(lexer)
    ast, errors = parser.parse(text_code)

    if errors:
        for error in errors:
            print(error)
        exit(1)
    # print(ast)

    # fmatter = Format()
    # tree = fmatter.visit(ast, 0)

    # print(tree)
    return ast


def collect(ast):
    collect_errors = []
    collect = Collector(collect_errors)
    collect.visit(ast)

    if len(collect_errors):
        for e in collect_errors[::-1]:
            print(e)
        exit(1)
    return collect.context


def builder(ast, context):
    builder_errors = []
    builder = Builder(context, builder_errors)

    builder.visit(ast)

    if len(builder_errors):
        for e in builder_errors:
            print(e)
        exit(1)
    return builder.context


def checker(ast, context):
    checker_errors = []
    checker = Checker(context, checker_errors)
    scope = checker.visit(ast, Scope())

    if len(checker_errors):
        for e in checker_errors:
            print(e)
        exit(1)
    return checker.context


def codegen(ast, context, output_cil=False):
    cil = COOL_TO_CIL(context)
    cil_ast = cil.visit(ast)

    if output_cil:
        formatted_ast = CIL_FORMATTER().visit(cil_ast)
        with open('out.cil', 'w') as f:
            f.write(formatted_ast)

    emsamb = CIL_TO_MIPS()
    emsamb.visit(cil_ast)

    f_ast = emsamb.mips.compile()

    return str(f_ast)


if __name__ == "__main__":
    args = sys.argv
    if not len(args) in (3, 4):
        exit(1)
    compile_code(*args[1:])
