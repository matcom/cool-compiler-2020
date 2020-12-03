
.text
main:
	move       $fp, $sp
	subu       $sp, $sp, 12
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
	usw        $t0, vt_A+0
	la         $t0, Object_type_name
	usw        $t0, vt_A+4
	la         $t0, Object_copy
	usw        $t0, vt_A+8
	la         $t0, A_value
	usw        $t0, vt_A+40
	la         $t0, A_set_var
	usw        $t0, vt_A+44
	la         $t0, A_method1
	usw        $t0, vt_A+48
	la         $t0, A_method2
	usw        $t0, vt_A+52
	la         $t0, A_method3
	usw        $t0, vt_A+56
	la         $t0, A_method4
	usw        $t0, vt_A+60
	la         $t0, A_method5
	usw        $t0, vt_A+64
	la         $t0, A___init__
	usw        $t0, vt_A+68
	la         $t0, Object_abort
	usw        $t0, vt_B+0
	la         $t0, Object_type_name
	usw        $t0, vt_B+4
	la         $t0, Object_copy
	usw        $t0, vt_B+8
	la         $t0, A_value
	usw        $t0, vt_B+40
	la         $t0, A_set_var
	usw        $t0, vt_B+44
	la         $t0, A_method1
	usw        $t0, vt_B+48
	la         $t0, A_method2
	usw        $t0, vt_B+52
	la         $t0, A_method3
	usw        $t0, vt_B+56
	la         $t0, A_method4
	usw        $t0, vt_B+60
	la         $t0, B_method5
	usw        $t0, vt_B+64
	la         $t0, B___init__
	usw        $t0, vt_B+68
	la         $t0, Object_abort
	usw        $t0, vt_C+0
	la         $t0, Object_type_name
	usw        $t0, vt_C+4
	la         $t0, Object_copy
	usw        $t0, vt_C+8
	la         $t0, A_value
	usw        $t0, vt_C+40
	la         $t0, A_set_var
	usw        $t0, vt_C+44
	la         $t0, A_method1
	usw        $t0, vt_C+48
	la         $t0, A_method2
	usw        $t0, vt_C+52
	la         $t0, A_method3
	usw        $t0, vt_C+56
	la         $t0, A_method4
	usw        $t0, vt_C+60
	la         $t0, C_method5
	usw        $t0, vt_C+64
	la         $t0, C_method6
	usw        $t0, vt_C+72
	la         $t0, C___init__
	usw        $t0, vt_C+68
	la         $t0, Object_abort
	usw        $t0, vt_D+0
	la         $t0, Object_type_name
	usw        $t0, vt_D+4
	la         $t0, Object_copy
	usw        $t0, vt_D+8
	la         $t0, A_value
	usw        $t0, vt_D+40
	la         $t0, A_set_var
	usw        $t0, vt_D+44
	la         $t0, A_method1
	usw        $t0, vt_D+48
	la         $t0, A_method2
	usw        $t0, vt_D+52
	la         $t0, A_method3
	usw        $t0, vt_D+56
	la         $t0, A_method4
	usw        $t0, vt_D+60
	la         $t0, B_method5
	usw        $t0, vt_D+64
	la         $t0, D_method7
	usw        $t0, vt_D+76
	la         $t0, D___init__
	usw        $t0, vt_D+68
	la         $t0, Object_abort
	usw        $t0, vt_E+0
	la         $t0, Object_type_name
	usw        $t0, vt_E+4
	la         $t0, Object_copy
	usw        $t0, vt_E+8
	la         $t0, A_value
	usw        $t0, vt_E+40
	la         $t0, A_set_var
	usw        $t0, vt_E+44
	la         $t0, A_method1
	usw        $t0, vt_E+48
	la         $t0, A_method2
	usw        $t0, vt_E+52
	la         $t0, A_method3
	usw        $t0, vt_E+56
	la         $t0, A_method4
	usw        $t0, vt_E+60
	la         $t0, B_method5
	usw        $t0, vt_E+64
	la         $t0, D_method7
	usw        $t0, vt_E+76
	la         $t0, E_method6
	usw        $t0, vt_E+72
	la         $t0, E___init__
	usw        $t0, vt_E+68
	la         $t0, Object_abort
	usw        $t0, vt_A2I+0
	la         $t0, Object_type_name
	usw        $t0, vt_A2I+4
	la         $t0, Object_copy
	usw        $t0, vt_A2I+8
	la         $t0, A2I_c2i
	usw        $t0, vt_A2I+80
	la         $t0, A2I_i2c
	usw        $t0, vt_A2I+84
	la         $t0, A2I_a2i
	usw        $t0, vt_A2I+88
	la         $t0, A2I_a2i_aux
	usw        $t0, vt_A2I+92
	la         $t0, A2I_i2a
	usw        $t0, vt_A2I+96
	la         $t0, A2I_i2a_aux
	usw        $t0, vt_A2I+100
	la         $t0, A2I___init__
	usw        $t0, vt_A2I+68
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
	la         $t0, Main_menu
	usw        $t0, vt_Main+104
	la         $t0, Main_prompt
	usw        $t0, vt_Main+108
	la         $t0, Main_get_int
	usw        $t0, vt_Main+112
	la         $t0, Main_is_even
	usw        $t0, vt_Main+116
	la         $t0, Main_class_type
	usw        $t0, vt_Main+120
	la         $t0, Main_print
	usw        $t0, vt_Main+124
	la         $t0, Main_main
	usw        $t0, vt_Main+128
	la         $t0, Main___init__
	usw        $t0, vt_Main+68
	#          self = ALLOCATE Main ;
	li         $a0, 28
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	la         $t0, vt_Main
	sw         $t0, 8($v0)
	#          local_1 = VCALL Main __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        Main___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
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
	sw         $v0, -12($fp)
	#          RETURN main_result ;
	lw         $v0, -12($fp)
	addu       $sp, $sp, 12
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

	sb         $zero, ($t0)
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

	sb         $zero, ($t1)
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
	#          local_228 = LOAD data_66 ;
	la         $t0, data_66
	sw         $t0, -4($fp)
	#          RETURN local_228 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Int_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_229 = LOAD data_67 ;
	la         $t0, data_67
	sw         $t0, -4($fp)
	#          RETURN local_229 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_230 = LOAD data_68 ;
	la         $t0, data_68
	sw         $t0, -4($fp)
	#          RETURN local_230 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
A___init__:
	move       $fp, $sp
	subu       $sp, $sp, 12
	#          local_1 = LOAD data_1 ;
	la         $t0, data_1
	sw         $t0, -8($fp)
	#          SETATTR self @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, 0($fp)
	sw         $t0, 0($t1)
	#          local_2 = 16 ;
	li         $t0, 16
	sw         $t0, -12($fp)
	#          SETATTR self size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          SETATTR self var 0 ;
	li         $t0, 0
	lw         $t1, 0($fp)
	sw         $t0, 12($t1)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
A_value:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_0 = GETATTR self var ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -4($fp)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
A_set_var:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          SETATTR self var num ;
	lw         $t0, 0($fp)
	lw         $t1, 4($fp)
	sw         $t0, 12($t1)
	#          RETURN self ;
	lw         $v0, 4($fp)
	addu       $sp, $sp, 0
	jr         $ra
A_method1:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          RETURN self ;
	lw         $v0, 4($fp)
	addu       $sp, $sp, 0
	jr         $ra
A_method2:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_0 = num1 + num2 ;
	lw         $t0, 4($fp)
	lw         $t1, 0($fp)
	add        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          x = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          local_3 = ALLOCATE B ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -16($fp)
	la         $t0, vt_B
	sw         $t0, 8($v0)
	#          local_4 = VCALL B __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        B___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          local_2 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_5 = VCALL local_2 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          RETURN local_5 ;
	lw         $v0, -24($fp)
	addu       $sp, $sp, 24
	jr         $ra
A_method3:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_0 = ~ num
	lw         $t0, 0($fp)
	neg        $t0, $t0
	sw         $t0, -4($fp)
	#          x = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          local_3 = ALLOCATE C ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -16($fp)
	la         $t0, vt_C
	sw         $t0, 8($v0)
	#          local_4 = VCALL C __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        C___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          local_2 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_5 = VCALL local_2 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          RETURN local_5 ;
	lw         $v0, -24($fp)
	addu       $sp, $sp, 24
	jr         $ra
