from semantic import Scope, VariableInfo
import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILToMIPSVisitor():
    def __init__(self):
        self.mips_code = ''
        self.mips_comm_for_binary_op = {
            '+' : 'add',
            '-' : 'sub',
            '*' : 'mul',
            '/' : 'div'
        }

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(CIL_AST.Program)
    def visit(self, node):
        for node_type in node.dottypes.values():
            self.visit(node_type)
        
        # Write MIPS for node.dotdata

        for node_function in node.dotcode:
            self.visit(node_function)
        
        return self.mips_code.strip()
    
    @visitor.when(CIL_AST.Function)
    def visit(self, node):
        for param_node in params:
            self.visit(param_node)
        
        for local_node in localvars:
            self.visit(local_node)
        
        for instruction in instructions:
            self.visit(instruction)
    
    @visitor.when(CIL_AST.BinaryOperator)
    def visit(self, node):
        mips_comm = self.mips_comm_for_binary_op[node.op]
        self.visit(left)
        self.mips_code += 'sw $a0, 0(sp)\n'
        self.mips_code += 'addiu $sp, $sp, -4\n'
        self.visit(right)
        self.mips_code += 'lw $t1, 4($sp)\n'
        self.mips_code += f'{mips_comm} $a0, $t1, $a0\n'
        self.mips_code += 'addiu $sp, $sp, 4\n'
    
    @visitor.when(CIL_AST.INTEGER)
    def visit(self, node):
        self.mips_code += f'li $a0, {node.value}\n'

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
        mips_code = cil_to_mips.visit(cil_ast)
       
        with open(f'{sys.argv[1][:-3]}.asm', 'w') as f:
            f.write(f'{mips_code}')