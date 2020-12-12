from cil_ast import *
from type_defined import *

DATA = []
CIL_TYPES = {}
LABELS_COUNT = 0
PARAM_COUNT = 0
MAX_LOCALS_COUNT = 0
MAX_PARAMS_COUNT = 0

def next_label():
    global LABELS_COUNT
    result = "custom_label_" + str(LABELS_COUNT)
    LABELS_COUNT += 1
    return result


def generate_mips(cil):
    global CIL_TYPES, LABELS_COUNT
    LABELS_COUNT = 0
    CIL_TYPES = cil[0]

    # this is called from type_defined
    refresh_methods_id()

    data = generate_data(cil[1], cil[3], cil[4])
    code = generate_code(cil[2], cil[6])

    return data + code


def generate_data(data, locals, max_param_count):
    global DATA, CIL_TYPES, MAX_LOCALS_COUNT, MAX_PARAMS_COUNT
    MAX_PARAMS_COUNT = max_param_count
    MAX_LOCALS_COUNT = locals
    
    if len(data) == 0 and locals == 0:
        return ""

    result = ".data\n\n"

    result += "abort_msg: .asciiz \"Abort called from class \"\n"
    result += "end_of_line: .asciiz \"\\n\"\n"
    result += "string_read_buffer: .space 1024\n"
    for t in CIL_TYPES.values():
        result += "type_" + t.type_name + ": .asciiz \"" + t.type_name + "\"\n"

    for l in range(0, locals):
        result += "local_" + str(l) + ": .word 0, 0\n"

    for d in data.values():
        DATA.append(d.id)
        result += d.id + ": .asciiz \"" + d.value.replace("\n", "\\n") + "\"\n"

    global PARAMS
    
    for i in range(0, max_param_count):
        result += "param_" + str(i) + ": .word 0, 0\n"
        PARAMS["param_" + str(i)] = None

    result += "\n\n"

    return result

PARAMS = {}
CURR_PARAM_COUNT = 0
CURR_FUNC = ""

# se le pasa en $s0 la cantidad de variables a escribir en la funcion que la llama
def generate_locals_write():
    result = "locals_write:\n"
    result += "addi $t7, $s0, 0\n"

    locals_write_end_label = next_label()

    counter = 0

    for i in range(0, MAX_LOCALS_COUNT):
        result += "beq $t7, 0, " + locals_write_end_label + "\n"
        name = "local_" + str(counter)
        result += "la $t1, " + name + "\n"
        result += "lw $t0, ($t1)\n"
        result += "sw $t0, ($sp)\n"
        result += "lw $t0, 4($t1)\n"
        result += "sw $t0, 4($sp)\n"
        result += "addi $sp, $sp, 8\n"
        result += "addi $t7, $t7, -1\n"
        counter += 1

    result += locals_write_end_label + ":\n"

    result += "jr $ra\n\n"

    return result

# se le pasa en s0 la cantidad de variables a leer en la funcion que la llama
def generate_locals_load():
    result = "locals_load:\n"
    result += "addi $t7, $s0, 0\n"
    
    locals_load_end_label = next_label()
    
    counter = 0

    result += "li $t6, 8\n"

    global MAX_LOCALS_COUNT
    for i in range(0, MAX_LOCALS_COUNT):
        result += "beq $t7, 0, " + locals_load_end_label + "\n"
        name = "local_" + str(counter)
        result += "mult $t7, $t6\n"
        result += "mflo $t5\n"
        result += "sub $t4, $sp, $t5\n"
        result += "lw $t0, ($t4)\n"
        result += "addi $t5, $t5, -4\n"
        result += "sub $t4, $sp, $t5\n"
        result += "lw $t1, ($t4)\n"
        result += "la $t2, " + name + "\n"
        result += "sw $t0, ($t2)\n"
        result += "sw $t1, 4($t2)\n"
        result += "addi $t7, $t7, -1\n"
        counter += 1

    result += locals_load_end_label + ":\n"
    result += "mult $s0, $t6\n"
    result += "mflo $t5\n"
    result += "sub $sp, $sp, $t5\n"

    result += "jr $ra\n\n"

    return result

# en s0 te mandan la cantidad de parametros a cargar
def generate_params_load():
    result = "params_load:\n"

    result += "addi $t7, $s0, 0\n"
    result += "li $t6, 8\n"
    result += "mult $t7, $t6\n"
    result += "mflo $t5\n"
    result += "addi $t5, 4\n"
    result += "sub $t6, $sp, $t5\n"

    counter = 0

    params_load_end_label = next_label()

    global MAX_PARAMS_COUNT
    for i in range(0, MAX_PARAMS_COUNT):
        result += "sub $t5, $sp, $t6\n"
        result += "blt $t5, 8, " + params_load_end_label + "\n"
        name = "param_" + str(counter)
        result += "lw $t0, ($t6)\n"
        result += "addi $t6, 4\n"
        result += "lw $t1, ($t6)\n"
        result += "addi $t6, 4\n"
        result += "la $t2, " + name + "\n"
        result += "sw $t0, ($t2)\n"
        result += "sw $t1, 4($t2)\n"
        counter += 1

    result += params_load_end_label + ":\n"
    result += "jr $ra\n\n"

    return result

