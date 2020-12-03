from cil_ast import *

DATA = []
CIL_TYPES = {}
LABELS_COUNT = 0
PARAM_COUNT = 0

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
    code = generate_code(cil[2])

    return data + code


def generate_data(data, locals, max_param_count):
    global DATA, CIL_TYPES
    
    if len(data) == 0 and len(locals) == 0:
        return ""

    result = ".data\n\n"

    for t in CIL_TYPES.values():
        result += "type_" + t.type_name + ": .asciiz \"" + t.type_name + "\"\n"

    for l in locals.values():
        DATA.append(l.id)
        result += l.id + ": .word 0\n"

    for d in data.values():
        DATA.append(d.id)
        result += d.id + ": .asciiz \"" + d.value.replace("\n", "\\n") + "\"\n"

    global PARAMS
    
    for i in range(0, max_param_count):
        result += "param_" + str(i) + ": .word 0\n"
        PARAMS["param_" + str(i)] = None

    result += "\n\n"

    return result

PARAMS = {}
CURR_PARAM_COUNT = 0
LOCALS_WRITE = ""
PARAMS_AND_LOCALS_RELOAD = ""

def generate_code(functions_code):
    result = ".text\n\n"

    global PARAMS, CURR_PARAM_COUNT, PARAM_COUNT, LOCALS_WRITE, PARAMS_AND_LOCALS_RELOAD

    for f in functions_code:
        CURR_PARAM_COUNT = 0
        PARAMS_LOAD = ""
        LOCALS_LOAD = ""
        LOCALS_WRITE = "" 

        result += f.name + ":\n"

        counter = len(f.locals)
        for l in f.locals:
            local_name = l.id
            
            LOCALS_WRITE += "lw $t0, " + local_name + "\n"
            LOCALS_WRITE += "sw $t0, ($sp)\n"
            LOCALS_WRITE += "addi $sp, $sp, 4\n"

            LOCALS_LOAD += "lw $t0, -" + str(counter * 4) + "($sp)\n"
            LOCALS_LOAD += "sw $t0, " + local_name + "\n"

            counter -= 1

        LOCALS_LOAD += "addi $sp, $sp, -" + str(4 * len(f.locals)) + "\n"

        counter = len(f.params)

        for p in f.params:
            param_name = "param_" + str(PARAM_COUNT)
            PARAM_COUNT += 1
            PARAMS[p.id] = param_name
            result += "lw $t0, -" + str(4 * counter) + "($sp)\n"
            result += "sw $t0, " + param_name + "\n"
            
            PARAMS_LOAD += "lw $t0, -" + str(4 * counter + 4) + "($sp)\n"
            PARAMS_LOAD += "sw $t0, " + param_name + "\n"

            counter -= 1
            CURR_PARAM_COUNT += 1

        PARAMS_AND_LOCALS_RELOAD = LOCALS_LOAD + PARAMS_LOAD

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

    elif type(instruction) == ReturnNode:
        return convert_ReturnNode(instruction)

    elif type(instruction) == ToStrNode:
        return convert_ToStrNode(instruction)

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

    global DATA, PARAMS
    
    if instruction.son in DATA:
        son = instruction.son
    else:
        son = PARAMS[instruction.son]
    
    if instruction.father in DATA:
        father = instruction.father
    else:
        father = PARAMS[instruction.father]

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]
    

    result += "addi $sp, $sp, 4\n"
    result += "lw $t0, " + son + "\n"
    result += "sw $t0, ($sp)\n"
    result += "addi $sp, $sp, 4\n"
    result += "lw $t0, " + father + "\n"
    result += "sw $t0, ($sp)\n"
    result += "addi $sp, $sp, 4\n"
    result += "jal is_son\n"
    result += "sw $v0, " + dest + "\n"

    return result


def convert_LocalSaveNode(instruction):
    global LOCALS_WRITE
    return LOCALS_WRITE
def convert_LoadDataNode(instruction):
    result = ""

    result += "la $t0, " + instruction.data + "\n"

    global DATA, PARAMS

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    result += "lw $t1, " + dest + "\n"
    result += "addi $t1, $t1, 4\n"

    load_data_loop_start_label = next_label()

    result += "li $t3, 0\n"
    result += load_data_loop_start_label + ":\n"
    result += "lb $t3, ($t0)\n"
    result += "sb $t3, ($t1)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $t1, $t1, 1\n"
    result += "bne $t3, 0, " + load_data_loop_start_label + "\n"

    return result

def convert_ReadNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]
    
    # ponemos en a0 la direccion a que apunta la variable local 
    result += "lw $a0, " + dest + "\n"
    result += "addi $a0, $a0, 4\n"
    result += "li $v0, 8\n"
    result += "syscall\n"

    read_node_loop_start = next_label()
    read_node_loop_end = next_label()

    result += read_node_loop_start + ":\n"
    result += "lb $t0, ($a0)\n"
    result += "beq $t0, 10, " + read_node_loop_end + "\n"
    result += "addi $a0, $a0, 1\n"
    result += "j " + read_node_loop_start + "\n"
    result += read_node_loop_end + ":\n"
    result += "li $t0, 0\n"
    result += "sb $t0, ($a0)\n"

    return result


