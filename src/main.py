from sys import exit
from core.cmp.CoolUtils import tokenize_text, CoolParser
from core.cmp.lex import CoolLexer
from pprint import pprint


def main(args):
    # Read code
    try:
        with open(args.file, 'r') as fd:
            code = fd.read()
    except:
        print(f"(0,0) - CompilerError: file {args.file} not found") #TODO: Customize errors
        exit(1)

    # Lexer
    lexer = CoolLexer()
    
    # Tokenize
    tokens = lexer.tokenize(code)

    if len(tokens) == 1 and tokens[0].lex == '$':
        print("(0, 0) - SyntacticError: Unexpected token EOF") 
        exit(1)

    lexer_err = False
    for token in tokens:
        if token.token_type == "ERROR":
            lexer_err = True
    
    if lexer_err:
        exit(1)

    # Parse
    parse, (failure, token) = CoolParser(tokens)
    
    if failure:
        print(f"({token.row},{token.column}) - SyntacticError: Unexpected token {token}") #TODO: Use correct line and column
        exit(1)

    # Comming soon pipeline steps
    #print(parse)


    exit(0)


if __name__ == "__main__":
    import argparse 

    parser = argparse.ArgumentParser(description='CoolCompiler pipeline')
    parser.add_argument('-f', '--file', type=str, default='code.cl', help='node address')

    args = parser.parse_args()
    main(args)

