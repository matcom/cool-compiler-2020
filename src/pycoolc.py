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
        # Tratar los \t en el programa como 4 espacios por comodidad
        # a la hora de reportar errores de fila y columna
        program = program.replace('\t', ' ' * 4)
    except AssertionError as e:
        print(e)
        sys.exit(1)

    # El programa no contiene comentarios en esta fase
    # por lo que es seguro pasarselo al LEXER
    try:
        tokens = LEXER(program)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Parsear los tokens para obtener un arbol de derivacion
    try:
        parse = PARSER(tokens)
    except Exception as e:
        print(e)
        sys.exit(1)
    # Construir el AST a partir del arbol de derivacion obtenido
    try:
        ast = evaluate_right_parse(parse, tokens[:-1])
    except Exception as e:
        print(e)
        sys.exit(1)
    ########################
    # Empezar los visitors #
    ########################

    # Ejecutar los visitors que recolectan los tipos,
    # los crean y luego realizan un chequeo semantico
    # sobre el programa y la inferencia de tipos
    errors, context, scope = ast.check_semantics(deep)
    if errors:
        report(errors)
        sys.exit(1)

    # Correr el visitor que transforma el AST de COOL
    # en un AST de CIL
    cil_visitor = CoolToCILVisitor(context)
    try:
        cil_program = cil_visitor.visit(ast, scope)
    except Exception as e:
        print(e)
        sys.exit(1)

    assert isinstance(cil_program, CilProgramNode)

    # Convertir el AST de CIL en instrucciones de MIPS
    code_gen = MipsCodeGenerator()

    # Obtener la representacion en str de las instrucciones
    # en MIPS
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
