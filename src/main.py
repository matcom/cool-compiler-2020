from pipeline import Pipeline
from tools.reader import Reader
from cl_lexer import CoolLexer
from cl_parser import CoolParser
from visitors import *

import sys

def main():
    program = sys.argv[1]
    
    pipeline = Pipeline()

    pipeline.submit_state(Reader('Reader'))
    pipeline.submit_state(CoolParser('Parser'))
    pipeline.submit_state(TypeCollector('TCollector'))
    pipeline.submit_state(TypeBuilder('TBuilder'))
    pipeline.submit_state(VarCollector('VCollector'))
    pipeline.submit_state(TypeChecker('TChecker'))

    ast, context, scope = None, None, None
    try:
        ast, context, scope = pipeline.run_pipeline(program)
    except:
        pass
    
    pipeline.report_errors()

    if pipeline.pipeline_errors:
        exit(1)
    else:
        cv = codeVisitor(context)
        cil_ast = cv.visit(ast, None, scope)
        
        mips = MIPS()
        code = mips.visit(cil_ast)
        path = program[:-2]
        path += 'mips'
        f = open(path, "w+")
        f.write(code)

if __name__ == "__main__":
    main()