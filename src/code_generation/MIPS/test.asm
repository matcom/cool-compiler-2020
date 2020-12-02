
.text
main:
	move       $fp, $sp
	subu       $sp, $sp, 16
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
	la         $t0, Int_abort
	usw        $t0, vt_Int+0
	la         $t0, Int_type_name
	usw        $t0, vt_Int+4
	la         $t0, Object_copy
	usw        $t0, vt_Int+8
	la         $t0, String_abort
	usw        $t0, vt_String+0
	la         $t0, String_type_name
	usw        $t0, vt_String+4
	la         $t0, Object_copy
	usw        $t0, vt_String+8
	la         $t0, String_length
	usw        $t0, vt_String+28
	la         $t0, String_concat
	usw        $t0, vt_String+32
	la         $t0, String_substr
	usw        $t0, vt_String+36
	la         $t0, Bool_abort
	usw        $t0, vt_Bool+0
	la         $t0, Bool_type_name
	usw        $t0, vt_Bool+4
	la         $t0, Object_copy
	usw        $t0, vt_Bool+8
	la         $t0, Object_abort
	usw        $t0, vt_A2I+0
	la         $t0, Object_type_name
	usw        $t0, vt_A2I+4
	la         $t0, Object_copy
	usw        $t0, vt_A2I+8
	la         $t0, A2I_c2i
	usw        $t0, vt_A2I+40
	la         $t0, A2I_i2c
	usw        $t0, vt_A2I+44
	la         $t0, A2I_a2i
	usw        $t0, vt_A2I+48
	la         $t0, A2I_a2i_aux
	usw        $t0, vt_A2I+52
	la         $t0, A2I_i2a
	usw        $t0, vt_A2I+56
	la         $t0, A2I_i2a_aux
	usw        $t0, vt_A2I+60
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
	usw        $t0, vt_Main+64
	#          self = ALLOCATE Main ;
	li         $a0, 12
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
	#          local_2 = 12 ;
	li         $t0, 12
	sw         $t0, -12($fp)
	#          SETATTR self @size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
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
	sw         $v0, -16($fp)
	#          RETURN main_result ;
	lw         $v0, -16($fp)
	addu       $sp, $sp, 16
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
	lw         $t1, ($t0)
	sw         $t1, -4($fp)
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
	lw         $t2, 0($fp)
	li         $t1, 0
	length_loop:

	lb         $t0, ($t2)
	beqz       $t0, end_length_loop
	addu       $t2, $t2, 1
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
	la         $t0, concat_result
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

	la         $t0, concat_result
	sw         $t0, -4($fp)
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

	la         $t1, substring_result
	sw         $t1, -4($fp)
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
Int_abort:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          ABORT Int ;
	la         $a0, data_abort
	li         $v0, 4
	syscall
	la         $a0, abort_Int
	li         $v0, 4
	syscall
	la         $a0, new_line
	li         $v0, 4
	syscall
	li         $v0, 10
	syscall
Bool_abort:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          ABORT Bool ;
	la         $a0, data_abort
	li         $v0, 4
	syscall
	la         $a0, abort_Bool
	li         $v0, 4
	syscall
	la         $a0, new_line
	li         $v0, 4
	syscall
	li         $v0, 10
	syscall
Bool_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_23 = LOAD data_19 ;
	la         $t0, data_19
	sw         $t0, -4($fp)
	#          RETURN local_23 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Int_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_24 = LOAD data_20 ;
	la         $t0, data_20
	sw         $t0, -4($fp)
	#          RETURN local_24 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_25 = LOAD data_21 ;
	la         $t0, data_21
	sw         $t0, -4($fp)
	#          RETURN local_25 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
