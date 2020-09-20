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
	.word	8
	.word	type_3_dispatch
	.word	0
	.word	-1

type_4_dispatch:
	.word	 L_14

type_4_proto:
	.word	3
	.word	8
	.word	type_4_dispatch
	.word	0
	.word	-1

type_5_dispatch:
	.word	 L_2
	.word	 L_3
	.word	 L_4

type_5_proto:
	.word	4
	.word	16
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
	.word	 L_16

type_6_proto:
	.word	5
	.word	4
	.word	type_6_dispatch
	.word	-1
	.text
	.globl main
main:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
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
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_2:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
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
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $t5, 0($sp)
	addi $sp, $sp, -4
	sw $t6, 0($sp)
	lw $t5, 0($fp)
	lw $t5, 0($t5)
	sll $t5 $t5 2
	la $t6, type_name_table
	addu $t5 $t5 $t6
	sw $t5, -8($fp)
	lw $t5, -8($fp)
	addi $sp, $sp, -4
	sw $t5, 0($sp)
	jal L_10
	sw $v0, -12($fp)
	addi $sp, $sp, 4
	lw $v0, -12($fp)
	lw $t6, 0($sp)
	addi $sp, $sp, 4
	lw $t5, 0($sp)
	addi $sp, $sp, 4
	lw $ra, 0($sp)
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
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_5:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_6:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_7:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_8:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_9:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_10:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -12
	addi $sp, $sp, 12
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_11:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_12:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	addi $sp, $sp, 8
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_13:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -28
	addi $sp, $sp, 28
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_14:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_15:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_16:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -36
	addi $sp, $sp, 36
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_17:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra