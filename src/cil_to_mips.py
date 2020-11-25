from semantic import Scope, VariableInfo
import visitor
import ast_nodes as COOL_AST
import cil_ast_nodes as CIL_AST

class CILToMIPSVisitor():
    def __init__(self):
        self.mips_code = ''
        self.text = ''
        self.data = ''
        self.mips_comm_for_operators = {
            '+' : 'add',
            '-' : 'sub',
            '*' : 'mul',
            '/' : 'div',
            '<' : 'slt',
            '<=' : 'sle',
            '=' : 'seq',
            '~' : 'neg',
            'not': 'not'
        }
        self.current_function = None
        self.types = None
        self.attr_offset = {}
        self.method_offset = {}
        self.var_offset = {}
        self.runtime_errors = {}
        self.register_runtime_errors()

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
        
    def register_runtime_errors(self):
        self.runtime_errors['dispatch_void'] = 'Runtime Error: A dispatch (static or dynamic) on void'
        self.runtime_errors['case_void'] = 'Runtime Error: A case on void'
        self.runtime_errors['case_no_match'] = 'Runtime Error: Execution of a case statement without a matching branch'
        self.runtime_errors['div_zero'] = 'Runtime Error: Division by zero'
        self.runtime_errors['substr'] = 'Runtime Error: Substring out of range'
        self.runtime_errors['heap'] = 'Runtime Error: Heap overflow'
        for error in self.runtime_errors:
            self.data += f'{error}: .asciiz "{self.runtime_errors[error]}"\n'
            self.generate_runtime_error(error)

    def generate_runtime_error(self, error):
        self.text += f'{error}_error:\n'
        self.text += f'la $a0 {error}\n'
        self.text += f'li $v0, 4\n'
        self.text += 'syscall\n'
        self.text += 'li $v0, 10\n'
        self.text += 'syscall\n'

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(CIL_AST.Program)
    def visit(self, node):
        self.types = node.dottypes
        
        self.data += 'void: .word 0\n'
        
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

        self.var_offset.__setitem__(self.current_function.name, {})
       
        for idx, var in enumerate(self.current_function.localvars + self.current_function.params):
            self.var_offset[self.current_function.name][var.name] = (idx + 1)*4
         

        self.text += f'{node.name}:\n'
        # self.text += f'move $fp, $sp\n'  #save frame pointer of current function
        
        # for local_node in reversed(node.localvars): #save space for locals 
        #     self.visit(local_node)
        self.text += f'addi $sp, $sp, {-4 * len(node.localvars)}\n'
        
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

        idx = 0
        self.attr_offset.__setitem__(node.name, {})
        for attr in node.attributes:
            self.attr_offset[node.name][attr] = 4*idx + 16
            idx = idx + 1
        
        idx = 0
        self.method_offset.__setitem__(node.name, {})
        for met in node.methods:
            self.method_offset[node.name][met] = 4*idx
            idx = idx + 1
        
        
    @visitor.when(CIL_AST.Assign)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.local_dest]
        
        if isinstance(node.right_expr, int):
            self.text += f'li $t1, {node.right_expr}\n'
        else:
            right_offset = self.var_offset[self.current_function.name][node.right_expr]
            self.text += f'lw $t1, {right_offset}($sp)\n'

        self.text += f'sw $t1, {offset}($sp)\n'


    @visitor.when(CIL_AST.Allocate)
    def visit(self, node):
        amount = len(self.types[node.type].attributes) + 4
        self.text += f'li $a0, {amount * 4}\n' 
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        self.text += f'move $t0, $v0\n'
        
        #Initialize Object Layout
        self.text += f'li $t1, {node.tag}\n' #tag
        self.text += f'sw $t1, 0($t0)\n'
        self.text += f'la $t1, {node.type}_name\n' #type_name
        self.text += f'sw $t1, 4($t0)\n'
        self.text += f'li $t1, {amount}\n' #size
        self.text += f'sw $t1, 8($t0)\n'
        self.text += f'la $t1, {node.type}_methods\n' #methods pointer
        self.text += f'sw $t1, 12($t0)\n'

        offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t0, {offset}($sp)\n'  #store instance address in local

    @visitor.when(CIL_AST.ParamDec)
    def visit(self, node):
        pass

    @visitor.when(CIL_AST.LocalDec)
    def visit(self, node):
        # self.text += 'addi $sp, $sp, -4\n'
        # self.text += 'sw $zero, 0($sp)\n'
        pass

    @visitor.when(CIL_AST.GetAttr)
    def visit(self, node):
        self_offset = self.var_offset[self.current_function.name][node.instance]
        self.text += f'lw $t0, {self_offset}($sp)\n'  #get self address
        
        attr_offset = self.attr_offset[node.static_type][node.attr]
        self.text += f'lw $t1, {attr_offset}($t0)\n'  #get attribute
        
        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t1, {result_offset}($sp)\n' #store attribute in local

    @visitor.when(CIL_AST.SetAttr)
    def visit(self, node):
        self_offset = self.var_offset[self.current_function.name][node.instance]
        self.text += f'lw $t0, {self_offset}($sp)\n'  #get self address

        if node.value:
            value_offset = self.var_offset[self.current_function.name][node.value]  # get value from local
            self.text += f'lw $t1, {value_offset}($sp)\n'
        else:
            self.text += f'la $t1, void\n'  # not initialized attribute
            
        attr_offset = self.attr_offset[node.static_type][node.attr]
        self.text += f'sw $t1, {attr_offset}($t0)\n' #set attribute in instance


    @visitor.when(CIL_AST.Arg)
    def visit(self, node):
        value_offset = self.var_offset[self.current_function.name][node.arg]  # get value from local
        self.text += f'lw $t1, {value_offset}($t0)\n'
        self.text += 'addi $sp, $sp, -4\n'
        self.text += 'sw $t1, 0($sp)\n'

    @visitor.when(CIL_AST.VCall)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'
        
        for arg in node.params:
            self.visit(arg)

        value_offset = self.var_offset[self.current_function.name][node.instance]  
        self.text += f'lw $t1, {value_offset}($t0)\n'  # get instance from local
        self.text += 'la $t0, void\n'
        self.text += 'beq $t1, $t0, dispatch_void_error\n'
        
        self.text += f'lw $t2, 12($t1)\n' #get dispatch table address

        method_offset = self.method_offset[node.dynamic_type][node.function]
        self.text += f'lw $t3, {method_offset}($t2)\n' # get method address
        
        self.text += 'jal $t3\n'


    @visitor.when(CIL_AST.Call)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'
        
        for arg in node.params:
            self.visit(arg)

        self.text += f'jal {node.function}\n'

    @visitor.when(CIL_AST.Case)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.local_expr]
        self.text += f'lw $t0, {offset}($sp)\n'
        self.text += f'lw $t1, 0($t0)\n'
        self.text += 'la $a0, void\n'
        self.text += f'bne	$t1 $a0 {node.first_label}\n'
        self.text += 'b case_void_error'

    @visitor.when(CIL_AST.Action)
    def visit(self, node):
        self.text += f'blt	$t1 {node.tag} {node.next_label}\n'
        self.text += f'bgt	$t1 {node.max_tag} {node.next_label}\n'


    @visitor.when(CIL_AST.BinaryOperator)
    def visit(self, node):
        mips_comm = self.mips_comm_for_operators[node.op]
        left_offset = self.var_offset[self.current_function.name][node.left]
        right_offset = self.var_offset[self.current_function.name][node.right]
        self.text += f'lw $a0, {left_offset}($sp)\n'
        self.text += f'lw $t1, {right_offset}($sp)\n'
        if node.op == '/':
            self.text += 'beq $t1, 0, div_zero_error\n'
        self.text += f'{mips_comm} $a0, $t1, $a0\n'
        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $a0, {result_offset}($sp)\n'
    
    @visitor.when(CIL_AST.UnaryOperator)
    def visit(self, node):
        mips_comm = self.mips_comm_for_operators[node.op]
        expr_offset = self.var_offset[self.current_function.name][node.expr_value]
        self.text += f'lw $t1, {expr_offset}($sp)\n'
        self.text += f'{mips_comm} $a0, $t1 \n'
      
        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $a0, {result_offset}($sp)\n'
        
    @visitor.when(CIL_AST.IfGoto)
    def visit(self, node):
        predicate_offset = self.var_offset[self.current_function.name][node.variable]
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
            self.text += f'li $v0 , 1\n'
            self.text += f'li $a0 , {node.variable}\n'
            self.text += f'syscall\n'
        else:
            var_offset = self.var_offset[self.current_function.name][node.variable]
            self.text += f'li $v0 , 1\n'
            self.text += f'lw $a0 , {var_offset}($sp)\n'
            self.text += f'syscall\n'

    @visitor.when(CIL_AST.PrintString)
    def visit(self, node):
        var_offset = self.var_offset[self.current_function.name][node.variable]
        self.text += f'lw $a0, {var_offset}($sp)\n'
        self.text += f'li $v0, 4\n'
        self.text += f'syscall\n'

    @visitor.when(CIL_AST.ReadInteger)
    def visit(self, node):
        read_offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'li $v0, 5\n'
        self.text += f'syscall\n'
        self.text += f'sw $v0, {read_offset}($sp)\n'

    @visitor.when(CIL_AST.LoadStr)
    def visit(self, node):
        self.text += f'la $t0, {node.msg}\n'
        offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t0, {offset}($sp)\n'

    @visitor.when(CIL_AST.LoadInt)
    def visit(self, node):
        self.text += f'li $t0, {node.num}\n'
        offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t0, {offset}($sp)\n'

    @visitor.when(CIL_AST.Halt)
    def visit(self, node):
        self.text += 'li $v0, 10\n'
        self.text += 'syscall\n'

    @visitor.when(CIL_AST.TypeOf)
    def visit(self, node):
        obj_offset = self.var_offset[self.current_function.name][node.variable] 
        self.text += f'lw $t0, {obj_offset}($sp)\n' #get obj address from local
        self.text += 'lw $t1, 4($t0)\n' # get type name from the sec pos in obj layout
        res_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t1, {res_offset}($sp)\n'

    @visitor.when(CIL_AST.IsVoid)
    def visit(self, node):
        self.text += 'la $t0, void\n'
        offset = self.var_offset[self.current_function.name][node.expre_value] 
        self.text += f'lw $t1, {offset}($sp)\n' 
        self.text += 'seq $a0, $t0, $t1\n'  
        res_offset = self.var_offset[self.current_function.name][node.result_local]
        self.text += f'sw $a0, {res_offset}($sp)\n'
    
    @visitor.when(CIL_AST.Copy)
    def visit(self, node):
        # offset = self.var_offset[self.current_function.name][self.current_function.params[0].name] 
        self_offset = self.var_offset[self.current_function.name][node.type]
        self.text += f'lw $t0, {self_offset}($sp)\n'  # get self address
        self.text += f'lw $a0, 8($t0)\n'  # get self size
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        self.text += f'move $t1, $v0\n'

        # Copy All Slots inlcuding Tag, Size, methods ptr and each atrribute 
        # Tenemos q hacerlo en MIPS porq copy está a nivel de Object y en python
        # en este punto no sabemos el tipo dinamico (para asi saber el tamaño real) 
        # hasta q se haga el VCALL por lo el ciclo hayq  hacerlo en MIPS)

        self.text += 'li $a0, 0\n'
        self.text += 'copy_object_word:\n'
        self.text += 'lw $t2, ($t0)\n' # load current object word
        self.text += 'sw $t2, ($t1)\n' # store word in copy object
        self.text += 'addi $t0, $t0, 4\n' # move to the next word in orginal object
        self.text += 'addi $t1, $t1, 4\n' # move to the next word in copy object
        self.text += 'addi $a0, $a0, 4\n' # size count
        '''
        Src2 can either be a register or an immediate value (a 16 bit integer).
        blt Rsrc1, Src2, label (Branch on Less Than)
        Conditionally branch to the instruction at the label if the contents of register Rsrc1 are less than Src2.
        '''
        self.text += 'lw $t3, 8($t0)\n'
        self.text += 'blt $a0, $t3, copy_object_word\n' # 8($t0) is the orginal object size

        offset = self.var_offset[self.current_function.name][node.local_dest]
        # $t1 is pointing at the end of the object
        # if $v0 is modified for any reason (it should not, but...)
        # before looping we can move $t3, $t1 and use $t3 but this should work 
        self.text += f'sw $v0, {offset}($sp)\n'  #store instance address in local

    @visitor.when(CIL_AST.Length)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.variable]
        self.text += f'lw $t0, {offset}($sp)\n'
        self.text += 'li $a0, 0\n'
        self.text += 'count_char:\n'
        self.text += 'lb $t1, ($t0)\n' # loading current char
        self.text += 'beqz $t1, finish_chars_count\n' # finish if a zero is found
        self.text += 'addi $t0, $t0, 1\n' # move to the next char
        self.text += 'addi $a0, $a0, 1\n' # length_count += 1
        self.text += 'j count_char\n'
        self.text += 'finish_chars_count:\n'

        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $a0, {offset}($sp)\n'  # store length count address in local
    
    @visitor.when(CIL_AST.Concat)
    def visit(self, node):
        offset_str1 = self.var_offset[self.current_function.name][node.str1]
        offset_len1 = self.var_offset[self.current_function.name][node.len1]

        offset_str2 = self.var_offset[self.current_function.name][node.str2]
        offset_len2 = self.var_offset[self.current_function.name][node.len2]

        # reserve space for concatenation result
        self.text += f'lw $a0, {offset_len1}($sp)\n'
        self.text += f'lw $t0, {offset_len2}($sp)\n'
        # add Rdest, Rsrc1, Src2 Addition (with overflow)
        # is similar to addi but 2do summand can be a register
        self.text += 'add $a0, $a0, $t0\n'
        self.text += 'addi $a0, $a0, 1\n' # reserve 1 more byte for '\0'
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        # the beginning of new reserved address is in $v0

        self.text += f'lw $t0, {offset_str1}($sp)\n'
        self.text += f'lw $t1, {offset_str2}($sp)\n'

        # copy str1 starting in $t0 to $v0
        self.text += 'copy_str1_char:\n'
        self.text += 'lb $t2, ($t0)\n' # loading current char from str1
        self.text += 'sb $t2, ($v0)\n' # storing current char into result_str end
        self.text += 'beqz $t2, concat_str2_char\n' # finish if a zero is found
        self.text += 'addi $t0, $t0, 1\n' # move to the next char
        self.text += 'addi $v0, $v0, 1\n' # move to the next available byte
        self.text += 'j copy_str1_char\n'

        # concat str2 starting in $t1 to $v0
        self.text += 'concat_str2_char:\n'
        self.text += 'lb $t2, ($t0)\n' # loading current char from str1
        self.text += 'sb $t2, ($v0)\n' # storing current char into result_str end
        self.text += 'beqz $t2, finish_str2_concat\n' # finish if a zero is found
        self.text += 'addi $t1, $t1, 1\n' # move to the next char
        self.text += 'addi $v0, $v0, 1\n' # move to the next available byte
        self.text += 'j concat_str2_char\n'
        self.text += 'finish_str2_concat:\n'
        self.text += 'sb $0, ($v0)\n' # put '\0' at the end
        
        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $v0, {offset}($sp)\n'  # store length count address in local

    @visitor.when(CIL_AST.SubStr)
    def visit(self, node):
        offset_idx = self.var_offset[self.current_function.name][node.i]
        offset_len = self.var_offset[self.current_function.name][node.length]
        offset_str = self.var_offset[self.current_function.name][node.string]

        # reserve space for substring result
        self.text += f'lw $a0, {offset_len}($sp)\n'
        self.text += 'addi $a0, $a0, 1\n' # reserve 1 more byte for '\0'
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        # the beginning of new reserved address is in $v0
        
        self.text += f'lw $t0, {offset_idx}($sp)\n'
        self.text += f'lw $t1, {offset_len}($sp)\n'
        self.text += f'lw $t2, {offset_str}($sp)\n'

        self.text += 'bltz $t0, substr_error\n'

        # jump first i chars
        self.text += 'li $a0, 0\n'
        self.text += 'jump_str_char:\n'
        self.text += f'beq $a0, $t0, finish_index_jump\n' # finish if we are at index i
        self.text += 'addi $a0, $a0, 1\n' # chars count
        self.text += 'addi $t2, $t2, 1\n'  # move to the next char
        self.text += 'beq $t2, $zero, substr_error\n'
        self.text += 'j jump_str_char\n'
        self.text += 'finish_index_jump:\n'
        self.text += 'li $a0, 0\n' # reset $a0 to count the length

        # coping chars from string $t2 (starting in $t0 index) until length $t1 to $v0
        self.text += 'copy_substr_char:\n'
        self.text += 'beq $a0, $t1 finish_substr_copy\n' # finish if the chars count is equals to length
        self.text += 'lb $t0, ($t2)\n' # loading current char from string
        self.text += 'sb $t0, ($v0)\n' # storing current char into result_str end
        self.text += 'addi $t2, $t2, 1\n'  # move to the next char
        self.text += 'beq $t2, $zero, substr_error\n'
        self.text += 'addi $v0, $v0, 1\n' # move to the next available byte
        self.text += 'addi $a0, $a0, 1\n' # chars count
        self.text += 'j copy_substr_char\n'
        self.text += 'finish_substr_copy:\n'
        self.text += 'sb $0, ($v0)\n' # put '\0' at the end
        
        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $v0, {offset}($sp)\n'  # store length count address in local


