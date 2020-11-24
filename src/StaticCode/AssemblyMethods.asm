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
     sw $v0, $a0
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
     sw $s1, $s0
     jr $ra

     #Los numeros como argumentos $a0 y $a1, y $a2 como donde guardar el resultado
     .Int.suma:
     lw $t1, $a0
     lw $t2, $a1
     add $v0, $t1, $t2
     sw $v0, $a2
     jr $ra

     .Int.resta:
     lw $t1, $a0
     lw $t2, $a1
     sub $v0, $t1, $t2
     sw $v0, $a2
     jr $ra

     .Int.multiplicacion:
     lw $t1, $a0
     lw $t2, $a1
     mult $t1, $t2
     mflo $v0
     sw $v0, $a2
     jr $ra

     .Int.division:
     lw $t1, $a0
     lw $t2, $a1
     div $t1, $t2
     mflo $v0
     sw $v0, $a2
     jr $ra

     .Int.lesser:
     lw $t1, $a0
     lw $t2, $a1
     blt $t1, $t2, LesserTrue
     move $v0, zero
     b LesserEnd
     LesserTrue:
     li $v0, 1
     LesserEnd:
     sw $v0, $a2
     jr $ra

     .Int.lesserequal:
     lw $t1, $a0
     lw $t2, $a1
     ble $t1, $t2, LesserEqualTrue
     li $v0, 0
     b LesserEqualEnd
     LesserEqualTrue:
     li $v0, 1
     LesserEqualEnd:
     sw $v0, $a2
     jr $ra

     .Int.not:
     lw $t1, $a0
     move $t2, zero
     beq $t1, $t2, FalseBool
     li $v0, 0
     b NotBool
     FalseBool:
     li $v0, 1
     NotBool:
     sw $v0, $a1
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
     sw $v0, $a2
     jr $ra

     .Str.stringlength:
     lw $t1, $a0
     move $v0, zero
     move $t2, zero

     InicioStrLen:
     add $t0, $t1, $vo
     lb $t2, $t0
     beq $t2, zero, FinStrLen
     addi $v0, $v0, 1
     b InicioStrLen

     FinStrLen:
     sw $v0, $a1
     jr $ra

     .Object.abort:
     li $v0, 10
     syscall
     jr $ra

     .Str.stringcomparison:
     lw $t1, $a0
     lw $t2, $a1
     move $v0, zero
     move $t3, zero
     move $t4, zero
     move $v0, zero

     StrCompCiclo:
     add $t0, $t1, $v0
     lb $t3, $to
     add $t0, $t2, $v0
     lb $t4, $to
     bne $t3, $t4, StrDiferentes
     beq $t3, zero, StrIguales
     b StrCompCiclo

     StrDiferentes:
     li $v0, 1
     StrIguales:
     sw $v0, $a2
     jr $ra

     .Str.stringconcat:
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
     
     move $a1, 0($sp)

     #Obteniendo el lenght de la nueva cadena
     jal .Str.stringlength
     move $s4, $v0
     move $a0, $s1
     move $a1, $sp
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
     move $t2, zero
     move $t3, zero
     
     StrCicloCopia:
     lb $t2, $t1
     addi $t1, 1
     addi $t0, 1
     
     bne $t2, zero, StrCicloCopia
     sb $t2, $t0

     bne $t3, zero, StrFinCopia
     move $t1, $s1

     b StrCicloCopia

     StrFinCopia:
     sb zero, $t0

     #sw $v0, $s2

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
     blt $a1, zero, SubStrWrongIndex

     addi $sp, $sp, -20
     
     sw  $s0 4($sp)
     sw  $s1 8($sp)
     sw  $s2 12($sp)
     sw  $s3 16$sp)

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
     move $t2, zero

     StrInicioCopiaSubStr:
     lb $t3, $t1
     sb $t3, $t0
     addi $t0, $t0, 1
     addi $t1, $t0, 1
     addi $t2, $t2, 1
     ble $t2, $s1, StrInicioCopiaSubStr

     sb zero, $t0
     
     sw $v0, $s2

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
     beq $s1, zero, $finciclocopia
     lw $t0, $s0
     sw $t0, $t1
     addi $s0, 4
     addi $t1, 4
     addi $s1, -1
     b $ciclocopia
     $finciclocopia:
     lw $s0, 0($sp)
     lw $s1, 4($sp)
     addi $sp, 8
     jr $ra