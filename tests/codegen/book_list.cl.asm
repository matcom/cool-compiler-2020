.data
st0: .asciiz "Object"
st1: .asciiz "Main"
st2: .asciiz "Compilers, Principles, Techniques, and Tools"
st3: .asciiz "Aho, Sethi, and Ullman"
st4: .asciiz "The Top 100 CD_ROMs"
st5: .asciiz "Ulanoff"
st6: .asciiz "PC Magazine"
st7: .asciiz "IO"
st8: .asciiz "String"
st9: .asciiz "Bool"
st10: .asciiz ""
st11: .asciiz ""
st12: .asciiz "Book"
st13: .asciiz "title:      "
st14: .asciiz "\n"
st15: .asciiz "author:     "
st16: .asciiz "\n"
st17: .asciiz "BookList"
st18: .asciiz ""
st19: .asciiz "Article"
st20: .asciiz "periodical:  "
st21: .asciiz "\n"
st22: .asciiz "Cons"
st23: .asciiz "- dynamic type was Article -\n"
st24: .asciiz "- dynamic type was Book -\n"
st25: .asciiz "Nil"
Objectclase: .word 0,f0,f3,f2,f4
Mainclase: .word Objectclase,f5,f6,f2,f4,f7
IOclase: .word Objectclase,f8,f9,f2,f4,f10,f11,f12,f13
Stringclase: .word Objectclase,f14,f15,f2,f4,f16,f17,f18
Boolclase: .word Objectclase,f19,f20,f2,f4
Bookclase: .word IOclase,f21,f22,f2,f4,f10,f11,f12,f13,f23,f24
BookListclase: .word IOclase,f25,f26,f2,f4,f10,f11,f12,f13,f27,f28,f29,f30,f31
Articleclase: .word Bookclase,f32,f33,f2,f4,f10,f11,f12,f13,f23,f35,f34
Consclase: .word BookListclase,f36,f37,f2,f4,f10,f11,f12,f13,f38,f28,f40,f41,f42,f39
Nilclase: .word BookListclase,f43,f44,f2,f4,f10,f11,f12,f13,f45,f28,f29,f30,f46
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
li $a0,8
li $v0, 9
syscall
la $t0, Mainclase
sw $t0, 0($v0)
sw $zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var154
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var154<-['Main', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var154
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var155<-['Main', 'main']
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
li $t0,0
move $v0, $t0
sw $v0,4($a0)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f6: #Main.type_name
addi $sp, $sp, -12
la $v0, st1
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f7: #Main.main
addi $sp, $sp, -124
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,12
li $v0, 9
syscall
la $t0, Bookclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
#Argument var.var10
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var10<-['Book', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
la $v0, st2
sw $v0,16($sp)
la $v0, st3
sw $v0,24($sp)
lw $t0,8($sp)
#Argument var.var10
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
#Argument var.var11
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,32($sp)
#Argument var.var12
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var13<-['Book', 'initBook']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,28($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,16
li $v0, 9
syscall
la $t0, Articleclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,40($sp)
lw $t0,40($sp)
#Argument var.var15
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var15<-['Article', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,40($sp)
la $v0, st4
sw $v0,48($sp)
la $v0, st5
sw $v0,56($sp)
la $v0, st6
sw $v0,64($sp)
lw $t0,40($sp)
#Argument var.var15
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
#Argument var.var16
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,64($sp)
#Argument var.var17
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0,76($sp)
#Argument var.var18
addi $sp, $sp, -4
sw $a3, 0($sp)
move $a3,$t0
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var19<-['Article', 'initArticle']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a3, 0($sp)
lw $a2, 4($sp)
lw $a1, 8($sp)
lw $a0, 12($sp)
addi $sp, $sp, 16
sw $v0,68($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
li $v0, 9
syscall
la $t0, Nilclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,80($sp)
lw $t0,80($sp)
#Argument var.var21
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var21<-['Nil', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,80($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
#Argument var.var21
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,88($sp)
#Argument var.var22
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var23<-['Nil', 'cons']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,88($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,92($sp)
lw $t0,88($sp)
#Argument var.var23
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var24
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var25<-['Cons', 'cons']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,4($a0)
lw $t0,4($a0)
move $v0, $t0
sw $v0,100($sp)
lw $t0,100($sp)
#Argument var.var26
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var27<-['BookList', 'print_list']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
addi $sp, $sp, 124
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
jal $t0 #var.var34<-['Object', '$init']
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
la $v0, st7
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
jal $t0 #var.var39<-['Object', '$init']
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
la $v0, st8
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
jal $t0 #var.var44<-['Object', '$init']
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
la $v0, st9
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f21: #Book.$init
addi $sp, $sp, -28
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var49<-['IO', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
la $v0, st10
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($a0)
la $v0, st11
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, 28
jr $ra
f22: #Book.type_name
addi $sp, $sp, -12
la $v0, st12
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f23: #Book.initBook
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
f24: #Book.print
addi $sp, $sp, -80
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
la $v0, st13
sw $v0,12($sp)
lw $t0,4($sp)
#Argument var.var57
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
#Argument var.var58
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var59<-['Book', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,16($sp)
lw $t0,4($a0)
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
#Argument var.var59
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
#Argument var.var60
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var61<-['Book', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,24($sp)
la $v0, st14
sw $v0,32($sp)
lw $t0,24($sp)
#Argument var.var61
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
#Argument var.var62
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var63<-['Book', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,36($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
la $v0, st15
sw $v0,48($sp)
lw $t0,40($sp)
#Argument var.var64
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
#Argument var.var65
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var66<-['Book', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
#Argument var.var66
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
#Argument var.var67
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var68<-['Book', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,60($sp)
la $v0, st16
sw $v0,68($sp)
lw $t0,60($sp)
#Argument var.var68
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
#Argument var.var69
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var70<-['Book', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,72($sp)
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
addi $sp, $sp, 80
jr $ra
f25: #BookList.$init
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
jal $t0 #var.var74<-['IO', '$init']
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
f26: #BookList.type_name
addi $sp, $sp, -12
la $v0, st17
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f27: #BookList.isNil
addi $sp, $sp, -16
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var77
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var78<-['BookList', 'abort']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
li $t0,1
move $v0, $t0
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f28: #BookList.cons
addi $sp, $sp, -40
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,12
li $v0, 9
syscall
la $t0, Consclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
#Argument var.var80
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var80<-['Cons', '$init']
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
lw $t0,4($sp)
move $v0, $t0
sw $v0,16($sp)
move $t0,$a1
move $v0, $t0
sw $v0,20($sp)
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
lw $t0,16($sp)
#Argument var.var82
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
#Argument var.var83
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,32($sp)
#Argument var.var84
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var85<-['Cons', 'init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,36($sp)
addi $sp, $sp, 40
jr $ra
f29: #BookList.car
addi $sp, $sp, -16
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var88
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var89<-['BookList', 'abort']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,12
li $v0, 9
syscall
la $t0, Bookclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
#Argument var.var90
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var90<-['Book', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f30: #BookList.cdr
addi $sp, $sp, -16
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var91
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var92<-['BookList', 'abort']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
li $v0, 9
syscall
la $t0, BookListclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
#Argument var.var93
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var93<-['BookList', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
addi $sp, $sp, 16
jr $ra
f31: #BookList.print_list
addi $sp, $sp, -12
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var94
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,12($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var95<-['BookList', 'abort']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f32: #Article.$init
addi $sp, $sp, -20
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bookclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var98<-['Book', '$init']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
la $v0, st18
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,12($a0)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
addi $sp, $sp, 20
jr $ra
f33: #Article.type_name
addi $sp, $sp, -12
la $v0, st19
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f34: #Article.initArticle
addi $sp, $sp, -32
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
move $t0,$a2
move $v0, $t0
sw $v0,12($sp)
lw $t0,4($sp)
#Argument var.var102
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
#Argument var.var103
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0,20($sp)
#Argument var.var104
addi $sp, $sp, -4
sw $a2, 0($sp)
move $a2,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var105<-['Article', 'initBook']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a2, 0($sp)
lw $a1, 4($sp)
lw $a0, 8($sp)
addi $sp, $sp, 12
sw $v0,16($sp)
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
f35: #Article.print
addi $sp, $sp, -52
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var108
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bookclase
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var109<-['Book', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
la $v0, st20
sw $v0,20($sp)
lw $t0,12($sp)
#Argument var.var110
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
#Argument var.var111
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var112<-['Article', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,24($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,28($sp)
lw $t0,24($sp)
#Argument var.var112
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,32($sp)
#Argument var.var113
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var114<-['Article', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,32($sp)
la $v0, st21
sw $v0,40($sp)
lw $t0,32($sp)
#Argument var.var114
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
#Argument var.var115
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var116<-['Article', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
addi $sp, $sp, 52
jr $ra
f36: #Cons.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,BookListclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var120<-['BookList', '$init']
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
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f37: #Cons.type_name
addi $sp, $sp, -12
la $v0, st22
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f38: #Cons.isNil
addi $sp, $sp, -8
move $t0, $zero
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f39: #Cons.init
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
f40: #Cons.car
addi $sp, $sp, -8
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f41: #Cons.cdr
addi $sp, $sp, -8
lw $t0,8($a0)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f42: #Cons.print_list
addi $sp, $sp, -116
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
#Argument var.var129
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var130<-['Book', 'print']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
la $t1,Articleclase
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
bgtz $t0, var.var136
lw $t0,24($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
move $t0,$a0
move $v0, $t0
sw $v0,44($sp)
la $v0, st23
sw $v0,52($sp)
lw $t0,44($sp)
#Argument var.var138
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
#Argument var.var139
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var140<-['Cons', 'out_string']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a1, 0($sp)
lw $a0, 4($sp)
addi $sp, $sp, 8
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,12($sp)
b var.var132
var.var136:
lw $t0,8($sp)
la $t1,Bookclase
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
bgtz $t0, var.var145
lw $t0,24($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
la $v0, st24
sw $v0,92($sp)
lw $t0,84($sp)
#Argument var.var147
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
#Argument var.var148
addi $sp, $sp, -4
sw $a1, 0($sp)
move $a1,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var149<-['Cons', 'out_string']
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
sw $v0,24($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,12($sp)
b var.var132
var.var145:
var.var132:
lw $t0,12($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
#Argument var.var152
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $ra,$t0 #var.var153<-['BookList', 'print_list']
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,112($sp)
addi $sp, $sp, 116
jr $ra
f43: #Nil.$init
addi $sp, $sp, -12
move $t0,$a0
#Argument self
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,BookListclase
lw $t0,4($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0 #var.var156<-['BookList', '$init']
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
f44: #Nil.type_name
addi $sp, $sp, -12
la $v0, st25
sw $v0,8($sp)
addi $sp, $sp, 12
jr $ra
f45: #Nil.isNil
addi $sp, $sp, -8
li $t0,1
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
f46: #Nil.print_list
addi $sp, $sp, -8
li $t0,1
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, 8
jr $ra