def convert_ReadIntNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    # leemos el numero
    result += "li $v0, 5\n"
    result += "syscall\n"

    # ponemos 'I' al principio de donde empieza el entero en memoria
    result += "lw $t0, " + dest + "\n"
    
    result += "li $t1, 'I'\n"
    result += "sw $t1, ($t0)\n"
    
    # ponemos el entero despues de la 'I' en memoria
    result += "sw $v0, 4($t0)\n"

    return result


def convert_PrintNode(instruction):
    result = ""

    global DATA

    if instruction.str in DATA:
        dest = instruction.str
    else:
        dest = PARAMS[instruction.str]
    
    # ponemos en a0 la direccion del string(sumamos uno pq ls string tienen una 'S' delante)
    result += "lw $a0, " + dest + "\n"
    result += "addi $a0, $a0, 4\n"
    
    result += "li $v0, 4\n"
    result += "syscall\n"

    return result


def convert_ReturnNode(instruction):
    result = ""

    global DATA

    # devolvemos en v0 la direccion en memoria del valor de retorno, si es void seria 0

    if instruction.return_value == "":
        result += "li $v0, 0\n"
    else:
        if instruction.return_value in DATA:
            dest = instruction.return_value
        else:
           dest = PARAMS[instruction.return_value]
        
        result += "lw $v0, " + dest + "\n"

    global CURR_PARAM_COUNT

    result += "lw $ra, -4($sp)\n"
    result += "addi $sp, $sp, -" + str(4 * (CURR_PARAM_COUNT + 1)) + "\n"

    result += "jr $ra\n"

    return result


def convert_TypeOfNode(instruction):
    result = ""
    
    global DATA, PARAMS

    if instruction.variable in DATA:
        val = instruction.variable
    else:
        val = PARAMS[instruction.variable]

    result += "lw $t0, " + val + "\n"
    
    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    result += "lw $t1, " + dest + "\n"
    result += "addi $t1, $t1, 4\n"

    typeof_int_case_label = next_label()
    typeof_bool_case_label = next_label()
    typeof_string_case_label = next_label()
    typeof_string_copy_start_label = next_label()
    typeof_end_label = next_label()

    result += "li $t2, 0\n"
    result += "lb $t2, ($t0)\n"
    result += "beq $t2, 'I', " + typeof_int_case_label + "\n"
    result += "beq $t2, 'B', " + typeof_bool_case_label + "\n"
    result += "beq $t2, 'S', " + typeof_string_case_label + "\n"
    # aqui se llegaria si el valor no fuera de ningun tipo basico
    result += "addi $t0, $t0, 4\n"
    result += "lw $t2, ($t0)\n"
    result += typeof_string_copy_start_label + ":\n"
    result += "lb $t3, ($t2)\n"
    result += "sb $t3, ($t1)\n"
    result += "beq $t3, 0, " + typeof_end_label + "\n"
    result += "addi $t2, $t2, 1\n"
    result += "addi $t1, $t1, 1\n"
    result += "j " + typeof_string_copy_start_label + "\n"
    # si el valor es de tipo entero
    result += typeof_int_case_label + ":\n"
    result += "li $t2, 'I'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'n'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 't'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 0\n"
    result += "sb $t2, ($t1)\n"
    result += "j " + typeof_end_label + "\n"
    # si el valor es de tipo booleano
    result += typeof_bool_case_label + ":\n"
    result += "li $t2, 'B'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'o'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'o'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'l'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 0\n"
    result += "sb $t2, ($t1)\n"
    result += "j " + typeof_end_label + "\n"
    # si el valor es de tipo string
    result += typeof_string_case_label + ":\n"
    result += "li $t2, 'S'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 't'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'r'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'i'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'n'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 'g'\n"
    result += "sb $t2, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "li $t2, 0\n"
    result += "sb $t2, ($t1)\n"
    result += typeof_end_label + ":\n"

    return result


def convert_CopyNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in DATA:
        val = instruction.value
    else:
        val = PARAMS[instruction.value]

    result += "lw $t0, " + val + "\n"

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    
    copy_object_start_label = next_label()
    copy_string_start_label = next_label()
    copy_other_start_label = next_label()
    copy_end_label = next_label()

    result += "li $t1, 0\n"
    result += "lb $t1, ($t0)\n"
    result += "beq $t1, 'O', " + copy_object_start_label + "\n"
    result += "beq $t1, 'S', " + copy_string_start_label + "\n"
    result += "j " + copy_other_start_label + "\n"
    # ponemos en t2 el tamanyo del objeto a copiar
    result += copy_object_start_label + ":\n"
    result += "addi $t2, $t0, 8\n"
    result += "lw $t2, ($t2)\n"

    result += "addi $a0, $t2, 0\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, " + dest + "\n"
    result += "addi $t1, $v0, 0\n"

    # ponemos en t2 la direccion hasta donde se debe copiar
    result += "add $t2, $t0, $t2\n"

    # copiamos desde t0 a t2 todo en el destino (t1)
    copy_object_loop_start_label = next_label()

    result += copy_object_loop_start_label + ":\n"
    result += "lb $t3, ($t0)\n"
    result += "sb $t3, ($t1)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $t1, $t1, 1\n"
    result += "bne $t0, $t2, " + copy_object_loop_start_label + "\n"

    result += "j " + copy_end_label + "\n"


    # aqui es si el valor es string
    result += copy_string_start_label + ":\n"

    result += "li $a0, 1028\n"
    result += "li $v0, 9\n"
    result += "syscall\n"

    result += "sw $v0, " + dest + "\n"
    result += "addi $t1, $v0, 0\n"


    # ponemos en t2 la direccion hasta donde se debe copiar
    result += "addi $t2, $t0, 1028\n"

    # copiamos desde t0 a t2 todo en el destino (t1)
    copy_string_loop_start_label = next_label()

    result += copy_string_loop_start_label + ":\n"
    result += "lb $t3, ($t0)\n"
    result += "sb $t3, ($t1)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $t1, $t1, 1\n"
    result += "bne $t0, $t2, " + copy_string_loop_start_label + "\n"
    result += "j " + copy_end_label + "\n"

    result += copy_other_start_label + ":\n"
    
    result += "li $a0, 8\n"
    result += "li $v0, 9\n"
    result += "syscall\n"
    result += "sw $v0, " + dest + "\n"

    result += "lw $t3, ($t0)\n"
    result += "sw $t3, ($v0)\n"
    result += "lw $t3, 4($t0)\n"
    result += "sw $t3, 4($v0)\n"

    result += copy_end_label + ":\n"

    return result  


def convert_StrlenNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.str in DATA:
        val = instruction.str
    else:
        val = PARAMS[instruction.str]
        
    # en t0 va la direccion del string    
    result += "lw $t0, " + val + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]
    
    # en $t1 va la direccion donde pondremos el valor de salida
    result += "lw $t1, " + dest + "\n"
    result += "addi $t1, $t1, 4\n"

    # en t2 vamos metiendo el caracter actual q vamos comprobando
    result += "li $t2, 0\n"
    result += "lb $t2, ($t0)\n"
    # y en t3 el contador de cantidad de caracteres
    result += "li $t3, 0\n"

    strlen_loop_start_label = next_label()
    strlen_loop_end_label = next_label()

    result += strlen_loop_start_label + ":\n"
    # si en t2 hay un '\0' terminamos
    result += "beq $t2, 0, " + strlen_loop_end_label + "\n"
    # aumentamos 1 al valor de retorno
    result += "addi $t3, $t3, 1\n"
    # aumentamos uno a la direccion en memoria
    result += "addi $t0, $t0, 1\n"
    # actualizamos t2 con el siguiente caracter
    result += "lb $t2, ($t0)\n"
    result += "j " + strlen_loop_start_label + "\n"
    result += strlen_loop_end_label + ":\n"

    # ponemos la 'I' y el valor correspondiente en memoria
    result += "sw $t3, ($t1)\n"

    return result

def convert_StrcatNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.str_a in DATA:
        val_a = instruction.str_a
    else:
        val_a = PARAMS[instruction.str_a]
        
    # en t0 va la direccion del primer string    
    result += "lw $t0, " + val_a + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.str_b in DATA:
        val_b = instruction.str_b
    else:
        val_b = PARAMS[instruction.str_b]
        
    # en t1 va la direccion del segundo string    
    result += "lw $t1, " + val_b + "\n"
    result += "addi $t1, $t1, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]
        
    # en t2 va la direccion del string resultante    
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    strcat_first_start_label = next_label()
    strcat_first_done_label = next_label()
    strcat_second_start_label = next_label()

    # copiamos primero el primer string
    result += strcat_first_start_label + ":\n"
    result += "lb $t3, ($t0)\n"
    result += "beq $t3, $0, " + strcat_first_done_label + "\n"
    result += "sb $t3, ($t2)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $t2, $t2, 1\n"
    result += "j " + strcat_first_start_label + "\n"
    result += strcat_first_done_label + ":\n"
    # copiamos despues el segundo string
    result += strcat_second_start_label + ":\n"
    result += "lb $t3, ($t1)\n"
    result += "sb $t3, ($t2)\n"
    result += "addi $t1, $t1, 1\n"
    result += "addi $t2, $t2, 1\n"
    result += "bne $t3, $0, " + strcat_second_start_label + "\n"

    return result


