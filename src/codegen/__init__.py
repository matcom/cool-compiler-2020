from codegen.visitors.cil_visitor import COOLToCILVisitor
from codegen.visitors.cil_format_visitor import get_formatter
from codegen.visitors.mips_visitor import CILToMIPSVistor
from pprint import pprint

def codegen_pipeline(context, ast, scope, debug=False):
    if debug:
        print('============= TRANSFORMING TO CIL =============')
    cool_to_cil = COOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)
    if debug:
        formatter = get_formatter()
        print(formatter(cil_ast))
    inherit_graph = context.build_inheritance_graph()
    # pprint(inherit_graph)
    data_code, text_code = CILToMIPSVistor(inherit_graph).visit(cil_ast)
    return get_code(data_code, text_code, debug)

def get_code(data_code, text_code, debug):
    text = '\n'.join(text_code) + '\n' + '\n'.join(data_code)
    if debug:
        print(text)
        with open('test.asm', 'w+') as fd:
            fd.write(text)
    return text