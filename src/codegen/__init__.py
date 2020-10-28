from codegen.visitors.cil_visitor import COOLToCILVisitor
from codegen.visitors.cil_format_visitor import get_formatter

def codegen_pipeline(context, ast, scope):
    print('============= TRANSFORMING TO CIL =============')
    cool_to_cil = COOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)
    formatter = get_formatter()
    print(formatter(cil_ast))
    return ast, context, scope, cil_ast