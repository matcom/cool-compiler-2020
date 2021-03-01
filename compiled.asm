	.data
data_1: .asciiz "Object"
data_2: .asciiz "IO"
data_3: .asciiz "String"
data_4: .asciiz "Int"
data_5: .asciiz "A"
data_6: .asciiz "Main"
data_7: .asciiz "Program aborted"
data_8: .asciiz "Dispatch on void"
data_9: .asciiz "Case on void"
data_10: .asciiz "Execution of a case statement without a matching branch"
data_11: .asciiz "Division by zero"
data_12: .asciiz "Substring out of range"
data_13: .asciiz "n"

type_name_table:
	.word	data_1
	.word	data_2
	.word	data_3
	.word	data_4
	.word	data_5
	.word	data_6

proto_table:
	.word	type_1_proto
	.word	type_2_proto
	.word	type_3_proto
	.word	type_4_proto
	.word	type_5_proto
	.word	type_6_proto

type_1_dispatch:
	.word	 L_1
	.word	 L_2
	.word	 L_3
	.word	 L_4

type_1_proto:
	.word	0
	.word	4
	.word	type_1_dispatch
	.word	-1

type_2_dispatch:
	.word	 L_5
	.word	 L_6
	.word	 L_7
	.word	 L_8
	.word	 L_9

type_2_proto:
	.word	1
	.word	4
	.word	type_2_dispatch
	.word	-1

type_3_dispatch:
	.word	 L_10
	.word	 L_11
	.word	 L_12
	.word	 L_13

type_3_proto:
	.word	2
	.word	6
	.word	type_3_dispatch
	.word	0
	.word	0
	.word	-1

type_4_dispatch:
	.word	 L_14

type_4_proto:
	.word	3
	.word	5
	.word	type_4_dispatch
	.word	0
	.word	-1

type_5_dispatch:
	.word	 L_2
	.word	 L_3
	.word	 L_4
	.word	 L_15
	.word	 L_16
	.word	 L_17
	.word	 L_18
	.word	 L_19

type_5_proto:
	.word	4
	.word	7
	.word	type_5_dispatch
	.word	0
	.word	0
	.word	0
	.word	-1

type_6_dispatch:
	.word	 L_2
	.word	 L_3
	.word	 L_4
	.word	 L_6
	.word	 L_7
	.word	 L_8
	.word	 L_9
	.word	 L_21

type_6_proto:
	.word	5
	.word	4
	.word	type_6_dispatch
	.word	-1
	.text
	.globl main