def generate_allocate_Int():
    result = "allocate_Int:\n"

    result += "la $t1, type_Int\n"
    result += "sw $t1, ($s0)\n"
    result += "li $t1, 0\n"
    result += "sw $t1, 4($s0)\n"

    result += "jr $ra\n\n"

    return result

def generate_allocate_Bool():
    result = "allocate_Bool:\n"

    result += "la $t1, type_Bool\n"
    result += "sw $t1, ($s0)\n"
    result += "li $t1, 0\n"
    result += "sw $t1, 4($s0)\n"

    result += "jr $ra\n\n"

    return result

def generate_allocate_String():
    result = "allocate_String:\n"

    result += "la $t1, type_String\n"
    result += "sw $t1, ($s0)\n"
    result += "li $a0, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"
    result += "sw $v0, 4($s0)\n"
    result += "li $t1, 0\n"
    result += "sw $t1, ($v0)\n"
    result += "sb $t1, 4($v0)\n"

    result += "jr $ra\n\n"

    return result

def generate_allocate_Void():
    result = "allocate_Void:\n"

    result += "li $t1, 0\n"
    result += "sw $t1, ($s0)\n"
    result += "sw $t1, 4($s0)\n"

    result += "jr $ra\n\n"

    return result

def generate_is_descendant(son_father_tuples):
    result = "is_descendant:\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"

    result += "li $v0, 0\n"

    is_descendant_end_label = next_label()

    for t in son_father_tuples:
        is_descendant_next_label = next_label()
        result += "la $t2, type_" + t[0] + "\n"
        result += "la $t3, type_" + t[1] + "\n"
        result += "seq $t2, $t2, $s0\n"
        result += "seq $t3, $t3, $s1\n"
        result += "add $t2, $t2, $t3\n"
        result += "bne $t2, 2, " + is_descendant_next_label + "\n"
        result += "li $v0, 1\n"
        result += "j " + is_descendant_end_label + "\n"
        result += is_descendant_next_label + ":\n"

    result += is_descendant_end_label + ":\n"

    result += "sw $v0, 4($s7)\n"

    result += "jr $ra\n\n"

    return result

# se entran 3 ($s0, $s1 y $s2), la primera es la 
# direccion inicio desde donde copiar, la segunda es el offset, o sea, 
# cuantos elementos copiar, y la tercera la direccion donde se va a pegar
def generate_copy_from_to():
    result = "copy_from_to:\n"

    copy_from_to_loop_label = next_label()
    copy_from_to_end_label = next_label()

    result += copy_from_to_loop_label + ":\n"
    result += "beq $s1, 0, " + copy_from_to_end_label + "\n"
    result += "lb $t3, ($s0)\n"
    result += "sb $t3, ($s2)\n"
    result += "addi $s1, $s1, -1\n"
    result += "addi $s0, $s0, 1\n"
    result += "addi $s2, $s2, 1\n"
    result += "j " + copy_from_to_loop_label + "\n"
    result += copy_from_to_end_label + ":\n"

    result += "jr $ra\n\n"

    return result

# gets in ($s1) the direction of a string and returns in $s1 the length
def generate_get_length():
    result = "get_length:\n"

    end_label = next_label()
    loop_label = next_label()

    result += "li $s1, 0\n"
    result += loop_label + ":\n"
    result += "lb $t0, ($s0)\n"
    result += "beq $t0, 0, " + end_label + "\n"
    result += "addi $s1, $s1, 1\n"
    result += "addi $s0, $s0, 1\n"
    result += "j " + loop_label + "\n"
    result += end_label + ":\n"

    result += "jr $ra\n\n"

    return result

def generate_equality_function():
    result = "equality_function:\n"

    compare_strings_label = next_label()
    compare_strings_false_label = next_label()
    compare_strings_loop_label = next_label()
    equal_end_label = next_label()

    result += "lw $t3, ($s0)\n"
    result += "la $t4, type_String\n"
    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"
    result += "beq $t3, $t4, " + compare_strings_label + "\n"
    result += "seq $s0, $s0, $s1\n"
    result += "j " + equal_end_label + "\n"
    result += compare_strings_label + ":\n"
    result += "lw $t3, ($s0)\n"
    result += "lw $t4, ($s1)\n"
    result += "bne $t3, $t4, " + compare_strings_false_label + "\n"
    result += "li $t3, 0\n"
    result += "li $t4, 0\n"
    result += compare_strings_loop_label + ":\n"
    result += "lb $t3, 4($s0)\n"
    result += "lb $t4, 4($s1)\n"
    result += "bne $t3, $t4, " + compare_strings_false_label + "\n"
    result += "addi $s0, $s0, 1\n"
    result += "addi $s1, $s1, 1\n"
    result += "bne $t3, 0, " + compare_strings_loop_label + "\n"
    result += "li $s0, 1\n"
    result += "j " + equal_end_label + "\n"
    result += compare_strings_false_label + ":\n"
    result += "li $s0, 0\n"
    result += equal_end_label + ":\n"
    result += "sw $s0, 4($s2)\n"

    result += "jr $ra\n\n"

    return result

