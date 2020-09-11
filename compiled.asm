	.data
data_1: .asciiz "Object"
data_2: .asciiz "IO"
data_3: .asciiz "String"
data_4: .asciiz "Int"
data_5: .asciiz "Main"
data_6: .asciiz "A"
data_7: .asciiz "Program aborted"
data_8: .asciiz "Hello World!"

types_names_table:
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
	.word	 L_6
	.word	 L_7
	.word	 L_8
	.word	 L_9
	.word	 L_15

type_5_proto:
	.word	4
	.word	4
	.word	type_5_dispatch
	.word	-1

type_6_dispatch:
	.word	 L_2
	.word	 L_3
	.word	 L_4

type_6_proto:
	.word	5
	.word	16
	.word	type_6_dispatch
	.word	0
	.word	0
	.word	0
	.word	-1
	.text
	.globl main
main:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -8
	li $v0, 9
	li $a0, 4
	syscall
	la $t0, type_5
	sw $t0, 0($v0)
	sw $v0, -12($fp)
	lw $t0, -12($fp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	jal L_15
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
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	li $v0, 9
	li $a0, 4
	syscall
	la $t0, type_1
	sw $t0, 0($v0)
	sw $v0, -8($fp)
	lw $v0, -8($fp)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
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
	sw $t1, 0($sp)
	lw $t1, 0($fp)
	lw $t1, 0($t1)
	lw $t1, 0($t1)
	sw $t1, -8($fp)
	lw $t1, -8($fp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	jal L_10
	sw $v0, -12($fp)
	addi $sp, $sp, 4
	lw $v0, -12($fp)
	lw $t1, 0($sp)
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
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	li $v0, 9
	li $a0, 4
	syscall
	la $t1, type_1
	sw $t1, 0($v0)
	sw $v0, -8($fp)
	lw $v0, -8($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
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
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	lw $t1, 0($fp)
	lw $t1, 4($t1)
	sw $t1, -8($fp)
	li $v0, 4
	lw $a0, -8($fp)
	syscall
	lw $v0, 4($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
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
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	lw $t1, 0($fp)
	lw $t1, 4($t1)
	sw $t1, -8($fp)
	li $v0, 1
	lw $a0, -8($fp)
	syscall
	lw $v0, 4($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
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
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t2, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	li $v0, 9
	li $a0, 8
	syscall
	la $t1, type_3
	sw $t1, 0($v0)
	sw $v0, -8($fp)
	lw $t2, -8($fp)
	lw $t1, 0($fp)
	sw $t1, 4($t2)
	lw $v0, -8($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
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
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_13:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_14:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t2, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	li $v0, 9
	li $a0, 8
	syscall
	la $t1, type_4
	sw $t1, 0($v0)
	sw $v0, -8($fp)
	lw $t2, -8($fp)
	lw $t1, 0($fp)
	sw $t1, 4($t2)
	lw $v0, -8($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $t2, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_15:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -16
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	la $t1, data_8 + 0
	sw $t1, -12($fp)
	lw $t1, -12($fp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	jal L_10
	sw $v0, -16($fp)
	addi $sp, $sp, 4
	lw $t1, -16($fp)
	sw $t1, -8($fp)
	lw $t1, 0($fp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	lw $t1, -8($fp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	jal L_6
	sw $v0, -20($fp)
	addi $sp, $sp, 8
	lw $v0, -20($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 16
	lw $fp, 0($sp)
	addi $sp, $sp, 4
	jr $ra
L_16:
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	addi $fp, $sp, 4
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	addi $sp, $sp, -4
	sw $t1, 0($sp)
	li $v0, 9
	li $a0, 4
	syscall
	la $t1, type_5
	sw $t1, 0($v0)
	sw $v0, -8($fp)
	lw $v0, -8($fp)
	lw $t1, 0($sp)
	addi $sp, $sp, 4
	lw $a0, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
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