A2I_c2i:
	move       $fp, $sp
	subu       $sp, $sp, 168
	#          local_0 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -4($fp)
	#          local_1 = char == local_0 ;
	lw         $t0, 0($fp)
	lw         $t1, -4($fp)
	li         $v0, 1
	sw         $v0, -8($fp)
	equal_loop_1:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_1
	beqz       $t2, end_loop_1
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_1
	b          end_loop_1
	not_equal_1:

	li         $v0, 0
	sw         $v0, -8($fp)
	end_loop_1:

	#          local_2 = local_1 ;
	lw         $t0, -8($fp)
	sw         $t0, -12($fp)
	#          IF local_2 GOTO label_19 ;
	lw         $t0, -12($fp)
	bnez       $t0, label_19
	#          local_3 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -16($fp)
	#          local_4 = char == local_3 ;
	lw         $t0, 0($fp)
	lw         $t1, -16($fp)
	li         $v0, 1
	sw         $v0, -20($fp)
	equal_loop_2:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_2
	beqz       $t2, end_loop_2
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_2
	b          end_loop_2
	not_equal_2:

	li         $v0, 0
	sw         $v0, -20($fp)
	end_loop_2:

	#          local_5 = local_4 ;
	lw         $t0, -20($fp)
	sw         $t0, -24($fp)
	#          IF local_5 GOTO label_17 ;
	lw         $t0, -24($fp)
	bnez       $t0, label_17
	#          local_6 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -28($fp)
	#          local_7 = char == local_6 ;
	lw         $t0, 0($fp)
	lw         $t1, -28($fp)
	li         $v0, 1
	sw         $v0, -32($fp)
	equal_loop_3:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_3
	beqz       $t2, end_loop_3
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_3
	b          end_loop_3
	not_equal_3:

	li         $v0, 0
	sw         $v0, -32($fp)
	end_loop_3:

	#          local_8 = local_7 ;
	lw         $t0, -32($fp)
	sw         $t0, -36($fp)
	#          IF local_8 GOTO label_15 ;
	lw         $t0, -36($fp)
	bnez       $t0, label_15
	#          local_9 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -40($fp)
	#          local_10 = char == local_9 ;
	lw         $t0, 0($fp)
	lw         $t1, -40($fp)
	li         $v0, 1
	sw         $v0, -44($fp)
	equal_loop_4:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_4
	beqz       $t2, end_loop_4
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_4
	b          end_loop_4
	not_equal_4:

	li         $v0, 0
	sw         $v0, -44($fp)
	end_loop_4:

	#          local_11 = local_10 ;
	lw         $t0, -44($fp)
	sw         $t0, -48($fp)
	#          IF local_11 GOTO label_13 ;
	lw         $t0, -48($fp)
	bnez       $t0, label_13
	#          local_12 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -52($fp)
	#          local_13 = char == local_12 ;
	lw         $t0, 0($fp)
	lw         $t1, -52($fp)
	li         $v0, 1
	sw         $v0, -56($fp)
	equal_loop_5:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_5
	beqz       $t2, end_loop_5
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_5
	b          end_loop_5
	not_equal_5:

	li         $v0, 0
	sw         $v0, -56($fp)
	end_loop_5:

	#          local_14 = local_13 ;
	lw         $t0, -56($fp)
	sw         $t0, -60($fp)
	#          IF local_14 GOTO label_11 ;
	lw         $t0, -60($fp)
	bnez       $t0, label_11
	#          local_15 = LOAD data_7 ;
	la         $t0, data_7
	sw         $t0, -64($fp)
	#          local_16 = char == local_15 ;
	lw         $t0, 0($fp)
	lw         $t1, -64($fp)
	li         $v0, 1
	sw         $v0, -68($fp)
	equal_loop_6:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_6
	beqz       $t2, end_loop_6
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_6
	b          end_loop_6
	not_equal_6:

	li         $v0, 0
	sw         $v0, -68($fp)
	end_loop_6:

	#          local_17 = local_16 ;
	lw         $t0, -68($fp)
	sw         $t0, -72($fp)
	#          IF local_17 GOTO label_9 ;
	lw         $t0, -72($fp)
	bnez       $t0, label_9
	#          local_18 = LOAD data_8 ;
	la         $t0, data_8
	sw         $t0, -76($fp)
	#          local_19 = char == local_18 ;
	lw         $t0, 0($fp)
	lw         $t1, -76($fp)
	li         $v0, 1
	sw         $v0, -80($fp)
	equal_loop_7:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_7
	beqz       $t2, end_loop_7
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_7
	b          end_loop_7
	not_equal_7:

	li         $v0, 0
	sw         $v0, -80($fp)
	end_loop_7:

	#          local_20 = local_19 ;
	lw         $t0, -80($fp)
	sw         $t0, -84($fp)
	#          IF local_20 GOTO label_7 ;
	lw         $t0, -84($fp)
	bnez       $t0, label_7
	#          local_21 = LOAD data_9 ;
	la         $t0, data_9
	sw         $t0, -88($fp)
	#          local_22 = char == local_21 ;
	lw         $t0, 0($fp)
	lw         $t1, -88($fp)
	li         $v0, 1
	sw         $v0, -92($fp)
	equal_loop_8:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_8
	beqz       $t2, end_loop_8
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_8
	b          end_loop_8
	not_equal_8:

	li         $v0, 0
	sw         $v0, -92($fp)
	end_loop_8:

	#          local_23 = local_22 ;
	lw         $t0, -92($fp)
	sw         $t0, -96($fp)
	#          IF local_23 GOTO label_5 ;
	lw         $t0, -96($fp)
	bnez       $t0, label_5
	#          local_24 = LOAD data_10 ;
	la         $t0, data_10
	sw         $t0, -100($fp)
	#          local_25 = char == local_24 ;
	lw         $t0, 0($fp)
	lw         $t1, -100($fp)
	li         $v0, 1
	sw         $v0, -104($fp)
	equal_loop_9:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_9
	beqz       $t2, end_loop_9
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_9
	b          end_loop_9
	not_equal_9:

	li         $v0, 0
	sw         $v0, -104($fp)
	end_loop_9:

	#          local_26 = local_25 ;
	lw         $t0, -104($fp)
	sw         $t0, -108($fp)
	#          IF local_26 GOTO label_3 ;
	lw         $t0, -108($fp)
	bnez       $t0, label_3
	#          local_27 = LOAD data_11 ;
	la         $t0, data_11
	sw         $t0, -112($fp)
	#          local_28 = char == local_27 ;
	lw         $t0, 0($fp)
	lw         $t1, -112($fp)
	li         $v0, 1
	sw         $v0, -116($fp)
	equal_loop_10:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_10
	beqz       $t2, end_loop_10
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_10
	b          end_loop_10
	not_equal_10:

	li         $v0, 0
	sw         $v0, -116($fp)
	end_loop_10:

	#          local_29 = local_28 ;
	lw         $t0, -116($fp)
	sw         $t0, -120($fp)
	#          IF local_29 GOTO label_1 ;
	lw         $t0, -120($fp)
	bnez       $t0, label_1
	#          local_30 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -124($fp)
	#          local_31 = VCALL local_30 abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -124($fp)
	ulw        $t1, 0($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -128($fp)
	#          local_32 = 0 ;
	li         $t0, 0
	sw         $t0, -132($fp)
	#          GOTO label_2 ;
	b          label_2
	#          LABEL label_1 ;
	label_1:

	#          local_32 = 9 ;
	li         $t0, 9
	sw         $t0, -132($fp)
	#          LABEL label_2 ;
	label_2:

	#          local_33 = local_32 ;
	lw         $t0, -132($fp)
	sw         $t0, -136($fp)
	#          GOTO label_4 ;
	b          label_4
	#          LABEL label_3 ;
	label_3:

	#          local_33 = 8 ;
	li         $t0, 8
	sw         $t0, -136($fp)
	#          LABEL label_4 ;
	label_4:

	#          local_34 = local_33 ;
	lw         $t0, -136($fp)
	sw         $t0, -140($fp)
	#          GOTO label_6 ;
	b          label_6
	#          LABEL label_5 ;
	label_5:

	#          local_34 = 7 ;
	li         $t0, 7
	sw         $t0, -140($fp)
	#          LABEL label_6 ;
	label_6:

	#          local_35 = local_34 ;
	lw         $t0, -140($fp)
	sw         $t0, -144($fp)
	#          GOTO label_8 ;
	b          label_8
	#          LABEL label_7 ;
	label_7:

	#          local_35 = 6 ;
	li         $t0, 6
	sw         $t0, -144($fp)
	#          LABEL label_8 ;
	label_8:

	#          local_36 = local_35 ;
	lw         $t0, -144($fp)
	sw         $t0, -148($fp)
	#          GOTO label_10 ;
	b          label_10
	#          LABEL label_9 ;
	label_9:

	#          local_36 = 5 ;
	li         $t0, 5
	sw         $t0, -148($fp)
	#          LABEL label_10 ;
	label_10:

	#          local_37 = local_36 ;
	lw         $t0, -148($fp)
	sw         $t0, -152($fp)
	#          GOTO label_12 ;
	b          label_12
	#          LABEL label_11 ;
	label_11:

	#          local_37 = 4 ;
	li         $t0, 4
	sw         $t0, -152($fp)
	#          LABEL label_12 ;
	label_12:

	#          local_38 = local_37 ;
	lw         $t0, -152($fp)
	sw         $t0, -156($fp)
	#          GOTO label_14 ;
	b          label_14
	#          LABEL label_13 ;
	label_13:

	#          local_38 = 3 ;
	li         $t0, 3
	sw         $t0, -156($fp)
	#          LABEL label_14 ;
	label_14:

	#          local_39 = local_38 ;
	lw         $t0, -156($fp)
	sw         $t0, -160($fp)
	#          GOTO label_16 ;
	b          label_16
	#          LABEL label_15 ;
	label_15:

	#          local_39 = 2 ;
	li         $t0, 2
	sw         $t0, -160($fp)
	#          LABEL label_16 ;
	label_16:

	#          local_40 = local_39 ;
	lw         $t0, -160($fp)
	sw         $t0, -164($fp)
	#          GOTO label_18 ;
	b          label_18
	#          LABEL label_17 ;
	label_17:

	#          local_40 = 1 ;
	li         $t0, 1
	sw         $t0, -164($fp)
	#          LABEL label_18 ;
	label_18:

	#          local_41 = local_40 ;
	lw         $t0, -164($fp)
	sw         $t0, -168($fp)
	#          GOTO label_20 ;
	b          label_20
	#          LABEL label_19 ;
	label_19:

	#          local_41 = 0 ;
	li         $t0, 0
	sw         $t0, -168($fp)
	#          LABEL label_20 ;
	label_20:

	#          RETURN local_41 ;
	lw         $v0, -168($fp)
	addu       $sp, $sp, 168
	jr         $ra
A2I_i2c:
	move       $fp, $sp
	subu       $sp, $sp, 172
	#          local_0 = i == 0 ;
	lw         $t0, 0($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          local_1 = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          IF local_1 GOTO label_39 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_39
	#          local_3 = i == 1 ;
	lw         $t0, 0($fp)
	li         $t1, 1
	seq        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          local_4 = local_3 ;
	lw         $t0, -16($fp)
	sw         $t0, -20($fp)
	#          IF local_4 GOTO label_37 ;
	lw         $t0, -20($fp)
	bnez       $t0, label_37
	#          local_6 = i == 2 ;
	lw         $t0, 0($fp)
	li         $t1, 2
	seq        $t0, $t0, $t1
	sw         $t0, -28($fp)
	#          local_7 = local_6 ;
	lw         $t0, -28($fp)
	sw         $t0, -32($fp)
	#          IF local_7 GOTO label_35 ;
	lw         $t0, -32($fp)
	bnez       $t0, label_35
	#          local_9 = i == 3 ;
	lw         $t0, 0($fp)
	li         $t1, 3
	seq        $t0, $t0, $t1
	sw         $t0, -40($fp)
	#          local_10 = local_9 ;
	lw         $t0, -40($fp)
	sw         $t0, -44($fp)
	#          IF local_10 GOTO label_33 ;
	lw         $t0, -44($fp)
	bnez       $t0, label_33
	#          local_12 = i == 4 ;
	lw         $t0, 0($fp)
	li         $t1, 4
	seq        $t0, $t0, $t1
	sw         $t0, -52($fp)
	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          IF local_13 GOTO label_31 ;
	lw         $t0, -56($fp)
	bnez       $t0, label_31
	#          local_15 = i == 5 ;
	lw         $t0, 0($fp)
	li         $t1, 5
	seq        $t0, $t0, $t1
	sw         $t0, -64($fp)
	#          local_16 = local_15 ;
	lw         $t0, -64($fp)
	sw         $t0, -68($fp)
	#          IF local_16 GOTO label_29 ;
	lw         $t0, -68($fp)
	bnez       $t0, label_29
	#          local_18 = i == 6 ;
	lw         $t0, 0($fp)
	li         $t1, 6
	seq        $t0, $t0, $t1
	sw         $t0, -76($fp)
	#          local_19 = local_18 ;
	lw         $t0, -76($fp)
	sw         $t0, -80($fp)
	#          IF local_19 GOTO label_27 ;
	lw         $t0, -80($fp)
	bnez       $t0, label_27
	#          local_21 = i == 7 ;
	lw         $t0, 0($fp)
	li         $t1, 7
	seq        $t0, $t0, $t1
	sw         $t0, -88($fp)
	#          local_22 = local_21 ;
	lw         $t0, -88($fp)
	sw         $t0, -92($fp)
	#          IF local_22 GOTO label_25 ;
	lw         $t0, -92($fp)
	bnez       $t0, label_25
	#          local_24 = i == 8 ;
	lw         $t0, 0($fp)
	li         $t1, 8
	seq        $t0, $t0, $t1
	sw         $t0, -100($fp)
	#          local_25 = local_24 ;
	lw         $t0, -100($fp)
	sw         $t0, -104($fp)
	#          IF local_25 GOTO label_23 ;
	lw         $t0, -104($fp)
	bnez       $t0, label_23
	#          local_27 = i == 9 ;
	lw         $t0, 0($fp)
	li         $t1, 9
	seq        $t0, $t0, $t1
	sw         $t0, -112($fp)
	#          local_28 = local_27 ;
	lw         $t0, -112($fp)
	sw         $t0, -116($fp)
	#          IF local_28 GOTO label_21 ;
	lw         $t0, -116($fp)
	bnez       $t0, label_21
	#          local_30 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -124($fp)
	#          local_31 = VCALL local_30 abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -124($fp)
	ulw        $t1, 0($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -128($fp)
	#          local_32 = LOAD data_12 ;
	la         $t0, data_12
	sw         $t0, -132($fp)
	#          local_33 = local_32 ;
	lw         $t0, -132($fp)
	sw         $t0, -136($fp)
	#          GOTO label_22 ;
	b          label_22
	#          LABEL label_21 ;
	label_21:

	#          local_29 = LOAD data_11 ;
	la         $t0, data_11
	sw         $t0, -120($fp)
	#          local_33 = local_29 ;
	lw         $t0, -120($fp)
	sw         $t0, -136($fp)
	#          LABEL label_22 ;
	label_22:

	#          local_34 = local_33 ;
	lw         $t0, -136($fp)
	sw         $t0, -140($fp)
	#          GOTO label_24 ;
	b          label_24
	#          LABEL label_23 ;
	label_23:

	#          local_26 = LOAD data_10 ;
	la         $t0, data_10
	sw         $t0, -108($fp)
	#          local_34 = local_26 ;
	lw         $t0, -108($fp)
	sw         $t0, -140($fp)
	#          LABEL label_24 ;
	label_24:

	#          local_35 = local_34 ;
	lw         $t0, -140($fp)
	sw         $t0, -144($fp)
	#          GOTO label_26 ;
	b          label_26
	#          LABEL label_25 ;
	label_25:

	#          local_23 = LOAD data_9 ;
	la         $t0, data_9
	sw         $t0, -96($fp)
	#          local_35 = local_23 ;
	lw         $t0, -96($fp)
	sw         $t0, -144($fp)
	#          LABEL label_26 ;
	label_26:

	#          local_36 = local_35 ;
	lw         $t0, -144($fp)
	sw         $t0, -148($fp)
	#          GOTO label_28 ;
	b          label_28
	#          LABEL label_27 ;
	label_27:

	#          local_20 = LOAD data_8 ;
	la         $t0, data_8
	sw         $t0, -84($fp)
	#          local_36 = local_20 ;
	lw         $t0, -84($fp)
	sw         $t0, -148($fp)
	#          LABEL label_28 ;
	label_28:

	#          local_37 = local_36 ;
	lw         $t0, -148($fp)
	sw         $t0, -152($fp)
	#          GOTO label_30 ;
	b          label_30
	#          LABEL label_29 ;
	label_29:

	#          local_17 = LOAD data_7 ;
	la         $t0, data_7
	sw         $t0, -72($fp)
	#          local_37 = local_17 ;
	lw         $t0, -72($fp)
	sw         $t0, -152($fp)
	#          LABEL label_30 ;
	label_30:

	#          local_38 = local_37 ;
	lw         $t0, -152($fp)
	sw         $t0, -156($fp)
	#          GOTO label_32 ;
	b          label_32
	#          LABEL label_31 ;
	label_31:

	#          local_14 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -60($fp)
	#          local_38 = local_14 ;
	lw         $t0, -60($fp)
	sw         $t0, -156($fp)
	#          LABEL label_32 ;
	label_32:

	#          local_39 = local_38 ;
	lw         $t0, -156($fp)
	sw         $t0, -160($fp)
	#          GOTO label_34 ;
	b          label_34
	#          LABEL label_33 ;
	label_33:

	#          local_11 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -48($fp)
	#          local_39 = local_11 ;
	lw         $t0, -48($fp)
	sw         $t0, -160($fp)
	#          LABEL label_34 ;
	label_34:

	#          local_40 = local_39 ;
	lw         $t0, -160($fp)
	sw         $t0, -164($fp)
	#          GOTO label_36 ;
	b          label_36
	#          LABEL label_35 ;
	label_35:

	#          local_8 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -36($fp)
	#          local_40 = local_8 ;
	lw         $t0, -36($fp)
	sw         $t0, -164($fp)
	#          LABEL label_36 ;
	label_36:

	#          local_41 = local_40 ;
	lw         $t0, -164($fp)
	sw         $t0, -168($fp)
	#          GOTO label_38 ;
	b          label_38
	#          LABEL label_37 ;
	label_37:

	#          local_5 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -24($fp)
	#          local_41 = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -168($fp)
	#          LABEL label_38 ;
	label_38:

	#          local_42 = local_41 ;
	lw         $t0, -168($fp)
	sw         $t0, -172($fp)
	#          GOTO label_40 ;
	b          label_40
	#          LABEL label_39 ;
	label_39:

	#          local_2 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -12($fp)
	#          local_42 = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -172($fp)
	#          LABEL label_40 ;
	label_40:

	#          RETURN local_42 ;
	lw         $v0, -172($fp)
	addu       $sp, $sp, 172
	jr         $ra
A2I_a2i:
	move       $fp, $sp
	subu       $sp, $sp, 136
	#          local_1 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          local_2 = local_1 == 0 ;
	lw         $t0, -8($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -12($fp)
	#          local_3 = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -16($fp)
	#          IF local_3 GOTO label_45 ;
	lw         $t0, -16($fp)
	bnez       $t0, label_45
	#          local_5 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_6 = LOAD data_13 ;
	la         $t0, data_13
	sw         $t0, -28($fp)
	#          local_7 = local_5 == local_6 ;
	lw         $t0, -24($fp)
	lw         $t1, -28($fp)
	li         $v0, 1
	sw         $v0, -32($fp)
	equal_loop_11:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_11
	beqz       $t2, end_loop_11
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_11
	b          end_loop_11
	not_equal_11:

	li         $v0, 0
	sw         $v0, -32($fp)
	end_loop_11:

	#          local_8 = local_7 ;
	lw         $t0, -32($fp)
	sw         $t0, -36($fp)
	#          IF local_8 GOTO label_43 ;
	lw         $t0, -36($fp)
	bnez       $t0, label_43
	#          local_18 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -76($fp)
	#          local_19 = LOAD data_14 ;
	la         $t0, data_14
	sw         $t0, -80($fp)
	#          local_20 = local_18 == local_19 ;
	lw         $t0, -76($fp)
	lw         $t1, -80($fp)
	li         $v0, 1
	sw         $v0, -84($fp)
	equal_loop_12:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_12
	beqz       $t2, end_loop_12
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_12
	b          end_loop_12
	not_equal_12:

	li         $v0, 0
	sw         $v0, -84($fp)
	end_loop_12:

	#          local_21 = local_20 ;
	lw         $t0, -84($fp)
	sw         $t0, -88($fp)
	#          IF local_21 GOTO label_41 ;
	lw         $t0, -88($fp)
	bnez       $t0, label_41
	#          local_29 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -120($fp)
	#          local_30 = VCALL local_29 a2i_aux ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -120($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -124($fp)
	#          local_31 = local_30 ;
	lw         $t0, -124($fp)
	sw         $t0, -128($fp)
	#          GOTO label_42 ;
	b          label_42
	#          LABEL label_41 ;
	label_41:

	#          local_22 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -92($fp)
	#          local_25 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -104($fp)
	#          local_26 = local_25 - 1 ;
	lw         $t0, -104($fp)
	li         $t1, 1
	sub        $t0, $t0, $t1
	sw         $t0, -108($fp)
	#          local_27 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_26 ;
	lw         $t0, -108($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -112($fp)
	#          local_28 = VCALL local_22 a2i_aux ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_27 ;
	lw         $t0, -112($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -92($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -116($fp)
	#          local_31 = local_28 ;
	lw         $t0, -116($fp)
	sw         $t0, -128($fp)
	#          LABEL label_42 ;
	label_42:

	#          local_32 = local_31 ;
	lw         $t0, -128($fp)
	sw         $t0, -132($fp)
	#          GOTO label_44 ;
	b          label_44
	#          LABEL label_43 ;
	label_43:

	#          local_9 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -40($fp)
	#          local_12 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = local_12 - 1 ;
	lw         $t0, -52($fp)
	li         $t1, 1
	sub        $t0, $t0, $t1
	sw         $t0, -56($fp)
	#          local_14 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_13 ;
	lw         $t0, -56($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -60($fp)
	#          local_15 = VCALL local_9 a2i_aux ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_14 ;
	lw         $t0, -60($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -40($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -64($fp)
	#          local_16 = ~ local_15
	not        $t0, $t0
	sw         $t0, -68($fp)
	#          local_32 = local_16 ;
	lw         $t0, -68($fp)
	sw         $t0, -132($fp)
	#          LABEL label_44 ;
	label_44:

	#          local_33 = local_32 ;
	lw         $t0, -132($fp)
	sw         $t0, -136($fp)
	#          GOTO label_46 ;
	b          label_46
	#          LABEL label_45 ;
	label_45:

	#          local_33 = 0 ;
	li         $t0, 0
	sw         $t0, -136($fp)
	#          LABEL label_46 ;
	label_46:

	#          RETURN local_33 ;
	lw         $v0, -136($fp)
	addu       $sp, $sp, 136
	jr         $ra
A2I_a2i_aux:
	move       $fp, $sp
	subu       $sp, $sp, 56
	#          int = 0 ;
	li         $t0, 0
	sw         $t0, -4($fp)
	#          local_2 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -12($fp)
	#          j = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -16($fp)
	#          i = 0 ;
	li         $t0, 0
	sw         $t0, -20($fp)
	#          LABEL label_47 ;
	label_47:

	#          local_5 = i < j ;
	lw         $t0, -20($fp)
	lw         $t1, -16($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -24($fp)
	#          IF local_5 GOTO label_48 ;
	lw         $t0, -24($fp)
	bnez       $t0, label_48
	#          GOTO label_49 ;
	b          label_49
	#          LABEL label_48 ;
	label_48:

	#          local_6 = int * 10 ;
	lw         $t0, -4($fp)
	li         $t1, 10
	mul        $t0, $t0, $t1
	sw         $t0, -28($fp)
	#          local_7 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -32($fp)
	#          local_9 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -40($fp)
	#          local_10 = VCALL local_7 c2i ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_9 ;
	lw         $t0, -40($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -32($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -44($fp)
	#          local_11 = local_6 + local_10 ;
	lw         $t0, -28($fp)
	lw         $t1, -44($fp)
	add        $t0, $t0, $t1
	sw         $t0, -48($fp)
	#          int = local_11 ;
	lw         $t0, -48($fp)
	sw         $t0, -4($fp)
	#          local_12 = i + 1 ;
	lw         $t0, -20($fp)
	li         $t1, 1
	add        $t0, $t0, $t1
	sw         $t0, -52($fp)
	#          i = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -20($fp)
	#          GOTO label_47 ;
	b          label_47
	#          LABEL label_49 ;
	label_49:

	#          local_13 = 0 ;
	li         $t0, 0
	sw         $t0, -56($fp)
	#          RETURN int ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 56
	jr         $ra
A2I_i2a:
	move       $fp, $sp
	subu       $sp, $sp, 60
	#          local_0 = i == 0 ;
	lw         $t0, 0($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          local_1 = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          IF local_1 GOTO label_52 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_52
	#          local_3 = 0 < i ;
	li         $t0, 0
	lw         $t1, 0($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          IF local_3 GOTO label_50 ;
	lw         $t0, -16($fp)
	bnez       $t0, label_50
	#          local_7 = LOAD data_13 ;
	la         $t0, data_13
	sw         $t0, -32($fp)
	#          local_8 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -36($fp)
	#          local_9 = ~ 1
	li         $t0, 1
	not        $t0, $t0
	sw         $t0, -40($fp)
	#          local_10 = i * local_9 ;
	lw         $t0, 0($fp)
	lw         $t1, -40($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -44($fp)
	#          local_11 = VCALL local_8 i2a_aux ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_10 ;
	lw         $t0, -44($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -36($fp)
	ulw        $t1, 60($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          local_12 = VCALL String concat ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_11 ;
	lw         $t0, -48($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_concat
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          GOTO label_51 ;
	b          label_51
	#          LABEL label_50 ;
	label_50:

	#          local_4 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -20($fp)
	#          local_5 = VCALL local_4 i2a_aux ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -20($fp)
	ulw        $t1, 60($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_13 = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -56($fp)
	#          LABEL label_51 ;
	label_51:

	#          local_14 = local_13 ;
	lw         $t0, -56($fp)
	sw         $t0, -60($fp)
	#          GOTO label_53 ;
	b          label_53
	#          LABEL label_52 ;
	label_52:

	#          local_2 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -12($fp)
	#          local_14 = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -60($fp)
	#          LABEL label_53 ;
	label_53:

	#          RETURN local_14 ;
	lw         $v0, -60($fp)
	addu       $sp, $sp, 60
	jr         $ra
A2I_i2a_aux:
	move       $fp, $sp
	subu       $sp, $sp, 56
	#          local_0 = i == 0 ;
	lw         $t0, 0($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          local_1 = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          IF local_1 GOTO label_54 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_54
	#          local_3 = i / 10 ;
	lw         $t0, 0($fp)
	li         $t1, 10
	div        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          next = local_3 ;
	lw         $t0, -16($fp)
	sw         $t0, -20($fp)
	#          local_6 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_7 = VCALL local_6 i2a_aux ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG next ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 60($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          local_8 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -36($fp)
	#          local_9 = next * 10 ;
	lw         $t0, -20($fp)
	li         $t1, 10
	mul        $t0, $t0, $t1
	sw         $t0, -40($fp)
	#          local_10 = i - local_9 ;
	lw         $t0, 0($fp)
	lw         $t1, -40($fp)
	sub        $t0, $t0, $t1
	sw         $t0, -44($fp)
	#          local_11 = VCALL local_8 i2c ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_10 ;
	lw         $t0, -44($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -36($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          local_12 = VCALL String concat ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_11 ;
	lw         $t0, -48($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_concat
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          GOTO label_55 ;
	b          label_55
	#          LABEL label_54 ;
	label_54:

	#          local_2 = LOAD data_12 ;
	la         $t0, data_12
	sw         $t0, -12($fp)
	#          local_13 = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -56($fp)
	#          LABEL label_55 ;
	label_55:

	#          RETURN local_13 ;
	lw         $v0, -56($fp)
	addu       $sp, $sp, 56
	jr         $ra
Main_main:
	move       $fp, $sp
	subu       $sp, $sp, 92
	#          local_1 = ALLOCATE A2I ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -8($fp)
	la         $t0, vt_A2I
	sw         $t0, 8($v0)
	#          local_2 = LOAD data_15 ;
	la         $t0, data_15
	sw         $t0, -12($fp)
	#          SETATTR local_1 @type local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, -8($fp)
	sw         $t0, 0($t1)
	#          local_3 = 12 ;
	li         $t0, 12
	sw         $t0, -16($fp)
	#          SETATTR local_1 @size local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, -8($fp)
	sw         $t0, 4($t1)
	#          local_0 = GETTYPEADDR local_1 ;
	lw         $t1, -8($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_4 = LOAD data_16 ;
	la         $t0, data_16
	sw         $t0, -20($fp)
	#          local_5 = VCALL local_0 a2i ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 48($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          a = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -28($fp)
	#          local_8 = ALLOCATE A2I ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -36($fp)
	la         $t0, vt_A2I
	sw         $t0, 8($v0)
	#          local_9 = LOAD data_15 ;
	la         $t0, data_15
	sw         $t0, -40($fp)
	#          SETATTR local_8 @type local_9 ;
	lw         $t0, -40($fp)
	lw         $t1, -36($fp)
	sw         $t0, 0($t1)
	#          local_10 = 12 ;
	li         $t0, 12
	sw         $t0, -44($fp)
	#          SETATTR local_8 @size local_10 ;
	lw         $t0, -44($fp)
	lw         $t1, -36($fp)
	sw         $t0, 4($t1)
	#          local_7 = GETTYPEADDR local_8 ;
	lw         $t1, -36($fp)
	lw         $t0, 8($t1)
	sw         $t0, -32($fp)
	#          local_11 = VCALL local_7 i2a ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_8 ;
	lw         $t0, -36($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 678987 ;
	li         $t0, 678987
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -32($fp)
	ulw        $t1, 56($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          b = local_11 ;
	lw         $t0, -48($fp)
	sw         $t0, -52($fp)
	#          local_13 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -56($fp)
	#          local_14 = VCALL local_13 out_int ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG a ;
	lw         $t0, -28($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -56($fp)
	ulw        $t1, 16($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -60($fp)
	#          local_15 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -64($fp)
	#          local_16 = LOAD data_17 ;
	la         $t0, data_17
	sw         $t0, -68($fp)
	#          local_17 = VCALL local_15 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_16 ;
	lw         $t0, -68($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -64($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -72($fp)
	#          local_18 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -76($fp)
	#          local_19 = VCALL local_18 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG b ;
	lw         $t0, -52($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -76($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -80($fp)
	#          local_20 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -84($fp)
	#          local_21 = LOAD data_18 ;
	la         $t0, data_18
	sw         $t0, -88($fp)
	#          local_22 = VCALL local_20 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_21 ;
	lw         $t0, -88($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -84($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -92($fp)
	#          RETURN local_22 ;
	lw         $v0, -92($fp)
	addu       $sp, $sp, 92
	jr         $ra

.data
	data_1:
		.asciiz    "Main"
	data_2:
		.asciiz    "0"
	data_3:
		.asciiz    "1"
	data_4:
		.asciiz    "2"
	data_5:
		.asciiz    "3"
	data_6:
		.asciiz    "4"
	data_7:
		.asciiz    "5"
	data_8:
		.asciiz    "6"
	data_9:
		.asciiz    "7"
	data_10:
		.asciiz    "8"
	data_11:
		.asciiz    "9"
	data_12:
		.asciiz    ""
	data_13:
		.asciiz    "-"
	data_14:
		.asciiz    "+"
	data_15:
		.asciiz    "A2I"
	data_16:
		.asciiz    "678987"
	data_17:
		.asciiz    " == "
	data_18:
		.asciiz    "\n"
	data_19:
		.asciiz    "Bool"
	data_20:
		.asciiz    "Int"
	data_21:
		.asciiz    "String"
	data_abort:
		.asciiz    "Abort called from class "
	new_line:
		.asciiz    "\n"
	vt_Object:
		.space     188
	vt_IO:
		.space     188
	vt_Int:
		.space     188
	vt_String:
		.space     188
	vt_Bool:
		.space     188
	vt_A2I:
		.space     188
	vt_Main:
		.space     188
	str:
		.space     1024
	concat_result:
		.space     2048
	substring_result:
		.space     1024
	abort_String:
		.asciiz    "String"
	abort_Int:
		.asciiz    "Int"
	abort_Bool:
		.asciiz    "Bool"
