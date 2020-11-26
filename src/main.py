from lexer import CoolLexer
from utils.errors import CompilerError
from semantic.semantic import semantic_analysis
from codegen import codegen_pipeline
from cool_parser import CoolParser
from ply.lex import LexToken
import sys

def run_pipeline(input):
    try:
        with open(input_) as f:
            text = f.read()

        lexer = CoolLexer()
        tokens = lexer.run(text)

        p = CoolParser(lexer)

        ast = p.parse(text, debug=True)
        if p.errors:
            raise Exception()
        
        ast, errors, context, scope = semantic_analysis(ast, debug=False)
        # if errors:
        #     for err in errors:
        #         print(err)
        #     raise Exception()
        # else:
        ast, context, scope, cil_ast = codegen_pipeline(context, ast, scope, debug=True)

    except FileNotFoundError:
        error_text = CompilerError.UNKNOWN_FILE % input_
        print(CompilerError(error_text, 0, 0))


if __name__ == "__main__":
    # input_ = sys.argv[1]
    # print(input_)
    input_ = f'test1.cl' 
    # output_ = args.output
    run_pipeline(input_)