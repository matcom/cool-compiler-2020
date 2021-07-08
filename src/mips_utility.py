enter = "\n"

def build_label(label,visitor):
    fname = '{}_{}'.format(label,visitor.internal_count)
    visitor.internal_count += 1
    return fname



def ReservaMemoria(size):
    # tam = size*4
    text =("# reserva memoria" + enter
          + "li $a0, " + str(size) + enter
          + "li $v0, 9" + enter
          + "syscall" + enter)
    return text # en v0 guarda laposicion d memoria inicial

def PrintStr(varname):
    text = ("" + "la $t1, " + varname + enter
        + "move $a0, $t1" + enter
        + "li $v0, 4" + enter
        + "syscall" + enter)
    return text


def AccederALabel(className ,fpos):
    calcpos = (fpos * 4) + 8
    text = ("" + "la $t1, " + className + str(calcpos) + enter)
    return text

def SalvaRegistros():
    text = ("# Salva registros" + enter
        + "addi $sp, $sp, -76" + enter
        + "sw $t1, 0($sp)" + enter
        + "sw $t2, 4($sp)" + enter
        + "sw $t3, 8($sp)" + enter
        + "sw $t4, 12($sp)" + enter
        + "sw $t5, 16($sp)" + enter
        + "sw $t6, 20($sp)" + enter
        + "sw $t7, 24($sp)" + enter
        + "sw $a0, 28($sp)" + enter
        + "sw $a1, 32($sp)" + enter
        + "sw $a2, 36($sp)" + enter
        + "sw $a3, 40($sp)" + enter
        + "sw $ra, 44($sp)" + enter
        + "sw $s1, 48($sp)" + enter
        + "sw $s2, 52($sp)" + enter
        + "sw $s3, 56($sp)" + enter
        + "sw $s4, 60($sp)" + enter
        + "sw $s5, 64($sp)" + enter
        + "sw $s6, 68($sp)" + enter
        + "sw $s7, 72($sp)" + enter
        
    )
    return text

def CargaRegistros():
    text = ("# Carga registros" + enter
        + "lw $t1, 0($sp)" + enter
        + "lw $t2, 4($sp)" + enter
        + "lw $t3, 8($sp)" + enter
        + "lw $t4, 12($sp)" + enter
        + "lw $t5, 16($sp)" + enter
        + "lw $t6, 20($sp)" + enter
        + "lw $t7, 24($sp)" + enter
        + "lw $a0, 28($sp)" + enter
        + "lw $a1, 32($sp)" + enter
        + "lw $a2, 36($sp)" + enter
        + "lw $a3, 40($sp)" + enter
        + "lw $ra, 44($sp)" + enter
        + "lw $s1, 48($sp)" + enter
        + "lw $s2, 52($sp)" + enter
        + "lw $s3, 56($sp)" + enter
        + "lw $s4, 60($sp)" + enter
        + "lw $s5, 64($sp)" + enter
        + "lw $s6, 68($sp)" + enter
        + "lw $s7, 72($sp)" + enter
        + "addi $sp, $sp, 76" + enter
    )
    return text

# def CalcPosicPila(distacia):
#     return distacia*4


def Opera(op,node):
    text = ""
    if(isinstance(node.left,int)):
        text += "li $t2, " +str(node.left) + enter
    else:
         text += "lw $t2, " + "-" + str(4*(node.left.vmholder))+"($a3)" + enter
    if(isinstance(node.right,int)):
        text += "li $t3, " +str(node.right) + enter
    else:
         text += "lw $t3, " + "-" + str(4*(node.right.vmholder))+"($a3)" + enter
    text += (op + " $t1, $t2, $t3" + enter
        + "sw $t1, " + "-" + str(4*(node.dest.vmholder))+"($a3)" + enter)



    # text = ("lw $t1, " + str(dest)+"($a3)" + enter
    # text = ( "lw $t2, " + "-" + str(left)+"($a3)" + enter
    #         +"lw $t3, " + "-" + str(right)+"($a3)" + enter
    #         + op +  " $t1, $t2, $t3" + enter
    #         + "sw $t1, " + "-" + str(dest)+"($a3)" + enter)
    return text

def OperaSpecial(op,node):
    # text = ("lw $t1, " + str(dest)+"($a3)" + enter
    text = ""
    if(isinstance(node.left,int)):
            text += "li $t2, " +str(node.left) + enter
    else:
         text += "lw $t2, " + "-" + str(4*(node.left.vmholder))+"($a3)" + enter
    if(isinstance(node.right,int)):
        text += "li $t3, " +str(node.right) + enter
    else:
         text += "lw $t3, " + "-" + str(4*(node.right.vmholder))+"($a3)" + enter

    text += ( op +  "  $t2, $t3" + enter
             + "mflo $t1, " + enter
             + "sw $t1, " + "-" + str(4* node.dest.vmholder)+"($a3)" + enter)

    # text =  ( "lw $t2, " + "-" + str(left)+"($a3)" + enter
    #         + "lw $t3, " + "-" + str(right)+"($a3)" + enter
    #         + op +  "  $t2, $t3" + enter
    #         + "mfhi $t1, " + enter
    #         + "sw $t1, " + "-" + str(dest)+"($a3)" + enter)
    return text