def generate_abort():
    result = "abort:\n"

    # write abort message
    result += "la $a0, abort_msg\n"
    result += "li $v0, 4\n"
    result += "syscall\n"

    # write type who called abort
    result += "lw $a0, 4($s0)\n"
    result += "li $v0, 4\n"
    result += "syscall\n"

    # write an end of line
    result += "la $a0, end_of_line\n"
    result += "li $v0, 4\n"
    result += "syscall\n"

    result += "li $v0, 10\n"
    result += "syscall\n"

    result += "jr $ra\n\n"

    return result

def generate_mov_func():
    result = "mov_func:\n"

    result += "lw $t2, ($s0)\n"
    result += "sw $t2, ($s1)\n"

    result += "lw $t2, 4($s0)\n"
    result += "sw $t2, 4($s1)\n"

    result += "jr $ra\n\n"

    return result

def generate_put_argument():
    result = "put_argument:\n"

    result += "lw $t1, ($s0)\n"
    result += "sw $t1, ($sp)\n"
    result += "lw $t1, 4($s0)\n"
    result += "sw $t1, 4($sp)\n"
    result += "addi $sp, $sp, 8\n"

    result += "jr $ra\n\n"

    return result

def generate_concat_func():
    result = "concat_func:\n"

    result += "sw $ra, ($sp)\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s6, 4($s6)\n"

    result += "lw $s1, ($s0)\n"
    result += "lw $t7, ($s6)\n"
    result += "add $a0, $s1, $t7\n"
    result += "addi $a0, $a0, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($s2)\n"
    result += "addi $a0, $a0, -5\n"
    result += "sw $a0, ($v0)\n"
    result += "addi $s2, $v0, 4\n"

    result += "addi $s0, $s0, 4\n"
    result += "jal copy_from_to\n"
    
    result += "addi $s0, $s6, 4\n"
    result += "addi $s1, $t7, 1\n"
    result += "jal copy_from_to\n"

    result += "lw $ra, ($sp)\n"

    result += "jr $ra\n\n"

    return result

def generate_print_func():
    result = "print_func:\n"

    result += "addi $a0, $s0, 0\n"
    result += "lw $a0, 4($a0)\n"
    result += "addi $a0, $a0, 4\n"
    
    result += "li $v0, 4\n"
    result += "syscall\n"

    result += "jr $ra\n\n"

    return result

def generate_print_int_func():
    result = "print_int_func:\n"

    result += "lw $a0, 4($s0)\n"
    result += "li $v0, 1\n"
    result += "syscall\n"

    result += "jr $ra\n\n"

    return result

def generate_read_int_func():
    result = "read_int_func:\n"

    result += "li $v0, 5\n"
    result += "syscall\n"
    
    result += "sw $v0, 4($t0)\n"

    result += "jr $ra\n\n"

    return result

def generate_load_data_func():
    result = "load_data_func:\n"

    result += "sw $ra, ($sp)\n"

    result += "addi $t7, $s0, 0\n"
    result += "jal get_length\n"
    result += "addi $s0, $t7, 0\n"

    result += "addi $a0, $s1, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($s2)\n"
    result += "sw $s1, ($v0)\n"

    result += "addi $s1, $s1, 1\n"
    result += "addi $s2, $v0, 4\n"

    result += "jal copy_from_to\n"

    result += "lw $ra, ($sp)\n"

    result += "jr $ra\n\n"

    return result

def generate_read_string_func():
    result = "read_string_func:\n"

    result += "sw $ra, ($sp)\n"

    result += "la $a0, string_read_buffer\n"
    result += "li $v0, 8\n"
    result += "syscall\n"

    result += "la $s0, string_read_buffer\n"

    result += "jal get_length\n"

    result += "la $s0, string_read_buffer\n"

    result += "addi $a0, $s1, 4\n"
    result += "li $v0, 9\n"
    result += "syscall\n"


    result += "sw $v0, 4($s2)\n"
    result += "addi $s1, $s1, -1\n"
    result += "sw $s1, ($v0)\n"

    result += "addi $s2, $v0, 4\n"


    result += "jal copy_from_to\n"

    result += "li $t3, 0\n"
    result += "sb $t3, ($s2)\n"

    result += "lw $ra, ($sp)\n"

    result += "jr $ra\n\n"

    return result


