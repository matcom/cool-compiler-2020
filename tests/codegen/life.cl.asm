.data
st0: .asciiz "Object"
st1: .asciiz "IO"
st2: .asciiz "String"
st3: .asciiz "Bool"
st4: .asciiz "Board"
st5: .asciiz ""
st6: .asciiz "CellularAutomaton"
st7: .asciiz "\n"
st8: .asciiz "\n"
st9: .asciiz "\n"
st10: .asciiz " "
st11: .asciiz " "
st12: .asciiz " "
st13: .asciiz " "
st14: .asciiz " "
st15: .asciiz " "
st16: .asciiz " "
st17: .asciiz " "
st18: .asciiz " "
st19: .asciiz " "
st20: .asciiz " "
st21: .asciiz " "
st22: .asciiz " "
st23: .asciiz " "
st24: .asciiz "X"
st25: .asciiz "X"
st26: .asciiz "X"
st27: .asciiz "X"
st28: .asciiz "X"
st29: .asciiz "X"
st30: .asciiz "X"
st31: .asciiz "X"
st32: .asciiz "X"
st33: .asciiz "X"
st34: .asciiz "X"
st35: .asciiz "-"
st36: .asciiz "-"
st37: .asciiz ""
st38: .asciiz "\nPlease chose a number:\n"
st39: .asciiz "\t1: A cross\n"
st40: .asciiz "\t2: A slash from the upper left to lower right\n"
st41: .asciiz "\t3: A slash from the upper right to lower left\n"
st42: .asciiz "\t4: An X\n"
st43: .asciiz "\t5: A greater than sign \n"
st44: .asciiz "\t6: A less than sign\n"
st45: .asciiz "\t7: Two greater than signs\n"
st46: .asciiz "\t8: Two less than signs\n"
st47: .asciiz "\t9: A 'V'\n"
st48: .asciiz "\t10: An inverse 'V'\n"
st49: .asciiz "\t11: Numbers 9 and 10 combined\n"
st50: .asciiz "\t12: A full grid\n"
st51: .asciiz "\t13: A 'T'\n"
st52: .asciiz "\t14: A plus '+'\n"
st53: .asciiz "\t15: A 'W'\n"
st54: .asciiz "\t16: An 'M'\n"
st55: .asciiz "\t17: An 'E'\n"
st56: .asciiz "\t18: A '3'\n"
st57: .asciiz "\t19: An 'O'\n"
st58: .asciiz "\t20: An '8'\n"
st59: .asciiz "\t21: An 'S'\n"
st60: .asciiz "Your choice => "
st61: .asciiz "\n"
st62: .asciiz " XX  XXXX XXXX  XX  "
st63: .asciiz "    X   X   X   X   X    "
st64: .asciiz "X     X     X     X     X"
st65: .asciiz "X   X X X   X   X X X   X"
st66: .asciiz "X     X     X   X   X    "
st67: .asciiz "    X   X   X     X     X"
st68: .asciiz "X  X  X  XX  X      "
st69: .asciiz " X  XX  X  X  X     "
st70: .asciiz "X   X X X   X  "
st71: .asciiz "  X   X X X   X"
st72: .asciiz "X X X X X X X X"
st73: .asciiz "XXXXXXXXXXXXXXXXXXXXXXXXX"
st74: .asciiz "XXXXX  X    X    X    X  "
st75: .asciiz "  X    X  XXXXX  X    X  "
st76: .asciiz "X     X X X X   X X  "
st77: .asciiz "  X X   X X X X     X"
st78: .asciiz "XXXXX   X   XXXXX   X   XXXX"
st79: .asciiz "XXX    X   X  X    X   XXXX "
st80: .asciiz " XX X  XX  X XX "
st81: .asciiz " XX X  XX  X XX X  XX  X XX "
st82: .asciiz " XXXX   X    XX    X   XXXX "
st83: .asciiz "                         "
st84: .asciiz ""
st85: .asciiz "Would you like to continue with the next generation? \n"
st86: .asciiz "Please use lowercase y or n for your answer [y]: "
st87: .asciiz "\n"
st88: .asciiz "n"
st89: .asciiz ""
st90: .asciiz "\n\n"
st91: .asciiz "Would you like to choose a background pattern? \n"
st92: .asciiz "Please use lowercase y or n for your answer [n]: "
st93: .asciiz "y"
st94: .asciiz "Main"
st95: .asciiz ""
st96: .asciiz "Welcome to the Game of Life.\n"
st97: .asciiz "There are many initial states to choose from. \n"
Objectclase: .word 0,f0,f3,f2,f4
IOclase: .word Objectclase,f5,f6,f2,f4,f7,f8,f9,f10
Stringclase: .word Objectclase,f11,f12,f2,f4,f13,f14,f15
Boolclase: .word Objectclase,f16,f17,f2,f4
Boardclase: .word IOclase,f18,f19,f2,f4,f7,f8,f9,f10,f20,f21
CellularAutomatonclase: .word Boardclase,f22,f23,f2,f4,f7,f8,f9,f10,f20,f21,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41
Mainclase: .word CellularAutomatonclase,f42,f43,f2,f4,f7,f8,f9,f10,f20,f21,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f44
.text
.globl main
main:
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal Main.Special
lw $ra, 0($sp)
addi $sp ,$sp, 4
jr $ra
li $v0, 10
syscall
     #$a0 debe ser el string
     .IO.out_string:
     li $v0, 4
     syscall
     jr $ra

     #$a0 debe ser el string
     .IO.out_int:
     li $v0, 1
     syscall
     jr $ra

     .IO.in_int:
     li $v0, 5
     syscall
     jr $ra

     .IO.in_string:
     li $v0, 9
     move $s0, $a0
     li $a0, 1024
     syscall
     move $t1, $v0
     move $a0, $v0
     li $a1, 1024
     li $v0, 8
     syscall
     move $v0, $t1
     #Buscando y arreglando posible salto de linea
     move $t0, $v0
     move $t1, $zero
     li $t2, 10
     Iniciochequeofinlinea:
     lb $t1, 0($t0)
     beq $t1, $t2, Cambiafinlinea
     addi $t0, $t0, 1
     bne $t1, $zero, Iniciochequeofinlinea
     jr $ra
     Cambiafinlinea:
     sb $zero, 0($t0)
     jr $ra

     #Los numeros como argumentos $a0 y $a1, y $a2 como donde guardar el resultado
     .Int.suma:
     lw $t1, 0($a0)
     lw $t2, 0($a1)
     add $v0, $t1, $t2
     sw $v0, 0($a2)
     jr $ra

     .Int.resta:
     lw $t1, 0($a0)
     lw $t2, 0($a1)
     sub $v0, $t1, $t2
     sw $v0, 0($a2)
     jr $ra

     .Int.multiplicacion:
     lw $t1, 0($a0)
     lw $t2, 0($a1)
     mult $t1, $t2
     mflo $v0
     sw $v0, 0($a2)
     jr $ra

     .Int.division:
     lw $t1, 0($a0)
     lw $t2, 0($a1)
     div $t1, $t2
     mflo $v0
     sw $v0, 0($a2)
     jr $ra

     .Int.lesser:
     lw $t1, 0($a0)
     lw $t2, 0($a1)
     blt $t1, $t2, LesserTrue
     move $v0, $zero
     b LesserEnd
     LesserTrue:
     li $v0, 1
     LesserEnd:
     sw $v0, 0($a2)
     jr $ra

     .Int.lesserequal:
     lw $t1, 0($a0)
     lw $t2, 0($a1)
     ble $t1, $t2, LesserEqualTrue
     li $v0, 0
     b LesserEqualEnd
     LesserEqualTrue:
     li $v0, 1
     LesserEqualEnd:
     sw $v0, 0($a2)
     jr $ra

     .Int.not:
     lw $t1, 0($a0)
     move $t2, $zero
     beq $t1, $t2, FalseBool
     li $v0, 0
     b NotBool
     FalseBool:
     li $v0, 1
     NotBool:
     sw $v0, 0($a1)
     jr $ra

     .Int.igual:
     move $t1, $a0
     move $t2, $a1
     beq $t1, $t2, Iguales
     li $v0, 0
     b FinalIgual
     Iguales:
     li $v0, 1
     FinalIgual:
     sw $v0, 0($a2)
     jr $ra

     .Str.stringlength:
     move $t1, $a0
     move $v0, $zero
     move $t2, $zero

     InicioStrLen:
     add $t0, $t1, $v0
     lb $t2, 0($t0)
     beq $t2, $zero, FinStrLen
     addi $v0, $v0, 1
     b InicioStrLen

     FinStrLen:
     #sw $v0, 0($a1) El protocolo cambió
     jr $ra

     .Object.abort:
     li $v0, 10
     syscall
     jr $ra

     .Str.stringcomparison:
     move $t1, $a0
     move $t2, $a1
     move $v0, $zero
     move $t3, $zero
     move $t4, $zero
     move $v0, $zero

     StrCompCiclo:
     add $t0, $t1, $v0
     lb $t3, 0($t0)
     add $t0, $t2, $v0
     lb $t4, 0($t0)
     addi $v0, $v0, 1
     bne $t3, $t4, StrDiferentes
     beq $t3, $zero, StrIguales
     b StrCompCiclo

     StrDiferentes:
     move $v0, $zero
     jr $ra
     StrIguales:
     li $v0, 1
     jr $ra

     .Str.stringconcat:
     addi $sp, $sp, -20

     sw  $s0, 0($sp)
     sw  $s1, 4($sp)
     sw  $s2, 8($sp)
     sw  $s3, 12($sp)
     sw  $s4, 16($sp)

     move $s0, $a0
     move $s1, $a1
     move $s2, $a2
     move $s3, $ra

     jal .Str.stringlength
     move $s4, $v0
     move $a0, $s1
     jal .Str.stringlength
     add $s4, $s4, $v0
     addi $s4, $s4, 1

     #Reservando memoria
     move $a0, $s4 
     li $v0, 9
     syscall

     move $t0, $v0
     move $t1, $zero
     move $t2, $s0
     move $t3, $s1

     InicioCicloCopia:
     lb $t1, 0($t2)
     beq $t1, $zero, SegundoString
     sb $t1, 0($t0)
     addi $t0, $t0, 1
     addi $t2, $t2, 1
     b InicioCicloCopia

     SegundoString:
     lb $t1, 0($t3)
     beq $t1, $zero, FinalCopia
     sb $t1, 0($t0)
     addi $t0, $t0, 1
     addi $t3, $t3, 1
     b SegundoString

     FinalCopia:
     sb $zero, 0($t0)


     move $a0, $s0
     move $a1, $s1
     move $a2, $s2
     move $ra, $s3

     lw $s0, 0($sp)
     lw $s1, 4($sp)
     lw $s2, 8($sp)
     lw $s3, 12($sp)
     lw $s4, 16($sp)

     addi $sp, $sp, 20

     jr $ra

     #Old.Str.stringconcat:
     #Salvando registros
     addi $sp, $sp, -20
     
     sw  $s0, 4($sp)
     sw  $s1, 8($sp)
     sw  $s2, 12($sp)
     sw  $s3, 16($sp)

     move $s0, $a0
     move $s1, $a1
     move $s2, $a2
     move $s3, $ra
     
     #sw $a0, 0($sp)

     #Obteniendo el lenght de la nueva cadena
     jal .Str.stringlength
     move $s4, $v0
     move $a0, $s1
     #move $a1, $sp
     jal .Str.stringlength
     add $s4, $s4, $v0
     addi $sp, $sp, 4
     addi $s4, $s4, 1

     #Reservando memoria
     move $a0, $s4 
     li $v0, 9
     syscall

     move $t0, $v0
     move $t1, $s0
     move $t2, $zero
     move $t3, $zero
     
     StrCicloCopia:
     lb $t2, 0($t1)
     addi $t1, 1
     addi $t0, 1
     
     bne $t2, $zero, StrCicloCopia
     sb $t2, 0($t0)

     bne $t3, $zero, StrFinCopia
     move $t1, $s1

     b StrCicloCopia

     StrFinCopia:
     sb $zero, 0($t0)

     #sw $v0, 0($s2)

     move $a0, $s0
     move $a1, $s1
     move $a2, $s2
     move $ra, $s3

     lw $s0, 4($sp)
     lw $s1, 8($sp)
     lw $s2, 12($sp)
     lw $s3, 16($sp)

     addi $sp, $sp, 20

     jr $ra

     .Str.substring:
     addi $sp, $sp, -16
     
     sw  $s0 4($sp)
     sw  $s1 8($sp)
     sw  $s2 12($sp)

     move $s0, $a0
     move $s1, $a1
     move $s2, $a2

     addi $a0, $a2, 1 
     li $v0, 9
     syscall

     add $t0, $s0, $s1
     move $t1, $zero
     move $t2, $zero

     iniciocopianuevosubstr:

     add $t3, $v0, $t1
     lb $t2, 0($t0)
     sb $t2, 0($t3)

     addi $t0, $t0, 1
     addi $t1, $t1, 1

     blt $t1, $s2, iniciocopianuevosubstr
     add $t3, $v0, $t1
     sb $zero, 0($t3)

     move $a0, $s0
     move $a1, $s1
     move $a2, $s2

     lw $s0, 4($sp)
     lw $s1, 8($sp)
     lw $s2, 12($sp)

     addi $sp, $sp, 16

     jr $ra



     .Str.substringOld:
     blt $a1, $zero, SubStrWrongIndex

     addi $sp, $sp, -20
     
     sw  $s0 4($sp)
     sw  $s1 8($sp)
     sw  $s2 12($sp)
     sw  $s3 16($sp)

     move $s0, $a0
     move $s1, $a1
     move $s2, $a2
     move $s3, $ra

      
     jal .Str.stringlength

     blt $v0, $s1, SubStrWrongIndex

     addi $v0, $v0, 1

     #Reservando memoria
     move $a0, $v0 
     li $v0, 9
     syscall

     move $t0, $v0
     move $t1, $s0
     move $t2, $zero

     StrInicioCopiaSubStr:
     lb $t3, 0($t1)
     sb $t3, 0($t0)
     addi $t0, $t0, 1
     addi $t1, $t0, 1
     addi $t2, $t2, 1
     ble $t2, $s1, StrInicioCopiaSubStr

     sb $zero, 0($t0)
     
     sw $v0, 0($s2)

     move $ra, $s3

     move $a0, $s0
     move $a1, $s1
     move $a2, $s2

     lw $s0, 4($sp)
     lw $s1, 8($sp)
     lw $s2, 12($sp)
     lw $s3, 16($sp)

     addi $sp, $sp, 20

     jr $ra

     SubStrWrongIndex:
     la $a0, index_error
     li $v0, 4
     syscall
     li $v0, 10
     syscall
     
     #En este método violé la regla usual de que los parámetros van en los registros a, y se encuentran en los t.
     #Esto se realizó ya que este método solo se usa en un lugar y atendiendo a la estructura del conversor a MIPS
     .Object.Copy:
     addi $sp, $sp, -8

     sw $s0, 0($sp)
     sw $s1, 4($sp)
     move $s0, $t0
     move $s1, $t1
     addi $s1, 1
     move $a0, $s1
     li $v0, 9
     syscall
     move $t1, $v0
     $ciclocopia:
     beq $s1, $zero, $finciclocopia
     lw $t0, 0($s0)
     sw $t0, 0($t1)
     addi $s0, 4
     addi $t1, 4
     addi $s1, -1
     b $ciclocopia
     $finciclocopia:
     lw $s0, 0($sp)
     lw $s1, 4($sp)
     addi $sp, 8
     jr $ra

     .TypeCheck:
     lw $t0, 0($t0)
     InicioChequeo:
     lw $t0, 0($t0)
     beq $t0, $zero, ChequeoFalse
     beq $t0, $t1, ChequeoTrue
     b InicioChequeo
     ChequeoFalse:
     move $v0, $zero
     jr $ra
     ChequeoTrue:
     li $v0, 1
     jr $ra
