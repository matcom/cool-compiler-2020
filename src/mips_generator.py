from cil_ast import *

DATA = []
CIL_TYPES = {}
LABELS_COUNT = 0
PARAM_COUNT = 0
MAX_LOCALS_COUNT = 0

def next_label():
    global LABELS_COUNT
    result = "custom_label_" + str(LABELS_COUNT)
    LABELS_COUNT += 1
    return result


def generate_mips(cil):
    global CIL_TYPES, LABELS_COUNT
    LABELS_COUNT = 0
    CIL_TYPES = cil[0]

    data = generate_data(cil[1], cil[3], cil[4])
    code = generate_code(cil[2], cil[6])

    return data + code


def generate_data(data, locals, max_param_count):
    global DATA, CIL_TYPES, MAX_LOCALS_COUNT
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
PARAMS_LOAD = ""

def generate_locals_write():
    result = "locals_write:\n"

    global MAX_LOCALS_COUNT
    for i in range(0, MAX_LOCALS_COUNT):
        name = "local_" + str(i)
        result += "la $t1, " + name + "\n"
        result += "lw $t0, ($t1)\n"
        result += "sw $t0, ($sp)\n"
        result += "lw $t0, 4($t1)\n"
        result += "sw $t0, 4($sp)\n"
        result += "addi $sp, $sp, 8\n"

    result += "jr $ra\n\n"

    return result

def generate_locals_load():
    result = "locals_load:\n"

    global MAX_LOCALS_COUNT
    for i in range(0, MAX_LOCALS_COUNT):
        name = "local_" + str(i)
        result += "lw $t0, -" + str((MAX_LOCALS_COUNT - i) * 8) + "($sp)\n"
        result += "lw $t1, -" + str((MAX_LOCALS_COUNT - i) * 8 - 4) + "($sp)\n"
        result += "la $t2, " + name + "\n"
        result += "sw $t0, ($t2)\n"
        result += "sw $t1, 4($t2)\n"

    result += "addi $sp, $sp, -" + str(8 * MAX_LOCALS_COUNT) + "\n"

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

    result += "lw $t0, -8($sp)\n"
    result += "lw $t1, -4($sp)\n"
    result += "addi $sp, $sp, -8\n"

    result += "li $v0, 0\n"

    is_descendant_end_label = next_label()

    for t in son_father_tuples:
        is_descendant_next_label = next_label()
        result += "la $t2, type_" + t[0] + "\n"
        result += "la $t3, type_" + t[1] + "\n"
        result += "seq $t2, $t2, $t0\n"
        result += "seq $t3, $t3, $t1\n"
        result += "add $t2, $t2, $t3\n"
        result += "bne $t2, 2, " + is_descendant_next_label + "\n"
        result += "li $v0, 1\n"
        result += "j " + is_descendant_end_label + "\n"
        result += is_descendant_next_label + ":\n"

    result += is_descendant_end_label + ":\n"

    result += "jr $ra\n\n"

    return result

def generate_code(functions_code, son_father_tuples):
    result = ".text\n\n"

    result += generate_locals_write()
    result += generate_locals_load()
    result += generate_allocate_Int()
    result += generate_allocate_Bool()
    result += generate_allocate_String()
    result += generate_allocate_Void()
    result += generate_is_descendant(son_father_tuples)
    

    global PARAMS, CURR_PARAM_COUNT, PARAM_COUNT, PARAMS_LOAD

    for f in functions_code:
        CURR_PARAM_COUNT = 0
        PARAMS_LOAD = ""

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
            
            PARAMS_LOAD += "lw $t0, -" + str(8 * counter + 4) + "($sp)\n"
            PARAMS_LOAD += "lw $t1, -" + str(8 * counter) + "($sp)\n"
            PARAMS_LOAD += "la $t2, " + param_name + "\n"
            PARAMS_LOAD += "sw $t0, ($t2)\n"
            PARAMS_LOAD += "sw $t1, 4($t2)\n"

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

    result += "la $t0, " + son + "\n"
    result += "lw $t0, 4($t0)\n"

    result += "la $t1, " + father + "\n"
    result += "lw $t1, 4($t1)\n"

    result += "sw $t0, ($sp)\n"
    result += "sw $t1, 4($sp)\n"
    result += "addi $sp, $sp, 8\n"

    result += "jal is_descendant\n"

    result += "la $t3, " + dest + "\n"
    result += "sw $v0, 4($t3)\n"

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

    result += "la $t0, " + t_addr + "\n"
    result += "lw $t0, 4($t0)\n"
    result += get_length_with_registers("$t0", "$t1", "$t2")
    result += "la $t0, " + t_addr + "\n"
    result += "lw $t0, 4($t0)\n"

    result += "la $t2, " + dest + "\n"
    
    result += "addi $a0, $t1, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($t2)\n"
    result += "sw $t1, ($v0)\n"

    t_name_loop_start_label = next_label()

    result += "li $t3, 0\n"
    result += t_name_loop_start_label + ":\n"
    result += "lb $t3, ($t0)\n"
    result += "sb $t3, 4($v0)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $v0, $v0, 1\n"
    result += "bne $t3, 0, " + t_name_loop_start_label + "\n"

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


    result += "la $t0, " + dest + "\n"
    result += "lw $a0, 4($t0)\n"
    result += "li $v0, 1\n"
    result += "syscall\n"

    return result


def convert_LocalSaveNode(instruction):
    result = "jal locals_write\n"    
    return result
def convert_LoadDataNode(instruction):
    result = ""

    result += "la $t0, " + instruction.data + "\n"
    result += get_length_with_registers("$t0", "$t1", "$t2")
    result += "la $t0, " + instruction.data + "\n"

    global DATA, PARAMS

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t2, " + dest + "\n"
    
    result += "addi $a0, $t1, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($t2)\n"
    result += "sw $t1, ($v0)\n"


    load_data_loop_start_label = next_label()

    result += "li $t3, 0\n"
    result += load_data_loop_start_label + ":\n"
    result += "lb $t3, ($t0)\n"
    result += "sb $t3, 4($v0)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $v0, $v0, 1\n"
    result += "bne $t3, 0, " + load_data_loop_start_label + "\n"

    return result

def convert_ReadNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    # ponemos en a0 la direccion a que apunta la variable local 
    result += "la $a0, string_read_buffer\n"
    result += "li $v0, 8\n"
    result += "syscall\n"

    # ponemos en t2 la direccion del string leido
    result += "addi $t2, $a0, 0\n"

    # ponemos en t0 la cantidad de caracteres (contando el '\n' del final)
    result += get_length_with_registers("$a0", "$t0", "$t1")
    result += "addi $t0, $t0, -1\n"

    # ponemos en t1 la dieccion de destino
    result += "la $t1, " + dest + "\n"

    result += "addi $a0, $t0, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($t1)\n"
    result += "sw $t0, ($v0)\n"

    read_node_loop_start = next_label()
    read_node_loop_end = next_label()

    result += "li $t0, 0\n"
    result += read_node_loop_start + ":\n"
    result += "lb $t0, ($t2)\n"
    result += "sb $t0, 4($v0)\n"
    result += "beq $t0, 10, " + read_node_loop_end + "\n"
    result += "addi $t2, $t2, 1\n"
    result += "addi $v0, $v0, 1\n"
    result += "j " + read_node_loop_start + "\n"
    result += read_node_loop_end + ":\n"
    result += "li $t0, 0\n"
    result += "sb $t0, 4($v0)\n"

    return result


def convert_ReadIntNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
        
    # leemos el numero
    result += "li $v0, 5\n"
    result += "syscall\n"

    result += "la $t0, " + dest + "\n"
    
    result += "sw $v0, 4($t0)\n"

    return result


def convert_PrintNode(instruction):
    result = ""

    global DATA

    if instruction.str in PARAMS:
        dest = PARAMS[instruction.str]
    else:
        dest = instruction.str
    
    # ponemos en a0 la direccion del string
    result += "la $a0, " + dest + "\n"
    result += "lw $a0, 4($a0)\n"
    result += "addi $a0, $a0, 4\n"
    
    result += "li $v0, 4\n"
    result += "syscall\n"

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
    result += "addi $sp, $sp, -" + str(8 * (CURR_PARAM_COUNT) + 4) + "\n"

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

    result += "la $t0, " + val + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t1, " + dest + "\n"

    # primero copiar la direccion del tipo de dato
    result += "lw $t2, ($t0)\n"
    result += "sw $t2, ($t1)\n"
    
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
    result += "lw $t0, 4($t0)\n"
    result += "lw $a0, ($t0)\n"
    result += "li $v0, 9\n"
    result += "syscall\n"
    result += "sw $v0, 4($t1)\n"
    result += "add $a0, $t0, $a0\n"
    result += copy_object_loop_start_label + ":\n"
    result += "lw $t3, ($t0)\n"
    result += "sw $t3, ($v0)\n"
    result += "addi $t0, $t0, 4\n"
    result += "addi $v0, $v0, 4\n"
    result += "bne $t0, $a0, " + copy_object_loop_start_label + "\n"
    result += "j " + copy_end_label + "\n"
    result += copy_int_or_bool_label + ":\n"
    result += "lw $t2, 4($t0)\n"
    result += "sw $t2, 4($t1)\n"
    result += "j " + copy_end_label + "\n"
    result += copy_string_label + ":\n"
    result += "lw $t0, 4($t0)\n"
    result += "lw $t6, ($t0)\n"
    result += "addi $a0, $t6, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"
    result += "sw $v0, 4($t1)\n"
    result += "sw $t6, ($v0)\n"
    result += copy_string_loop_start_label + ":\n"
    result += "lb $t3, 4($t0)\n"
    result += "sb $t3, 4($v0)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $v0, $v0, 1\n"
    result += "bne $t3, 0, " + copy_string_loop_start_label + "\n"
    result += copy_end_label + ":\n"

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
        
    # en t0 va la direccion del primer string    
    result += "la $t0, " + val_a + "\n"
    result += "lw $t0, 4($t0)\n"

    if instruction.str_b in PARAMS:
        val_b = PARAMS[instruction.str_b]
    else:
        val_b = instruction.str_b
        
    # en t1 va la direccion del segundo string    
    result += "la $t1, " + val_b + "\n"
    result += "lw $t1, 4($t1)\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
        
    # en t2 va la direccion del string resultante    
    result += "la $t2, " + dest + "\n"
    
    result += "lw $a0, ($t0)\n"
    result += "lw $t3, ($t1)\n"
    result += "add $a0, $a0, $t3\n"
    result += "addi $a0, $a0, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($t2)\n"
    result += "addi $a0, $a0, -5\n"
    result += "sw $a0, ($v0)\n"

    strcat_first_start_label = next_label()
    strcat_first_done_label = next_label()
    strcat_second_start_label = next_label()

    # copiamos primero el primer string
    result += "li $t3, 0\n"
    result += strcat_first_start_label + ":\n"
    result += "lb $t3, 4($t0)\n"
    result += "beq $t3, 0, " + strcat_first_done_label + "\n"
    result += "sb $t3, 4($v0)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $v0, $v0, 1\n"
    result += "j " + strcat_first_start_label + "\n"
    result += strcat_first_done_label + ":\n"
    # copiamos despues el segundo string
    result += strcat_second_start_label + ":\n"
    result += "lb $t3, 4($t1)\n"
    result += "sb $t3, 4($v0)\n"
    result += "addi $t1, $t1, 1\n"
    result += "addi $v0, $v0, 1\n"
    result += "bne $t3, 0, " + strcat_second_start_label + "\n"

    return result


def convert_StrsubNode(instruction):
    global DATA, PARAMS
    
    result = ""
    
    if instruction.str in PARAMS:
        val = PARAMS[instruction.str]
    else:
        val = instruction.str
    
    # en t0 metemos la direccion del string
    result += "la $t0, " + val + "\n"
    result += "lw $t0, 4($t0)\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.i in PARAMS:   
        index = PARAMS[instruction.i]    
    else:
        index = instruction.i 
    
    # en t1 metemos el entero del indice donde empieza la subcadena
    result += "la $t1, " + index + "\n"
    result += "lw $t1, 4($t1)\n"

    # ponemos en t0 la direccion del inicio de la subcadena
    result += "add $t0, $t0, $t1\n"

    if instruction.len in PARAMS:
        lenght = PARAMS[instruction.len]
    else:
        lenght = instruction.len
     
    # en t1 ponemos el entero q dice la cantidad de caracteres a copiar
    result += "la $t1, " + lenght + "\n"
    result += "lw $t1, 4($t1)\n"

    # en t1 dejamos la direccion del final de la subcadena
    result += "add $t1, $t0, $t1\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
        
    # en t2 va la direccion donde pondremos la subcadena resultante
    result += "la $t2, " + dest + "\n"

    result += "sub $a0, $t1, $t0\n"
    result += "addi $a0, $a0, 5\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($t2)\n"
    result += "addi $a0, $a0, -5\n"
    result += "sw $a0, ($v0)\n"


    strsub_loop_start_label = next_label()
    strsub_loop_end_label = next_label()

    result += strsub_loop_start_label + ":\n"
    result += "beq $t0, $t1, " + strsub_loop_end_label + "\n"
    # pasamos caracter a caracter de t0 a t2
    result += "lb $t3, ($t0)\n"
    result += "sb $t3, 4($v0)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $v0, $v0, 1\n"
    result += "j " + strsub_loop_start_label + "\n"
    result += strsub_loop_end_label + ":\n"
    # ponemos \0 al final de la cadena resultante
    result += "li $t3, 0\n"
    result += "sb $t3, 4($v0)\n"

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

        # ponemos 0 en t3
        result += "li $t3, 0\n"

        # ponemos las letras correspondientes a cada attributo
        for l in attrs:
            result += "la $t1, type_" + l + "\n"
            result += "sw $t1, 4($v0)\n"
            result += "sw $t3, 8($v0)\n"
            result += "addi $v0, $v0, 8\n"

    return result
    