def DeLaPila(pos):
    return "-" + str(4*pos)+"($a3)" + enter

def Push(reg):
    text = ("# push" + enter 
         + "addi $sp, $sp, -4" + enter
         + "sw " +reg+", 0($sp)" + enter)
    return text

def Pop(reg):
    text = ("# pop" + enter 
         + "sw " +reg+", 0($sp)" + enter
         + "addi $sp, $sp, 4" + enter )
    return text

def ReservaPila(size):
    tam = size * 4
    text = "add $sp, $sp, -" + str(tam) + enter
    return text


def Length(name,visitor):
    while1 = build_label("while",visitor)
    fin = build_label("fin",visitor)
    text = (" # Length" + enter
            + "li $s0, 0" + enter
            + while1 + ":" + enter
           + "lw $t0, -" + str(4*name)+ "($a3)" + enter
           + "add $t0, $t0,$s0" + enter
           + "lb $t1, 0($t0)" + enter
           + "beq $t1, $zero, " +fin  + enter
           + "addi $s0,$s0,1" + enter
           + "j " + while1 + enter 
           + fin +":" + enter)
    return text

def Substring(i,j,pos,visitor):
    # while1 = build_label("while",visitor)
    # fin = build_label("fin",visitor)
    # text = (" # Substring" + enter
    #     + "lw $s3, " +str(pos)+"($a3)" + enter
    #     + "addi $s3, $s3, " + str(i) + enter
    #     + "li $t2, " + str(n) + enter
    #     + "li $a0,  10" + enter
    #     + "li $v0, 9" + enter
    #     + "syscall" + enter
    #     + "li $s0, 0" + enter
    #     + while1 +":" + enter
    #     + "move $t4, $v0" + enter
    #     + "move $t0, $s3"  + enter
    #     + "add $t0, $t0,$s0" + enter
    #     + "add $t4, $t4, $s0" + enter
    #     + "lb $t1, 0($t0)" + enter
    #     + "sb $t1, 0($t4)" + enter
    #     + "addi $s0,$s0,1" + enter
    #     + "beq $s0, $t2, "+ fin + enter
    #     + "j "+ while1  + enter
    #     + fin + ":" + enter
    #     + "addi $s0,$s0,1" + enter
    #     + "add $t4, $t4, $s0" + enter
    #     + "li $t5, 0" + enter
    #     + "lb $t5, 0($t4)" + enter)
    # return text

    while1 = build_label("while",visitor)
    fin = build_label("fin",visitor)
    text = (" # Substring" + enter
        + "lw $s3, -" +str(pos)+"($a3)" + enter
        + "lw $t1, -" +str(i)+"($a3)" + enter
        + "lw $t2, -" +str(j)+"($a3)" + enter                
        + "add $s3, $s3, $t1" + enter
        # + "sub $t2, $t2, $t1" + enter
        # + "move $t2, $t3" + enter
        # + "addi $t2,  $t2, 1" + enter

        + "addi $a0,  $t2, 1" + enter
        + "li $v0, 9" + enter
        + "syscall" + enter
        + "li $s0, 0" + enter
        + while1 +":" + enter
        + "move $t4, $v0" + enter
        + "move $t0, $s3"  + enter
        + "add $t0, $t0,$s0" + enter
        + "add $t4, $t4, $s0" + enter
        + "lb $t1, 0($t0)" + enter
        + "sb $t1, 0($t4)" + enter
        + "addi $s0,$s0,1" + enter
        + "beq $s0, $t2, "+ fin + enter
        + "j "+ while1  + enter
        + fin + ":" + enter
        + "addi $s0,$s0,1" + enter
        + "addi $t4, $t4, 1" + enter
        + "li $t5, 0" + enter
        + "lb $t5, 0($t4)" + enter)
    return text

