.data
	str_buffer: .space 1024
	
	_index_negative_msg: .align 2 
			 .asciiz "Index to substr is negative\n"
	_index_out_msg: .align 2 
			 .asciiz "Index out range exception\n"
	_abort_msg: .align 2 
			 .asciiz "Execution aborted\n"
	_div_zero_msg: .align 2 
			 .asciiz "Division by zero exception\n"
	
	data_0: .align 2 
 			.asciiz ""
	data_1: .align 2 
 			.asciiz "678987"
	data_2: .align 2 
 			.asciiz " == "
	data_3: .align 2 
 			.asciiz "\n"
	data_4: .align 2 
 			.asciiz "0"
	data_5: .align 2 
 			.asciiz "1"
	data_6: .align 2 
 			.asciiz "2"
	data_7: .align 2 
 			.asciiz "3"
	data_8: .align 2 
 			.asciiz "4"
	data_9: .align 2 
 			.asciiz "5"
	data_10: .align 2 
 			.asciiz "6"
	data_11: .align 2 
 			.asciiz "7"
	data_12: .align 2 
 			.asciiz "8"
	data_13: .align 2 
 			.asciiz "9"
	data_14: .align 2 
 			.asciiz "-"
	data_15: .align 2 
 			.asciiz "+"
	
	classname_void: .align 2 
			.asciiz "void"
	classname_Object: .align 2 
			.asciiz "Object"
	classname_IO: .align 2 
			.asciiz "IO"
	classname_Main: .align 2 
			.asciiz "Main"
	classname_Int: .align 2 
			.asciiz "Int"
	classname_Bool: .align 2 
			.asciiz "Bool"
	classname_String: .align 2 
			.asciiz "String"
	classname_A2I: .align 2 
			.asciiz "A2I"
	type_void: .align 2 
			 .asciiz ""

.text
main:
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_build_class_name_table
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_allocate_prototypes_table
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_build_prototypes
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_build_dispatch_tables
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_build_class_parents_table
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# ALLOCATE
	lw $t0 24($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	# ALLOCATE
	lw $t0 24($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	sw $v0 0($sp)
	addiu $sp $sp -4
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Main__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp $sp 4
	sw $v0 0($sp)
	addiu $sp $sp -4
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Main_main
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp $sp 4
	li $v0 10
	syscall
	
########## STATIC FUNCTIONS ##########

function___conforms:
	move $fp, $sp
	lw $t0 12($fp)
	lw $t1 16($fp)
	beq $t1 1 _conforms_ret_true_
_conforms_loop_:
	beq $t0 $t1 _conforms_ret_true_
	beq $t0 1 _conforms_ret_false_
	mul $t0 $t0 4
	addu $t0 $t0 $s2
	lw $t0 0($t0)
	j _conforms_loop_
_conforms_ret_true_:
	li $v0 1
	j _conforms_ret_
_conforms_ret_false_:
	li $v0 0
	_conforms_ret_:
	jr $ra
	
function__isvoid:
	move $fp, $sp
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	lw $t0 12($fp)
	la $t1 type_void
	beq $t0 $t1 _is_void_true_
	sw $0 12($v0)
	j _is_void_end_
_is_void_true_:
	li $t0 1
	sw $t0 12($v0)
_is_void_end_:
	jr $ra
	
function_Object_abort:
	move $fp, $sp
	jr $ra
	
function_Object_copy:
	move $fp, $sp
	lw $t0 12($fp)
	lw $a0 4($t0)
	move $t4 $a0
	li $v0 9
	syscall
	move $t2 $v0
	li $t3 0
_objcopy_loop:
	lw $t1 0($t0)
	sw $t1 0($v0)
	addiu $t0 $t0 4
	addiu $v0 $v0 4
	addiu $t3 $t3 4
	ble $t4 $t3 _objcopy_loop
_objcopy_div_end_:
	move $v0 $t2
	jr $ra
	
function_Object_type_name:
	move $fp, $sp
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	move $v1 $v0
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	lw $a1 12($fp)
	lw $a1 0($a1)
	mul $a1 $a1 4
	addu $a1 $a1 $s1
	lw $a1 0($a1)
	move $a2 $0
	move $t2 $a1
_str_len_clsname_:
	lb $a0 0($t2)
	beq $a0 $0 _end_clsname_len_
	addiu $a2 $a2 1
	addiu $t2 $t2 1
	j _str_len_clsname_
_end_clsname_len_:
	sw $a2, 12($v0)
	sw $v0, 12($v1)
	sw $a1, 16($v1)
	move $v0 $v1
	jr $ra
	
function_String_length:
	move $fp, $sp
	lw $a0 12($fp)
	lw $v0 12($a0)
	jr $ra
	
function_String_concat:
	move $fp, $sp
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	move $v1 $v0
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	move $t3 $v0
	lw $a1 12($fp)
	lw $a2 16($fp)
	lw $t1 12($a1)
	lw $t1 12($t1)
	lw $t2 12($a2)
	lw $t2 12($t2)
	addu $t0 $t2 $t1
	sw $t0 12($v1)
	lw $a1 16($a1)
	lw $a2 16($a2)
	addiu $t0 $t0 1
	move $a0 $t0
	li $v0 9
	syscall
	move $t5 $v0
	move $t4 $a1
	addu $a1 $a1 $t1
_strcat_copy_:
	beq $t4 $a1 _end_strcat_copy_
	lb $a0 0($t4)
	sb $a0 0($t5)
	addiu $t5 $t5 1
	addiu $t4 $t4 1
	j _strcat_copy_
_end_strcat_copy_:
	move $t4 $a2
	addu $a2 $a2 $t2
_strcat_copy_snd_:
	beq $t4 $a2 _end_strcat_copy_snd_
	lb $a0 0($t4)
	sb $a0 0($t5)
	addiu $t5 $t5 1
	addiu $t4 $t4 1
	j _strcat_copy_snd_
_end_strcat_copy_snd_:
	sb $0 0($t5)
	sw $v1 12($t3)
	sw $v0 16($t3)
	move $v0 $t3
	jr $ra
	
function_String_substr:
	move $fp, $sp
	lw $t5 12($fp)
	lw $a1 16($fp)
	lw $a1 12($a1)
	lw $a2 20($fp)
	lw $a2 12($a2)
	blt $a1 $0 _index_negative
	blt $a2 $0 _index_negative
	add $a2 $a1 $a2
	lw $a3 12($t5)
	lw $a3 12($a3)
	bgt $a2 $a3 _index_out
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	move $v1 $v0
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	move $t0 $v0
	move $t7 $a2
	subu $t7 $t7 $a1
	sw $t7 12($t0)
	move $a0 $a2
	li $v0 9
	syscall
	sw $t0 12($v1)
	sw $v0 16($v1)
	move $t1 $v0
	lw $t5 16($t5)
	move $t4 $t5
	addu $t4 $t4 $a1
	addu $t5 $t5 $a2
_substr_copy_:
	bge $t4 $t5 _end_substr_copy_
	lb $a0 0($t4)
	sb $a0 0($t1)
	addiu $t1 $t1 1
	addiu $t4 $t4 1
	j _substr_copy_
_index_negative:
	la $a0 _index_negative_msg
	b _subst_abort
_index_out:
	la $a0 _index_out_msg
	b _subst_abort
_subst_abort:
	li $v0 4
	syscall
	la	$a0 _abort_msg
	li $v0 4
	syscall
	li $v0 10
	syscall
_end_substr_copy_:
	move $v0 $v1
	jr $ra
	
function_IO_in_int:
	move $fp, $sp
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	move $t0 $v0
	li $v0 5
	syscall
	sw $v0 12($t0)
	move $v0 $t0
	jr $ra
	
function_IO_in_string:
	move $fp, $sp
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	move $v1 $v0
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	addiu $sp, $sp, 4
	
	sw $v1 12($v0)
	move $t5 $v0
	la $a0 str_buffer
	li $a1 1025
	li $v0 8
	syscall
	move $a0 $0
	la $t2 str_buffer
_in_string_str_len_:
	lb $t0 0($t2)
	beq $t0 $0 _end_in_string_str_len_
	beq $t0 10 _end_in_string_str_len_
	addiu $a0 $a0 1
	addiu $t2 $t2 1
	j _in_string_str_len_
_end_in_string_str_len_:
	sw $a0 12($v1)
	li $v0 9
	syscall
	la $t4 str_buffer
	move $t1 $v0
_in_str_copy_:
	lb $t0 0($t4)
	beq $t0 $0 _end_in_str_copy_
	beq $t0 10 _end_in_str_copy_
	sb $t0 0($t1)
	addiu $t4 $t4 1
	addiu $t1 $t1 1
	j _in_str_copy_
_end_in_str_copy_:
	sw $v0 16($t5)
	la $t4 str_buffer
_in_str_clean_:
	lb $t0 0($t4)
	beq $t0 $0 _end_in_str_clean_
	sb $0 0($t4)
	addiu $t4 $t4 1
	j _in_str_clean_
_end_in_str_clean_:
	move $v0 $t5
	jr $ra
	
function_IO_out_int:
	move $fp, $sp
	lw $a0 16($fp)
	lw $a0 12($a0)
	li $v0 1
	syscall
	lw $v0 12($fp)
	jr $ra
	
function_IO_out_string:
	move $fp, $sp
	lw $a0 16($fp)
	lw $a0 16($a0)
	li $v0 4
	syscall
	lw $v0 12($fp)
	jr $ra
	
	
############## TABLES ################

function_build_class_name_table:
	li $a0 32
	li $v0 9
	syscall
	move $s1 $v0
	la $t1 classname_void
	sw $t1 0($s1)
	la $t1 classname_Object
	sw $t1 4($s1)
	la $t1 classname_IO
	sw $t1 8($s1)
	la $t1 classname_Main
	sw $t1 12($s1)
	la $t1 classname_Int
	sw $t1 16($s1)
	la $t1 classname_Bool
	sw $t1 20($s1)
	la $t1 classname_String
	sw $t1 24($s1)
	la $t1 classname_A2I
	sw $t1 28($s1)
	jr $ra
	
function_allocate_prototypes_table:
	li $a0 64
	li $v0 9
	syscall
	move $s0 $v0
	jr $ra
	
function_build_prototypes:
	# Type void
	li $a0 12
	li $v0 9
	syscall
	li $a0 0
	sw $a0 0($v0)
	li $a0 12
	sw $a0 4($v0)
	sw $v0 0($s0)
	
	# Type Object
	li $a0 12
	li $v0 9
	syscall
	li $a0 1
	sw $a0 0($v0)
	li $a0 12
	sw $a0 4($v0)
	sw $v0 8($s0)
	
	# Type IO
	li $a0 12
	li $v0 9
	syscall
	li $a0 2
	sw $a0 0($v0)
	li $a0 12
	sw $a0 4($v0)
	sw $v0 16($s0)
	
	# Type Main
	li $a0 12
	li $v0 9
	syscall
	li $a0 3
	sw $a0 0($v0)
	li $a0 12
	sw $a0 4($v0)
	sw $v0 24($s0)
	
	# Type Int
	li $a0 16
	li $v0 9
	syscall
	li $a0 4
	sw $a0 0($v0)
	li $a0 16
	sw $a0 4($v0)
	sw $v0 32($s0)
	
	# Type Bool
	li $a0 16
	li $v0 9
	syscall
	li $a0 5
	sw $a0 0($v0)
	li $a0 16
	sw $a0 4($v0)
	sw $v0 40($s0)
	
	# Type String
	li $a0 20
	li $v0 9
	syscall
	li $a0 6
	sw $a0 0($v0)
	li $a0 20
	sw $a0 4($v0)
	sw $v0 48($s0)
	
	# Type A2I
	li $a0 12
	li $v0 9
	syscall
	li $a0 7
	sw $a0 0($v0)
	li $a0 12
	sw $a0 4($v0)
	sw $v0 56($s0)
	
	jr $ra
	
function_build_dispatch_tables:
	# Type void
	li $a0 0
	li $v0 9
	syscall
	lw $t0 0($s0)
	sw $v0 8($t0)
	
	# Type Object
	li $a0 12
	li $v0 9
	syscall
	la $t1 function_Object_abort
	sw $t1 0($v0)
	la $t1 function_Object_copy
	sw $t1 4($v0)
	la $t1 function_Object_type_name
	sw $t1 8($v0)
	lw $t0 8($s0)
	sw $v0 8($t0)
	
	# Type IO
	li $a0 28
	li $v0 9
	syscall
	la $t1 function_Object_abort
	sw $t1 0($v0)
	la $t1 function_Object_copy
	sw $t1 4($v0)
	la $t1 function_Object_type_name
	sw $t1 8($v0)
	la $t1 function_IO_in_int
	sw $t1 12($v0)
	la $t1 function_IO_in_string
	sw $t1 16($v0)
	la $t1 function_IO_out_int
	sw $t1 20($v0)
	la $t1 function_IO_out_string
	sw $t1 24($v0)
	lw $t0 16($s0)
	sw $v0 8($t0)
	
	# Type Main
	li $a0 32
	li $v0 9
	syscall
	la $t1 function_Object_abort
	sw $t1 0($v0)
	la $t1 function_Object_copy
	sw $t1 4($v0)
	la $t1 function_Object_type_name
	sw $t1 8($v0)
	la $t1 function_IO_in_int
	sw $t1 12($v0)
	la $t1 function_IO_in_string
	sw $t1 16($v0)
	la $t1 function_IO_out_int
	sw $t1 20($v0)
	la $t1 function_IO_out_string
	sw $t1 24($v0)
	la $t1 function_Main_main
	sw $t1 28($v0)
	lw $t0 24($s0)
	sw $v0 8($t0)
	
	# Type Int
	li $a0 12
	li $v0 9
	syscall
	la $t1 function_Object_abort
	sw $t1 0($v0)
	la $t1 function_Object_copy
	sw $t1 4($v0)
	la $t1 function_Object_type_name
	sw $t1 8($v0)
	lw $t0 32($s0)
	sw $v0 8($t0)
	
	# Type Bool
	li $a0 12
	li $v0 9
	syscall
	la $t1 function_Object_abort
	sw $t1 0($v0)
	la $t1 function_Object_copy
	sw $t1 4($v0)
	la $t1 function_Object_type_name
	sw $t1 8($v0)
	lw $t0 40($s0)
	sw $v0 8($t0)
	
	# Type String
	li $a0 24
	li $v0 9
	syscall
	la $t1 function_Object_abort
	sw $t1 0($v0)
	la $t1 function_Object_copy
	sw $t1 4($v0)
	la $t1 function_Object_type_name
	sw $t1 8($v0)
	la $t1 function_String_length
	sw $t1 12($v0)
	la $t1 function_String_concat
	sw $t1 16($v0)
	la $t1 function_String_substr
	sw $t1 20($v0)
	lw $t0 48($s0)
	sw $v0 8($t0)
	
	# Type A2I
	li $a0 36
	li $v0 9
	syscall
	la $t1 function_Object_abort
	sw $t1 0($v0)
	la $t1 function_Object_copy
	sw $t1 4($v0)
	la $t1 function_Object_type_name
	sw $t1 8($v0)
	la $t1 function_A2I_c2i
	sw $t1 12($v0)
	la $t1 function_A2I_i2c
	sw $t1 16($v0)
	la $t1 function_A2I_a2i
	sw $t1 20($v0)
	la $t1 function_A2I_a2i_aux
	sw $t1 24($v0)
	la $t1 function_A2I_i2a
	sw $t1 28($v0)
	la $t1 function_A2I_i2a_aux
	sw $t1 32($v0)
	lw $t0 56($s0)
	sw $v0 8($t0)
	
	jr $ra
	
function_build_class_parents_table:
	li $a0 32
	li $v0 9
	syscall
	move $s2 $v0
	
	li $t0 2
	mul $t0 $t0 4
	add $t0 $t0 $s2
	li $t1 1
	sw $t1 0($t0)
	
	li $t0 4
	mul $t0 $t0 4
	add $t0 $t0 $s2
	li $t1 1
	sw $t1 0($t0)
	
	li $t0 5
	mul $t0 $t0 4
	add $t0 $t0 $s2
	li $t1 1
	sw $t1 0($t0)
	
	li $t0 6
	mul $t0 $t0 4
	add $t0 $t0 $s2
	li $t1 1
	sw $t1 0($t0)
	
	li $t0 7
	mul $t0 $t0 4
	add $t0 $t0 $s2
	li $t1 1
	sw $t1 0($t0)
	
	li $t0 3
	mul $t0 $t0 4
	add $t0 $t0 $s2
	li $t1 2
	sw $t1 0($t0)
	
	jr $ra
	
	
########### COOL FUNCTIONS ##########

function_Object__init:
	move $fp, $sp
	subu $sp, $sp, 0
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 0
	jr $ra
	
function_IO__init:
	move $fp, $sp
	subu $sp, $sp, 0
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# POPPARAM
	addiu $sp $sp 4
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 0
	jr $ra
	
function_Main__init:
	move $fp, $sp
	subu $sp, $sp, 0
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_IO__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# POPPARAM
	addiu $sp $sp 4
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 0
	jr $ra
	
function_Main_main:
	move $fp, $sp
	subu $sp, $sp, 92
	# ALLOCATE
	lw $t0 56($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 0($fp)
	
	addiu $sp, $sp, 4
	
	# PUSHPARAM
	lw $a0, 0($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_A2I__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -4($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -20($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -20($fp)
	li $a0, 6
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -16($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -16($fp)
	lw $a0 -20($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -16($fp)
	la $a0, data_1
	sw $a0 16($a1)
	
	# PUSHPARAM
	lw $a0, -16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 0($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 0($fp)
	lw $a0 0($a1)
	sw $a0 -8($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -8($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -12($fp)
	lw $a2, -8($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 56($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -24($fp)
	
	addiu $sp, $sp, 4
	
	# PUSHPARAM
	lw $a0, -24($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_A2I__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -28($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -40($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -40($fp)
	li $a0, 678987
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -40($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, -24($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -24($fp)
	lw $a0 0($a1)
	sw $a0 -32($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -32($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 28($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -36($fp)
	lw $a2, -32($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -44($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -44($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -48($fp)
	lw $a2, -44($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -64($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -64($fp)
	li $a0, 4
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -60($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -60($fp)
	lw $a0 -64($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -60($fp)
	la $a0, data_2
	sw $a0 16($a1)
	
	# PUSHPARAM
	lw $a0, -60($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -52($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -52($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -56($fp)
	lw $a2, -52($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -36($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -68($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -68($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -72($fp)
	lw $a2, -68($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -88($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -88($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -84($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -84($fp)
	lw $a0 -88($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -84($fp)
	la $a0, data_3
	sw $a0 16($a1)
	
	# PUSHPARAM
	lw $a0, -84($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -76($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -76($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -80($fp)
	lw $a2, -76($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# RETURN
	lw $v0, -80($fp)
	addiu $sp, $sp, 92
	jr $ra
	
function_Int__init:
	move $fp, $sp
	subu $sp, $sp, 0
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# POPPARAM
	addiu $sp $sp 4
	
	# SETATTR
	lw $a1 12($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 0
	jr $ra
	
function_Bool__init:
	move $fp, $sp
	subu $sp, $sp, 0
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# POPPARAM
	addiu $sp $sp 4
	
	# SETATTR
	lw $a1 12($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 0
	jr $ra
	
function_String__init:
	move $fp, $sp
	subu $sp, $sp, 0
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# POPPARAM
	addiu $sp $sp 4
	
	# SETATTR
	lw $a1 12($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 12($fp)
	la $a0, data_0
	sw $a0 16($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 0
	jr $ra
	
function_A2I__init:
	move $fp, $sp
	subu $sp, $sp, 0
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	
	# POPPARAM
	addiu $sp $sp 4
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 0
	jr $ra
	
function_A2I_c2i:
	move $fp, $sp
	subu $sp, $sp, 292
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -20($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -20($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -16($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -16($fp)
	lw $a0 -20($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -16($fp)
	la $a0, data_4
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -16($fp)
	beq $t0 $zero _eq_false_1_
	beq $t1 $zero _eq_false_1_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_1_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_1
	li $a2 5
	beq $a0 $a2 _eq_int_bool_1
	li $a2 6
	bne $a0 $a2 _not_basic_type_1_
_eq_str_1_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_1_
	beq $t3 $0 _eq_true_1_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_1_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_1_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_1_
	b _eq_true_1_
_not_basic_type_1_:
	bne $t0 $t1 _eq_false_1_
	b _eq_true_1_
_eq_int_bool_1:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_1_
_eq_true_1_:
	li $a0 1
	sw $a0 -8($fp)
	b end_equal_1_
_eq_false_1_:
	li $a0 0
	sw $a0 -8($fp)
end_equal_1_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -12($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -12($fp)
	lw $a0 -8($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -12($fp)
	lw $a0 12($a1)
	sw $a0 -4($fp)
	
	# IF GOTO
	lw $a0, -4($fp)
	bnez $a0, _cil_label_LABEL_0
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -44($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -44($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -40($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -40($fp)
	lw $a0 -44($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -40($fp)
	la $a0, data_5
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -40($fp)
	beq $t0 $zero _eq_false_2_
	beq $t1 $zero _eq_false_2_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_2_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_2
	li $a2 5
	beq $a0 $a2 _eq_int_bool_2
	li $a2 6
	bne $a0 $a2 _not_basic_type_2_
_eq_str_2_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_2_
	beq $t3 $0 _eq_true_2_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_2_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_2_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_2_
	b _eq_true_2_
_not_basic_type_2_:
	bne $t0 $t1 _eq_false_2_
	b _eq_true_2_
_eq_int_bool_2:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_2_
_eq_true_2_:
	li $a0 1
	sw $a0 -32($fp)
	b end_equal_2_
_eq_false_2_:
	li $a0 0
	sw $a0 -32($fp)
end_equal_2_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -36($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -36($fp)
	lw $a0 -32($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -36($fp)
	lw $a0 12($a1)
	sw $a0 -28($fp)
	
	# IF GOTO
	lw $a0, -28($fp)
	bnez $a0, _cil_label_LABEL_2
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -68($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -68($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -64($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -64($fp)
	lw $a0 -68($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -64($fp)
	la $a0, data_6
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -64($fp)
	beq $t0 $zero _eq_false_3_
	beq $t1 $zero _eq_false_3_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_3_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_3
	li $a2 5
	beq $a0 $a2 _eq_int_bool_3
	li $a2 6
	bne $a0 $a2 _not_basic_type_3_
_eq_str_3_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_3_
	beq $t3 $0 _eq_true_3_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_3_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_3_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_3_
	b _eq_true_3_
_not_basic_type_3_:
	bne $t0 $t1 _eq_false_3_
	b _eq_true_3_
_eq_int_bool_3:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_3_
_eq_true_3_:
	li $a0 1
	sw $a0 -56($fp)
	b end_equal_3_
_eq_false_3_:
	li $a0 0
	sw $a0 -56($fp)
end_equal_3_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -60($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -60($fp)
	lw $a0 -56($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -60($fp)
	lw $a0 12($a1)
	sw $a0 -52($fp)
	
	# IF GOTO
	lw $a0, -52($fp)
	bnez $a0, _cil_label_LABEL_4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -92($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -92($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -88($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -88($fp)
	lw $a0 -92($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -88($fp)
	la $a0, data_7
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -88($fp)
	beq $t0 $zero _eq_false_4_
	beq $t1 $zero _eq_false_4_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_4_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_4
	li $a2 5
	beq $a0 $a2 _eq_int_bool_4
	li $a2 6
	bne $a0 $a2 _not_basic_type_4_
_eq_str_4_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_4_
	beq $t3 $0 _eq_true_4_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_4_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_4_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_4_
	b _eq_true_4_
_not_basic_type_4_:
	bne $t0 $t1 _eq_false_4_
	b _eq_true_4_
_eq_int_bool_4:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_4_
_eq_true_4_:
	li $a0 1
	sw $a0 -80($fp)
	b end_equal_4_
_eq_false_4_:
	li $a0 0
	sw $a0 -80($fp)
end_equal_4_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -84($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -84($fp)
	lw $a0 -80($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -84($fp)
	lw $a0 12($a1)
	sw $a0 -76($fp)
	
	# IF GOTO
	lw $a0, -76($fp)
	bnez $a0, _cil_label_LABEL_6
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -116($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -116($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -112($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -112($fp)
	lw $a0 -116($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -112($fp)
	la $a0, data_8
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -112($fp)
	beq $t0 $zero _eq_false_5_
	beq $t1 $zero _eq_false_5_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_5_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_5
	li $a2 5
	beq $a0 $a2 _eq_int_bool_5
	li $a2 6
	bne $a0 $a2 _not_basic_type_5_
_eq_str_5_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_5_
	beq $t3 $0 _eq_true_5_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_5_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_5_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_5_
	b _eq_true_5_
_not_basic_type_5_:
	bne $t0 $t1 _eq_false_5_
	b _eq_true_5_
_eq_int_bool_5:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_5_
_eq_true_5_:
	li $a0 1
	sw $a0 -104($fp)
	b end_equal_5_
_eq_false_5_:
	li $a0 0
	sw $a0 -104($fp)
end_equal_5_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -108($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -108($fp)
	lw $a0 -104($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -108($fp)
	lw $a0 12($a1)
	sw $a0 -100($fp)
	
	# IF GOTO
	lw $a0, -100($fp)
	bnez $a0, _cil_label_LABEL_8
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -140($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -140($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -136($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -136($fp)
	lw $a0 -140($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -136($fp)
	la $a0, data_9
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -136($fp)
	beq $t0 $zero _eq_false_6_
	beq $t1 $zero _eq_false_6_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_6_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_6
	li $a2 5
	beq $a0 $a2 _eq_int_bool_6
	li $a2 6
	bne $a0 $a2 _not_basic_type_6_
_eq_str_6_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_6_
	beq $t3 $0 _eq_true_6_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_6_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_6_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_6_
	b _eq_true_6_
_not_basic_type_6_:
	bne $t0 $t1 _eq_false_6_
	b _eq_true_6_
_eq_int_bool_6:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_6_
_eq_true_6_:
	li $a0 1
	sw $a0 -128($fp)
	b end_equal_6_
_eq_false_6_:
	li $a0 0
	sw $a0 -128($fp)
end_equal_6_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -132($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -132($fp)
	lw $a0 -128($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -132($fp)
	lw $a0 12($a1)
	sw $a0 -124($fp)
	
	# IF GOTO
	lw $a0, -124($fp)
	bnez $a0, _cil_label_LABEL_10
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -164($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -164($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -160($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -160($fp)
	lw $a0 -164($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -160($fp)
	la $a0, data_10
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -160($fp)
	beq $t0 $zero _eq_false_7_
	beq $t1 $zero _eq_false_7_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_7_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_7
	li $a2 5
	beq $a0 $a2 _eq_int_bool_7
	li $a2 6
	bne $a0 $a2 _not_basic_type_7_
_eq_str_7_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_7_
	beq $t3 $0 _eq_true_7_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_7_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_7_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_7_
	b _eq_true_7_
_not_basic_type_7_:
	bne $t0 $t1 _eq_false_7_
	b _eq_true_7_
_eq_int_bool_7:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_7_
_eq_true_7_:
	li $a0 1
	sw $a0 -152($fp)
	b end_equal_7_
_eq_false_7_:
	li $a0 0
	sw $a0 -152($fp)
end_equal_7_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -156($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -156($fp)
	lw $a0 -152($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -156($fp)
	lw $a0 12($a1)
	sw $a0 -148($fp)
	
	# IF GOTO
	lw $a0, -148($fp)
	bnez $a0, _cil_label_LABEL_12
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -188($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -188($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -184($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -184($fp)
	lw $a0 -188($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -184($fp)
	la $a0, data_11
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -184($fp)
	beq $t0 $zero _eq_false_8_
	beq $t1 $zero _eq_false_8_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_8_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_8
	li $a2 5
	beq $a0 $a2 _eq_int_bool_8
	li $a2 6
	bne $a0 $a2 _not_basic_type_8_
_eq_str_8_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_8_
	beq $t3 $0 _eq_true_8_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_8_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_8_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_8_
	b _eq_true_8_
_not_basic_type_8_:
	bne $t0 $t1 _eq_false_8_
	b _eq_true_8_
_eq_int_bool_8:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_8_
_eq_true_8_:
	li $a0 1
	sw $a0 -176($fp)
	b end_equal_8_
_eq_false_8_:
	li $a0 0
	sw $a0 -176($fp)
end_equal_8_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -180($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -180($fp)
	lw $a0 -176($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -180($fp)
	lw $a0 12($a1)
	sw $a0 -172($fp)
	
	# IF GOTO
	lw $a0, -172($fp)
	bnez $a0, _cil_label_LABEL_14
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -212($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -212($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -208($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -208($fp)
	lw $a0 -212($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -208($fp)
	la $a0, data_12
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -208($fp)
	beq $t0 $zero _eq_false_9_
	beq $t1 $zero _eq_false_9_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_9_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_9
	li $a2 5
	beq $a0 $a2 _eq_int_bool_9
	li $a2 6
	bne $a0 $a2 _not_basic_type_9_
_eq_str_9_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_9_
	beq $t3 $0 _eq_true_9_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_9_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_9_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_9_
	b _eq_true_9_
_not_basic_type_9_:
	bne $t0 $t1 _eq_false_9_
	b _eq_true_9_
_eq_int_bool_9:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_9_
_eq_true_9_:
	li $a0 1
	sw $a0 -200($fp)
	b end_equal_9_
_eq_false_9_:
	li $a0 0
	sw $a0 -200($fp)
end_equal_9_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -204($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -204($fp)
	lw $a0 -200($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -204($fp)
	lw $a0 12($a1)
	sw $a0 -196($fp)
	
	# IF GOTO
	lw $a0, -196($fp)
	bnez $a0, _cil_label_LABEL_16
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -236($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -236($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -232($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -232($fp)
	lw $a0 -236($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -232($fp)
	la $a0, data_13
	sw $a0 16($a1)
	
	lw $t0 16($fp)
	lw $t1 -232($fp)
	beq $t0 $zero _eq_false_10_
	beq $t1 $zero _eq_false_10_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_10_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_10
	li $a2 5
	beq $a0 $a2 _eq_int_bool_10
	li $a2 6
	bne $a0 $a2 _not_basic_type_10_
_eq_str_10_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_10_
	beq $t3 $0 _eq_true_10_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_10_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_10_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_10_
	b _eq_true_10_
_not_basic_type_10_:
	bne $t0 $t1 _eq_false_10_
	b _eq_true_10_
_eq_int_bool_10:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_10_
_eq_true_10_:
	li $a0 1
	sw $a0 -224($fp)
	b end_equal_10_
_eq_false_10_:
	li $a0 0
	sw $a0 -224($fp)
end_equal_10_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -228($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -228($fp)
	lw $a0 -224($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -228($fp)
	lw $a0 12($a1)
	sw $a0 -220($fp)
	
	# IF GOTO
	lw $a0, -220($fp)
	bnez $a0, _cil_label_LABEL_18
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -240($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -240($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 0($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -244($fp)
	lw $a2, -240($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -248($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -248($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -248($fp)
	sw $a0, -216($fp)
	
	# GOTO
	j _cil_label_LABEL_19
	
_cil_label_LABEL_18:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -252($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -252($fp)
	li $a0, 9
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -252($fp)
	sw $a0, -216($fp)
	
_cil_label_LABEL_19:
	# ASSIGN
	lw $a0, -216($fp)
	sw $a0, -192($fp)
	
	# GOTO
	j _cil_label_LABEL_17
	
_cil_label_LABEL_16:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -256($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -256($fp)
	li $a0, 8
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -256($fp)
	sw $a0, -192($fp)
	
_cil_label_LABEL_17:
	# ASSIGN
	lw $a0, -192($fp)
	sw $a0, -168($fp)
	
	# GOTO
	j _cil_label_LABEL_15
	
_cil_label_LABEL_14:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -260($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -260($fp)
	li $a0, 7
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -260($fp)
	sw $a0, -168($fp)
	
_cil_label_LABEL_15:
	# ASSIGN
	lw $a0, -168($fp)
	sw $a0, -144($fp)
	
	# GOTO
	j _cil_label_LABEL_13
	
_cil_label_LABEL_12:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -264($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -264($fp)
	li $a0, 6
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -264($fp)
	sw $a0, -144($fp)
	
_cil_label_LABEL_13:
	# ASSIGN
	lw $a0, -144($fp)
	sw $a0, -120($fp)
	
	# GOTO
	j _cil_label_LABEL_11
	
_cil_label_LABEL_10:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -268($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -268($fp)
	li $a0, 5
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -268($fp)
	sw $a0, -120($fp)
	
_cil_label_LABEL_11:
	# ASSIGN
	lw $a0, -120($fp)
	sw $a0, -96($fp)
	
	# GOTO
	j _cil_label_LABEL_9
	
_cil_label_LABEL_8:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -272($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -272($fp)
	li $a0, 4
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -272($fp)
	sw $a0, -96($fp)
	
_cil_label_LABEL_9:
	# ASSIGN
	lw $a0, -96($fp)
	sw $a0, -72($fp)
	
	# GOTO
	j _cil_label_LABEL_7
	
_cil_label_LABEL_6:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -276($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -276($fp)
	li $a0, 3
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -276($fp)
	sw $a0, -72($fp)
	
_cil_label_LABEL_7:
	# ASSIGN
	lw $a0, -72($fp)
	sw $a0, -48($fp)
	
	# GOTO
	j _cil_label_LABEL_5
	
_cil_label_LABEL_4:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -280($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -280($fp)
	li $a0, 2
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -280($fp)
	sw $a0, -48($fp)
	
_cil_label_LABEL_5:
	# ASSIGN
	lw $a0, -48($fp)
	sw $a0, -24($fp)
	
	# GOTO
	j _cil_label_LABEL_3
	
_cil_label_LABEL_2:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -284($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -284($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -284($fp)
	sw $a0, -24($fp)
	
_cil_label_LABEL_3:
	# ASSIGN
	lw $a0, -24($fp)
	sw $a0, 0($fp)
	
	# GOTO
	j _cil_label_LABEL_1
	
_cil_label_LABEL_0:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -288($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -288($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -288($fp)
	sw $a0, 0($fp)
	
_cil_label_LABEL_1:
	# RETURN
	lw $v0, 0($fp)
	addiu $sp, $sp, 292
	jr $ra
	
function_A2I_i2c:
	move $fp, $sp
	subu $sp, $sp, 296
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -16($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -16($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -16($fp)
	beq $t0 $zero _eq_false_11_
	beq $t1 $zero _eq_false_11_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_11_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_11
	li $a2 5
	beq $a0 $a2 _eq_int_bool_11
	li $a2 6
	bne $a0 $a2 _not_basic_type_11_
_eq_str_11_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_11_
	beq $t3 $0 _eq_true_11_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_11_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_11_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_11_
	b _eq_true_11_
_not_basic_type_11_:
	bne $t0 $t1 _eq_false_11_
	b _eq_true_11_
_eq_int_bool_11:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_11_
_eq_true_11_:
	li $a0 1
	sw $a0 -8($fp)
	b end_equal_11_
_eq_false_11_:
	li $a0 0
	sw $a0 -8($fp)
end_equal_11_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -12($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -12($fp)
	lw $a0 -8($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -12($fp)
	lw $a0 12($a1)
	sw $a0 -4($fp)
	
	# IF GOTO
	lw $a0, -4($fp)
	bnez $a0, _cil_label_LABEL_20
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -36($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -36($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -36($fp)
	beq $t0 $zero _eq_false_12_
	beq $t1 $zero _eq_false_12_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_12_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_12
	li $a2 5
	beq $a0 $a2 _eq_int_bool_12
	li $a2 6
	bne $a0 $a2 _not_basic_type_12_
_eq_str_12_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_12_
	beq $t3 $0 _eq_true_12_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_12_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_12_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_12_
	b _eq_true_12_
_not_basic_type_12_:
	bne $t0 $t1 _eq_false_12_
	b _eq_true_12_
_eq_int_bool_12:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_12_
_eq_true_12_:
	li $a0 1
	sw $a0 -28($fp)
	b end_equal_12_
_eq_false_12_:
	li $a0 0
	sw $a0 -28($fp)
end_equal_12_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -32($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -32($fp)
	lw $a0 -28($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -32($fp)
	lw $a0 12($a1)
	sw $a0 -24($fp)
	
	# IF GOTO
	lw $a0, -24($fp)
	bnez $a0, _cil_label_LABEL_22
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -56($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -56($fp)
	li $a0, 2
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -56($fp)
	beq $t0 $zero _eq_false_13_
	beq $t1 $zero _eq_false_13_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_13_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_13
	li $a2 5
	beq $a0 $a2 _eq_int_bool_13
	li $a2 6
	bne $a0 $a2 _not_basic_type_13_
_eq_str_13_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_13_
	beq $t3 $0 _eq_true_13_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_13_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_13_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_13_
	b _eq_true_13_
_not_basic_type_13_:
	bne $t0 $t1 _eq_false_13_
	b _eq_true_13_
_eq_int_bool_13:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_13_
_eq_true_13_:
	li $a0 1
	sw $a0 -48($fp)
	b end_equal_13_
_eq_false_13_:
	li $a0 0
	sw $a0 -48($fp)
end_equal_13_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -52($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -52($fp)
	lw $a0 -48($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -52($fp)
	lw $a0 12($a1)
	sw $a0 -44($fp)
	
	# IF GOTO
	lw $a0, -44($fp)
	bnez $a0, _cil_label_LABEL_24
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -76($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -76($fp)
	li $a0, 3
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -76($fp)
	beq $t0 $zero _eq_false_14_
	beq $t1 $zero _eq_false_14_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_14_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_14
	li $a2 5
	beq $a0 $a2 _eq_int_bool_14
	li $a2 6
	bne $a0 $a2 _not_basic_type_14_
_eq_str_14_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_14_
	beq $t3 $0 _eq_true_14_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_14_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_14_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_14_
	b _eq_true_14_
_not_basic_type_14_:
	bne $t0 $t1 _eq_false_14_
	b _eq_true_14_
_eq_int_bool_14:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_14_
_eq_true_14_:
	li $a0 1
	sw $a0 -68($fp)
	b end_equal_14_
_eq_false_14_:
	li $a0 0
	sw $a0 -68($fp)
end_equal_14_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -72($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -72($fp)
	lw $a0 -68($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -72($fp)
	lw $a0 12($a1)
	sw $a0 -64($fp)
	
	# IF GOTO
	lw $a0, -64($fp)
	bnez $a0, _cil_label_LABEL_26
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -96($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -96($fp)
	li $a0, 4
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -96($fp)
	beq $t0 $zero _eq_false_15_
	beq $t1 $zero _eq_false_15_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_15_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_15
	li $a2 5
	beq $a0 $a2 _eq_int_bool_15
	li $a2 6
	bne $a0 $a2 _not_basic_type_15_
_eq_str_15_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_15_
	beq $t3 $0 _eq_true_15_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_15_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_15_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_15_
	b _eq_true_15_
_not_basic_type_15_:
	bne $t0 $t1 _eq_false_15_
	b _eq_true_15_
_eq_int_bool_15:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_15_
_eq_true_15_:
	li $a0 1
	sw $a0 -88($fp)
	b end_equal_15_
_eq_false_15_:
	li $a0 0
	sw $a0 -88($fp)
end_equal_15_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -92($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -92($fp)
	lw $a0 -88($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -92($fp)
	lw $a0 12($a1)
	sw $a0 -84($fp)
	
	# IF GOTO
	lw $a0, -84($fp)
	bnez $a0, _cil_label_LABEL_28
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -116($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -116($fp)
	li $a0, 5
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -116($fp)
	beq $t0 $zero _eq_false_16_
	beq $t1 $zero _eq_false_16_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_16_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_16
	li $a2 5
	beq $a0 $a2 _eq_int_bool_16
	li $a2 6
	bne $a0 $a2 _not_basic_type_16_
_eq_str_16_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_16_
	beq $t3 $0 _eq_true_16_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_16_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_16_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_16_
	b _eq_true_16_
_not_basic_type_16_:
	bne $t0 $t1 _eq_false_16_
	b _eq_true_16_
_eq_int_bool_16:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_16_
_eq_true_16_:
	li $a0 1
	sw $a0 -108($fp)
	b end_equal_16_
_eq_false_16_:
	li $a0 0
	sw $a0 -108($fp)
end_equal_16_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -112($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -112($fp)
	lw $a0 -108($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -112($fp)
	lw $a0 12($a1)
	sw $a0 -104($fp)
	
	# IF GOTO
	lw $a0, -104($fp)
	bnez $a0, _cil_label_LABEL_30
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -136($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -136($fp)
	li $a0, 6
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -136($fp)
	beq $t0 $zero _eq_false_17_
	beq $t1 $zero _eq_false_17_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_17_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_17
	li $a2 5
	beq $a0 $a2 _eq_int_bool_17
	li $a2 6
	bne $a0 $a2 _not_basic_type_17_
_eq_str_17_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_17_
	beq $t3 $0 _eq_true_17_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_17_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_17_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_17_
	b _eq_true_17_
_not_basic_type_17_:
	bne $t0 $t1 _eq_false_17_
	b _eq_true_17_
_eq_int_bool_17:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_17_
_eq_true_17_:
	li $a0 1
	sw $a0 -128($fp)
	b end_equal_17_
_eq_false_17_:
	li $a0 0
	sw $a0 -128($fp)
end_equal_17_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -132($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -132($fp)
	lw $a0 -128($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -132($fp)
	lw $a0 12($a1)
	sw $a0 -124($fp)
	
	# IF GOTO
	lw $a0, -124($fp)
	bnez $a0, _cil_label_LABEL_32
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -156($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -156($fp)
	li $a0, 7
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -156($fp)
	beq $t0 $zero _eq_false_18_
	beq $t1 $zero _eq_false_18_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_18_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_18
	li $a2 5
	beq $a0 $a2 _eq_int_bool_18
	li $a2 6
	bne $a0 $a2 _not_basic_type_18_
_eq_str_18_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_18_
	beq $t3 $0 _eq_true_18_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_18_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_18_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_18_
	b _eq_true_18_
_not_basic_type_18_:
	bne $t0 $t1 _eq_false_18_
	b _eq_true_18_
_eq_int_bool_18:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_18_
_eq_true_18_:
	li $a0 1
	sw $a0 -148($fp)
	b end_equal_18_
_eq_false_18_:
	li $a0 0
	sw $a0 -148($fp)
end_equal_18_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -152($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -152($fp)
	lw $a0 -148($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -152($fp)
	lw $a0 12($a1)
	sw $a0 -144($fp)
	
	# IF GOTO
	lw $a0, -144($fp)
	bnez $a0, _cil_label_LABEL_34
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -176($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -176($fp)
	li $a0, 8
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -176($fp)
	beq $t0 $zero _eq_false_19_
	beq $t1 $zero _eq_false_19_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_19_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_19
	li $a2 5
	beq $a0 $a2 _eq_int_bool_19
	li $a2 6
	bne $a0 $a2 _not_basic_type_19_
_eq_str_19_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_19_
	beq $t3 $0 _eq_true_19_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_19_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_19_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_19_
	b _eq_true_19_
_not_basic_type_19_:
	bne $t0 $t1 _eq_false_19_
	b _eq_true_19_
_eq_int_bool_19:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_19_
_eq_true_19_:
	li $a0 1
	sw $a0 -168($fp)
	b end_equal_19_
_eq_false_19_:
	li $a0 0
	sw $a0 -168($fp)
end_equal_19_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -172($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -172($fp)
	lw $a0 -168($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -172($fp)
	lw $a0 12($a1)
	sw $a0 -164($fp)
	
	# IF GOTO
	lw $a0, -164($fp)
	bnez $a0, _cil_label_LABEL_36
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -196($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -196($fp)
	li $a0, 9
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -196($fp)
	beq $t0 $zero _eq_false_20_
	beq $t1 $zero _eq_false_20_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_20_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_20
	li $a2 5
	beq $a0 $a2 _eq_int_bool_20
	li $a2 6
	bne $a0 $a2 _not_basic_type_20_
_eq_str_20_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_20_
	beq $t3 $0 _eq_true_20_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_20_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_20_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_20_
	b _eq_true_20_
_not_basic_type_20_:
	bne $t0 $t1 _eq_false_20_
	b _eq_true_20_
_eq_int_bool_20:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_20_
_eq_true_20_:
	li $a0 1
	sw $a0 -188($fp)
	b end_equal_20_
_eq_false_20_:
	li $a0 0
	sw $a0 -188($fp)
end_equal_20_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -192($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -192($fp)
	lw $a0 -188($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -192($fp)
	lw $a0 12($a1)
	sw $a0 -184($fp)
	
	# IF GOTO
	lw $a0, -184($fp)
	bnez $a0, _cil_label_LABEL_38
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -200($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -200($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 0($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -204($fp)
	lw $a2, -200($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -212($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -212($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -208($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -208($fp)
	lw $a0 -212($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -208($fp)
	la $a0, data_0
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -208($fp)
	sw $a0, -180($fp)
	
	# GOTO
	j _cil_label_LABEL_39
	
_cil_label_LABEL_38:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -220($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -220($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -216($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -216($fp)
	lw $a0 -220($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -216($fp)
	la $a0, data_13
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -216($fp)
	sw $a0, -180($fp)
	
_cil_label_LABEL_39:
	# ASSIGN
	lw $a0, -180($fp)
	sw $a0, -160($fp)
	
	# GOTO
	j _cil_label_LABEL_37
	
_cil_label_LABEL_36:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -228($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -228($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -224($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -224($fp)
	lw $a0 -228($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -224($fp)
	la $a0, data_12
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -224($fp)
	sw $a0, -160($fp)
	
_cil_label_LABEL_37:
	# ASSIGN
	lw $a0, -160($fp)
	sw $a0, -140($fp)
	
	# GOTO
	j _cil_label_LABEL_35
	
_cil_label_LABEL_34:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -236($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -236($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -232($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -232($fp)
	lw $a0 -236($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -232($fp)
	la $a0, data_11
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -232($fp)
	sw $a0, -140($fp)
	
_cil_label_LABEL_35:
	# ASSIGN
	lw $a0, -140($fp)
	sw $a0, -120($fp)
	
	# GOTO
	j _cil_label_LABEL_33
	
_cil_label_LABEL_32:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -244($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -244($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -240($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -240($fp)
	lw $a0 -244($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -240($fp)
	la $a0, data_10
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -240($fp)
	sw $a0, -120($fp)
	
_cil_label_LABEL_33:
	# ASSIGN
	lw $a0, -120($fp)
	sw $a0, -100($fp)
	
	# GOTO
	j _cil_label_LABEL_31
	
_cil_label_LABEL_30:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -252($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -252($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -248($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -248($fp)
	lw $a0 -252($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -248($fp)
	la $a0, data_9
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -248($fp)
	sw $a0, -100($fp)
	
_cil_label_LABEL_31:
	# ASSIGN
	lw $a0, -100($fp)
	sw $a0, -80($fp)
	
	# GOTO
	j _cil_label_LABEL_29
	
_cil_label_LABEL_28:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -260($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -260($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -256($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -256($fp)
	lw $a0 -260($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -256($fp)
	la $a0, data_8
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -256($fp)
	sw $a0, -80($fp)
	
_cil_label_LABEL_29:
	# ASSIGN
	lw $a0, -80($fp)
	sw $a0, -60($fp)
	
	# GOTO
	j _cil_label_LABEL_27
	
_cil_label_LABEL_26:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -268($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -268($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -264($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -264($fp)
	lw $a0 -268($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -264($fp)
	la $a0, data_7
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -264($fp)
	sw $a0, -60($fp)
	
_cil_label_LABEL_27:
	# ASSIGN
	lw $a0, -60($fp)
	sw $a0, -40($fp)
	
	# GOTO
	j _cil_label_LABEL_25
	
_cil_label_LABEL_24:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -276($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -276($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -272($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -272($fp)
	lw $a0 -276($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -272($fp)
	la $a0, data_6
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -272($fp)
	sw $a0, -40($fp)
	
_cil_label_LABEL_25:
	# ASSIGN
	lw $a0, -40($fp)
	sw $a0, -20($fp)
	
	# GOTO
	j _cil_label_LABEL_23
	
_cil_label_LABEL_22:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -284($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -284($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -280($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -280($fp)
	lw $a0 -284($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -280($fp)
	la $a0, data_5
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -280($fp)
	sw $a0, -20($fp)
	
_cil_label_LABEL_23:
	# ASSIGN
	lw $a0, -20($fp)
	sw $a0, 0($fp)
	
	# GOTO
	j _cil_label_LABEL_21
	
_cil_label_LABEL_20:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -292($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -292($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -288($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -288($fp)
	lw $a0 -292($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -288($fp)
	la $a0, data_4
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -288($fp)
	sw $a0, 0($fp)
	
_cil_label_LABEL_21:
	# RETURN
	lw $v0, 0($fp)
	addiu $sp, $sp, 296
	jr $ra
	
function_A2I_a2i:
	move $fp, $sp
	subu $sp, $sp, 228
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -16($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -16($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 12($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -20($fp)
	lw $a2, -16($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -24($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -24($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	lw $t0 -20($fp)
	lw $t1 -24($fp)
	beq $t0 $zero _eq_false_21_
	beq $t1 $zero _eq_false_21_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_21_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_21
	li $a2 5
	beq $a0 $a2 _eq_int_bool_21
	li $a2 6
	bne $a0 $a2 _not_basic_type_21_
_eq_str_21_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_21_
	beq $t3 $0 _eq_true_21_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_21_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_21_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_21_
	b _eq_true_21_
_not_basic_type_21_:
	bne $t0 $t1 _eq_false_21_
	b _eq_true_21_
_eq_int_bool_21:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_21_
_eq_true_21_:
	li $a0 1
	sw $a0 -8($fp)
	b end_equal_21_
_eq_false_21_:
	li $a0 0
	sw $a0 -8($fp)
end_equal_21_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -12($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -12($fp)
	lw $a0 -8($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -12($fp)
	lw $a0 12($a1)
	sw $a0 -4($fp)
	
	# IF GOTO
	lw $a0, -4($fp)
	bnez $a0, _cil_label_LABEL_40
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -52($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -52($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -52($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -56($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -56($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -56($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -44($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -44($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -48($fp)
	lw $a2, -44($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -64($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -64($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -60($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -60($fp)
	lw $a0 -64($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -60($fp)
	la $a0, data_14
	sw $a0 16($a1)
	
	lw $t0 -48($fp)
	lw $t1 -60($fp)
	beq $t0 $zero _eq_false_22_
	beq $t1 $zero _eq_false_22_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_22_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_22
	li $a2 5
	beq $a0 $a2 _eq_int_bool_22
	li $a2 6
	bne $a0 $a2 _not_basic_type_22_
_eq_str_22_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_22_
	beq $t3 $0 _eq_true_22_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_22_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_22_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_22_
	b _eq_true_22_
_not_basic_type_22_:
	bne $t0 $t1 _eq_false_22_
	b _eq_true_22_
_eq_int_bool_22:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_22_
_eq_true_22_:
	li $a0 1
	sw $a0 -36($fp)
	b end_equal_22_
_eq_false_22_:
	li $a0 0
	sw $a0 -36($fp)
end_equal_22_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -40($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -40($fp)
	lw $a0 -36($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -40($fp)
	lw $a0 12($a1)
	sw $a0 -32($fp)
	
	# IF GOTO
	lw $a0, -32($fp)
	bnez $a0, _cil_label_LABEL_42
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -92($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -92($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -92($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -96($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -96($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -96($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -84($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -84($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -88($fp)
	lw $a2, -84($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -104($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -104($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -100($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -100($fp)
	lw $a0 -104($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -100($fp)
	la $a0, data_15
	sw $a0 16($a1)
	
	lw $t0 -88($fp)
	lw $t1 -100($fp)
	beq $t0 $zero _eq_false_23_
	beq $t1 $zero _eq_false_23_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_23_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_23
	li $a2 5
	beq $a0 $a2 _eq_int_bool_23
	li $a2 6
	bne $a0 $a2 _not_basic_type_23_
_eq_str_23_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_23_
	beq $t3 $0 _eq_true_23_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_23_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_23_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_23_
	b _eq_true_23_
_not_basic_type_23_:
	bne $t0 $t1 _eq_false_23_
	b _eq_true_23_
_eq_int_bool_23:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_23_
_eq_true_23_:
	li $a0 1
	sw $a0 -76($fp)
	b end_equal_23_
_eq_false_23_:
	li $a0 0
	sw $a0 -76($fp)
end_equal_23_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -80($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -80($fp)
	lw $a0 -76($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -80($fp)
	lw $a0 12($a1)
	sw $a0 -72($fp)
	
	# IF GOTO
	lw $a0, -72($fp)
	bnez $a0, _cil_label_LABEL_44
	
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -108($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -108($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -112($fp)
	lw $a2, -108($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ASSIGN
	lw $a0, -112($fp)
	sw $a0, -68($fp)
	
	# GOTO
	j _cil_label_LABEL_45
	
_cil_label_LABEL_44:
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -148($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -148($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 12($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -152($fp)
	lw $a2, -148($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -156($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -156($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -152($fp)
	lw $a0 12($a1)
	sw $a0 -136($fp)
	
	# GETATTR
	lw $a1 -156($fp)
	lw $a0 12($a1)
	sw $a0 -140($fp)
	
	# -
	lw $a0, -136($fp)
	lw $a1, -140($fp)
	sub $a0, $a0, $a1
	sw $a0, -132($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -144($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -144($fp)
	lw $a0 -132($fp)
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -144($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -160($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -160($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -160($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -124($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -124($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -128($fp)
	lw $a2, -124($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -128($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -116($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -116($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -120($fp)
	lw $a2, -116($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ASSIGN
	lw $a0, -120($fp)
	sw $a0, -68($fp)
	
_cil_label_LABEL_45:
	# ASSIGN
	lw $a0, -68($fp)
	sw $a0, -28($fp)
	
	# GOTO
	j _cil_label_LABEL_43
	
_cil_label_LABEL_42:
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -208($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -208($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 12($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -212($fp)
	lw $a2, -208($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -216($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -216($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -212($fp)
	lw $a0 12($a1)
	sw $a0 -196($fp)
	
	# GETATTR
	lw $a1 -216($fp)
	lw $a0 12($a1)
	sw $a0 -200($fp)
	
	# -
	lw $a0, -196($fp)
	lw $a1, -200($fp)
	sub $a0, $a0, $a1
	sw $a0, -192($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -204($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -204($fp)
	lw $a0 -192($fp)
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -204($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -220($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -220($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -220($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -184($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -184($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -188($fp)
	lw $a2, -184($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -188($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -176($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -176($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -180($fp)
	lw $a2, -176($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# GETATTR
	lw $a1 -180($fp)
	lw $a0 12($a1)
	sw $a0 -164($fp)
	
	# -
	li $a0 0
	lw $a1, -164($fp)
	sub $a0, $a0, $a1
	sw $a0, -168($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -172($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -172($fp)
	lw $a0 -168($fp)
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -172($fp)
	sw $a0, -28($fp)
	
_cil_label_LABEL_43:
	# ASSIGN
	lw $a0, -28($fp)
	sw $a0, 0($fp)
	
	# GOTO
	j _cil_label_LABEL_41
	
_cil_label_LABEL_40:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -224($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -224($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -224($fp)
	sw $a0, 0($fp)
	
_cil_label_LABEL_41:
	# RETURN
	lw $v0, 0($fp)
	addiu $sp, $sp, 228
	jr $ra
	
function_A2I_a2i_aux:
	move $fp, $sp
	subu $sp, $sp, 116
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 0($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 0($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -4($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -4($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 12($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -8($fp)
	lw $a2, -4($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -12($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -12($fp)
	li $a0, 0
	sw $a0 12($a1)
	
_cil_label_LABEL_46:
	# GETATTR
	lw $a1 -12($fp)
	lw $a0 12($a1)
	sw $a0 -28($fp)
	
	# GETATTR
	lw $a1 -8($fp)
	lw $a0 12($a1)
	sw $a0 -32($fp)
	
	# <
	lw $a1, -28($fp)
	lw $a2, -32($fp)
	slt $a0, $a1, $a2
	sw $a0, -24($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -36($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -36($fp)
	lw $a0 -24($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -36($fp)
	lw $a0 12($a1)
	sw $a0 -20($fp)
	
	# IF GOTO
	lw $a0, -20($fp)
	bnez $a0, _cil_label_LABEL_47
	
	# GOTO
	j _cil_label_LABEL_48
	
_cil_label_LABEL_47:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -72($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -72($fp)
	li $a0, 10
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 0($fp)
	lw $a0 12($a1)
	sw $a0 -60($fp)
	
	# GETATTR
	lw $a1 -72($fp)
	lw $a0 12($a1)
	sw $a0 -64($fp)
	
	# *
	lw $a0, -60($fp)
	lw $a1, -64($fp)
	mul $a0, $a0, $a1
	sw $a0, -56($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -68($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -68($fp)
	lw $a0 -56($fp)
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -92($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -92($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -92($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, -12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 16($fp)
	lw $a0 0($a1)
	sw $a0 -84($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -84($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -88($fp)
	lw $a2, -84($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -88($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -76($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -76($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 12($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -80($fp)
	lw $a2, -76($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# GETATTR
	lw $a1 -68($fp)
	lw $a0 12($a1)
	sw $a0 -44($fp)
	
	# GETATTR
	lw $a1 -80($fp)
	lw $a0 12($a1)
	sw $a0 -48($fp)
	
	# +
	lw $a0, -44($fp)
	lw $a1, -48($fp)
	add $a0, $a0, $a1
	sw $a0, -40($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -52($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -52($fp)
	lw $a0 -40($fp)
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -52($fp)
	sw $a0, 0($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -112($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -112($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -12($fp)
	lw $a0 12($a1)
	sw $a0 -100($fp)
	
	# GETATTR
	lw $a1 -112($fp)
	lw $a0 12($a1)
	sw $a0 -104($fp)
	
	# +
	lw $a0, -100($fp)
	lw $a1, -104($fp)
	add $a0, $a0, $a1
	sw $a0, -96($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -108($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -108($fp)
	lw $a0 -96($fp)
	sw $a0 12($a1)
	
	# ASSIGN
	lw $a0, -108($fp)
	sw $a0, -12($fp)
	
	# GOTO
	j _cil_label_LABEL_46
	
_cil_label_LABEL_48:
	# ALLOCATE
	la $v0 type_void
	sw $v0 -16($fp)
	
	# RETURN
	lw $v0, 0($fp)
	addiu $sp, $sp, 116
	jr $ra
	
function_A2I_i2a:
	move $fp, $sp
	subu $sp, $sp, 120
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -16($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -16($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -16($fp)
	beq $t0 $zero _eq_false_24_
	beq $t1 $zero _eq_false_24_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_24_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_24
	li $a2 5
	beq $a0 $a2 _eq_int_bool_24
	li $a2 6
	bne $a0 $a2 _not_basic_type_24_
_eq_str_24_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_24_
	beq $t3 $0 _eq_true_24_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_24_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_24_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_24_
	b _eq_true_24_
_not_basic_type_24_:
	bne $t0 $t1 _eq_false_24_
	b _eq_true_24_
_eq_int_bool_24:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_24_
_eq_true_24_:
	li $a0 1
	sw $a0 -8($fp)
	b end_equal_24_
_eq_false_24_:
	li $a0 0
	sw $a0 -8($fp)
end_equal_24_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -12($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -12($fp)
	lw $a0 -8($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -12($fp)
	lw $a0 12($a1)
	sw $a0 -4($fp)
	
	# IF GOTO
	lw $a0, -4($fp)
	bnez $a0, _cil_label_LABEL_49
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -44($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -44($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -44($fp)
	lw $a0 12($a1)
	sw $a0 -32($fp)
	
	# GETATTR
	lw $a1 16($fp)
	lw $a0 12($a1)
	sw $a0 -36($fp)
	
	# <
	lw $a1, -32($fp)
	lw $a2, -36($fp)
	slt $a0, $a1, $a2
	sw $a0, -28($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -40($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -40($fp)
	lw $a0 -28($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -40($fp)
	lw $a0 12($a1)
	sw $a0 -24($fp)
	
	# IF GOTO
	lw $a0, -24($fp)
	bnez $a0, _cil_label_LABEL_51
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -52($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -52($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -48($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -48($fp)
	lw $a0 -52($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -48($fp)
	la $a0, data_14
	sw $a0 16($a1)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -100($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -100($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -100($fp)
	lw $a0 12($a1)
	sw $a0 -88($fp)
	
	# -
	li $a0 0
	lw $a1, -88($fp)
	sub $a0, $a0, $a1
	sw $a0, -92($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -96($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -96($fp)
	lw $a0 -92($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 16($fp)
	lw $a0 12($a1)
	sw $a0 -76($fp)
	
	# GETATTR
	lw $a1 -96($fp)
	lw $a0 12($a1)
	sw $a0 -80($fp)
	
	# *
	lw $a0, -76($fp)
	lw $a1, -80($fp)
	mul $a0, $a0, $a1
	sw $a0, -72($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -84($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -84($fp)
	lw $a0 -72($fp)
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -84($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -64($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -64($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 32($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -68($fp)
	lw $a2, -64($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -68($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, -48($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -48($fp)
	lw $a0 0($a1)
	sw $a0 -56($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -56($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 16($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -60($fp)
	lw $a2, -56($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ASSIGN
	lw $a0, -60($fp)
	sw $a0, -20($fp)
	
	# GOTO
	j _cil_label_LABEL_52
	
_cil_label_LABEL_51:
	# PUSHPARAM
	lw $a0, 16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -104($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -104($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 32($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -108($fp)
	lw $a2, -104($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ASSIGN
	lw $a0, -108($fp)
	sw $a0, -20($fp)
	
_cil_label_LABEL_52:
	# ASSIGN
	lw $a0, -20($fp)
	sw $a0, 0($fp)
	
	# GOTO
	j _cil_label_LABEL_50
	
_cil_label_LABEL_49:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -116($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -116($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -112($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -112($fp)
	lw $a0 -116($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -112($fp)
	la $a0, data_4
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -112($fp)
	sw $a0, 0($fp)
	
_cil_label_LABEL_50:
	# RETURN
	lw $v0, 0($fp)
	addiu $sp, $sp, 120
	jr $ra
	
function_A2I_i2a_aux:
	move $fp, $sp
	subu $sp, $sp, 108
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -16($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -16($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	lw $t0 16($fp)
	lw $t1 -16($fp)
	beq $t0 $zero _eq_false_25_
	beq $t1 $zero _eq_false_25_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_25_
	li $a2 4
	beq $a0 $a2 _eq_int_bool_25
	li $a2 5
	beq $a0 $a2 _eq_int_bool_25
	li $a2 6
	bne $a0 $a2 _not_basic_type_25_
_eq_str_25_:
	lw	$t3 12($t0)
	lw	$t3 12($t3)
	lw	$t4, 12($t1)
	lw	$t4, 12($t4)
	bne $t3 $t4 _eq_false_25_
	beq $t3 $0 _eq_true_25_
	addu $t0 $t0 16
	lw $t0 0($t0)
	addu $t1 $t1 16
	lw $t1 0($t1)
	move $t2 $t3
_verify_ascii_sequences_25_:
	lb $a0 0($t0)
	lb $a1 0($t1)
	bne $a0 $a1 _eq_false_25_
	addu $t0 $t0 1
	addu $t1 $t1 1
	addiu $t2 $t2 -1
	bnez $t2 _verify_ascii_sequences_25_
	b _eq_true_25_
_not_basic_type_25_:
	bne $t0 $t1 _eq_false_25_
	b _eq_true_25_
_eq_int_bool_25:
	lw $a3 12($t0)
	lw $t4 12($t1)
	bne $a3 $t4 _eq_false_25_
_eq_true_25_:
	li $a0 1
	sw $a0 -8($fp)
	b end_equal_25_
_eq_false_25_:
	li $a0 0
	sw $a0 -8($fp)
end_equal_25_:
	# ALLOCATE
	lw $t0 40($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -12($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -12($fp)
	lw $a0 -8($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -12($fp)
	lw $a0 12($a1)
	sw $a0 -4($fp)
	
	# IF GOTO
	lw $a0, -4($fp)
	bnez $a0, _cil_label_LABEL_53
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -36($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -36($fp)
	li $a0, 10
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 16($fp)
	lw $a0 12($a1)
	sw $a0 -24($fp)
	
	# GETATTR
	lw $a1 -36($fp)
	lw $a0 12($a1)
	sw $a0 -28($fp)
	
	# /
	lw $a0, -24($fp)
	lw $a1, -28($fp)
	beqz $a1 _div_error_26_
	div $a0, $a0, $a1
	sw $a0, -20($fp)
	b _div_end_26_
_div_error_26_:
	la $a0 _div_zero_msg
	li $v0 4
	syscall
	la $a0 _abort_msg
	li $v0 4
	syscall
	li $v0 10
	syscall
_div_end_26_:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -32($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -32($fp)
	lw $a0 -20($fp)
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -32($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -40($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -40($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 32($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -44($fp)
	lw $a2, -40($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -96($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -96($fp)
	li $a0, 10
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 -32($fp)
	lw $a0 12($a1)
	sw $a0 -84($fp)
	
	# GETATTR
	lw $a1 -96($fp)
	lw $a0 12($a1)
	sw $a0 -88($fp)
	
	# *
	lw $a0, -84($fp)
	lw $a1, -88($fp)
	mul $a0, $a0, $a1
	sw $a0, -80($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -92($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -92($fp)
	lw $a0 -80($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 16($fp)
	lw $a0 12($a1)
	sw $a0 -68($fp)
	
	# GETATTR
	lw $a1 -92($fp)
	lw $a0 12($a1)
	sw $a0 -72($fp)
	
	# -
	lw $a0, -68($fp)
	lw $a1, -72($fp)
	sub $a0, $a0, $a1
	sw $a0, -64($fp)
	
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -76($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -76($fp)
	lw $a0 -64($fp)
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -76($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, 12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 12($fp)
	lw $a0 0($a1)
	sw $a0 -56($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -56($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 16($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -60($fp)
	lw $a2, -56($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -60($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, -44($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -44($fp)
	lw $a0 0($a1)
	sw $a0 -48($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -48($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 16($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -52($fp)
	lw $a2, -48($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ASSIGN
	lw $a0, -52($fp)
	sw $a0, 0($fp)
	
	# GOTO
	j _cil_label_LABEL_54
	
_cil_label_LABEL_53:
	# ALLOCATE
	lw $t0 32($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -104($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -104($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	# ALLOCATE
	lw $t0 48($s0)
	sw $t0, 0($sp)
	addiu $sp, $sp, -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Object_copy
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -100($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -100($fp)
	lw $a0 -104($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -100($fp)
	la $a0, data_0
	sw $a0 16($a1)
	
	# ASSIGN
	lw $a0, -100($fp)
	sw $a0, 0($fp)
	
_cil_label_LABEL_54:
	# RETURN
	lw $v0, 0($fp)
	addiu $sp, $sp, 108
	jr $ra
	
	
#####################################