def convert_StrsubNode(instruction):
    global DATA, PARAMS
    
    result = ""
    
    if instruction.str in DATA:
        val = instruction.str
    else:
        val = PARAMS[instruction.str]
    
    # en t0 metemos la direccion del string
    result += "lw $t0, " + val + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.i in DATA:
        index = instruction.i        
    elif instruction.i in PARAMS:
        index = PARAMS[instruction.i]
    
    # en t1 metemos el entero del indice donde empieza la subcadena
    result += "lw $t1, " + index + "\n"
    result += "addi $t1, $t1, 4\n"
    result += "lw $t1, ($t1)\n"

    # ponemos en t0 la direccion del inicio de la subcadena
    result += "add $t0, $t0, $t1\n"

    if instruction.len in DATA:
        lenght = instruction.len
    elif instruction.i in PARAMS:
        lenght = PARAMS[instruction.len]
     
    # en t1 ponemos el entero q dice la cantidad de caracteres a copiar
    result += "lw $t1, " + lenght + "\n"
    result += "addi $t1, $t1, 4\n"
    result += "lw $t1, ($t1)\n"

    # en t1 dejamos la direccion del final de la subcadena
    result += "add $t1, $t0, $t1\n"

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]
        
    # en t2 va la direccion donde pondremos la subcadena resultante
    result += "lw $t2, " + dest + "\n"

    # ponemos la 'S' inicial
    result += "li $t3, 'S'\n"
    result += "sb $t3, ($t2)\n"
    result += "addi $t2, $t2, 4\n"


    strsub_loop_start_label = next_label()
    strsub_loop_end_label = next_label()

    result += strsub_loop_start_label + ":\n"
    result += "beq $t0, $t1, " + strsub_loop_end_label + "\n"
    # pasamos caracter a caracter de t0 a t2
    result += "lb $t3, ($t0)\n"
    result += "sb $t3, ($t2)\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $t2, $t2, 1\n"
    result += "j " + strsub_loop_start_label + "\n"
    result += strsub_loop_end_label + ":\n"
    # ponemos \0 al final de la cadena resultante
    result += "li $t3, 0\n"
    result += "sb $t3, ($t2)\n"

    return result
    

def convert_AllocateNode(instruction):
    result = ""

    global DATA, PARAMS, CIL_TYPES

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    do_realocate = next_label()
    allocate_end_label = next_label()

    # first check if there is already a value in local
    result += "lw $t1, " + dest + "\n"
    result += "beq $t1, 0, " + do_realocate + "\n"

    if instruction.type == "Int" or instruction.type == "Bool" or instruction.type == "Pointer":
        # put correct letter first
        if instruction.type == "Int":
            result += "li $t0, 'I'\n"
        elif instruction.type == "Bool":
            result +=   "li $t0, 'B'\n"
        else:
            result +=   "li $t0, 'P'\n"

        result += "sb $t0, ($t1)\n"
    
        # put zero value       
        result += "li $t0, 0\n"
        result += "sw $t0, 4($t1)\n"
        result += "j " + allocate_end_label + "\n"
    
    elif instruction.type == "String":
        # first check if there is already a string
        result += "li $t0, 0\n"
        result += "lb $t0, ($t1)\n"
        # if there is not a string then realocate
        result += "bne $t0, 'S', " + do_realocate + "\n"
        # if there is a string then change it to ""
        result += "li $t0, 0\n"
        result += "sw $t0, 4($t1)\n"
        result += "j " + allocate_end_label + "\n"
    
    elif instruction.type == "void":
        result += "li $t0, 0\n"
        result += "sw $t0, " + dest + "\n"
        result += "j " + allocate_end_label + "\n"

    else:
        # first check if there is already an object of this type
        result += "li $t0, 0\n"
        result += "lb $t0, ($t1)\n"
        # if there is not an object then realocate
        result += "bne $t0, 'O', " + do_realocate + "\n"
    
        # check that the same type is stored
        result += "li $t3, 0\n"
        result += "lw $t2, 4($t1)\n"
        for i in range(0, len(instruction.type)):
            result += "lb $t3, ($t2)\n"
            result += "bne $t3, '" + instruction.type[i] + "', " + do_realocate + "\n"
            result += "addi $t2, $t2, 1\n"
        
        result += "lb $t3, ($t2)\n"
        result += "bne $t3, 0, " + do_realocate + "\n"

        result += "j " + allocate_end_label + "\n"        

    result += do_realocate + ":\n"

    # los datos Int y Bool toman 8 bytes, 4 para la letra inicial I o B
    # y los restantes 4 para el valor
    if instruction.type == "Int" or instruction.type == "Bool" or instruction.type == "Pointer":
        result += "li $a0, 8\n"
        result += "li $v0, 9\n"
        result += "syscall\n"

        # ponemos la direccion en la variable local correspondiente
        result += "sw $v0, " + dest + "\n"

        # ponemos la letra correspondiente
        if instruction.type == "Int":
            result += "li $t0, 'I'\n"
        elif instruction.type == "Bool":
            result +=   "li $t0, 'B'\n"
        else:
            result +=   "li $t0, 'P'\n"

        result += "sb $t0, ($v0)\n"
        
        # inicializamos el valor a 0
        result += "li $t0, 0\n"
        result += "sw $t0, 4($v0)\n" 

    # los datos String se llevan 1028 bytes, 4 para la 'S' y los restantes
    # 1024 para el valor de la cadena
    elif instruction.type == "String":
        result += "li $a0, 1028\n"
        result += "li $v0, 9\n"
        result += "syscall\n"

        # ponemos la direccion en la variable local correspondiente
        result += "sw $v0, " + dest + "\n"

        # ponemos la letra correspondiente
        result += "li $t0, 'S'\n"
        result += "sb $t0, ($v0)\n"
        
        # inicializamos el valor a ""
        result += "li $t0, 0\n"
        result += "sw $t0, 4($v0)\n" 

    elif instruction.type == "void":

        # reaching here means that destiny local was already zero
        return result

    else:
        # los objetos no basicos comienzan con una 'O' y luego tienen
        # 4 con la direccion en memoria donde se encuentra el nombre del
        # tipo del objeto
        object_size = 12
        attrs = []
        for a in CIL_TYPES[instruction.type].attributes.values():
            if a.attribute_name == "self":
                continue
            if a.attribute_type.name == "String":
                object_size += 1028
                attrs.append('S')
            elif a.attribute_type.name == "Int":
                object_size += 8
                attrs.append('I')
            elif a.attribute_type.name == "Bool":
                object_size += 8
                attrs.append('B')
            else:
                # los atributos que no son de tipo basico consisten en punteros
                # a la direccion en memoria de los respectivos objetos
                object_size += 8
                attrs.append('P')
        
        result += "li $a0, " + str(object_size) + "\n"
        result += "li $v0, 9\n"
        result += "syscall\n"

        # ponemos la direccion en la variable local correspondiente
        result += "sw $v0, " + dest + "\n"

        # ponemos la letra correspondiente
        result += "li $t0, 'O'\n"
        result += "sb $t0, ($v0)\n"

        result += "addi $v0, $v0, 4\n"

        # ponemos la direccion al nombre del tipo
        result += "la $t0, type_" + instruction.type + "\n"
        result += "sw $t0, ($v0)\n"

        result += "addi $v0, $v0, 4\n"

        # ponemos el tamanyo correspondiente
        result += "li $t0, " + str(object_size) + "\n"
        result += "sw $t0, ($v0)\n"

        result += "addi $v0, $v0, 4\n"

        # ponemos las letras correspondientes a cada attributo
        for l in attrs:
            result += "li $t0, '" + l + "'\n"
            result += "sb $t0, ($v0)\n"
            if l == 'S':
                result += "addi $v0, $v0, 1028\n"
            else:
                result += "addi $v0, $v0, 8\n"

    result += allocate_end_label + ":\n"

    return result
    

