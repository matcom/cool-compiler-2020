import argparse

def create_arg_parser():
    arg_parser = argparse.ArgumentParser(prog="pycoolc")

    arg_parser.add_argument(
        "cool_program",
        type=str, nargs="1",
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

    if not str(program).endswith(".cl"):
        print("Cool program files must end with a \`.cl\` extension.\r\n")
        arg_parser.print_usage()
        exit(1)

    try:
        with open(program, encoding="utf-8") as file:
            cool_program_code += file.read()
    except (IOError, FileNotFoundError):
        print(f"Error! File {program} not found.")
    except Exception:
        print("An unexpected error occurred!")

    if args.tokens:
        print("Run lexical analysis") if args.debug else None

    if args.ast:
        print("Getting ast") if args.debug else None

    if args.semantics:
        print("Running Semantic Analysis") if args.debug else None


if __name__ == "__main__":
    main()

