.data
st0: .asciiz "Object"
st1: .asciiz "JustThere"
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
st32: .asciiz "Main"
st33: .asciiz "678987"
st34: .asciiz " == "
st35: .asciiz "\n"
Objectclase: .word 0,f0,f3,f2,f4
JustThereclase: .word Objectclase,f5,f6,f2,f4
A2Iclase: .word Objectclase,f7,f8,f2,f4,f9,f10,f11,f12,f13,f14
IOclase: .word Objectclase,f15,f16,f2,f4,f17,f18,f19,f20
Stringclase: .word Objectclase,f21,f22,f2,f4,f23,f24,f25
Boolclase: .word Objectclase,f26,f27,f2,f4
Mainclase: .word IOclase,f28,f29,f2,f4,f17,f18,f19,f20,f30
.text
.globl main
main:
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal Main.Special
lw $ra, 0($sp)
addi $sp ,$sp, 4
jr $ra
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
     sw $v0, 0($a0)
     jr $ra

     .IO.in_string:
     li $v0, 9
     move $s0, $a0
     li $a0, 1024
     syscall
     move $s1, $v0
     move $a0, $v0
     li $a0, 1024
     li $v0, 8
     syscall
     sw $s1, 0($s0)
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
     sw $v0, 0($a1)
     jr $ra

     .Object.abort:
     li $v0, 10
     syscall
     jr $ra

     .Str.stringcomparison:
     lw $t1, 0($a0)
     lw $t2, 0($a1)
     move $v0, $zero
     move $t3, $zero
     move $t4, $zero
     move $v0, $zero

     StrCompCiclo:
     add $t0, $t1, $v0
     lb $t3, 0($t0)
     add $t0, $t2, $v0
     lb $t4, 0($t0)
     bne $t3, $t4, StrDiferentes
     beq $t3, $zero, StrIguales
     b StrCompCiclo

     StrDiferentes:
     li $v0, 1
     StrIguales:
     sw $v0, 0($a2)
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
     move $a0, $a1
     jal .Str.stringlength
     add $s4, $s4, $v0

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
li $a0,4
li $v0, 9
syscall
la $t0, Mainclase
sw $t0, 0($v0)
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
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f0:
addi $sp, $sp, -8
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f3:
addi $sp, $sp, -12
la $v0, st0
sw $v0,8($sp)
lw $v0, 0($sp)
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
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f2:
addi $sp, $sp, -8
jal .Object.abort
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f5:
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
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f6:
addi $sp, $sp, -12
la $v0, st1
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f7:
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
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f8:
addi $sp, $sp, -12
la $v0, st2
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f9:
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
bgtz $t0, Lbl18
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
bgtz $t0, Lbl16
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
bgtz $t0, Lbl14
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
bgtz $t0, Lbl12
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
bgtz $t0, Lbl10
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
bgtz $t0, Lbl8
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
bgtz $t0, Lbl6
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
bgtz $t0, Lbl4
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
bgtz $t0, Lbl2
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
bgtz $t0, Lbl0
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
sw $v0,248($sp)
li $t0,0
move $v0, $t0
sw $v0,252($sp)
lw $t0,252($sp)
move $v0, $t0
sw $v0,256($sp)
b Lbl1
Lbl0:
li $t0,9
move $v0, $t0
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,256($sp)
Lbl1:
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
lw $t0,260($sp)
move $v0, $t0
sw $v0,264($sp)
b Lbl3
Lbl2:
li $t0,8
move $v0, $t0
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,264($sp)
Lbl3:
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
b Lbl5
Lbl4:
li $t0,7
move $v0, $t0
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,272($sp)
Lbl5:
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,280($sp)
b Lbl7
Lbl6:
li $t0,6
move $v0, $t0
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,280($sp)
Lbl7:
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
b Lbl9
Lbl8:
li $t0,5
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,288($sp)
Lbl9:
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
b Lbl11
Lbl10:
li $t0,4
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,296($sp)
Lbl11:
lw $t0,296($sp)
move $v0, $t0
sw $v0,300($sp)
lw $t0,300($sp)
move $v0, $t0
sw $v0,304($sp)
b Lbl13
Lbl12:
li $t0,3
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,304($sp)
Lbl13:
lw $t0,304($sp)
move $v0, $t0
sw $v0,308($sp)
lw $t0,308($sp)
move $v0, $t0
sw $v0,312($sp)
b Lbl15
Lbl14:
li $t0,2
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,312($sp)
Lbl15:
lw $t0,312($sp)
move $v0, $t0
sw $v0,316($sp)
lw $t0,316($sp)
move $v0, $t0
sw $v0,320($sp)
b Lbl17
Lbl16:
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,320($sp)
Lbl17:
lw $t0,320($sp)
move $v0, $t0
sw $v0,324($sp)
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
b Lbl19
Lbl18:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,328($sp)
Lbl19:
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
lw $v0, 0($sp)
addi $sp, $sp, 336
jr $ra
f10:
addi $sp, $sp, -340
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl38
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
li $t0,1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,40($sp)
lw $t0,40($sp)
bgtz $t0, Lbl36
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
li $t0,2
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl34
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
li $t0,3
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
lw $t1,80($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,88($sp)
lw $t0,88($sp)
bgtz $t0, Lbl32
move $t0,$a1
move $v0, $t0
sw $v0,100($sp)
li $t0,4
move $v0, $t0
sw $v0,104($sp)
lw $t0,100($sp)
lw $t1,104($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,112($sp)
lw $t0,112($sp)
bgtz $t0, Lbl30
move $t0,$a1
move $v0, $t0
sw $v0,124($sp)
li $t0,5
move $v0, $t0
sw $v0,128($sp)
lw $t0,124($sp)
lw $t1,128($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,136($sp)
lw $t0,136($sp)
bgtz $t0, Lbl28
move $t0,$a1
move $v0, $t0
sw $v0,148($sp)
li $t0,6
move $v0, $t0
sw $v0,152($sp)
lw $t0,148($sp)
lw $t1,152($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,160($sp)
lw $t0,160($sp)
bgtz $t0, Lbl26
move $t0,$a1
move $v0, $t0
sw $v0,172($sp)
li $t0,7
move $v0, $t0
sw $v0,176($sp)
lw $t0,172($sp)
lw $t1,176($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,184($sp)
lw $t0,184($sp)
bgtz $t0, Lbl24
move $t0,$a1
move $v0, $t0
sw $v0,196($sp)
li $t0,8
move $v0, $t0
sw $v0,200($sp)
lw $t0,196($sp)
lw $t1,200($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,208($sp)
lw $t0,208($sp)
bgtz $t0, Lbl22
move $t0,$a1
move $v0, $t0
sw $v0,220($sp)
li $t0,9
move $v0, $t0
sw $v0,224($sp)
lw $t0,220($sp)
lw $t1,224($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,232($sp)
lw $t0,232($sp)
bgtz $t0, Lbl20
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
sw $v0,248($sp)
la $v0, st23
sw $v0,256($sp)
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
b Lbl21
Lbl20:
la $v0, st22
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,260($sp)
Lbl21:
lw $t0,260($sp)
move $v0, $t0
sw $v0,264($sp)
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
b Lbl23
Lbl22:
la $v0, st21
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,268($sp)
Lbl23:
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
b Lbl25
Lbl24:
la $v0, st20
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,276($sp)
Lbl25:
lw $t0,276($sp)
move $v0, $t0
sw $v0,280($sp)
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
b Lbl27
Lbl26:
la $v0, st19
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,284($sp)
Lbl27:
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
b Lbl29
Lbl28:
la $v0, st18
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,292($sp)
Lbl29:
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,296($sp)
move $v0, $t0
sw $v0,300($sp)
b Lbl31
Lbl30:
la $v0, st17
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,300($sp)
Lbl31:
lw $t0,300($sp)
move $v0, $t0
sw $v0,304($sp)
lw $t0,304($sp)
move $v0, $t0
sw $v0,308($sp)
b Lbl33
Lbl32:
la $v0, st16
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,308($sp)
Lbl33:
lw $t0,308($sp)
move $v0, $t0
sw $v0,312($sp)
lw $t0,312($sp)
move $v0, $t0
sw $v0,316($sp)
b Lbl35
Lbl34:
la $v0, st15
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,316($sp)
Lbl35:
lw $t0,316($sp)
move $v0, $t0
sw $v0,320($sp)
lw $t0,320($sp)
move $v0, $t0
sw $v0,324($sp)
b Lbl37
Lbl36:
la $v0, st14
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,324($sp)
Lbl37:
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
b Lbl39
Lbl38:
la $v0, st13
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,332($sp)
Lbl39:
lw $t0,332($sp)
move $v0, $t0
sw $v0,336($sp)
lw $v0, 0($sp)
addi $sp, $sp, 340
jr $ra
f11:
addi $sp, $sp, -216
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
li $t0,0
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,20($sp)
lw $t0,20($sp)
bgtz $t0, Lbl44
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,0
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
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
bgtz $t0, Lbl42
move $t0,$a1
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,0
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
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
bgtz $t0, Lbl40
move $t0,$a0
move $v0, $t0
sw $v0,180($sp)
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,184($sp)
lw $t0,184($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,188($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
b Lbl41
Lbl40:
move $t0,$a0
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,148($sp)
lw $t0,148($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,156($sp)
li $t0,1
move $v0, $t0
sw $v0,160($sp)
lw $t0,156($sp)
lw $t1,160($sp)
sub $v0, $t0, $t1
sw $v0,168($sp)
lw $t0,168($sp)
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
sw $v0,172($sp)
lw $t0,172($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,176($sp)
lw $t0,176($sp)
move $v0, $t0
sw $v0,192($sp)
Lbl41:
lw $t0,192($sp)
move $v0, $t0
sw $v0,196($sp)
lw $t0,196($sp)
move $v0, $t0
sw $v0,200($sp)
b Lbl43
Lbl42:
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
li $t0,1
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
lw $t1,80($sp)
sub $v0, $t0, $t1
sw $v0,88($sp)
lw $t0,88($sp)
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
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
not $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,200($sp)
Lbl43:
lw $t0,200($sp)
move $v0, $t0
sw $v0,204($sp)
lw $t0,204($sp)
move $v0, $t0
sw $v0,208($sp)
b Lbl45
Lbl44:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,208($sp)
Lbl45:
lw $t0,208($sp)
move $v0, $t0
sw $v0,212($sp)
lw $v0, 0($sp)
addi $sp, $sp, 216
jr $ra
f12:
addi $sp, $sp, -132
li $t0,0
move $v0, $t0
sw $v0,8($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
li $t0,0
move $v0, $t0
sw $v0,28($sp)
Lbl46:
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
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1
sw $v0,52($sp)
lw $t0,52($sp)
bgtz $t0, Lbl47
lw $t0,4($sp)
move $v0, $t0
sw $v0,56($sp)
li $t0,10
move $v0, $t0
sw $v0,60($sp)
lw $t0,56($sp)
lw $t1,60($sp)
mult $t0, $t1
mflo $v0
sw $v0,68($sp)
move $t0,$a0
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
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
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $t0,68($sp)
lw $t1,92($sp)
add $v0, $t0, $t1
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,4($sp)
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
lw $t0,116($sp)
move $v0, $t0
sw $v0,24($sp)
b Lbl46
Lbl47:
li $t0,0
move $v0, $t0
sw $v0,124($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,128($sp)
lw $v0, 0($sp)
addi $sp, $sp, 132
jr $ra
f13:
addi $sp, $sp, -116
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl50
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
bgtz $t0, Lbl48
la $v0, st27
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
li $t0,1
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
not $v0, $t0
sw $v0,80($sp)
lw $t0,68($sp)
lw $t1,80($sp)
mult $t0, $t1
mflo $v0
sw $v0,88($sp)
lw $t0,88($sp)
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
sw $v0,92($sp)
lw $t0,92($sp)
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
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl49
Lbl48:
move $t0,$a0
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
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
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl49:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
b Lbl51
Lbl50:
la $v0, st26
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,108($sp)
Lbl51:
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
lw $v0, 0($sp)
addi $sp, $sp, 116
jr $ra
f14:
addi $sp, $sp, -108
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl52
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
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
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
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,64($sp)
lw $t0,28($sp)
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
lw $t0,64($sp)
lw $t1,80($sp)
sub $v0, $t0, $t1
sw $v0,88($sp)
lw $t0,88($sp)
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
sw $v0,92($sp)
lw $t0,92($sp)
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
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl53
Lbl52:
la $v0, st28
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl53:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $v0, 0($sp)
addi $sp, $sp, 108
jr $ra
f15:
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
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f16:
addi $sp, $sp, -12
la $v0, st29
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f17:
addi $sp, $sp, -8
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.out_string
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
move $a1,$t0
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f18:
addi $sp, $sp, -8
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.out_int
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
move $a1,$t0
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
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
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f20:
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
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f21:
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
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f22:
addi $sp, $sp, -12
la $v0, st30
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f23:
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
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f24:
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
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f25:
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
lw $v0, 0($sp)
addi $sp, $sp, 8
jr $ra
f26:
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
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f27:
addi $sp, $sp, -12
la $v0, st31
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f28:
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
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f29:
addi $sp, $sp, -12
la $v0, st32
sw $v0,8($sp)
lw $v0, 0($sp)
addi $sp, $sp, 12
jr $ra
f30:
addi $sp, $sp, -96
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
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st33
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
sw $v0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
li $v0, 9
syscall
la $t0, A2Iclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $t0,28($sp)
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
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,678987
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
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
sw $v0,36($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
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
sw $v0,48($sp)
move $t0,$a0
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st34
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,64($sp)
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
move $t0,$a0
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st35
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $v0, 0($sp)
addi $sp, $sp, 96
jr $ra