def generate_copy_func():
    result = "copy_func:\n"

    result += "sw $ra, ($sp)\n"

    result += "lw $t2, ($s6)\n"
    result += "sw $t2, ($s7)\n"
    
    copy_int_or_bool_label = next_label()
    copy_string_label = next_label()
    copy_string_loop_start_label = next_label()
    copy_object_loop_start_label = next_label()
    copy_end_label = next_label()

    result += "la $t3, type_Int\n"
    result += "beq $t2, $t3, " + copy_int_or_bool_label + "\n"
    result += "la $t3, type_Bool\n"
    result += "beq $t2, $t3, " + copy_int_or_bool_label + "\n"
    result += "la $t3, type_String\n"
    result += "beq $t2, $t3, " + copy_string_label + "\n"
    result += "lw $s0, 4($s6)\n"
    result += "lw $a0, ($s0)\n"
    result += "li $v0, 9\n"
    result += "syscall\n"
    result += "sw $v0, 4($s7)\n"
    result += "addi $s2, $v0, 0\n"
    result += "add $s1, $a0, 0\n"
    result += "jal copy_from_to\n"
    result += "j " + copy_end_label + "\n"
    result += copy_int_or_bool_label + ":\n"
    result += "lw $t2, 4($s6)\n"
    result += "sw $t2, 4($s7)\n"
    result += "j " + copy_end_label + "\n"
    result += copy_string_label + ":\n"
    result += "lw $s0, 4($s6)\n"
    result += "lw $t6, ($s0)\n"
    result += "addi $a0, $t6, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"
    result += "sw $v0, 4($s7)\n"
    result += "addi $s2, $v0, 0\n"
    result += "add $s1, $a0, 0\n"
    result += "jal copy_from_to\n"
    result += copy_end_label + ":\n"

    result += "lw $ra, ($sp)\n"

    result += "jr $ra\n\n"

    return result

def generate_substring_func():
    result = "substring_func:\n"

    result += "sw $ra, ($sp)\n"

    result += "lw $s0, 4($s0)\n"
    result += "addi $s0, $s0, 4\n"
    result += "lw $s7, 4($s7)\n"
    result += "add $s0, $s0, $s7\n"
    result += "lw $s1, 4($s1)\n"

    result += "addi $a0, $s1, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($s6)\n"
    result += "sw $s1, ($v0)\n"
    result += "addi $s2, $v0, 4\n"
    result += "jal copy_from_to\n"
    result += "li $t3, 0\n"
    result += "sb $t3, ($s2)\n"

    result += "lw $ra, ($sp)\n"

    result += "jr $ra\n\n"

    return result

def generate_less_func():
    result = "less_func:\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"
    result += "slt $s0, $s0, $s1\n"
    result += "sw $s0, 4($s2)\n"

    result += "jr $ra\n\n"

    return result

def generate_less_equal_func():
    result = "less_equal_func:\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"
    result += "sle $s0, $s0, $s1\n"
    result += "sw $s0, 4($s2)\n"

    result += "jr $ra\n\n"

    return result

def generate_divide_func():
    result = "divide_func:\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"
    result += "div $s0, $s0, $s1\n"
    result += "sw $s0, 4($s2)\n"

    result += "jr $ra\n\n"

    return result

def generate_multiply_func():
    result = "multiply_func:\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"
    result += "mult $s0, $s1\n"
    result += "mflo $s0\n"
    result += "sw $s0, 4($s2)\n"

    result += "jr $ra\n\n"

    return result

def generate_substract_func():
    result = "substract_func:\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"
    result += "sub $s0, $s0, $s1\n"
    result += "sw $s0, 4($s2)\n"

    result += "jr $ra\n\n"

    return result

def generate_add_func():
    result = "add_func:\n"

    result += "lw $s0, 4($s0)\n"
    result += "lw $s1, 4($s1)\n"
    result += "add $s0, $s0, $s1\n"
    result += "sw $s0, 4($s2)\n"

    result += "jr $ra\n\n"

    return result

def generate_call_func():
    result = "call_func:\n"

    result += "lw $s0, 4($s0)\n"

    call_func_end_label = next_label()

    for t in CIL_TYPES.values():

        is_not_this_type_label = next_label()

        result += "la $t1, type_" + t.type_name + "\n"
        result += "bne $s0, $t1, " + is_not_this_type_label + "\n"

        for m in t.methods.keys():
            is_not_this_method_label = next_label()

            result += "bne $s1, " + str(METHODS_NAME_TO_ID[m]) + ", " + is_not_this_method_label + "\n"

            result += "la $s3, " + t.methods[m] + "_" + m + "\n"

            result += "j " + call_func_end_label + "\n"

            result += is_not_this_method_label + ":\n"

        result += is_not_this_type_label + ":\n"

    result += call_func_end_label + ":\n"

    result += "jr $ra\n\n"

    return result

