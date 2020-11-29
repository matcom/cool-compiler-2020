.data
st0: .asciiz "Object"
st1: .asciiz "A"
st2: .asciiz "A2I"
st3: .asciiz "0"
st4: .asciiz "1"
st5: .asciiz "2"
st6: .asciiz "3"
st7: .asciiz "4"
st8: .asciiz "5"
st9: .asciiz "6"
st10: .asciiz "7"
st11: .asciiz "8"
st12: .asciiz "9"
st13: .asciiz "0"
st14: .asciiz "1"
st15: .asciiz "2"
st16: .asciiz "3"
st17: .asciiz "4"
st18: .asciiz "5"
st19: .asciiz "6"
st20: .asciiz "7"
st21: .asciiz "8"
st22: .asciiz "9"
st23: .asciiz ""
st24: .asciiz "-"
st25: .asciiz "+"
st26: .asciiz "0"
st27: .asciiz "-"
st28: .asciiz ""
st29: .asciiz "IO"
st30: .asciiz "String"
st31: .asciiz "Bool"
st32: .asciiz "B"
st33: .asciiz "C"
st34: .asciiz "D"
st35: .asciiz "E"
st36: .asciiz ""
st37: .asciiz "Main"
st38: .asciiz "\n\tTo add a number to "
st39: .asciiz "...enter a:\n"
st40: .asciiz "\tTo negate "
st41: .asciiz "...enter b:\n"
st42: .asciiz "\tTo find the difference between "
st43: .asciiz "and another number...enter c:\n"
st44: .asciiz "\tTo find the factorial of "
st45: .asciiz "...enter d:\n"
st46: .asciiz "\tTo square "
st47: .asciiz "...enter e:\n"
st48: .asciiz "\tTo cube "
st49: .asciiz "...enter f:\n"
st50: .asciiz "\tTo find out if "
st51: .asciiz "is a multiple of 3...enter g:\n"
st52: .asciiz "\tTo divide "
st53: .asciiz "by 8...enter h:\n"
st54: .asciiz "\tTo get a new number...enter j:\n"
st55: .asciiz "\tTo quit...enter q:\n\n"
st56: .asciiz "\n"
st57: .asciiz "Please enter a number...  "
st58: .asciiz "Class type is now E\n"
st59: .asciiz "Class type is now D\n"
st60: .asciiz "Class type is now C\n"
st61: .asciiz "Class type is now B\n"
st62: .asciiz "Class type is now A\n"
st63: .asciiz "Oooops\n"
st64: .asciiz " "
st65: .asciiz "number "
st66: .asciiz "is even!\n"
st67: .asciiz "is odd!\n"
st68: .asciiz "a"
st69: .asciiz "b"
st70: .asciiz "Oooops\n"
st71: .asciiz "c"
st72: .asciiz "d"
st73: .asciiz "e"
st74: .asciiz "f"
st75: .asciiz "g"
st76: .asciiz "number "
st77: .asciiz "is divisible by 3.\n"
st78: .asciiz "number "
st79: .asciiz "is not divisible by 3.\n"
st80: .asciiz "h"
st81: .asciiz "number "
st82: .asciiz "is equal to "
st83: .asciiz "times 8 with a remainder of "
st84: .asciiz "\n"
st85: .asciiz "j"
st86: .asciiz "q"
Objectclase: .word 0,f0,f3,f2,f4
Aclase: .word Objectclase,f5,f6,f2,f4,f7,f8,f9,f10,f11,f12,f13
A2Iclase: .word Objectclase,f14,f15,f2,f4,f16,f17,f18,f19,f20,f21
IOclase: .word Objectclase,f22,f23,f2,f4,f24,f25,f26,f27
Stringclase: .word Objectclase,f28,f29,f2,f4,f30,f31,f32
Boolclase: .word Objectclase,f33,f34,f2,f4
Bclase: .word Aclase,f35,f36,f2,f4,f7,f8,f9,f10,f11,f12,f37
Cclase: .word Bclase,f38,f39,f2,f4,f7,f8,f9,f10,f11,f12,f41,f40
Dclase: .word Bclase,f42,f43,f2,f4,f7,f8,f9,f10,f11,f12,f37,f44
Eclase: .word Dclase,f45,f46,f2,f4,f7,f8,f9,f10,f11,f12,f37,f44,f47
Mainclase: .word IOclase,f48,f49,f2,f4,f24,f25,f26,f27,f50,f51,f52,f53,f54,f55,f56
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
     #lw $t0, 0($t0)
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
li $a0,20
li $v0, 9
syscall
la $t0, Mainclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var498
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var498<-['Main', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var498
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var499<-['Main', 'main']
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
f5: #A.$init
addi $sp, $sp, -16
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
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f6: #A.type_name
addi $sp, $sp, -12
la $v0, st1
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f7: #A.value
addi $sp, $sp, -8
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f8: #A.set_var
addi $sp, $sp, -16
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f9: #A.method1
addi $sp, $sp, -8
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f10: #A.method2
addi $sp, $sp, -52
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
move $t0,$a2
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
add $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Bclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $t0,32($sp)
#Argument var.var21
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var21<-['B', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
#Argument var.var21
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
#Argument var.var22
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var23<-['B', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
addi $sp, $sp, 52
jr $ra
f11: #A.method3
addi $sp, $sp, -48
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
neg $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $t0,28($sp)
#Argument var.var30
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var30<-['C', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
#Argument var.var30
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
#Argument var.var31
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var32<-['C', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
addi $sp, $sp, 48
jr $ra
f12: #A.method4
addi $sp, $sp, -120
move $t0,$a2
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
slt $v0, $t0, $t1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl0
li $t0,0
move $v0, $t0
sw $v0,68($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,20($sp)
move $t0,$a2
move $v0, $t0
sw $v0,76($sp)
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
lw $t1,80($sp)
sub $v0, $t0, $t1
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $t0,92($sp)
#Argument var.var56
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var56<-['D', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,96($sp)
lw $t0,92($sp)
#Argument var.var56
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,100($sp)
#Argument var.var57
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var58<-['D', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,20($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
b Lbl1
Lbl0:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,20($sp)
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
move $t0,$a2
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
lw $t1,36($sp)
sub $v0, $t0, $t1
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,48($sp)
lw $t0,48($sp)
#Argument var.var45
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var45<-['D', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,48($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,48($sp)
#Argument var.var45
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
#Argument var.var46
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var47<-['D', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,20($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,112($sp)
Lbl1:
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
addi $sp, $sp, 120
jr $ra
f13: #A.method5
addi $sp, $sp, -120
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
li $t0,1
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,16($sp)
Lbl2:
lw $t0,16($sp)
move $v0, $t0
sw $v0,28($sp)
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
sle $v0, $t0, $t1
sw $v0,40($sp)
lw $t0,40($sp)
seq $v0, $t0, $zero
sw $v0,48($sp)
lw $t0,48($sp)
bgtz $t0, Lbl3
lw $t0,4($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
mult $t0, $t1
mflo $v0
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,68($sp)
li $t0,1
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
lw $t1,72($sp)
add $v0, $t0, $t1
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,16($sp)
b Lbl2
Lbl3:
li $t0,0
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,92($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,92($sp)
move $v0, $t0
sw $v0,96($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,100($sp)
lw $t0,100($sp)
#Argument var.var83
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var83<-['E', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,100($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,100($sp)
#Argument var.var83
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
#Argument var.var84
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var85<-['E', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
addi $sp, $sp, 120
jr $ra
f14: #A2I.$init
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
jal $t0 #var.var90<-['Object', '$init']
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
f15: #A2I.type_name
addi $sp, $sp, -12
la $v0, st2
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f16: #A2I.c2i
addi $sp, $sp, -336
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
la $v0, st3
sw $v0,12($sp)
lw $t0,4($sp)
lw $t1,12($sp)
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
sw $v0,20($sp)
lw $t0,20($sp)
bgtz $t0, Lbl22
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
la $v0, st4
sw $v0,36($sp)
lw $t0,28($sp)
lw $t1,36($sp)
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
sw $v0,44($sp)
lw $t0,44($sp)
bgtz $t0, Lbl20
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
la $v0, st5
sw $v0,60($sp)
lw $t0,52($sp)
lw $t1,60($sp)
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
sw $v0,68($sp)
lw $t0,68($sp)
bgtz $t0, Lbl18
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
la $v0, st6
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
bgtz $t0, Lbl16
move $t0,$a1
move $v0, $t0
sw $v0,100($sp)
la $v0, st7
sw $v0,108($sp)
lw $t0,100($sp)
lw $t1,108($sp)
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
sw $v0,116($sp)
lw $t0,116($sp)
bgtz $t0, Lbl14
move $t0,$a1
move $v0, $t0
sw $v0,124($sp)
la $v0, st8
sw $v0,132($sp)
lw $t0,124($sp)
lw $t1,132($sp)
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
sw $v0,140($sp)
lw $t0,140($sp)
bgtz $t0, Lbl12
move $t0,$a1
move $v0, $t0
sw $v0,148($sp)
la $v0, st9
sw $v0,156($sp)
lw $t0,148($sp)
lw $t1,156($sp)
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
sw $v0,164($sp)
lw $t0,164($sp)
bgtz $t0, Lbl10
move $t0,$a1
move $v0, $t0
sw $v0,172($sp)
la $v0, st10
sw $v0,180($sp)
lw $t0,172($sp)
lw $t1,180($sp)
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
sw $v0,188($sp)
lw $t0,188($sp)
bgtz $t0, Lbl8
move $t0,$a1
move $v0, $t0
sw $v0,196($sp)
la $v0, st11
sw $v0,204($sp)
lw $t0,196($sp)
lw $t1,204($sp)
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
sw $v0,212($sp)
lw $t0,212($sp)
bgtz $t0, Lbl6
move $t0,$a1
move $v0, $t0
sw $v0,220($sp)
la $v0, st12
sw $v0,228($sp)
lw $t0,220($sp)
lw $t1,228($sp)
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
sw $v0,236($sp)
lw $t0,236($sp)
bgtz $t0, Lbl4
move $t0,$a0
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
#Argument var.var143
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var144<-['A2I', 'abort']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,248($sp)
li $t0,0
move $v0, $t0
sw $v0,252($sp)
lw $t0,252($sp)
move $v0, $t0
sw $v0,256($sp)
b Lbl5
Lbl4:
li $t0,9
move $v0, $t0
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,256($sp)
Lbl5:
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
lw $t0,260($sp)
move $v0, $t0
sw $v0,264($sp)
b Lbl7
Lbl6:
li $t0,8
move $v0, $t0
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,264($sp)
Lbl7:
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
b Lbl9
Lbl8:
li $t0,7
move $v0, $t0
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,272($sp)
Lbl9:
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,280($sp)
b Lbl11
Lbl10:
li $t0,6
move $v0, $t0
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,280($sp)
Lbl11:
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
b Lbl13
Lbl12:
li $t0,5
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,288($sp)
Lbl13:
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
b Lbl15
Lbl14:
li $t0,4
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,296($sp)
Lbl15:
lw $t0,296($sp)
move $v0, $t0
sw $v0,300($sp)
lw $t0,300($sp)
move $v0, $t0
sw $v0,304($sp)
b Lbl17
Lbl16:
li $t0,3
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,304($sp)
Lbl17:
lw $t0,304($sp)
move $v0, $t0
sw $v0,308($sp)
lw $t0,308($sp)
move $v0, $t0
sw $v0,312($sp)
b Lbl19
Lbl18:
li $t0,2
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,312($sp)
Lbl19:
lw $t0,312($sp)
move $v0, $t0
sw $v0,316($sp)
lw $t0,316($sp)
move $v0, $t0
sw $v0,320($sp)
b Lbl21
Lbl20:
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,320($sp)
Lbl21:
lw $t0,320($sp)
move $v0, $t0
sw $v0,324($sp)
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
b Lbl23
Lbl22:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,328($sp)
Lbl23:
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
addi $sp, $sp, 336
jr $ra
f17: #A2I.i2c
addi $sp, $sp, -340
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
bgtz $t0, Lbl42
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
li $t0,1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
seq $v0 ,$t0, $t1
sw $v0,40($sp)
lw $t0,40($sp)
bgtz $t0, Lbl40
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
li $t0,2
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
seq $v0 ,$t0, $t1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl38
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
li $t0,3
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
lw $t1,80($sp)
seq $v0 ,$t0, $t1
sw $v0,88($sp)
lw $t0,88($sp)
bgtz $t0, Lbl36
move $t0,$a1
move $v0, $t0
sw $v0,100($sp)
li $t0,4
move $v0, $t0
sw $v0,104($sp)
lw $t0,100($sp)
lw $t1,104($sp)
seq $v0 ,$t0, $t1
sw $v0,112($sp)
lw $t0,112($sp)
bgtz $t0, Lbl34
move $t0,$a1
move $v0, $t0
sw $v0,124($sp)
li $t0,5
move $v0, $t0
sw $v0,128($sp)
lw $t0,124($sp)
lw $t1,128($sp)
seq $v0 ,$t0, $t1
sw $v0,136($sp)
lw $t0,136($sp)
bgtz $t0, Lbl32
move $t0,$a1
move $v0, $t0
sw $v0,148($sp)
li $t0,6
move $v0, $t0
sw $v0,152($sp)
lw $t0,148($sp)
lw $t1,152($sp)
seq $v0 ,$t0, $t1
sw $v0,160($sp)
lw $t0,160($sp)
bgtz $t0, Lbl30
move $t0,$a1
move $v0, $t0
sw $v0,172($sp)
li $t0,7
move $v0, $t0
sw $v0,176($sp)
lw $t0,172($sp)
lw $t1,176($sp)
seq $v0 ,$t0, $t1
sw $v0,184($sp)
lw $t0,184($sp)
bgtz $t0, Lbl28
move $t0,$a1
move $v0, $t0
sw $v0,196($sp)
li $t0,8
move $v0, $t0
sw $v0,200($sp)
lw $t0,196($sp)
lw $t1,200($sp)
seq $v0 ,$t0, $t1
sw $v0,208($sp)
lw $t0,208($sp)
bgtz $t0, Lbl26
move $t0,$a1
move $v0, $t0
sw $v0,220($sp)
li $t0,9
move $v0, $t0
sw $v0,224($sp)
lw $t0,220($sp)
lw $t1,224($sp)
seq $v0 ,$t0, $t1
sw $v0,232($sp)
lw $t0,232($sp)
bgtz $t0, Lbl24
move $t0,$a0
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
#Argument var.var216
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var217<-['A2I', 'abort']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,248($sp)
la $v0, st23
sw $v0,256($sp)
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
b Lbl25
Lbl24:
la $v0, st22
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,260($sp)
Lbl25:
lw $t0,260($sp)
move $v0, $t0
sw $v0,264($sp)
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
b Lbl27
Lbl26:
la $v0, st21
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,268($sp)
Lbl27:
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
b Lbl29
Lbl28:
la $v0, st20
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,276($sp)
Lbl29:
lw $t0,276($sp)
move $v0, $t0
sw $v0,280($sp)
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
b Lbl31
Lbl30:
la $v0, st19
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,284($sp)
Lbl31:
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
b Lbl33
Lbl32:
la $v0, st18
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,292($sp)
Lbl33:
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,296($sp)
move $v0, $t0
sw $v0,300($sp)
b Lbl35
Lbl34:
la $v0, st17
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,300($sp)
Lbl35:
lw $t0,300($sp)
move $v0, $t0
sw $v0,304($sp)
lw $t0,304($sp)
move $v0, $t0
sw $v0,308($sp)
b Lbl37
Lbl36:
la $v0, st16
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,308($sp)
Lbl37:
lw $t0,308($sp)
move $v0, $t0
sw $v0,312($sp)
lw $t0,312($sp)
move $v0, $t0
sw $v0,316($sp)
b Lbl39
Lbl38:
la $v0, st15
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,316($sp)
Lbl39:
lw $t0,316($sp)
move $v0, $t0
sw $v0,320($sp)
lw $t0,320($sp)
move $v0, $t0
sw $v0,324($sp)
b Lbl41
Lbl40:
la $v0, st14
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,324($sp)
Lbl41:
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
b Lbl43
Lbl42:
la $v0, st13
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,332($sp)
Lbl43:
lw $t0,332($sp)
move $v0, $t0
sw $v0,336($sp)
addi $sp, $sp, 340
jr $ra
f18: #A2I.a2i
addi $sp, $sp, -216
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var239
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var240<-['String', 'length']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
li $t0,0
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
seq $v0 ,$t0, $t1
sw $v0,20($sp)
lw $t0,20($sp)
bgtz $t0, Lbl48
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
li $t0,0
move $v0, $t0
sw $v0,32($sp)
li $t0,1
move $v0, $t0
sw $v0,36($sp)
lw $t0,28($sp)
#Argument var.var245
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
#Argument var.var246
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,44($sp)
#Argument var.var247
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var248<-['String', 'substr']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,40($sp)
la $v0, st24
sw $v0,48($sp)
lw $t0,40($sp)
lw $t1,48($sp)
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
sw $v0,56($sp)
lw $t0,56($sp)
bgtz $t0, Lbl46
move $t0,$a1
move $v0, $t0
sw $v0,108($sp)
li $t0,0
move $v0, $t0
sw $v0,112($sp)
li $t0,1
move $v0, $t0
sw $v0,116($sp)
lw $t0,108($sp)
#Argument var.var263
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,116($sp)
#Argument var.var264
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,124($sp)
#Argument var.var265
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var266<-['String', 'substr']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,120($sp)
la $v0, st25
sw $v0,128($sp)
lw $t0,120($sp)
lw $t1,128($sp)
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
sw $v0,136($sp)
lw $t0,136($sp)
bgtz $t0, Lbl44
move $t0,$a0
move $v0, $t0
sw $v0,180($sp)
move $t0,$a1
move $v0, $t0
sw $v0,184($sp)
lw $t0,180($sp)
#Argument var.var280
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,188($sp)
#Argument var.var281
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var282<-['A2I', 'a2i_aux']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,188($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
b Lbl45
Lbl44:
move $t0,$a0
move $v0, $t0
sw $v0,140($sp)
move $t0,$a1
move $v0, $t0
sw $v0,144($sp)
li $t0,1
move $v0, $t0
sw $v0,148($sp)
move $t0,$a1
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
#Argument var.var273
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var274<-['String', 'length']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,156($sp)
li $t0,1
move $v0, $t0
sw $v0,160($sp)
lw $t0,156($sp)
lw $t1,160($sp)
sub $v0, $t0, $t1
sw $v0,168($sp)
lw $t0,144($sp)
#Argument var.var271
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,152($sp)
#Argument var.var272
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,176($sp)
#Argument var.var276
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var278<-['String', 'substr']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,172($sp)
lw $t0,140($sp)
#Argument var.var270
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,176($sp)
#Argument var.var278
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var279<-['A2I', 'a2i_aux']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,176($sp)
lw $t0,176($sp)
move $v0, $t0
sw $v0,192($sp)
Lbl45:
lw $t0,192($sp)
move $v0, $t0
sw $v0,196($sp)
lw $t0,196($sp)
move $v0, $t0
sw $v0,200($sp)
b Lbl47
Lbl46:
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
move $t0,$a1
move $v0, $t0
sw $v0,64($sp)
li $t0,1
move $v0, $t0
sw $v0,68($sp)
move $t0,$a1
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
#Argument var.var255
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var256<-['String', 'length']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
li $t0,1
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
lw $t1,80($sp)
sub $v0, $t0, $t1
sw $v0,88($sp)
lw $t0,64($sp)
#Argument var.var253
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
#Argument var.var254
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,96($sp)
#Argument var.var258
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var260<-['String', 'substr']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,92($sp)
lw $t0,60($sp)
#Argument var.var252
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var260
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var261<-['A2I', 'a2i_aux']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
neg $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,200($sp)
Lbl47:
lw $t0,200($sp)
move $v0, $t0
sw $v0,204($sp)
lw $t0,204($sp)
move $v0, $t0
sw $v0,208($sp)
b Lbl49
Lbl48:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,208($sp)
Lbl49:
lw $t0,208($sp)
move $v0, $t0
sw $v0,212($sp)
addi $sp, $sp, 216
jr $ra
f19: #A2I.a2i_aux
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
move $t0,$a1
move $v0, $t0
sw $v0,20($sp)
lw $t0,20($sp)
#Argument var.var291
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var292<-['String', 'length']
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
li $t0,0
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,32($sp)
Lbl50:
lw $t0,32($sp)
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
bgtz $t0, Lbl51
lw $t0,4($sp)
move $v0, $t0
sw $v0,68($sp)
li $t0,10
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
lw $t1,72($sp)
mult $t0, $t1
mflo $v0
sw $v0,80($sp)
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
move $t0,$a1
move $v0, $t0
sw $v0,88($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,92($sp)
li $t0,1
move $v0, $t0
sw $v0,96($sp)
lw $t0,88($sp)
#Argument var.var306
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var307
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,104($sp)
#Argument var.var308
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var309<-['String', 'substr']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,100($sp)
lw $t0,84($sp)
#Argument var.var305
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,104($sp)
#Argument var.var309
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var310<-['A2I', 'c2i']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,104($sp)
lw $t0,80($sp)
lw $t1,104($sp)
add $v0, $t0, $t1
sw $v0,112($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,116($sp)
li $t0,1
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
add $v0, $t0, $t1
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,32($sp)
b Lbl50
Lbl51:
li $t0,0
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,148($sp)
move $v0, $t0
sw $v0,152($sp)
lw $t0,4($sp)
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
f20: #A2I.i2a
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
bgtz $t0, Lbl54
li $t0,0
move $v0, $t0
sw $v0,28($sp)
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
slt $v0, $t0, $t1
sw $v0,40($sp)
lw $t0,40($sp)
bgtz $t0, Lbl52
la $v0, st27
sw $v0,60($sp)
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
li $t0,1
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
neg $v0, $t0
sw $v0,80($sp)
lw $t0,68($sp)
lw $t1,80($sp)
mult $t0, $t1
mflo $v0
sw $v0,88($sp)
lw $t0,64($sp)
#Argument var.var338
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,92($sp)
#Argument var.var342
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var344<-['A2I', 'i2a_aux']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,92($sp)
lw $t0,60($sp)
#Argument var.var337
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var344
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
la $t0,Stringclase
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var345<-['String', 'concat']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl53
Lbl52:
move $t0,$a0
move $v0, $t0
sw $v0,44($sp)
move $t0,$a1
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
#Argument var.var334
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
#Argument var.var335
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var336<-['A2I', 'i2a_aux']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl53:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
b Lbl55
Lbl54:
la $v0, st26
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,108($sp)
Lbl55:
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
addi $sp, $sp, 116
jr $ra
f21: #A2I.i2a_aux
addi $sp, $sp, -120
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
bgtz $t0, Lbl56
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
li $t0,10
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
lw $t1,36($sp)
div $t0, $t1
mflo $v0
sw $v0,44($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,28($sp)
move $t0,$a0
move $v0, $t0
sw $v0,52($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
#Argument var.var360
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
#Argument var.var361
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var362<-['A2I', 'i2a_aux']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,60($sp)
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,72($sp)
li $t0,10
move $v0, $t0
sw $v0,76($sp)
lw $t0,72($sp)
lw $t1,76($sp)
mult $t0, $t1
mflo $v0
sw $v0,84($sp)
lw $t0,68($sp)
lw $t1,84($sp)
sub $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,64($sp)
#Argument var.var363
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var369
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var371<-['A2I', 'i2c']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,60($sp)
#Argument var.var362
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,100($sp)
#Argument var.var371
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
la $t0,Stringclase
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var372<-['String', 'concat']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
b Lbl57
Lbl56:
la $v0, st28
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,112($sp)
Lbl57:
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
addi $sp, $sp, 120
jr $ra
f22: #IO.$init
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
jal $t0 #var.var379<-['Object', '$init']
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
f23: #IO.type_name
addi $sp, $sp, -12
la $v0, st29
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f24: #IO.out_string
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
f25: #IO.out_int
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
f26: #IO.in_string
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
f27: #IO.in_int
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
f28: #String.$init
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
jal $t0 #var.var384<-['Object', '$init']
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
f29: #String.type_name
addi $sp, $sp, -12
la $v0, st30
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f30: #String.Length
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
f31: #String.Concat
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
f32: #String.Substring
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
f33: #Bool.$init
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
jal $t0 #var.var389<-['Object', '$init']
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
f34: #Bool.type_name
addi $sp, $sp, -12
la $v0, st31
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f35: #B.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Aclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var394<-['A', '$init']
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
f36: #B.type_name
addi $sp, $sp, -12
la $v0, st32
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f37: #B.method5
addi $sp, $sp, -52
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
move $t0,$a1
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
mult $t0, $t1
mflo $v0
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $t0,32($sp)
#Argument var.var403
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var403<-['E', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
#Argument var.var403
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
#Argument var.var404
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var405<-['E', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
addi $sp, $sp, 52
jr $ra
f38: #C.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var410<-['B', '$init']
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
f39: #C.type_name
addi $sp, $sp, -12
la $v0, st33
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f40: #C.method6
addi $sp, $sp, -48
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
neg $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $t0,28($sp)
#Argument var.var417
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var417<-['A', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
#Argument var.var417
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
#Argument var.var418
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var419<-['A', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
addi $sp, $sp, 48
jr $ra
f41: #C.method5
addi $sp, $sp, -64
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
move $t0,$a1
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
mult $t0, $t1
mflo $v0
sw $v0,28($sp)
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
mult $t0, $t1
mflo $v0
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $t0,44($sp)
#Argument var.var431
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var431<-['E', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
#Argument var.var431
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
#Argument var.var432
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var433<-['E', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
addi $sp, $sp, 64
jr $ra
f42: #D.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var438<-['B', '$init']
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
f43: #D.type_name
addi $sp, $sp, -12
la $v0, st34
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f44: #D.method7
addi $sp, $sp, -176
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl64
li $t0,0
move $v0, $t0
sw $v0,52($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
seq $v0 ,$t0, $t1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl62
li $t0,1
move $v0, $t0
sw $v0,72($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,76($sp)
lw $t0,72($sp)
lw $t1,76($sp)
seq $v0 ,$t0, $t1
sw $v0,84($sp)
lw $t0,84($sp)
bgtz $t0, Lbl60
li $t0,2
move $v0, $t0
sw $v0,92($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,96($sp)
lw $t0,92($sp)
lw $t1,96($sp)
seq $v0 ,$t0, $t1
sw $v0,104($sp)
lw $t0,104($sp)
bgtz $t0, Lbl58
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,116($sp)
li $t0,3
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
sub $v0, $t0, $t1
sw $v0,128($sp)
lw $t0,112($sp)
#Argument var.var466
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,132($sp)
#Argument var.var469
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var471<-['D', 'method7']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl59
Lbl58:
move $t0, $zero
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl59:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
b Lbl61
Lbl60:
move $t0, $zero
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,144($sp)
Lbl61:
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
lw $t0,148($sp)
move $v0, $t0
sw $v0,152($sp)
b Lbl63
Lbl62:
li $t0,1
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,152($sp)
Lbl63:
lw $t0,152($sp)
move $v0, $t0
sw $v0,156($sp)
lw $t0,156($sp)
move $v0, $t0
sw $v0,160($sp)
b Lbl65
Lbl64:
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
neg $v0, $t0
sw $v0,44($sp)
lw $t0,32($sp)
#Argument var.var447
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
#Argument var.var449
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var450<-['D', 'method7']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,160($sp)
Lbl65:
lw $t0,160($sp)
move $v0, $t0
sw $v0,164($sp)
lw $t0,164($sp)
move $v0, $t0
sw $v0,168($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,172($sp)
addi $sp, $sp, 176
jr $ra
f45: #E.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Dclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var484<-['D', '$init']
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
f46: #E.type_name
addi $sp, $sp, -12
la $v0, st35
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f47: #E.method6
addi $sp, $sp, -52
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
li $t0,8
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
div $t0, $t1
mflo $v0
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $t0,32($sp)
#Argument var.var493
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var493<-['A', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
#Argument var.var493
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
#Argument var.var494
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var495<-['A', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
addi $sp, $sp, 52
jr $ra
f48: #Main.$init
addi $sp, $sp, -24
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var500<-['IO', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
la $v0, st36
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($a0)
li $t0,0
move $v0, $t0
sw $v0,8($a0)
li $t0,0
move $v0, $t0
sw $v0,12($a0)
li $t0,1
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,16($a0)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f49: #Main.type_name
addi $sp, $sp, -12
la $v0, st37
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f50: #Main.menu
addi $sp, $sp, -396
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
la $v0, st38
sw $v0,12($sp)
lw $t0,4($sp)
#Argument var.var505
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
#Argument var.var506
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var507<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
#Argument var.var508
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
#Argument var.var509
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var510<-['Main', 'print']
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
#Argument var.var511
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
#Argument var.var512
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var513<-['Main', 'out_string']
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
#Argument var.var514
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
#Argument var.var515
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var516<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,60($sp)
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
#Argument var.var517
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
#Argument var.var518
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var519<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,72($sp)
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
la $v0, st41
sw $v0,84($sp)
lw $t0,76($sp)
#Argument var.var520
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,88($sp)
#Argument var.var521
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var522<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,88($sp)
move $t0,$a0
move $v0, $t0
sw $v0,92($sp)
la $v0, st42
sw $v0,100($sp)
lw $t0,92($sp)
#Argument var.var523
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,104($sp)
#Argument var.var524
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var525<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,104($sp)
move $t0,$a0
move $v0, $t0
sw $v0,108($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,112($sp)
lw $t0,108($sp)
#Argument var.var526
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,116($sp)
#Argument var.var527
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var528<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,116($sp)
move $t0,$a0
move $v0, $t0
sw $v0,120($sp)
la $v0, st43
sw $v0,128($sp)
lw $t0,120($sp)
#Argument var.var529
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,132($sp)
#Argument var.var530
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var531<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,132($sp)
move $t0,$a0
move $v0, $t0
sw $v0,136($sp)
la $v0, st44
sw $v0,144($sp)
lw $t0,136($sp)
#Argument var.var532
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,148($sp)
#Argument var.var533
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var534<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,148($sp)
move $t0,$a0
move $v0, $t0
sw $v0,152($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,156($sp)
lw $t0,152($sp)
#Argument var.var535
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,160($sp)
#Argument var.var536
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var537<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,160($sp)
move $t0,$a0
move $v0, $t0
sw $v0,164($sp)
la $v0, st45
sw $v0,172($sp)
lw $t0,164($sp)
#Argument var.var538
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,176($sp)
#Argument var.var539
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var540<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,176($sp)
move $t0,$a0
move $v0, $t0
sw $v0,180($sp)
la $v0, st46
sw $v0,188($sp)
lw $t0,180($sp)
#Argument var.var541
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,192($sp)
#Argument var.var542
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var543<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,192($sp)
move $t0,$a0
move $v0, $t0
sw $v0,196($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,200($sp)
lw $t0,196($sp)
#Argument var.var544
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,204($sp)
#Argument var.var545
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var546<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,204($sp)
move $t0,$a0
move $v0, $t0
sw $v0,208($sp)
la $v0, st47
sw $v0,216($sp)
lw $t0,208($sp)
#Argument var.var547
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,220($sp)
#Argument var.var548
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var549<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,220($sp)
move $t0,$a0
move $v0, $t0
sw $v0,224($sp)
la $v0, st48
sw $v0,232($sp)
lw $t0,224($sp)
#Argument var.var550
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,236($sp)
#Argument var.var551
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var552<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,236($sp)
move $t0,$a0
move $v0, $t0
sw $v0,240($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,244($sp)
lw $t0,240($sp)
#Argument var.var553
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,248($sp)
#Argument var.var554
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var555<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,248($sp)
move $t0,$a0
move $v0, $t0
sw $v0,252($sp)
la $v0, st49
sw $v0,260($sp)
lw $t0,252($sp)
#Argument var.var556
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,264($sp)
#Argument var.var557
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var558<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,264($sp)
move $t0,$a0
move $v0, $t0
sw $v0,268($sp)
la $v0, st50
sw $v0,276($sp)
lw $t0,268($sp)
#Argument var.var559
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,280($sp)
#Argument var.var560
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var561<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,280($sp)
move $t0,$a0
move $v0, $t0
sw $v0,284($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,288($sp)
lw $t0,284($sp)
#Argument var.var562
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,292($sp)
#Argument var.var563
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var564<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,292($sp)
move $t0,$a0
move $v0, $t0
sw $v0,296($sp)
la $v0, st51
sw $v0,304($sp)
lw $t0,296($sp)
#Argument var.var565
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,308($sp)
#Argument var.var566
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var567<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,308($sp)
move $t0,$a0
move $v0, $t0
sw $v0,312($sp)
la $v0, st52
sw $v0,320($sp)
lw $t0,312($sp)
#Argument var.var568
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,324($sp)
#Argument var.var569
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var570<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,324($sp)
move $t0,$a0
move $v0, $t0
sw $v0,328($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,332($sp)
lw $t0,328($sp)
#Argument var.var571
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,336($sp)
#Argument var.var572
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var573<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,336($sp)
move $t0,$a0
move $v0, $t0
sw $v0,340($sp)
la $v0, st53
sw $v0,348($sp)
lw $t0,340($sp)
#Argument var.var574
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,352($sp)
#Argument var.var575
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var576<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,352($sp)
move $t0,$a0
move $v0, $t0
sw $v0,356($sp)
la $v0, st54
sw $v0,364($sp)
lw $t0,356($sp)
#Argument var.var577
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,368($sp)
#Argument var.var578
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var579<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,368($sp)
move $t0,$a0
move $v0, $t0
sw $v0,372($sp)
la $v0, st55
sw $v0,380($sp)
lw $t0,372($sp)
#Argument var.var580
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,384($sp)
#Argument var.var581
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var582<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,384($sp)
move $t0,$a0
move $v0, $t0
sw $v0,388($sp)
lw $t0,388($sp)
#Argument var.var583
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var584<-['Main', 'in_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,392($sp)
addi $sp, $sp, 396
jr $ra
f51: #Main.prompt
addi $sp, $sp, -44
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
la $v0, st56
sw $v0,12($sp)
lw $t0,4($sp)
#Argument var.var585
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
#Argument var.var586
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var587<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
la $v0, st57
sw $v0,28($sp)
lw $t0,20($sp)
#Argument var.var588
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,32($sp)
#Argument var.var589
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var590<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,32($sp)
move $t0,$a0
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
#Argument var.var591
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var592<-['Main', 'in_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,40($sp)
addi $sp, $sp, 44
jr $ra
f52: #Main.get_int
addi $sp, $sp, -60
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
li $v0, 9
syscall
la $t0, A2Iclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
#Argument var.var593
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var593<-['A2I', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
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
#Argument var.var595
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var596<-['Main', 'prompt']
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
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
#Argument var.var598
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
#Argument var.var599
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var600<-['A2I', 'a2i']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,56($sp)
addi $sp, $sp, 60
jr $ra
f53: #Main.is_even
addi $sp, $sp, -148
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl70
li $t0,0
move $v0, $t0
sw $v0,52($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
seq $v0 ,$t0, $t1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl68
li $t0,1
move $v0, $t0
sw $v0,72($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,76($sp)
lw $t0,72($sp)
lw $t1,76($sp)
seq $v0 ,$t0, $t1
sw $v0,84($sp)
lw $t0,84($sp)
bgtz $t0, Lbl66
move $t0,$a0
move $v0, $t0
sw $v0,92($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,96($sp)
li $t0,2
move $v0, $t0
sw $v0,100($sp)
lw $t0,96($sp)
lw $t1,100($sp)
sub $v0, $t0, $t1
sw $v0,108($sp)
lw $t0,92($sp)
#Argument var.var625
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
#Argument var.var628
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var630<-['Main', 'is_even']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,112($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
b Lbl67
Lbl66:
move $t0, $zero
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,116($sp)
Lbl67:
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
b Lbl69
Lbl68:
li $t0,1
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,124($sp)
Lbl69:
lw $t0,124($sp)
move $v0, $t0
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,132($sp)
b Lbl71
Lbl70:
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
neg $v0, $t0
sw $v0,44($sp)
lw $t0,32($sp)
#Argument var.var611
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
#Argument var.var613
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var614<-['Main', 'is_even']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,132($sp)
Lbl71:
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
addi $sp, $sp, 148
jr $ra
f54: #Main.class_type
addi $sp, $sp, -284
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
la $t1,Eclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,24($sp)
lw $t0,24($sp)
seq $v0, $t0, $zero
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, var.var645
lw $t0,20($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,20($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
la $v0, st58
sw $v0,48($sp)
lw $t0,40($sp)
#Argument var.var647
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
#Argument var.var648
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var649<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,20($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,8($sp)
b var.var641
var.var645:
lw $t0,4($sp)
la $t1,Dclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,68($sp)
lw $t0,68($sp)
seq $v0, $t0, $zero
sw $v0,72($sp)
lw $t0,72($sp)
bgtz $t0, var.var654
lw $t0,64($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,64($sp)
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
la $v0, st59
sw $v0,92($sp)
lw $t0,84($sp)
#Argument var.var656
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var657
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var658<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,64($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,8($sp)
b var.var641
var.var654:
lw $t0,4($sp)
la $t1,Cclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,112($sp)
lw $t0,112($sp)
seq $v0, $t0, $zero
sw $v0,116($sp)
lw $t0,116($sp)
bgtz $t0, var.var663
lw $t0,108($sp)
move $v0, $t0
sw $v0,124($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,108($sp)
move $t0,$a0
move $v0, $t0
sw $v0,128($sp)
la $v0, st60
sw $v0,136($sp)
lw $t0,128($sp)
#Argument var.var665
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,140($sp)
#Argument var.var666
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var667<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
lw $t0,124($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,8($sp)
b var.var641
var.var663:
lw $t0,4($sp)
la $t1,Bclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,156($sp)
lw $t0,156($sp)
seq $v0, $t0, $zero
sw $v0,160($sp)
lw $t0,160($sp)
bgtz $t0, var.var672
lw $t0,152($sp)
move $v0, $t0
sw $v0,168($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,152($sp)
move $t0,$a0
move $v0, $t0
sw $v0,172($sp)
la $v0, st61
sw $v0,180($sp)
lw $t0,172($sp)
#Argument var.var674
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,184($sp)
#Argument var.var675
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var676<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,184($sp)
lw $t0,184($sp)
move $v0, $t0
sw $v0,188($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,152($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,8($sp)
b var.var641
var.var672:
lw $t0,4($sp)
la $t1,Aclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,200($sp)
lw $t0,200($sp)
seq $v0, $t0, $zero
sw $v0,204($sp)
lw $t0,204($sp)
bgtz $t0, var.var681
lw $t0,196($sp)
move $v0, $t0
sw $v0,212($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,196($sp)
move $t0,$a0
move $v0, $t0
sw $v0,216($sp)
la $v0, st62
sw $v0,224($sp)
lw $t0,216($sp)
#Argument var.var683
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,228($sp)
#Argument var.var684
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var685<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,228($sp)
lw $t0,228($sp)
move $v0, $t0
sw $v0,232($sp)
lw $t0,212($sp)
move $v0, $t0
sw $v0,196($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,8($sp)
b var.var641
var.var681:
lw $t0,4($sp)
la $t1,Objectclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,244($sp)
lw $t0,244($sp)
seq $v0, $t0, $zero
sw $v0,248($sp)
lw $t0,248($sp)
bgtz $t0, var.var690
lw $t0,240($sp)
move $v0, $t0
sw $v0,256($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,240($sp)
move $t0,$a0
move $v0, $t0
sw $v0,260($sp)
la $v0, st63
sw $v0,268($sp)
lw $t0,260($sp)
#Argument var.var692
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,272($sp)
#Argument var.var693
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var694<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,272($sp)
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,256($sp)
move $v0, $t0
sw $v0,240($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,8($sp)
b var.var641
var.var690:
var.var641:
lw $t0,8($sp)
move $v0, $t0
sw $v0,280($sp)
addi $sp, $sp, 284
jr $ra
f55: #Main.print
addi $sp, $sp, -64
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
li $v0, 9
syscall
la $t0, A2Iclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
#Argument var.var697
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var697<-['A2I', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
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
lw $t0,4($sp)
move $v0, $t0
sw $v0,20($sp)
move $t0,$a1
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
#Argument var.var701
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var702<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $t0,20($sp)
#Argument var.var700
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,32($sp)
#Argument var.var702
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var703<-['A2I', 'i2a']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,32($sp)
lw $t0,16($sp)
#Argument var.var699
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
#Argument var.var703
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var704<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,36($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
la $v0, st64
sw $v0,48($sp)
lw $t0,40($sp)
#Argument var.var705
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
#Argument var.var706
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var707<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
addi $sp, $sp, 64
jr $ra
f56: #Main.main
addi $sp, $sp, -1068
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
#Argument var.var710
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var710<-['A', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,8($a0)
Lbl72:
lw $t0,16($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
seq $v0, $t0, $zero
sw $v0,20($sp)
lw $t0,20($sp)
bgtz $t0, Lbl73
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
la $v0, st65
sw $v0,32($sp)
lw $t0,24($sp)
#Argument var.var713
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
#Argument var.var714
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var715<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,36($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
#Argument var.var716
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
#Argument var.var717
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var718<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,48($sp)
move $t0,$a0
move $v0, $t0
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
#Argument var.var720
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var721<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,60($sp)
lw $t0,52($sp)
#Argument var.var719
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,64($sp)
#Argument var.var721
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var722<-['Main', 'is_even']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl74
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
la $v0, st67
sw $v0,92($sp)
lw $t0,84($sp)
#Argument var.var726
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var727
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var728<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl75
Lbl74:
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
la $v0, st66
sw $v0,76($sp)
lw $t0,68($sp)
#Argument var.var723
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,80($sp)
#Argument var.var724
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var725<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl75:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
move $t0,$a0
move $v0, $t0
sw $v0,108($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,112($sp)
lw $t0,108($sp)
#Argument var.var731
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,116($sp)
#Argument var.var732
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var733<-['Main', 'class_type']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,116($sp)
move $t0,$a0
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
#Argument var.var734
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var735<-['Main', 'menu']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,4($a0)
lw $t0,4($a0)
move $v0, $t0
sw $v0,132($sp)
la $v0, st68
sw $v0,140($sp)
lw $t0,132($sp)
lw $t1,140($sp)
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
sw $v0,148($sp)
lw $t0,148($sp)
bgtz $t0, Lbl96
lw $t0,4($a0)
move $v0, $t0
sw $v0,196($sp)
la $v0, st69
sw $v0,204($sp)
lw $t0,196($sp)
lw $t1,204($sp)
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
sw $v0,212($sp)
lw $t0,212($sp)
bgtz $t0, Lbl94
lw $t0,4($a0)
move $v0, $t0
sw $v0,376($sp)
la $v0, st71
sw $v0,384($sp)
lw $t0,376($sp)
lw $t1,384($sp)
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
sw $v0,392($sp)
lw $t0,392($sp)
bgtz $t0, Lbl92
lw $t0,4($a0)
move $v0, $t0
sw $v0,436($sp)
la $v0, st72
sw $v0,444($sp)
lw $t0,436($sp)
lw $t1,444($sp)
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
sw $v0,452($sp)
lw $t0,452($sp)
bgtz $t0, Lbl90
lw $t0,4($a0)
move $v0, $t0
sw $v0,472($sp)
la $v0, st73
sw $v0,480($sp)
lw $t0,472($sp)
lw $t1,480($sp)
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
sw $v0,488($sp)
lw $t0,488($sp)
bgtz $t0, Lbl88
lw $t0,4($a0)
move $v0, $t0
sw $v0,508($sp)
la $v0, st74
sw $v0,516($sp)
lw $t0,508($sp)
lw $t1,516($sp)
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
sw $v0,524($sp)
lw $t0,524($sp)
bgtz $t0, Lbl86
lw $t0,4($a0)
move $v0, $t0
sw $v0,544($sp)
la $v0, st75
sw $v0,552($sp)
lw $t0,544($sp)
lw $t1,552($sp)
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
sw $v0,560($sp)
lw $t0,560($sp)
bgtz $t0, Lbl84
lw $t0,4($a0)
move $v0, $t0
sw $v0,676($sp)
la $v0, st80
sw $v0,684($sp)
lw $t0,676($sp)
lw $t1,684($sp)
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
sw $v0,692($sp)
lw $t0,692($sp)
bgtz $t0, Lbl82
lw $t0,4($a0)
move $v0, $t0
sw $v0,912($sp)
la $v0, st85
sw $v0,920($sp)
lw $t0,912($sp)
lw $t1,920($sp)
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
sw $v0,928($sp)
lw $t0,928($sp)
bgtz $t0, Lbl80
lw $t0,4($a0)
move $v0, $t0
sw $v0,936($sp)
la $v0, st86
sw $v0,944($sp)
lw $t0,936($sp)
lw $t1,944($sp)
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
sw $v0,952($sp)
lw $t0,952($sp)
bgtz $t0, Lbl78
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,964($sp)
lw $t0,964($sp)
#Argument var.var918
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var918<-['A', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,964($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,968($sp)
lw $t0,968($sp)
#Argument var.var919
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var920<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,972($sp)
lw $t0,964($sp)
#Argument var.var918
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,976($sp)
#Argument var.var920
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var921<-['A', 'method1']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,976($sp)
lw $t0,976($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,980($sp)
b Lbl79
Lbl78:
move $t0, $zero
move $v0, $t0
sw $v0,960($sp)
lw $t0,960($sp)
move $v0, $t0
sw $v0,16($a0)
lw $t0,16($a0)
move $v0, $t0
sw $v0,980($sp)
Lbl79:
lw $t0,980($sp)
move $v0, $t0
sw $v0,984($sp)
lw $t0,984($sp)
move $v0, $t0
sw $v0,988($sp)
b Lbl81
Lbl80:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,932($sp)
lw $t0,932($sp)
#Argument var.var912
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var912<-['A', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,932($sp)
lw $t0,932($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,988($sp)
Lbl81:
lw $t0,988($sp)
move $v0, $t0
sw $v0,992($sp)
lw $t0,992($sp)
move $v0, $t0
sw $v0,996($sp)
b Lbl83
Lbl82:
li $t0,0
move $v0, $t0
sw $v0,700($sp)
lw $t0,696($sp)
move $v0, $t0
sw $v0,704($sp)
lw $t0,700($sp)
move $v0, $t0
sw $v0,696($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,708($sp)
lw $t0,708($sp)
#Argument var.var862
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var862<-['E', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,708($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,712($sp)
lw $t0,712($sp)
#Argument var.var863
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var864<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,716($sp)
lw $t0,708($sp)
#Argument var.var862
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,720($sp)
#Argument var.var864
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var865<-['E', 'method6']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,720($sp)
lw $t0,720($sp)
move $v0, $t0
sw $v0,696($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,728($sp)
lw $t0,728($sp)
#Argument var.var866
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var867<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,732($sp)
lw $t0,696($sp)
move $v0, $t0
sw $v0,736($sp)
lw $t0,736($sp)
#Argument var.var868
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var869<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,740($sp)
li $t0,8
move $v0, $t0
sw $v0,744($sp)
lw $t0,740($sp)
lw $t1,744($sp)
mult $t0, $t1
mflo $v0
sw $v0,752($sp)
lw $t0,732($sp)
lw $t1,752($sp)
sub $v0, $t0, $t1
sw $v0,760($sp)
lw $t0,724($sp)
move $v0, $t0
sw $v0,764($sp)
lw $t0,760($sp)
move $v0, $t0
sw $v0,724($sp)
move $t0,$a0
move $v0, $t0
sw $v0,768($sp)
la $v0, st81
sw $v0,776($sp)
lw $t0,768($sp)
#Argument var.var876
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,780($sp)
#Argument var.var877
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var878<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,780($sp)
move $t0,$a0
move $v0, $t0
sw $v0,784($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,788($sp)
lw $t0,784($sp)
#Argument var.var879
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,792($sp)
#Argument var.var880
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var881<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,792($sp)
move $t0,$a0
move $v0, $t0
sw $v0,796($sp)
la $v0, st82
sw $v0,804($sp)
lw $t0,796($sp)
#Argument var.var882
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,808($sp)
#Argument var.var883
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var884<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,808($sp)
move $t0,$a0
move $v0, $t0
sw $v0,812($sp)
lw $t0,696($sp)
move $v0, $t0
sw $v0,816($sp)
lw $t0,812($sp)
#Argument var.var885
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,820($sp)
#Argument var.var886
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var887<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,820($sp)
move $t0,$a0
move $v0, $t0
sw $v0,824($sp)
la $v0, st83
sw $v0,832($sp)
lw $t0,824($sp)
#Argument var.var888
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,836($sp)
#Argument var.var889
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var890<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,836($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
li $v0, 9
syscall
la $t0, A2Iclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,840($sp)
lw $t0,840($sp)
#Argument var.var891
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var891<-['A2I', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,840($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,844($sp)
lw $t0,840($sp)
move $v0, $t0
sw $v0,276($sp)
move $t0,$a0
move $v0, $t0
sw $v0,848($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,852($sp)
lw $t0,724($sp)
move $v0, $t0
sw $v0,856($sp)
lw $t0,852($sp)
#Argument var.var894
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,860($sp)
#Argument var.var895
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var896<-['A2I', 'i2a']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,860($sp)
lw $t0,848($sp)
#Argument var.var893
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,864($sp)
#Argument var.var896
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var897<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,864($sp)
move $t0,$a0
move $v0, $t0
sw $v0,868($sp)
la $v0, st84
sw $v0,876($sp)
lw $t0,868($sp)
#Argument var.var898
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,880($sp)
#Argument var.var899
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var900<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,880($sp)
lw $t0,880($sp)
move $v0, $t0
sw $v0,884($sp)
lw $t0,844($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,884($sp)
move $v0, $t0
sw $v0,888($sp)
lw $t0,888($sp)
move $v0, $t0
sw $v0,892($sp)
lw $t0,764($sp)
move $v0, $t0
sw $v0,724($sp)
lw $t0,892($sp)
move $v0, $t0
sw $v0,896($sp)
lw $t0,696($sp)
move $v0, $t0
sw $v0,900($sp)
lw $t0,900($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,904($sp)
lw $t0,704($sp)
move $v0, $t0
sw $v0,696($sp)
lw $t0,904($sp)
move $v0, $t0
sw $v0,908($sp)
lw $t0,908($sp)
move $v0, $t0
sw $v0,996($sp)
Lbl83:
lw $t0,996($sp)
move $v0, $t0
sw $v0,1000($sp)
lw $t0,1000($sp)
move $v0, $t0
sw $v0,1004($sp)
b Lbl85
Lbl84:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,564($sp)
lw $t0,564($sp)
#Argument var.var832
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var832<-['D', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,564($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,568($sp)
lw $t0,568($sp)
#Argument var.var833
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var834<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,572($sp)
lw $t0,564($sp)
#Argument var.var832
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,576($sp)
#Argument var.var834
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var835<-['D', 'method7']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,576($sp)
lw $t0,576($sp)
bgtz $t0, Lbl76
move $t0,$a0
move $v0, $t0
sw $v0,624($sp)
la $v0, st78
sw $v0,632($sp)
lw $t0,624($sp)
#Argument var.var845
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,636($sp)
#Argument var.var846
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var847<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,636($sp)
move $t0,$a0
move $v0, $t0
sw $v0,640($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,644($sp)
lw $t0,640($sp)
#Argument var.var848
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,648($sp)
#Argument var.var849
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var850<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,648($sp)
move $t0,$a0
move $v0, $t0
sw $v0,652($sp)
la $v0, st79
sw $v0,660($sp)
lw $t0,652($sp)
#Argument var.var851
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,664($sp)
#Argument var.var852
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var853<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,664($sp)
lw $t0,664($sp)
move $v0, $t0
sw $v0,668($sp)
b Lbl77
Lbl76:
move $t0,$a0
move $v0, $t0
sw $v0,580($sp)
la $v0, st76
sw $v0,588($sp)
lw $t0,580($sp)
#Argument var.var836
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,592($sp)
#Argument var.var837
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var838<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,592($sp)
move $t0,$a0
move $v0, $t0
sw $v0,596($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,600($sp)
lw $t0,596($sp)
#Argument var.var839
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,604($sp)
#Argument var.var840
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var841<-['Main', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,604($sp)
move $t0,$a0
move $v0, $t0
sw $v0,608($sp)
la $v0, st77
sw $v0,616($sp)
lw $t0,608($sp)
#Argument var.var842
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,620($sp)
#Argument var.var843
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var844<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,620($sp)
lw $t0,620($sp)
move $v0, $t0
sw $v0,668($sp)
Lbl77:
lw $t0,668($sp)
move $v0, $t0
sw $v0,672($sp)
lw $t0,672($sp)
move $v0, $t0
sw $v0,1004($sp)
Lbl85:
lw $t0,1004($sp)
move $v0, $t0
sw $v0,1008($sp)
lw $t0,1008($sp)
move $v0, $t0
sw $v0,1012($sp)
b Lbl87
Lbl86:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,528($sp)
lw $t0,528($sp)
#Argument var.var824
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var824<-['C', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,528($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,532($sp)
lw $t0,532($sp)
#Argument var.var825
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var826<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,536($sp)
lw $t0,528($sp)
#Argument var.var824
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,540($sp)
#Argument var.var826
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
la $t0,Cclase
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var827<-['C', 'method5']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,540($sp)
lw $t0,540($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,1012($sp)
Lbl87:
lw $t0,1012($sp)
move $v0, $t0
sw $v0,1016($sp)
lw $t0,1016($sp)
move $v0, $t0
sw $v0,1020($sp)
b Lbl89
Lbl88:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,492($sp)
lw $t0,492($sp)
#Argument var.var816
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var816<-['C', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,492($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,496($sp)
lw $t0,496($sp)
#Argument var.var817
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var818<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,500($sp)
lw $t0,492($sp)
#Argument var.var816
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,504($sp)
#Argument var.var818
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
la $t0,Bclase
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var819<-['B', 'method5']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,504($sp)
lw $t0,504($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,1020($sp)
Lbl89:
lw $t0,1020($sp)
move $v0, $t0
sw $v0,1024($sp)
lw $t0,1024($sp)
move $v0, $t0
sw $v0,1028($sp)
b Lbl91
Lbl90:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,456($sp)
lw $t0,456($sp)
#Argument var.var808
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var808<-['C', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,456($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,460($sp)
lw $t0,460($sp)
#Argument var.var809
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var810<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,464($sp)
lw $t0,456($sp)
#Argument var.var808
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,468($sp)
#Argument var.var810
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
la $t0,Aclase
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var811<-['A', 'method5']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,468($sp)
lw $t0,468($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,1028($sp)
Lbl91:
lw $t0,1028($sp)
move $v0, $t0
sw $v0,1032($sp)
lw $t0,1032($sp)
move $v0, $t0
sw $v0,1036($sp)
b Lbl93
Lbl92:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,396($sp)
lw $t0,396($sp)
#Argument var.var794
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var794<-['A', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,396($sp)
move $t0,$a0
move $v0, $t0
sw $v0,400($sp)
lw $t0,400($sp)
#Argument var.var795
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var796<-['Main', 'get_int']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,404($sp)
lw $t0,396($sp)
#Argument var.var794
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,408($sp)
#Argument var.var796
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var797<-['A', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,408($sp)
lw $t0,408($sp)
move $v0, $t0
sw $v0,12($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,412($sp)
lw $t0,412($sp)
#Argument var.var798
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var798<-['D', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,412($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,416($sp)
lw $t0,416($sp)
#Argument var.var799
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var800<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,420($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,424($sp)
lw $t0,424($sp)
#Argument var.var801
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var802<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,428($sp)
lw $t0,412($sp)
#Argument var.var798
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,424($sp)
#Argument var.var800
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,436($sp)
#Argument var.var802
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var803<-['D', 'method4']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,432($sp)
lw $t0,432($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,1036($sp)
Lbl93:
lw $t0,1036($sp)
move $v0, $t0
sw $v0,1040($sp)
lw $t0,1040($sp)
move $v0, $t0
sw $v0,1044($sp)
b Lbl95
Lbl94:
lw $t0,8($a0)
move $v0, $t0
sw $v0,216($sp)
lw $t0,216($sp)
la $t1,Cclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,236($sp)
lw $t0,236($sp)
seq $v0, $t0, $zero
sw $v0,240($sp)
lw $t0,240($sp)
bgtz $t0, var.var760
lw $t0,232($sp)
move $v0, $t0
sw $v0,248($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,232($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,252($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,256($sp)
lw $t0,256($sp)
#Argument var.var763
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var764<-['C', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,260($sp)
lw $t0,252($sp)
#Argument var.var762
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,264($sp)
#Argument var.var764
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var765<-['C', 'method6']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,264($sp)
lw $t0,264($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,268($sp)
lw $t0,248($sp)
move $v0, $t0
sw $v0,232($sp)
lw $t0,268($sp)
move $v0, $t0
sw $v0,220($sp)
b var.var756
var.var760:
lw $t0,216($sp)
la $t1,Aclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,280($sp)
lw $t0,280($sp)
seq $v0, $t0, $zero
sw $v0,284($sp)
lw $t0,284($sp)
bgtz $t0, var.var770
lw $t0,276($sp)
move $v0, $t0
sw $v0,292($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,300($sp)
lw $t0,300($sp)
#Argument var.var773
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var774<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,304($sp)
lw $t0,296($sp)
#Argument var.var772
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,308($sp)
#Argument var.var774
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var775<-['A', 'method3']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,308($sp)
lw $t0,308($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,312($sp)
lw $t0,292($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,312($sp)
move $v0, $t0
sw $v0,220($sp)
b var.var756
var.var770:
lw $t0,216($sp)
la $t1,Objectclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,324($sp)
lw $t0,324($sp)
seq $v0, $t0, $zero
sw $v0,328($sp)
lw $t0,328($sp)
bgtz $t0, var.var780
lw $t0,320($sp)
move $v0, $t0
sw $v0,336($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,320($sp)
move $t0,$a0
move $v0, $t0
sw $v0,340($sp)
la $v0, st70
sw $v0,348($sp)
lw $t0,340($sp)
#Argument var.var782
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,352($sp)
#Argument var.var783
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var784<-['Main', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,352($sp)
move $t0,$a0
move $v0, $t0
sw $v0,356($sp)
lw $t0,356($sp)
#Argument var.var785
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var786<-['Main', 'abort']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,360($sp)
li $t0,0
move $v0, $t0
sw $v0,364($sp)
lw $t0,364($sp)
move $v0, $t0
sw $v0,368($sp)
lw $t0,336($sp)
move $v0, $t0
sw $v0,320($sp)
lw $t0,368($sp)
move $v0, $t0
sw $v0,220($sp)
b var.var756
var.var780:
var.var756:
lw $t0,220($sp)
move $v0, $t0
sw $v0,372($sp)
lw $t0,372($sp)
move $v0, $t0
sw $v0,1044($sp)
Lbl95:
lw $t0,1044($sp)
move $v0, $t0
sw $v0,1048($sp)
lw $t0,1048($sp)
move $v0, $t0
sw $v0,1052($sp)
b Lbl97
Lbl96:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,156($sp)
lw $t0,156($sp)
#Argument var.var740
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var740<-['A', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,156($sp)
move $t0,$a0
move $v0, $t0
sw $v0,160($sp)
lw $t0,160($sp)
#Argument var.var741
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var742<-['Main', 'get_int']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,164($sp)
lw $t0,156($sp)
#Argument var.var740
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,168($sp)
#Argument var.var742
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var743<-['A', 'set_var']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,12($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, Bclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,172($sp)
lw $t0,172($sp)
#Argument var.var744
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var744<-['B', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,172($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,176($sp)
lw $t0,176($sp)
#Argument var.var745
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var746<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,180($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,184($sp)
lw $t0,184($sp)
#Argument var.var747
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var748<-['A', 'value']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,188($sp)
lw $t0,172($sp)
#Argument var.var744
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,184($sp)
#Argument var.var746
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,196($sp)
#Argument var.var748
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var749<-['B', 'method2']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,1052($sp)
Lbl97:
lw $t0,1052($sp)
move $v0, $t0
sw $v0,1056($sp)
b Lbl72
Lbl73:
li $t0,0
move $v0, $t0
sw $v0,1064($sp)
addi $sp, $sp, 1068
jr $ra