main:
	jal mem_manager_init
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	li $t0, 5
	sll $t0 $t0 2
	la $t1, proto_table
	addu $t1 $t1 $t0
	lw $t1, 0($t1)
	lw $a0, 4($t1)
	sll $a0 $a0 2
	jal malloc
	move $a2 $a0
	move $a0 $t1
	move $a1 $v0
	jal copy
	sw $v0, -12($fp)
	lw $t0, -12($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_21
	sw $v0, -8($fp)
	addi $sp, $sp, 4
	li $v0, 0
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	li $v0, 10
	syscall
L_1:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	li $t0, 0
	sll $t0 $t0 2
	la $t1, proto_table
	addu $t1 $t1 $t0
	lw $t1, 0($t1)
	lw $a0, 4($t1)
	sll $a0 $a0 2
	jal malloc
	move $a2 $a0
	move $a0 $t1
	move $a1 $v0
	jal copy
	sw $v0, -8($fp)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_2:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	la $t0, data_7 + 0
	sw $t0, -8($fp)
	li $v0, 4
	lw $a0, -8($fp)
	syscall
	li $v0, 10
	syscall
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_3:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	lw $t0, 0($fp)
	lw $t0, 0($t0)
	sll $t0 $t0 2
	la $t1, type_name_table
	addu $t0 $t0 $t1
	lw $t0, 0($t0)
	sw $t0, -8($fp)
	lw $t0, -8($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_10
	sw $v0, -12($fp)
	addi $sp, $sp, 4
	lw $v0, -12($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_4:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	lw $t0, 0($fp)
	lw $a0, 4($t0)
	jal malloc
	move $a2 $a0
	move $a0 $t0
	move $a1 $v0
	jal copy
	sw $v0, -8($fp)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_5:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	li $t0, 0
	sll $t0 $t0 2
	la $t1, proto_table
	addu $t1 $t1 $t0
	lw $t1, 0($t1)
	lw $a0, 4($t1)
	sll $a0 $a0 2
	jal malloc
	move $a2 $a0
	move $a0 $t1
	move $a1 $v0
	jal copy
	sw $v0, -8($fp)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_6:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	lw $t0, 0($fp)
	lw $t0, 12($t0)
	sw $t0, -8($fp)
	li $v0, 4
	lw $a0, -8($fp)
	syscall
	lw $v0, 4($fp)
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_7:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	lw $t0, 0($fp)
	lw $t0, 12($t0)
	sw $t0, -8($fp)
	li $v0, 1
	lw $a0, -8($fp)
	syscall
	lw $v0, 4($fp)
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_8:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	jal read_str
	sw $v0, -8($fp)
	lw $t0, -8($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_10
	sw $v0, -12($fp)
	addi $sp, $sp, 4
	lw $v0, -12($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_9:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	li $v0, 5
	syscall
	sw $v0, -8($fp)
	lw $t0, -8($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_14
	sw $v0, -12($fp)
	addi $sp, $sp, 4
	lw $v0, -12($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_10:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -12
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	li $t0, 2
	sll $t0 $t0 2
	la $t1, proto_table
	addu $t1 $t1 $t0
	lw $t1, 0($t1)
	lw $a0, 4($t1)
	sll $a0 $a0 2
	jal malloc
	move $a2 $a0
	move $a0 $t1
	move $a1 $v0
	jal copy
	sw $v0, -8($fp)
	lw $t1, -8($fp)
	lw $t0, 0($fp)
	sw $t0, 12($t1)
	lw $a0, 0($fp)
	jal len
	sw $v0, -12($fp)
	lw $t0, -12($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_14
	sw $v0, -16($fp)
	addi $sp, $sp, 4
	lw $t1, -8($fp)
	lw $t0, -16($fp)
	sw $t0, 16($t1)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 12
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_11:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 0($fp)
	lw $t0, 16($t0)
	sw $t0, -8($fp)
	lw $v0, -8($fp)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_12:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $a0, 4($fp)
	lw $a1, 0($fp)
	jal concat
	sw $v0, -8($fp)
	lw $t0, -8($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_10
	sw $v0, -12($fp)
	addi $sp, $sp, 4
	lw $v0, -12($fp)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_13:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -28
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	lw $t0, 4($fp)
	lw $t0, 12($t0)
	sw $t0, -12($fp)
	lw $t0, 0($fp)
	lw $t0, 12($t0)
	sw $t0, -16($fp)
	lw $t0, 8($fp)
	lw $t0, 16($t0)
	sw $t0, -20($fp)
	lw $t0, -16($fp)
	lw $t1, -12($fp)
	add $t0 $t0 $t1
	sw $t0, -24($fp)
	lw $a0, -20($fp)
	lw $a1, -24($fp)
	jal less
	sw $v0, -28($fp)
	lw $t0, -28($fp)
	bne $t0 $zero L_23
	j L_24
	L_23:
	li $v0, 4
	la $a0, data_12
	syscall
	li $v0, 10
	syscall
	L_24:
	lw $a0, 8($fp)
	lw $a1, -12($fp)
	lw $a2, -16($fp)
	jal substr
	sw $v0, -8($fp)
	lw $t0, -8($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_10
	sw $v0, -32($fp)
	addi $sp, $sp, 4
	lw $v0, -32($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 28
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_14:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	li $t0, 3
	sll $t0 $t0 2
	la $t1, proto_table
	addu $t1 $t1 $t0
	lw $t1, 0($t1)
	lw $a0, 4($t1)
	sll $a0 $a0 2
	jal malloc
	move $a2 $a0
	move $a0 $t1
	move $a1 $v0
	jal copy
	sw $v0, -8($fp)
	lw $t1, -8($fp)
	lw $t0, 0($fp)
	sw $t0, 12($t1)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_15:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 0($fp)
	lw $t0, 12($t0)
	sw $t0, -8($fp)
	lw $v0, -8($fp)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_16:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, 0
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	lw $t1, 4($fp)
	lw $t0, 0($fp)
	sw $t0, 16($t1)
	lw $v0, 0($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 0
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_17:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 0($fp)
	lw $t0, 16($t0)
	sw $t0, -8($fp)
	lw $v0, -8($fp)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_18:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, 0
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	lw $t1, 4($fp)
	lw $t0, 0($fp)
	sw $t0, 20($t1)
	lw $v0, 0($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 0
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_19:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 0($fp)
	lw $t0, 20($t0)
	sw $t0, -8($fp)
	lw $v0, -8($fp)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_20:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	li $t0, 4
	sll $t0 $t0 2
	la $t1, proto_table
	addu $t1 $t1 $t0
	lw $t1, 0($t1)
	lw $a0, 4($t1)
	sll $a0 $a0 2
	jal malloc
	move $a2 $a0
	move $a0 $t1
	move $a1 $v0
	jal copy
	sw $v0, -8($fp)
	li $t0, 18
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_14
	sw $v0, -12($fp)
	addi $sp, $sp, 4
	lw $t1, -8($fp)
	lw $t0, -12($fp)
	sw $t0, 12($t1)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_21:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -128
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	jal L_20
	sw $v0, -16($fp)
	lw $t0, -16($fp)
	sw $t0, -12($fp)
	lw $t0, 0($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_8
	sw $v0, -24($fp)
	addi $sp, $sp, 4
	lw $t0, -24($fp)
	sw $t0, -20($fp)
	lw $t0, -20($fp)
	sw $t0, -28($fp)
	lw $t0, -12($fp)
	sw $t0, -36($fp)
	lw $a0, -36($fp)
	li $a1, 0
	jal equals
	sw $v0, -40($fp)
	lw $t0, -40($fp)
	bne $t0 $zero L_25
	j L_26
	L_25:
	li $v0, 4
	la $a0, data_8
	syscall
	li $v0, 10
	syscall
	L_26:
	lw $t0, -36($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -28($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -36($fp)
	lw $t0, 0($t0)
	sw $t0, -44($fp)
	la $t0, proto_table
	lw $t1, -44($fp)
	sll $t1 $t1 2
	addu $t0 $t0 $t1
	lw $t0, 0($t0)
	lw $t0, 8($t0)
	addiu $t0 $t0 16
	lw $t0, 0($t0)
	jal $t0
	sw $v0, -32($fp)
	addi $sp, $sp, 8
	lw $t0, -12($fp)
	sw $t0, -56($fp)
	lw $a0, -56($fp)
	li $a1, 0
	jal equals
	sw $v0, -60($fp)
	lw $t0, -60($fp)
	bne $t0 $zero L_27
	j L_28
	L_27:
	li $v0, 4
	la $a0, data_8
	syscall
	li $v0, 10
	syscall
	L_28:
	lw $t0, -56($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -56($fp)
	lw $t0, 0($t0)
	sw $t0, -64($fp)
	la $t0, proto_table
	lw $t1, -64($fp)
	sll $t1 $t1 2
	addu $t0 $t0 $t1
	lw $t0, 0($t0)
	lw $t0, 8($t0)
	addiu $t0 $t0 20
	lw $t0, 0($t0)
	jal $t0
	sw $v0, -52($fp)
	addi $sp, $sp, 4
	lw $t0, -52($fp)
	sw $t0, -48($fp)
	lw $t0, 0($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -48($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_6
	sw $v0, -68($fp)
	addi $sp, $sp, 8
	la $t0, data_13 + 0
	sw $t0, -76($fp)
	lw $t0, -76($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_10
	sw $v0, -80($fp)
	addi $sp, $sp, 4
	lw $t0, -80($fp)
	sw $t0, -72($fp)
	lw $t0, 0($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -72($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_6
	sw $v0, -84($fp)
	addi $sp, $sp, 8
	lw $t0, 0($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_9
	sw $v0, -92($fp)
	addi $sp, $sp, 4
	lw $t0, -92($fp)
	sw $t0, -88($fp)
	lw $t0, -12($fp)
	sw $t0, -100($fp)
	lw $a0, -100($fp)
	li $a1, 0
	jal equals
	sw $v0, -104($fp)
	lw $t0, -104($fp)
	bne $t0 $zero L_29
	j L_30
	L_29:
	li $v0, 4
	la $a0, data_8
	syscall
	li $v0, 10
	syscall
	L_30:
	lw $t0, -100($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -88($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -100($fp)
	lw $t0, 0($t0)
	sw $t0, -108($fp)
	la $t0, proto_table
	lw $t1, -108($fp)
	sll $t1 $t1 2
	addu $t0 $t0 $t1
	lw $t0, 0($t0)
	lw $t0, 8($t0)
	addiu $t0 $t0 24
	lw $t0, 0($t0)
	jal $t0
	sw $v0, -96($fp)
	addi $sp, $sp, 8
	lw $t0, -12($fp)
	sw $t0, -120($fp)
	lw $a0, -120($fp)
	li $a1, 0
	jal equals
	sw $v0, -124($fp)
	lw $t0, -124($fp)
	bne $t0 $zero L_31
	j L_32
	L_31:
	li $v0, 4
	la $a0, data_8
	syscall
	li $v0, 10
	syscall
	L_32:
	lw $t0, -120($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -120($fp)
	lw $t0, 0($t0)
	sw $t0, -128($fp)
	la $t0, proto_table
	lw $t1, -128($fp)
	sll $t1 $t1 2
	addu $t0 $t0 $t1
	lw $t0, 0($t0)
	lw $t0, 8($t0)
	addiu $t0 $t0 28
	lw $t0, 0($t0)
	jal $t0
	sw $v0, -116($fp)
	addi $sp, $sp, 4
	lw $t0, -116($fp)
	sw $t0, -112($fp)
	lw $t0, 0($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, -112($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_7
	sw $v0, -132($fp)
	addi $sp, $sp, 8
	lw $t0, -132($fp)
	sw $t0, -8($fp)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 128
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_22:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a1, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $a2, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	li $t0, 5
	sll $t0 $t0 2
	la $t1, proto_table
	addu $t1 $t1 $t0
	lw $t1, 0($t1)
	lw $a0, 4($t1)
	sll $a0 $a0 2
	jal malloc
	move $a2 $a0
	move $a0 $t1
	move $a1 $v0
	jal copy
	sw $v0, -8($fp)
	lw $v0, -8($fp)
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	lw $a2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra

header_size = 12 #in bytes
header_size_slot = 0
header_next_slot = 4
header_reachable_slot = 8
alloc_size       = 2048
total_alloc_size =  2060 #alloc_size + header_size
neg_header_size = -12 #-header_size
free_list = 0
used_list = header_size
state_size = 4
stack_base = -4
init_alloc_size = 28 #(header_size*2) +  state_size
object_mark = -1
meta_data_object_size = 4   #in words
object_expanded = -2
reachable = 1
new_line = 10
str_size_treshold = 1024

    

#####################################################################################################
# Initialize memory manager                                                                         #
# Args:                                                                                             #
#                                                                                                   #
# Return:                                                                                           # 
#                                                                                                   #
# Summary:                                                                                          #
#    The initial blocks for Free-List and Used-List are created.                                    #
#    The $gp is set to use as reference when initial blocks or values related to memory manager     #
#    state are needed.                                                                              #
#    A block of size alloc_size is created an added to Free-List                                    #
##################################################################################################### 
mem_manager_init:
    
    addiu $sp $sp -16
    sw $v0 0($sp)
    sw $a0 4($sp)
    sw $a1 8($sp)
    sw $ra 12($sp)


    li $v0 9
    li $a0 init_alloc_size
    syscall                         #Creating free-list start point
    move $gp $v0                    
    addiu $gp $gp state_size

    sw $zero header_size_slot($gp)       #The free-list start with a block without space, just header, that will always be there.
    sw $zero header_next_slot($gp)
    sw $zero header_reachable_slot($gp) 

    move $a0 $gp
    li $a1 alloc_size
    jal extend_heap

    addiu $a0 $a0 header_size
    sw $zero header_size_slot($a0)      #The used-list start with a block without space, just header, that will always be there.
    sw $zero header_next_slot($a0)
    sw $zero header_reachable_slot($a0)

    
    
    lw $v0 0($sp)
    lw $a0 4($sp)
    lw $a1 8($sp)
    lw $ra 12($sp)
    addiu $sp $sp 16
    
    sw $sp stack_base($gp)

    jr $ra
    

#####################################################################################################
# Free a block previously allocated                                                                 #
# Args:                                                                                             #
# $a0 Block to free address                                                                         #
# Return:                                                                                           # 
#                                                                                                   #
# Summary:                                                                                          #
#    Remove the block from the used-list and add it to the free-list                                #
##################################################################################################### 
free_block:
    addiu $sp $sp -28
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $a0 12($sp)
    sw $ra 16($sp)
    sw $t3 20($sp)
    sw $t4 24($sp)

    move $t0 $a0
    
    addiu $t1 $gp free_list         # Store in $t1 the initial block of the free-list

    addiu $t3 $gp used_list         # Store in $t3 the initial block of the used-list

free_block_loop_used_list:          # Iterate througth the used-list until find the block
    lw $t4 header_next_slot($t3)
    beq $t4 $t0 free_block_loop_free_list
    move $t3 $t4
    j free_block_loop_used_list


free_block_loop_free_list:          # Iterate througth the free-list to find the antecesor of the block in the free-list
    lw $t2 header_next_slot($t1)
    beq $t2 $zero free_block_founded_prev
    bge $t2 $t0 free_block_founded_prev
    move $t1 $t2
    j free_block_loop_free_list

free_block_founded_prev:        
    # Remove the block from the used-list
    lw $t4 header_next_slot($t0)
    sw $t4 header_next_slot($t3)
    
    # Add the block to the free-list
    sw $t2 header_next_slot($t0)
    sw $t0 header_next_slot($t1)

free_block_end:
   
    # Try to merge the list where the new block was added
    move $a0 $t0
    jal expand_block
    move $a0 $t1
    jal expand_block

    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $a0 12($sp)
    lw $ra 16($sp)
    lw $t3 20($sp)
    lw $t4 24($sp)
    addiu $sp $sp 28

    jr $ra


#####################################################################################################
# Merge two continuos blocks of the free-list                                                       #
# Args:                                                                                             #
# $a0  First of the two blocks to merge                                                             #
# Return:                                                                                           # 
#                                                                                                   #
# Summary:                                                                                          #
#    Check if a block can be merged with its sucesor in the free list                               #
##################################################################################################### 
expand_block:
    addiu $sp $sp -16
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)

    
    addiu $t0 $gp free_list     # $t0 = the initial block of the free-list

    beq $t0 $a0 expand_block_end  # The initial block can't be expanded, the initial block always will have size 0

    move $t0 $a0

    # Check if the block and its sucesor in the free list are contiguous in memory
    lw $t1 header_next_slot($t0)
    lw $t2 header_size_slot($t0)
    move $t3 $t2
    addiu $t2 $t2 header_size
    addu $t2 $t2 $t0
    beq $t2 $t1 expand_block_expand
    j expand_block_end

expand_block_expand:    #Increment the size of the first block and update next field
    lw $t2 header_size_slot($t1)
    addi $t2 $t2 header_size
    add $t2 $t2 $t3
    sw $t2 header_size_slot($t0)
    lw $t1 header_next_slot($t1)
    sw $t1 header_next_slot($t0)
    
expand_block_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    addiu $sp $sp 16

    jr $ra


#####################################################################################################
# Allocate more memory for the process and add it to the free-list                                  #
# Args:                                                                                             #
# $a0  Last block of the free-list                                                                  #
# $a1  Memory amount to alloc                                                                       #
# Return:                                                                                           # 
#                                                                                                   #
# Summary:                                                                                          #
#    More memory is allocated and add it to the free-list as a block.                               #
##################################################################################################### 
extend_heap:
    addiu $sp $sp -12
    sw $a0 0($sp)
    sw $a1 4($sp)
    sw $t0 8($sp)

    # Increase the amount of memory by header_size to create a block with that size
    li $v0 9
    addiu $a0 $a1 header_size
    syscall
    
    # Set values of the block_header
    move $t0 $a1 
    sw $t0 header_size_slot($v0)
    sw $zero header_next_slot($v0)
    sw $zero header_reachable_slot($v0)

    # Add block to the end of the free-list
    lw $t0, 0($sp)
    sw $v0 header_next_slot($t0)

    move $a0 $t0
    lw $a1 4($sp)
    lw $t0 8($sp)
    addiu $sp $sp 12

    jr $ra


  
#####################################################################################################
# Split a block into two blocks, one of the requested size and the other with the rest.             #
# Args:                                                                                             #
# $a0  Address of the block to split                                                                #
# $a1  Size requested for one block                                                                 #
# Return:                                                                                           # 
#                                                                                                   #
# Summary:                                                                                          #
#    The block is splitted into two blocks if the size allow it.                                    #
##################################################################################################### 
split_block:
    addiu $sp $sp -16
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $a0 8($sp)
    sw $a1 12($sp)

    # Check if the block can be splitted in two blocks, one of the requested size
    lw $t0 header_size_slot($a0)
    bgt $a1 $t0 split_block_error_small
    
    # Check if after a split the block there is enough space to create another block, if there is not do not split
    sub $t0 $t0 $a1
    li $t1 header_size
    ble $t0 $t1 split_block_same_size

    # Compute the address of the second block
    addu $t0 $a0 $a1
    addiu $t0 $t0 header_size     

    #Update headers of the two blocks
    lw $t1 header_next_slot($a0)    
    sw $t1 header_next_slot($t0)
    sw $t0 header_next_slot($a0)

    lw $t1 header_size_slot($a0)    #update sizes
    sub $t1 $t1 $a1

    addi $t1 $t1 neg_header_size
    sw $t1 header_size_slot($t0)
    sw $a1 header_size_slot($a0)
    move $v0 $a0
    j split_block_end

split_block_same_size:
    move $v0 $a0
    j split_block_end

split_block_error_small:
    j split_block_end

split_block_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $a0 8($sp)
    lw $a1 12($sp)
    addiu $sp $sp 16

    jr $ra


#####################################################################################################
# Best Fit strategy is used to select the block                                                     #
# Args:                                                                                             #
# $a0 size to alloc                                                                                 #
# Return:                                                                                           # 
# $v0 address of allocated block                                                                    #
# Summary:                                                                                          #
#   Actual block is store in $t0, the size block is checked to know if it is a                      #
#   valid block (a block is valid if its size is larger or equal than the required size),           #
#   if the block is valid we compare it with the actual best block and keep the shorter block.      #
#   If there is not a block with the required size, a new block of size                             #
#   max(total_alloc_size, size requested) is requested with sbrk and splitted if necessary          #
##################################################################################################### 
malloc:
    move $v0 $zero
    addiu $sp $sp -28
    sw $t1 0($sp)
    sw $t0 4($sp)
    sw $a0 8($sp)
    sw $a1 12($sp)
    sw $ra 16($sp)
    sw $t2 20($sp)
    sw $t3 24($sp)
    
    addiu $t0 $gp free_list
    j malloc_loop

malloc_end:

    move $a0 $v0
    lw $a1 8($sp)                  # a1 = requested block size
    jal split_block

    lw $t1 header_next_slot($v0)
    sw $t1 header_next_slot($t3)

    addiu $t1 $gp used_list
    lw $a0 header_next_slot($t1)

    sw $a0 header_next_slot($v0)
    sw $v0 header_next_slot($t1)
    
    addiu $v0 $v0 header_size

    lw $t3 24($sp)
    lw $t2 20($sp)
    lw $ra 16($sp)
    lw $a1 12($sp)
    lw $a0 8($sp)
    lw $t0 4($sp)
    lw $t1 0($sp)
    addiu $sp $sp 28

    jr $ra
#######################################################################
# t0 = actual block address                                           #
#######################################################################
malloc_loop:
    move $t2 $t0                        # save previous block in $t2 (this is usefull when we lw $t3 24($sp)need to alloc the new block)
    lw $t0 header_next_slot($t0)        # t0 = next block address
    beq $t0 $zero malloc_search_end     # if t0 == 0 we reach to the free-list end
    j malloc_check_valid_block

#######################################################################
# $v0 = actual selected block address                                 #
#######################################################################
malloc_search_end:
    beq $v0 $zero malloc_alloc_new_block  # if v0 == 0 a valid block was not found
    j malloc_end

#######################################################################
# t2 = last block of free list                                        #
# a0 = requested block size                                           #
#######################################################################
malloc_alloc_new_block:
    li $t1 alloc_size               # t1 = standard alloc size
    move $t3 $t2
    move $a1 $a0                    # a1 = requested block size
    move $a0 $t2                    # a0 = last block of free list
    bge $a1 $t1 malloc_big_block    # if the requested size is bigger than the standar alloc size go to malloc_big_block
    li $a1 alloc_size         # a1 = standard alloc size
    jal extend_heap
    
    j malloc_end

######################################################################
# a1 = requested block size                                          #
######################################################################
malloc_big_block:
    #addiu $a1 $a1 header_size              # Add header size to alloc size
    jal extend_heap
    j malloc_end



########################################################################
# t0 = actual block address                                            #                                            
########################################################################
malloc_check_valid_block:
    lw $t1 header_size_slot($t0)             # t1 = size new block
    bge $t1 $a0 malloc_valid_block    # the actual block have the required size
    j malloc_loop

########################################################################
# t0 = actual block address                                            #
# t1 = size actual block                                               #
# v0 = actual selected block address(0 if no one have been selected)   #
# v1 = actual selected block size                                      #
########################################################################
malloc_valid_block:
    beq $v0 $zero malloc_first_valid_block     # this is the first valid block
    bge $t1 $v1 malloc_loop                    # the selected block is smaller than actual block
    move $v0 $t0                        # selected block address = actual block address
    move $v1 $t1                        # selected block size = actual block size
    move $t3 $t2
    j malloc_loop


########################################################################
# t0 = actual block address                                            # 
# t1 = size actual block                                               # 
# v0 = actual selected block address(0 if no one have been selected)   #
# v1 = actual selected block size                                      #
########################################################################
malloc_first_valid_block:
    move $v0 $t0                        # selected block address = actual block address
    move $v1 $t1                        # selected block size    = actual block size
    move $t3 $t2 
    j malloc_loop


#TODO Look for objects in registers
#####################################################################################################
# Remove from used-list the blocks that are not reachables, the root objects are in the stack and   #
# registers                                                                                         #
# Args:                                                                                             #
#                                                                                                   #
# Return:                                                                                           # 
#                                                                                                   #
# Summary:                                                                                          #
#     First the objects in stack and registers are marked as reachables, after that the objects     #
#     that are reachables from them are marked as reachable too using a dfs algorithm. When all     #
#     reachables objects are marked the used-list is scanned and all the objects that are not       #
#     marked as reachables are released.                                                            #
##################################################################################################### 

gc_collect:
    addiu $sp $sp -24
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)
    sw $a0 16($sp)
    sw $ra 20($sp)

    li $t3 reachable    # $t3 = reachable value
    addiu $t0 $sp 20    # $t0 = the start of the stack without count this function
    lw $t1 stack_base($gp)  # $t1 = the end of the stack

    li $t2 1
# Go through the stack searching for objects
gc_collect_loop:
    addiu $t0 $t0 4
    beq $t0 $t1 gc_collect_dfs      # If the end of the stack was reached finish this loop
    
    lw $a0 0($t0)
    jal check_if_is_object
    
    bne $v0 $t2 gc_collect_loop

    addiu $a0 $a0 neg_header_size
    sw $t3 header_reachable_slot($a0)
    
    j gc_collect_loop

gc_collect_dfs:
    addiu $t1 $gp used_list

# Go through the used-list and try to expand any reachable block
gc_collect_outer_loop:
    lw $t1 header_next_slot($t1)
    beq $t1 $zero gc_collect_free
    lw $t2 header_reachable_slot($t1)
    beq $t2 reachable gc_collect_expand
    j gc_collect_outer_loop

gc_collect_expand:
    addiu $a0 $t1 header_size      # expand an object not a block
    jal gc_collect_recursive_expand
    j gc_collect_outer_loop

gc_collect_free:
    addiu $t0 $gp used_list
    lw $t0 header_next_slot($t0)

# Go through the used-list and free any unreachable object and set the reachable and expanded field to their default values
gc_collect_free_loop:
    beq $t0 $zero gc_collect_end
    lw $t1 header_reachable_slot($t0)
    bne $t1 reachable gc_collect_free_loop_free
    sw $zero header_reachable_slot($t0)
    move $a0 $t0
    jal check_if_is_object
    beq $v0 $zero gc_collect_free_loop
    li $t1 object_mark
    addiu $t2 $t0 header_size
    lw $t3 4($t2)
    sll $t3 $t3 2
    addu $t2 $t2 $t3
    sw $t1 -4($t2)
    lw $t0 header_next_slot($t0)
    j gc_collect_free_loop

gc_collect_free_loop_free:
    move $a0 $t0
    lw $t0 header_next_slot($t0)
    jal free_block
    j gc_collect_free_loop

    
gc_collect_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    lw $a0 16($sp)
    lw $ra 20($sp)
    addiu $sp $sp 24

    jr $ra




#####################################################################################################
# Mark the objects that are reachable from the attrs of one object in a recursive way.              #
# Args:                                                                                             #
# $a0: Object to expand                                                                             #
# Return:                                                                                           # 
#                                                                                                   #
# Summary:                                                                                          #
#     The actual object is marked as reachable and expanded to avoid infinite cycles, and this      #
#     routine is called recursively to expand the objects in the attrs of the actual object.        #
##################################################################################################### 
gc_collect_recursive_expand:
    addiu $sp $sp -16
    sw $a0 0($sp)
    sw $t0 4($sp)
    sw $t1 8($sp)
    sw $ra 12($sp)
    
    jal check_if_is_object  # If is not an object can not be expanded
    beq $v0 $zero gc_collect_recursive_expand_end

    lw $t0 4($a0)
    sll $t0 $t0 2
    addiu $t0 $t0 -4
    addu $t0 $a0 $t0
    lw $t1 0($t0)   # Check if the object was ready expanded to avoid infinite cycles
    beq $t1 object_expanded gc_collect_recursive_expand_end
    
    # Mark the block that contains the object as reachable
    li $t1 reachable
    addiu $a0 $a0 neg_header_size
    sw $t1 header_reachable_slot($a0)
    addiu $a0 $a0 header_size 

    # Mark the object as expanded
    li $t1 object_expanded
    sw $t1 0($t0)

    lw $t0 0($a0)   # $t0 = type of the object
    
    # int and string types are special cases
    la $t1 int_type
    lw $t1 0($t1)
    beq $t0 $t1 gc_collect_recursive_expand_end

    la $t1 string_type
    lw $t1 0($t1)
    beq $t0 $t1 gc_collect_recursive_expand_string_object

    lw $t0 4($a0)
    li $t1 meta_data_object_size
    sub $t0 $t0 $t1
    
    addiu $t1 $a0 12

# call this routine in every attr of the object
gc_collect_recursive_expand_attr_loop:
    beq $t0 $zero gc_collect_recursive_expand_end
    lw $a0 0($t1)
    jal gc_collect_recursive_expand
    addiu $t1 $t1 4
    sub $t0 $t0 1
    j gc_collect_recursive_expand_attr_loop

# the value field of string object is not an object but it is a 
# reference to the block where the string is saved, so that block 
# needs to be marked as reachable
gc_collect_recursive_expand_string_object:
    lw $t0 8($a0)
    addiu $t0 $t0 neg_header_size
    li $t1 reachable
    sw $t1 header_reachable_slot($t0)
    

gc_collect_recursive_expand_end:
    lw $a0 0($sp)
    lw $t0 4($sp)
    lw $t1 8($sp)
    lw $ra 12($sp)
    addiu $sp $sp 16

    jr $ra



  




# $a0 address from 
# $a1 address to
# $a2 size
copy:
    addiu $sp $sp -16
    sw $a0 0($sp)
    sw $a1 4($sp)
    sw $a2 8($sp)
    sw $t0 12($sp)

copy_loop:
    beq $a2 $zero copy_end
    lw $t0 0($a0)
    sw $t0 0($a1)
    addiu $a0 $a0 4
    addiu $a1 $a1 4
    addi $a2 $a2 -4
    j copy_loop 

copy_end:
    lw $a0 0($sp)
    lw $a1 4($sp)
    lw $a2 8($sp)
    lw $t0 12($sp)
    addiu $sp $sp 16

    jr $ra


#####################################################################################################
# Check if a value is a reference to an object                                                      #
# Args:                                                                                             #
# $a0: Value to check                                                                               #
# Return:                                                                                           # 
#    $v0: 1 if is a reference to an object else 0                                                   #
# Summary:                                                                                          #
#     Check if a value is a valid heap address and if it is check if in that address there are      #
#     values that match with the object schema                                                      #
##################################################################################################### 
check_if_is_object:
    addiu $sp $sp -20
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)
    sw $a0 16($sp)

    move $t0 $a0

    li $v0 9
    move $a0 $zero
    syscall

    addiu $t1 $v0 -4    # Last word of heap

    # Check that the first word is a type object
    blt $t0 $gp check_if_is_object_not_object
    bgt $t0 $t1 check_if_is_object_not_object
    lw $t2 0($t0)
    blt $t2 $zero check_if_is_object_not_object
    la $t3 type_number
    lw $t3 0($t3)
    bge $t2 $t3 check_if_is_object_not_object

    addiu $t0 $t0 4
    blt $t0 $gp check_if_is_object_not_object
    bgt $t0 $t1 check_if_is_object_not_object
    lw $t2 0($t0)   #Store size in $t2

    addiu $t0 $t0 8
    

    li $t3 meta_data_object_size
    sub $t2 $t2 $t3 
    sll $t2 $t2 2
    addu $t0 $t0 $t2
    
    # Check if the last word of the object is an object mark
    blt $t0 $gp check_if_is_object_not_object
    bgt $t0 $t1 check_if_is_object_not_object
    lw $t2 0($t0)
    beq $t2 object_mark check_if_is_object_is_object
    beq $t2 object_expanded check_if_is_object_is_object

check_if_is_object_not_object:
    li $v0 0
    j check_if_is_object_end
    
    
check_if_is_object_is_object:
    li $v0 1


check_if_is_object_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    lw $a0 16($sp)
    addiu $sp $sp 20

    jr $ra


equals:
    beq $a0 $a1 equals_equal
    li $v0 0
    j equals_end
    
equals_equal:
    li $v0 1

equals_end:
    jr $ra



less_equal:
    ble $a0 $a1 less_equal_true
    li $v0 0
    j less_equal_end

less_equal_true:
    li $v0 1

less_equal_end:
    jr $ra


less:
    blt $a0 $a1 less_true
    li $v0 0
    j less_end

less_true:
    li $v0 1

less_end:
    jr $ra


len:
    addiu $sp $sp -8
    sw $t0 0($sp)
    sw $t1 4($sp)

    move $t0 $a0
    move $v0 $zero

len_loop:
    lb $t1 0($t0)
    beq $t1 $zero len_end
    addi $v0 $v0 1
    addiu $t0 $t0 1
    j len_loop

len_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    addiu $sp $sp 8

    jr $ra


use_block:
    addiu $sp $sp -12
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)

    addiu $t0 $gp free_list

use_block_loop:
    move $t1 $t0
    lw $t0 header_next_slot($t0)
    beq $t0 $zero use_block_end
    beq $t0 $a0 use_block_founded
    j use_block_loop

use_block_founded:
    lw $t2 header_next_slot($t0)
    sw $t2 header_next_slot($t1)

    addiu $t1 $gp used_list
    lw $t2 header_next_slot($t1)
    sw $t0 header_next_slot($t1)
    sw $t2 header_next_slot($t0)

use_block_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    addiu $sp $sp 12

    jr $ra




read_str:
    addiu $sp $sp -36
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)
	sw $t4 16($sp)
	sw $t5 20($sp)
    sw $a0 24($sp)
    sw $a1 28($sp)
    sw $ra 32($sp)
	
    addiu $t0 $gp free_list
    move $t1 $zero
    move $t2 $t0

read_str_larger_block_loop:
    lw $t0 header_next_slot($t0)
    beq $t0 $zero read_str_reading
    lw $t3 header_size_slot($t0)
    bge $t1 $t3 read_str_larger_block_loop
    move $t1 $t3
    move $t2 $t0
    j read_str_larger_block_loop

read_str_reading:
    beq $t1 $zero read_str_new_block
    move $a1 $t1
    li $v0 8
    addiu $a0 $t2 header_size
    syscall
    move $t0 $a0
    move $t1 $zero

read_str_look_nl:
    lb $t2 0($t0)
    beq $t2 $zero read_str_no_nl
    beq $t2 new_line read_str_nl_founded
    addi $t1 $t1 1
    addi $t0 $t0 1
    j read_str_look_nl

read_str_nl_founded:
    sb $zero 0($t0)
    addi $t1 $t1 1
	li $t2 4
	div $t1 $t2
	mfhi $t3
	beq $t3 $zero read_str_nl_founded_alligned
	sub $t2 $t2 $t3
	add $t1 $t1 $t2
read_str_nl_founded_alligned:
    move $a1 $t1
    addiu $a0 $a0 neg_header_size
    jal split_block
    jal use_block

    addiu $v0 $a0 header_size
	j read_str_end


read_str_no_nl:
	addi $t1 $t1 1
    blt $t1 str_size_treshold read_str_dup
	addi $t1 $t1 alloc_size
	j read_str_extend_heap
read_str_dup:
	sll $t1 $t1 1
read_str_extend_heap:
	move $a1 $t1
	move $t0 $a0
	addiu $a0 $gp free_list

read_str_last_block_loop:
	lw $t1 header_next_slot($a0)
	beq $t1 $zero read_str_last_block_founded
	lw $a0 header_next_slot($a0)
	j read_str_last_block_loop

read_str_last_block_founded:
	jal extend_heap
	jal expand_block
	lw $t1 header_next_slot($a0)
	bne $t1 $zero read_str_copy_prev
	move $t1 $a0

read_str_copy_prev:
	lw $t3 header_size_slot($t1)
	move $t2 $zero
	move $t5 $t1
	addiu $t1 $t1 header_size

read_str_copy_loop:
	lb $t4 0($t0)
	beq $t4 $zero read_str_copy_end
	sb $t4 0($t1)
	addi $t2 $t2 1
	addi $t0 $t0 1
	addi $t1 $t1 1
	j read_str_copy_loop

read_str_copy_end:
	sub $t3 $t3 $t2
	move $a0 $t1
	move $a1 $t3
	li $v0 8
	syscall
	move $t0 $a0
	move $t1 $t2
	addiu $a0 $t5 header_size
	j read_str_look_nl

	
read_str_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
	lw $t4 16($sp)
	lw $t5 20($sp)
    lw $a0 24($sp)
    lw $a1 28($sp)
    lw $ra 32($sp)
    addiu $sp $sp 36

    jr $ra


read_str_new_block:
    addiu $t0 $gp free_list

read_str_new_block_search_last:
    lw $t1 header_next_slot($t0)
    beq $t1 $zero read_str_new_block_create
    move $t0 $t1
    j read_str_new_block_search_last

read_str_new_block_create:
    move $a0 $t0
    li $a1 alloc_size
    jal extend_heap
    jal expand_block
    lw $t2 header_next_slot($a0)
    beq $t2 $zero read_str_new_block_expanded
    lw $t1 header_size_slot($t2)
    j read_str_reading

read_str_new_block_expanded:
    move $t2 $a0
    lw $t1 header_size_slot($a0)
    j read_str_reading



concat:
    addiu $sp $sp -24
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $a0 12($sp)
    sw $a1 16($sp)
    sw $ra 20($sp)

    move $t0 $a0
    move $t1 $a1
    addiu $a0 $a0 neg_header_size
    addiu $a1 $a1 neg_header_size

    lw $a0 header_size_slot($a0)
    lw $a1 header_size_slot($a1)
    
    add $a0 $a0 $a1
    jal malloc
    move $t2 $v0

concat_copy_first_loop:
    lb $a0 0($t0)
    beq $a0 $zero concat_copy_second_loop
    sb $a0 0($t2)
    addiu $t0 $t0 1
    addiu $t2 $t2 1
    j concat_copy_first_loop

concat_copy_second_loop:
    lb $a0 0($t1)
    beq $a0 $zero concat_end
    sb $a0 0($t2)
    addiu $t1 $t1 1
    addiu $t2 $t2 1
    j concat_copy_second_loop

concat_end:
    sb $zero 0($t2)
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $a0 12($sp)
    lw $a1 16($sp)
    lw $ra 20($sp)
    addiu $sp $sp 24

    jr $ra


substr:
    addiu $sp $sp -24
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)
    sw $a0 16($sp)
    sw $ra 20($sp)

    move $t0 $a0
    li $t1 4

    div $a2 $t1
 
    mfhi $t2
    bne $t2 $zero substr_allign_size
    move $t1 $a2
    j substr_new_block

substr_allign_size:
    sub $t1 $t1 $t2
    add $t1 $t1 $a2

substr_new_block:
    move $a0 $t1
    jal malloc
    move $t3 $v0
    move $t1 $zero
    addu $t0 $t0 $a1

substr_copy_loop:
    beq $t1 $a2 substr_end
    lb $t2 0($t0)
    sb $t2 0($t3)
    addiu $t0 $t0 1
    addiu $t3 $t3 1
    addiu $t1 $t1 1
    j substr_copy_loop

substr_end:
    sb $zero 0($t3)
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    lw $a0 16($sp)
    lw $ra 20($sp)
    addiu $sp $sp 24

    jr $ra










    






    

    









