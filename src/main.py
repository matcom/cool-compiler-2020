from pipeline import Pipeline
from tools.reader import Reader
from cl_lexer import CoolLexer
from cl_parser import CoolParser
from visitors import *

import sys

def main():
    program = sys.argv[1]

    # out_program = sys.argv[2]

    # mkdir(out_program, mode=0o777, *, dir_fd=None)

    # fd = open(out_program, 'rw')
    
    pipeline = Pipeline()

    pipeline.submit_state(Reader('Reader'))
    pipeline.submit_state(CoolParser('Parser'))
    pipeline.submit_state(TypeCollector('TCollector'))
    pipeline.submit_state(TypeBuilder('TBuilder'))
    pipeline.submit_state(VarCollector('VCollector'))
    pipeline.submit_state(TypeChecker('TChecker'))

    ast, context, scope = None, None, None
    #temporal
    try:
        ast, context, scope = pipeline.run_pipeline(program)
    except:
        pass
    
    pipeline.report_errors()

    if pipeline.pipeline_errors:
        exit(1)
    else:
        # print('-------------AST-------------')
        # for x in ast:
        #     print(x)

        cv = codeVisitor(context)
        cil_ast = cv.visit(ast, None, scope)
        # f2_n = program[:-3] + '_test.cil'
        # f2 = open(f2_n, 'w+')

        # formatter = get_formatter()
        # cil_code = formatter(cil_ast)
        # f2.write(f'{cil_code}')
        # f2.close()
        # print('LEN:::::',len(cv.instructions))
        mips = MIPS()
        code = mips.visit(cil_ast)

        # for c in cv.data:
        #     print(str(c))
        # for c in cv.code:
        #     print(str(c))

        path = program[:-2]
        # path = path[:-1]
        path += 'mips'
        # print(path)
        f = open(path, "w+")
        f.write(code)

        # except:
        #     pass

    

    # print('-------------------Done mips-------------------------------')
    # for line in code:
    #     print(code)
# except:
#     pass


if __name__ == "__main__":
    main()