from cil_types_collector import CILTypesCollector
from cil_data_collector import CILDataCollector
from cil_code_builder import CILCodeBuilder

if __name__ == '__main__':
    import sys
    from cparser import Parser

    parser = Parser()

    if len(sys.argv) > 1:

        input_file = sys.argv[1]
        with open(input_file, encoding="utf-8") as file:
            cool_program_code = file.read()

        cool_ast = parser.parse(cool_program_code)

        if parser.errors:
            print(parser.errors[0])
            exit(1)

        # semantic_analyzer = SemanticAnalyzer(cool_ast)
        # semantic_analyzer.analyze()

        # for e in semantic_analyzer.errors:
        #     print(e)
        #     exit(1)
        
        build_cil_ast(cool_ast)

def build_cil_ast(cool_ast):
    cil_types_collector = CILTypesCollector() 
    cil_data_collector = CILDataCollector() 
    cil_code_builder = CILCodeBuilder()