def Concat(pos1, pos2,visitor):
    whilel1 = build_label("whilel1",visitor)
    whilel2 = build_label("whilel2",visitor)
    fin = build_label("fin",visitor)
    pawhilel1 = build_label("pawhilel1",visitor)
    pawhilel2 = build_label("pawhilel2",visitor)
    whilecopy1 = build_label("whilecopy1",visitor)
    whilecopy2 = build_label("whilecopy2",visitor)
    pawhilecopy2 = build_label("pawhilecopy2",visitor)
    finl = build_label("finl",visitor)
    text = ( "# Concat" + enter 
        + "lw $t1, -" + str(pos1)+"($a3)" + enter 
        + "li $s0, 0 " + enter
        + whilel1 + ": " + enter
    
        + "lw $t0, -" + str(pos1)+"($a3)"  + enter
        + "add $t0, $t0,$s0 "  + enter
        + "lb $t1, 0($t0)  " + enter
        + "beq $t1, $zero, " + pawhilel2 + enter
        + "addi $s0,$s0,1  " + enter
        + "j " + whilel1 + enter
        + pawhilel2 + ":" + enter
    
        + "move $t7,$s0  " + enter
        + "li $s0, 0 " + enter
        + whilel2 +": " + enter
        + "lw $t0, -" + str(pos2)+"($a3)" + enter
        + "add $t0, $t0,$s0 "  + enter
        + "lb $t1, 0($t0) " + enter
        + "beq $t1, $zero, "+ finl + enter
        + "addi $s0, $s0,1    " + enter
        + "j " + whilel2 + enter
        + finl +": " + enter
    
        + "add $t7, $t7,$s0 " + enter
        + "addi $t7, $t7, 1 " + enter
        + "move $a0,$t7 " + enter
        + "li $v0, 9 " + enter
        + "syscall " + enter
        + "li $s0, 0 " + enter
        + "li $s1, 0 " + enter
        + "move $t5, $v0 " + enter
        + "# puntero en t5" + enter
        + whilecopy1 + ": " + enter
    
        + "# puntero en  a" + enter
        + "lw $t0, -" + str(pos1)+"($a3)" + enter
        + "add $t0, $t0,$s0 " + enter
        + "add $t4, $t5, $s0 " + enter
        + "lb $t1, 0($t0)" + enter
        + "beq $t1, $s1, " + pawhilecopy2  + enter
        + "addi $s0,$s0,1 " + enter
        + "# move $a0,$s0 " + enter
        + "# li $v0, 1 " + enter
        + "# syscall " + enter
        + "sb $t1, 0($t4)"  + enter
        + "j " + whilecopy1 + enter
        + pawhilecopy2 + ": " + enter
    
        + "# move $a0,$s0 " + enter
        + "# li $v0, 1 " + enter
        + "# syscall " + enter
        + "move $t7, $s0"  + enter
        + "li $s0, 0 " + enter
        + whilecopy2 +":" + enter
    
        + "# puntero en   a2" + enter
        + "lw $t0, -" + str(pos2)+"($a3)" + enter
        + "add $t0, $t0,$s0 " + enter
        + "add $t4, $t5, $t7 " + enter
        + "lb $t1, 0($t0) " + enter
        + "sb $t1, 0($t4) " + enter
        + "beq $t1, $zero, "+ fin + enter
        + "addi $s0,$s0,1 " + enter
        + "addi $t7,$t7,1 " + enter
        + "j " + whilecopy2 + enter
        + fin +": " + enter
    
        + "add $t4, $t5, $t7 " + enter
        + "li $t1, 0 " + enter
        + "lb $t1, 0($t4)"  + enter
        + "# li $v0, 4" + enter
        + "# move $a0, $t5" + enter
        + "# syscall" + enter)
    return text
            

def leerString(visitor):
    while1 = build_label("while1",visitor)
    while2 = build_label("while2",visitor)
    fin = build_label("fin",visitor)
    fin1 = build_label("fin1",visitor)

    text = (" # leer string" + enter
        + "li $s0,0 " + enter
        + "li $s3, 10 " + enter
        + "# coger tamanho y almacenar en buffer " + enter
        + while1 + ": " + enter
        
        + "la $t0, buffer " + enter 
        + "add $t0, $t0, $s0   " + enter
        + "li $v0, 12 " + enter
        + "syscall " + enter
        + "addi $s0,$s0,1 " + enter  
        + "beq $v0, $s3, " + fin  + enter  
        
        + "# beq $v0, $zero, error " + enter  
        + "# error " + enter
        + "sb $v0, 0($t0) " + enter
        + "j " + while1 + enter
        
        + fin + ": " + enter
        
        + "li $v0, 0 " + enter
        + "sb $v0, 0($t0) " + enter
        + "# reservar espacio " + enter 
        + "move $a0, $s0  " + enter
        + "li $v0, 9 " + enter
        + "syscall " + enter
        + "# asignar espacio a t5 " + enter
        + "move $t5, $v0 " + enter
        + "li $s0,0 " + enter
        + "li $s1,0 " + enter
        + "li $s2,0 " + enter
        + "# copiar de buffer pa t5 " + enter
        + while2 + ": " + enter
        
        + "la $t0, buffer " + enter 
        + "move $t1, $t5 " + enter
        + "add $t0, $t0, $s0 " + enter  
        + "add $t1, $t1, $s1 " + enter  
        + "lb $t2, 0($t0) " + enter
        + "sb $t2, 0($t1) " + enter
        + "beq $t2, $s2, " + fin1 + enter  
        
        + "addi $s0,$s0,1 " + enter  
        + "addi $s1,$s1,1 " + enter  
        
        + "j " + while2 + enter
        
        + fin1 + ": " + enter )
    return text


#  q usaste ply
#  visitor y q hacen, q erores
#  a;adir cosas a cil y q cosas usate 
#  dond se hizo case, representacion d tipos rn memoria, vt , boximh unboxing
# trabajo con la pila 