A_method4:
	move       $fp, $sp
	subu       $sp, $sp, 52
	#          local_0 = num2 < num1 ;
	lw         $t0, 0($fp)
	lw         $t1, 4($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          IF local_0 GOTO label_1 ;
	lw         $t0, -4($fp)
	bnez       $t0, label_1
	#          local_7 = num2 - num1 ;
	lw         $t0, 0($fp)
	lw         $t1, 4($fp)
	sub        $t0, $t0, $t1
	sw         $t0, -32($fp)
	#          x = local_7 ;
	lw         $t0, -32($fp)
	sw         $t0, -12($fp)
	#          local_9 = ALLOCATE D ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -40($fp)
	la         $t0, vt_D
	sw         $t0, 8($v0)
	#          local_10 = VCALL D __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_9 ;
	lw         $t0, -40($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        D___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -44($fp)
	#          local_8 = GETTYPEADDR local_9 ;
	lw         $t1, -40($fp)
	lw         $t0, 8($t1)
	sw         $t0, -36($fp)
	#          local_11 = VCALL local_8 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_9 ;
	lw         $t0, -40($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -12($fp)
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
	#          local_12 = local_11 ;
	lw         $t0, -48($fp)
	sw         $t0, -52($fp)
	#          GOTO label_2 ;
	b          label_2
	#          LABEL label_1 ;
	label_1:

	#          local_1 = num1 - num2 ;
	lw         $t0, 4($fp)
	lw         $t1, 0($fp)
	sub        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          x = local_1 ;
	lw         $t0, -8($fp)
	sw         $t0, -12($fp)
	#          local_4 = ALLOCATE D ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -20($fp)
	la         $t0, vt_D
	sw         $t0, 8($v0)
	#          local_5 = VCALL D __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        D___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_3 = GETTYPEADDR local_4 ;
	lw         $t1, -20($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_6 = VCALL local_3 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -28($fp)
	#          local_12 = local_6 ;
	lw         $t0, -28($fp)
	sw         $t0, -52($fp)
	#          LABEL label_2 ;
	label_2:

	#          RETURN local_12 ;
	lw         $v0, -52($fp)
	addu       $sp, $sp, 52
	jr         $ra
A_method5:
	move       $fp, $sp
	subu       $sp, $sp, 40
	#          x = 1 ;
	li         $t0, 1
	sw         $t0, -4($fp)
	#          y = 1 ;
	li         $t0, 1
	sw         $t0, -8($fp)
	#          LABEL label_3 ;
	label_3:

	#          local_2 = y <= num ;
	lw         $t0, -8($fp)
	lw         $t1, 0($fp)
	sle        $t0, $t0, $t1
	sw         $t0, -12($fp)
	#          IF local_2 GOTO label_4 ;
	lw         $t0, -12($fp)
	bnez       $t0, label_4
	#          GOTO label_5 ;
	b          label_5
	#          LABEL label_4 ;
	label_4:

	#          local_3 = x * y ;
	lw         $t0, -4($fp)
	lw         $t1, -8($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          x = local_3 ;
	lw         $t0, -16($fp)
	sw         $t0, -4($fp)
	#          local_4 = y + 1 ;
	lw         $t0, -8($fp)
	li         $t1, 1
	add        $t0, $t0, $t1
	sw         $t0, -20($fp)
	#          y = local_4 ;
	lw         $t0, -20($fp)
	sw         $t0, -8($fp)
	#          GOTO label_3 ;
	b          label_3
	#          LABEL label_5 ;
	label_5:

	#          local_5 = 0 ;
	li         $t0, 0
	sw         $t0, -24($fp)
	#          local_7 = ALLOCATE E ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -32($fp)
	la         $t0, vt_E
	sw         $t0, 8($v0)
	#          local_8 = VCALL E __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        E___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          local_6 = GETTYPEADDR local_7 ;
	lw         $t1, -32($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_9 = VCALL local_6 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -40($fp)
	#          RETURN local_9 ;
	lw         $v0, -40($fp)
	addu       $sp, $sp, 40
	jr         $ra
B___init__:
	move       $fp, $sp
	subu       $sp, $sp, 16
	#          local_1 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          local_2 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -12($fp)
	#          SETATTR self @type local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, 0($fp)
	sw         $t0, 0($t1)
	#          local_3 = 16 ;
	li         $t0, 16
	sw         $t0, -16($fp)
	#          SETATTR self size local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          SETATTR self var 0 ;
	li         $t0, 0
	lw         $t1, 0($fp)
	sw         $t0, 12($t1)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 16
	jr         $ra
B_method5:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_0 = num * num ;
	lw         $t0, 0($fp)
	lw         $t1, 0($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          x = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          local_3 = ALLOCATE E ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -16($fp)
	la         $t0, vt_E
	sw         $t0, 8($v0)
	#          local_4 = VCALL E __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        E___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          local_2 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_5 = VCALL local_2 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          RETURN local_5 ;
	lw         $v0, -24($fp)
	addu       $sp, $sp, 24
	jr         $ra
C___init__:
	move       $fp, $sp
	subu       $sp, $sp, 16
	#          local_1 = VCALL B __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        B___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          local_2 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -12($fp)
	#          SETATTR self @type local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, 0($fp)
	sw         $t0, 0($t1)
	#          local_3 = 16 ;
	li         $t0, 16
	sw         $t0, -16($fp)
	#          SETATTR self size local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          SETATTR self var 0 ;
	li         $t0, 0
	lw         $t1, 0($fp)
	sw         $t0, 12($t1)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 16
	jr         $ra
C_method6:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_0 = ~ num
	lw         $t0, 0($fp)
	neg        $t0, $t0
	sw         $t0, -4($fp)
	#          x = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          local_3 = ALLOCATE A ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -16($fp)
	la         $t0, vt_A
	sw         $t0, 8($v0)
	#          local_4 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          local_2 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_5 = VCALL local_2 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          RETURN local_5 ;
	lw         $v0, -24($fp)
	addu       $sp, $sp, 24
	jr         $ra
C_method5:
	move       $fp, $sp
	subu       $sp, $sp, 28
	#          local_0 = num * num ;
	lw         $t0, 0($fp)
	lw         $t1, 0($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          local_1 = local_0 * num ;
	lw         $t0, -4($fp)
	lw         $t1, 0($fp)
	mul        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          x = local_1 ;
	lw         $t0, -8($fp)
	sw         $t0, -12($fp)
	#          local_4 = ALLOCATE E ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -20($fp)
	la         $t0, vt_E
	sw         $t0, 8($v0)
	#          local_5 = VCALL E __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        E___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_3 = GETTYPEADDR local_4 ;
	lw         $t1, -20($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_6 = VCALL local_3 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -28($fp)
	#          RETURN local_6 ;
	lw         $v0, -28($fp)
	addu       $sp, $sp, 28
	jr         $ra
D___init__:
	move       $fp, $sp
	subu       $sp, $sp, 16
	#          local_1 = VCALL B __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        B___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          local_2 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -12($fp)
	#          SETATTR self @type local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, 0($fp)
	sw         $t0, 0($t1)
	#          local_3 = 16 ;
	li         $t0, 16
	sw         $t0, -16($fp)
	#          SETATTR self size local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          SETATTR self var 0 ;
	li         $t0, 0
	lw         $t1, 0($fp)
	sw         $t0, 12($t1)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 16
	jr         $ra
D_method7:
	move       $fp, $sp
	subu       $sp, $sp, 72
	#          x = num ;
	lw         $t0, 0($fp)
	sw         $t0, -4($fp)
	#          local_1 = x < 0 ;
	lw         $t0, -4($fp)
	li         $t1, 0
	slt        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          IF local_1 GOTO label_12 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_12
	#          local_5 = 0 == x ;
	li         $t0, 0
	lw         $t1, -4($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -24($fp)
	#          local_6 = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -28($fp)
	#          IF local_6 GOTO label_10 ;
	lw         $t0, -28($fp)
	bnez       $t0, label_10
	#          local_7 = 1 == x ;
	li         $t0, 1
	lw         $t1, -4($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -32($fp)
	#          local_8 = local_7 ;
	lw         $t0, -32($fp)
	sw         $t0, -36($fp)
	#          IF local_8 GOTO label_8 ;
	lw         $t0, -36($fp)
	bnez       $t0, label_8
	#          local_9 = 2 == x ;
	li         $t0, 2
	lw         $t1, -4($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -40($fp)
	#          local_10 = local_9 ;
	lw         $t0, -40($fp)
	sw         $t0, -44($fp)
	#          IF local_10 GOTO label_6 ;
	lw         $t0, -44($fp)
	bnez       $t0, label_6
	#          local_11 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -48($fp)
	#          local_12 = x - 3 ;
	lw         $t0, -4($fp)
	li         $t1, 3
	sub        $t0, $t0, $t1
	sw         $t0, -52($fp)
	#          local_13 = VCALL local_11 method7 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_12 ;
	lw         $t0, -52($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -48($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -56($fp)
	#          local_14 = local_13 ;
	lw         $t0, -56($fp)
	sw         $t0, -60($fp)
	#          GOTO label_7 ;
	b          label_7
	#          LABEL label_6 ;
	label_6:

	#          local_14 = 0 ;
	li         $t0, 0
	sw         $t0, -60($fp)
	#          LABEL label_7 ;
	label_7:

	#          local_15 = local_14 ;
	lw         $t0, -60($fp)
	sw         $t0, -64($fp)
	#          GOTO label_9 ;
	b          label_9
	#          LABEL label_8 ;
	label_8:

	#          local_15 = 0 ;
	li         $t0, 0
	sw         $t0, -64($fp)
	#          LABEL label_9 ;
	label_9:

	#          local_16 = local_15 ;
	lw         $t0, -64($fp)
	sw         $t0, -68($fp)
	#          GOTO label_11 ;
	b          label_11
	#          LABEL label_10 ;
	label_10:

	#          local_16 = 1 ;
	li         $t0, 1
	sw         $t0, -68($fp)
	#          LABEL label_11 ;
	label_11:

	#          local_17 = local_16 ;
	lw         $t0, -68($fp)
	sw         $t0, -72($fp)
	#          GOTO label_13 ;
	b          label_13
	#          LABEL label_12 ;
	label_12:

	#          local_2 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_3 = ~ x
	lw         $t0, -4($fp)
	neg        $t0, $t0
	sw         $t0, -16($fp)
	#          local_4 = VCALL local_2 method7 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          local_17 = local_4 ;
	lw         $t0, -20($fp)
	sw         $t0, -72($fp)
	#          LABEL label_13 ;
	label_13:

	#          RETURN local_17 ;
	lw         $v0, -72($fp)
	addu       $sp, $sp, 72
	jr         $ra
E___init__:
	move       $fp, $sp
	subu       $sp, $sp, 16
	#          local_1 = VCALL D __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        D___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          local_2 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -12($fp)
	#          SETATTR self @type local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, 0($fp)
	sw         $t0, 0($t1)
	#          local_3 = 16 ;
	li         $t0, 16
	sw         $t0, -16($fp)
	#          SETATTR self size local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          SETATTR self var 0 ;
	li         $t0, 0
	lw         $t1, 0($fp)
	sw         $t0, 12($t1)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 16
	jr         $ra
E_method6:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_0 = num / 8 ;
	lw         $t0, 0($fp)
	li         $t1, 8
	div        $t0, $t0, $t1
	sw         $t0, -4($fp)
	#          x = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          local_3 = ALLOCATE A ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -16($fp)
	la         $t0, vt_A
	sw         $t0, 8($v0)
	#          local_4 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          local_2 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_5 = VCALL local_2 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          RETURN local_5 ;
	lw         $v0, -24($fp)
	addu       $sp, $sp, 24
	jr         $ra
A2I___init__:
	move       $fp, $sp
	subu       $sp, $sp, 12
	#          local_1 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -8($fp)
	#          SETATTR self @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, 0($fp)
	sw         $t0, 0($t1)
	#          local_2 = 12 ;
	li         $t0, 12
	sw         $t0, -12($fp)
	#          SETATTR self size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
A2I_c2i:
	move       $fp, $sp
	subu       $sp, $sp, 168
	#          local_0 = LOAD data_7 ;
	la         $t0, data_7
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
	#          IF local_2 GOTO label_32 ;
	lw         $t0, -12($fp)
	bnez       $t0, label_32
	#          local_3 = LOAD data_8 ;
	la         $t0, data_8
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
	#          IF local_5 GOTO label_30 ;
	lw         $t0, -24($fp)
	bnez       $t0, label_30
	#          local_6 = LOAD data_9 ;
	la         $t0, data_9
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
	#          IF local_8 GOTO label_28 ;
	lw         $t0, -36($fp)
	bnez       $t0, label_28
	#          local_9 = LOAD data_10 ;
	la         $t0, data_10
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
	#          IF local_11 GOTO label_26 ;
	lw         $t0, -48($fp)
	bnez       $t0, label_26
	#          local_12 = LOAD data_11 ;
	la         $t0, data_11
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
	#          IF local_14 GOTO label_24 ;
	lw         $t0, -60($fp)
	bnez       $t0, label_24
	#          local_15 = LOAD data_12 ;
	la         $t0, data_12
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
	#          IF local_17 GOTO label_22 ;
	lw         $t0, -72($fp)
	bnez       $t0, label_22
	#          local_18 = LOAD data_13 ;
	la         $t0, data_13
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
	#          IF local_20 GOTO label_20 ;
	lw         $t0, -84($fp)
	bnez       $t0, label_20
	#          local_21 = LOAD data_14 ;
	la         $t0, data_14
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
	#          IF local_23 GOTO label_18 ;
	lw         $t0, -96($fp)
	bnez       $t0, label_18
	#          local_24 = LOAD data_15 ;
	la         $t0, data_15
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
	#          IF local_26 GOTO label_16 ;
	lw         $t0, -108($fp)
	bnez       $t0, label_16
	#          local_27 = LOAD data_16 ;
	la         $t0, data_16
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
	#          IF local_29 GOTO label_14 ;
	lw         $t0, -120($fp)
	bnez       $t0, label_14
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
	#          GOTO label_15 ;
	b          label_15
	#          LABEL label_14 ;
	label_14:

	#          local_32 = 9 ;
	li         $t0, 9
	sw         $t0, -132($fp)
	#          LABEL label_15 ;
	label_15:

	#          local_33 = local_32 ;
	lw         $t0, -132($fp)
	sw         $t0, -136($fp)
	#          GOTO label_17 ;
	b          label_17
	#          LABEL label_16 ;
	label_16:

	#          local_33 = 8 ;
	li         $t0, 8
	sw         $t0, -136($fp)
	#          LABEL label_17 ;
	label_17:

	#          local_34 = local_33 ;
	lw         $t0, -136($fp)
	sw         $t0, -140($fp)
	#          GOTO label_19 ;
	b          label_19
	#          LABEL label_18 ;
	label_18:

	#          local_34 = 7 ;
	li         $t0, 7
	sw         $t0, -140($fp)
	#          LABEL label_19 ;
	label_19:

	#          local_35 = local_34 ;
	lw         $t0, -140($fp)
	sw         $t0, -144($fp)
	#          GOTO label_21 ;
	b          label_21
	#          LABEL label_20 ;
	label_20:

	#          local_35 = 6 ;
	li         $t0, 6
	sw         $t0, -144($fp)
	#          LABEL label_21 ;
	label_21:

	#          local_36 = local_35 ;
	lw         $t0, -144($fp)
	sw         $t0, -148($fp)
	#          GOTO label_23 ;
	b          label_23
	#          LABEL label_22 ;
	label_22:

	#          local_36 = 5 ;
	li         $t0, 5
	sw         $t0, -148($fp)
	#          LABEL label_23 ;
	label_23:

	#          local_37 = local_36 ;
	lw         $t0, -148($fp)
	sw         $t0, -152($fp)
	#          GOTO label_25 ;
	b          label_25
	#          LABEL label_24 ;
	label_24:

	#          local_37 = 4 ;
	li         $t0, 4
	sw         $t0, -152($fp)
	#          LABEL label_25 ;
	label_25:

	#          local_38 = local_37 ;
	lw         $t0, -152($fp)
	sw         $t0, -156($fp)
	#          GOTO label_27 ;
	b          label_27
	#          LABEL label_26 ;
	label_26:

	#          local_38 = 3 ;
	li         $t0, 3
	sw         $t0, -156($fp)
	#          LABEL label_27 ;
	label_27:

	#          local_39 = local_38 ;
	lw         $t0, -156($fp)
	sw         $t0, -160($fp)
	#          GOTO label_29 ;
	b          label_29
	#          LABEL label_28 ;
	label_28:

	#          local_39 = 2 ;
	li         $t0, 2
	sw         $t0, -160($fp)
	#          LABEL label_29 ;
	label_29:

	#          local_40 = local_39 ;
	lw         $t0, -160($fp)
	sw         $t0, -164($fp)
	#          GOTO label_31 ;
	b          label_31
	#          LABEL label_30 ;
	label_30:

	#          local_40 = 1 ;
	li         $t0, 1
	sw         $t0, -164($fp)
	#          LABEL label_31 ;
	label_31:

	#          local_41 = local_40 ;
	lw         $t0, -164($fp)
	sw         $t0, -168($fp)
	#          GOTO label_33 ;
	b          label_33
	#          LABEL label_32 ;
	label_32:

	#          local_41 = 0 ;
	li         $t0, 0
	sw         $t0, -168($fp)
	#          LABEL label_33 ;
	label_33:

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
	#          IF local_1 GOTO label_52 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_52
	#          local_3 = i == 1 ;
	lw         $t0, 0($fp)
	li         $t1, 1
	seq        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          local_4 = local_3 ;
	lw         $t0, -16($fp)
	sw         $t0, -20($fp)
	#          IF local_4 GOTO label_50 ;
	lw         $t0, -20($fp)
	bnez       $t0, label_50
	#          local_6 = i == 2 ;
	lw         $t0, 0($fp)
	li         $t1, 2
	seq        $t0, $t0, $t1
	sw         $t0, -28($fp)
	#          local_7 = local_6 ;
	lw         $t0, -28($fp)
	sw         $t0, -32($fp)
	#          IF local_7 GOTO label_48 ;
	lw         $t0, -32($fp)
	bnez       $t0, label_48
	#          local_9 = i == 3 ;
	lw         $t0, 0($fp)
	li         $t1, 3
	seq        $t0, $t0, $t1
	sw         $t0, -40($fp)
	#          local_10 = local_9 ;
	lw         $t0, -40($fp)
	sw         $t0, -44($fp)
	#          IF local_10 GOTO label_46 ;
	lw         $t0, -44($fp)
	bnez       $t0, label_46
	#          local_12 = i == 4 ;
	lw         $t0, 0($fp)
	li         $t1, 4
	seq        $t0, $t0, $t1
	sw         $t0, -52($fp)
	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          IF local_13 GOTO label_44 ;
	lw         $t0, -56($fp)
	bnez       $t0, label_44
	#          local_15 = i == 5 ;
	lw         $t0, 0($fp)
	li         $t1, 5
	seq        $t0, $t0, $t1
	sw         $t0, -64($fp)
	#          local_16 = local_15 ;
	lw         $t0, -64($fp)
	sw         $t0, -68($fp)
	#          IF local_16 GOTO label_42 ;
	lw         $t0, -68($fp)
	bnez       $t0, label_42
	#          local_18 = i == 6 ;
	lw         $t0, 0($fp)
	li         $t1, 6
	seq        $t0, $t0, $t1
	sw         $t0, -76($fp)
	#          local_19 = local_18 ;
	lw         $t0, -76($fp)
	sw         $t0, -80($fp)
	#          IF local_19 GOTO label_40 ;
	lw         $t0, -80($fp)
	bnez       $t0, label_40
	#          local_21 = i == 7 ;
	lw         $t0, 0($fp)
	li         $t1, 7
	seq        $t0, $t0, $t1
	sw         $t0, -88($fp)
	#          local_22 = local_21 ;
	lw         $t0, -88($fp)
	sw         $t0, -92($fp)
	#          IF local_22 GOTO label_38 ;
	lw         $t0, -92($fp)
	bnez       $t0, label_38
	#          local_24 = i == 8 ;
	lw         $t0, 0($fp)
	li         $t1, 8
	seq        $t0, $t0, $t1
	sw         $t0, -100($fp)
	#          local_25 = local_24 ;
	lw         $t0, -100($fp)
	sw         $t0, -104($fp)
	#          IF local_25 GOTO label_36 ;
	lw         $t0, -104($fp)
	bnez       $t0, label_36
	#          local_27 = i == 9 ;
	lw         $t0, 0($fp)
	li         $t1, 9
	seq        $t0, $t0, $t1
	sw         $t0, -112($fp)
	#          local_28 = local_27 ;
	lw         $t0, -112($fp)
	sw         $t0, -116($fp)
	#          IF local_28 GOTO label_34 ;
	lw         $t0, -116($fp)
	bnez       $t0, label_34
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
	#          local_32 = LOAD data_17 ;
	la         $t0, data_17
	sw         $t0, -132($fp)
	#          local_33 = local_32 ;
	lw         $t0, -132($fp)
	sw         $t0, -136($fp)
	#          GOTO label_35 ;
	b          label_35
	#          LABEL label_34 ;
	label_34:

	#          local_29 = LOAD data_16 ;
	la         $t0, data_16
	sw         $t0, -120($fp)
	#          local_33 = local_29 ;
	lw         $t0, -120($fp)
	sw         $t0, -136($fp)
	#          LABEL label_35 ;
	label_35:

	#          local_34 = local_33 ;
	lw         $t0, -136($fp)
	sw         $t0, -140($fp)
	#          GOTO label_37 ;
	b          label_37
	#          LABEL label_36 ;
	label_36:

	#          local_26 = LOAD data_15 ;
	la         $t0, data_15
	sw         $t0, -108($fp)
	#          local_34 = local_26 ;
	lw         $t0, -108($fp)
	sw         $t0, -140($fp)
	#          LABEL label_37 ;
	label_37:

	#          local_35 = local_34 ;
	lw         $t0, -140($fp)
	sw         $t0, -144($fp)
	#          GOTO label_39 ;
	b          label_39
	#          LABEL label_38 ;
	label_38:

	#          local_23 = LOAD data_14 ;
	la         $t0, data_14
	sw         $t0, -96($fp)
	#          local_35 = local_23 ;
	lw         $t0, -96($fp)
	sw         $t0, -144($fp)
	#          LABEL label_39 ;
	label_39:

	#          local_36 = local_35 ;
	lw         $t0, -144($fp)
	sw         $t0, -148($fp)
	#          GOTO label_41 ;
	b          label_41
	#          LABEL label_40 ;
	label_40:

	#          local_20 = LOAD data_13 ;
	la         $t0, data_13
	sw         $t0, -84($fp)
	#          local_36 = local_20 ;
	lw         $t0, -84($fp)
	sw         $t0, -148($fp)
	#          LABEL label_41 ;
	label_41:

	#          local_37 = local_36 ;
	lw         $t0, -148($fp)
	sw         $t0, -152($fp)
	#          GOTO label_43 ;
	b          label_43
	#          LABEL label_42 ;
	label_42:

	#          local_17 = LOAD data_12 ;
	la         $t0, data_12
	sw         $t0, -72($fp)
	#          local_37 = local_17 ;
	lw         $t0, -72($fp)
	sw         $t0, -152($fp)
	#          LABEL label_43 ;
	label_43:

	#          local_38 = local_37 ;
	lw         $t0, -152($fp)
	sw         $t0, -156($fp)
	#          GOTO label_45 ;
	b          label_45
	#          LABEL label_44 ;
	label_44:

	#          local_14 = LOAD data_11 ;
	la         $t0, data_11
	sw         $t0, -60($fp)
	#          local_38 = local_14 ;
	lw         $t0, -60($fp)
	sw         $t0, -156($fp)
	#          LABEL label_45 ;
	label_45:

	#          local_39 = local_38 ;
	lw         $t0, -156($fp)
	sw         $t0, -160($fp)
	#          GOTO label_47 ;
	b          label_47
	#          LABEL label_46 ;
	label_46:

	#          local_11 = LOAD data_10 ;
	la         $t0, data_10
	sw         $t0, -48($fp)
	#          local_39 = local_11 ;
	lw         $t0, -48($fp)
	sw         $t0, -160($fp)
	#          LABEL label_47 ;
	label_47:

	#          local_40 = local_39 ;
	lw         $t0, -160($fp)
	sw         $t0, -164($fp)
	#          GOTO label_49 ;
	b          label_49
	#          LABEL label_48 ;
	label_48:

	#          local_8 = LOAD data_9 ;
	la         $t0, data_9
	sw         $t0, -36($fp)
	#          local_40 = local_8 ;
	lw         $t0, -36($fp)
	sw         $t0, -164($fp)
	#          LABEL label_49 ;
	label_49:

	#          local_41 = local_40 ;
	lw         $t0, -164($fp)
	sw         $t0, -168($fp)
	#          GOTO label_51 ;
	b          label_51
	#          LABEL label_50 ;
	label_50:

	#          local_5 = LOAD data_8 ;
	la         $t0, data_8
	sw         $t0, -24($fp)
	#          local_41 = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -168($fp)
	#          LABEL label_51 ;
	label_51:

	#          local_42 = local_41 ;
	lw         $t0, -168($fp)
	sw         $t0, -172($fp)
	#          GOTO label_53 ;
	b          label_53
	#          LABEL label_52 ;
	label_52:

	#          local_2 = LOAD data_7 ;
	la         $t0, data_7
	sw         $t0, -12($fp)
	#          local_42 = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -172($fp)
	#          LABEL label_53 ;
	label_53:

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
	#          IF local_3 GOTO label_58 ;
	lw         $t0, -16($fp)
	bnez       $t0, label_58
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
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_6 = LOAD data_18 ;
	la         $t0, data_18
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
	#          IF local_8 GOTO label_56 ;
	lw         $t0, -36($fp)
	bnez       $t0, label_56
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
	#          ARG 2048 ;
	li         $t0, 2048
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -76($fp)
	#          local_19 = LOAD data_19 ;
	la         $t0, data_19
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
	#          IF local_21 GOTO label_54 ;
	lw         $t0, -88($fp)
	bnez       $t0, label_54
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
	ulw        $t1, 92($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -124($fp)
	#          local_31 = local_30 ;
	lw         $t0, -124($fp)
	sw         $t0, -128($fp)
	#          GOTO label_55 ;
	b          label_55
	#          LABEL label_54 ;
	label_54:

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
	#          ARG 3072 ;
	li         $t0, 3072
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
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
	ulw        $t1, 92($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -116($fp)
	#          local_31 = local_28 ;
	lw         $t0, -116($fp)
	sw         $t0, -128($fp)
	#          LABEL label_55 ;
	label_55:

	#          local_32 = local_31 ;
	lw         $t0, -128($fp)
	sw         $t0, -132($fp)
	#          GOTO label_57 ;
	b          label_57
	#          LABEL label_56 ;
	label_56:

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
	#          ARG 1024 ;
	li         $t0, 1024
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
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
	ulw        $t1, 92($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -64($fp)
	#          local_16 = ~ local_15
	lw         $t0, -64($fp)
	neg        $t0, $t0
	sw         $t0, -68($fp)
	#          local_32 = local_16 ;
	lw         $t0, -68($fp)
	sw         $t0, -132($fp)
	#          LABEL label_57 ;
	label_57:

	#          local_33 = local_32 ;
	lw         $t0, -132($fp)
	sw         $t0, -136($fp)
	#          GOTO label_59 ;
	b          label_59
	#          LABEL label_58 ;
	label_58:

	#          local_33 = 0 ;
	li         $t0, 0
	sw         $t0, -136($fp)
	#          LABEL label_59 ;
	label_59:

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
	#          LABEL label_60 ;
	label_60:

	#          local_5 = i < j ;
	lw         $t0, -20($fp)
	lw         $t1, -16($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -24($fp)
	#          IF local_5 GOTO label_61 ;
	lw         $t0, -24($fp)
	bnez       $t0, label_61
	#          GOTO label_62 ;
	b          label_62
	#          LABEL label_61 ;
	label_61:

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
	#          ARG 4096 ;
	li         $t0, 4096
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_substr
	addu       $sp, $sp, 16
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
	ulw        $t1, 80($t0)
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
	#          GOTO label_60 ;
	b          label_60
	#          LABEL label_62 ;
	label_62:

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
	#          IF local_1 GOTO label_65 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_65
	#          local_3 = 0 < i ;
	li         $t0, 0
	lw         $t1, 0($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -16($fp)
	#          IF local_3 GOTO label_63 ;
	lw         $t0, -16($fp)
	bnez       $t0, label_63
	#          local_7 = LOAD data_18 ;
	la         $t0, data_18
	sw         $t0, -32($fp)
	#          local_8 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -36($fp)
	#          local_9 = ~ 1
	li         $t0, 1
	neg        $t0, $t0
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
	ulw        $t1, 100($t0)
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
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_concat
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          GOTO label_64 ;
	b          label_64
	#          LABEL label_63 ;
	label_63:

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
	ulw        $t1, 100($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_13 = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -56($fp)
	#          LABEL label_64 ;
	label_64:

	#          local_14 = local_13 ;
	lw         $t0, -56($fp)
	sw         $t0, -60($fp)
	#          GOTO label_66 ;
	b          label_66
	#          LABEL label_65 ;
	label_65:

	#          local_2 = LOAD data_7 ;
	la         $t0, data_7
	sw         $t0, -12($fp)
	#          local_14 = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -60($fp)
	#          LABEL label_66 ;
	label_66:

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
	#          IF local_1 GOTO label_67 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_67
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
	ulw        $t1, 100($t0)
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
	ulw        $t1, 84($t0)
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
	#          ARG 1024 ;
	li         $t0, 1024
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        String_concat
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          GOTO label_68 ;
	b          label_68
	#          LABEL label_67 ;
	label_67:

	#          local_2 = LOAD data_17 ;
	la         $t0, data_17
	sw         $t0, -12($fp)
	#          local_13 = local_2 ;
	lw         $t0, -12($fp)
	sw         $t0, -56($fp)
	#          LABEL label_68 ;
	label_68:

	#          RETURN local_13 ;
	lw         $v0, -56($fp)
	addu       $sp, $sp, 56
	jr         $ra
Main___init__:
	move       $fp, $sp
	subu       $sp, $sp, 12
	#          local_1 = LOAD data_20 ;
	la         $t0, data_20
	sw         $t0, -8($fp)
	#          SETATTR self @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, 0($fp)
	sw         $t0, 0($t1)
	#          local_2 = 28 ;
	li         $t0, 28
	sw         $t0, -12($fp)
	#          SETATTR self size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          SETATTR self flag 1 ;
	li         $t0, 1
	lw         $t1, 0($fp)
	sw         $t0, 24($t1)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
Main_menu:
	move       $fp, $sp
	subu       $sp, $sp, 320
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = LOAD data_21 ;
	la         $t0, data_21
	sw         $t0, -8($fp)
	#          local_2 = VCALL local_0 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -12($fp)
	#          local_3 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_4 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -20($fp)
	#          local_5 = VCALL local_3 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          local_6 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_7 = LOAD data_22 ;
	la         $t0, data_22
	sw         $t0, -32($fp)
	#          local_8 = VCALL local_6 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          local_9 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -40($fp)
	#          local_10 = LOAD data_23 ;
	la         $t0, data_23
	sw         $t0, -44($fp)
	#          local_11 = VCALL local_9 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_10 ;
	lw         $t0, -44($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -40($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          local_12 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -52($fp)
	#          local_13 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -56($fp)
	#          local_14 = VCALL local_12 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_13 ;
	lw         $t0, -56($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -52($fp)
	ulw        $t1, 124($t0)
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
	#          local_16 = LOAD data_24 ;
	la         $t0, data_24
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
	#          local_19 = LOAD data_25 ;
	la         $t0, data_25
	sw         $t0, -80($fp)
	#          local_20 = VCALL local_18 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_19 ;
	lw         $t0, -80($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -76($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -84($fp)
	#          local_21 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -88($fp)
	#          local_22 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -92($fp)
	#          local_23 = VCALL local_21 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_22 ;
	lw         $t0, -92($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -88($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -96($fp)
	#          local_24 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -100($fp)
	#          local_25 = LOAD data_26 ;
	la         $t0, data_26
	sw         $t0, -104($fp)
	#          local_26 = VCALL local_24 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_25 ;
	lw         $t0, -104($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -100($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -108($fp)
	#          local_27 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -112($fp)
	#          local_28 = LOAD data_27 ;
	la         $t0, data_27
	sw         $t0, -116($fp)
	#          local_29 = VCALL local_27 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_28 ;
	lw         $t0, -116($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -112($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -120($fp)
	#          local_30 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -124($fp)
	#          local_31 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -128($fp)
	#          local_32 = VCALL local_30 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_31 ;
	lw         $t0, -128($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -124($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -132($fp)
	#          local_33 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -136($fp)
	#          local_34 = LOAD data_28 ;
	la         $t0, data_28
	sw         $t0, -140($fp)
	#          local_35 = VCALL local_33 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_34 ;
	lw         $t0, -140($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -136($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -144($fp)
	#          local_36 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -148($fp)
	#          local_37 = LOAD data_29 ;
	la         $t0, data_29
	sw         $t0, -152($fp)
	#          local_38 = VCALL local_36 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_37 ;
	lw         $t0, -152($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -148($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -156($fp)
	#          local_39 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -160($fp)
	#          local_40 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -164($fp)
	#          local_41 = VCALL local_39 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_40 ;
	lw         $t0, -164($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -160($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -168($fp)
	#          local_42 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -172($fp)
	#          local_43 = LOAD data_30 ;
	la         $t0, data_30
	sw         $t0, -176($fp)
	#          local_44 = VCALL local_42 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_43 ;
	lw         $t0, -176($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -172($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -180($fp)
	#          local_45 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -184($fp)
	#          local_46 = LOAD data_31 ;
	la         $t0, data_31
	sw         $t0, -188($fp)
	#          local_47 = VCALL local_45 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_46 ;
	lw         $t0, -188($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -184($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -192($fp)
	#          local_48 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -196($fp)
	#          local_49 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -200($fp)
	#          local_50 = VCALL local_48 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_49 ;
	lw         $t0, -200($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -196($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -204($fp)
	#          local_51 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -208($fp)
	#          local_52 = LOAD data_32 ;
	la         $t0, data_32
	sw         $t0, -212($fp)
	#          local_53 = VCALL local_51 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_52 ;
	lw         $t0, -212($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -208($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -216($fp)
	#          local_54 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -220($fp)
	#          local_55 = LOAD data_33 ;
	la         $t0, data_33
	sw         $t0, -224($fp)
	#          local_56 = VCALL local_54 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_55 ;
	lw         $t0, -224($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -220($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -228($fp)
	#          local_57 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -232($fp)
	#          local_58 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -236($fp)
	#          local_59 = VCALL local_57 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_58 ;
	lw         $t0, -236($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -232($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -240($fp)
	#          local_60 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -244($fp)
	#          local_61 = LOAD data_34 ;
	la         $t0, data_34
	sw         $t0, -248($fp)
	#          local_62 = VCALL local_60 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_61 ;
	lw         $t0, -248($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -244($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -252($fp)
	#          local_63 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -256($fp)
	#          local_64 = LOAD data_35 ;
	la         $t0, data_35
	sw         $t0, -260($fp)
	#          local_65 = VCALL local_63 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_64 ;
	lw         $t0, -260($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -256($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -264($fp)
	#          local_66 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -268($fp)
	#          local_67 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -272($fp)
	#          local_68 = VCALL local_66 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_67 ;
	lw         $t0, -272($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -268($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -276($fp)
	#          local_69 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -280($fp)
	#          local_70 = LOAD data_36 ;
	la         $t0, data_36
	sw         $t0, -284($fp)
	#          local_71 = VCALL local_69 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_70 ;
	lw         $t0, -284($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -280($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -288($fp)
	#          local_72 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -292($fp)
	#          local_73 = LOAD data_37 ;
	la         $t0, data_37
	sw         $t0, -296($fp)
	#          local_74 = VCALL local_72 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_73 ;
	lw         $t0, -296($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -292($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -300($fp)
	#          local_75 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -304($fp)
	#          local_76 = LOAD data_38 ;
	la         $t0, data_38
	sw         $t0, -308($fp)
	#          local_77 = VCALL local_75 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_76 ;
	lw         $t0, -308($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -304($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -312($fp)
	#          local_78 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -316($fp)
	#          local_79 = VCALL local_78 in_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 0 ;
	li         $t0, 0
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -316($fp)
	ulw        $t1, 20($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -320($fp)
	#          RETURN local_79 ;
	lw         $v0, -320($fp)
	addu       $sp, $sp, 320
	jr         $ra
Main_prompt:
	move       $fp, $sp
	subu       $sp, $sp, 32
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = LOAD data_39 ;
	la         $t0, data_39
	sw         $t0, -8($fp)
	#          local_2 = VCALL local_0 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -12($fp)
	#          local_3 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_4 = LOAD data_40 ;
	la         $t0, data_40
	sw         $t0, -20($fp)
	#          local_5 = VCALL local_3 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
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
	#          local_6 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_7 = VCALL local_6 in_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG 1024 ;
	li         $t0, 1024
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 20($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          RETURN local_7 ;
	lw         $v0, -32($fp)
	addu       $sp, $sp, 32
	jr         $ra
Main_get_int:
	move       $fp, $sp
	subu       $sp, $sp, 32
	#          local_0 = ALLOCATE A2I ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	la         $t0, vt_A2I
	sw         $t0, 8($v0)
	#          local_1 = VCALL A2I __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A2I___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          z = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -12($fp)
	#          local_3 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_4 = VCALL local_3 prompt ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 108($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          s = local_4 ;
	lw         $t0, -20($fp)
	sw         $t0, -24($fp)
	#          local_6 = GETTYPEADDR z ;
	lw         $t1, -12($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_7 = VCALL local_6 a2i ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG z ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG s ;
	lw         $t0, -24($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 88($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          RETURN local_7 ;
	lw         $v0, -32($fp)
	addu       $sp, $sp, 32
	jr         $ra
Main_is_even:
	move       $fp, $sp
	subu       $sp, $sp, 60
	#          x = num ;
	lw         $t0, 0($fp)
	sw         $t0, -4($fp)
	#          local_1 = x < 0 ;
	lw         $t0, -4($fp)
	li         $t1, 0
	slt        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          IF local_1 GOTO label_73 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_73
	#          local_5 = 0 == x ;
	li         $t0, 0
	lw         $t1, -4($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -24($fp)
	#          local_6 = local_5 ;
	lw         $t0, -24($fp)
	sw         $t0, -28($fp)
	#          IF local_6 GOTO label_71 ;
	lw         $t0, -28($fp)
	bnez       $t0, label_71
	#          local_7 = 1 == x ;
	li         $t0, 1
	lw         $t1, -4($fp)
	seq        $t0, $t0, $t1
	sw         $t0, -32($fp)
	#          local_8 = local_7 ;
	lw         $t0, -32($fp)
	sw         $t0, -36($fp)
	#          IF local_8 GOTO label_69 ;
	lw         $t0, -36($fp)
	bnez       $t0, label_69
	#          local_9 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -40($fp)
	#          local_10 = x - 2 ;
	lw         $t0, -4($fp)
	li         $t1, 2
	sub        $t0, $t0, $t1
	sw         $t0, -44($fp)
	#          local_11 = VCALL local_9 is_even ;
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
	lw         $t0, -40($fp)
	ulw        $t1, 116($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          local_12 = local_11 ;
	lw         $t0, -48($fp)
	sw         $t0, -52($fp)
	#          GOTO label_70 ;
	b          label_70
	#          LABEL label_69 ;
	label_69:

	#          local_12 = 0 ;
	li         $t0, 0
	sw         $t0, -52($fp)
	#          LABEL label_70 ;
	label_70:

	#          local_13 = local_12 ;
	lw         $t0, -52($fp)
	sw         $t0, -56($fp)
	#          GOTO label_72 ;
	b          label_72
	#          LABEL label_71 ;
	label_71:

	#          local_13 = 1 ;
	li         $t0, 1
	sw         $t0, -56($fp)
	#          LABEL label_72 ;
	label_72:

	#          local_14 = local_13 ;
	lw         $t0, -56($fp)
	sw         $t0, -60($fp)
	#          GOTO label_74 ;
	b          label_74
	#          LABEL label_73 ;
	label_73:

	#          local_2 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_3 = ~ x
	lw         $t0, -4($fp)
	neg        $t0, $t0
	sw         $t0, -16($fp)
	#          local_4 = VCALL local_2 is_even ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 116($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          local_14 = local_4 ;
	lw         $t0, -20($fp)
	sw         $t0, -60($fp)
	#          LABEL label_74 ;
	label_74:

	#          RETURN local_14 ;
	lw         $v0, -60($fp)
	addu       $sp, $sp, 60
	jr         $ra
Main_class_type:
	move       $fp, $sp
	subu       $sp, $sp, 172
	#          local_0 = TYPEOF var ;
	lw         $t0, 0($fp)
	lw         $t1, ($t0)
	sw         $t1, -4($fp)
	#          local_3 = LOAD data_1 ;
	la         $t0, data_1
	sw         $t0, -16($fp)
	#          local_2 = local_0 == local_3 ;
	lw         $t0, -4($fp)
	lw         $t1, -16($fp)
	li         $v0, 1
	sw         $v0, -12($fp)
	equal_loop_13:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_13
	beqz       $t2, end_loop_13
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_13
	b          end_loop_13
	not_equal_13:

	li         $v0, 0
	sw         $v0, -12($fp)
	end_loop_13:

	#          local_1 = local_2 == 0 ;
	lw         $t0, -12($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          IF local_1 GOTO label_75 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_75
	#          a = var ;
	lw         $t0, 0($fp)
	sw         $t0, -20($fp)
	#          local_5 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -24($fp)
	#          local_6 = LOAD data_41 ;
	la         $t0, data_41
	sw         $t0, -28($fp)
	#          local_7 = VCALL local_5 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_6 ;
	lw         $t0, -28($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -24($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          LABEL label_75 ;
	label_75:

	#          local_10 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -44($fp)
	#          local_9 = local_0 == local_10 ;
	lw         $t0, -4($fp)
	lw         $t1, -44($fp)
	li         $v0, 1
	sw         $v0, -40($fp)
	equal_loop_14:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_14
	beqz       $t2, end_loop_14
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_14
	b          end_loop_14
	not_equal_14:

	li         $v0, 0
	sw         $v0, -40($fp)
	end_loop_14:

	#          local_8 = local_9 == 0 ;
	lw         $t0, -40($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -36($fp)
	#          IF local_8 GOTO label_76 ;
	lw         $t0, -36($fp)
	bnez       $t0, label_76
	#          b = var ;
	lw         $t0, 0($fp)
	sw         $t0, -48($fp)
	#          local_12 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -52($fp)
	#          local_13 = LOAD data_42 ;
	la         $t0, data_42
	sw         $t0, -56($fp)
	#          local_14 = VCALL local_12 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_13 ;
	lw         $t0, -56($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -52($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -60($fp)
	#          LABEL label_76 ;
	label_76:

	#          local_17 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -72($fp)
	#          local_16 = local_0 == local_17 ;
	lw         $t0, -4($fp)
	lw         $t1, -72($fp)
	li         $v0, 1
	sw         $v0, -68($fp)
	equal_loop_15:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_15
	beqz       $t2, end_loop_15
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_15
	b          end_loop_15
	not_equal_15:

	li         $v0, 0
	sw         $v0, -68($fp)
	end_loop_15:

	#          local_15 = local_16 == 0 ;
	lw         $t0, -68($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -64($fp)
	#          IF local_15 GOTO label_77 ;
	lw         $t0, -64($fp)
	bnez       $t0, label_77
	#          c = var ;
	lw         $t0, 0($fp)
	sw         $t0, -76($fp)
	#          local_19 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -80($fp)
	#          local_20 = LOAD data_43 ;
	la         $t0, data_43
	sw         $t0, -84($fp)
	#          local_21 = VCALL local_19 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_20 ;
	lw         $t0, -84($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -80($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -88($fp)
	#          LABEL label_77 ;
	label_77:

	#          local_24 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -100($fp)
	#          local_23 = local_0 == local_24 ;
	lw         $t0, -4($fp)
	lw         $t1, -100($fp)
	li         $v0, 1
	sw         $v0, -96($fp)
	equal_loop_16:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_16
	beqz       $t2, end_loop_16
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_16
	b          end_loop_16
	not_equal_16:

	li         $v0, 0
	sw         $v0, -96($fp)
	end_loop_16:

	#          local_22 = local_23 == 0 ;
	lw         $t0, -96($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -92($fp)
	#          IF local_22 GOTO label_78 ;
	lw         $t0, -92($fp)
	bnez       $t0, label_78
	#          d = var ;
	lw         $t0, 0($fp)
	sw         $t0, -104($fp)
	#          local_26 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -108($fp)
	#          local_27 = LOAD data_44 ;
	la         $t0, data_44
	sw         $t0, -112($fp)
	#          local_28 = VCALL local_26 out_string ;
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
	lw         $t0, -108($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -116($fp)
	#          LABEL label_78 ;
	label_78:

	#          local_31 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -128($fp)
	#          local_30 = local_0 == local_31 ;
	lw         $t0, -4($fp)
	lw         $t1, -128($fp)
	li         $v0, 1
	sw         $v0, -124($fp)
	equal_loop_17:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_17
	beqz       $t2, end_loop_17
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_17
	b          end_loop_17
	not_equal_17:

	li         $v0, 0
	sw         $v0, -124($fp)
	end_loop_17:

	#          local_29 = local_30 == 0 ;
	lw         $t0, -124($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -120($fp)
	#          IF local_29 GOTO label_79 ;
	lw         $t0, -120($fp)
	bnez       $t0, label_79
	#          e = var ;
	lw         $t0, 0($fp)
	sw         $t0, -132($fp)
	#          local_33 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -136($fp)
	#          local_34 = LOAD data_45 ;
	la         $t0, data_45
	sw         $t0, -140($fp)
	#          local_35 = VCALL local_33 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_34 ;
	lw         $t0, -140($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -136($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -144($fp)
	#          LABEL label_79 ;
	label_79:

	#          local_38 = LOAD data_46 ;
	la         $t0, data_46
	sw         $t0, -156($fp)
	#          local_37 = local_0 == local_38 ;
	lw         $t0, -4($fp)
	lw         $t1, -156($fp)
	li         $v0, 1
	sw         $v0, -152($fp)
	equal_loop_18:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_18
	beqz       $t2, end_loop_18
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_18
	b          end_loop_18
	not_equal_18:

	li         $v0, 0
	sw         $v0, -152($fp)
	end_loop_18:

	#          local_36 = local_37 == 0 ;
	lw         $t0, -152($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -148($fp)
	#          IF local_36 GOTO label_80 ;
	lw         $t0, -148($fp)
	bnez       $t0, label_80
	#          o = var ;
	lw         $t0, 0($fp)
	sw         $t0, -160($fp)
	#          local_40 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -164($fp)
	#          local_41 = LOAD data_47 ;
	la         $t0, data_47
	sw         $t0, -168($fp)
	#          local_42 = VCALL local_40 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_41 ;
	lw         $t0, -168($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -164($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -172($fp)
	#          LABEL label_80 ;
	label_80:

	#          RETURN local_42 ;
	lw         $v0, -172($fp)
	addu       $sp, $sp, 172
	jr         $ra
Main_print:
	move       $fp, $sp
	subu       $sp, $sp, 48
	#          local_0 = ALLOCATE A2I ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	la         $t0, vt_A2I
	sw         $t0, 8($v0)
	#          local_1 = VCALL A2I __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A2I___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          z = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -12($fp)
	#          local_3 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_4 = GETTYPEADDR z ;
	lw         $t1, -12($fp)
	lw         $t0, 8($t1)
	sw         $t0, -20($fp)
	#          local_5 = GETTYPEADDR var ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -24($fp)
	#          local_6 = VCALL local_5 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG var ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -24($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -28($fp)
	#          local_7 = VCALL local_4 i2a ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG z ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_6 ;
	lw         $t0, -28($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -20($fp)
	ulw        $t1, 96($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          local_8 = VCALL local_3 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          local_9 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -40($fp)
	#          local_10 = LOAD data_48 ;
	la         $t0, data_48
	sw         $t0, -44($fp)
	#          local_11 = VCALL local_9 out_string ;
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
	lw         $t0, -40($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          RETURN local_11 ;
	lw         $v0, -48($fp)
	addu       $sp, $sp, 48
	jr         $ra
Main_main:
	move       $fp, $sp
	subu       $sp, $sp, 912
	#          local_0 = ALLOCATE A ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	la         $t0, vt_A
	sw         $t0, 8($v0)
	#          local_1 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          SETATTR self avar local_0 ;
	lw         $t0, -4($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          LABEL label_108 ;
	label_108:

	#          local_2 = GETATTR self flag ;
	lw         $t0, 0($fp)
	lw         $t1, 24($t0)
	sw         $t1, -12($fp)
	#          IF local_2 GOTO label_109 ;
	lw         $t0, -12($fp)
	bnez       $t0, label_109
	#          GOTO label_110 ;
	b          label_110
	#          LABEL label_109 ;
	label_109:

	#          local_3 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_4 = LOAD data_49 ;
	la         $t0, data_49
	sw         $t0, -20($fp)
	#          local_5 = VCALL local_3 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
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
	#          local_6 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_7 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -32($fp)
	#          local_8 = VCALL local_6 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          local_9 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -40($fp)
	#          local_11 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -48($fp)
	#          local_10 = GETTYPEADDR local_11 ;
	lw         $t1, -48($fp)
	lw         $t0, 8($t1)
	sw         $t0, -44($fp)
	#          local_12 = VCALL local_10 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_11 ;
	lw         $t0, -48($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -44($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          local_13 = VCALL local_9 is_even ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_12 ;
	lw         $t0, -52($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -40($fp)
	ulw        $t1, 116($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -56($fp)
	#          IF local_13 GOTO label_81 ;
	lw         $t0, -56($fp)
	bnez       $t0, label_81
	#          local_17 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -72($fp)
	#          local_18 = LOAD data_51 ;
	la         $t0, data_51
	sw         $t0, -76($fp)
	#          local_19 = VCALL local_17 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
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
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -80($fp)
	#          local_20 = local_19 ;
	lw         $t0, -80($fp)
	sw         $t0, -84($fp)
	#          GOTO label_82 ;
	b          label_82
	#          LABEL label_81 ;
	label_81:

	#          local_14 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -60($fp)
	#          local_15 = LOAD data_50 ;
	la         $t0, data_50
	sw         $t0, -64($fp)
	#          local_16 = VCALL local_14 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
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
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -68($fp)
	#          local_20 = local_16 ;
	lw         $t0, -68($fp)
	sw         $t0, -84($fp)
	#          LABEL label_82 ;
	label_82:

	#          local_21 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -88($fp)
	#          local_22 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -92($fp)
	#          local_23 = VCALL local_21 class_type ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_22 ;
	lw         $t0, -92($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -88($fp)
	ulw        $t1, 120($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -96($fp)
	#          local_24 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -100($fp)
	#          local_25 = VCALL local_24 menu ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -100($fp)
	ulw        $t1, 104($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -104($fp)
	#          SETATTR self char local_25 ;
	lw         $t0, -104($fp)
	lw         $t1, 0($fp)
	sw         $t0, 12($t1)
	#          local_26 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -108($fp)
	#          local_27 = LOAD data_52 ;
	la         $t0, data_52
	sw         $t0, -112($fp)
	#          local_28 = local_26 == local_27 ;
	lw         $t0, -108($fp)
	lw         $t1, -112($fp)
	li         $v0, 1
	sw         $v0, -116($fp)
	equal_loop_19:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_19
	beqz       $t2, end_loop_19
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_19
	b          end_loop_19
	not_equal_19:

	li         $v0, 0
	sw         $v0, -116($fp)
	end_loop_19:

	#          local_29 = local_28 ;
	lw         $t0, -116($fp)
	sw         $t0, -120($fp)
	#          IF local_29 GOTO label_106 ;
	lw         $t0, -120($fp)
	bnez       $t0, label_106
	#          local_46 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -188($fp)
	#          local_47 = LOAD data_53 ;
	la         $t0, data_53
	sw         $t0, -192($fp)
	#          local_48 = local_46 == local_47 ;
	lw         $t0, -188($fp)
	lw         $t1, -192($fp)
	li         $v0, 1
	sw         $v0, -196($fp)
	equal_loop_20:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_20
	beqz       $t2, end_loop_20
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_20
	b          end_loop_20
	not_equal_20:

	li         $v0, 0
	sw         $v0, -196($fp)
	end_loop_20:

	#          local_49 = local_48 ;
	lw         $t0, -196($fp)
	sw         $t0, -200($fp)
	#          IF local_49 GOTO label_104 ;
	lw         $t0, -200($fp)
	bnez       $t0, label_104
	#          local_77 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -312($fp)
	#          local_78 = LOAD data_54 ;
	la         $t0, data_54
	sw         $t0, -316($fp)
	#          local_79 = local_77 == local_78 ;
	lw         $t0, -312($fp)
	lw         $t1, -316($fp)
	li         $v0, 1
	sw         $v0, -320($fp)
	equal_loop_21:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_21
	beqz       $t2, end_loop_21
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_21
	b          end_loop_21
	not_equal_21:

	li         $v0, 0
	sw         $v0, -320($fp)
	end_loop_21:

	#          local_80 = local_79 ;
	lw         $t0, -320($fp)
	sw         $t0, -324($fp)
	#          IF local_80 GOTO label_102 ;
	lw         $t0, -324($fp)
	bnez       $t0, label_102
	#          local_97 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -392($fp)
	#          local_98 = LOAD data_55 ;
	la         $t0, data_55
	sw         $t0, -396($fp)
	#          local_99 = local_97 == local_98 ;
	lw         $t0, -392($fp)
	lw         $t1, -396($fp)
	li         $v0, 1
	sw         $v0, -400($fp)
	equal_loop_22:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_22
	beqz       $t2, end_loop_22
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_22
	b          end_loop_22
	not_equal_22:

	li         $v0, 0
	sw         $v0, -400($fp)
	end_loop_22:

	#          local_100 = local_99 ;
	lw         $t0, -400($fp)
	sw         $t0, -404($fp)
	#          IF local_100 GOTO label_100 ;
	lw         $t0, -404($fp)
	bnez       $t0, label_100
	#          local_108 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -436($fp)
	#          local_109 = LOAD data_56 ;
	la         $t0, data_56
	sw         $t0, -440($fp)
	#          local_110 = local_108 == local_109 ;
	lw         $t0, -436($fp)
	lw         $t1, -440($fp)
	li         $v0, 1
	sw         $v0, -444($fp)
	equal_loop_23:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_23
	beqz       $t2, end_loop_23
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_23
	b          end_loop_23
	not_equal_23:

	li         $v0, 0
	sw         $v0, -444($fp)
	end_loop_23:

	#          local_111 = local_110 ;
	lw         $t0, -444($fp)
	sw         $t0, -448($fp)
	#          IF local_111 GOTO label_98 ;
	lw         $t0, -448($fp)
	bnez       $t0, label_98
	#          local_119 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -480($fp)
	#          local_120 = LOAD data_57 ;
	la         $t0, data_57
	sw         $t0, -484($fp)
	#          local_121 = local_119 == local_120 ;
	lw         $t0, -480($fp)
	lw         $t1, -484($fp)
	li         $v0, 1
	sw         $v0, -488($fp)
	equal_loop_24:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_24
	beqz       $t2, end_loop_24
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_24
	b          end_loop_24
	not_equal_24:

	li         $v0, 0
	sw         $v0, -488($fp)
	end_loop_24:

	#          local_122 = local_121 ;
	lw         $t0, -488($fp)
	sw         $t0, -492($fp)
	#          IF local_122 GOTO label_96 ;
	lw         $t0, -492($fp)
	bnez       $t0, label_96
	#          local_130 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -524($fp)
	#          local_131 = LOAD data_58 ;
	la         $t0, data_58
	sw         $t0, -528($fp)
	#          local_132 = local_130 == local_131 ;
	lw         $t0, -524($fp)
	lw         $t1, -528($fp)
	li         $v0, 1
	sw         $v0, -532($fp)
	equal_loop_25:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_25
	beqz       $t2, end_loop_25
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_25
	b          end_loop_25
	not_equal_25:

	li         $v0, 0
	sw         $v0, -532($fp)
	end_loop_25:

	#          local_133 = local_132 ;
	lw         $t0, -532($fp)
	sw         $t0, -536($fp)
	#          IF local_133 GOTO label_94 ;
	lw         $t0, -536($fp)
	bnez       $t0, label_94
	#          local_158 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -636($fp)
	#          local_159 = LOAD data_61 ;
	la         $t0, data_61
	sw         $t0, -640($fp)
	#          local_160 = local_158 == local_159 ;
	lw         $t0, -636($fp)
	lw         $t1, -640($fp)
	li         $v0, 1
	sw         $v0, -644($fp)
	equal_loop_26:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_26
	beqz       $t2, end_loop_26
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_26
	b          end_loop_26
	not_equal_26:

	li         $v0, 0
	sw         $v0, -644($fp)
	end_loop_26:

	#          local_161 = local_160 ;
	lw         $t0, -644($fp)
	sw         $t0, -648($fp)
	#          IF local_161 GOTO label_92 ;
	lw         $t0, -648($fp)
	bnez       $t0, label_92
	#          local_200 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -804($fp)
	#          local_201 = LOAD data_64 ;
	la         $t0, data_64
	sw         $t0, -808($fp)
	#          local_202 = local_200 == local_201 ;
	lw         $t0, -804($fp)
	lw         $t1, -808($fp)
	li         $v0, 1
	sw         $v0, -812($fp)
	equal_loop_27:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_27
	beqz       $t2, end_loop_27
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_27
	b          end_loop_27
	not_equal_27:

	li         $v0, 0
	sw         $v0, -812($fp)
	end_loop_27:

	#          local_203 = local_202 ;
	lw         $t0, -812($fp)
	sw         $t0, -816($fp)
	#          IF local_203 GOTO label_90 ;
	lw         $t0, -816($fp)
	bnez       $t0, label_90
	#          local_206 = GETATTR self char ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -828($fp)
	#          local_207 = LOAD data_65 ;
	la         $t0, data_65
	sw         $t0, -832($fp)
	#          local_208 = local_206 == local_207 ;
	lw         $t0, -828($fp)
	lw         $t1, -832($fp)
	li         $v0, 1
	sw         $v0, -836($fp)
	equal_loop_28:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_28
	beqz       $t2, end_loop_28
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_28
	b          end_loop_28
	not_equal_28:

	li         $v0, 0
	sw         $v0, -836($fp)
	end_loop_28:

	#          local_209 = local_208 ;
	lw         $t0, -836($fp)
	sw         $t0, -840($fp)
	#          IF local_209 GOTO label_88 ;
	lw         $t0, -840($fp)
	bnez       $t0, label_88
	#          local_211 = ALLOCATE A ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -848($fp)
	la         $t0, vt_A
	sw         $t0, 8($v0)
	#          local_212 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_211 ;
	lw         $t0, -848($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -852($fp)
	#          local_210 = GETTYPEADDR local_211 ;
	lw         $t1, -848($fp)
	lw         $t0, 8($t1)
	sw         $t0, -844($fp)
	#          local_214 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -860($fp)
	#          local_213 = GETTYPEADDR local_214 ;
	lw         $t1, -860($fp)
	lw         $t0, 8($t1)
	sw         $t0, -856($fp)
	#          local_215 = VCALL local_213 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_214 ;
	lw         $t0, -860($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -856($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -864($fp)
	#          local_216 = VCALL local_210 method1 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_211 ;
	lw         $t0, -848($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_215 ;
	lw         $t0, -864($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -844($fp)
	ulw        $t1, 48($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -868($fp)
	#          SETATTR self avar local_216 ;
	lw         $t0, -868($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_217 = local_216 ;
	lw         $t0, -868($fp)
	sw         $t0, -872($fp)
	#          GOTO label_89 ;
	b          label_89
	#          LABEL label_88 ;
	label_88:

	#          SETATTR self flag 0 ;
	li         $t0, 0
	lw         $t1, 0($fp)
	sw         $t0, 24($t1)
	#          local_217 = 0 ;
	li         $t0, 0
	sw         $t0, -872($fp)
	#          LABEL label_89 ;
	label_89:

	#          local_218 = local_217 ;
	lw         $t0, -872($fp)
	sw         $t0, -876($fp)
	#          GOTO label_91 ;
	b          label_91
	#          LABEL label_90 ;
	label_90:

	#          local_204 = ALLOCATE A ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -820($fp)
	la         $t0, vt_A
	sw         $t0, 8($v0)
	#          local_205 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_204 ;
	lw         $t0, -820($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -824($fp)
	#          SETATTR self avar local_204 ;
	lw         $t0, -820($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_218 = local_204 ;
	lw         $t0, -820($fp)
	sw         $t0, -876($fp)
	#          LABEL label_91 ;
	label_91:

	#          local_219 = local_218 ;
	lw         $t0, -876($fp)
	sw         $t0, -880($fp)
	#          GOTO label_93 ;
	b          label_93
	#          LABEL label_92 ;
	label_92:

	#          local_163 = ALLOCATE E ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -656($fp)
	la         $t0, vt_E
	sw         $t0, 8($v0)
	#          local_164 = VCALL E __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_163 ;
	lw         $t0, -656($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        E___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -660($fp)
	#          local_162 = GETTYPEADDR local_163 ;
	lw         $t1, -656($fp)
	lw         $t0, 8($t1)
	sw         $t0, -652($fp)
	#          local_166 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -668($fp)
	#          local_165 = GETTYPEADDR local_166 ;
	lw         $t1, -668($fp)
	lw         $t0, 8($t1)
	sw         $t0, -664($fp)
	#          local_167 = VCALL local_165 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_166 ;
	lw         $t0, -668($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -664($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -672($fp)
	#          local_168 = VCALL local_162 method6 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_163 ;
	lw         $t0, -656($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_167 ;
	lw         $t0, -672($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -652($fp)
	ulw        $t1, 72($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -676($fp)
	#          x = local_168 ;
	lw         $t0, -676($fp)
	sw         $t0, -680($fp)
	#          local_171 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -688($fp)
	#          local_170 = GETTYPEADDR local_171 ;
	lw         $t1, -688($fp)
	lw         $t0, 8($t1)
	sw         $t0, -684($fp)
	#          local_172 = VCALL local_170 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_171 ;
	lw         $t0, -688($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -684($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -692($fp)
	#          local_173 = GETTYPEADDR x ;
	lw         $t1, -680($fp)
	lw         $t0, 8($t1)
	sw         $t0, -696($fp)
	#          local_174 = VCALL local_173 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG x ;
	lw         $t0, -680($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -696($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -700($fp)
	#          local_175 = local_174 * 8 ;
	lw         $t0, -700($fp)
	li         $t1, 8
	mul        $t0, $t0, $t1
	sw         $t0, -704($fp)
	#          local_176 = local_172 - local_175 ;
	lw         $t0, -692($fp)
	lw         $t1, -704($fp)
	sub        $t0, $t0, $t1
	sw         $t0, -708($fp)
	#          r = local_176 ;
	lw         $t0, -708($fp)
	sw         $t0, -712($fp)
	#          local_178 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -716($fp)
	#          local_179 = VCALL local_178 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -716($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -720($fp)
	#          local_180 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -724($fp)
	#          local_181 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -728($fp)
	#          local_182 = VCALL local_180 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_181 ;
	lw         $t0, -728($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -724($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -732($fp)
	#          local_183 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -736($fp)
	#          local_184 = LOAD data_62 ;
	la         $t0, data_62
	sw         $t0, -740($fp)
	#          local_185 = VCALL local_183 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_184 ;
	lw         $t0, -740($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -736($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -744($fp)
	#          local_186 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -748($fp)
	#          local_187 = VCALL local_186 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG x ;
	lw         $t0, -680($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -748($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -752($fp)
	#          local_188 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -756($fp)
	#          local_189 = LOAD data_63 ;
	la         $t0, data_63
	sw         $t0, -760($fp)
	#          local_190 = VCALL local_188 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_189 ;
	lw         $t0, -760($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -756($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -764($fp)
	#          local_191 = ALLOCATE A2I ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -768($fp)
	la         $t0, vt_A2I
	sw         $t0, 8($v0)
	#          local_192 = VCALL A2I __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_191 ;
	lw         $t0, -768($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A2I___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -772($fp)
	#          a = local_191 ;
	lw         $t0, -768($fp)
	sw         $t0, -256($fp)
	#          local_193 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -776($fp)
	#          local_194 = GETTYPEADDR a ;
	lw         $t1, -256($fp)
	lw         $t0, 8($t1)
	sw         $t0, -780($fp)
	#          local_195 = VCALL local_194 i2a ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG a ;
	lw         $t0, -256($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG r ;
	lw         $t0, -712($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -780($fp)
	ulw        $t1, 96($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -784($fp)
	#          local_196 = VCALL local_193 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_195 ;
	lw         $t0, -784($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -776($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -788($fp)
	#          local_197 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -792($fp)
	#          local_198 = LOAD data_39 ;
	la         $t0, data_39
	sw         $t0, -796($fp)
	#          local_199 = VCALL local_197 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_198 ;
	lw         $t0, -796($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -792($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -800($fp)
	#          SETATTR self avar x ;
	lw         $t0, -680($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_219 = x ;
	lw         $t0, -680($fp)
	sw         $t0, -880($fp)
	#          LABEL label_93 ;
	label_93:

	#          local_220 = local_219 ;
	lw         $t0, -880($fp)
	sw         $t0, -884($fp)
	#          GOTO label_95 ;
	b          label_95
	#          LABEL label_94 ;
	label_94:

	#          local_135 = ALLOCATE D ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -544($fp)
	la         $t0, vt_D
	sw         $t0, 8($v0)
	#          local_136 = VCALL D __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_135 ;
	lw         $t0, -544($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        D___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -548($fp)
	#          local_134 = GETTYPEADDR local_135 ;
	lw         $t1, -544($fp)
	lw         $t0, 8($t1)
	sw         $t0, -540($fp)
	#          local_138 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -556($fp)
	#          local_137 = GETTYPEADDR local_138 ;
	lw         $t1, -556($fp)
	lw         $t0, 8($t1)
	sw         $t0, -552($fp)
	#          local_139 = VCALL local_137 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_138 ;
	lw         $t0, -556($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -552($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -560($fp)
	#          local_140 = VCALL local_134 method7 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_135 ;
	lw         $t0, -544($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_139 ;
	lw         $t0, -560($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -540($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -564($fp)
	#          IF local_140 GOTO label_86 ;
	lw         $t0, -564($fp)
	bnez       $t0, label_86
	#          local_149 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -600($fp)
	#          local_150 = VCALL local_149 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -600($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -604($fp)
	#          local_151 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -608($fp)
	#          local_152 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -612($fp)
	#          local_153 = VCALL local_151 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_152 ;
	lw         $t0, -612($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -608($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -616($fp)
	#          local_154 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -620($fp)
	#          local_155 = LOAD data_60 ;
	la         $t0, data_60
	sw         $t0, -624($fp)
	#          local_156 = VCALL local_154 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_155 ;
	lw         $t0, -624($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -620($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -628($fp)
	#          local_157 = local_156 ;
	lw         $t0, -628($fp)
	sw         $t0, -632($fp)
	#          GOTO label_87 ;
	b          label_87
	#          LABEL label_86 ;
	label_86:

	#          local_141 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -568($fp)
	#          local_142 = VCALL local_141 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -568($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -572($fp)
	#          local_143 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -576($fp)
	#          local_144 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -580($fp)
	#          local_145 = VCALL local_143 print ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_144 ;
	lw         $t0, -580($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -576($fp)
	ulw        $t1, 124($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -584($fp)
	#          local_146 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -588($fp)
	#          local_147 = LOAD data_59 ;
	la         $t0, data_59
	sw         $t0, -592($fp)
	#          local_148 = VCALL local_146 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_147 ;
	lw         $t0, -592($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -588($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -596($fp)
	#          local_157 = local_148 ;
	lw         $t0, -596($fp)
	sw         $t0, -632($fp)
	#          LABEL label_87 ;
	label_87:

	#          local_220 = local_157 ;
	lw         $t0, -632($fp)
	sw         $t0, -884($fp)
	#          LABEL label_95 ;
	label_95:

	#          local_221 = local_220 ;
	lw         $t0, -884($fp)
	sw         $t0, -888($fp)
	#          GOTO label_97 ;
	b          label_97
	#          LABEL label_96 ;
	label_96:

	#          local_124 = ALLOCATE C ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -500($fp)
	la         $t0, vt_C
	sw         $t0, 8($v0)
	#          local_125 = VCALL C __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_124 ;
	lw         $t0, -500($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        C___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -504($fp)
	#          local_123 = GETTYPEADDR local_124 ;
	lw         $t1, -500($fp)
	lw         $t0, 8($t1)
	sw         $t0, -496($fp)
	#          local_127 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -512($fp)
	#          local_126 = GETTYPEADDR local_127 ;
	lw         $t1, -512($fp)
	lw         $t0, 8($t1)
	sw         $t0, -508($fp)
	#          local_128 = VCALL local_126 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_127 ;
	lw         $t0, -512($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -508($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -516($fp)
	#          local_129 = VCALL C method5 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_124 ;
	lw         $t0, -500($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_128 ;
	lw         $t0, -516($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        C_method5
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -520($fp)
	#          SETATTR self avar local_129 ;
	lw         $t0, -520($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_221 = local_129 ;
	lw         $t0, -520($fp)
	sw         $t0, -888($fp)
	#          LABEL label_97 ;
	label_97:

	#          local_222 = local_221 ;
	lw         $t0, -888($fp)
	sw         $t0, -892($fp)
	#          GOTO label_99 ;
	b          label_99
	#          LABEL label_98 ;
	label_98:

	#          local_113 = ALLOCATE C ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -456($fp)
	la         $t0, vt_C
	sw         $t0, 8($v0)
	#          local_114 = VCALL C __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_113 ;
	lw         $t0, -456($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        C___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -460($fp)
	#          local_112 = GETTYPEADDR local_113 ;
	lw         $t1, -456($fp)
	lw         $t0, 8($t1)
	sw         $t0, -452($fp)
	#          local_116 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -468($fp)
	#          local_115 = GETTYPEADDR local_116 ;
	lw         $t1, -468($fp)
	lw         $t0, 8($t1)
	sw         $t0, -464($fp)
	#          local_117 = VCALL local_115 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_116 ;
	lw         $t0, -468($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -464($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -472($fp)
	#          local_118 = VCALL B method5 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_113 ;
	lw         $t0, -456($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_117 ;
	lw         $t0, -472($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        B_method5
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -476($fp)
	#          SETATTR self avar local_118 ;
	lw         $t0, -476($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_222 = local_118 ;
	lw         $t0, -476($fp)
	sw         $t0, -892($fp)
	#          LABEL label_99 ;
	label_99:

	#          local_223 = local_222 ;
	lw         $t0, -892($fp)
	sw         $t0, -896($fp)
	#          GOTO label_101 ;
	b          label_101
	#          LABEL label_100 ;
	label_100:

	#          local_102 = ALLOCATE C ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -412($fp)
	la         $t0, vt_C
	sw         $t0, 8($v0)
	#          local_103 = VCALL C __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_102 ;
	lw         $t0, -412($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        C___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -416($fp)
	#          local_101 = GETTYPEADDR local_102 ;
	lw         $t1, -412($fp)
	lw         $t0, 8($t1)
	sw         $t0, -408($fp)
	#          local_105 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -424($fp)
	#          local_104 = GETTYPEADDR local_105 ;
	lw         $t1, -424($fp)
	lw         $t0, 8($t1)
	sw         $t0, -420($fp)
	#          local_106 = VCALL local_104 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_105 ;
	lw         $t0, -424($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -420($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -428($fp)
	#          local_107 = VCALL A method5 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_102 ;
	lw         $t0, -412($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_106 ;
	lw         $t0, -428($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A_method5
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -432($fp)
	#          SETATTR self avar local_107 ;
	lw         $t0, -432($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_223 = local_107 ;
	lw         $t0, -432($fp)
	sw         $t0, -896($fp)
	#          LABEL label_101 ;
	label_101:

	#          local_224 = local_223 ;
	lw         $t0, -896($fp)
	sw         $t0, -900($fp)
	#          GOTO label_103 ;
	b          label_103
	#          LABEL label_102 ;
	label_102:

	#          local_82 = ALLOCATE A ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -332($fp)
	la         $t0, vt_A
	sw         $t0, 8($v0)
	#          local_83 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_82 ;
	lw         $t0, -332($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -336($fp)
	#          local_81 = GETTYPEADDR local_82 ;
	lw         $t1, -332($fp)
	lw         $t0, 8($t1)
	sw         $t0, -328($fp)
	#          local_84 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -340($fp)
	#          local_85 = VCALL local_84 get_int ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -340($fp)
	ulw        $t1, 112($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -344($fp)
	#          local_86 = VCALL local_81 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_82 ;
	lw         $t0, -332($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_85 ;
	lw         $t0, -344($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -328($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -348($fp)
	#          SETATTR self a_var local_86 ;
	lw         $t0, -348($fp)
	lw         $t1, 0($fp)
	sw         $t0, 20($t1)
	#          local_88 = ALLOCATE D ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -356($fp)
	la         $t0, vt_D
	sw         $t0, 8($v0)
	#          local_89 = VCALL D __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_88 ;
	lw         $t0, -356($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        D___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -360($fp)
	#          local_87 = GETTYPEADDR local_88 ;
	lw         $t1, -356($fp)
	lw         $t0, 8($t1)
	sw         $t0, -352($fp)
	#          local_91 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -368($fp)
	#          local_90 = GETTYPEADDR local_91 ;
	lw         $t1, -368($fp)
	lw         $t0, 8($t1)
	sw         $t0, -364($fp)
	#          local_92 = VCALL local_90 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_91 ;
	lw         $t0, -368($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -364($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -372($fp)
	#          local_94 = GETATTR self a_var ;
	lw         $t0, 0($fp)
	lw         $t1, 20($t0)
	sw         $t1, -380($fp)
	#          local_93 = GETTYPEADDR local_94 ;
	lw         $t1, -380($fp)
	lw         $t0, 8($t1)
	sw         $t0, -376($fp)
	#          local_95 = VCALL local_93 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_94 ;
	lw         $t0, -380($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -376($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -384($fp)
	#          local_96 = VCALL local_87 method4 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_88 ;
	lw         $t0, -356($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_92 ;
	lw         $t0, -372($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_95 ;
	lw         $t0, -384($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -352($fp)
	ulw        $t1, 60($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -388($fp)
	#          SETATTR self avar local_96 ;
	lw         $t0, -388($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_224 = local_96 ;
	lw         $t0, -388($fp)
	sw         $t0, -900($fp)
	#          LABEL label_103 ;
	label_103:

	#          local_225 = local_224 ;
	lw         $t0, -900($fp)
	sw         $t0, -904($fp)
	#          GOTO label_105 ;
	b          label_105
	#          LABEL label_104 ;
	label_104:

	#          local_50 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -204($fp)
	#          local_51 = TYPEOF local_50 ;
	lw         $t0, -204($fp)
	lw         $t1, ($t0)
	sw         $t1, -208($fp)
	#          local_54 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -220($fp)
	#          local_53 = local_51 == local_54 ;
	lw         $t0, -208($fp)
	lw         $t1, -220($fp)
	li         $v0, 1
	sw         $v0, -216($fp)
	equal_loop_29:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_29
	beqz       $t2, end_loop_29
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_29
	b          end_loop_29
	not_equal_29:

	li         $v0, 0
	sw         $v0, -216($fp)
	end_loop_29:

	#          local_52 = local_53 == 0 ;
	lw         $t0, -216($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -212($fp)
	#          IF local_52 GOTO label_83 ;
	lw         $t0, -212($fp)
	bnez       $t0, label_83
	#          c = local_50 ;
	lw         $t0, -204($fp)
	sw         $t0, -224($fp)
	#          local_56 = GETTYPEADDR c ;
	lw         $t1, -224($fp)
	lw         $t0, 8($t1)
	sw         $t0, -228($fp)
	#          local_57 = GETTYPEADDR c ;
	lw         $t1, -224($fp)
	lw         $t0, 8($t1)
	sw         $t0, -232($fp)
	#          local_58 = VCALL local_57 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG c ;
	lw         $t0, -224($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -232($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -236($fp)
	#          local_59 = VCALL local_56 method6 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG c ;
	lw         $t0, -224($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_58 ;
	lw         $t0, -236($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -228($fp)
	ulw        $t1, 72($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -240($fp)
	#          SETATTR self avar local_59 ;
	lw         $t0, -240($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          LABEL label_83 ;
	label_83:

	#          local_62 = LOAD data_1 ;
	la         $t0, data_1
	sw         $t0, -252($fp)
	#          local_61 = local_51 == local_62 ;
	lw         $t0, -208($fp)
	lw         $t1, -252($fp)
	li         $v0, 1
	sw         $v0, -248($fp)
	equal_loop_30:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_30
	beqz       $t2, end_loop_30
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_30
	b          end_loop_30
	not_equal_30:

	li         $v0, 0
	sw         $v0, -248($fp)
	end_loop_30:

	#          local_60 = local_61 == 0 ;
	lw         $t0, -248($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -244($fp)
	#          IF local_60 GOTO label_84 ;
	lw         $t0, -244($fp)
	bnez       $t0, label_84
	#          a = local_50 ;
	lw         $t0, -204($fp)
	sw         $t0, -256($fp)
	#          local_64 = GETTYPEADDR a ;
	lw         $t1, -256($fp)
	lw         $t0, 8($t1)
	sw         $t0, -260($fp)
	#          local_65 = GETTYPEADDR a ;
	lw         $t1, -256($fp)
	lw         $t0, 8($t1)
	sw         $t0, -264($fp)
	#          local_66 = VCALL local_65 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG a ;
	lw         $t0, -256($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -264($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -268($fp)
	#          local_67 = VCALL local_64 method3 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG a ;
	lw         $t0, -256($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_66 ;
	lw         $t0, -268($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -260($fp)
	ulw        $t1, 56($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -272($fp)
	#          SETATTR self avar local_67 ;
	lw         $t0, -272($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          LABEL label_84 ;
	label_84:

	#          local_70 = LOAD data_46 ;
	la         $t0, data_46
	sw         $t0, -284($fp)
	#          local_69 = local_51 == local_70 ;
	lw         $t0, -208($fp)
	lw         $t1, -284($fp)
	li         $v0, 1
	sw         $v0, -280($fp)
	equal_loop_31:

	lb         $t2, ($t0)
	lb         $t3, ($t1)
	seq        $t4, $t2, $t3
	beqz       $t4, not_equal_31
	beqz       $t2, end_loop_31
	addu       $t0, $t0, 1
	addu       $t1, $t1, 1
	b          equal_loop_31
	b          end_loop_31
	not_equal_31:

	li         $v0, 0
	sw         $v0, -280($fp)
	end_loop_31:

	#          local_68 = local_69 == 0 ;
	lw         $t0, -280($fp)
	li         $t1, 0
	seq        $t0, $t0, $t1
	sw         $t0, -276($fp)
	#          IF local_68 GOTO label_85 ;
	lw         $t0, -276($fp)
	bnez       $t0, label_85
	#          o = local_50 ;
	lw         $t0, -204($fp)
	sw         $t0, -288($fp)
	#          local_72 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -292($fp)
	#          local_73 = LOAD data_47 ;
	la         $t0, data_47
	sw         $t0, -296($fp)
	#          local_74 = VCALL local_72 out_string ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_73 ;
	lw         $t0, -296($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -292($fp)
	ulw        $t1, 12($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -300($fp)
	#          local_75 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -304($fp)
	#          local_76 = VCALL local_75 abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -304($fp)
	ulw        $t1, 0($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -308($fp)
	#          LABEL label_85 ;
	label_85:

	#          local_225 = 0 ;
	li         $t0, 0
	sw         $t0, -904($fp)
	#          LABEL label_105 ;
	label_105:

	#          local_226 = local_225 ;
	lw         $t0, -904($fp)
	sw         $t0, -908($fp)
	#          GOTO label_107 ;
	b          label_107
	#          LABEL label_106 ;
	label_106:

	#          local_31 = ALLOCATE A ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -128($fp)
	la         $t0, vt_A
	sw         $t0, 8($v0)
	#          local_32 = VCALL A __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_31 ;
	lw         $t0, -128($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        A___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -132($fp)
	#          local_30 = GETTYPEADDR local_31 ;
	lw         $t1, -128($fp)
	lw         $t0, 8($t1)
	sw         $t0, -124($fp)
	#          local_33 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -136($fp)
	#          local_34 = VCALL local_33 get_int ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -136($fp)
	ulw        $t1, 112($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -140($fp)
	#          local_35 = VCALL local_30 set_var ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_31 ;
	lw         $t0, -128($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_34 ;
	lw         $t0, -140($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -124($fp)
	ulw        $t1, 44($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -144($fp)
	#          SETATTR self a_var local_35 ;
	lw         $t0, -144($fp)
	lw         $t1, 0($fp)
	sw         $t0, 20($t1)
	#          local_37 = ALLOCATE B ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -152($fp)
	la         $t0, vt_B
	sw         $t0, 8($v0)
	#          local_38 = VCALL B __init__ ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_37 ;
	lw         $t0, -152($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	jal        B___init__
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -156($fp)
	#          local_36 = GETTYPEADDR local_37 ;
	lw         $t1, -152($fp)
	lw         $t0, 8($t1)
	sw         $t0, -148($fp)
	#          local_40 = GETATTR self avar ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -164($fp)
	#          local_39 = GETTYPEADDR local_40 ;
	lw         $t1, -164($fp)
	lw         $t0, 8($t1)
	sw         $t0, -160($fp)
	#          local_41 = VCALL local_39 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_40 ;
	lw         $t0, -164($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -160($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -168($fp)
	#          local_43 = GETATTR self a_var ;
	lw         $t0, 0($fp)
	lw         $t1, 20($t0)
	sw         $t1, -176($fp)
	#          local_42 = GETTYPEADDR local_43 ;
	lw         $t1, -176($fp)
	lw         $t0, 8($t1)
	sw         $t0, -172($fp)
	#          local_44 = VCALL local_42 value ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_43 ;
	lw         $t0, -176($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -172($fp)
	ulw        $t1, 40($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -180($fp)
	#          local_45 = VCALL local_36 method2 ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_37 ;
	lw         $t0, -152($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_41 ;
	lw         $t0, -168($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_44 ;
	lw         $t0, -180($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -148($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -184($fp)
	#          SETATTR self avar local_45 ;
	lw         $t0, -184($fp)
	lw         $t1, 0($fp)
	sw         $t0, 16($t1)
	#          local_226 = local_45 ;
	lw         $t0, -184($fp)
	sw         $t0, -908($fp)
	#          LABEL label_107 ;
	label_107:

	#          GOTO label_108 ;
	b          label_108
	#          LABEL label_110 ;
	label_110:

	#          local_227 = 0 ;
	li         $t0, 0
	sw         $t0, -912($fp)
	#          RETURN local_227 ;
	lw         $v0, -912($fp)
	addu       $sp, $sp, 912
	jr         $ra

.data
	data_1:
		.asciiz    "A"
	data_2:
		.asciiz    "B"
	data_3:
		.asciiz    "C"
	data_4:
		.asciiz    "D"
	data_5:
		.asciiz    "E"
	data_6:
		.asciiz    "A2I"
	data_7:
		.asciiz    "0"
	data_8:
		.asciiz    "1"
	data_9:
		.asciiz    "2"
	data_10:
		.asciiz    "3"
	data_11:
		.asciiz    "4"
	data_12:
		.asciiz    "5"
	data_13:
		.asciiz    "6"
	data_14:
		.asciiz    "7"
	data_15:
		.asciiz    "8"
	data_16:
		.asciiz    "9"
	data_17:
		.asciiz    ""
	data_18:
		.asciiz    "-"
	data_19:
		.asciiz    "+"
	data_20:
		.asciiz    "Main"
	data_21:
		.asciiz    "\n\tTo add a number to "
	data_22:
		.asciiz    "...enter a:\n"
	data_23:
		.asciiz    "\tTo negate "
	data_24:
		.asciiz    "...enter b:\n"
	data_25:
		.asciiz    "\tTo find the difference between "
	data_26:
		.asciiz    "and another number...enter c:\n"
	data_27:
		.asciiz    "\tTo find the factorial of "
	data_28:
		.asciiz    "...enter d:\n"
	data_29:
		.asciiz    "\tTo square "
	data_30:
		.asciiz    "...enter e:\n"
	data_31:
		.asciiz    "\tTo cube "
	data_32:
		.asciiz    "...enter f:\n"
	data_33:
		.asciiz    "\tTo find out if "
	data_34:
		.asciiz    "is a multiple of 3...enter g:\n"
	data_35:
		.asciiz    "\tTo divide "
	data_36:
		.asciiz    "by 8...enter h:\n"
	data_37:
		.asciiz    "\tTo get a new number...enter j:\n"
	data_38:
		.asciiz    "\tTo quit...enter q:\n\n"
	data_39:
		.asciiz    "\n"
	data_40:
		.asciiz    "Please enter a number...  "
	data_41:
		.asciiz    "Class type is now A\n"
	data_42:
		.asciiz    "Class type is now B\n"
	data_43:
		.asciiz    "Class type is now C\n"
	data_44:
		.asciiz    "Class type is now D\n"
	data_45:
		.asciiz    "Class type is now E\n"
	data_46:
		.asciiz    "Object"
	data_47:
		.asciiz    "Oooops\n"
	data_48:
		.asciiz    " "
	data_49:
		.asciiz    "number "
	data_50:
		.asciiz    "is even!\n"
	data_51:
		.asciiz    "is odd!\n"
	data_52:
		.asciiz    "a"
	data_53:
		.asciiz    "b"
	data_54:
		.asciiz    "c"
	data_55:
		.asciiz    "d"
	data_56:
		.asciiz    "e"
	data_57:
		.asciiz    "f"
	data_58:
		.asciiz    "g"
	data_59:
		.asciiz    "is divisible by 3.\n"
	data_60:
		.asciiz    "is not divisible by 3.\n"
	data_61:
		.asciiz    "h"
	data_62:
		.asciiz    "is equal to "
	data_63:
		.asciiz    "times 8 with a remainder of "
	data_64:
		.asciiz    "j"
	data_65:
		.asciiz    "q"
	data_66:
		.asciiz    "Bool"
	data_67:
		.asciiz    "Int"
	data_68:
		.asciiz    "String"
	data_abort:
		.asciiz    "Abort called from class "
	new_line:
		.asciiz    "\n"
	concat_result:
		.space     4096
	substring_result:
		.space     5120
	read_result:
		.space     2048
	vt_Object:
		.space     476
	vt_IO:
		.space     476
	vt_Int:
		.space     476
	vt_String:
		.space     476
	vt_Bool:
		.space     476
	vt_A:
		.space     476
	vt_B:
		.space     476
	vt_C:
		.space     476
	vt_D:
		.space     476
	vt_E:
		.space     476
	vt_A2I:
		.space     476
	vt_Main:
		.space     476
	abort_String:
		.asciiz    "String"
	abort_Int:
		.asciiz    "Int"
	abort_Bool:
		.asciiz    "Bool"
