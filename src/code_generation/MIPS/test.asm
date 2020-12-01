
.text
main:
	move       $fp, $sp
	subu       $sp, $sp, 204
	la         $t0, Object_abort
	usw        $t0, vt_Object+0
	la         $t0, Object_type_name
	usw        $t0, vt_Object+4
	la         $t0, Object_copy
	usw        $t0, vt_Object+8
	la         $t0, Object_abort
	usw        $t0, vt_IO+0
	la         $t0, Object_type_name
	usw        $t0, vt_IO+4
	la         $t0, Object_copy
	usw        $t0, vt_IO+8
	la         $t0, IO_out_string
	usw        $t0, vt_IO+12
	la         $t0, IO_out_int
	usw        $t0, vt_IO+16
	la         $t0, IO_in_string
	usw        $t0, vt_IO+20
	la         $t0, IO_in_int
	usw        $t0, vt_IO+24
	la         $t0, Object_abort
	usw        $t0, vt_Int+0
	la         $t0, Object_type_name
	usw        $t0, vt_Int+4
	la         $t0, Object_copy
	usw        $t0, vt_Int+8
	la         $t0, String_abort
	usw        $t0, vt_String+0
	la         $t0, Object_type_name
	usw        $t0, vt_String+4
	la         $t0, Object_copy
	usw        $t0, vt_String+8
	la         $t0, String_length
	usw        $t0, vt_String+28
	la         $t0, String_concat
	usw        $t0, vt_String+32
	la         $t0, String_substr
	usw        $t0, vt_String+36
	la         $t0, Object_abort
	usw        $t0, vt_Bool+0
	la         $t0, Object_type_name
	usw        $t0, vt_Bool+4
	la         $t0, Object_copy
	usw        $t0, vt_Bool+8
	la         $t0, Object_abort
	usw        $t0, vt_Main+0
	la         $t0, Object_type_name
	usw        $t0, vt_Main+4
	la         $t0, Object_copy
	usw        $t0, vt_Main+8
	la         $t0, IO_out_string
	usw        $t0, vt_Main+12
	la         $t0, IO_out_int
	usw        $t0, vt_Main+16
	la         $t0, IO_in_string
	usw        $t0, vt_Main+20
	la         $t0, IO_in_int
	usw        $t0, vt_Main+24
	la         $t0, Main_main
	usw        $t0, vt_Main+40
	#          self = ALLOCATE Main ;
	li         $a0, 32
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	la         $t0, vt_Main
	sw         $t0, 8($v0)
	#          local_1 = LOAD data_1 ;
	la         $t0, data_1
	sw         $t0, -8($fp)
	#          SETATTR self @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 0($t1)
	#          local_2 = 32 ;
	li         $t0, 32
	sw         $t0, -12($fp)
	#          SETATTR self @size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_3 = GETTYPEADDR self ;
	lw         $t1, -4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_4 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -20($fp)
	#          local_5 = VCALL local_3 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          SETATTR self out 2 ;
	li         $t0, 2
	lw         $t1, -4($fp)
	sw         $t0, 12($t1)
	#          local_6 = GETATTR self out ;
	lw         $t0, -4($fp)
	lw         $t1, 12($t0)
	sw         $t1, -28($fp)
	#          SETATTR self testee local_6 ;
	lw         $t0, -28($fp)
	lw         $t1, -4($fp)
	sw         $t0, 16($t1)
	#          SETATTR self stop 500 ;
	li         $t0, 500
	lw         $t1, -4($fp)
	sw         $t0, 24($t1)
	#          LABEL label_13 ;
	label_13:

	#          IF 1 GOTO label_14 ;
	li         $t0, 1
	bnez       $t0, label_14
	#          GOTO label_15 ;
	b          label_15
	#          LABEL label_14 ;
	label_14:

	#          local_7 = GETATTR self testee ;
	lw         $t0, -4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -32($fp)
	#          local_8 = local_7 + 1 ;
	lw         $t0, -32($fp)
	li         $t1, 1
	add        $t0, $t0, $t1
	sw         $t0, -36($fp)
	#          SETATTR self testee local_8 ;
	lw         $t0, -36($fp)
	lw         $t1, -4($fp)
	sw         $t0, 16($t1)
	#          SETATTR self divisor 2 ;
	li         $t0, 2
	lw         $t1, -4($fp)
	sw         $t0, 20($t1)
	#          LABEL label_6 ;
	label_6:

	#          local_9 = GETATTR self testee ;
	lw         $t0, -4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -40($fp)
	#          local_10 = GETATTR self divisor ;
	lw         $t0, -4($fp)
	lw         $t1, 20($t0)
	sw         $t1, -44($fp)
	#          local_11 = GETATTR self divisor ;
	lw         $t0, -4($fp)
	lw         $t1, 20($t0)
	sw         $t1, -48($fp)
	#          local_12 = local_10 * local_11 ;
	lw         $t0, -44($fp)
	lw         $t1, -48($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -52($fp)
	#          local_13 = local_9 < local_12 ;
	lw         $t0, -40($fp)
	lw         $t1, -52($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -56($fp)
	#          IF local_13 GOTO label_4 ;
	lw         $t0, -56($fp)
	bnez       $t0, label_4
	#          local_14 = GETATTR self testee ;
	lw         $t0, -4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -60($fp)
	#          local_15 = GETATTR self divisor ;
	lw         $t0, -4($fp)
	lw         $t1, 20($t0)
	sw         $t1, -64($fp)
	#          local_16 = GETATTR self testee ;
	lw         $t0, -4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -68($fp)
	#          local_17 = GETATTR self divisor ;
	lw         $t0, -4($fp)
	lw         $t1, 20($t0)
	sw         $t1, -72($fp)
	#          local_18 = local_16 / local_17 ;
	lw         $t0, -68($fp)
	lw         $t1, -72($fp)
	div        $t0, $t0, $t1
	sw         $t0, -76($fp)
	#          local_19 = local_15 * local_18 ;
	lw         $t0, -64($fp)
	lw         $t1, -76($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -80($fp)
	#          local_20 = local_14 - local_19 ;
	lw         $t0, -60($fp)
	lw         $t1, -80($fp)
	sub        $t0, $t0, $t1
	sw         $t0, -84($fp)
	#          local_21 = local_20 - 0 ;
	lw         $t0, -84($fp)
	li         $t1, 0
	sub        $t0, $t0, $t1
	sw         $t0, -88($fp)
	#          local_22 = 0 ;
	li         $t0, 0
	sw         $t0, -92($fp)
	#          IF local_21 GOTO label_1 ;
	lw         $t0, -88($fp)
	bnez       $t0, label_1
	#          local_22 = 1 ;
	li         $t0, 1
	sw         $t0, -92($fp)
	#          LABEL label_1 ;
	label_1:

	#          IF local_22 GOTO label_2 ;
	lw         $t0, -92($fp)
	bnez       $t0, label_2
	#          local_23 = 1 ;
	li         $t0, 1
	sw         $t0, -96($fp)
	#          GOTO label_3 ;
	b          label_3
	#          LABEL label_2 ;
	label_2:

	#          local_23 = 0 ;
	li         $t0, 0
	sw         $t0, -96($fp)
	#          LABEL label_3 ;
	label_3:

	#          local_24 = local_23 ;
	lw         $t0, -96($fp)
	sw         $t0, -100($fp)
	#          GOTO label_5 ;
	b          label_5
	#          LABEL label_4 ;
	label_4:

	#          local_24 = 0 ;
	li         $t0, 0
	sw         $t0, -100($fp)
	#          LABEL label_5 ;
	label_5:

	#          IF local_24 GOTO label_7 ;
	lw         $t0, -100($fp)
	bnez       $t0, label_7
	#          GOTO label_8 ;
	b          label_8
	#          LABEL label_7 ;
	label_7:

	#          local_25 = GETATTR self divisor ;
	lw         $t0, -4($fp)
	lw         $t1, 20($t0)
	sw         $t1, -104($fp)
	#          local_26 = local_25 + 1 ;
	lw         $t0, -104($fp)
	li         $t1, 1
	add        $t0, $t0, $t1
	sw         $t0, -108($fp)
	#          SETATTR self divisor local_26 ;
	lw         $t0, -108($fp)
	lw         $t1, -4($fp)
	sw         $t0, 20($t1)
	#          GOTO label_6 ;
	b          label_6
	#          LABEL label_8 ;
	label_8:

	#          local_27 = 0 ;
	li         $t0, 0
	sw         $t0, -112($fp)
	#          local_28 = GETATTR self testee ;
	lw         $t0, -4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -116($fp)
	#          local_29 = GETATTR self divisor ;
	lw         $t0, -4($fp)
	lw         $t1, 20($t0)
	sw         $t1, -120($fp)
	#          local_30 = GETATTR self divisor ;
	lw         $t0, -4($fp)
	lw         $t1, 20($t0)
	sw         $t1, -124($fp)
	#          local_31 = local_29 * local_30 ;
	lw         $t0, -120($fp)
	lw         $t1, -124($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -128($fp)
	#          local_32 = local_28 < local_31 ;
	lw         $t0, -116($fp)
	lw         $t1, -128($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -132($fp)
	#          IF local_32 GOTO label_9 ;
	lw         $t0, -132($fp)
	bnez       $t0, label_9
	#          local_40 = 0 ;
	li         $t0, 0
	sw         $t0, -164($fp)
	#          GOTO label_10 ;
	b          label_10
	#          LABEL label_9 ;
	label_9:

	#          local_33 = GETATTR self testee ;
	lw         $t0, -4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -136($fp)
	#          SETATTR self out local_33 ;
	lw         $t0, -136($fp)
	lw         $t1, -4($fp)
	sw         $t0, 12($t1)
	#          local_34 = GETTYPEADDR self ;
	lw         $t1, -4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -140($fp)
	#          local_35 = GETATTR self out ;
	lw         $t0, -4($fp)
	lw         $t1, 12($t0)
	sw         $t1, -144($fp)
	#          local_36 = VCALL local_34 out_int ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_35 ;
	lw         $t0, -144($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -140($fp)
	ulw        $t1, 16($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -148($fp)
	#          local_37 = GETTYPEADDR self ;
	lw         $t1, -4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -152($fp)
	#          local_38 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -156($fp)
	#          local_39 = VCALL local_37 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_38 ;
	lw         $t0, -156($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -152($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -160($fp)
	#          local_40 = local_39 ;
	lw         $t0, -160($fp)
	sw         $t0, -164($fp)
	#          LABEL label_10 ;
	label_10:

	#          local_41 = GETATTR self stop ;
	lw         $t0, -4($fp)
	lw         $t1, 24($t0)
	sw         $t1, -168($fp)
	#          local_42 = GETATTR self testee ;
	lw         $t0, -4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -172($fp)
	#          local_43 = local_41 <= local_42 ;
	lw         $t0, -168($fp)
	lw         $t1, -172($fp)
	sle        $t0, $t0, $t1
	sw         $t0, -176($fp)
	#          IF local_43 GOTO label_11 ;
	lw         $t0, -176($fp)
	bnez       $t0, label_11
	#          local_47 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -192($fp)
	#          local_48 = local_47 ;
	lw         $t0, -192($fp)
	sw         $t0, -196($fp)
	#          GOTO label_12 ;
	b          label_12
	#          LABEL label_11 ;
	label_11:

	#          local_45 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -184($fp)
	#          local_46 = VCALL String abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_45 ;
	lw         $t0, -184($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_abort
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -188($fp)
	#          local_48 = local_46 ;
	lw         $t0, -188($fp)
	sw         $t0, -196($fp)
	#          LABEL label_12 ;
	label_12:

	#          GOTO label_13 ;
	b          label_13
	#          LABEL label_15 ;
	label_15:

	#          local_49 = 0 ;
	li         $t0, 0
	sw         $t0, -200($fp)
	#          SETATTR self m local_49 ;
	lw         $t0, -200($fp)
	lw         $t1, -4($fp)
	sw         $t0, 28($t1)
	#          main_result = VCALL Main main ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        Main_main
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -204($fp)
	#          RETURN main_result ;
	lw         $v0, -204($fp)
	addu       $sp, $sp, 204
	li         $v0, 10
	syscall
IO_out_int:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          PRINT int ;
	lw         $a0, 0($fp)
	li         $v0, 1
	syscall
	#          RETURN self ;
	lw         $v0, 4($fp)
	addu       $sp, $sp, 0
	jr         $ra
IO_out_string:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          PRINT str ;
	lw         $a0, 0($fp)
	li         $v0, 4
	syscall
	#          RETURN self ;
	lw         $v0, 4($fp)
	addu       $sp, $sp, 0
	jr         $ra
IO_in_string:
	move       $fp, $sp
	subu       $sp, $sp, 4
	la         $a0, str
	li         $a1, 1024
	li         $v0, 8
	syscall
	sw         $a0, -4($fp)
	#          RETURN str ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
IO_in_int:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          int = READINT ;
	li         $v0, 5
	syscall
	sw         $v0, -4($fp)
	#          RETURN int ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Object_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          type = TYPEOF self ;
	lw         $t0, 0($fp)
	sw         $t0, -4($fp)
	#          RETURN type ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Object_copy:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          copy = COPY self ;
	lw         $a0, 8($fp)
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	addu       $t1, $fp, 0
	addu       $t2, $fp, -4
	copy_loop:

	lw         $t0, ($t1)
	sw         $t0, ($t2)
	addu       $t1, $t1, 4
	addu       $t2, $t2, 4
	subu       $a0, $a0, 4
	beqz       $a0, end_copy_loop
	b          copy_loop
	end_copy_loop:

	#          RETURN copy ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_length:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          len_result = LENGTH self ;
	lb         $t0, 0($fp)
	li         $t1, 0
	length_loop:

	beqz       $t0, end_length_loop
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          length_loop
	end_length_loop:

	sw         $t1, -4($fp)
	#          RETURN len_result ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_concat:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          concat_result = CONCAT self x ;
	lw         $t0, -4($fp)
	lw         $t1, 4($fp)
	lw         $t2, 0($fp)
	concat_loop_a:

	lb         $a0, ($t1)
	beqz       $a0, concat_loop_b
	sb         $a0, ($t0)
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          concat_loop_a
	concat_loop_b:

	lb         $a0, ($t2)
	beqz       $a0, end_concat
	sb         $a0, ($t0)
	addu       $t0, $t0, 1
	addu       $t2, $t2, 1
	b          concat_loop_b
	end_concat:

	#          RETURN concat_result ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_substr:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          substring_result = SUBSTRING self i l;
	lw         $t0, 8($fp)
	la         $t1, substring_result
	lw         $t4, 4($fp)
	lw         $t2, 0($fp)
	addu       $t0, $t0, $t4
	substring_loop:

	beqz       $t2, end_substring_loop
	lb         $t3, ($t0)
	sb         $t3, ($t1)
	subu       $t2, $t2, 1
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          substring_loop
	end_substring_loop:

	#          RETURN substring_result ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Object_abort:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          ABORT None ;
	la         $a0, data_abort
	li         $v0, 4
	syscall
	lw         $a0, ($fp)
	li         $v0, 4
	syscall
	la         $a0, new_line
	li         $v0, 4
	syscall
	li         $v0, 10
	syscall
String_abort:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          ABORT String ;
	la         $a0, data_abort
	li         $v0, 4
	syscall
	la         $a0, abort_String
	li         $v0, 4
	syscall
	la         $a0, new_line
	li         $v0, 4
	syscall
	li         $v0, 10
	syscall
Main_main:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          RETURN ;
	li         $v0, 0
	addu       $sp, $sp, 0
	jr         $ra

.data
	data_1:
		.asciiz    "Main"
	data_2:
		.asciiz    "2 is trivially prime.\n"
	data_3:
		.asciiz    " is prime.\n"
	data_4:
		.asciiz    "halt"
	data_5:
		.asciiz    "continue"
	data_abort:
		.asciiz    "Abort called from class "
	new_line:
		.asciiz    "\n"
	vt_Object:
		.space     36
	vt_IO:
		.space     36
	vt_Int:
		.space     36
	vt_String:
		.space     36
	vt_Bool:
		.space     36
	vt_Main:
		.space     36
	str:
		.space     1024
	concat_result:
		.space     2048
	substring_result:
		.space     1024
	abort_String:
		.asciiz    "String"
