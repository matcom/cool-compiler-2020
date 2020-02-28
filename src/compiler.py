import argparse
from sys import argv

from lexer import make_lexer
from parser import make_parser

tokens = ""


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
    if not str(p).endswith(".cl"):
        print("Cool program files must end with a \`.cl\` extension.\r\n")
        arg_parser.print_usage()
        exit(1)

    try:
        with open(str(p)) as file:
            while True:
                i = file.read(1)
                if not(i):
                    break
                if i == '\0':
                    cool_program_code += r'\0'
                else:
                    cool_program_code += i

            # lexer, errors = make_lexer(cool_program_code)
            # print(len(errors))
            # if len(errors) > 0:
            #     for er in errors:
            #         print(er)
            #     exit(1)
            make_parser(cool_program_code)

    except (IOError, FileNotFoundError):
        print(f"Error! File {program} not found.")
        exit(1)
    except Exception:
        print("An unexpected error occurred!")
        exit(1)


if __name__ == "__main__":
    main()