def convert_ArgNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value
    
    result += "la $t0, " + val + "\n"
    result += "lw $t1, ($t0)\n"
    result += "sw $t1, ($sp)\n"
    result += "lw $t1, 4($t0)\n"
    result += "sw $t1, 4($sp)\n"
    result += "addi $sp, $sp, 8\n"

    return result


def convert_DispatchCallNode(instruction):
    result = ""

    global DATA, PARAMS, PARAMS_LOAD, CIL_TYPES

    if instruction.type_addr in PARAMS:
        t_addr = PARAMS[instruction.type_addr]
    else:
        t_addr = instruction.type_addr

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    dispatch_end_label = next_label()

    result += "la $t0, " + t_addr + "\n"
    result += "lw $t0, 4($t0)\n"

    for t in CIL_TYPES.values():

        if not (instruction.method in t.methods):
            continue

        dispatch_next_type_label = next_label()

        result += "la $t1, type_" + t.type_name + "\n"
        result += "bne $t0, $t1, " + dispatch_next_type_label + "\n"

        result += "jal " + t.methods[instruction.method] + "_" + instruction.method + "\n"

        result += "j " + dispatch_end_label + "\n"

        result += dispatch_next_type_label + ":\n"

    result += dispatch_end_label + ":\n"

    result += "lw $t6, ($v0)\n"
    result += "lw $t7, 4($v0)\n"

    result += "jal locals_load\n"
    result += PARAMS_LOAD

    result += "la $t0, " + dest + "\n"
    result += "sw $t6, ($t0)\n"
    result += "sw $t7, 4($t0)\n"

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
    result += "addi $t0, $t0, " + str(offset) + "\n"

    if instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    else:
        val = instruction.value


    # en t1 metemos la direccion del valor nuevo
    result += "la $t1, " + val + "\n"

    result += "lw $t2, ($t1)\n"
    result += "sw $t2, ($t0)\n"
    result += "lw $t2, 4($t1)\n"
    result += "sw $t2, 4($t0)\n"

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
    result += "addi $t0, $t0, " + str(offset) + "\n"
    
    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t1, " + dest + "\n"

    result += "lw $t2, ($t0)\n"
    result += "sw $t2, ($t1)\n"
    result += "lw $t2, 4($t0)\n"
    result += "sw $t2, 4($t1)\n"
    
    return result


def convert_ENode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    # poner en t0 la direccion del primer dato
    result += "la $t0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right

   # poner en t1 la direccion del segundo dato
    result += "la $t1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    # poner en t2 la direccion donde se pondra 0 o 1
    result += "la $t2, " + dest + "\n"

    compare_strings_label = next_label()
    compare_strings_false_label = next_label()
    compare_strings_loop_label = next_label()
    equal_end_label = next_label()

    result += "lw $t3, ($t0)\n"
    result += "la $t4, type_String\n"
    result += "lw $t0, 4($t0)\n"
    result += "lw $t1, 4($t1)\n"
    result += "beq $t3, $t4, " + compare_strings_label + "\n"
    result += "seq $t0, $t0, $t1\n"
    result += "j " + equal_end_label + "\n"
    result += compare_strings_label + ":\n"
    result += "lw $t3, ($t0)\n"
    result += "lw $t4, ($t1)\n"
    result += "bne $t3, $t4, " + compare_strings_false_label + "\n"
    result += "li $t3, 0\n"
    result += "li $t4, 0\n"
    result += compare_strings_loop_label + ":\n"
    result += "lb $t3, 4($t0)\n"
    result += "lb $t4, 4($t1)\n"
    result += "bne $t3, $t4, " + compare_strings_false_label + "\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $t1, $t1, 1\n"
    result += "bne $t3, 0, " + compare_strings_loop_label + "\n"
    result += "li $t0, 1\n"
    result += "j " + equal_end_label + "\n"
    result += compare_strings_false_label + ":\n"
    result += "li $t0, 0\n"
    result += equal_end_label + ":\n"
    result += "sw $t0, 4($t2)\n"

    return result 


