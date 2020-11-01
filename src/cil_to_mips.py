from semantic import Scope, VariableInfo
import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILToMIPSVisitor():
    def __init__(self):
        self.mips_code = ''
        self.text = ''
        self.data = ''
        self.mips_comm_for_binary_op = {
            '+' : 'add',
            '-' : 'sub',
            '*' : 'mul',
            '/' : 'div'
        }
        self.current_function = None

    def search_local_offset(self, name):
        for i, local in enumerate(self.current_function.locals):
            if local.name == name:
                return (len(self.current_function.locals) - i)*4

    def search_param_offset(self, name):
        for i, local in enumerate(self.current_function.params):
            if local.name == name:
                return (i + 1)*4

    def is_param(self, name):
        return name in self.current_function.params
        

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
        self.current_function = node

        self.text += f'{node.name}:/n'
        self.text += f'move $fp $sp/n'  #save frame pointer of current function
        
        for local_node in node.localvars: #save space for locals 
            self.visit(local_node)
        
        self.text += 'addi $sp, $sp, -4\n' # save return address
        self.text += 'sw $ra, 0($sp)\n'

        for instruction in node.instructions:
            self.visit(instruction)
        
        self.text += 'lw $ra, 0($sp)\n'  #recover return address
        total = 4 * len(node.locals) + 4 * len(node.params) + 8 
        self.text += f'addi $sp, $sp, {total}\n' #pop locals,parameters,return address and caller fp from the stack
        self.text += 'lw $fp, 0($sp)\n' # recover caller function frame pointer
        self.text += 'jr $ra\n' 

    
    @visitor.when(Allocate)
    def visit(self, node):
        self.mips_code += f'lw $a0, {node.type}'
        # main = "lw $a0, {}\nli $v0, 9\nsyscall\nla $t1, {}\nmove $t0, $v0\nsw $t1, ($t0)\n".format(node.type, node.type)
        # return main

    @visitor.when(CIL_AST.ParamDec)
    def visit(self, node):
        pass

    @visitor.when(CIL_AST.LocalDec)
    def visit(self, node):
        self.text += 'addi $sp, $sp, -4\n'
        self.text += 'sw $zero, 0($sp)\n'


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
