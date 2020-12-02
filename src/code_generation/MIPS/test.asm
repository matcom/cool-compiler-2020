
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
	la         $t0, Main_main
	usw        $t0, vt_Main+40
	la         $t0, Object_abort
	usw        $t0, vt_Complex+0
	la         $t0, Object_type_name
	usw        $t0, vt_Complex+4
	la         $t0, Object_copy
	usw        $t0, vt_Complex+8
	la         $t0, IO_out_string
	usw        $t0, vt_Complex+12
	la         $t0, IO_out_int
	usw        $t0, vt_Complex+16
	la         $t0, IO_in_string
	usw        $t0, vt_Complex+20
	la         $t0, IO_in_int
	usw        $t0, vt_Complex+24
	la         $t0, Complex_init
	usw        $t0, vt_Complex+44
	la         $t0, Complex_print
	usw        $t0, vt_Complex+48
	la         $t0, Complex_reflect_0
	usw        $t0, vt_Complex+52
	la         $t0, Complex_reflect_X
	usw        $t0, vt_Complex+56
	la         $t0, Complex_reflect_Y
	usw        $t0, vt_Complex+60
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
	#          local_5 = LOAD data_7 ;
	la         $t0, data_7
	sw         $t0, -4($fp)
	#          RETURN local_5 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Int_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_6 = LOAD data_8 ;
	la         $t0, data_8
	sw         $t0, -4($fp)
	#          RETURN local_6 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_7 = LOAD data_9 ;
	la         $t0, data_9
	sw         $t0, -4($fp)
	#          RETURN local_7 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Main_main:
	move       $fp, $sp
	subu       $sp, $sp, 84
	#          local_1 = ALLOCATE Complex ;
	li         $a0, 20
	li         $v0, 9
	syscall
	sw         $v0, -8($fp)
	la         $t0, vt_Complex
	sw         $t0, 8($v0)
	#          local_2 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -12($fp)
	#          SETATTR local_1 @type local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, -8($fp)
	sw         $t0, 0($t1)
	#          local_3 = 20 ;
	li         $t0, 20
	sw         $t0, -16($fp)
	#          SETATTR local_1 @size local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, -8($fp)
	sw         $t0, 4($t1)
	#          local_0 = GETTYPEADDR local_1 ;
	lw         $t1, -8($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_4 = VCALL local_0 init ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          c = local_4 ;
	lw         $t0, -20($fp)
	sw         $t0, -24($fp)
	#          local_7 = GETTYPEADDR c ;
	lw         $t1, -24($fp)
	lw         $t0, 8($t1)
	sw         $t0, -32($fp)
	#          local_8 = VCALL local_7 reflect_X ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG c ;
	lw         $t0, -24($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -32($fp)
	ulw        $t1, 56($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          local_6 = GETTYPEADDR local_8 ;
	lw         $t1, -36($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_9 = VCALL local_6 reflect_Y ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG local_8 ;
	lw         $t0, -36($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 60($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -40($fp)
	#          local_10 = GETTYPEADDR c ;
	lw         $t1, -24($fp)
	lw         $t0, 8($t1)
	sw         $t0, -44($fp)
	#          local_11 = VCALL local_10 reflect_0 ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG c ;
	lw         $t0, -24($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -44($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          local_12 = local_9 == local_11 ;
	lw         $t0, -40($fp)
	lw         $t1, -48($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -52($fp)
	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          IF local_13 GOTO label_1 ;
	lw         $t0, -56($fp)
	bnez       $t0, label_1
	#          local_17 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -72($fp)
	#          local_18 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -76($fp)
	#          local_19 = VCALL local_17 out_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_18 ;
	lw         $t0, -76($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -72($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -80($fp)
	#          local_20 = local_19 ;
	lw         $t0, -80($fp)
	sw         $t0, -84($fp)
	#          GOTO label_2 ;
	b          label_2
	#          LABEL label_1 ;
	label_1:

	#          local_14 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -60($fp)
	#          local_15 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -64($fp)
	#          local_16 = VCALL local_14 out_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_15 ;
	lw         $t0, -64($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -60($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -68($fp)
	#          local_20 = local_16 ;
	lw         $t0, -68($fp)
	sw         $t0, -84($fp)
	#          LABEL label_2 ;
	label_2:

	#          RETURN local_20 ;
	lw         $v0, -84($fp)
	addu       $sp, $sp, 84
	jr         $ra
Complex_init:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_0 = GETATTR self x ;
	lw         $t0, 8($fp)
	lw         $t1, 12($t0)
	sw         $t1, -4($fp)
	#          local_1 = local_0 == a ;
	lw         $t0, -4($fp)
	lw         $t1, 4($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          local_2 = local_1 ;
	lw         $t0, -8($fp)
	sw         $t0, -12($fp)
	#          local_3 = GETATTR self y ;
	lw         $t0, 8($fp)
	lw         $t1, 16($t0)
	sw         $t1, -16($fp)
	#          local_4 = local_3 == b ;
	lw         $t0, -16($fp)
	lw         $t1, 0($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -20($fp)
	#          local_5 = local_4 ;
	lw         $t0, -20($fp)
	sw         $t0, -24($fp)
	#          RETURN self ;
	lw         $v0, 8($fp)
	addu       $sp, $sp, 24
	jr         $ra
Complex_print:
	move       $fp, $sp
	subu       $sp, $sp, 76
	#          local_0 = GETATTR self y ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -4($fp)
	#          local_1 = local_0 == 0 ;
	lw         $t0, -4($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          local_2 = local_1 ;
	lw         $t0, -8($fp)
	sw         $t0, -12($fp)
	#          IF local_2 GOTO label_3 ;
	lw         $t0, -12($fp)
	bnez       $t0, label_3
	#          local_9 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -40($fp)
	#          local_10 = GETATTR self x ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -44($fp)
	#          local_11 = VCALL local_9 out_int ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_10 ;
	lw         $t0, -44($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -40($fp)
	ulw        $t1, 16($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          local_8 = GETTYPEADDR local_11 ;
	lw         $t1, -48($fp)
	lw         $t0, 8($t1)
	sw         $t0, -36($fp)
	#          local_12 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -52($fp)
	#          local_13 = VCALL local_8 out_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG local_11 ;
	lw         $t0, -48($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_12 ;
	lw         $t0, -52($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -36($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -56($fp)
	#          local_7 = GETTYPEADDR local_13 ;
	lw         $t1, -56($fp)
	lw         $t0, 8($t1)
	sw         $t0, -32($fp)
	#          local_14 = GETATTR self y ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -60($fp)
	#          local_15 = VCALL local_7 out_int ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG local_13 ;
	lw         $t0, -56($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_14 ;
	lw         $t0, -60($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -32($fp)
	ulw        $t1, 16($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -64($fp)
	#          local_6 = GETTYPEADDR local_15 ;
	lw         $t1, -64($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_16 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -68($fp)
	#          local_17 = VCALL local_6 out_string ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG local_15 ;
	lw         $t0, -64($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_16 ;
	lw         $t0, -68($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -72($fp)
	#          local_18 = local_17 ;
	lw         $t0, -72($fp)
	sw         $t0, -76($fp)
	#          GOTO label_4 ;
	b          label_4
	#          LABEL label_3 ;
	label_3:

	#          local_3 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_4 = GETATTR self x ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -20($fp)
	#          local_5 = VCALL local_3 out_int ;
	subu       $sp, $sp, 8
	sw         $fp, 0($sp)
	sw         $ra, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 16($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $fp, 0($sp)
	lw         $ra, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_18 = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -76($fp)
	#          LABEL label_4 ;
	label_4:

	#          RETURN local_18 ;
	lw         $v0, -76($fp)
	addu       $sp, $sp, 76
	jr         $ra
Complex_reflect_0:
	move       $fp, $sp
	subu       $sp, $sp, 40
	#          local_0 = GETATTR self x ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -4($fp)
	#          local_1 = GETATTR self x ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -8($fp)
	#          local_2 = ~ local_1
	not        $t0, $t0
	sw         $t0, -12($fp)
	#          local_3 = local_0 == local_2 ;
	lw         $t0, -4($fp)
	lw         $t1, -12($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          local_4 = local_3 ;
	lw         $t0, -16($fp)
	sw         $t0, -20($fp)
	#          local_5 = GETATTR self y ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -24($fp)
	#          local_6 = GETATTR self y ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -28($fp)
	#          local_7 = ~ local_6
	not        $t0, $t0
	sw         $t0, -32($fp)
	#          local_8 = local_5 == local_7 ;
	lw         $t0, -24($fp)
	lw         $t1, -32($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -36($fp)
	#          local_9 = local_8 ;
	lw         $t0, -36($fp)
	sw         $t0, -40($fp)
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 40
	jr         $ra
Complex_reflect_X:
	move       $fp, $sp
	subu       $sp, $sp, 20
	#          local_0 = GETATTR self y ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -4($fp)
	#          local_1 = GETATTR self y ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -8($fp)
	#          local_2 = ~ local_1
	not        $t0, $t0
	sw         $t0, -12($fp)
	#          local_3 = local_0 == local_2 ;
	lw         $t0, -4($fp)
	lw         $t1, -12($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          local_4 = local_3 ;
	lw         $t0, -16($fp)
	sw         $t0, -20($fp)
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 20
	jr         $ra
Complex_reflect_Y:
	move       $fp, $sp
	subu       $sp, $sp, 20
	#          local_0 = GETATTR self x ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -4($fp)
	#          local_1 = GETATTR self x ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -8($fp)
	#          local_2 = ~ local_1
	not        $t0, $t0
	sw         $t0, -12($fp)
	#          local_3 = local_0 == local_2 ;
	lw         $t0, -4($fp)
	lw         $t1, -12($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          local_4 = local_3 ;
	lw         $t0, -16($fp)
	sw         $t0, -20($fp)
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 20
	jr         $ra

.data
	data_1:
		.asciiz    "Main"
	data_2:
		.asciiz    "Complex"
	data_3:
		.asciiz    "=)\n"
	data_4:
		.asciiz    "=(\n"
	data_5:
		.asciiz    "+"
	data_6:
		.asciiz    "I"
	data_7:
		.asciiz    "Bool"
	data_8:
		.asciiz    "Int"
	data_9:
		.asciiz    "String"
	data_abort:
		.asciiz    "Abort called from class "
	new_line:
		.asciiz    "\n"
	vt_Object:
		.space     200
	vt_IO:
		.space     200
	vt_Int:
		.space     200
	vt_String:
		.space     200
	vt_Bool:
		.space     200
	vt_Main:
		.space     200
	vt_Complex:
		.space     200
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
