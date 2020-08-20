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
from core.cmp.cool_to_cil import COOLToCILVisitor


def main(args):
    # Read code
    try:
        with open(args.file, 'r') as fd:
            code = fd.read()
    except:
        print(f"(0,0) - CompilerError: file {args.file} not found")
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
        print(f"({token.row},{token.column}) - SyntacticError: Unexpected token {token.lex}")
        exit(1)

    # AST
    parse, operations = parsedData
    ast = evaluate_reverse_parse(parse, operations, tokens)
    errors = []

    # Collect user types
    collector = TypeCollector()
    collector.visit(ast)
    context = collector.context
    errors.extend(collector.errors)

    # Building types
    builder = TypeBuilder(context)
    builder.visit(ast)
    errors.extend(builder.errors)

    # Checking types
    inferencer = InferenceVisitor(context)
    while inferencer.visit(ast)[0]: pass
    inferencer.errors.clear()
    _, scope = inferencer.visit(ast)
    errors.extend(inferencer.errors)
    
    if errors:
        for (msg, token) in errors:
            print(f"({token.row},{token.column}) - SemanticError: {msg}")
        exit(1)
    # else:
    #     print(FormatVisitor().visit(ast))

    #CIL Transformation
    cool_to_cil = COOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)
    #formatter = get_formatter()
    #ast_cil = formatter(cil_ast)
    #print(ast_cil)
    
    exit(0)


if __name__ == "__main__":
    import argparse 

    parser = argparse.ArgumentParser(description='CoolCompiler pipeline')
    parser.add_argument('-f', '--file', type=str, default='code.cl', help='node address')

    args = parser.parse_args()
    main(args)

    # test()
