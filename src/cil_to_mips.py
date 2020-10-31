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
        self.stack_values = []
        self.current_function = None

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
        for param_node in node.params.reverse():
            self.visit(param_node)
        
        for local_node in node.localvars:
            self.visit(local_node)
        
        for instruction in node.instructions:
            self.visit(instruction)
        
        self.stack_values = []
    
    @visitor.when(Allocate)
    def visit(self, node):
        self.mips_code += f'lw $a0, {node.type}'
        # main = "lw $a0, {}\nli $v0, 9\nsyscall\nla $t1, {}\nmove $t0, $v0\nsw $t1, ($t0)\n".format(node.type, node.type)
        # return main

    @visitor.when(CIL_AST.ParamDec)
    def visit(self, node):
        self.stack_values.append(node.name)

    @visitor.when(CIL_AST.LocalDec)
    def visit(self, node):
        self.stack_values.append(node.name)

    @visitor.when(CIL_AST.LocalDec)
    def visit(self, node):
        self.locals.append(node.name)

    @visitor.when(CIL_AST.BinaryOperator)
    def visit(self, node):
        mips_comm = self.mips_comm_for_binary_op[node.op]
        self.visit(node.left)
        self.mips_code += 'sw $a0, 0(sp)\n'
        self.mips_code += 'addiu $sp, $sp, -4\n'
        self.visit(node.right)
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
        
        formatter = CIL_AST.get_formatter()
        cil_code = formatter(cil_ast)

        with open(f'{sys.argv[1][:-3]}.cil', 'w') as f:
            f.write(f'{cil_code}')

        cil_to_mips = CILToMIPSVisitor()
        mips_code = cil_to_mips.visit(cil_ast)
       
        with open(f'{sys.argv[1][:-3]}.asm', 'w') as f:
            f.write(f'{mips_code}')