def convert_ArgNode(instruction):
    result = ""

    global DATA, PARAMS
    
    if instruction.value in DATA:
        val = instruction.value
    else:
        val = PARAMS[instruction.value]
    
    result += "lw $t0, " + val + "\n"
    result += "sw $t0, ($sp)\n"
    result += "addi $sp, $sp, 4\n"

    return result


def convert_DispatchCallNode(instruction):
    result = ""

    global DATA, PARAMS, PARAMS_LOAD, CIL_TYPES

    if instruction.type_name in DATA:
        tp = instruction.type_name
    else:
        tp = PARAMS[instruction.type_name]

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    dispatch_after_call_label = next_label()

    # tenemos que buscar a q funcion llamar dependiendo del tipo de la instancia
    # que se obtiene en ejecucion
    for t in CIL_TYPES.values():

        if not (instruction.method in t.methods):
            continue

        result += "la $t0, type_" + t.type_name + "\n"
        
        result += "lw $t1, " + tp + "\n"
        result += "addi $t1, $t1, 4\n"

        # en t0 estara el tipo actual y en t1 el tipo del metodo a llamar

        dispatch_string_comparison_start_label = next_label()
        dispatch_string_first_ended = next_label()
        dispatch_string_false = next_label()
        dispatch_end_label = next_label()

        result += dispatch_string_comparison_start_label + ":\n"

        result += "li $t3, 0\n"
        result += "li $t4, 0\n"

        result += "lb $t3, ($t0)\n"
        result += "lb $t4, ($t1)\n"
        
        result += "beq $t3, 0, " + dispatch_string_first_ended + "\n"

        # si el segundo llega a su final y el primero no ha llegado
        # entonces no son iguales
        result += "beq $t4, 0, " + dispatch_string_false + "\n"

        result += "addi $t0, $t0, 1\n"
        result += "addi $t1, $t1, 1\n"

        result += "beq $t3, $t4, " + dispatch_string_comparison_start_label + "\n"

        # si los dos caracteres comparados no son iguales entonces
        # los strings no son iguales
        result += dispatch_string_false + ":\n"
        result += "li $t3, 0\n"
        result += "j " + dispatch_end_label + "\n"
        result += dispatch_string_first_ended + ":\n"

        # si el primero llega al final y el segundo no ha llegado
        # entonces los strings no son iguales
        result += "bne $t4, 0, " + dispatch_string_false + "\n"

        # aqui solamente se llega si los dos strings tuvieron los mismos
        # caracteres y llegaron al final a la misma vez
        result += "li $t3, 1\n"
        result += "j " + dispatch_end_label + "\n"

        # en este punto si en t3 se encuentra la igualdad o no del tipo actual
        # y del tipo de la instancia

        result += dispatch_end_label + ":\n"

        dispatch_continue_label = next_label()

        result += "bne $t3, 1, " + dispatch_continue_label + "\n"

        result += "jal " + t.methods[instruction.method] + "_" + instruction.method + "\n"

        result += PARAMS_AND_LOCALS_RELOAD

        result += "sw $v0, " + dest + "\n"
        result += "j " + dispatch_after_call_label + "\n"
        result += dispatch_continue_label + ":\n"

    result += dispatch_after_call_label + ":\n"

    return result

