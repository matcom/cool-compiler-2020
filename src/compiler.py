import argparse
from lexer import make_lexer
from parser import make_parser
from semantic import check_semantic

from visitor import *

def create_arg_parser():
    arg_parser = argparse.ArgumentParser(prog="pycoolc")

    arg_parser.add_argument(
        "cool_program",
        type=str, nargs="+",
        help="One cool program source code file ending with *.cl extension.")

    arg_parser.add_argument(
        "-o", "--outfile",
        type=str, action="store", nargs=1, default=None,
        help="Output program name.")

    arg_parser.add_argument(
        "--tokens",
        action="store_true", default=False,
        help="Displays tokens.")

    arg_parser.add_argument(
        "--ast",
        action="store_true", default=False,
        help="Displays ast.")

    arg_parser.add_argument(
        "--semantics",
        action="store_true", default=False,
        help="Displays semantic analysis.")

    arg_parser.add_argument(
        "--debug",
        action="store_true", default=False,
        help="Debug sections.")

    return arg_parser


def main():
    arg_parser = create_arg_parser()

    args = arg_parser.parse_args()
    program = args.cool_program

    cool_program_code = ""

    p = program[0]
    if '\r' == p[-1:]:
        p = p[:-1]
    if not str(p).endswith(".cl"):
        print("Cool program files must end with a \`.cl\` extension.\r\n")
        arg_parser.print_usage()
        exit(1)

    try:
        with open(str(p)) as file:
            while True:
                i = file.read(1)
                if not i:
                    break
                if i == '\0':
                    cool_program_code += r'\0'
                else:
                    cool_program_code += i
            s = cool_program_code
            
            lexer, errors = make_lexer(cool_program_code)

            # Print lexer errors
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)

            ast, errors = make_parser(s)

            # Print parser errors
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)

            formatter = FormatVisitor()
            tree = formatter.visit(ast)
            print(tree)

            #errors = check_semantic(ast)
            # Print semantic errors
            #if len(errors) > 0:
            #    for er in errors:
            #        print(er)
            #    exit(1)

    except (IOError, FileNotFoundError):
        print(f"Error! File {program} not found.")
        exit(1)
    except Exception as e:
        print(f'An unexpected error occurred! {e}')
        exit(1)


if __name__ == "__main__":
    main()
