from sys import exit
from pprint import pprint
from core.cmp.visitors import *
from core.cmp.lex import CoolLexer
from core.cmp.evaluation import evaluate_reverse_parse
from core.cmp.CoolUtils import tokenize_text, CoolParser
from core.cmp.lex import CoolLexer
from core.cmp.evaluation import *
from core.cmp.cil import get_formatter
from pprint import pprint


def main(args):
    # Read code
    try:
        with open(args.file, 'r') as fd:
            code = fd.read()
    except:
        print(f"(0,0) - CompilerError: file {args.file} not found") #//TODO: Customize errors
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
            print(token.lex)
    
    if lexer_err:
        exit(1)

    # Parse
    parsedData, (failure, token) = CoolParser(tokens, get_shift_reduce=True)
    
    if failure:
        print(f"({token.row},{token.column}) - SyntacticError: Unexpected token {token}") #//TODO: Use correct line and column
        exit(1)

    # AST
    parse, operations = parsedData
    ast = evaluate_reverse_parse(parse, operations, tokens)

    # Collect user types
    collector = TypeCollector()
    collector.visit(ast)
    context = collector.context

    if collector.errors:
        # Display errors
        print('Collector have errors!!')

    # Building types
    builder = TypeBuilder(context)
    builder.visit(ast)

    if builder.errors:
        # Display errors
        print('Builder have errors!!')

    # Checking types
    checker = TypeChecker(context)
    scope = checker.visit(ast)

    if checker.errors:
        # Display errors
        print('Checker have errors!!')

    # Infering types
    inferer = InferenceVisitor(context)
    while True:
        old = scope.count_auto()
        scope = inferer.visit(ast)
        if old == scope.count_auto():
            break
    inferer.errors.clear()
    scope = inferer.visit(ast)

    if inferer.errors:
        # Display errors
        print('Inferer have errors!!')

    #CIL Transformation
    cool_to_cil = COOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)
    formatter = get_formatter()
    ast_cil = formatter(cil_ast)
    print(ast_cil)
    #Write cil to a source file

    exit(0)


if __name__ == "__main__":
    import argparse 

    parser = argparse.ArgumentParser(description='CoolCompiler pipeline')
    parser.add_argument('-f', '--file', type=str, default='code.cl', help='node address')

    args = parser.parse_args()
    main(args)