def convert_SetAttributeNode(instruction):
    result = ""

    global CIL_TYPES, DATA, PARAMS

    offset = 12

    for a in CIL_TYPES[instruction.type_name].attributes.values():
        if a.attribute_name == "self":
            continue
        if a.attribute_name == instruction.attr:
            attr_type = a.attribute_type
            break
        if a.attribute_type.name == "String":
            offset += 1028
        elif a.attribute_type.name == "Int":
            offset += 8
        elif a.attribute_type.name == "Bool":
            offset += 8
        else:
            offset += 8

    if instruction.instance in DATA:
        ins = instruction.instance
    else:
        ins = PARAMS[instruction.instance]
    
    # en t0 metemos la direccion del valor a modificar
    result += "lw $t0, " + ins + "\n"
    result += "addi $t0, $t0, " + str(offset + 4) + "\n"

    if instruction.value in DATA:
        val = instruction.value
    else:
        val = PARAMS[instruction.value]

    # en t1 metemos la direccion del valor nuevo
    result += "lw $t1, " + val + "\n"
    result += "addi $t1, $t1, 4\n"

    # copiamos el valor de la direccion t0 a t1
    sattr_string_copy_start_label = next_label()

    if attr_type.name == "String":
        result += sattr_string_copy_start_label + ":\n"
        result += "lb $t3, ($t1)\n"
        result += "sb $t3, ($t0)\n"
        result += "addi $t0, $t0, 1\n"
        result += "addi $t1, $t1, 1\n"
        result += "bne $t3, 0, " + sattr_string_copy_start_label + "\n"
    elif attr_type.name == "Int" or attr_type.name == "Bool":
        result += "lw $t3, ($t1)\n"
        result += "sw $t3, ($t0)\n"
    else:
        result += "addi $t3, $t1, -4\n"
        result += "sw $t3, ($t0)\n"

    return result


def convert_GetAttributeNode(instruction):
    result = ""

    global CIL_TYPES, DATA, PARAMS

    offset = 12

    for a in CIL_TYPES[instruction.type_name].attributes.values():
        if a.attribute_name == "self":
            continue
        if a.attribute_name == instruction.attr:
            attr_type = a.attribute_type
            break
        if a.attribute_type.name == "String":
            offset += 1028
        elif a.attribute_type.name == "Int":
            offset += 8
        elif a.attribute_type.name == "Bool":
            offset += 8
        else:
            offset += 8

    if instruction.value in DATA:
        val = instruction.value
    else:
        val = PARAMS[instruction.value]
    
    # en t0 metemos la direccion del valor a devolver
    result += "lw $t0, " + val + "\n"
    result += "addi $t0, $t0, " + str(offset + 4) + "\n"
    
    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    result += "lw $t1, " + dest + "\n"
    result += "addi $t1, $t1, 4\n"

    # copiamos el valor de la direccion t0 a t1
    gattr_string_copy_start_label = next_label()

    if attr_type.name == "String":
        result += gattr_string_copy_start_label + ":\n"
        result += "lb $t3, ($t0)\n"
        result += "sb $t3, ($t1)\n"
        result += "addi $t0, $t0, 1\n"
        result += "addi $t1, $t1, 1\n"
        result += "bne $t3, $0, " + gattr_string_copy_start_label + "\n"
    elif attr_type.name == "Int" or attr_type.name == "Bool":
        result += "lw $t3, ($t0)\n"
        result += "sw $t3, ($t1)\n"
    else:
        result += "lw $t3, ($t0)\n"
        result += "sw $t3, " + dest + "\n"

    return result


def convert_ENode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in DATA:
        left = instruction.left
    elif instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    
    # poner en t0 la direccion del primer dato
    result += "lw $t0, " + left + "\n"

    if instruction.right in DATA:
        right = instruction.right
    elif instruction.right in PARAMS:
        right = PARAMS[instruction.right]
    else:
        right = instruction.right

   # poner en t1 la direccion del segundo dato
    result += "lw $t1, " + right + "\n"

    if instruction.result in DATA:
        dest = instruction.result
    elif instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    
    # poner en t2 la direccion donde se pondra 0 o 1
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    result += "li $t4, 0\n"
    # metemos en t3 la letra del tipo de dato de t0
    result += "li $t3, 0\n"
    result += "lb $t3, ($t0)\n"

    equal_not_object_label = next_label()
    equal_end_label = next_label()
    equal_not_string_label = next_label()
    equal_string_comparison_start_label = next_label()
    equal_string_first_ended = next_label()
    equal_string_false = next_label()

    result += "bne $t3, 'O', " + equal_not_object_label + "\n"
    # aqui checkeamos q si son objetos tengan la misma direccion
    result += "seq $t0, $t0, $t1\n"
    result += "j " + equal_end_label + "\n"
    result += equal_not_object_label + ":\n"
    result += "bne $t3, 'S', " + equal_not_string_label + "\n"
    # aqui checkeamos q si son strings sean iguales
    result += "addi $t0, $t0, 3\n"
    result += "addi $t1, $t1, 3\n"
    result += equal_string_comparison_start_label + ":\n"
    result += "addi $t0, $t0, 1\n"
    result += "addi $t1, $t1, 1\n"
    result += "lb $t3, ($t0)\n"
    result += "lb $t4, ($t1)\n"
    result += "beq $t3, $0, " + equal_string_first_ended + "\n"
    # si el segundo llega a su final y el primero no ha llegado
    # entonces no son iguales
    result += "beq $t4, $0, " + equal_string_false + "\n"
    result += "beq $t3, $t4, " + equal_string_comparison_start_label + "\n"
    # si los dos caracteres comparados no son iguales entonces
    # los strings no son iguales
    result += equal_string_false + ":\n"
    result += "li $t0, 0\n"
    result += "j " + equal_end_label + "\n"
    result += equal_string_first_ended + ":\n"
    # si el primero llega al final y el segundo no ha llegado
    # entonces los strings no son iguales
    result += "bne $t4, $0, " + equal_string_false + "\n"
    # aqui solamente se llega si los dos strings tuvieron los mismos
    # caracteres y llegaron al final a la misma vez
    result += "li $t0, 1\n"
    result += "j " + equal_end_label + "\n"
    result += equal_not_string_label + ":\n"
    # aqui se llega si los datos son Int o Bool,
    # entonces seria comparar los valores almacenados
    result += "addi $t0, $t0, 4\n"
    result += "addi $t1, $t1, 4\n"
    result += "lw $t0, ($t0)\n"
    result += "lw $t1, ($t1)\n"
    result += "seq $t0, $t0, $t1\n"
    result += equal_end_label + ":\n"
    # poner el resultado en la direccion correspondiente q estaba en t2
    result += "sw $t0, ($t2)\n"

    return result 


