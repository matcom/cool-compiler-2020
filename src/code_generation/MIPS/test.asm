
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
	#          local_18 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -4($fp)
	#          RETURN local_18 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Int_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_19 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -4($fp)
	#          RETURN local_19 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_20 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -4($fp)
	#          RETURN local_20 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Main_main:
	move       $fp, $sp
	subu       $sp, $sp, 72
	#          local_1 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -8($fp)
	#          local_4 = ALLOCATE Object ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -20($fp)
	la         $t0, vt_Object
	sw         $t0, 8($v0)
	#          local_5 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -24($fp)
	#          SETATTR local_4 @type local_5 ;
	lw         $t0, -24($fp)
	lw         $t1, -20($fp)
	sw         $t0, 0($t1)
	#          local_6 = 12 ;
	li         $t0, 12
	sw         $t0, -28($fp)
	#          SETATTR local_4 @size local_6 ;
	lw         $t0, -28($fp)
	lw         $t1, -20($fp)
	sw         $t0, 4($t1)
	#          local_3 = GETTYPEADDR local_4 ;
	lw         $t1, -20($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_7 = VCALL local_3 type_name ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 4($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          local_8 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 4 ;
	li         $t0, 4
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
	sw         $v0, -36($fp)
	#          local_9 = VCALL local_1 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_8 ;
	lw         $t0, -36($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -8($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -40($fp)
	#          local_0 = GETTYPEADDR local_9 ;
	lw         $t1, -40($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_12 = VCALL Bool type_name ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        Bool_type_name
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = VCALL String substr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_12 ;
	lw         $t0, -52($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1 ;
	li         $t0, 1
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 3 ;
	li         $t0, 3
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -56($fp)
	#          local_14 = VCALL local_0 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_9 ;
	lw         $t0, -40($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_13 ;
	lw         $t0, -56($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 12($t0)
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
	#          local_16 = LOAD data_3 ;
	la         $t0, data_3
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
	#          RETURN local_17 ;
	lw         $v0, -72($fp)
	addu       $sp, $sp, 72
	jr         $ra

.data
	data_1:
		.asciiz    "Main"
	data_2:
		.asciiz    "Object"
	data_3:
		.asciiz    "\n"
	data_4:
		.asciiz    "Bool"
	data_5:
		.asciiz    "Int"
	data_6:
		.asciiz    "String"
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
	abort_Int:
		.asciiz    "Int"
	abort_Bool:
		.asciiz    "Bool"
