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
        self.types = None

    def search_var_offset(self, name):
        for i, local in enumerate(self.current_function.localvars + self.current_function.params):
            if local.name == name:
                return (i + 1)*4


    def search_attr_offset(self,type_name, attr_name):
        for i, attr in enumerate(self.types[type_name].attributes):
            if attr == attr_name:
                return i * 4
                
    def search_method_offset(self, type_name, method_name):
        for i, method in enumerate(self.types[type_name].methods):
            if method == method_name:
                return i*4

    def is_param(self, name):
        return name in self.current_function.params
        

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(CIL_AST.Program)
    def visit(self, node):
        self.types = node.dottypes

        for node_type in node.dottypes.values():
            self.visit(node_type)
        
        for node_data in node.dotdata.keys():
            self.data += f'{node_data}: .asciiz "{node.dotdata[node_data]}"\n'

        for node_function in node.dotcode:
            self.visit(node_function)
        
        self.mips_code = '.data\n' + self.data + '.text\n' + self.text 
        return self.mips_code.strip()
    
    @visitor.when(CIL_AST.Function)
    def visit(self, node):
        self.current_function = node

        self.text += f'{node.name}:\n'
        # self.text += f'move $fp, $sp\n'  #save frame pointer of current function
        
        for local_node in reversed(node.localvars): #save space for locals 
            self.visit(local_node)
        
        self.text += 'addi $sp, $sp, -4\n' # save return address
        self.text += 'sw $ra, 0($sp)\n'

        for instruction in node.instructions:
            self.visit(instruction)
        
        self.text += 'lw $ra, 0($sp)\n'  #recover return address
        total = 4 * len(node.localvars) + 4 * len(node.params) + 4
        self.text += f'addi $sp, $sp, {total}\n' #pop locals,parameters,return address from the stack
        # self.text += 'lw $fp, 0($sp)\n' # recover caller function frame pointer
        self.text += 'jr $ra\n' 

    @visitor.when(CIL_AST.Type)
    def visit(self, node):
        self.data += f'{node.name}_name: .asciiz "{node.name}"\n'
        self.data += f'{node.name}_methods:\n'
        for method in node.methods.values():
            self.data += f'.word {method}\n'
        
    @visitor.when(CIL_AST.Assign)
    def visit(self, node):
        offset = self.search_var_offset(node.local_dest)
        
        if isinstance(node.right_expr, int):
            self.text += f'li $t1, {node.right_expr}\n'
        else:
            right_offset = self.search_var_offset(node.right_expr)
            self.text += f'lw $t1, {right_offset}($sp)\n'

        self.text += f'sw $t1, {offset}($sp)\n'


    @visitor.when(CIL_AST.Allocate)
    def visit(self, node):
        amount = len(self.types[node.type].attributes) + 3
        self.text += f'li $a0, {amount}\n' 
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += f'move $t0, $v0\n'
        
        #Initialize Object Layout
        self.text += f'la $t1, {node.type}_name\n' #tag
        self.text += f'sw $t1, 0($t0)\n'
        self.text += f'li $t1, {amount}\n' #size
        self.text += f'sw $t1, 4($t0)\n'
        self.text += f'la $t1, {node.type}_methods\n' #methods pointer
        self.text += f'sw $t1, 8($t0)\n'

        offset = self.search_var_offset(node.local_dest)
        self.text += f'sw $t0, {offset}($sp)\n'  #store instance address in local

    @visitor.when(CIL_AST.ParamDec)
    def visit(self, node):
        pass

    @visitor.when(CIL_AST.LocalDec)
    def visit(self, node):
        self.text += 'addi $sp, $sp, -4\n'
        self.text += 'sw $zero, 0($sp)\n'

    @visitor.when(CIL_AST.GetAttr)
    def visit(self, node):
        self_offset = self.search_var_offset(node.instance)
        self.text += f'lw $t0, {self_offset}($sp)\n'  #get self address
        
        attr_offset = self.search_attr_offset(node.static_type, node.attr)
        self.text += f'lw $t1, {attr_offset}($t0)\n'  #get attribute
        
        result_offset = self.search_var_offset(node.local_dest)
        self.text += f'sw $t1, {result_offset}($sp)\n' #store attribute in local

    @visitor.when(CIL_AST.SetAttr)
    def visit(self, node):
        self_offset = self.search_var_offset(node.instance)
        self.text += f'lw $t0, {self_offset}($sp)\n'  #get self address

        if node.value:
            value_offset = self.search_var_offset(
                node.value)  # get value from local
            self.text += f'lw $t1, {value_offset}($sp)\n'
        else:
            self.text += f'lw $t1, $zero\n'  # not initialized attribute
            
        attr_offset = self.search_attr_offset(node.static_type, node.attr)
        self.text += f'sw $t1, {attr_offset}($t0)\n' #set attribute in instance


    @visitor.when(CIL_AST.Arg)
    def visit(self, node):
        value_offset = self.search_var_offset(node.arg)  # get value from local
        self.text += f'lw $t1, {value_offset}($t0)\n'
        self.text += 'addi $sp, $sp, -4\n'
        self.text += 'sw $t1, 0($sp)\n'

    @visitor.when(CIL_AST.VCall)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'
        
        for arg in node.params:
            self.visit(arg)

        value_offset = self.search_var_offset(node.instance)  
        self.text += f'lw $t1, {value_offset}($t0)\n'  # get instance from local

        self.text += f'lw $t2, 8($t1)\n' #get dispatch table address

        method_offset = self.search_method_offset(node.dynamic_type, node.function)
        self.text += f'lw $t3, {method_offset}($t2)\n' # get method address
        
        self.text += 'jal $t3\n'


    @visitor.when(CIL_AST.Call)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'
        
        for arg in node.params:
            self.visit(arg)

        self.text += f'jal {node.function}\n'


    @visitor.when(CIL_AST.BinaryOperator)
    def visit(self, node):
        mips_comm = self.mips_comm_for_binary_op[node.op]
        left_offset = self.search_var_offset(node.left)
        right_offset = self.search_var_offset(node.right)
        self.text += f'lw $a0, {left_offset}($sp)\n'
        self.text += f'lw $t1, {right_offset}($sp)\n'
        self.text += f'{mips_comm} $a0, $t1, $a0\n'
        result_offset = self.search_var_offset(node.local_dest)
        self.text += f'sw $a0, {result_offset}($sp)\n'
    
    @visitor.when(CIL_AST.INTEGER)
    def visit(self, node):
        self.text += f'li $a0, {node.value}\n'
    
    @visitor.when(CIL_AST.IfGoto)
    def visit(self, node):
        predicate_offset = self.search_var_offset(node.variable)
        self.text += f'lw $a0, {predicate_offset}($sp)\n'
        self.text += f'li $t1, 1\n'
        self.text += f'beq $a0, $t1 {node.label}\n'
    
    @visitor.when(CIL_AST.Goto)
    def visit(self, node):
        self.text += f'b {node.label}\n'
    
    @visitor.when(CIL_AST.Label)
    def visit(self, node):
        self.text += f'{node.label}:\n'

    @visitor.when(CIL_AST.PrintInteger)
    def visit(self, node):   
        if isinstance(node.variable, int):
            self.text += $"\t li $v0 , 1\n";
            self.text += $"\t li $a0 , {node.variable}\n";
            self.text += $"\t syscall\n";
        else:
            var_offset = self.search_var_offset(node.variable)
            self.text += $"\t li $v0 , 1\n";
            self.text += $"\t lw $a0 , {var_offset}($sp)\n";
            self.text += $"\t syscall\n";

    @visitor.when(CIL_AST.PrintString)
    def visit(self, node):
        pass

    

if __name__ == '__main__':
    import sys
    from cparser import Parser
    from semantic_analyzer import SemanticAnalyzer
    from cool_to_cil import COOLToCILVisitor

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
        
        cool_to_cil = COOLToCILVisitor(context)
        cil_ast = cool_to_cil.visit(cool_ast, scope)
        
        formatter = CIL_AST.get_formatter()
        cil_code = formatter(cil_ast)
        with open(f'{sys.argv[1][:-3]}.cil', 'w') as f:
            f.write(f'{cil_code}')

        cil_to_mips = CILToMIPSVisitor()
        mips_code = cil_to_mips.visit(cil_ast)
       
        with open(f'{sys.argv[1][:-3]}.s', 'w') as f:
            f.write(f'{mips_code}')
