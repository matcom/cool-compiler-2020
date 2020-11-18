import argparse
from lexer import make_lexer
from parser import make_parser
from semantic import check_semantic
from code_generation import generate_code


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

    #try:
    with open(str(p)) as file:
        while True:
            i = file.read(1)
            if not i:
                break
            if i == '\0':
                cool_program_code += r'\0'
                continue
            else:
                if i == "\t":
                    cool_program_code += "    "
                    continue
                cool_program_code += i
            
        data = cool_program_code

        newData = ""

        i = 0
        while i < len(data):
            if data[i] == '(' and i < len(data) - 1 and data[i + 1] == '*':
                counter = 0
                j = i + 2
                newData += "  "
                paster = ""
                matched = False
                while j < len(data) - 1:
                    if data[j] == '(' and data[j + 1] == '*':
                        counter += 1
                        j += 2
                        newData += "  "
                        continue
                    if data[j] == '*' and data[j + 1] == ')':
                        newData += "  "
                        if counter == 0:
                            matched = True
                            break
                        else:
                            counter -= 1
                    if data[j] == '\n':
                        paster += "\n"
                    j += 1
                    newData += " "
                if matched:
                    newData += paster
                    i = j + 2
                    continue
            newData += data[i]
            i += 1

        s = newData
        
        lexer, errors = make_lexer(s)

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
               
        errors, types = check_semantic(ast)

        # Print semantic errors
        if len(errors) > 0:
            for er in errors:
                print(er)
            exit(1)

        #cil, mips = generate_code(types)
        cil = generate_code(types)

        #print(cil)

    #except (IOError, FileNotFoundError):
    #    print(f"Error! File {program} not found.")
    #    exit(1)
    #except Exception as e:
    #    print(f'An unexpected error occurred! {e}')
    #    exit(1)


if __name__ == "__main__":
    main()
