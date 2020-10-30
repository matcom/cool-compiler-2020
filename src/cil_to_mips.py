from cil_types_collector import CILTypesCollector
from cil_data_collector import CILDataCollector
from cil_code_builder import CILCodeBuilder
from semantic import Scope, VariableInfo
import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILToMIPSVisitor():
    @visitor.on('node')
    def visit(self, node):
        pass
    

if __name__ == '__main__':
    import sys
    from cparser import Parser
    from semantic_analyzer import SemanticAnalyzer
    from cool_to_cil import MiniCOOLToCILVisitor

    parser = Parser()

    sys.argv.append('test.cl')

    if len(sys.argv) > 1:

        input_file = sys.argv[1]
        with open(input_file, encoding="utf-8") as file:
            cool_program_code = file.read()

        cool_ast = parser.parse(cool_program_code)

        if parser.errors:
            print(parser.errors)
        
        if parser.errors:
            exit(1)

        semantic_analyzer = SemanticAnalyzer(cool_ast)
        context, scope = semantic_analyzer.analyze()

        for e in semantic_analyzer.errors:
            print(e)

        if semantic_analyzer.errors:    
            exit(1)
        
        cool_to_cil = MiniCOOLToCILVisitor(context)
        cil_ast = cool_to_cil.visit(cool_ast, scope)
        
        # formatter = CIL_AST.get_formatter()
        # print(formatter(cil_ast))

        cil_to_mips = CILToMIPSVisitor()
        mips_code = cil_to_mips.(cil_ast)
       
        with open(f'{sys.argv[1][:-3]}.asm', 'w') as f:
            f.write(f'{mips_code}')