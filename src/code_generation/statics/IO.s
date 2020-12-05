IO.out_string:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
li $v0, 4
lw $a0, 8($sp)
syscall
lw $ra, 4($sp)
addiu $sp, $sp, 12
lw $fp, 0($sp)
jr $ra


IO.out_int:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
li $v0, 1
lw $a0, 8($sp)
syscall
lw $ra, 4($sp)
addiu $sp, $sp, 12
lw $fp, 0($sp)
jr $ra


IO.in_string:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
la $a0, buffer
li $a1, 1024
li $v0, 8
syscall
sw $fp, 0($sp)
addiu $sp, $sp, -4
sw $a0, 0($sp)
addiu $sp, $sp, -4
jal String.length
addiu $a0, $a0, 1
li $v0, 9
syscall
move $t0, $v0
la $a0, buffer
istr_copy:
lb $t1, ($a0)
sb $t1, ($t0)
addiu $a0, $a0, 1
addiu $t0, $t0, 1
bne $t1, $zero, istr_copy
addiu $t0, $t0, -2
li $t1 10
lb $t2, ($t0)
bne $t1 , $t2 not_slash
sb $zero, ($t0)
not_slash:
move $a0, $v0
lw $ra, 4($fp)
addiu $sp, $sp, 8
lw $fp, 0($sp)
jr $ra 


IO.in_int:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
lw $a0, 4($fp)
li $v0, 5
syscall
move $a0, $v0
lw $ra, 4($fp)
addiu $sp, $sp, 8
lw $fp, 0($sp)
jr $ra 