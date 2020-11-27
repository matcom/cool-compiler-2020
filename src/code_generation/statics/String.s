
String.length:
addi $sp, $sp, -12
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $t0, 16($sp)
li $a0, 0
count_char:
lb $t1, ($t0)
beqz $t1, finish_chars_count
addi $t0, $t0, 1
addi $a0, $a0, 1
j count_char
finish_chars_count:
sw $a0, 4($sp)
li $a0, 20
li $v0, 9
syscall
# bge $v0, $sp heap_error
move $t0, $v0
li $t1, 1
sw $t1, 0($t0)
la $t1, Int_name
sw $t1, 4($t0)
li $t1, 5
sw $t1, 8($t0)
la $t1, IO_VT
sw $t1, 12($t0)
sw $t0, 8($sp)
move $t0, $sp
lw $t1, 4($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
lw $t1, 8($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
jal IO_VT
sw $a1, 12($sp)
lw $a1, 4($sp)
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra


String.concat:
addi $sp, $sp, -28
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $t0, 32($sp)
lw $t1, 16($t0)
sw $t1, 4($sp)
move $t0, $sp
lw $t1, 4($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
jal String.length
sw $a1, 8($sp)
lw $t0, 36($sp)
lw $t1, 16($t0)
sw $t1, 12($sp)
move $t0, $sp
lw $t1, 12($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
jal String.length
sw $a1, 16($sp)
lw $a0, 8($sp)
lw $t0, 16($sp)
add $a0, $a0, $t0
addi $a0, $a0, 1
li $v0, 9
syscall
# bge $v0, $sp heap_error
lw $t0, 4($sp)
lw $t1, 12($sp)
copy_str1_char:
lb $t2, ($t0)
sb $t2, ($v0)
beqz $t2, concat_str2_char
addi $t0, $t0, 1
addi $v0, $v0, 1
j copy_str1_char
concat_str2_char:
lb $t2, ($t0)
sb $t2, ($v0)
beqz $t2, finish_str2_concat
addi $t1, $t1, 1
addi $v0, $v0, 1
j concat_str2_char
finish_str2_concat:
sb $0, ($v0)
sw $v0, 20($sp)
li $a0, 20
li $v0, 9
syscall
# bge $v0, $sp heap_error
move $t0, $v0
li $t1, 1
sw $t1, 0($t0)
# la $t1, String_name
sw $t1, 4($t0)
li $t1, 5
sw $t1, 8($t0)
la $t1, String_VT
sw $t1, 12($t0)
sw $t0, 24($sp)
move $t0, $sp
lw $t1, 20($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
lw $t1, 24($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
jal String.Constructor
sw $a1, 28($sp)
lw $a1, 24($sp)
lw $ra, 0($sp)
addi $sp, $sp, 40
jr $ra


String.substr:
addi $sp, $sp, -20
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $t0, 28($sp)
lw $t1, 16($t0)
sw $t1, 4($sp)
lw $t0, 32($sp)
lw $t1, 16($t0)
sw $t1, 8($sp)
lw $a0, 8($sp)
addi $a0, $a0, 1
li $v0, 9
syscall
# bge $v0, $sp heap_error
lw $t0, 4($sp)
lw $t1, 8($sp)
lw $t2, 24($sp)
bltz $t0, strsubstrexception
li $a0, 0
jump_str_char:
beq $a0, $t0, finish_index_jump
addi $a0, $a0, 1
addi $t2, $t2, 1
beq $t2, $zero, strsubstrexception
j jump_str_char
finish_index_jump:
li $a0, 0
copy_substr_char:
beq $a0, $t1 finish_substr_copy
lb $t0, ($t2)
sb $t0, ($v0)
addi $t2, $t2, 1
beq $t2, $zero, strsubstrexception
addi $v0, $v0, 1
addi $a0, $a0, 1
j copy_substr_char
finish_substr_copy:
sb $0, ($v0)
sw $v0, 12($sp)
li $a0, 20
li $v0, 9
syscall
# bge $v0, $sp heap_error
move $t0, $v0
li $t1, 1
sw $t1, 0($t0)
# la $t1, String_name
sw $t1, 4($t0)
li $t1, 5
sw $t1, 8($t0)
la $t1, String_VT
sw $t1, 12($t0)
sw $t0, 16($sp)
move $t0, $sp
lw $t1, 12($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
lw $t1, 16($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
jal String.Constructor
sw $a1, 20($sp)
lw $a1, 16($sp)
lw $ra, 0($sp)
addi $sp, $sp, 36
jr $ra



_substrexception:
la $a0, strsubstrexception
li $v0, 4
syscall
li $v0, 10
syscall


_stringcmp:
li $v0, 1
_stringcmp.loop:
lb $a2, 0($a0)
lb $a3, 0($a1)
beqz $a2, _stringcmp.end
beq $a2, $zero, _stringcmp.end
beq $a3, $zero, _stringcmp.end
bne $a2, $a3, _stringcmp.differents
addiu $a0, $a0, 1
addiu $a1, $a1, 1
j _stringcmp.loop
_stringcmp.end:
beq $a2, $a3, _stringcmp.equals
_stringcmp.differents:
li $v0, 0
jr $ra
_stringcmp.equals:
li $v0, 1
jr $ra