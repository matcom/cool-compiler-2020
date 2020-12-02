
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
	la         $t0, Main_pal
	usw        $t0, vt_Main+40
	la         $t0, Main_main
	usw        $t0, vt_Main+44
	#          self = ALLOCATE Main ;
	li         $a0, 16
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
	#          local_2 = 16 ;
	li         $t0, 16
	sw         $t0, -12($fp)
	#          SETATTR self @size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          main_result = VCALL Main main ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        Main_main
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
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
	la         $a0, read_result
	lw         $t0, 0($fp)
	addu       $a0, $a0, $t0
	li         $a1, 1024
	li         $v0, 8
	syscall
	remove_nl_loop:

	lb         $t0, ($a0)
	la         $t1, new_line
	lb         $t2, ($t1)
	beq        $t0, $t2, end_loop
	addu       $a0, $a0, 1
	b          remove_nl_loop
	end_loop:

	sb         $zero, ($a0)
	la         $a0, read_result
	lw         $t0, 0($fp)
	addu       $a0, $a0, $t0
	sw         $a0, -4($fp)
	#          RETURN read_result ;
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
	lw         $t1, 8($fp)
	lw         $t2, 4($fp)
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
	lw         $t0, 12($fp)
	la         $t5, substring_result
	lw         $t1, 0($fp)
	addu       $t1, $t1, $t5
	lw         $t4, 8($fp)
	lw         $t2, 4($fp)
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

	la         $t5, substring_result
	lw         $t1, 0($fp)
	addu       $t1, $t1, $t5
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
	#          local_15 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -4($fp)
	#          RETURN local_15 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Int_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_16 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -4($fp)
	#          RETURN local_16 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_17 = LOAD data_7 ;
	la         $t0, data_7
	sw         $t0, -4($fp)
	#          RETURN local_17 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Main_pal:
	move       $fp, $sp
	subu       $sp, $sp, 108
	#          local_1 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
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
	#          IF local_3 GOTO label_5 ;
	lw         $t0, -16($fp)
	bnez       $t0, label_5
	#          local_5 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_6 = local_5 == 1 ;
	lw         $t0, -24($fp)
	li         $t1, 1
	seq        $t0, $t0, $t1
	sw         $t0, -28($fp)
	#          local_7 = local_6 ;
	lw         $t0, -28($fp)
	sw         $t0, -32($fp)
	#          IF local_7 GOTO label_3 ;
	lw         $t0, -32($fp)
	bnez       $t0, label_3
	#          local_9 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
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
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -40($fp)
	#          local_12 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = local_12 - 1 ;
	lw         $t0, -52($fp)
	li         $t1, 1
	sub        $t0, $t0, $t1
	sw         $t0, -56($fp)
	#          local_14 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_13 ;
	lw         $t0, -56($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 4 ;
	li         $t0, 4
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -60($fp)
	#          local_15 = local_9 == local_14 ;
	lw         $t0, -40($fp)
	lw         $t1, -60($fp)
	li         $v0, 1
	sw         $v0, -64($fp)
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
	sw         $v0, -64($fp)
	end_loop_1:

	#          local_16 = local_15 ;
	lw         $t0, -64($fp)
	sw         $t0, -68($fp)
	#          IF local_16 GOTO label_1 ;
	lw         $t0, -68($fp)
	bnez       $t0, label_1
	#          local_24 = 0 ;
	li         $t0, 0
	sw         $t0, -100($fp)
	#          GOTO label_2 ;
	b          label_2
	#          LABEL label_1 ;
	label_1:

	#          local_17 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -72($fp)
	#          local_20 = VCALL String length ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_length
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -84($fp)
	#          local_21 = local_20 - 2 ;
	lw         $t0, -84($fp)
	li         $t1, 2
	sub        $t0, $t0, $t1
	sw         $t0, -88($fp)
	#          local_22 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG s ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_21 ;
	lw         $t0, -88($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 8 ;
	li         $t0, 8
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -92($fp)
	#          local_23 = VCALL local_17 pal ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_22 ;
	lw         $t0, -92($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -72($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -96($fp)
	#          local_24 = local_23 ;
	lw         $t0, -96($fp)
	sw         $t0, -100($fp)
	#          LABEL label_2 ;
	label_2:

	#          local_25 = local_24 ;
	lw         $t0, -100($fp)
	sw         $t0, -104($fp)
	#          GOTO label_4 ;
	b          label_4
	#          LABEL label_3 ;
	label_3:

	#          local_25 = 1 ;
	li         $t0, 1
	sw         $t0, -104($fp)
	#          LABEL label_4 ;
	label_4:

	#          local_26 = local_25 ;
	lw         $t0, -104($fp)
	sw         $t0, -108($fp)
	#          GOTO label_6 ;
	b          label_6
	#          LABEL label_5 ;
	label_5:

	#          local_26 = 1 ;
	li         $t0, 1
	sw         $t0, -108($fp)
	#          LABEL label_6 ;
	label_6:

	#          RETURN local_26 ;
	lw         $v0, -108($fp)
	addu       $sp, $sp, 108
	jr         $ra
Main_main:
	move       $fp, $sp
	subu       $sp, $sp, 60
	#          local_0 = ~ 1
	li         $t0, 1
	not        $t0, $t0
	sw         $t0, -4($fp)
	#          SETATTR self i local_0 ;
	lw         $t0, -4($fp)
	lw         $t1, 0($fp)
	sw         $t0, 12($t1)
	#          local_1 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -8($fp)
	#          local_2 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -12($fp)
	#          local_3 = VCALL local_1 out_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_2 ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -8($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -16($fp)
	#          local_4 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -20($fp)
	#          local_5 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -24($fp)
	#          local_6 = VCALL local_5 in_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -24($fp)
	ulw        $t1, 20($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -28($fp)
	#          local_7 = VCALL local_4 pal ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_6 ;
	lw         $t0, -28($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -20($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          IF local_7 GOTO label_7 ;
	lw         $t0, -32($fp)
	bnez       $t0, label_7
	#          local_11 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -48($fp)
	#          local_12 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -52($fp)
	#          local_13 = VCALL local_11 out_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_12 ;
	lw         $t0, -52($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -48($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -56($fp)
	#          local_14 = local_13 ;
	lw         $t0, -56($fp)
	sw         $t0, -60($fp)
	#          GOTO label_8 ;
	b          label_8
	#          LABEL label_7 ;
	label_7:

	#          local_8 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -36($fp)
	#          local_9 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -40($fp)
	#          local_10 = VCALL local_8 out_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_9 ;
	lw         $t0, -40($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -36($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -44($fp)
	#          local_14 = local_10 ;
	lw         $t0, -44($fp)
	sw         $t0, -60($fp)
	#          LABEL label_8 ;
	label_8:

	#          RETURN local_14 ;
	lw         $v0, -60($fp)
	addu       $sp, $sp, 60
	jr         $ra

.data
	data_1:
		.asciiz    "Main"
	data_2:
		.asciiz    "enter a string\n"
	data_3:
		.asciiz    "that was a palindrome\n"
	data_4:
		.asciiz    "that was not a palindrome\n"
	data_5:
		.asciiz    "Bool"
	data_6:
		.asciiz    "Int"
	data_7:
		.asciiz    "String"
	data_abort:
		.asciiz    "Abort called from class "
	new_line:
		.asciiz    "\n"
	concat_result:
		.space     2048
	substring_result:
		.space     4096
	read_result:
		.space     2048
	vt_Object:
		.space     152
	vt_IO:
		.space     152
	vt_Int:
		.space     152
	vt_String:
		.space     152
	vt_Bool:
		.space     152
	vt_Main:
		.space     152
	abort_String:
		.asciiz    "String"
	abort_Int:
		.asciiz    "Int"
	abort_Bool:
		.asciiz    "Bool"
