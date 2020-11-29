.data
st0: .asciiz "Object"
st1: .asciiz "Main"
st2: .asciiz "do nothing"
st3: .asciiz "IO"
st4: .asciiz "String"
st5: .asciiz "Bool"
st6: .asciiz "Bazz"
st7: .asciiz "Foo"
st8: .asciiz "Razz"
st9: .asciiz "Bar"
Objectclase: .word 0,f0,f3,f2,f4
Mainclase: .word Objectclase,f5,f6,f2,f4,f7
IOclase: .word Objectclase,f8,f9,f2,f4,f10,f11,f12,f13
Stringclase: .word Objectclase,f14,f15,f2,f4,f16,f17,f18
Boolclase: .word Objectclase,f19,f20,f2,f4
Bazzclase: .word IOclase,f21,f22,f2,f4,f10,f11,f12,f13,f23,f24
Fooclase: .word Bazzclase,f25,f26,f2,f4,f10,f11,f12,f13,f23,f27
Razzclase: .word Fooclase,f28,f29,f2,f4,f10,f11,f12,f13,f23,f27
Barclase: .word Razzclase,f30,f31,f2,f4,f10,f11,f12,f13,f23,f27
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
#Argument var.var177
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var177<-['Main', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var177
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var178<-['Main', 'main']
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
f5: #Main.$init
addi $sp, $sp, -28
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
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,16
li $v0, 9
syscall
la $t0, Bazzclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
#Argument var.var8
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var8<-['Bazz', '$init']
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
li $a0,24
li $v0, 9
syscall
la $t0, Fooclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
#Argument var.var9
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var9<-['Foo', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,8($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,32
li $v0, 9
syscall
la $t0, Razzclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
sw $zero, 24($v0)
sw $zero, 28($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
lw $t0,16($sp)
#Argument var.var10
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var10<-['Razz', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,12($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
li $v0, 9
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
sw $zero, 24($v0)
sw $zero, 28($v0)
sw $zero, 32($v0)
sw $zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
#Argument var.var11
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var11<-['Bar', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,16($a0)
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, 28
jr $ra
f6: #Main.type_name
addi $sp, $sp, -12
la $v0, st1
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f7: #Main.main
addi $sp, $sp, -12
la $v0, st2
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f8: #IO.$init
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
f9: #IO.type_name
addi $sp, $sp, -12
la $v0, st3
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f10: #IO.out_string
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
f11: #IO.out_int
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
f12: #IO.in_string
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
f13: #IO.in_int
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
f14: #String.$init
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
jal $t0 #var.var22<-['Object', '$init']
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
f15: #String.type_name
addi $sp, $sp, -12
la $v0, st4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f16: #String.Length
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
f17: #String.Concat
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
f18: #String.Substring
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
f19: #Bool.$init
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
jal $t0 #var.var27<-['Object', '$init']
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
f20: #Bool.type_name
addi $sp, $sp, -12
la $v0, st5
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f21: #Bazz.$init
addi $sp, $sp, -156
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var32<-['IO', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
la $t1,Barclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,32($sp)
lw $t0,32($sp)
seq $v0, $t0, $zero
sw $v0,36($sp)
lw $t0,36($sp)
bgtz $t0, var.var40
lw $t0,28($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,16($sp)
b var.var36
var.var40:
lw $t0,12($sp)
la $t1,Razzclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,60($sp)
lw $t0,60($sp)
seq $v0, $t0, $zero
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, var.var47
lw $t0,28($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
li $v0, 9
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
sw $zero, 24($v0)
sw $zero, 28($v0)
sw $zero, 32($v0)
sw $zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
lw $t0,76($sp)
#Argument var.var49
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var49<-['Bar', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,16($sp)
b var.var36
var.var47:
lw $t0,12($sp)
la $t1,Fooclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,88($sp)
lw $t0,88($sp)
seq $v0, $t0, $zero
sw $v0,92($sp)
lw $t0,92($sp)
bgtz $t0, var.var54
lw $t0,28($sp)
move $v0, $t0
sw $v0,100($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,32
li $v0, 9
syscall
la $t0, Razzclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
sw $zero, 24($v0)
sw $zero, 28($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,104($sp)
lw $t0,104($sp)
#Argument var.var56
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var56<-['Razz', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,16($sp)
b var.var36
var.var54:
lw $t0,12($sp)
la $t1,Bazzclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,116($sp)
lw $t0,116($sp)
seq $v0, $t0, $zero
sw $v0,120($sp)
lw $t0,120($sp)
bgtz $t0, var.var61
lw $t0,28($sp)
move $v0, $t0
sw $v0,128($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,24
li $v0, 9
syscall
la $t0, Fooclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,132($sp)
lw $t0,132($sp)
#Argument var.var63
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var63<-['Foo', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,16($sp)
b var.var36
var.var61:
var.var36:
lw $t0,16($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
#Argument var.var66
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var67<-['Bazz', 'printh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,148($sp)
lw $t0,148($sp)
move $v0, $t0
sw $v0,12($a0)
move $t0,$a0
move $v0, $t0
sw $v0,152($sp)
addi $sp, $sp, 156
jr $ra
f22: #Bazz.type_name
addi $sp, $sp, -12
la $v0, st6
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f23: #Bazz.printh
addi $sp, $sp, -20
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
#Argument var.var70
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
#Argument var.var71
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var72<-['Bazz', 'out_int']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,12($sp)
li $t0,0
move $v0, $t0
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f24: #Bazz.doh
addi $sp, $sp, -48
lw $t0,4($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,4($a0)
move $v0, $t0
sw $v0,20($sp)
li $t0,1
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
lw $t1,24($sp)
add $v0, $t0, $t1
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,4($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
addi $sp, $sp, 48
jr $ra
f25: #Foo.$init
addi $sp, $sp, -172
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bazzclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var85<-['Bazz', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
la $t1,Barclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,28($sp)
lw $t0,28($sp)
seq $v0, $t0, $zero
sw $v0,32($sp)
lw $t0,32($sp)
bgtz $t0, var.var92
lw $t0,24($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,12($sp)
b var.var88
var.var92:
lw $t0,8($sp)
la $t1,Razzclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,56($sp)
lw $t0,56($sp)
seq $v0, $t0, $zero
sw $v0,60($sp)
lw $t0,60($sp)
bgtz $t0, var.var99
lw $t0,24($sp)
move $v0, $t0
sw $v0,68($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
li $v0, 9
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
sw $zero, 24($v0)
sw $zero, 28($v0)
sw $zero, 32($v0)
sw $zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,72($sp)
lw $t0,72($sp)
#Argument var.var101
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var101<-['Bar', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,76($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,12($sp)
b var.var88
var.var99:
lw $t0,8($sp)
la $t1,Fooclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,84($sp)
lw $t0,84($sp)
seq $v0, $t0, $zero
sw $v0,88($sp)
lw $t0,88($sp)
bgtz $t0, var.var106
lw $t0,24($sp)
move $v0, $t0
sw $v0,96($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,32
li $v0, 9
syscall
la $t0, Razzclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
sw $zero, 24($v0)
sw $zero, 28($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,100($sp)
lw $t0,100($sp)
#Argument var.var108
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var108<-['Razz', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,12($sp)
b var.var88
var.var106:
var.var88:
lw $t0,12($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,16($a0)
lw $t0,16($a0)
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
#Argument var.var111
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var112<-['Razz', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,116($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
#Argument var.var113
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var114<-['Foo', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,124($sp)
lw $t0,116($sp)
lw $t1,124($sp)
add $v0, $t0, $t1
sw $v0,132($sp)
move $t0,$a0
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
#Argument var.var117
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var118<-['Foo', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,140($sp)
lw $t0,132($sp)
lw $t1,140($sp)
add $v0, $t0, $t1
sw $v0,148($sp)
move $t0,$a0
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
#Argument var.var121
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var122<-['Foo', 'printh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,156($sp)
lw $t0,148($sp)
lw $t1,156($sp)
add $v0, $t0, $t1
sw $v0,164($sp)
lw $t0,164($sp)
move $v0, $t0
sw $v0,20($a0)
move $t0,$a0
move $v0, $t0
sw $v0,168($sp)
addi $sp, $sp, 172
jr $ra
f26: #Foo.type_name
addi $sp, $sp, -12
la $v0, st7
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f27: #Foo.doh
addi $sp, $sp, -48
lw $t0,4($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,4($a0)
move $v0, $t0
sw $v0,20($sp)
li $t0,2
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
lw $t1,24($sp)
add $v0, $t0, $t1
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,4($a0)
lw $t0,12($a0)
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,12($a0)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
addi $sp, $sp, 48
jr $ra
f28: #Razz.$init
addi $sp, $sp, -160
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Fooclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var138<-['Foo', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
la $t1,Barclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,28($sp)
lw $t0,28($sp)
seq $v0, $t0, $zero
sw $v0,32($sp)
lw $t0,32($sp)
bgtz $t0, var.var145
lw $t0,24($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,12($sp)
b var.var141
var.var145:
lw $t0,8($sp)
la $t1,Razzclase
addi $sp ,$sp, -4
sw $ra, 0($sp)
jal .TypeCheck
lw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,56($sp)
lw $t0,56($sp)
seq $v0, $t0, $zero
sw $v0,60($sp)
lw $t0,60($sp)
bgtz $t0, var.var152
lw $t0,24($sp)
move $v0, $t0
sw $v0,68($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
li $v0, 9
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
sw $zero, 20($v0)
sw $zero, 24($v0)
sw $zero, 28($v0)
sw $zero, 32($v0)
sw $zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,72($sp)
lw $t0,72($sp)
#Argument var.var154
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var154<-['Bar', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,76($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,12($sp)
b var.var141
var.var152:
var.var141:
lw $t0,12($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,24($a0)
lw $t0,16($a0)
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
#Argument var.var157
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bazzclase
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var158<-['Bazz', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,88($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,92($sp)
lw $t0,92($sp)
#Argument var.var159
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var160<-['Foo', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,88($sp)
lw $t1,96($sp)
add $v0, $t0, $t1
sw $v0,104($sp)
lw $t0,24($a0)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
#Argument var.var163
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var164<-['Bar', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,112($sp)
lw $t0,104($sp)
lw $t1,112($sp)
add $v0, $t0, $t1
sw $v0,120($sp)
move $t0,$a0
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
#Argument var.var167
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var168<-['Razz', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,128($sp)
lw $t0,120($sp)
lw $t1,128($sp)
add $v0, $t0, $t1
sw $v0,136($sp)
move $t0,$a0
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
#Argument var.var171
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var172<-['Razz', 'printh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,144($sp)
lw $t0,136($sp)
lw $t1,144($sp)
add $v0, $t0, $t1
sw $v0,152($sp)
lw $t0,152($sp)
move $v0, $t0
sw $v0,28($a0)
move $t0,$a0
move $v0, $t0
sw $v0,156($sp)
addi $sp, $sp, 160
jr $ra
f29: #Razz.type_name
addi $sp, $sp, -12
la $v0, st8
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f30: #Bar.$init
addi $sp, $sp, -28
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Razzclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var179<-['Razz', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
#Argument var.var180
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var181<-['Bar', 'doh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,32($a0)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
#Argument var.var182
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var183<-['Bar', 'printh']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,36($a0)
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, 28
jr $ra
f31: #Bar.type_name
addi $sp, $sp, -12
la $v0, st9
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
