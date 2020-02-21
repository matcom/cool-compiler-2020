import lexer
import sys


if __name__ == "__main__":
    cool_lexer = lexer.Cool_Lexer()
    cool_lexer.build()

    input_file = sys.argv[1]
    # input_file = 'comment1.cl'
    input_file = open(input_file)
    data = ''

    while True:
        data_readed = input_file.read(1024)
        if not data_readed:
            break
        data += data_readed

    cool_lexer.lexer.input(data)

    for token in cool_lexer.lexer:
        if token.type == 'error' or token.type == 'eof':
            print(token.value)
            exit(1)




