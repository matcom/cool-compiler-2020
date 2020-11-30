from lexer import CoolLexer
from utils.errors import CompilerError
from semantic.semantic import semantic_analysis
from codegen import codegen_pipeline
from cool_parser import CoolParser
from ply.lex import LexToken
import sys

def run_pipeline(input_, outpt):
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
        if errors:
            for err in errors:
                print(err)
            raise Exception()
        else:
            mips_code = codegen_pipeline(context, ast, scope, debug=False)
            with open(outpt, 'w+') as f:
                f.write(mips_code)

    except FileNotFoundError:
        error_text = CompilerError.UNKNOWN_FILE % input_
        print(CompilerError(error_text, 0, 0))

if __name__ == "__main__":
    input_ = sys.argv[1]
    output_ = sys.argv[2]
    # print(input_)
    # input_ = f'hello_world.cl' 
    # output_ = 'test.mips'
    run_pipeline(input_, output_)