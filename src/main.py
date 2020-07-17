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
    pipeline.submit_state(FormatVisitor('Formatter', './ast.txt'))
    pipeline.submit_state(TypeCollector('TCollector'))
    pipeline.submit_state(TypeBuilder('TBuilder'))
    pipeline.submit_state(VarCollector('VCollector'))
    #pipeline.submit_state(TypeChecker('TChecker'))

    ast, context, scope = pipeline.run_pipeline(program)
    print(context)
    print('-'*25)
    print(scope)
    
    pipeline.report_errors()

    if pipeline.pipeline_errors:
        exit(1)
 
if __name__ == "__main__":
    main()