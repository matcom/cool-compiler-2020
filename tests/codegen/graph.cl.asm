.data
st0: .asciiz "Object"
st1: .asciiz "Graph"
st2: .asciiz "BoolOp"
st3: .asciiz "IO"
st4: .asciiz "String"
st5: .asciiz "Bool"
st6: .asciiz "Vertice"
st7: .asciiz "Edge"
st8: .asciiz " ("
st9: .asciiz ","
st10: .asciiz ")"
st11: .asciiz "EList"
st12: .asciiz "\n"
st13: .asciiz "VList"
st14: .asciiz "\n"
st15: .asciiz ""
st16: .asciiz "Parse"
st17: .asciiz "\n"
st18: .asciiz ""
st19: .asciiz "0"
st20: .asciiz "1"
st21: .asciiz "2"
st22: .asciiz "3"
st23: .asciiz "4"
st24: .asciiz "5"
st25: .asciiz "6"
st26: .asciiz "7"
st27: .asciiz "8"
st28: .asciiz "9"
st29: .asciiz "-"
st30: .asciiz " "
st31: .asciiz " "
st32: .asciiz ","
st33: .asciiz ""
st34: .asciiz ""
st35: .asciiz "ECons"
st36: .asciiz "VCons"
st37: .asciiz "Main"
Objectclase: .word 0,f0,f3,f2,f4
Graphclase: .word Objectclase,f5,f6,f2,f4,f7,f8,f9
BoolOpclase: .word Objectclase,f10,f11,f2,f4,f12,f13
IOclase: .word Objectclase,f14,f15,f2,f4,f16,f17,f18,f19
Stringclase: .word Objectclase,f20,f21,f2,f4,f22,f23,f24
Boolclase: .word Objectclase,f25,f26,f2,f4
Verticeclase: .word IOclase,f27,f28,f2,f4,f16,f17,f18,f19,f29,f30,f31,f32,f33
Edgeclase: .word IOclase,f34,f35,f2,f4,f16,f17,f18,f19,f36,f37
EListclase: .word IOclase,f38,f39,f2,f4,f16,f17,f18,f19,f40,f41,f42,f43,f44,f45
VListclase: .word IOclase,f46,f47,f2,f4,f16,f17,f18,f19,f48,f49,f50,f51,f52
Parseclase: .word IOclase,f53,f54,f2,f4,f16,f17,f18,f19,f55,f56,f57,f58,f59
EConsclase: .word EListclase,f60,f61,f2,f4,f16,f17,f18,f19,f62,f63,f64,f43,f44,f66,f65
VConsclase: .word VListclase,f67,f68,f2,f4,f16,f17,f18,f19,f69,f70,f71,f51,f73,f72
Mainclase: .word Parseclase,f74,f75,f2,f4,f16,f17,f18,f19,f55,f56,f57,f58,f59,f76
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
Main.Special:
addi $sp, $sp, -12
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,16
li $v0, 9
syscall
la $t0, Mainclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f0:
addi $sp, $sp, -8
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f3:
addi $sp, $sp, -12
la $v0, st0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f4:
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
f2:
addi $sp, $sp, -8
jal .Object.abort
addi $sp, $sp, 8
jr $ra
f5:
addi $sp, $sp, -20
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, VListclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, EListclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f6:
addi $sp, $sp, -12
la $v0, st1
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f7:
addi $sp, $sp, -40
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,4($a0)
move $v0, $t0
sw $v0,28($sp)
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,4($a0)
addi $sp, $sp, 40
jr $ra
f8:
addi $sp, $sp, -12
lw $t0,8($a0)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f9:
addi $sp, $sp, -12
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f10:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
f11:
addi $sp, $sp, -12
la $v0, st2
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f12:
addi $sp, $sp, -24
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
bgtz $t0, Lbl0
move $t0, $zero
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,16($sp)
b Lbl1
Lbl0:
move $t0,$a2
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,16($sp)
Lbl1:
lw $t0,16($sp)
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f13:
addi $sp, $sp, -24
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
bgtz $t0, Lbl2
move $t0,$a2
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,16($sp)
b Lbl3
Lbl2:
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,16($sp)
Lbl3:
lw $t0,16($sp)
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f14:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
f15:
addi $sp, $sp, -12
la $v0, st3
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f16:
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
f17:
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
f18:
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
f19:
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
f20:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
f21:
addi $sp, $sp, -12
la $v0, st4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f22:
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
f23:
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
f24:
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
f25:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
f26:
addi $sp, $sp, -12
la $v0, st5
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f27:
addi $sp, $sp, -16
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,4($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
li $v0, 9
syscall
la $t0, EListclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f28:
addi $sp, $sp, -12
la $v0, st6
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f29:
addi $sp, $sp, -8
lw $t0,8($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f30:
addi $sp, $sp, -8
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f31:
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
f32:
addi $sp, $sp, -24
lw $t0,8($a0)
move $v0, $t0
sw $v0,8($sp)
move $t0,$a1
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f33:
addi $sp, $sp, -24
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,12($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f34:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
f35:
addi $sp, $sp, -12
la $v0, st7
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f36:
addi $sp, $sp, -32
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
move $t0,$a2
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a3
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,12($a0)
move $t0,$a0
move $v0, $t0
sw $v0,28($sp)
addi $sp, $sp, 32
jr $ra
f37:
addi $sp, $sp, -88
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
la $v0, st8
sw $v0,12($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
lw $t0,4($a0)
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,28($sp)
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
la $v0, st9
sw $v0,40($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,52($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,56($sp)
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
la $v0, st10
sw $v0,68($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,72($sp)
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,84($sp)
addi $sp, $sp, 88
jr $ra
f38:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,4($a0)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f39:
addi $sp, $sp, -12
la $v0, st11
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f40:
addi $sp, $sp, -8
li $t0,1
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f41:
addi $sp, $sp, -16
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,4($a0)
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f42:
addi $sp, $sp, -16
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f43:
addi $sp, $sp, -20
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,12
li $v0, 9
syscall
la $t0, EConsclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f44:
addi $sp, $sp, -52
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
bgtz $t0, Lbl4
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
move $t0,$a1
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,28($sp)
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,36($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
b Lbl5
Lbl4:
move $t0,$a1
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,44($sp)
Lbl5:
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
addi $sp, $sp, 52
jr $ra
f45:
addi $sp, $sp, -20
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
la $v0, st12
sw $v0,12($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f46:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,4($a0)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f47:
addi $sp, $sp, -12
la $v0, st13
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f48:
addi $sp, $sp, -8
li $t0,1
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f49:
addi $sp, $sp, -16
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,4($a0)
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f50:
addi $sp, $sp, -16
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f51:
addi $sp, $sp, -20
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,12
li $v0, 9
syscall
la $t0, VConsclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f52:
addi $sp, $sp, -20
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
la $v0, st14
sw $v0,12($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f53:
addi $sp, $sp, -24
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
li $v0, 9
syscall
la $t0, BoolOpclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
la $v0, st15
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f54:
addi $sp, $sp, -12
la $v0, st16
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f55:
addi $sp, $sp, -136
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,12
li $v0, 9
syscall
la $t0, Graphclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,12($sp)
Lbl6:
lw $t0,4($a0)
move $v0, $t0
sw $v0,24($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
la $v0, st17
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
sne $v0, $t0, $zero
sw $v0,52($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,56($sp)
la $v0, st18
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
sne $v0, $t0, $zero
sw $v0,80($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,84($sp)
lw $t0,84($sp)
sne $v0, $t0, $zero
sw $v0,92($sp)
lw $t0,92($sp)
bgtz $t0, Lbl7
lw $t0,4($sp)
move $v0, $t0
sw $v0,96($sp)
move $t0,$a0
move $v0, $t0
sw $v0,100($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,100($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,108($sp)
lw $t0,96($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,112($sp)
move $t0,$a0
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,12($sp)
b Lbl6
Lbl7:
li $t0,0
move $v0, $t0
sw $v0,128($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,132($sp)
addi $sp, $sp, 136
jr $ra
f56:
addi $sp, $sp, -140
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,12
li $v0, 9
syscall
la $t0, Verticeclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,20($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,4($sp)
Lbl8:
lw $t0,8($a0)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
li $t0,0
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
lw $t1,36($sp)
seq $v0 ,$t0, $t1
sw $v0,44($sp)
lw $t0,44($sp)
sne $v0, $t0, $zero
sw $v0,52($sp)
lw $t0,52($sp)
sne $v0, $t0, $zero
sw $v0,60($sp)
lw $t0,60($sp)
bgtz $t0, Lbl9
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,76($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,64($sp)
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,88($sp)
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,92($sp)
lw $t0,92($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,96($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,16
li $v0, 9
syscall
la $t0, Edgeclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,100($sp)
lw $t0,100($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,100($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,108($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,100($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,120($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0,128($sp)
addi $sp, $sp, -4
sw $a3, 0($sp)
move $a3,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a3, 0($sp)
lw $a2, 4($sp)
lw $a1, 8($sp)
lw $a0, 12($sp)
addi $sp, $sp, 16
sw $v0,120($sp)
lw $t0,96($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,124($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,124($sp)
b Lbl8
Lbl9:
li $t0,0
move $v0, $t0
sw $v0,132($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,136($sp)
addi $sp, $sp, 140
jr $ra
f57:
addi $sp, $sp, -336
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
la $v0, st19
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
bgtz $t0, Lbl28
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
la $v0, st20
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
bgtz $t0, Lbl26
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
la $v0, st21
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
bgtz $t0, Lbl24
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
la $v0, st22
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
bgtz $t0, Lbl22
move $t0,$a1
move $v0, $t0
sw $v0,100($sp)
la $v0, st23
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
bgtz $t0, Lbl20
move $t0,$a1
move $v0, $t0
sw $v0,124($sp)
la $v0, st24
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
bgtz $t0, Lbl18
move $t0,$a1
move $v0, $t0
sw $v0,148($sp)
la $v0, st25
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
bgtz $t0, Lbl16
move $t0,$a1
move $v0, $t0
sw $v0,172($sp)
la $v0, st26
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
bgtz $t0, Lbl14
move $t0,$a1
move $v0, $t0
sw $v0,196($sp)
la $v0, st27
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
bgtz $t0, Lbl12
move $t0,$a1
move $v0, $t0
sw $v0,220($sp)
la $v0, st28
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
bgtz $t0, Lbl10
move $t0,$a0
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
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
b Lbl11
Lbl10:
li $t0,9
move $v0, $t0
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,256($sp)
Lbl11:
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
lw $t0,260($sp)
move $v0, $t0
sw $v0,264($sp)
b Lbl13
Lbl12:
li $t0,8
move $v0, $t0
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,264($sp)
Lbl13:
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
b Lbl15
Lbl14:
li $t0,7
move $v0, $t0
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,272($sp)
Lbl15:
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,280($sp)
b Lbl17
Lbl16:
li $t0,6
move $v0, $t0
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,280($sp)
Lbl17:
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
b Lbl19
Lbl18:
li $t0,5
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,288($sp)
Lbl19:
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
b Lbl21
Lbl20:
li $t0,4
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,296($sp)
Lbl21:
lw $t0,296($sp)
move $v0, $t0
sw $v0,300($sp)
lw $t0,300($sp)
move $v0, $t0
sw $v0,304($sp)
b Lbl23
Lbl22:
li $t0,3
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,304($sp)
Lbl23:
lw $t0,304($sp)
move $v0, $t0
sw $v0,308($sp)
lw $t0,308($sp)
move $v0, $t0
sw $v0,312($sp)
b Lbl25
Lbl24:
li $t0,2
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,312($sp)
Lbl25:
lw $t0,312($sp)
move $v0, $t0
sw $v0,316($sp)
lw $t0,316($sp)
move $v0, $t0
sw $v0,320($sp)
b Lbl27
Lbl26:
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,320($sp)
Lbl27:
lw $t0,320($sp)
move $v0, $t0
sw $v0,324($sp)
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
b Lbl29
Lbl28:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,328($sp)
Lbl29:
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
addi $sp, $sp, 336
jr $ra
f58:
addi $sp, $sp, -216
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
bgtz $t0, Lbl34
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
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,40($sp)
la $v0, st29
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
bgtz $t0, Lbl32
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
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,116($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,124($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,120($sp)
la $v0, st30
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
bgtz $t0, Lbl30
move $t0,$a0
move $v0, $t0
sw $v0,180($sp)
move $t0,$a1
move $v0, $t0
sw $v0,184($sp)
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,188($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,188($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
b Lbl31
Lbl30:
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
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,176($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,172($sp)
lw $t0,140($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,176($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,176($sp)
lw $t0,176($sp)
move $v0, $t0
sw $v0,192($sp)
Lbl31:
lw $t0,192($sp)
move $v0, $t0
sw $v0,196($sp)
lw $t0,196($sp)
move $v0, $t0
sw $v0,200($sp)
b Lbl33
Lbl32:
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
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
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
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,96($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,92($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
not $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,200($sp)
Lbl33:
lw $t0,200($sp)
move $v0, $t0
sw $v0,204($sp)
lw $t0,204($sp)
move $v0, $t0
sw $v0,208($sp)
b Lbl35
Lbl34:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,208($sp)
Lbl35:
lw $t0,208($sp)
move $v0, $t0
sw $v0,212($sp)
addi $sp, $sp, 216
jr $ra
f59:
addi $sp, $sp, -372
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,12($sp)
li $t0,0
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,24($sp)
Lbl36:
lw $t0,24($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
lw $t1,36($sp)
slt $v0, $t0, $t1
sw $v0,44($sp)
lw $t0,44($sp)
sne $v0, $t0, $zero
sw $v0,52($sp)
lw $t0,52($sp)
bgtz $t0, Lbl37
move $t0,$a1
move $v0, $t0
sw $v0,60($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,64($sp)
li $t0,1
move $v0, $t0
sw $v0,68($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,76($sp)
la $v0, st31
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
bgtz $t0, Lbl42
lw $t0,56($sp)
move $v0, $t0
sw $v0,160($sp)
la $v0, st32
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
bgtz $t0, Lbl40
lw $t0,4($sp)
move $v0, $t0
sw $v0,240($sp)
li $t0,10
move $v0, $t0
sw $v0,244($sp)
lw $t0,240($sp)
lw $t1,244($sp)
mult $t0, $t1
mflo $v0
sw $v0,252($sp)
move $t0,$a0
move $v0, $t0
sw $v0,256($sp)
move $t0,$a1
move $v0, $t0
sw $v0,260($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,264($sp)
li $t0,1
move $v0, $t0
sw $v0,268($sp)
lw $t0,260($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,268($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,276($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,272($sp)
lw $t0,256($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,276($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,276($sp)
lw $t0,252($sp)
lw $t1,276($sp)
add $v0, $t0, $t1
sw $v0,284($sp)
lw $t0,284($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,288($sp)
li $t0,1
move $v0, $t0
sw $v0,292($sp)
lw $t0,288($sp)
lw $t1,292($sp)
add $v0, $t0, $t1
sw $v0,300($sp)
lw $t0,300($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,304($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,308($sp)
lw $t0,304($sp)
lw $t1,308($sp)
seq $v0 ,$t0, $t1
sw $v0,316($sp)
lw $t0,316($sp)
bgtz $t0, Lbl38
la $v0, st34
sw $v0,332($sp)
lw $t0,332($sp)
move $v0, $t0
sw $v0,336($sp)
b Lbl39
Lbl38:
la $v0, st33
sw $v0,324($sp)
lw $t0,324($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,8($a0)
move $v0, $t0
sw $v0,336($sp)
Lbl39:
lw $t0,336($sp)
move $v0, $t0
sw $v0,340($sp)
lw $t0,340($sp)
move $v0, $t0
sw $v0,344($sp)
b Lbl41
Lbl40:
move $t0,$a1
move $v0, $t0
sw $v0,180($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,184($sp)
li $t0,1
move $v0, $t0
sw $v0,188($sp)
lw $t0,184($sp)
lw $t1,188($sp)
add $v0, $t0, $t1
sw $v0,196($sp)
move $t0,$a1
move $v0, $t0
sw $v0,200($sp)
lw $t0,200($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,204($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,208($sp)
lw $t0,204($sp)
lw $t1,208($sp)
sub $v0, $t0, $t1
sw $v0,216($sp)
li $t0,1
move $v0, $t0
sw $v0,220($sp)
lw $t0,216($sp)
lw $t1,220($sp)
sub $v0, $t0, $t1
sw $v0,228($sp)
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,200($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,236($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,232($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,12($sp)
move $v0, $t0
sw $v0,236($sp)
lw $t0,236($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,344($sp)
Lbl41:
lw $t0,344($sp)
move $v0, $t0
sw $v0,348($sp)
lw $t0,348($sp)
move $v0, $t0
sw $v0,352($sp)
b Lbl43
Lbl42:
move $t0,$a1
move $v0, $t0
sw $v0,100($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,104($sp)
li $t0,1
move $v0, $t0
sw $v0,108($sp)
lw $t0,104($sp)
lw $t1,108($sp)
add $v0, $t0, $t1
sw $v0,116($sp)
move $t0,$a1
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Stringclase
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,124($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,128($sp)
lw $t0,124($sp)
lw $t1,128($sp)
sub $v0, $t0, $t1
sw $v0,136($sp)
li $t0,1
move $v0, $t0
sw $v0,140($sp)
lw $t0,136($sp)
lw $t1,140($sp)
sub $v0, $t0, $t1
sw $v0,148($sp)
lw $t0,100($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,120($sp)
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,156($sp)
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
la $t0,Stringclase
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,152($sp)
lw $t0,152($sp)
move $v0, $t0
sw $v0,8($a0)
lw $t0,12($sp)
move $v0, $t0
sw $v0,156($sp)
lw $t0,156($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,352($sp)
Lbl43:
lw $t0,352($sp)
move $v0, $t0
sw $v0,356($sp)
b Lbl36
Lbl37:
li $t0,0
move $v0, $t0
sw $v0,364($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,368($sp)
addi $sp, $sp, 372
jr $ra
f60:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,EListclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f61:
addi $sp, $sp, -12
la $v0, st35
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f62:
addi $sp, $sp, -8
move $t0, $zero
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f63:
addi $sp, $sp, -8
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f64:
addi $sp, $sp, -8
lw $t0,8($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f65:
addi $sp, $sp, -24
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
move $t0,$a2
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f66:
addi $sp, $sp, -20
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f67:
addi $sp, $sp, -12
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,VListclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f68:
addi $sp, $sp, -12
la $v0, st36
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f69:
addi $sp, $sp, -8
move $t0, $zero
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f70:
addi $sp, $sp, -8
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f71:
addi $sp, $sp, -8
lw $t0,8($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f72:
addi $sp, $sp, -24
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
move $t0,$a2
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, 24
jr $ra
f73:
addi $sp, $sp, -20
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f74:
addi $sp, $sp, -20
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Parseclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,12($a0)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f75:
addi $sp, $sp, -12
la $v0, st37
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f76:
addi $sp, $sp, -20
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