def generate_code(functions_code, son_father_tuples):
    result = ".text\n\n"

    result += generate_allocate_Int()
    result += generate_allocate_Bool()
    result += generate_allocate_String()
    result += generate_allocate_Void()
    result += generate_locals_write()
    result += generate_locals_load()
    result += generate_params_load()
    result += generate_copy_from_to()
    result += generate_get_length()
    result += generate_equality_function()
    result += generate_abort()
    result += generate_is_descendant(son_father_tuples)
    result += generate_mov_func()
    result += generate_put_argument()
    result += generate_concat_func()
    result += generate_print_func()
    result += generate_read_int_func()
    result += generate_read_string_func()
    result += generate_load_data_func()
    result += generate_print_int_func()
    result += generate_copy_func()
    result += generate_substring_func()
    result += generate_less_func()
    result += generate_less_equal_func()
    result += generate_divide_func()
    result += generate_multiply_func()
    result += generate_substract_func()
    result += generate_add_func()
    result += generate_call_func()

    global PARAMS, CURR_LOCAL_COUNT, CURR_PARAM_COUNT, PARAM_COUNT, CURR_FUNC

    for f in functions_code:
        CURR_PARAM_COUNT = 0
        CURR_LOCAL_COUNT = len(f.locals)
        CURR_FUNC = f.name

        result += f.name + ":\n"
        
        counter = len(f.params)

        for p in f.params:
            param_name = "param_" + str(CURR_PARAM_COUNT)
            PARAM_COUNT += 1
            PARAMS[p.id] = param_name
            result += "lw $t0, -" + str(8 * counter) + "($sp)\n"
            result += "lw $t1, -" + str(8 * counter - 4) + "($sp)\n"
            result += "la $t2, " + param_name + "\n"
            result += "sw $t0, ($t2)\n"
            result += "sw $t1, 4($t2)\n"

            counter -= 1
            CURR_PARAM_COUNT += 1

        if len(f.params) > 0:
            result += "sw $ra, ($sp)\n"
            result += "addi $sp, $sp, 4\n"
        
        for i in f.body:
            result += convert_cil_instruction(i)

        result += "\n\n"

    result = result[0:-2] + "li $v0, 10\n"
    result += "syscall\n"

    return result

def convert_cil_instruction(instruction):
    if type(instruction) == PrintNode:
        return convert_PrintNode(instruction)

    elif type(instruction) == PrintIntNode:
        return convert_PrintIntNode(instruction)
    
    elif type(instruction) == TypeNameNode:
        return convert_TypeNameNode(instruction)
    
    elif type(instruction) == TypeAddressNode:
        return convert_TypeAddressNode(instruction)

    elif type(instruction) == ReturnNode:
        return convert_ReturnNode(instruction)

    elif type(instruction) == ReadNode:
        return convert_ReadNode(instruction)

    elif type(instruction) == ReadIntNode:
        return convert_ReadIntNode(instruction)

    elif type(instruction) == TypeOfNode:
        return convert_TypeOfNode(instruction)

    elif type(instruction) == CopyNode:
        return convert_CopyNode(instruction)

    elif type(instruction) == StrlenNode:
        return convert_StrlenNode(instruction)

    elif type(instruction) == StrcatNode:
        return convert_StrcatNode(instruction)

    elif type(instruction) == StrsubNode:
        return convert_StrsubNode(instruction)

    elif type(instruction) == AllocateNode:
        return convert_AllocateNode(instruction)

    elif type(instruction) == ArgNode:
        return convert_ArgNode(instruction)

    elif type(instruction) == DispatchCallNode:
        return convert_DispatchCallNode(instruction)

    elif type(instruction) == SetAttributeNode:
        return convert_SetAttributeNode(instruction)

    elif type(instruction) == GetAttributeNode:
        return convert_GetAttributeNode(instruction)

    elif type(instruction) == ENode:
        return convert_ENode(instruction)

    elif type(instruction) == LNode:
        return convert_LNode(instruction)

    elif type(instruction) == LENode:
        return convert_LENode(instruction)

    elif type(instruction) == DivNode:
        return convert_DivNode(instruction)

    elif type(instruction) == MulNode:
        return convert_MulNode(instruction)
    
    elif type(instruction) == SubNode:
        return convert_SubNode(instruction)
    
    elif type(instruction) == AddNode:
        return convert_AddNode(instruction)
    
    elif type(instruction) == VDNode:
        return convert_VDNode(instruction)
    
    elif type(instruction) == AbortNode:
        return convert_AbortNode(instruction)

    elif type(instruction) == CmpNode:
        return convert_CmpNode(instruction)
    
    elif type(instruction) == NtNode:
        return convert_NtNode(instruction)
    
    elif type(instruction) == MovNode:
        return convert_MovNode(instruction)

    elif type(instruction) == SetStringNode:
        return convert_SetStringNode(instruction)
    
    elif type(instruction) == IfGotoNode:
        return convert_IfGotoNode(instruction)

    elif type(instruction) == GotoNode:
        return convert_GotoNode(instruction)

    elif type(instruction) == LabelNode:
        return convert_LabelNode(instruction)

    elif type(instruction) == LoadDataNode:
        return convert_LoadDataNode(instruction)

    elif type(instruction) == LocalSaveNode:
        return convert_LocalSaveNode(instruction)

    elif type(instruction) == IsSonNode:
        return convert_IsSonNode(instruction)

    else:
        print(str(type(instruction)) + " doesn't have convert method")
        return ""

