Object.copy:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
lw $a1, -4($sp)
lw $a0, -8($sp)
li $v0, 9
syscall
lw $a1, -4($sp)
lw $a0, 4($a1)
move $a3, $v0
_copy.loop:
lw $a2, 0($a1)
sw $a2, 0($a3)
addiu $a0, $a0, -1
addiu $a1, $a1, 4
addiu $a3, $a3, 4
beq $a0, $zero, _copy.end
j _copy.loop
_copy.end:
lw $ra, 8($sp)
addiu $sp, $sp, 12
lw $fp, 0($sp)
jr $ra


Object.abort:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
li $v0, 10
syscall
lw $ra, 4($sp)
addiu $sp, $sp, 8
lw $fp, 0($sp)
jr $ra
