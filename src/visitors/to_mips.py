import os
from code_generation import *
# from code_generation.tools import *
from semantic.context import VariableInfo
from semantic.types import Attribute
from typing import List
import visitors.visitor as visitor

class MIPS:
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

    @visitor.when(ProgramNodeIL)
    def visit(self, node):
        self.types = node.dottypes
        
        self.data += 'temp_string: .space 2048\n' 
        self.data += 'void: .word 0\n'
        
        for node_type in node.dottypes.values():
            self.visit(node_type)
        
        for node_data in node.dotdata.keys():
            self.data += f'{node_data}: .asciiz "{node.dotdata[node_data]}"\n'

        for node_function in node.dotcode:
            self.visit(node_function)
        
        self.mips_code = '.data\n' + self.data + '.text\n' + self.text 
        return self.mips_code.strip()
    
    @visitor.when(FunctionNodeIL)
    def visit(self, node):
        self.current_function = node

        self.var_offset.__setitem__(self.current_function.name, {})
    
        for idx, var in enumerate(self.current_function.localvars + self.current_function.params):
            self.var_offset[self.current_function.name][var.name] = (idx + 1)*4
        

        self.text += f'{node.name}:\n'
        
        self.text += f'addi $sp, $sp, {-4 * len(node.localvars)}\n'
        
        self.text += 'addi $sp, $sp, -4\n' 
        self.text += 'sw $ra, 0($sp)\n'

        for instruction in node.instructions:
            self.visit(instruction)
        
        self.text += 'lw $ra, 0($sp)\n'  
        total = 4 * len(node.localvars) + 4 * len(node.params) + 4
        self.text += f'addi $sp, $sp, {total}\n' 
        self.text += 'jr $ra\n' 

    @visitor.when(TypeNodeIL)
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
        
        
    @visitor.when(AssignNodeIL)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.dest]
        if node.source:
            if isinstance(node.source, int):
                self.text += f'li $t1, {node.source}\n'
            else:
                right_offset = self.var_offset[self.current_function.name][node.source]
                self.text += f'lw $t1, {right_offset}($sp)\n'
        else:
            self.text += f'la $t1, void\n'

        self.text += f'sw $t1, {offset}($sp)\n'


    @visitor.when(AllocateNodeIL)
    def visit(self, node):
        amount = len(self.types[node.type].attributes) + 4
        self.text += f'li $a0, {amount * 4}\n' 
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        self.text += f'move $t0, $v0\n'
        
        self.text += f'li $t1, {node.name}\n' 
        self.text += f'sw $t1, 0($t0)\n'
        self.text += f'la $t1, {node.type}_name\n' 
        self.text += f'sw $t1, 4($t0)\n'
        self.text += f'li $t1, {amount}\n' 
        self.text += f'sw $t1, 8($t0)\n'
        self.text += f'la $t1, {node.type}_methods\n' 
        self.text += f'sw $t1, 12($t0)\n'

        offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $t0, {offset}($sp)\n' 

    @visitor.when(ParamNodeIL)
    def visit(self, node):
        pass

    @visitor.when(LocalNodeIL)
    def visit(self, node):
        pass

    @visitor.when(GetAttribNodeIL)
    def visit(self, node):
        self_offset = self.var_offset[self.current_function.name][node.obj]
        self.text += f'lw $t0, {self_offset}($sp)\n'  
        
        attr_offset = self.attr_offset[node.attr_type][node.attr]
        self.text += f'lw $t1, {attr_offset}($t0)\n'  
        
        result_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $t1, {result_offset}($sp)\n' 

    @visitor.when(SetAttribNodeIL)
    def visit(self, node):
        self_offset = self.var_offset[self.current_function.name][node.obj]
        self.text += f'lw $t0, {self_offset}($sp)\n'  

        if node.value:
            value_offset = self.var_offset[self.current_function.name][node.value]  
            self.text += f'lw $t1, {value_offset}($sp)\n'
        else:
            self.text += f'la $t1, void\n'  
            
        attr_offset = self.attr_offset[node.attr_type][node.attr]
        self.text += f'sw $t1, {attr_offset}($t0)\n' 


    @visitor.when(ArgNodeIL)
    def visit(self, node):
        value_offset = self.var_offset[self.current_function.name][node.dest]  
        self.text += f'lw $t1, {value_offset}($t0)\n'
        self.text += 'addi $sp, $sp, -4\n'
        self.text += 'sw $t1, 0($sp)\n'

    @visitor.when(DynamicCallNodeIL)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'
        
        for arg in node.args:
            self.visit(arg)
        value_offset = self.var_offset[self.current_function.name][node.obj]  
        self.text += f'lw $t1, {value_offset}($t0)\n'  
        self.text += 'la $t0, void\n'
        self.text += 'beq $t1, $t0, dispatch_void_error\n'
        
        self.text += f'lw $t2, 12($t1)\n' 

        method_offset = self.method_offset[node.type][node.method]
        self.text += f'lw $t3, {method_offset}($t2)\n' 
        
        self.text += 'jal $t3\n'

        result_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $a1, {result_offset}($sp)\n'


    @visitor.when(StaticCallNodeIL)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'
        for arg in node.args:
            self.visit(arg)

        self.text += f'jal {node.function}\n'

        result_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $a1, {result_offset}($sp)\n'

    @visitor.when(ReturnNodeIL)
    def visit(self, node):
        if node.value:
            offset = self.var_offset[self.current_function.name][node.value]
            self.text += f'lw $a1, {offset}($sp)\n'
        else:
            self.text += f'move $a1, $zero\n'

    @visitor.when(CaseNodeIL)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.local_expr]
        self.text += f'lw $t0, {offset}($sp)\n'
        self.text += f'lw $t1, 0($t0)\n'
        self.text += 'la $a0, void\n'
        self.text += f'bne $t1 $a0 {node.first_label}\n'
        self.text += 'b case_void_error\n'

    @visitor.when(OptionNodeIL)
    def visit(self, node):
        self.text += f'blt $t1 {node.tag} {node.next_label}\n'
        self.text += f'bgt $t1 {node.max_tag} {node.next_label}\n'


    @visitor.when(BinaryNodeIL)
    def visit(self, node):
        mips_comm = self.mips_comm_for_operators[node.op]
        left_offset = self.var_offset[self.current_function.name][node.left]
        right_offset = self.var_offset[self.current_function.name][node.right]
        self.text += f'lw $a0, {left_offset}($sp)\n'
        self.text += f'lw $t1, {right_offset}($sp)\n'
        if node.op == '/':
            self.text += 'beq $t1, 0, div_zero_error\n'
        self.text += f'{mips_comm} $a0, $a0, $t1\n'
        result_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $a0, {result_offset}($sp)\n'
    
    @visitor.when(UnaryNodeIL)
    def visit(self, node):
        expr_offset = self.var_offset[self.current_function.name][node.expr]
        self.text += f'lw $t1, {expr_offset}($sp)\n'
        if node.op == 'not':
            self.text += f'xor $a0, $t1, 1\n'
        else:
            self.text += f'neg $a0, $t1 \n'
    
        result_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $a0, {result_offset}($sp)\n'
        
    @visitor.when(GotoIfNodeIL)
    def visit(self, node):
        predicate_offset = self.var_offset[self.current_function.name][node.cond]
        self.text += f'lw $t0, {predicate_offset}($sp)\n'
        self.text += f'lw $a0, 16($t0)\n'
        self.text += f'bnez $a0, {node.label}\n'
    
    @visitor.when(GotoNodeIL)
    def visit(self, node):
        self.text += f'b {node.label}\n'
    
    @visitor.when(LabelNodeIL)
    def visit(self, node):
        self.text += f'{node.label}:\n'

    @visitor.when(OutIntNodeIL)
    def visit(self, node):
        if isinstance(node.value, int):
            self.text += f'li $v0 , 1\n'
            self.text += f'li $a0 , {node.value}\n'
            self.text += f'syscall\n'
        else:
            var_offset = self.var_offset[self.current_function.name][node.value]
            self.text += f'li $v0 , 1\n'
            self.text += f'lw $a0 , {var_offset}($sp)\n'
            self.text += f'syscall\n'

    @visitor.when(OutStringNodeIL)
    def visit(self, node):
        var_offset = self.var_offset[self.current_function.name][node.value]
        self.text += f'lw $a0, {var_offset}($sp)\n'
        self.text += f'li $v0, 4\n'
        self.text += f'syscall\n'

    @visitor.when(ReadIntNodeIL)
    def visit(self, node):
        read_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'li $v0, 5\n'
        self.text += f'syscall\n'
        self.text += f'sw $v0, {read_offset}($sp)\n'

    @visitor.when(ReadStringNodeIL)
    def visit(self, node):
        read_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'la $a0, temp_string\n'
        self.text += f'li $a1, 2048\n'
        self.text += f'li $v0, 8\n'
        self.text += f'syscall\n'

        self.text += 'move $t0, $a0\n'
        self.text += 'jump_read_str_char:\n'
        self.text += 'li $t1, 0\n'
        self.text += 'lb $t1, 0($t0)\n'
        self.text += 'beqz $t1, analize_str_end\n'
        self.text += 'addi $t0, $t0, 1\n'
        self.text += 'j jump_read_str_char\n'

        self.text += 'analize_str_end:\n'
        self.text += 'addi $t0, $t0, -1\n' 
        self.text += 'li $t1, 0\n'
        self.text += 'lb $t1, 0($t0)\n'
        self.text += 'bne $t1, 10, finish_jump_read_str_char\n' 
        self.text += 'sb $0, 0($t0)\n' 
        self.text += 'addi $t0, $t0, -1\n' 
        self.text += 'lb $t1, 0($t0)\n'
        self.text += 'bne $t1, 13, finish_jump_read_str_char\n' 
        self.text += 'sb $0, 0($t0)\n' 
        self.text += 'j analize_str_end\n'
        self.text += 'finish_jump_read_str_char:\n'

        self.text += f'sw $a0, {read_offset}($sp)\n'

    @visitor.when(LoadNodeIL)
    def visit(self, node):
        if node.msg != None:
            if isinstance(node.msg, str):
                self.text += f'la $t0, {node.msg}\n'
                offset = self.var_offset[self.current_function.name][node.dest]
                self.text += f'sw $t0, {offset}($sp)\n'
            else:
                self.text += f'li $t0, {node.msg}\n'
                offset = self.var_offset[self.current_function.name][node.dest]
                self.text += f'sw $t0, {offset}($sp)\n'

    @visitor.when(HaltNodeIL)
    def visit(self, node):
        self.text += 'li $v0, 10\n'
        self.text += 'syscall\n'

    @visitor.when(TypeOfNodeIL)
    def visit(self, node):
        obj_offset = self.var_offset[self.current_function.name][node.obj] 
        self.text += f'lw $t0, {obj_offset}($sp)\n' #get obj address from local
        self.text += 'lw $t1, 4($t0)\n' # get type name from the sec pos in obj layout
        res_offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $t1, {res_offset}($sp)\n'

    @visitor.when(IsVoidNodeIL)
    def visit(self, node):
        self.text += 'la $t0, void\n'
        offset = self.var_offset[self.current_function.name][node.expre_value] 
        self.text += f'lw $t1, {offset}($sp)\n' 
        self.text += 'seq $a0, $t0, $t1\n'  
        res_offset = self.var_offset[self.current_function.name][node.result_local]
        self.text += f'sw $a0, {res_offset}($sp)\n'
    
    @visitor.when(CopyNodeIL)
    def visit(self, node):
        self_offset = self.var_offset[self.current_function.name][node.source]
        self.text += f'lw $t0, {self_offset}($sp)\n'  
        self.text += f'lw $a0, 8($t0)\n'  
        self.text += f'mul $a0, $a0, 4\n' 
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        self.text += f'move $t1, $v0\n'

        self.text += 'li $a0, 0\n'
        self.text += 'lw $t3, 8($t0)\n'
        self.text += 'copy_object_word:\n'
        self.text += 'lw $t2, 0($t0)\n' 
        self.text += 'sw $t2, 0($t1)\n' 
        self.text += 'addi $t0, $t0, 4\n' 
        self.text += 'addi $t1, $t1, 4\n' 
        self.text += 'addi $a0, $a0, 1\n' 
        
        self.text += 'blt $a0, $t3, copy_object_word\n' 

        offset = self.var_offset[self.current_function.name][node.dest]
        
        self.text += f'sw $v0, {offset}($sp)\n'  

    @visitor.when(LengthNodeIL)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.arg]
        self.text += f'lw $t0, {offset}($sp)\n'
        self.text += f'lw $t0, 16($t0)\n'
        
        self.text += 'li $a0, 0\n'
        self.text += 'count_char:\n'
        self.text += 'lb $t1, 0($t0)\n' 
        self.text += 'beqz $t1, finish_chars_count\n' 
        self.text += 'addi $t0, $t0, 1\n' 
        self.text += 'addi $a0, $a0, 1\n' 
        self.text += 'j count_char\n'
        self.text += 'finish_chars_count:\n'

        offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $a0, {offset}($sp)\n'
    
    @visitor.when(ConcatNodeIL)
    def visit(self, node):
        offset_arg1 = self.var_offset[self.current_function.name][node.arg1]
        offset_len1 = self.var_offset[self.current_function.name][node.len1]

        offset_arg2 = self.var_offset[self.current_function.name][node.arg2]
        offset_len2 = self.var_offset[self.current_function.name][node.len2]

        self.text += f'lw $a0, {offset_len1}($sp)\n'
        self.text += f'lw $t0, {offset_len2}($sp)\n'

        self.text += 'add $a0, $a0, $t0\n'
        self.text += 'addi $a0, $a0, 1\n'
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        self.text += 'move $t3, $v0\n'

        self.text += f'lw $t0, {offset_arg1}($sp)\n'
        self.text += f'lw $t1, {offset_arg2}($sp)\n'
    
        self.text += 'copy_arg1_char:\n'
        self.text += 'lb $t2, 0($t0)\n' 
        self.text += 'sb $t2, 0($v0)\n' 
        self.text += 'beqz $t2, concat_arg2_char\n' 
        self.text += 'addi $t0, $t0, 1\n' 
        self.text += 'addi $v0, $v0, 1\n' 
        self.text += 'j copy_arg1_char\n'

        self.text += 'concat_arg2_char:\n'
        self.text += 'lb $t2, 0($t1)\n' 
        self.text += 'sb $t2, 0($v0)\n' 
        self.text += 'beqz $t2, finish_arg2_concat\n' 
        self.text += 'addi $t1, $t1, 1\n' 
        self.text += 'addi $v0, $v0, 1\n' 
        self.text += 'j concat_arg2_char\n'
        self.text += 'finish_arg2_concat:\n'
        self.text += 'sb $0, ($v0)\n' 
        
        offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $t3, {offset}($sp)\n'  

    @visitor.when(SubstringNodeIL)
    def visit(self, node):
        offset_idx = self.var_offset[self.current_function.name][node.begin]
        offset_len = self.var_offset[self.current_function.name][node.end]
        offset_str = self.var_offset[self.current_function.name][node.word]

        self.text += f'lw $a0, {offset_len}($sp)\n'
        self.text += 'addi $a0, $a0, 1\n' 
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        
        self.text += f'lw $t0, {offset_idx}($sp)\n'
        self.text += f'lw $t1, {offset_len}($sp)\n'
        self.text += f'lw $t4, {offset_str}($sp)\n'
        self.text += f'lw $t2, 16($t4)\n'

        self.text += 'bltz $t0, substr_error\n'

        self.text += 'li $a0, 0\n'
        self.text += 'jump_str_char:\n'
        self.text += f'beq $a0, $t0, finish_index_jump\n' 
        self.text += 'addi $a0, $a0, 1\n' 
        self.text += 'addi $t2, $t2, 1\n' 
        self.text += 'beq $t2, $zero, substr_error\n'
        self.text += 'j jump_str_char\n'
        self.text += 'finish_index_jump:\n'
        self.text += 'li $a0, 0\n' 
        self.text += 'move $t3, $v0\n' 

        
        self.text += 'copy_substr_char:\n'
        self.text += 'beq $a0, $t1 finish_substr_copy\n' 
        self.text += 'li $t0, 0\n' 
        self.text += 'lb $t0, 0($t2)\n' 
        self.text += 'sb $t0, 0($v0)\n' 
        self.text += 'addi $t2, $t2, 1\n'  
        self.text += 'beq $t2, $zero, substr_error\n'
        self.text += 'addi $v0, $v0, 1\n' 
        self.text += 'addi $a0, $a0, 1\n' 
        self.text += 'j copy_substr_char\n'
        self.text += 'finish_substr_copy:\n'
        self.text += 'sb $0, ($v0)\n' 
        
        offset = self.var_offset[self.current_function.name][node.dest]
        self.text += f'sw $t3, {offset}($sp)\n'  

    @visitor.when(StringEqualsNodeIL)
    def visit(self, node):
        offset_arg1 = self.var_offset[self.current_function.name][node.s1]
        offset_arg2 = self.var_offset[self.current_function.name][node.s2]
        
        self.text += f'lw $t1, {offset_arg1}($sp)\n'
        self.text += f'lw $t2, {offset_arg2}($sp)\n'

        
        self.text += 'compare_str_char:\n'
        self.text += 'li $t3, 0\n' 
        self.text += 'lb $t3, 0($t1)\n' 
        self.text += 'li $t4, 0\n' 
        self.text += 'lb $t4, 0($t2)\n' 
        self.text += 'seq $a0, $t3, $t4\n' 
        self.text += 'beqz $a0, finish_compare_str\n' 
        self.text += 'beqz $t3, finish_compare_str\n' 
        self.text += 'beqz $t4, finish_compare_str\n' 
        self.text += 'addi $t1, $t1, 1\n' 
        self.text += 'addi $t2, $t2, 1\n' 
        self.text += 'j compare_str_char\n'
        self.text += 'finish_compare_str:\n'

        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $a0, {offset}($sp)\n'