def convert_LNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in DATA:
        left = instruction.left
    elif instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    
    result += "lw $t0, " + left + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.right in DATA:
        right = instruction.right
    elif instruction.right in PARAMS:
        right = PARAMS[instruction.right]
   
    result += "lw $t1, " + right + "\n"
    result += "addi $t1, $t1, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    elif instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    result += "lw $t0, ($t0)\n"
    result += "lw $t1, ($t1)\n"
    result += "slt $t0, $t0, $t1\n"
    result += "sw $t0, ($t2)\n"

    return result 


def convert_LENode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in DATA:
        left = instruction.left
    elif instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    
    result += "lw $t0, " + left + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.right in DATA:
        right = instruction.right
    elif instruction.right in PARAMS:
        right = PARAMS[instruction.right]
   
    result += "lw $t1, " + right + "\n"
    result += "addi $t1, $t1, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    elif instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    result += "lw $t0, ($t0)\n"
    result += "lw $t1, ($t1)\n"
    result += "sle $t0, $t0, $t1\n"
    result += "sw $t0, ($t2)\n"

    return result 


def convert_DivNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in DATA:
        left = instruction.left
    elif instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    
    result += "lw $t0, " + left + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.right in DATA:
        right = instruction.right
    elif instruction.right in PARAMS:
        right = PARAMS[instruction.right]
   
    result += "lw $t1, " + right + "\n"
    result += "addi $t1, $t1, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    elif instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    result += "lw $t0, ($t0)\n"
    result += "lw $t1, ($t1)\n"
    result += "div $t0, $t0, $t1\n"
    result += "sw $t0, ($t2)\n"

    return result 


def convert_MulNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in DATA:
        left = instruction.left
    elif instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    
    result += "lw $t0, " + left + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.right in DATA:
        right = instruction.right
    elif instruction.right in PARAMS:
        right = PARAMS[instruction.right]
   
    result += "lw $t1, " + right + "\n"
    result += "addi $t1, $t1, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    elif instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    result += "lw $t0, ($t0)\n"
    result += "lw $t1, ($t1)\n"
    result += "mult $t0, $t1\n"
    result += "mflo $t0\n"
    result += "sw $t0, ($t2)\n"

    return result


def convert_SubNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in DATA:
        left = instruction.left
    elif instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    
    result += "lw $t0, " + left + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.right in DATA:
        right = instruction.right
    elif instruction.right in PARAMS:
        right = PARAMS[instruction.right]
   
    result += "lw $t1, " + right + "\n"
    result += "addi $t1, $t1, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    elif instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    result += "lw $t0, ($t0)\n"
    result += "lw $t1, ($t1)\n"
    result += "sub $t0, $t0, $t1\n"
    result += "sw $t0, ($t2)\n"

    return result


def convert_AddNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.left in DATA:
        left = instruction.left
    elif instruction.left in PARAMS:
        left = PARAMS[instruction.left]
    
    result += "lw $t0, " + left + "\n"
    result += "addi $t0, $t0, 4\n"

    if instruction.right in DATA:
        right = instruction.right
    elif instruction.right in PARAMS:
        right = PARAMS[instruction.right]
   
    result += "lw $t1, " + right + "\n"
    result += "addi $t1, $t1, 4\n"

    if instruction.result in DATA:
        dest = instruction.result
    elif instruction.result in PARAMS:
        dest = PARAMS[instruction.result]
    
    result += "lw $t2, " + dest + "\n"
    result += "addi $t2, $t2, 4\n"

    result += "lw $t0, ($t0)\n"
    result += "lw $t1, ($t1)\n"
    result += "add $t0, $t0, $t1\n"
    result += "sw $t0, ($t2)\n"

    return result


def convert_VDNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in DATA:
        val = instruction.value
    elif instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    
    result += "lw $t0, " + val + "\n"

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    result += "lw $t1, " + dest + "\n"
    result += "addi $t1, $t1, 4\n"

    result += "seq $t2, $t0, 0\n"
    result += "sw $t2, ($t1)\n"

    return result


