from codegen.visitors.cil_visitor import COOLToCILVisitor
from codegen.visitors.cil_format_visitor import get_formatter
from codegen.visitors.mips_visitor import CILToMIPSVistor


def codegen_pipeline(context, ast, scope):
    print('============= TRANSFORMING TO CIL =============')
    cool_to_cil = COOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)
    formatter = get_formatter()
    print(formatter(cil_ast))
    data_code, text_code = CILToMIPSVistor().visit(cil_ast)
    save_code(data_code, text_code)
    return ast, context, scope, cil_ast

def save_code(data_code, text_code):
    text = '\n'.join(text_code) + '\n' + '\n'.join(data_code)
    print(text)
    with open('test.asm', 'w+') as fd:
        fd.write(text)