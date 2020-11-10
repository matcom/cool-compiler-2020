     .macro out_string($arg)
     li $v0, 4
     move $a0, $arg
     syscall
     .end_macro

     .macro out_int($arg)
     li $v0, 1
     move $a0, $arg
     syscall
     .end_macro

     .macro in_int()
     li $v0, 5
     syscall
     .end_macro

     .macro in_string()
     li $v0, 9
     li $a0, 1024
     syscall
     move $a0, $v0
     li $a1, 1024
     li $v0, 8
     syscall
     .end_macro

     .macro suma($arg1, $arg2, $result)
     lw $t1, $arg1
     lw $t2, $arg2
     add $v0, $t1, $t2
     sw $v0, $result
     .end_macro

     .macro resta($arg1, $arg2, $result)
     lw $t1, $arg1
     lw $t2, $arg2
     sub $v0, $t1, $t2
     sw $v0, $result
     .end_macro

     .macro multiplicacion($arg1, $arg2, $result)
     lw $t1, $arg1
     lw $t2, $arg2
     mult $t1, $t2
     mflo $v0
     sw $v0, $result
     .end_macro

     .macro division($arg1, $arg2, $result)
     lw $t1, $arg1
     lw $t2, $arg2
     div $t1, $t2
     mflo $v0
     sw $v0, $result
     .end_macro

     .macro lesser($arg1, $arg2, $result)
     lw $t1, $arg1
     lw $t2, $arg2
     blt $t1, $t2, LesserTrue
     li $v0, 0
     b LesserEnd
     LesserTrue:
     li $v0, 1
     LesserEnd:
     sw $v0, $result
     .end_macro

     .macro lesserequal($arg1, $arg2, $result)
     lw $t1, $arg1
     lw $t2, $arg2
     ble $t1, $t2, LesserEqualTrue
     li $v0, 0
     b LesserEqualEnd
     LesserEqualTrue:
     li $v0, 1
     LesserEqualEnd:
     sw $v0, $result
     .end_macro

     .macro not($arg1, $result)
     lw $t1, $arg1
     move $t2, zero
     beq $t1, $t2, FalseBool
     li $v0, 0
     b NotBool
     FalseBool:
     li $v0, 1
     NotBool:
     sw $v0, $result
     .end_macro

     .macro igual($arg1, $arg2, $result)
     lw $t1, $arg1
     lw $t2, $arg2
     beq $t1, $t2, Iguales
     li $v0, 0
     b FinalIgual
     Iguales:
     li $v0, 1
     FinalIgual:
     sw $v0, $result
     .end_macro

     .macro stringlength($arg1, $result)
     lw $t1, $arg1
     move $v0, zero
     move $t2, zero

     InicioStrLen:
     add $t0, $t1, $vo
     lb $t2, $t0
     beq $t2, zero, FinStrLen
     addi $v0, $v0, 1
     b InicioStrLen

     FinStrLen:
     sw $v0, $result
     .end_macro

     .macro abort()
     li $v0, 10
     syscall
     .end_macro