from Files_from_TypeInferencer.core.cmp.CoolUtils import tokenize_text, CoolParser
from missing_files import lexer

def main(args):
    # Read code
    try:
        with open(args.file, 'w') as fd:
            code = fd.read()
    except:
        print(f"(0,0) - CompilerError: file {args.file} not found") #TODO: Customize errors
        exit(1)

    # Lexer
    text = lexer(code)

    # Tokenize
    tokens = tokenize_text(text)
    
    # Parse
    parse, (failure, token) = CoolParser([t.token_type for t in tokens])
    if failure:
        print(f"(0,0) - SemanticError: Unexpected token {token}") #TODO: Use correct line and column
        exit(1)

    # Comming soon pipeline steps
    print(parse)


    exit(0)


if __name__ == "__main__":
    import argparse 

    parser = argparse.ArgumentParser(description='CoolCompiler pipeline')
    parser.add_argument('-f', '--file', type=str, default='code.cl', help='node address')

    args = parser.parse_args()
    main(args)

