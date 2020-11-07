from codegen.visitors.cil_visitor import COOLToCILVisitor
from codegen.visitors.cil_format_visitor import get_formatter
from codegen.visitors.mips_visitor import CILToMIPSVistor


def codegen_pipeline(context, ast, scope):
    print('============= TRANSFORMING TO CIL =============')
    cool_to_cil = COOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)
    formatter = get_formatter()
    cil_to_mips = CILToMIPSVistor().visit(cil_ast)
    print(formatter(cil_ast))
    return ast, context, scope, cil_ast