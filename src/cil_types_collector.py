import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILTypesCollector:
    def __init__(self, cil_ast, context):
        self.cil_ast = cil_ast
        self.context = context
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(COOL_AST.Program)
    def visit(self, node):
        for name, type in self.context.types.items():
            if name in ['ErrorType', 'SELF_TYPE']:
                continue
            
            cil_attributes = [CIL_AST.Attribute(attr) for attr in type.get_all_attributes()]
            cil_methods = [CIL_AST.Method(method, f'func_{kclass}_{method}') for kclass, method in type.get_all_methods()]
            cil_type = CIL_AST.Type(name, cil_attributes, cil_methods)
            self.cil_ast.types.append(cil_type)