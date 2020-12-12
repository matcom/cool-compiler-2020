from lexer import make_lexer
from parser import make_parser
from semantic import check_semantic
from cil_generator import generate_cil
from mips_generator import generate_mips
import sys


def main():
    cool_program_code = ""

    if len(sys.argv) < 2:
        print('Must contains cool file')
        exit(1)

    p = sys.argv[1]
    current = ''
    index = 0
    while True:
        if str(current).endswith(".cl"):
            p = current
            break
        if index > len(p):
            print("Cool program files must end with a \`.cl\` extension.\r\n")
            exit(1)
            break
        current += p[index]
        index += 1

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

        cil = generate_cil(types)

        mips = generate_mips(cil)

        with open(p[:-2] + "mips", "w") as p:
            p.write(mips)


if __name__ == "__main__":
    main()