Main.Special: #Main.special.main
addi $sp, $sp, -12
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,24
li $v0, 9
syscall
la $t0, Mainclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var787
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var787<-['Main', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var787
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,116($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var788<-['Main', 'main']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f0: #Object.$init
addi $sp, $sp, -8
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f3: #Object.type_name
addi $sp, $sp, -12
la $v0, st0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f4: #Object.Copy
addi $sp, $sp, -8
move $t0,$a0
li $t1,0
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .Object.Copy
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f2: #Object.Abort
addi $sp, $sp, -8
jal .Object.abort
addi $sp, $sp, 8
jr $ra
f5: #IO.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var7<-['Object', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f6: #IO.type_name
addi $sp, $sp, -12
la $v0, st1
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f7: #IO.out_string
addi $sp, $sp, -8
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $a1
jal .IO.out_string
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
move $v0, $a0
move $a1,$t0
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f8: #IO.out_int
addi $sp, $sp, -8
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $a1
jal .IO.out_int
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
move $v0, $a0
move $a1,$t0
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f9: #IO.in_string
addi $sp, $sp, -8
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.in_string
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f10: #IO.in_int
addi $sp, $sp, -8
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.in_int
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f11: #String.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var12<-['Object', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f12: #String.type_name
addi $sp, $sp, -12
la $v0, st2
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f13: #String.Length
addi $sp, $sp, -8
move $t0,$a0
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .Str.stringlength
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f14: #String.Concat
addi $sp, $sp, -8
move $t0,$a0
move $t1,$a1
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringconcat
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f15: #String.Substring
addi $sp, $sp, -8
move $t0,$a0
move $t1,$a1
move $t2,$a2
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $ra, 12($sp)
move $a0, $t0
move $a1, $t1
move $a2, $t2
jal .Str.substring
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $ra, 12($sp)
addi $sp, $sp, 16
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f16: #Bool.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var17<-['Object', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f17: #Bool.type_name
addi $sp, $sp, -12
la $v0, st3
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f18: #Board.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var22<-['IO', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,4($a0)
li $t0,0
move $v0, $t0
sw $v0,8($a0)
li $t0,0
move $v0, $t0
sw $v0,12($a0)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f19: #Board.type_name
addi $sp, $sp, -12
la $v0, st4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f20: #Board.size_of_board
addi $sp, $sp, -12
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var25
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var26<-['String', 'length']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f21: #Board.board_init
addi $sp, $sp, -276
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
move $t0,$a1
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
#Argument var.var27
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
#Argument var.var28
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var29<-['Board', 'size_of_board']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,24($sp)
li $t0,15
move $v0, $t0
sw $v0,28($sp)
lw $t0,24($sp)
lw $t1,28($sp)
seq $v0 ,$t0, $t1
sw $v0,36($sp)
lw $t0,36($sp)
bgtz $t0, Lbl10
lw $t0,4($sp)
move $v0, $t0
sw $v0,64($sp)
li $t0,16
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
seq $v0 ,$t0, $t1
sw $v0,76($sp)
lw $t0,76($sp)
bgtz $t0, Lbl8
lw $t0,4($sp)
move $v0, $t0
sw $v0,92($sp)
li $t0,20
move $v0, $t0
sw $v0,96($sp)
lw $t0,92($sp)
lw $t1,96($sp)
seq $v0 ,$t0, $t1
sw $v0,104($sp)
lw $t0,104($sp)
bgtz $t0, Lbl6
lw $t0,4($sp)
move $v0, $t0
sw $v0,120($sp)
li $t0,21
move $v0, $t0
sw $v0,124($sp)
lw $t0,120($sp)
lw $t1,124($sp)
seq $v0 ,$t0, $t1
sw $v0,132($sp)
lw $t0,132($sp)
bgtz $t0, Lbl4
lw $t0,4($sp)
move $v0, $t0
sw $v0,148($sp)
li $t0,25
move $v0, $t0
sw $v0,152($sp)
lw $t0,148($sp)
lw $t1,152($sp)
seq $v0 ,$t0, $t1
sw $v0,160($sp)
lw $t0,160($sp)
bgtz $t0, Lbl2
lw $t0,4($sp)
move $v0, $t0
sw $v0,176($sp)
li $t0,28
move $v0, $t0
sw $v0,180($sp)
lw $t0,176($sp)
lw $t1,180($sp)
seq $v0 ,$t0, $t1
sw $v0,188($sp)
lw $t0,188($sp)
bgtz $t0, Lbl0
li $t0,5
move $v0, $t0
sw $v0,204($sp)
lw $t0,204($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,5
move $v0, $t0
sw $v0,208($sp)
lw $t0,208($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($sp)
move $v0, $t0
sw $v0,212($sp)
lw $t0,212($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,216($sp)
b Lbl1
Lbl0:
li $t0,7
move $v0, $t0
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,4
move $v0, $t0
sw $v0,196($sp)
lw $t0,196($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($sp)
move $v0, $t0
sw $v0,200($sp)
lw $t0,200($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,216($sp)
Lbl1:
lw $t0,216($sp)
move $v0, $t0
sw $v0,220($sp)
lw $t0,220($sp)
move $v0, $t0
sw $v0,224($sp)
b Lbl3
Lbl2:
li $t0,5
move $v0, $t0
sw $v0,164($sp)
lw $t0,164($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,5
move $v0, $t0
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($sp)
move $v0, $t0
sw $v0,172($sp)
lw $t0,172($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,224($sp)
Lbl3:
lw $t0,224($sp)
move $v0, $t0
sw $v0,228($sp)
lw $t0,228($sp)
move $v0, $t0
sw $v0,232($sp)
b Lbl5
Lbl4:
li $t0,3
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,7
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($sp)
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,232($sp)
Lbl5:
lw $t0,232($sp)
move $v0, $t0
sw $v0,236($sp)
lw $t0,236($sp)
move $v0, $t0
sw $v0,240($sp)
b Lbl7
Lbl6:
li $t0,4
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,5
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,240($sp)
Lbl7:
lw $t0,240($sp)
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
move $v0, $t0
sw $v0,248($sp)
b Lbl9
Lbl8:
li $t0,4
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,4
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($sp)
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,248($sp)
Lbl9:
lw $t0,248($sp)
move $v0, $t0
sw $v0,252($sp)
lw $t0,252($sp)
move $v0, $t0
sw $v0,256($sp)
b Lbl11
Lbl10:
li $t0,3
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,5
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($sp)
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,256($sp)
Lbl11:
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
move $t0,$a0
move $v0, $t0
sw $v0,264($sp)
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
addi $sp, $sp, 276
jr $ra
f22: #CellularAutomaton.$init
addi $sp, $sp, -20
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Boardclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var93<-['Board', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
la $v0, st5
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,16($a0)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f23: #CellularAutomaton.type_name
addi $sp, $sp, -12
la $v0, st6
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f24: #CellularAutomaton.init
addi $sp, $sp, -28
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,16($a0)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
#Argument var.var98
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
#Argument var.var99
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var100<-['CellularAutomaton', 'board_init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,20($sp)
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, 28
jr $ra
f25: #CellularAutomaton.print
addi $sp, $sp, -168
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,28($sp)
la $v0, st7
sw $v0,36($sp)
lw $t0,28($sp)
#Argument var.var106
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
#Argument var.var107
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var108<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,40($sp)
Lbl12:
lw $t0,4($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
slt $v0, $t0, $t1
sw $v0,56($sp)
lw $t0,56($sp)
seq $v0, $t0, $zero
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl13
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
lw $t0,16($a0)
move $v0, $t0
sw $v0,72($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,76($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,80($sp)
lw $t0,72($sp)
#Argument var.var115
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,80($sp)
#Argument var.var116
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,88($sp)
#Argument var.var117
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var118<-['String', 'substr']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,84($sp)
lw $t0,68($sp)
#Argument var.var114
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,88($sp)
#Argument var.var118
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var119<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,88($sp)
move $t0,$a0
move $v0, $t0
sw $v0,92($sp)
la $v0, st8
sw $v0,100($sp)
lw $t0,92($sp)
#Argument var.var120
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,104($sp)
#Argument var.var121
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var122<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,104($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,112($sp)
lw $t0,108($sp)
lw $t1,112($sp)
add $v0, $t0, $t1
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,4($sp)
b Lbl12
Lbl13:
li $t0,0
move $v0, $t0
sw $v0,128($sp)
move $t0,$a0
move $v0, $t0
sw $v0,132($sp)
la $v0, st9
sw $v0,140($sp)
lw $t0,132($sp)
#Argument var.var128
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,144($sp)
#Argument var.var129
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var130<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,144($sp)
move $t0,$a0
move $v0, $t0
sw $v0,148($sp)
lw $t0,148($sp)
move $v0, $t0
sw $v0,152($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,152($sp)
move $v0, $t0
sw $v0,156($sp)
lw $t0,156($sp)
move $v0, $t0
sw $v0,160($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,160($sp)
move $v0, $t0
sw $v0,164($sp)
addi $sp, $sp, 168
jr $ra
f26: #CellularAutomaton.num_cells
addi $sp, $sp, -12
lw $t0,16($a0)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var136
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var137<-['String', 'length']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f27: #CellularAutomaton.cell
addi $sp, $sp, -64
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
move $t0,$a1
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl14
lw $t0,16($a0)
move $v0, $t0
sw $v0,40($sp)
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,40($sp)
#Argument var.var146
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
#Argument var.var147
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,56($sp)
#Argument var.var148
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var149<-['String', 'substr']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,56($sp)
b Lbl15
Lbl14:
la $v0, st10
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,56($sp)
Lbl15:
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
addi $sp, $sp, 64
jr $ra
f28: #CellularAutomaton.north
addi $sp, $sp, -72
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl16
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
sub $v0, $t0, $t1
sw $v0,56($sp)
lw $t0,40($sp)
#Argument var.var160
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
#Argument var.var163
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var165<-['CellularAutomaton', 'cell']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,64($sp)
b Lbl17
Lbl16:
la $v0, st11
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,64($sp)
Lbl17:
lw $t0,64($sp)
move $v0, $t0
sw $v0,68($sp)
addi $sp, $sp, 72
jr $ra
f29: #CellularAutomaton.south
addi $sp, $sp, -72
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
add $v0, $t0, $t1
sw $v0,20($sp)
lw $t0,4($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl18
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
add $v0, $t0, $t1
sw $v0,56($sp)
lw $t0,40($sp)
#Argument var.var176
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
#Argument var.var179
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var181<-['CellularAutomaton', 'cell']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,64($sp)
b Lbl19
Lbl18:
la $v0, st12
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,64($sp)
Lbl19:
lw $t0,64($sp)
move $v0, $t0
sw $v0,68($sp)
addi $sp, $sp, 72
jr $ra
f30: #CellularAutomaton.east
addi $sp, $sp, -108
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
add $v0, $t0, $t1
sw $v0,16($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
div $t0, $t1
mflo $v0
sw $v0,28($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
mult $t0, $t1
mflo $v0
sw $v0,40($sp)
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
add $v0, $t0, $t1
sw $v0,56($sp)
lw $t0,40($sp)
lw $t1,56($sp)
seq $v0 ,$t0, $t1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl20
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
add $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,76($sp)
#Argument var.var201
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var204
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var206<-['CellularAutomaton', 'cell']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl21
Lbl20:
la $v0, st13
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl21:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
addi $sp, $sp, 108
jr $ra
f31: #CellularAutomaton.west
addi $sp, $sp, -116
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
seq $v0 ,$t0, $t1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl24
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
div $t0, $t1
mflo $v0
sw $v0,40($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
mult $t0, $t1
mflo $v0
sw $v0,52($sp)
move $t0,$a1
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
seq $v0 ,$t0, $t1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl22
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
sub $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,76($sp)
#Argument var.var225
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var228
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var230<-['CellularAutomaton', 'cell']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl23
Lbl22:
la $v0, st15
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl23:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
b Lbl25
Lbl24:
la $v0, st14
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,108($sp)
Lbl25:
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
addi $sp, $sp, 116
jr $ra
f32: #CellularAutomaton.northwest
addi $sp, $sp, -128
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl28
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
div $t0, $t1
mflo $v0
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
mult $t0, $t1
mflo $v0
sw $v0,64($sp)
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
seq $v0 ,$t0, $t1
sw $v0,76($sp)
lw $t0,76($sp)
bgtz $t0, Lbl26
move $t0,$a0
move $v0, $t0
sw $v0,88($sp)
move $t0,$a1
move $v0, $t0
sw $v0,92($sp)
li $t0,1
move $v0, $t0
sw $v0,96($sp)
lw $t0,92($sp)
lw $t1,96($sp)
sub $v0, $t0, $t1
sw $v0,104($sp)
lw $t0,88($sp)
#Argument var.var254
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
#Argument var.var257
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var259<-['CellularAutomaton', 'north']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
b Lbl27
Lbl26:
la $v0, st17
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,112($sp)
Lbl27:
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
b Lbl29
Lbl28:
la $v0, st16
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,120($sp)
Lbl29:
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
addi $sp, $sp, 128
jr $ra
f33: #CellularAutomaton.northeast
addi $sp, $sp, -152
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl32
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
li $t0,1
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
add $v0, $t0, $t1
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
div $t0, $t1
mflo $v0
sw $v0,64($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
mult $t0, $t1
mflo $v0
sw $v0,76($sp)
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
add $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,76($sp)
lw $t1,92($sp)
seq $v0 ,$t0, $t1
sw $v0,100($sp)
lw $t0,100($sp)
bgtz $t0, Lbl30
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
move $t0,$a1
move $v0, $t0
sw $v0,116($sp)
li $t0,1
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
add $v0, $t0, $t1
sw $v0,128($sp)
lw $t0,112($sp)
#Argument var.var289
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,132($sp)
#Argument var.var292
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var294<-['CellularAutomaton', 'north']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl31
Lbl30:
la $v0, st19
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl31:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
b Lbl33
Lbl32:
la $v0, st18
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,144($sp)
Lbl33:
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
addi $sp, $sp, 152
jr $ra
f34: #CellularAutomaton.southeast
addi $sp, $sp, -152
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
add $v0, $t0, $t1
sw $v0,20($sp)
lw $t0,4($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl36
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
li $t0,1
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
add $v0, $t0, $t1
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
div $t0, $t1
mflo $v0
sw $v0,64($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
mult $t0, $t1
mflo $v0
sw $v0,76($sp)
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
add $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,76($sp)
lw $t1,92($sp)
seq $v0 ,$t0, $t1
sw $v0,100($sp)
lw $t0,100($sp)
bgtz $t0, Lbl34
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
move $t0,$a1
move $v0, $t0
sw $v0,116($sp)
li $t0,1
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
add $v0, $t0, $t1
sw $v0,128($sp)
lw $t0,112($sp)
#Argument var.var324
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,132($sp)
#Argument var.var327
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,64($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var329<-['CellularAutomaton', 'south']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl35
Lbl34:
la $v0, st21
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl35:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
b Lbl37
Lbl36:
la $v0, st20
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,144($sp)
Lbl37:
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
addi $sp, $sp, 152
jr $ra
f35: #CellularAutomaton.southwest
addi $sp, $sp, -128
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
add $v0, $t0, $t1
sw $v0,20($sp)
lw $t0,4($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl40
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
div $t0, $t1
mflo $v0
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
mult $t0, $t1
mflo $v0
sw $v0,64($sp)
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
seq $v0 ,$t0, $t1
sw $v0,76($sp)
lw $t0,76($sp)
bgtz $t0, Lbl38
move $t0,$a0
move $v0, $t0
sw $v0,88($sp)
move $t0,$a1
move $v0, $t0
sw $v0,92($sp)
li $t0,1
move $v0, $t0
sw $v0,96($sp)
lw $t0,92($sp)
lw $t1,96($sp)
sub $v0, $t0, $t1
sw $v0,104($sp)
lw $t0,88($sp)
#Argument var.var353
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
#Argument var.var356
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,64($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var358<-['CellularAutomaton', 'south']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
b Lbl39
Lbl38:
la $v0, st23
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,112($sp)
Lbl39:
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
b Lbl41
Lbl40:
la $v0, st22
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,120($sp)
Lbl41:
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
addi $sp, $sp, 128
jr $ra
f36: #CellularAutomaton.neighbors
addi $sp, $sp, -412
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
#Argument var.var363
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
#Argument var.var364
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var365<-['CellularAutomaton', 'north']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,12($sp)
la $v0, st24
sw $v0,20($sp)
lw $t0,12($sp)
lw $t1,20($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl42
li $t0,0
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
b Lbl43
Lbl42:
li $t0,1
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,40($sp)
Lbl43:
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
lw $t0,48($sp)
#Argument var.var373
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
#Argument var.var374
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,64($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var375<-['CellularAutomaton', 'south']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,56($sp)
la $v0, st25
sw $v0,64($sp)
lw $t0,56($sp)
lw $t1,64($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,72($sp)
lw $t0,72($sp)
bgtz $t0, Lbl44
li $t0,0
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,84($sp)
b Lbl45
Lbl44:
li $t0,1
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,84($sp)
Lbl45:
lw $t0,84($sp)
move $v0, $t0
sw $v0,88($sp)
lw $t0,44($sp)
lw $t1,88($sp)
add $v0, $t0, $t1
sw $v0,96($sp)
move $t0,$a0
move $v0, $t0
sw $v0,100($sp)
move $t0,$a1
move $v0, $t0
sw $v0,104($sp)
lw $t0,100($sp)
#Argument var.var385
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
#Argument var.var386
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,68($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var387<-['CellularAutomaton', 'east']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,108($sp)
la $v0, st26
sw $v0,116($sp)
lw $t0,108($sp)
lw $t1,116($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,124($sp)
lw $t0,124($sp)
bgtz $t0, Lbl46
li $t0,0
move $v0, $t0
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl47
Lbl46:
li $t0,1
move $v0, $t0
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl47:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,96($sp)
lw $t1,140($sp)
add $v0, $t0, $t1
sw $v0,148($sp)
move $t0,$a0
move $v0, $t0
sw $v0,152($sp)
move $t0,$a1
move $v0, $t0
sw $v0,156($sp)
lw $t0,152($sp)
#Argument var.var397
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,160($sp)
#Argument var.var398
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,72($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var399<-['CellularAutomaton', 'west']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,160($sp)
la $v0, st27
sw $v0,168($sp)
lw $t0,160($sp)
lw $t1,168($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,176($sp)
lw $t0,176($sp)
bgtz $t0, Lbl48
li $t0,0
move $v0, $t0
sw $v0,184($sp)
lw $t0,184($sp)
move $v0, $t0
sw $v0,188($sp)
b Lbl49
Lbl48:
li $t0,1
move $v0, $t0
sw $v0,180($sp)
lw $t0,180($sp)
move $v0, $t0
sw $v0,188($sp)
Lbl49:
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
lw $t0,148($sp)
lw $t1,192($sp)
add $v0, $t0, $t1
sw $v0,200($sp)
move $t0,$a0
move $v0, $t0
sw $v0,204($sp)
move $t0,$a1
move $v0, $t0
sw $v0,208($sp)
lw $t0,204($sp)
#Argument var.var409
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,212($sp)
#Argument var.var410
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,80($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var411<-['CellularAutomaton', 'northeast']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,212($sp)
la $v0, st28
sw $v0,220($sp)
lw $t0,212($sp)
lw $t1,220($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,228($sp)
lw $t0,228($sp)
bgtz $t0, Lbl50
li $t0,0
move $v0, $t0
sw $v0,236($sp)
lw $t0,236($sp)
move $v0, $t0
sw $v0,240($sp)
b Lbl51
Lbl50:
li $t0,1
move $v0, $t0
sw $v0,232($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,240($sp)
Lbl51:
lw $t0,240($sp)
move $v0, $t0
sw $v0,244($sp)
lw $t0,200($sp)
lw $t1,244($sp)
add $v0, $t0, $t1
sw $v0,252($sp)
move $t0,$a0
move $v0, $t0
sw $v0,256($sp)
move $t0,$a1
move $v0, $t0
sw $v0,260($sp)
lw $t0,256($sp)
#Argument var.var421
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,264($sp)
#Argument var.var422
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,76($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var423<-['CellularAutomaton', 'northwest']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,264($sp)
la $v0, st29
sw $v0,272($sp)
lw $t0,264($sp)
lw $t1,272($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,280($sp)
lw $t0,280($sp)
bgtz $t0, Lbl52
li $t0,0
move $v0, $t0
sw $v0,288($sp)
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
b Lbl53
Lbl52:
li $t0,1
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
move $v0, $t0
sw $v0,292($sp)
Lbl53:
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,252($sp)
lw $t1,296($sp)
add $v0, $t0, $t1
sw $v0,304($sp)
move $t0,$a0
move $v0, $t0
sw $v0,308($sp)
move $t0,$a1
move $v0, $t0
sw $v0,312($sp)
lw $t0,308($sp)
#Argument var.var433
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,316($sp)
#Argument var.var434
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,84($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var435<-['CellularAutomaton', 'southeast']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,316($sp)
la $v0, st30
sw $v0,324($sp)
lw $t0,316($sp)
lw $t1,324($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,332($sp)
lw $t0,332($sp)
bgtz $t0, Lbl54
li $t0,0
move $v0, $t0
sw $v0,340($sp)
lw $t0,340($sp)
move $v0, $t0
sw $v0,344($sp)
b Lbl55
Lbl54:
li $t0,1
move $v0, $t0
sw $v0,336($sp)
lw $t0,336($sp)
move $v0, $t0
sw $v0,344($sp)
Lbl55:
lw $t0,344($sp)
move $v0, $t0
sw $v0,348($sp)
lw $t0,304($sp)
lw $t1,348($sp)
add $v0, $t0, $t1
sw $v0,356($sp)
move $t0,$a0
move $v0, $t0
sw $v0,360($sp)
move $t0,$a1
move $v0, $t0
sw $v0,364($sp)
lw $t0,360($sp)
#Argument var.var445
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,368($sp)
#Argument var.var446
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,88($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var447<-['CellularAutomaton', 'southwest']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,368($sp)
la $v0, st31
sw $v0,376($sp)
lw $t0,368($sp)
lw $t1,376($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,384($sp)
lw $t0,384($sp)
bgtz $t0, Lbl56
li $t0,0
move $v0, $t0
sw $v0,392($sp)
lw $t0,392($sp)
move $v0, $t0
sw $v0,396($sp)
b Lbl57
Lbl56:
li $t0,1
move $v0, $t0
sw $v0,388($sp)
lw $t0,388($sp)
move $v0, $t0
sw $v0,396($sp)
Lbl57:
lw $t0,396($sp)
move $v0, $t0
sw $v0,400($sp)
lw $t0,356($sp)
lw $t1,400($sp)
add $v0, $t0, $t1
sw $v0,408($sp)
addi $sp, $sp, 412
jr $ra
f37: #CellularAutomaton.cell_at_next_evolution
addi $sp, $sp, -136
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
#Argument var.var457
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
#Argument var.var458
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,92($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var459<-['CellularAutomaton', 'neighbors']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,12($sp)
li $t0,3
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
lw $t1,16($sp)
seq $v0 ,$t0, $t1
sw $v0,24($sp)
lw $t0,24($sp)
bgtz $t0, Lbl62
move $t0,$a0
move $v0, $t0
sw $v0,36($sp)
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
lw $t0,36($sp)
#Argument var.var464
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
#Argument var.var465
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,92($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var466<-['CellularAutomaton', 'neighbors']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,44($sp)
li $t0,2
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
seq $v0 ,$t0, $t1
sw $v0,56($sp)
lw $t0,56($sp)
bgtz $t0, Lbl60
la $v0, st36
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
b Lbl61
Lbl60:
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
move $t0,$a1
move $v0, $t0
sw $v0,64($sp)
lw $t0,60($sp)
#Argument var.var470
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,68($sp)
#Argument var.var471
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var472<-['CellularAutomaton', 'cell']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,68($sp)
la $v0, st33
sw $v0,76($sp)
lw $t0,68($sp)
lw $t1,76($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,84($sp)
lw $t0,84($sp)
bgtz $t0, Lbl58
la $v0, st35
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
b Lbl59
Lbl58:
la $v0, st34
sw $v0,92($sp)
lw $t0,92($sp)
move $v0, $t0
sw $v0,104($sp)
Lbl59:
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,120($sp)
Lbl61:
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
move $v0, $t0
sw $v0,128($sp)
b Lbl63
Lbl62:
la $v0, st32
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,128($sp)
Lbl63:
lw $t0,128($sp)
move $v0, $t0
sw $v0,132($sp)
addi $sp, $sp, 136
jr $ra
f38: #CellularAutomaton.evolve
addi $sp, $sp, -152
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
lw $t0,20($sp)
#Argument var.var487
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var488<-['CellularAutomaton', 'num_cells']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,24($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,16($sp)
la $v0, st37
sw $v0,40($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,32($sp)
Lbl64:
lw $t0,4($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,48($sp)
lw $t1,52($sp)
slt $v0, $t0, $t1
sw $v0,60($sp)
lw $t0,60($sp)
seq $v0, $t0, $zero
sw $v0,68($sp)
lw $t0,68($sp)
bgtz $t0, Lbl65
lw $t0,32($sp)
move $v0, $t0
sw $v0,72($sp)
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
#Argument var.var498
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,84($sp)
#Argument var.var499
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,96($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var500<-['CellularAutomaton', 'cell_at_next_evolution']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,84($sp)
lw $t0,72($sp)
#Argument var.var497
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,88($sp)
#Argument var.var500
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
la $t0,Stringclase
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var501<-['String', 'concat']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,92($sp)
li $t0,1
move $v0, $t0
sw $v0,96($sp)
lw $t0,92($sp)
lw $t1,96($sp)
add $v0, $t0, $t1
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,4($sp)
b Lbl64
Lbl65:
li $t0,0
move $v0, $t0
sw $v0,112($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,16($a0)
move $t0,$a0
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
move $v0, $t0
sw $v0,128($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
addi $sp, $sp, 152
jr $ra
f39: #CellularAutomaton.option
addi $sp, $sp, -1096
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
la $v0, st38
sw $v0,24($sp)
lw $t0,16($sp)
#Argument var.var517
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
#Argument var.var518
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var519<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,28($sp)
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
la $v0, st39
sw $v0,40($sp)
lw $t0,32($sp)
#Argument var.var520
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
#Argument var.var521
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var522<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
la $v0, st40
sw $v0,56($sp)
lw $t0,48($sp)
#Argument var.var523
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
#Argument var.var524
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var525<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,60($sp)
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
la $v0, st41
sw $v0,72($sp)
lw $t0,64($sp)
#Argument var.var526
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
#Argument var.var527
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var528<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,76($sp)
move $t0,$a0
move $v0, $t0
sw $v0,80($sp)
la $v0, st42
sw $v0,88($sp)
lw $t0,80($sp)
#Argument var.var529
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,92($sp)
#Argument var.var530
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var531<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,92($sp)
move $t0,$a0
move $v0, $t0
sw $v0,96($sp)
la $v0, st43
sw $v0,104($sp)
lw $t0,96($sp)
#Argument var.var532
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
#Argument var.var533
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var534<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,108($sp)
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
la $v0, st44
sw $v0,120($sp)
lw $t0,112($sp)
#Argument var.var535
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,124($sp)
#Argument var.var536
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var537<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,124($sp)
move $t0,$a0
move $v0, $t0
sw $v0,128($sp)
la $v0, st45
sw $v0,136($sp)
lw $t0,128($sp)
#Argument var.var538
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,140($sp)
#Argument var.var539
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var540<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,140($sp)
move $t0,$a0
move $v0, $t0
sw $v0,144($sp)
la $v0, st46
sw $v0,152($sp)
lw $t0,144($sp)
#Argument var.var541
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,156($sp)
#Argument var.var542
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var543<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,156($sp)
move $t0,$a0
move $v0, $t0
sw $v0,160($sp)
la $v0, st47
sw $v0,168($sp)
lw $t0,160($sp)
#Argument var.var544
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,172($sp)
#Argument var.var545
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var546<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,172($sp)
move $t0,$a0
move $v0, $t0
sw $v0,176($sp)
la $v0, st48
sw $v0,184($sp)
lw $t0,176($sp)
#Argument var.var547
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,188($sp)
#Argument var.var548
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var549<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,188($sp)
move $t0,$a0
move $v0, $t0
sw $v0,192($sp)
la $v0, st49
sw $v0,200($sp)
lw $t0,192($sp)
#Argument var.var550
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,204($sp)
#Argument var.var551
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var552<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,204($sp)
move $t0,$a0
move $v0, $t0
sw $v0,208($sp)
la $v0, st50
sw $v0,216($sp)
lw $t0,208($sp)
#Argument var.var553
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,220($sp)
#Argument var.var554
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var555<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,220($sp)
move $t0,$a0
move $v0, $t0
sw $v0,224($sp)
la $v0, st51
sw $v0,232($sp)
lw $t0,224($sp)
#Argument var.var556
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,236($sp)
#Argument var.var557
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var558<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,236($sp)
move $t0,$a0
move $v0, $t0
sw $v0,240($sp)
la $v0, st52
sw $v0,248($sp)
lw $t0,240($sp)
#Argument var.var559
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,252($sp)
#Argument var.var560
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var561<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,252($sp)
move $t0,$a0
move $v0, $t0
sw $v0,256($sp)
la $v0, st53
sw $v0,264($sp)
lw $t0,256($sp)
#Argument var.var562
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,268($sp)
#Argument var.var563
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var564<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,268($sp)
move $t0,$a0
move $v0, $t0
sw $v0,272($sp)
la $v0, st54
sw $v0,280($sp)
lw $t0,272($sp)
#Argument var.var565
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,284($sp)
#Argument var.var566
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var567<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,284($sp)
move $t0,$a0
move $v0, $t0
sw $v0,288($sp)
la $v0, st55
sw $v0,296($sp)
lw $t0,288($sp)
#Argument var.var568
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,300($sp)
#Argument var.var569
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var570<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,300($sp)
move $t0,$a0
move $v0, $t0
sw $v0,304($sp)
la $v0, st56
sw $v0,312($sp)
lw $t0,304($sp)
#Argument var.var571
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,316($sp)
#Argument var.var572
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var573<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,316($sp)
move $t0,$a0
move $v0, $t0
sw $v0,320($sp)
la $v0, st57
sw $v0,328($sp)
lw $t0,320($sp)
#Argument var.var574
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,332($sp)
#Argument var.var575
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var576<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,332($sp)
move $t0,$a0
move $v0, $t0
sw $v0,336($sp)
la $v0, st58
sw $v0,344($sp)
lw $t0,336($sp)
#Argument var.var577
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,348($sp)
#Argument var.var578
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var579<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,348($sp)
move $t0,$a0
move $v0, $t0
sw $v0,352($sp)
la $v0, st59
sw $v0,360($sp)
lw $t0,352($sp)
#Argument var.var580
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,364($sp)
#Argument var.var581
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var582<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,364($sp)
move $t0,$a0
move $v0, $t0
sw $v0,368($sp)
la $v0, st60
sw $v0,376($sp)
lw $t0,368($sp)
#Argument var.var583
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,380($sp)
#Argument var.var584
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var585<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,380($sp)
move $t0,$a0
move $v0, $t0
sw $v0,384($sp)
lw $t0,384($sp)
#Argument var.var586
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var587<-['CellularAutomaton', 'in_int']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,388($sp)
lw $t0,388($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,392($sp)
la $v0, st61
sw $v0,400($sp)
lw $t0,392($sp)
#Argument var.var588
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,404($sp)
#Argument var.var589
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var590<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,404($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,408($sp)
li $t0,1
move $v0, $t0
sw $v0,412($sp)
lw $t0,408($sp)
lw $t1,412($sp)
seq $v0 ,$t0, $t1
sw $v0,420($sp)
lw $t0,420($sp)
bgtz $t0, Lbl106
lw $t0,4($sp)
move $v0, $t0
sw $v0,432($sp)
li $t0,2
move $v0, $t0
sw $v0,436($sp)
lw $t0,432($sp)
lw $t1,436($sp)
seq $v0 ,$t0, $t1
sw $v0,444($sp)
lw $t0,444($sp)
bgtz $t0, Lbl104
lw $t0,4($sp)
move $v0, $t0
sw $v0,456($sp)
li $t0,3
move $v0, $t0
sw $v0,460($sp)
lw $t0,456($sp)
lw $t1,460($sp)
seq $v0 ,$t0, $t1
sw $v0,468($sp)
lw $t0,468($sp)
bgtz $t0, Lbl102
lw $t0,4($sp)
move $v0, $t0
sw $v0,480($sp)
li $t0,4
move $v0, $t0
sw $v0,484($sp)
lw $t0,480($sp)
lw $t1,484($sp)
seq $v0 ,$t0, $t1
sw $v0,492($sp)
lw $t0,492($sp)
bgtz $t0, Lbl100
lw $t0,4($sp)
move $v0, $t0
sw $v0,504($sp)
li $t0,5
move $v0, $t0
sw $v0,508($sp)
lw $t0,504($sp)
lw $t1,508($sp)
seq $v0 ,$t0, $t1
sw $v0,516($sp)
lw $t0,516($sp)
bgtz $t0, Lbl98
lw $t0,4($sp)
move $v0, $t0
sw $v0,528($sp)
li $t0,6
move $v0, $t0
sw $v0,532($sp)
lw $t0,528($sp)
lw $t1,532($sp)
seq $v0 ,$t0, $t1
sw $v0,540($sp)
lw $t0,540($sp)
bgtz $t0, Lbl96
lw $t0,4($sp)
move $v0, $t0
sw $v0,552($sp)
li $t0,7
move $v0, $t0
sw $v0,556($sp)
lw $t0,552($sp)
lw $t1,556($sp)
seq $v0 ,$t0, $t1
sw $v0,564($sp)
lw $t0,564($sp)
bgtz $t0, Lbl94
lw $t0,4($sp)
move $v0, $t0
sw $v0,576($sp)
li $t0,8
move $v0, $t0
sw $v0,580($sp)
lw $t0,576($sp)
lw $t1,580($sp)
seq $v0 ,$t0, $t1
sw $v0,588($sp)
lw $t0,588($sp)
bgtz $t0, Lbl92
lw $t0,4($sp)
move $v0, $t0
sw $v0,600($sp)
li $t0,9
move $v0, $t0
sw $v0,604($sp)
lw $t0,600($sp)
lw $t1,604($sp)
seq $v0 ,$t0, $t1
sw $v0,612($sp)
lw $t0,612($sp)
bgtz $t0, Lbl90
lw $t0,4($sp)
move $v0, $t0
sw $v0,624($sp)
li $t0,10
move $v0, $t0
sw $v0,628($sp)
lw $t0,624($sp)
lw $t1,628($sp)
seq $v0 ,$t0, $t1
sw $v0,636($sp)
lw $t0,636($sp)
bgtz $t0, Lbl88
lw $t0,4($sp)
move $v0, $t0
sw $v0,648($sp)
li $t0,11
move $v0, $t0
sw $v0,652($sp)
lw $t0,648($sp)
lw $t1,652($sp)
seq $v0 ,$t0, $t1
sw $v0,660($sp)
lw $t0,660($sp)
bgtz $t0, Lbl86
lw $t0,4($sp)
move $v0, $t0
sw $v0,672($sp)
li $t0,12
move $v0, $t0
sw $v0,676($sp)
lw $t0,672($sp)
lw $t1,676($sp)
seq $v0 ,$t0, $t1
sw $v0,684($sp)
lw $t0,684($sp)
bgtz $t0, Lbl84
lw $t0,4($sp)
move $v0, $t0
sw $v0,696($sp)
li $t0,13
move $v0, $t0
sw $v0,700($sp)
lw $t0,696($sp)
lw $t1,700($sp)
seq $v0 ,$t0, $t1
sw $v0,708($sp)
lw $t0,708($sp)
bgtz $t0, Lbl82
lw $t0,4($sp)
move $v0, $t0
sw $v0,720($sp)
li $t0,14
move $v0, $t0
sw $v0,724($sp)
lw $t0,720($sp)
lw $t1,724($sp)
seq $v0 ,$t0, $t1
sw $v0,732($sp)
lw $t0,732($sp)
bgtz $t0, Lbl80
lw $t0,4($sp)
move $v0, $t0
sw $v0,744($sp)
li $t0,15
move $v0, $t0
sw $v0,748($sp)
lw $t0,744($sp)
lw $t1,748($sp)
seq $v0 ,$t0, $t1
sw $v0,756($sp)
lw $t0,756($sp)
bgtz $t0, Lbl78
lw $t0,4($sp)
move $v0, $t0
sw $v0,768($sp)
li $t0,16
move $v0, $t0
sw $v0,772($sp)
lw $t0,768($sp)
lw $t1,772($sp)
seq $v0 ,$t0, $t1
sw $v0,780($sp)
lw $t0,780($sp)
bgtz $t0, Lbl76
lw $t0,4($sp)
move $v0, $t0
sw $v0,792($sp)
li $t0,17
move $v0, $t0
sw $v0,796($sp)
lw $t0,792($sp)
lw $t1,796($sp)
seq $v0 ,$t0, $t1
sw $v0,804($sp)
lw $t0,804($sp)
bgtz $t0, Lbl74
lw $t0,4($sp)
move $v0, $t0
sw $v0,816($sp)
li $t0,18
move $v0, $t0
sw $v0,820($sp)
lw $t0,816($sp)
lw $t1,820($sp)
seq $v0 ,$t0, $t1
sw $v0,828($sp)
lw $t0,828($sp)
bgtz $t0, Lbl72
lw $t0,4($sp)
move $v0, $t0
sw $v0,840($sp)
li $t0,19
move $v0, $t0
sw $v0,844($sp)
lw $t0,840($sp)
lw $t1,844($sp)
seq $v0 ,$t0, $t1
sw $v0,852($sp)
lw $t0,852($sp)
bgtz $t0, Lbl70
lw $t0,4($sp)
move $v0, $t0
sw $v0,864($sp)
li $t0,20
move $v0, $t0
sw $v0,868($sp)
lw $t0,864($sp)
lw $t1,868($sp)
seq $v0 ,$t0, $t1
sw $v0,876($sp)
lw $t0,876($sp)
bgtz $t0, Lbl68
lw $t0,4($sp)
move $v0, $t0
sw $v0,888($sp)
li $t0,21
move $v0, $t0
sw $v0,892($sp)
lw $t0,888($sp)
lw $t1,892($sp)
seq $v0 ,$t0, $t1
sw $v0,900($sp)
lw $t0,900($sp)
bgtz $t0, Lbl66
la $v0, st83
sw $v0,916($sp)
lw $t0,916($sp)
move $v0, $t0
sw $v0,920($sp)
b Lbl67
Lbl66:
la $v0, st82
sw $v0,908($sp)
lw $t0,908($sp)
move $v0, $t0
sw $v0,920($sp)
Lbl67:
lw $t0,920($sp)
move $v0, $t0
sw $v0,924($sp)
lw $t0,924($sp)
move $v0, $t0
sw $v0,928($sp)
b Lbl69
Lbl68:
la $v0, st81
sw $v0,884($sp)
lw $t0,884($sp)
move $v0, $t0
sw $v0,928($sp)
Lbl69:
lw $t0,928($sp)
move $v0, $t0
sw $v0,932($sp)
lw $t0,932($sp)
move $v0, $t0
sw $v0,936($sp)
b Lbl71
Lbl70:
la $v0, st80
sw $v0,860($sp)
lw $t0,860($sp)
move $v0, $t0
sw $v0,936($sp)
Lbl71:
lw $t0,936($sp)
move $v0, $t0
sw $v0,940($sp)
lw $t0,940($sp)
move $v0, $t0
sw $v0,944($sp)
b Lbl73
Lbl72:
la $v0, st79
sw $v0,836($sp)
lw $t0,836($sp)
move $v0, $t0
sw $v0,944($sp)
Lbl73:
lw $t0,944($sp)
move $v0, $t0
sw $v0,948($sp)
lw $t0,948($sp)
move $v0, $t0
sw $v0,952($sp)
b Lbl75
Lbl74:
la $v0, st78
sw $v0,812($sp)
lw $t0,812($sp)
move $v0, $t0
sw $v0,952($sp)
Lbl75:
lw $t0,952($sp)
move $v0, $t0
sw $v0,956($sp)
lw $t0,956($sp)
move $v0, $t0
sw $v0,960($sp)
b Lbl77
Lbl76:
la $v0, st77
sw $v0,788($sp)
lw $t0,788($sp)
move $v0, $t0
sw $v0,960($sp)
Lbl77:
lw $t0,960($sp)
move $v0, $t0
sw $v0,964($sp)
lw $t0,964($sp)
move $v0, $t0
sw $v0,968($sp)
b Lbl79
Lbl78:
la $v0, st76
sw $v0,764($sp)
lw $t0,764($sp)
move $v0, $t0
sw $v0,968($sp)
Lbl79:
lw $t0,968($sp)
move $v0, $t0
sw $v0,972($sp)
lw $t0,972($sp)
move $v0, $t0
sw $v0,976($sp)
b Lbl81
Lbl80:
la $v0, st75
sw $v0,740($sp)
lw $t0,740($sp)
move $v0, $t0
sw $v0,976($sp)
Lbl81:
lw $t0,976($sp)
move $v0, $t0
sw $v0,980($sp)
lw $t0,980($sp)
move $v0, $t0
sw $v0,984($sp)
b Lbl83
Lbl82:
la $v0, st74
sw $v0,716($sp)
lw $t0,716($sp)
move $v0, $t0
sw $v0,984($sp)
Lbl83:
lw $t0,984($sp)
move $v0, $t0
sw $v0,988($sp)
lw $t0,988($sp)
move $v0, $t0
sw $v0,992($sp)
b Lbl85
Lbl84:
la $v0, st73
sw $v0,692($sp)
lw $t0,692($sp)
move $v0, $t0
sw $v0,992($sp)
Lbl85:
lw $t0,992($sp)
move $v0, $t0
sw $v0,996($sp)
lw $t0,996($sp)
move $v0, $t0
sw $v0,1000($sp)
b Lbl87
Lbl86:
la $v0, st72
sw $v0,668($sp)
lw $t0,668($sp)
move $v0, $t0
sw $v0,1000($sp)
Lbl87:
lw $t0,1000($sp)
move $v0, $t0
sw $v0,1004($sp)
lw $t0,1004($sp)
move $v0, $t0
sw $v0,1008($sp)
b Lbl89
Lbl88:
la $v0, st71
sw $v0,644($sp)
lw $t0,644($sp)
move $v0, $t0
sw $v0,1008($sp)
Lbl89:
lw $t0,1008($sp)
move $v0, $t0
sw $v0,1012($sp)
lw $t0,1012($sp)
move $v0, $t0
sw $v0,1016($sp)
b Lbl91
Lbl90:
la $v0, st70
sw $v0,620($sp)
lw $t0,620($sp)
move $v0, $t0
sw $v0,1016($sp)
Lbl91:
lw $t0,1016($sp)
move $v0, $t0
sw $v0,1020($sp)
lw $t0,1020($sp)
move $v0, $t0
sw $v0,1024($sp)
b Lbl93
Lbl92:
la $v0, st69
sw $v0,596($sp)
lw $t0,596($sp)
move $v0, $t0
sw $v0,1024($sp)
Lbl93:
lw $t0,1024($sp)
move $v0, $t0
sw $v0,1028($sp)
lw $t0,1028($sp)
move $v0, $t0
sw $v0,1032($sp)
b Lbl95
Lbl94:
la $v0, st68
sw $v0,572($sp)
lw $t0,572($sp)
move $v0, $t0
sw $v0,1032($sp)
Lbl95:
lw $t0,1032($sp)
move $v0, $t0
sw $v0,1036($sp)
lw $t0,1036($sp)
move $v0, $t0
sw $v0,1040($sp)
b Lbl97
Lbl96:
la $v0, st67
sw $v0,548($sp)
lw $t0,548($sp)
move $v0, $t0
sw $v0,1040($sp)
Lbl97:
lw $t0,1040($sp)
move $v0, $t0
sw $v0,1044($sp)
lw $t0,1044($sp)
move $v0, $t0
sw $v0,1048($sp)
b Lbl99
Lbl98:
la $v0, st66
sw $v0,524($sp)
lw $t0,524($sp)
move $v0, $t0
sw $v0,1048($sp)
Lbl99:
lw $t0,1048($sp)
move $v0, $t0
sw $v0,1052($sp)
lw $t0,1052($sp)
move $v0, $t0
sw $v0,1056($sp)
b Lbl101
Lbl100:
la $v0, st65
sw $v0,500($sp)
lw $t0,500($sp)
move $v0, $t0
sw $v0,1056($sp)
Lbl101:
lw $t0,1056($sp)
move $v0, $t0
sw $v0,1060($sp)
lw $t0,1060($sp)
move $v0, $t0
sw $v0,1064($sp)
b Lbl103
Lbl102:
la $v0, st64
sw $v0,476($sp)
lw $t0,476($sp)
move $v0, $t0
sw $v0,1064($sp)
Lbl103:
lw $t0,1064($sp)
move $v0, $t0
sw $v0,1068($sp)
lw $t0,1068($sp)
move $v0, $t0
sw $v0,1072($sp)
b Lbl105
Lbl104:
la $v0, st63
sw $v0,452($sp)
lw $t0,452($sp)
move $v0, $t0
sw $v0,1072($sp)
Lbl105:
lw $t0,1072($sp)
move $v0, $t0
sw $v0,1076($sp)
lw $t0,1076($sp)
move $v0, $t0
sw $v0,1080($sp)
b Lbl107
Lbl106:
la $v0, st62
sw $v0,428($sp)
lw $t0,428($sp)
move $v0, $t0
sw $v0,1080($sp)
Lbl107:
lw $t0,1080($sp)
move $v0, $t0
sw $v0,1084($sp)
lw $t0,1084($sp)
move $v0, $t0
sw $v0,1088($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,1088($sp)
move $v0, $t0
sw $v0,1092($sp)
addi $sp, $sp, 1096
jr $ra
f40: #CellularAutomaton.prompt
addi $sp, $sp, -120
la $v0, st84
sw $v0,12($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
la $v0, st85
sw $v0,28($sp)
lw $t0,20($sp)
#Argument var.var743
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,32($sp)
#Argument var.var744
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var745<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,32($sp)
move $t0,$a0
move $v0, $t0
sw $v0,36($sp)
la $v0, st86
sw $v0,44($sp)
lw $t0,36($sp)
#Argument var.var746
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
#Argument var.var747
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var748<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,48($sp)
move $t0,$a0
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
#Argument var.var749
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var750<-['CellularAutomaton', 'in_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
la $v0, st87
sw $v0,68($sp)
lw $t0,60($sp)
#Argument var.var751
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
#Argument var.var752
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var753<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,72($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,76($sp)
la $v0, st88
sw $v0,84($sp)
lw $t0,76($sp)
lw $t1,84($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,92($sp)
lw $t0,92($sp)
bgtz $t0, Lbl108
li $t0,1
move $v0, $t0
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
b Lbl109
Lbl108:
move $t0, $zero
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,104($sp)
Lbl109:
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
addi $sp, $sp, 120
jr $ra
f41: #CellularAutomaton.prompt2
addi $sp, $sp, -120
la $v0, st89
sw $v0,12($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
la $v0, st90
sw $v0,28($sp)
lw $t0,20($sp)
#Argument var.var766
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,32($sp)
#Argument var.var767
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var768<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,32($sp)
move $t0,$a0
move $v0, $t0
sw $v0,36($sp)
la $v0, st91
sw $v0,44($sp)
lw $t0,36($sp)
#Argument var.var769
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
#Argument var.var770
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var771<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,48($sp)
move $t0,$a0
move $v0, $t0
sw $v0,52($sp)
la $v0, st92
sw $v0,60($sp)
lw $t0,52($sp)
#Argument var.var772
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,64($sp)
#Argument var.var773
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var774<-['CellularAutomaton', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,64($sp)
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
#Argument var.var775
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var776<-['CellularAutomaton', 'in_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,76($sp)
la $v0, st93
sw $v0,84($sp)
lw $t0,76($sp)
lw $t1,84($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,92($sp)
lw $t0,92($sp)
bgtz $t0, Lbl110
move $t0, $zero
move $v0, $t0
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
b Lbl111
Lbl110:
li $t0,1
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,104($sp)
Lbl111:
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
addi $sp, $sp, 120
jr $ra
f42: #Main.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,CellularAutomatonclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var789<-['CellularAutomaton', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,20($a0)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f43: #Main.type_name
addi $sp, $sp, -12
la $v0, st94
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f44: #Main.main
addi $sp, $sp, -200
move $t0, $zero
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
la $v0, st95
sw $v0,24($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
la $v0, st96
sw $v0,40($sp)
lw $t0,32($sp)
#Argument var.var796
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
#Argument var.var797
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var798<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
la $v0, st97
sw $v0,56($sp)
lw $t0,48($sp)
#Argument var.var799
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
#Argument var.var800
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var801<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,60($sp)
Lbl112:
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
#Argument var.var802
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,112($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var803<-['Main', 'prompt2']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,68($sp)
lw $t0,68($sp)
seq $v0, $t0, $zero
sw $v0,76($sp)
lw $t0,76($sp)
bgtz $t0, Lbl113
li $t0,1
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
#Argument var.var806
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,104($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var807<-['Main', 'option']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,20
li $v0, 9
syscall
la $t0, CellularAutomatonclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
#Argument var.var808
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var808<-['CellularAutomaton', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,100($sp)
lw $t0,96($sp)
#Argument var.var808
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,104($sp)
#Argument var.var809
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var810<-['CellularAutomaton', 'init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,20($a0)
lw $t0,20($a0)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
#Argument var.var811
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var812<-['CellularAutomaton', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,112($sp)
Lbl114:
lw $t0,4($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
seq $v0, $t0, $zero
sw $v0,124($sp)
lw $t0,124($sp)
bgtz $t0, Lbl115
move $t0,$a0
move $v0, $t0
sw $v0,128($sp)
lw $t0,128($sp)
#Argument var.var815
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,108($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var816<-['Main', 'prompt']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,132($sp)
lw $t0,132($sp)
bgtz $t0, Lbl116
move $t0, $zero
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,156($sp)
b Lbl117
Lbl116:
lw $t0,20($a0)
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
#Argument var.var817
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,100($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var818<-['CellularAutomaton', 'evolve']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,140($sp)
lw $t0,20($a0)
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
#Argument var.var819
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var820<-['CellularAutomaton', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,148($sp)
lw $t0,148($sp)
move $v0, $t0
sw $v0,156($sp)
Lbl117:
lw $t0,156($sp)
move $v0, $t0
sw $v0,160($sp)
b Lbl114
Lbl115:
li $t0,0
move $v0, $t0
sw $v0,168($sp)
b Lbl112
Lbl113:
li $t0,0
move $v0, $t0
sw $v0,176($sp)
move $t0,$a0
move $v0, $t0
sw $v0,180($sp)
lw $t0,180($sp)
move $v0, $t0
sw $v0,184($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,184($sp)
move $v0, $t0
sw $v0,188($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,196($sp)
addi $sp, $sp, 200
jr $ra
