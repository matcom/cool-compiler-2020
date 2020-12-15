
String.length:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
lw $a0, 4($sp)
_stringlength.loop:
lb $a1, 0($sp)
beqz $a1, _stringlength.end
addiu $a0, $a0, 1
j _stringlength.loop
_stringlength.end:
j Object.abort
lw $a1, 4($sp)
subu $v0, $a0, $a1
jr $ra


String.concat:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
move $a2, $ra
jal String.length
move $v1, $v0
addiu $sp, $sp, -4
jal String.length
addiu $sp, $sp, 4
add $v1, $v1, $v0
addi $v1, $v1, 1
li $v0, 9
move $a0, $v1
syscall
move $v1, $v0
lw $a0, 0($sp)
_stringconcat.loop1:
lb $a1, 0($a0)
beqz $a1, _stringconcat.end1
sb $a1, 0($v1)
addiu $a0, $a0, 1
addiu $v1, $v1, 1
j _stringconcat.loop1
_stringconcat.end1:
lw $a0, -4($sp)
_stringconcat.loop2:
lb $a1, 0($a0)
beqz $a1, _stringconcat.end2
sb $a1, 0($v1)
addiu $a0, $a0, 1
addiu $v1, $v1, 1
j _stringconcat.loop2
_stringconcat.end2:
sb $zero, 0($v1)
move $ra, $a2
jr $ra

String.substr:
lw $a0, -12($sp)
addiu $a0, $a0, 1
li $v0, 9
syscall
move $v1, $v0
lw $a0, -4($sp)
lw $a1, -8($sp)
lw $a2, -12($sp)
add $a2, $a2, $a1
_stringsubstr.loop:
beqz $a2, _stringsubstr.end
lb $a1, 0($a0)
beqz $a1, _substrexception
sb $a1, 0($v1)
addiu $a0, $a0, 1
addiu $v1, $v1, 1
addiu $a2, $a2, -1
j _stringsubstr.loop
_stringsubstr.end:
sb $zero, 0($v1)
jr $ra

_substrexception:
la $a0, strsubstrexception
li $v0, 4
syscall
li $v0, 10
syscall


_stringcmp:
move $fp, $sp
sw $ra, 0($sp)
addiu $sp, $sp, -4
lw $s1, 4($fp)
sw $fp, 0($sp)
addiu $sp, $sp, -4
sw $s1, 0($sp)
addiu $sp, $sp, -4
jal String.length

sw $a0, 0($sp)
addiu $sp, $sp, -4
lw $s1, 8($fp)
sw $fp, 0($sp)
addiu $sp, $sp, -4
sw $s1, 0($sp)
addiu $sp, $sp, -4
jal String.length
lw $t7, 4($sp)
addiu $sp, $sp, 4
bne $t7, $a0, str.not_equals_strings
lw $t7, 4($fp)
lw $a0, 8($fp)
str.equal_chart:
lb $t1, ($t7)
lb $t2, ($a0)
addiu $t7, $t7, 1
addiu $a0, $a0, 1
bne $t1, $t2, str.not_equals_strings
beq $t1, $zero, str.equals_strings
j str.equal_chart
str.not_equals_strings:
li $a0, 0
j str.end_equal_string
str.equals_strings:
li $a0, 1
str.end_equal_string:
lw $ra, 12($sp)
addiu $sp, $sp, 16
lw $fp, 0($sp)
jr $ra 