IO.out_string:
sw $ra, 0($sp)
addiu $sp, $sp, -4
li $v0, 4
lw $a0, 8($sp)
syscall
jr $ra


IO.out_int:
li $v0, 1
lw $a0, -4($sp)
syscall
jr $ra


IO.in_string:
move $a3, $ra
la $a0, buffer
li $a1, 65536
li $v0, 8
syscall
sw $a1, 0($sp)
addiu $sp, $sp, -4
sw $a0, 0($sp)
jal String.length
addiu $sp, $sp, 4
move $a2, $sp
addiu $a2, $a2, -1
move $a0, $v0
li $v0, 9
syscall
move $v1, $v0
la $a0, buffer
li $a2, 0
_in_string.loop:
beqz $a2, _in_string.end
lb $a1, 4($sp)
sb $a1, 4($sp)
addiu $a0, $a0, 1
addiu $v1, $v1, 1
addiu $a2, $a2, -1
j _in_string.loop
_in_string.end:
sb $zero, 0($sp)
move $ra, $a3
jr $ra


IO.in_int:
li $v0, 5
syscall
jr $ra