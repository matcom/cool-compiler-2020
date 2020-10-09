from cil_types_collector import CILTypesCollector
from cil_data_collector import CILDataCollector
from cil_code_builder import CILCodeBuilder

import cil_ast_nodes as CIL_AST

def build_cil_ast(cool_ast, context):
    cil_ast = CIL_AST.Program()
    
    cil_types_collector = CILTypesCollector(cil_ast, context)
    cil_types_collector.visit(cool_ast)

    # cil_data_collector = CILDataCollector(cil_ast, context) 
    # cil_data_collector.visit(cool_ast)
    
    # cil_code_builder = CILCodeBuilder(cil_ast, context)
    # cil_code_builder.visit(cool_ast)

    return cil_ast

if __name__ == '__main__':
    import sys
    from cparser import Parser
    from semantic_analyzer import SemanticAnalyzer

    parser = Parser()

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
        context = semantic_analyzer.analyze()

        for e in semantic_analyzer.errors:
            print(e)

        if semantic_analyzer.errors:    
            exit(1)
        
        cil_ast = build_cil_ast(cool_ast, context)

        print(cil_ast)
        with open(f'{sys.argv[1][:-3]}.cil', 'w'): pass
        with open(f'{sys.argv[1][:-3]}.cil', 'a') as f:
            f.write(f'{cil_ast}')