def convert_CmpNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in DATA:
        val = instruction.value
    elif instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    
    result += "lw $t0, " + val + "\n"
    result += "addi $t0, $t0, 4\n"
    result += "lw $t0, ($t0)\n"

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    result += "lw $t1, " + dest + "\n"
    result += "addi $t1, $t1, 4\n"

    result += "li $t2, -1\n"
    result += "mult $t0, $t2\n"
    result += "mflo $t0\n"
    result += "sw $t0, ($t1)\n"

    return result

def convert_NtNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in DATA:
        val = instruction.value
    elif instruction.value in PARAMS:
        val = PARAMS[instruction.value]
    
    result += "lw $t0, " + val + "\n"
    result += "addi $t0, $t0, 4\n"
    result += "lw $t0, ($t0)\n"

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    result += "lw $t1, " + dest + "\n"
    result += "addi $t1, $t1, 4\n"

    result += "seq $t0, $t0, 0\n"
    result += "sw $t0, ($t1)\n"

    return result


def convert_MovNode(instruction):
    result = ""

    if type(instruction.value) == type(5):
        result += "li $t0, " + str(instruction.value) + "\n"
        result += "lw $t1, " + instruction.result + "\n"
        result += "sw $t0, 4($t1)\n"
    else:
        if instruction.value in DATA:
            val = instruction.value
        elif instruction.value in PARAMS:
            val = PARAMS[instruction.value]
        
        if instruction.result in DATA:
            res = instruction.result
        elif instruction.result in PARAMS:
            res = PARAMS[instruction.result]

        result += "lw $t0, " + val + "\n"
        result += "sw $t0, " + res + "\n"

    return result


def convert_SetStringNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.result in DATA:
        dest = instruction.result
    else:
        dest = PARAMS[instruction.result]

    result += "lw $t0, " + dest + "\n"
    result += "addi $t0, $t0, 4\n"

    for c in instruction.str:
        result += "li $t1, '" + c + "'\n"
        result += "sb $t1, ($t0)\n"
        result += "addi $t0, $t0, 1\n"

    result += "li $t1, 0\n"
    result += "sb $t1, ($t0)\n"

    return result



def convert_ToStrNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.value in DATA:
        val = instruction.value
    else:
        val = PARAMS[instruction.value]
    
    # aqui esta el valor entero a convertir
    result += "lw $t0, " + val + "\n"
    result += "addi $t0, $t0, 4\n"
    result += "lw $t0, ($t0)\n"


    if instruction.result in DATA:
        res = instruction.result
    else:
        res = PARAMS[str(instruction.result)]

    # aqui esta la direccion del string de salida 
    result += "lw $t1, " + res + "\n"
    result += "addi $t1, $t1, 4\n"

    tostr_loop_start_label = next_label()

    result += "li $t2, '0'\n"
    result += tostr_loop_start_label + ":\n"
    result += "div $t0, $t0, 10\n"
    result += "mfhi $t3\n"
    # sumamos el ascii del 0 con el valor de los digitos
    result += "add $t3, $t3, $t2\n"
    result += "sb $t3, ($t1)\n"
    result += "addi $t1, $t1, 1\n"
    result += "bne $t0, 0, " + tostr_loop_start_label + "\n"
    result += "li $t3, 0\n"
    result += "sb $t3, ($t1)\n"
    result += "addi $t1, $t1, -1\n"

    # en este punto se convirtio el entero
    # en string en la direccion resultado 

    if instruction.result in DATA:
        res = instruction.result
    else:
        res = PARAMS[str(instruction.result)]

    # en t2 metemos el principio de la direccion del string 
    result += "lw $t2, " + res + "\n"
    result += "addi $t2, $t2, 4\n"

    # como en t1 esta la direccion del ulrimo caracter del string
    # lo q hacemos es hacer swap con t1 y t2 hacer t1-- y t2++
    # hasta que se encuentren

    tostr_reverse_string_start_label = next_label()
    tostr_end_label = next_label()

    result += tostr_reverse_string_start_label + ":\n"
    result += "ble $t1, $t2, " + tostr_end_label + "\n"
    result += "lb $t0, ($t2)\n"
    result += "lb $t3, ($t1)\n"
    result += "sb $t3, ($t2)\n"
    result += "sb $t0, ($t1)\n"
    result += "addi $t1, $t1, -1\n"
    result += "addi $t2, $t2, 1\n"
    result += "j " + tostr_reverse_string_start_label + "\n"
    result += tostr_end_label + ":\n"

    return result

def convert_AbortNode(instruction):
    result = "li $v0, 10\n"
    result += "syscall\n"

    return result


def convert_IfGotoNode(instruction):
    result = ""

    global DATA, PARAMS

    if instruction.predicate in DATA:
        pred = instruction.predicate
    else:
        pred = PARAMS[instruction.predicate]

    result += "lw $t0, " + pred + "\n"
    result += "lw $t0, 4($t0)\n"
    result += "beq $t0, 1, " + instruction.label + "\n"

    return result


def convert_GotoNode(instruction):
    return "j " + instruction.label + "\n"


def convert_LabelNode(instruction):
    return instruction.label_name + ":\n"