from lexer import make_lexer
from parser import make_parser
from semantic import check_semantic
from cil_generator import generate_cil
from mips_generator import generate_mips
import sys


def main():
    cool_program_code = ""

    # se comprueba primero el fichero de entrada
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

    # se hace una primera pasada por el texto de entrada para poner los \0 en \\0
    # para que puedan ser notados por el lexer ... asi mismo se hace con los \t para
    # que puedan ser cambiados por la correspondiente cantidad de espacios en blanco
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

        new_data = ""

        # se ponen en blanco los comentarios multilinea
        i = 0
        while i < len(data):
            if data[i] == '(' and i < len(data) - 1 and data[i + 1] == '*':
                counter = 0
                j = i + 2
                new_data += "  "
                paster = ""
                matched = False
                while j < len(data) - 1:
                    if data[j] == '(' and data[j + 1] == '*':
                        counter += 1
                        j += 2
                        new_data += "  "
                        continue
                    if data[j] == '*' and data[j + 1] == ')':
                        new_data += "  "
                        if counter == 0:
                            matched = True
                            break
                        else:
                            counter -= 1
                    if data[j] == '\n':
                        paster += "\n"
                    j += 1
                    new_data += " "
                if matched:
                    new_data += paster
                    i = j + 2
                    continue
            new_data += data[i]
            i += 1

        s = new_data

        lexer, errors = make_lexer(s)

        # se imprimen los errores del lexer
        if len(errors) > 0:
            for er in errors:
                print(er)
            exit(1)

        ast, errors = make_parser(s)

        # se imprimen ls errores del parser
        if len(errors) > 0:
            for er in errors:
                print(er)
            exit(1)

        errors, types = check_semantic(ast)

        # se imprimen los errores en el chequeo semantico
        if len(errors) > 0:
            for er in errors:
                print(er)
            exit(1)

        cil = generate_cil(types)

        mips = generate_mips(cil)

        # se crea el archivo mips correspondiente y se guarda el codigo generado
        with open(p[:-2] + "mips", "w") as p:
            p.write(mips)


if __name__ == "__main__":
    main()