def convert_IsSonNode(instruction):
    result = ""

    global PARAMS

    if instruction.son in PARAMS:
        son = PARAMS[instruction.son]
    else:
        son = instruction.son
    
    if instruction.father in PARAMS:
        father = PARAMS[instruction.father]
    else:
        father = instruction.father

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $s0, " + son + "\n"
    result += "la $s1, " + father + "\n"
    result += "la $s7, " + dest + "\n"

    result += "jal is_descendant\n"    

    return result
    


def convert_TypeNameNode(instruction):
    global DATA, PARAMS

    result = ""

    if instruction.type_addr in PARAMS:
        t_addr = PARAMS[instruction.type_addr]
    else:
        t_addr = instruction.type_addr

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $s0, " + t_addr + "\n"
    result += "lw $s0, 4($s0)\n"
    # poner en $s1 el tamanyo del string que comienza en ($s0)
    result += "jal get_length\n"

    result += "la $s0, " + t_addr + "\n"
    result += "lw $s0, 4($s0)\n"

    result += "la $s2, " + dest + "\n"
    
    result += "addi $a0, $s1, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($s2)\n"
    result += "sw $s1, ($v0)\n"
    
    result += "addi $s2, $v0, 4\n"
    result += "addi $s1, $s1, 1\n"

    # copio deste ($s0) una cantidad de ($s1) bytes en ($s3)
    result += "jal copy_from_to\n"

    return result

def convert_TypeAddressNode(instruction):
    global DATA, PARAMS

    result = ""

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t0, type_" + instruction.type_name + "\n"
    result += "la $t1, " + dest + "\n"
    result += "sw $t0, 4($t1)\n"

    return result

def convert_PrintIntNode(instruction):
    global DATA, PARAMS

    result = ""

    if instruction.val in PARAMS:
        dest = PARAMS[instruction.val]
    else:
        dest = instruction.val


    result += "la $s0, " + dest + "\n"
    result += "jal print_int_func\n"

    return result


def convert_LocalSaveNode(instruction):
    global CURR_LOCAL_COUNT
    result = "li $s0, " + str(CURR_LOCAL_COUNT) + "\n"

    result += "jal locals_write\n"    
    return result


def convert_LoadDataNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $s0, " + instruction.data + "\n"

    result += "la $s2, " + dest + "\n"

    result += "jal load_data_func\n"

    return result

def convert_ReadNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s2, " + dest + "\n"

    result += "jal read_string_func\n"

    return result


def convert_ReadIntNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
        
    result += "la $t0, " + dest + "\n"

    result += "jal read_int_func\n"

    return result


def convert_PrintNode(instruction):
    result = ""

    global DATA

    if instruction.str in PARAMS:
        dest = PARAMS[instruction.str]
    else:
        dest = instruction.str
    
    # ponemos en a0 la direccion del string
    result += "la $s0, " + dest + "\n"

    result += "jal print_func\n"

    return result


def convert_ReturnNode(instruction):
    result = ""

    global DATA, PARAMS

    # devolvemos en v0 la direccion en memoria del valor de retorno, si es void seria 0

    if instruction.return_value == "":
        result += "li $v0, 0\n"
    else:
        if instruction.return_value in PARAMS:
            dest = PARAMS[instruction.return_value]
        else:
            dest = instruction.return_value

        result += "la $v0, " + dest + "\n"

    global CURR_PARAM_COUNT

    result += "lw $ra, -4($sp)\n"
    result += "addi $sp, $sp, -" + str(8 * CURR_PARAM_COUNT + 4) + "\n"

    result += "jr $ra\n"

    return result


def convert_TypeOfNode(instruction):
    result = ""
    
    global DATA, PARAMS

    if instruction.variable in PARAMS:
        val = PARAMS[instruction.variable]
    else:
        val = instruction.variable

    result += "la $t0, " + val + "\n"
    
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t1, " + dest + "\n"
    
    result += "lw $t2, ($t0)\n"
    result += "sw $t2, 4($t1)\n"

    return result


def convert_CopyNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value

    result += "la $s6, " + val + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $s7, " + dest + "\n"
    
    result += "jal copy_func\n"

    return result  


def convert_StrlenNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.str in PARAMS:
        val = PARAMS[instruction.str]
    else:
        val = instruction.str
        
    # en t0 va la direccion del string    
    result += "la $t0, " + val + "\n"
    result += "lw $t0, 4($t0)\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    # en $t1 va la direccion donde pondremos el valor de salida
    result += "la $t1, " + dest + "\n"

    result += "lw $t2, ($t0)\n"
    result += "sw $t2, 4($t1)\n"

    return result

def convert_StrcatNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.str_a in PARAMS:
        val_a = PARAMS[instruction.str_a]
    else:
        val_a = instruction.str_a
        
    # en s0 va la direccion del primer string    
    result += "la $s0, " + val_a + "\n"
    

    if instruction.str_b in PARAMS:
        val_b = PARAMS[instruction.str_b]
    else:
        val_b = instruction.str_b
        
    # en s6 va la direccion del segundo string    
    result += "la $s6, " + val_b + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
        
    # en s2 va la direccion del string resultante    
    result += "la $s2, " + dest + "\n"

    result += "jal concat_func\n"

    return result


def convert_StrsubNode(instruction):
    global DATA, PARAMS
    
    result = ""
    
    if instruction.str in PARAMS:
        val = PARAMS[instruction.str]
    else:
        val = instruction.str

    if instruction.i in PARAMS:   
        index = PARAMS[instruction.i]    
    else:
        index = instruction.i 

    if instruction.len in PARAMS:
        lenght = PARAMS[instruction.len]
    else:
        lenght = instruction.len
     
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s0, " + val + "\n"
    result += "la $s7, " + index + "\n"
    result += "la $s1, " + lenght + "\n"
    result += "la $s6, " + dest + "\n"

    result += "jal substring_func\n"

    return result
    

def convert_AllocateNode(instruction):
    result = ""

    global DATA, PARAMS, CIL_TYPES

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $s0, " + dest + "\n"

    if instruction.type == "Int":

        result += "jal allocate_Int\n"
    
    elif instruction.type == "Bool":

        result += "jal allocate_Bool\n"
       
    elif instruction.type == "String":
        
        result += "jal allocate_String\n"

    elif instruction.type == "void":

        result += "jal allocate_Void\n"

    else:
        result += "la $t1, type_" + instruction.type + "\n"
        result += "sw $t1, ($s0)\n"

        object_size = 4
        attrs = []
        for a in CIL_TYPES[instruction.type].attributes.values():
            if a.attribute_name == "self":
                continue
            object_size += 8
            attrs.append(a.attribute_type.name)
        
        result += "li $a0, " + str(object_size) + "\n"
        result += "li $v0, 9\n"
        result += "syscall\n"

        # ponemos la direccion en la variable local correspondiente
        result += "sw $v0, 4($s0)\n"

        # ponemos el tamanyo correspondiente
        result += "sw $a0, ($v0)\n"

        result += "li $t3, 0\n"
        # ponemos las letras correspondientes a cada attributo
        for l in attrs:
            result += "la $t1, type_" + l + "\n"
            result += "sw $t1, 4($v0)\n"
            result += "sw $t3, 8($v0)\n"
            result += "addi $v0, $v0, 8\n"

        global CURR_LOCAL_COUNT, CURR_PARAM_COUNT
        result += "li $s0, " + str(CURR_LOCAL_COUNT) + "\n"
        result += "jal locals_write\n"

        result += "la $s0, " + dest + "\n"
        result += "jal put_argument\n"

        result += "jal " + instruction.type + "_Attributes_Initialization\n"

        result += "li $s0, " + str(CURR_LOCAL_COUNT) + "\n"
        result += "jal locals_load\n"
        result += "li $s0, " + str(CURR_PARAM_COUNT) + "\n"
        result += "jal params_load\n"

    return result
    

def convert_ArgNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value
    
    result += "la $s0, " + val + "\n"

    result += "jal put_argument\n"

    return result


def convert_DispatchCallNode(instruction):
    result = ""

    global DATA, PARAMS, CIL_TYPES

    if instruction.type_addr in PARAMS:
        t_addr = PARAMS[instruction.type_addr]
    else:
        t_addr = instruction.type_addr

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    dispatch_end_label = next_label()

    result += "la $s0, " + t_addr + "\n"
    result += "li $s1, " + str(METHODS_NAME_TO_ID[instruction.method]) + "\n"

    result += "jal call_func\n"

    result += "jal $s3\n"

    result += "lw $s6, ($v0)\n"
    result += "lw $s7, 4($v0)\n"

    global CURR_LOCAL_COUNT, CURR_PARAM_COUNT
    result += "li $s0, " + str(CURR_LOCAL_COUNT) + "\n"
    result += "jal locals_load\n"
    result += "li $s0, " + str(CURR_PARAM_COUNT) + "\n"
    result += "jal params_load\n"

    result += "la $t0, " + dest + "\n"
    result += "sw $s6, ($t0)\n"
    result += "sw $s7, 4($t0)\n"

    return result