if __name__ == '__main__':
    import sys
    from cparser import Parser
    from lexer import Lexer
    from semantic_analyzer import SemanticAnalyzer
    from cool_to_cil import COOLToCILVisitor

    lexer = Lexer()
    parser = Parser()

    sys.argv.append('hello_world.cl')

    if len(sys.argv) > 1:

        input_file = sys.argv[1]
        with open(input_file, encoding="utf-8") as file:
            cool_program_code = file.read()

        lexer.input(cool_program_code)
        for token in lexer: pass
        
        if lexer.errors:
            print(lexer.errors[0])
            exit(1)

        cool_ast = parser.parse(cool_program_code)

        if parser.errors:
            print(parser.errors[0])
            exit(1)

        semantic_analyzer = SemanticAnalyzer(cool_ast)
        context, scope = semantic_analyzer.analyze()

        if semantic_analyzer.errors:
            print(semantic_analyzer.errors[0])  
            exit(1)
        
        cool_to_cil = COOLToCILVisitor(context)
        cil_ast = cool_to_cil.visit(cool_ast, scope)
        
        # formatter = CIL_AST.get_formatter()
        # cil_code = formatter(cil_ast)
        # with open(f'{sys.argv[1][:-3]}.cil', 'w') as f:
        #     f.write(f'{cil_code}')

        cil_to_mips = CILToMIPSVisitor()
        mips_code = cil_to_mips.visit(cil_ast)
       
        with open(f'{sys.argv[1][:-3]}.s', 'w') as f:
            f.write(f'{mips_code}')
