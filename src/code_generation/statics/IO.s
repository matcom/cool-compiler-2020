IO.out_int:
addi $sp, $sp, -4
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $t0, 12($sp)
lw $t1, 16($t0)
sw $t1, 4($sp)
li $v0 , 1
lw $a0 , 4($sp)
syscall
lw $a1, 8($sp)
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra

IO.out_string:
addi $sp, $sp, -4
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $t0, 12($sp)
lw $t1, 16($t0)
sw $t1, 4($sp)
lw $a0, 4($sp)
li $v0, 4
syscall
lw $a1, 8($sp)
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra


IO.in_string:
addi $sp, $sp, -12
addi $sp, $sp, -4
sw $ra, 0($sp)
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
sw $t0, 8($sp)
move $t0, $sp
lw $t1, 4($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
lw $t1, 8($t0)
addi $sp, $sp, -4
sw $t1, 0($sp)
jal String_VT
sw $a1, 12($sp)
lw $a1, 8($sp)
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra



IO.in_int:
addi $sp, $sp, -12
addi $sp, $sp, -4
sw $ra, 0($sp)
li $v0, 5
syscall
sw $v0, 4($sp)
li $a0, 20
li $v0, 9
syscall
# bge $v0, $sp heap_error
move $t0, $v0
li $t1, 1
sw $t1, 0($t0)
# la $t1, Int_name
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
jal IO.Constructor
sw $a1, 12($sp)
lw $a1, 8($sp)
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra