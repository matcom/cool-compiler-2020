Object.copy:
addi $sp, $sp, -4
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $t0, 8($sp)
lw $a0, 8($t0)
li $v0, 9
syscall
# bge $v0, $sp heap_error
move $t1, $v0
li $a0, 0
copy_object_word:
lw $t2, ($t0)
sw $t2, ($t1)
addi $t0, $t0, 4
addi $t1, $t1, 4
addi $a0, $a0, 4
lw $t3, 8($t0)
blt $a0, $t3, copy_object_word
sw $v0, 4($sp)
lw $a1, 4($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra

Object.abort:
addi $sp, $sp, -4
addi $sp, $sp, -4
sw $ra, 0($sp)
la $t0, s_0
sw $t0, 4($sp)
lw $a0, 4($sp)
li $v0, 4
syscall
li $v0, 10
syscall
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra

Object.type_name:
