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
 			.asciiz "=(\n"
	data_2: .align 2 
 			.asciiz "=)\n"
	data_3: .align 2 
 			.asciiz "+"
	data_4: .align 2 
 			.asciiz "I"
	
	classname_void: .align 2 
			.asciiz "void"
	classname_Object: .align 2 
			.asciiz "Object"
	classname_IO: .align 2 
			.asciiz "IO"
	classname_Main: .align 2 
			.asciiz "Main"
	classname_Complex: .align 2 
			.asciiz "Complex"
	classname_Int: .align 2 
			.asciiz "Int"
	classname_Bool: .align 2 
			.asciiz "Bool"
	classname_String: .align 2 
			.asciiz "String"
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
	
	addiu $sp, $sp, 4
	
	move $v1 $v0
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
	
	move $v1 $v0
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
	
	addiu $sp, $sp, 4
	
	move $v1 $v0
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
	
	move $t0 $v0
	li $v0 5
	syscall
	sw $v0 12($t0)
	move $v0 $t0
	jr $ra
	
function_IO_in_string:
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
	
	move $v1 $v0
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
	la $t1 classname_Complex
	sw $t1 16($s1)
	la $t1 classname_Int
	sw $t1 20($s1)
	la $t1 classname_Bool
	sw $t1 24($s1)
	la $t1 classname_String
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
	
	# Type Complex
	li $a0 20
	li $v0 9
	syscall
	li $a0 4
	sw $a0 0($v0)
	li $a0 20
	sw $a0 4($v0)
	sw $v0 32($s0)
	
	# Type Int
	li $a0 16
	li $v0 9
	syscall
	li $a0 5
	sw $a0 0($v0)
	li $a0 16
	sw $a0 4($v0)
	sw $v0 40($s0)
	
	# Type Bool
	li $a0 16
	li $v0 9
	syscall
	li $a0 6
	sw $a0 0($v0)
	li $a0 16
	sw $a0 4($v0)
	sw $v0 48($s0)
	
	# Type String
	li $a0 20
	li $v0 9
	syscall
	li $a0 7
	sw $a0 0($v0)
	li $a0 20
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
	
	# Type Complex
	li $a0 48
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
	la $t1 function_Complex_init
	sw $t1 28($v0)
	la $t1 function_Complex_print
	sw $t1 32($v0)
	la $t1 function_Complex_reflect_0
	sw $t1 36($v0)
	la $t1 function_Complex_reflect_X
	sw $t1 40($v0)
	la $t1 function_Complex_reflect_Y
	sw $t1 44($v0)
	lw $t0 32($s0)
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
	lw $t0 40($s0)
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
	lw $t0 48($s0)
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
	
	li $t0 4
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
	subu $sp, $sp, 96
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
	
	# PUSHPARAM
	lw $a0, 0($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Complex__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -4($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
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
	sw $v0 -16($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -16($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -16($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
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
	sw $v0 -20($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -20($fp)
	li $a0, 1
	sw $a0 12($a1)
	
	# PUSHPARAM
	lw $a0, -20($fp)
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
	lw $a0 28($a2)
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
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -12($fp)
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
	lw $a0 40($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -44($fp)
	lw $a2, -40($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
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
	lw $a0 44($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -52($fp)
	lw $a2, -48($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# PUSHPARAM
	lw $a0, -12($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -12($fp)
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
	lw $a0 36($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -60($fp)
	lw $a2, -56($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	lw $t0 -52($fp)
	lw $t1 -60($fp)
	beq $t0 $zero _eq_false_1_
	beq $t1 $zero _eq_false_1_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_1_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_1
	li $a2 6
	beq $a0 $a2 _eq_int_bool_1
	li $a2 7
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
	sw $a0 -32($fp)
	b end_equal_1_
_eq_false_1_:
	li $a0 0
	sw $a0 -32($fp)
end_equal_1_:
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
	bnez $a0, _cil_label_LABEL_0
	
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
	sw $v0 -76($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -76($fp)
	li $a0, 3
	sw $a0 12($a1)
	
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
	sw $v0 -72($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -72($fp)
	lw $a0 -76($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -72($fp)
	la $a0, data_1
	sw $a0 16($a1)
	
	# PUSHPARAM
	lw $a0, -72($fp)
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
	lw $a0 24($a2)
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
	
	# ASSIGN
	lw $a0, -68($fp)
	sw $a0, -24($fp)
	
	# GOTO
	j _cil_label_LABEL_1
	
_cil_label_LABEL_0:
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
	li $a0, 3
	sw $a0 12($a1)
	
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
	sw $v0 -88($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -88($fp)
	lw $a0 -92($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -88($fp)
	la $a0, data_2
	sw $a0 16($a1)
	
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
	sw $a0 -80($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -80($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -84($fp)
	lw $a2, -80($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ASSIGN
	lw $a0, -84($fp)
	sw $a0, -24($fp)
	
_cil_label_LABEL_1:
	# RETURN
	lw $v0, -24($fp)
	addiu $sp, $sp, 96
	jr $ra
	
function_Complex__init:
	move $fp, $sp
	subu $sp, $sp, 8
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
	jal function_Int__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 0($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# SETATTR
	lw $a1 12($fp)
	lw $a0 0($fp)
	sw $a0 12($a1)
	
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
	sw $v0 -4($fp)
	
	addiu $sp, $sp, 4
	
	# PUSHPARAM
	lw $a0, -4($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# CALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	jal function_Int__init
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -4($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# SETATTR
	lw $a1 12($fp)
	lw $a0 -4($fp)
	sw $a0 16($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 8
	jr $ra
	
function_Complex_init:
	move $fp, $sp
	subu $sp, $sp, 24
	# GETATTR
	lw $a1 12($fp)
	lw $a0 12($a1)
	sw $a0 -8($fp)
	
	lw $t0 -8($fp)
	lw $t1 16($fp)
	beq $t0 $zero _eq_false_2_
	beq $t1 $zero _eq_false_2_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_2_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_2
	li $a2 6
	beq $a0 $a2 _eq_int_bool_2
	li $a2 7
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
	sw $a0 0($fp)
	b end_equal_2_
_eq_false_2_:
	li $a0 0
	sw $a0 0($fp)
end_equal_2_:
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
	sw $v0 -4($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -4($fp)
	lw $a0 0($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 16($a1)
	sw $a0 -20($fp)
	
	lw $t0 -20($fp)
	lw $t1 20($fp)
	beq $t0 $zero _eq_false_3_
	beq $t1 $zero _eq_false_3_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_3_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_3
	li $a2 6
	beq $a0 $a2 _eq_int_bool_3
	li $a2 7
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
	sw $a0 -12($fp)
	b end_equal_3_
_eq_false_3_:
	li $a0 0
	sw $a0 -12($fp)
end_equal_3_:
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
	lw $a0 -12($fp)
	sw $a0 12($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 24
	jr $ra
	
function_Complex_print:
	move $fp, $sp
	subu $sp, $sp, 92
	# GETATTR
	lw $a1 12($fp)
	lw $a0 16($a1)
	sw $a0 -16($fp)
	
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
	sw $v0 -20($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -20($fp)
	li $a0, 0
	sw $a0 12($a1)
	
	lw $t0 -16($fp)
	lw $t1 -20($fp)
	beq $t0 $zero _eq_false_4_
	beq $t1 $zero _eq_false_4_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_4_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_4
	li $a2 6
	beq $a0 $a2 _eq_int_bool_4
	li $a2 7
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
	sw $a0 -8($fp)
	b end_equal_4_
_eq_false_4_:
	li $a0 0
	sw $a0 -8($fp)
end_equal_4_:
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
	bnez $a0, _cil_label_LABEL_2
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 12($a1)
	sw $a0 -32($fp)
	
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
	sw $a0 -24($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -24($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -28($fp)
	lw $a2, -24($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
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
	sw $v0 -48($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -48($fp)
	li $a0, 1
	sw $a0 12($a1)
	
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
	sw $v0 -44($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -44($fp)
	lw $a0 -48($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -44($fp)
	la $a0, data_3
	sw $a0 16($a1)
	
	# PUSHPARAM
	lw $a0, -44($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, -28($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -28($fp)
	lw $a0 0($a1)
	sw $a0 -36($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -36($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 24($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -40($fp)
	lw $a2, -36($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 16($a1)
	sw $a0 -60($fp)
	
	# PUSHPARAM
	lw $a0, -60($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, -40($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -40($fp)
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
	lw $a0 20($a2)
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
	sw $v0 -76($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -76($fp)
	li $a0, 1
	sw $a0 12($a1)
	
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
	sw $v0 -72($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -72($fp)
	lw $a0 -76($fp)
	sw $a0 12($a1)
	
	# SETATTR
	lw $a1 -72($fp)
	la $a0, data_4
	sw $a0 16($a1)
	
	# PUSHPARAM
	lw $a0, -72($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# PUSHPARAM
	lw $a0, -56($fp)
	sw $a0 0($sp)
	addiu $sp $sp -4
	
	# TYPEOF
	lw $a1 -56($fp)
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
	lw $a0 24($a2)
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
	
	# ASSIGN
	lw $a0, -68($fp)
	sw $a0, 0($fp)
	
	# GOTO
	j _cil_label_LABEL_3
	
_cil_label_LABEL_2:
	# GETATTR
	lw $a1 12($fp)
	lw $a0 12($a1)
	sw $a0 -88($fp)
	
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
	sw $a0 -80($fp)
	
	# VCALL
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 8($sp)
	lw $a2, -80($fp)
	mul $a2, $a2, 8
	addu $a2, $a2, $s0
	lw $a1, 0($a2)
	lw $a2, 8($a1)
	lw $a0 20($a2)
	jalr $a0
	lw $fp, 8($sp)
	lw $ra, 4($sp)
	addiu $sp, $sp, 8
	sw $v0 -84($fp)
	lw $a2, -80($fp)
	
	# POPPARAM
	addiu $sp $sp 4
	
	# POPPARAM
	addiu $sp $sp 4
	
	# ASSIGN
	lw $a0, -84($fp)
	sw $a0, 0($fp)
	
_cil_label_LABEL_3:
	# RETURN
	lw $v0, 0($fp)
	addiu $sp, $sp, 92
	jr $ra
	
function_Complex_reflect_0:
	move $fp, $sp
	subu $sp, $sp, 56
	# GETATTR
	lw $a1 12($fp)
	lw $a0 12($a1)
	sw $a0 -8($fp)
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 12($a1)
	sw $a0 -24($fp)
	
	# GETATTR
	lw $a1 -24($fp)
	lw $a0 12($a1)
	sw $a0 -12($fp)
	
	# -
	li $a0 0
	lw $a1, -12($fp)
	sub $a0, $a0, $a1
	sw $a0, -16($fp)
	
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
	sw $v0 -20($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -20($fp)
	lw $a0 -16($fp)
	sw $a0 12($a1)
	
	lw $t0 -8($fp)
	lw $t1 -20($fp)
	beq $t0 $zero _eq_false_5_
	beq $t1 $zero _eq_false_5_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_5_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_5
	li $a2 6
	beq $a0 $a2 _eq_int_bool_5
	li $a2 7
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
	sw $a0 0($fp)
	b end_equal_5_
_eq_false_5_:
	li $a0 0
	sw $a0 0($fp)
end_equal_5_:
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
	sw $v0 -4($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -4($fp)
	lw $a0 0($fp)
	sw $a0 12($a1)
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 16($a1)
	sw $a0 -36($fp)
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 16($a1)
	sw $a0 -52($fp)
	
	# GETATTR
	lw $a1 -52($fp)
	lw $a0 12($a1)
	sw $a0 -40($fp)
	
	# -
	li $a0 0
	lw $a1, -40($fp)
	sub $a0, $a0, $a1
	sw $a0, -44($fp)
	
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
	sw $v0 -48($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -48($fp)
	lw $a0 -44($fp)
	sw $a0 12($a1)
	
	lw $t0 -36($fp)
	lw $t1 -48($fp)
	beq $t0 $zero _eq_false_6_
	beq $t1 $zero _eq_false_6_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_6_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_6
	li $a2 6
	beq $a0 $a2 _eq_int_bool_6
	li $a2 7
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
	sw $a0 -28($fp)
	b end_equal_6_
_eq_false_6_:
	li $a0 0
	sw $a0 -28($fp)
end_equal_6_:
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
	sw $v0 -32($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -32($fp)
	lw $a0 -28($fp)
	sw $a0 12($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 56
	jr $ra
	
function_Complex_reflect_X:
	move $fp, $sp
	subu $sp, $sp, 28
	# GETATTR
	lw $a1 12($fp)
	lw $a0 16($a1)
	sw $a0 -8($fp)
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 16($a1)
	sw $a0 -24($fp)
	
	# GETATTR
	lw $a1 -24($fp)
	lw $a0 12($a1)
	sw $a0 -12($fp)
	
	# -
	li $a0 0
	lw $a1, -12($fp)
	sub $a0, $a0, $a1
	sw $a0, -16($fp)
	
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
	sw $v0 -20($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -20($fp)
	lw $a0 -16($fp)
	sw $a0 12($a1)
	
	lw $t0 -8($fp)
	lw $t1 -20($fp)
	beq $t0 $zero _eq_false_7_
	beq $t1 $zero _eq_false_7_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_7_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_7
	li $a2 6
	beq $a0 $a2 _eq_int_bool_7
	li $a2 7
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
	sw $a0 0($fp)
	b end_equal_7_
_eq_false_7_:
	li $a0 0
	sw $a0 0($fp)
end_equal_7_:
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
	sw $v0 -4($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -4($fp)
	lw $a0 0($fp)
	sw $a0 12($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 28
	jr $ra
	
function_Complex_reflect_Y:
	move $fp, $sp
	subu $sp, $sp, 28
	# GETATTR
	lw $a1 12($fp)
	lw $a0 12($a1)
	sw $a0 -8($fp)
	
	# GETATTR
	lw $a1 12($fp)
	lw $a0 12($a1)
	sw $a0 -24($fp)
	
	# GETATTR
	lw $a1 -24($fp)
	lw $a0 12($a1)
	sw $a0 -12($fp)
	
	# -
	li $a0 0
	lw $a1, -12($fp)
	sub $a0, $a0, $a1
	sw $a0, -16($fp)
	
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
	sw $v0 -20($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -20($fp)
	lw $a0 -16($fp)
	sw $a0 12($a1)
	
	lw $t0 -8($fp)
	lw $t1 -20($fp)
	beq $t0 $zero _eq_false_8_
	beq $t1 $zero _eq_false_8_
	lw $a0 0($t0)
	lw $a1 0($t1)
	bne $a0 $a1 _eq_false_8_
	li $a2 5
	beq $a0 $a2 _eq_int_bool_8
	li $a2 6
	beq $a0 $a2 _eq_int_bool_8
	li $a2 7
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
	sw $a0 0($fp)
	b end_equal_8_
_eq_false_8_:
	li $a0 0
	sw $a0 0($fp)
end_equal_8_:
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
	sw $v0 -4($fp)
	
	addiu $sp, $sp, 4
	
	# SETATTR
	lw $a1 -4($fp)
	lw $a0 0($fp)
	sw $a0 12($a1)
	
	# RETURN
	lw $v0, 12($fp)
	addiu $sp, $sp, 28
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
	
	
#####################################