def convert_LNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $t0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $t1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $t2, " + dest + "\n"

    result += "lw $t0, 4($t0)\n"
    result += "lw $t1, 4($t1)\n"
    result += "slt $t0, $t0, $t1\n"
    result += "sw $t0, 4($t2)\n"

    return result 


def convert_LENode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $t0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $t1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $t2, " + dest + "\n"

    result += "lw $t0, 4($t0)\n"
    result += "lw $t1, 4($t1)\n"
    result += "sle $t0, $t0, $t1\n"
    result += "sw $t0, 4($t2)\n"

    return result 


def convert_DivNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $t0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $t1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $t2, " + dest + "\n"

    result += "lw $t0, 4($t0)\n"
    result += "lw $t1, 4($t1)\n"
    result += "div $t0, $t0, $t1\n"
    result += "sw $t0, 4($t2)\n"

    return result 


def convert_MulNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $t0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $t1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $t2, " + dest + "\n"
    
    result += "lw $t0, 4($t0)\n"
    result += "lw $t1, 4($t1)\n"
    result += "mult $t0, $t1\n"
    result += "mflo $t0\n"
    result += "sw $t0, 4($t2)\n"

    return result


def convert_SubNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $t0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $t1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $t2, " + dest + "\n"

    result += "lw $t0, 4($t0)\n"
    result += "lw $t1, 4($t1)\n"
    result += "sub $t0, $t0, $t1\n"
    result += "sw $t0, 4($t2)\n"

    return result


def convert_AddNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    else:
        left = instruction.left
    
    result += "la $t0, " + left + "\n"

    if instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right
   
    result += "la $t1, " + right + "\n"

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result
    
    result += "la $t2, " + dest + "\n"

    result += "lw $t0, 4($t0)\n"
    result += "lw $t1, 4($t1)\n"
    result += "add $t0, $t0, $t1\n"
    result += "sw $t0, 4($t2)\n"

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
    else:
        if instruction.value in PARAMS:
            val = PARAMS[instruction.value]
        else:
            val = instruction.value
        
        if instruction.result in PARAMS:
            res = PARAMS[instruction.result]
        else:
            res = instruction.result

        result += "la $t0, " + val + "\n"
        result += "la $t1, " + res + "\n"

        result += "lw $t2, ($t0)\n"
        result += "sw $t2, ($t1)\n"

        result += "lw $t2, 4($t0)\n"
        result += "sw $t2, 4($t1)\n"

    return result


def convert_SetStringNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    else:
        dest = instruction.result

    result += "la $t0, " + dest + "\n"

    result += "li $a0, " + str(4 + len(instruction.str) + 1) + "\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, 4($t0)\n"
    result += "li $t0, " + str(len(instruction.str)) + "\n"
    result += "sw $t0, ($v0)\n"

    for c in instruction.str:
        result += "li $t0, '" + c + "'\n"
        result += "sb $t0, 4($v0)\n"
        result += "addi $v0, $v0, 1\n"

    result += "li $t0, 0\n"
    result += "sb $t0, 4($v0)\n"

    return result





def convert_AbortNode(instruction):
    result = ""

    # write abort message
    result += "la $a0, abort_msg\n"
    result += "li $v0, 4\n"
    result += "syscall\n"

    global DATA, PARAMS

    if instruction.caller_type in PARAMS:
        caller = PARAMS[instruction.caller_type]
    else:
        caller = instruction.caller_type
    
    result += "la $t0, " + caller + "\n"
    
    # write type who called abort
    result += "lw $a0, 4($t0)\n"
    result += "li $v0, 4\n"
    result += "syscall\n"

    # write an end of line
    result += "la $a0, end_of_line\n"
    result += "li $v0, 4\n"
    result += "syscall\n"

    result += "li $v0, 10\n"
    result += "syscall\n"

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

def get_length_with_registers(str_reg, val_reg, aux_reg):
    result = ""

    end_label = next_label()
    loop_label = next_label()

    result += "li " + val_reg + ", 0\n"
    result += loop_label + ":\n"
    result += "lb " + aux_reg + ", (" + str_reg + ")\n"
    result += "beq " + aux_reg + ", 0, " + end_label + "\n"
    result += "addi " + val_reg + ", " + val_reg + ", 1\n"
    result += "addi " + str_reg + ", " + str_reg + ", 1\n"
    result += "j " + loop_label + "\n"
    result += end_label + ":\n"

    return result