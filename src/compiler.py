from sys import argv

from lexer import make_lexer
import my_parser

import type_checker
import type_builder
import type_collector

import cil_types
import cool_to_cil

import mips

tokens = ""



def main():
    args = argv
    
    cool_program_code = ""

    # Name of the file
    #p = args[2]
    p = args[1]
    print(str(p))
    if not str(p).endswith(".cl"):
        print("Cool program files must end with a \`.cl\` extension.\r\n")
        exit(1)

    if True:
        with open(str(p)) as file:
            while True:
                i = file.read(1)
                if not(i):
                    break
                if i == '\0':
                    cool_program_code += r'\0'
                else:
                    cool_program_code += i
            s = cool_program_code
            
            lexer, errors = make_lexer(cool_program_code)
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)
        
            
            ast, errors = my_parser.parse(s)
            
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)   

            #recolectar los tipos
            _type_collector = type_collector.TypeCollectorVisitor()
            _type_collector.visit(ast, errors)
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)

            #construir los tipos
            _type_builder = type_builder.TypeBuilderVisitor(_type_collector.Context)
            _type_builder.visit(ast, errors)
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)

            #chequear tipos
            _type_checker = type_checker.TypeCheckerVisitor()
            _type_checker.visit(ast, _type_builder.context, errors)
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1) 

            _cil_types = cil_types.CILTypes( _type_builder.context.Hierarchy)
            ast2 = _cil_types.visit(ast)

            
            _cool_to_cil_visitor = cool_to_cil.COOLToCILVisitor(ast2)
            cil_ast = _cool_to_cil_visitor.visit(ast)

            file_name = p[:-3] + '.mips'
            myfile = open(file_name, 'w')
            _mips = mips.VisitorMIPS()
            res = _mips.visit(cil_ast)
            myfile.write(res)  
            myfile.close()

if __name__ == "__main__":
    main()
