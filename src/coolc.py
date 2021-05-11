import re

import typer

from cmp.cil import CIL_FORMATTER, CIL_TO_MIPS, COOL_TO_CIL_VISITOR
from cmp.cool_lang.lexer import COOL_LEXER
from cmp.cool_lang.parser import COOL_PARSER
from cmp.cool_lang.semantics import COOL_CHECKER

app = typer.Typer()


@app.command()
def run(
    input_file: typer.FileText = typer.Argument(..., help="Cool file to compile."),
    output_file: typer.FileTextWrite = typer.Argument(..., help="Mips resultant file."),
    verbose: bool = typer.Option(False, help="Execute in verbose mode."),
    cil: bool = typer.Option(False, help="Compile to cil file."),
):
    code = input_file.read()

    clexer = COOL_LEXER()
    if not clexer.tokenize(code):
        for error in clexer.errors:
            print(error)
        exit(1)

    if not list(filter(lambda x: x.type != "COMMENT", clexer.result)):
        print("(0, 0) - SyntacticError: ERROR at or near EOF")
        exit(1)

    cparser = COOL_PARSER()
    if not cparser.parse(clexer):
        for error in cparser.errors:
            print(error)
        exit(1)

    program = cparser.result
    cchecker = COOL_CHECKER()
    if not cchecker.check_semantics(program, verbose=verbose):
        for error in cchecker.errors:
            print(error)
        exit(1)

    ctc = COOL_TO_CIL_VISITOR(cchecker.context)
    cil_ast = ctc.visit(program)

    if cil:
        with open(
            re.findall(r"^(.+)\.(.*)$", output_file.name)[0][0] + ".cil", "w"
        ) as out_fd:
            out_fd.write(CIL_FORMATTER().visit(cil_ast))

    ctm = CIL_TO_MIPS(cchecker.context)
    ctm.visit(cil_ast)
    mips_code = ctm.mips.compile()

    output_file.write(mips_code)

    exit(0)


if __name__ == "__main__":
    app()