def convert_SetAttributeNode(instruction):
    result = ""

    global CIL_TYPES, DATA, PARAMS

    offset = 4

    for a in CIL_TYPES[instruction.type_name].attributes.values():
        if a.attribute_name == "self":
            continue
        if a.attribute_name == instruction.attr:
            break
        offset += 8

    if instruction.instance in PARAMS:
        ins = PARAMS[instruction.instance]
    else:
        ins = instruction.instance
    
    # en t0 metemos la direccion del valor a modificar
    result += "la $t0, " + ins + "\n"
    result += "lw $t0, 4($t0)\n"
    result += "addi $s1, $t0, " + str(offset) + "\n"

    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value


    # en t1 metemos la direccion del valor nuevo
    result += "la $s0, " + val + "\n"

    result += "jal mov_func\n"

    return result


def convert_GetAttributeNode(instruction):
    result = ""

    global CIL_TYPES, DATA, PARAMS

    offset = 4

    for a in CIL_TYPES[instruction.type_name].attributes.values():
        if a.attribute_name == "self":
            continue
        if a.attribute_name == instruction.attr:
            break
        offset += 8

    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value
    
    # en t0 metemos la direccion del valor a devolver
    result += "la $t0, " + val + "\n"
    result += "lw $t0, 4($t0)\n"
    result += "addi $s0, $t0, " + str(offset) + "\n"
    
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $s1, " + dest + "\n"

    result += "jal mov_func\n"
    
    return result


def convert_ENode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    # poner en s0 la direccion del primer dato
    result += "la $s0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right

   # poner en s1 la direccion del segundo dato
    result += "la $s1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    # poner en s2 la direccion del booleano de salida
    result += "la $s2, " + dest + "\n"

    result += "jal equality_function\n"

    return result 


def convert_LNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $s0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $s1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s2, " + dest + "\n"

    result += "jal less_func\n"

    return result 


def convert_LENode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $s0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $s1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s2, " + dest + "\n"

    result += "jal less_equal_func\n"

    return result 


def convert_DivNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $s0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $s1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s2, " + dest + "\n"

    result += "jal divide_func\n"

    return result 


def convert_MulNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $s0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $s1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s2, " + dest + "\n"
    
    result += "jal multiply_func\n"

    return result


def convert_SubNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $s0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $s1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s2, " + dest + "\n"

    result += "jal substract_func\n"

    return result


def convert_AddNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $s0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $s1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $s2, " + dest + "\n"

    result += "jal add_func\n"

    return result


def convert_VDNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value
    
    result += "la $t0, " + val + "\n"
    result += "lw $t0, 4($t0)\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t1, " + dest + "\n"

    result += "seq $t2, $t0, 0\n"
    result += "sw $t2, 4($t1)\n"

    return result


def convert_CmpNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value
    
    result += "la $t0, " + val + "\n"
    result += "lw $t0, 4($t0)\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t1, " + dest + "\n"

    result += "li $t2, -1\n"
    result += "mult $t0, $t2\n"
    result += "mflo $t0\n"
    result += "sw $t0, 4($t1)\n"

    return result

def convert_NtNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value
    
    result += "la $t0, " + val + "\n"
    result += "lw $t0, 4($t0)\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t1, " + dest + "\n"

    result += "seq $t0, $t0, 0\n"
    result += "sw $t0, 4($t1)\n"

    return result


def convert_MovNode(instruction):
    result = ""

    if type(instruction.value) == type(5):
        result += "li $t0, " + str(instruction.value) + "\n"
        result += "la $t1, " + instruction.result + "\n"
        result += "sw $t0, 4($t1)\n"
    elif type(instruction.value) == type(True):
        if instruction.value:
            result += "li $t0, 1\n"
        else:
            result += "li $t0, 0\n"
        result += "la $t1, " + instruction.result + "\n"
        result += "sw $t0, 4($t1)\n"
    else:
        if instruction.value in PARAMS:
            val = PARAMS[instruction.value]
        else:
            val = instruction.value
        
        if instruction.result in PARAMS:
            res = PARAMS[instruction.result]
        else:
            res = instruction.result

        result += "la $s0, " + val + "\n"
        result += "la $s1, " + res + "\n"

        result += "jal mov_func\n"

    return result

def convert_AbortNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.caller_type in PARAMS:
        caller = PARAMS[instruction.caller_type]
    else:
        caller = instruction.caller_type
    
    result += "la $s0, " + caller + "\n"

    result += "jal abort\n"

    return result


def convert_IfGotoNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.predicate in PARAMS:
        pred = PARAMS[instruction.predicate]
    else:
        pred = instruction.predicate

    result += "la $t0, " + pred + "\n"
    result += "lw $t0, 4($t0)\n"
    result += "beq $t0, 1, " + instruction.label + "\n"

    return result


def convert_GotoNode(instruction):
    return "j " + instruction.label + "\n"


def convert_LabelNode(instruction):
    return instruction.label_name + ":\n"