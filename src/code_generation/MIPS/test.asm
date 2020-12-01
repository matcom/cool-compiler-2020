
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
	usw        $t0, vt_List+0
	la         $t0, Object_type_name
	usw        $t0, vt_List+4
	la         $t0, Object_copy
	usw        $t0, vt_List+8
	la         $t0, IO_out_string
	usw        $t0, vt_List+12
	la         $t0, IO_out_int
	usw        $t0, vt_List+16
	la         $t0, IO_in_string
	usw        $t0, vt_List+20
	la         $t0, IO_in_int
	usw        $t0, vt_List+24
	la         $t0, List_isNil
	usw        $t0, vt_List+40
	la         $t0, List_cons
	usw        $t0, vt_List+44
	la         $t0, List_car
	usw        $t0, vt_List+48
	la         $t0, List_cdr
	usw        $t0, vt_List+52
	la         $t0, List_rev
	usw        $t0, vt_List+56
	la         $t0, List_sort
	usw        $t0, vt_List+60
	la         $t0, List_insert
	usw        $t0, vt_List+64
	la         $t0, List_rcons
	usw        $t0, vt_List+68
	la         $t0, List_print_list
	usw        $t0, vt_List+72
	la         $t0, Object_abort
	usw        $t0, vt_Cons+0
	la         $t0, Object_type_name
	usw        $t0, vt_Cons+4
	la         $t0, Object_copy
	usw        $t0, vt_Cons+8
	la         $t0, IO_out_string
	usw        $t0, vt_Cons+12
	la         $t0, IO_out_int
	usw        $t0, vt_Cons+16
	la         $t0, IO_in_string
	usw        $t0, vt_Cons+20
	la         $t0, IO_in_int
	usw        $t0, vt_Cons+24
	la         $t0, Cons_isNil
	usw        $t0, vt_Cons+40
	la         $t0, List_cons
	usw        $t0, vt_Cons+44
	la         $t0, Cons_car
	usw        $t0, vt_Cons+48
	la         $t0, Cons_cdr
	usw        $t0, vt_Cons+52
	la         $t0, Cons_rev
	usw        $t0, vt_Cons+56
	la         $t0, Cons_sort
	usw        $t0, vt_Cons+60
	la         $t0, Cons_insert
	usw        $t0, vt_Cons+64
	la         $t0, Cons_rcons
	usw        $t0, vt_Cons+68
	la         $t0, Cons_print_list
	usw        $t0, vt_Cons+72
	la         $t0, Cons_init
	usw        $t0, vt_Cons+76
	la         $t0, Object_abort
	usw        $t0, vt_Nil+0
	la         $t0, Object_type_name
	usw        $t0, vt_Nil+4
	la         $t0, Object_copy
	usw        $t0, vt_Nil+8
	la         $t0, IO_out_string
	usw        $t0, vt_Nil+12
	la         $t0, IO_out_int
	usw        $t0, vt_Nil+16
	la         $t0, IO_in_string
	usw        $t0, vt_Nil+20
	la         $t0, IO_in_int
	usw        $t0, vt_Nil+24
	la         $t0, Nil_isNil
	usw        $t0, vt_Nil+40
	la         $t0, List_cons
	usw        $t0, vt_Nil+44
	la         $t0, List_car
	usw        $t0, vt_Nil+48
	la         $t0, List_cdr
	usw        $t0, vt_Nil+52
	la         $t0, Nil_rev
	usw        $t0, vt_Nil+56
	la         $t0, Nil_sort
	usw        $t0, vt_Nil+60
	la         $t0, Nil_insert
	usw        $t0, vt_Nil+64
	la         $t0, Nil_rcons
	usw        $t0, vt_Nil+68
	la         $t0, Nil_print_list
	usw        $t0, vt_Nil+72
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
	la         $t0, Main_iota
	usw        $t0, vt_Main+80
	la         $t0, Main_main
	usw        $t0, vt_Main+84
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
	#          local_13 = LOAD data_8 ;
	la         $t0, data_8
	sw         $t0, -4($fp)
	#          RETURN local_13 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Int_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_14 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -4($fp)
	#          RETURN local_14 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
String_type_name:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_15 = LOAD data_9 ;
	la         $t0, data_9
	sw         $t0, -4($fp)
	#          RETURN local_15 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
List_isNil:
	move       $fp, $sp
	subu       $sp, $sp, 8
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 0($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          RETURN 1 ;
	li         $v0, 1
	addu       $sp, $sp, 8
	jr         $ra
List_cons:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_0 = ALLOCATE Cons ;
	li         $a0, 20
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	la         $t0, vt_Cons
	sw         $t0, 8($v0)
	#          local_1 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 0($t1)
	#          local_2 = 20 ;
	li         $t0, 20
	sw         $t0, -12($fp)
	#          SETATTR local_0 @size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          new_cell = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -16($fp)
	#          local_4 = GETTYPEADDR new_cell ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -20($fp)
	#          local_5 = VCALL local_4 init ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG new_cell ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG hd ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -20($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -24($fp)
	#          RETURN local_5 ;
	lw         $v0, -24($fp)
	addu       $sp, $sp, 24
	jr         $ra
List_car:
	move       $fp, $sp
	subu       $sp, $sp, 20
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 0($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          local_2 = ALLOCATE Int ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -12($fp)
	la         $t0, vt_Int
	sw         $t0, 8($v0)
	#          local_3 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -16($fp)
	#          SETATTR local_2 @type local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, -12($fp)
	sw         $t0, 0($t1)
	#          local_4 = 12 ;
	li         $t0, 12
	sw         $t0, -20($fp)
	#          SETATTR local_2 @size local_4 ;
	lw         $t0, -20($fp)
	lw         $t1, -12($fp)
	sw         $t0, 4($t1)
	#          RETURN local_2 ;
	lw         $v0, -12($fp)
	addu       $sp, $sp, 20
	jr         $ra
List_cdr:
	move       $fp, $sp
	subu       $sp, $sp, 20
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 0($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          local_2 = ALLOCATE List ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -12($fp)
	la         $t0, vt_List
	sw         $t0, 8($v0)
	#          local_3 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -16($fp)
	#          SETATTR local_2 @type local_3 ;
	lw         $t0, -16($fp)
	lw         $t1, -12($fp)
	sw         $t0, 0($t1)
	#          local_4 = 12 ;
	li         $t0, 12
	sw         $t0, -20($fp)
	#          SETATTR local_2 @size local_4 ;
	lw         $t0, -20($fp)
	lw         $t1, -12($fp)
	sw         $t0, 4($t1)
	#          RETURN local_2 ;
	lw         $v0, -12($fp)
	addu       $sp, $sp, 20
	jr         $ra
List_rev:
	move       $fp, $sp
	subu       $sp, $sp, 8
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 cdr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          RETURN local_1 ;
	lw         $v0, -8($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_sort:
	move       $fp, $sp
	subu       $sp, $sp, 8
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 cdr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          RETURN local_1 ;
	lw         $v0, -8($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_insert:
	move       $fp, $sp
	subu       $sp, $sp, 8
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 cdr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          RETURN local_1 ;
	lw         $v0, -8($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_rcons:
	move       $fp, $sp
	subu       $sp, $sp, 8
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 cdr ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 52($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          RETURN local_1 ;
	lw         $v0, -8($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_print_list:
	move       $fp, $sp
	subu       $sp, $sp, 8
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 abort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 0($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          RETURN local_1 ;
	lw         $v0, -8($fp)
	addu       $sp, $sp, 8
	jr         $ra
Cons_isNil:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          RETURN ;
	li         $v0, 0
	addu       $sp, $sp, 0
	jr         $ra
Cons_init:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          SETATTR self xcar hd ;
	lw         $t0, 4($fp)
	lw         $t1, 8($fp)
	sw         $t0, 12($t1)
	#          SETATTR self xcdr tl ;
	lw         $t0, 0($fp)
	lw         $t1, 8($fp)
	sw         $t0, 16($t1)
	#          RETURN self ;
	lw         $v0, 8($fp)
	addu       $sp, $sp, 0
	jr         $ra
Cons_car:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_0 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -4($fp)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Cons_cdr:
	move       $fp, $sp
	subu       $sp, $sp, 4
	#          local_0 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -4($fp)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 4
	jr         $ra
Cons_rev:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_2 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -12($fp)
	#          local_1 = GETTYPEADDR local_2 ;
	lw         $t1, -12($fp)
	lw         $t0, 8($t1)
	sw         $t0, -8($fp)
	#          local_3 = VCALL local_1 rev ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_2 ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -8($fp)
	ulw        $t1, 56($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -16($fp)
	#          local_0 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_4 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -20($fp)
	#          local_5 = VCALL local_0 rcons ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 68($t0)
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
Cons_sort:
	move       $fp, $sp
	subu       $sp, $sp, 24
	#          local_2 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -12($fp)
	#          local_1 = GETTYPEADDR local_2 ;
	lw         $t1, -12($fp)
	lw         $t0, 8($t1)
	sw         $t0, -8($fp)
	#          local_3 = VCALL local_1 sort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_2 ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -8($fp)
	ulw        $t1, 60($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -16($fp)
	#          local_0 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_4 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -20($fp)
	#          local_5 = VCALL local_0 insert ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_4 ;
	lw         $t0, -20($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 64($t0)
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
Cons_insert:
	move       $fp, $sp
	subu       $sp, $sp, 68
	#          local_0 = GETATTR self xcar ;
	lw         $t0, 4($fp)
	lw         $t1, 12($t0)
	sw         $t1, -4($fp)
	#          local_1 = i < local_0 ;
	lw         $t0, 0($fp)
	lw         $t1, -4($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -8($fp)
	#          IF local_1 GOTO label_1 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_1
	#          local_8 = ALLOCATE Cons ;
	li         $a0, 20
	li         $v0, 9
	syscall
	sw         $v0, -36($fp)
	la         $t0, vt_Cons
	sw         $t0, 8($v0)
	#          local_9 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -40($fp)
	#          SETATTR local_8 @type local_9 ;
	lw         $t0, -40($fp)
	lw         $t1, -36($fp)
	sw         $t0, 0($t1)
	#          local_10 = 20 ;
	li         $t0, 20
	sw         $t0, -44($fp)
	#          SETATTR local_8 @size local_10 ;
	lw         $t0, -44($fp)
	lw         $t1, -36($fp)
	sw         $t0, 4($t1)
	#          local_7 = GETTYPEADDR local_8 ;
	lw         $t1, -36($fp)
	lw         $t0, 8($t1)
	sw         $t0, -32($fp)
	#          local_11 = GETATTR self xcar ;
	lw         $t0, 4($fp)
	lw         $t1, 12($t0)
	sw         $t1, -48($fp)
	#          local_13 = GETATTR self xcdr ;
	lw         $t0, 4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -56($fp)
	#          local_12 = GETTYPEADDR local_13 ;
	lw         $t1, -56($fp)
	lw         $t0, 8($t1)
	sw         $t0, -52($fp)
	#          local_14 = VCALL local_12 insert ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_13 ;
	lw         $t0, -56($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -52($fp)
	ulw        $t1, 64($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -60($fp)
	#          local_15 = VCALL local_7 init ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_8 ;
	lw         $t0, -36($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_11 ;
	lw         $t0, -48($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_14 ;
	lw         $t0, -60($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -32($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -64($fp)
	#          local_16 = local_15 ;
	lw         $t0, -64($fp)
	sw         $t0, -68($fp)
	#          GOTO label_2 ;
	b          label_2
	#          LABEL label_1 ;
	label_1:

	#          local_3 = ALLOCATE Cons ;
	li         $a0, 20
	li         $v0, 9
	syscall
	sw         $v0, -16($fp)
	la         $t0, vt_Cons
	sw         $t0, 8($v0)
	#          local_4 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -20($fp)
	#          SETATTR local_3 @type local_4 ;
	lw         $t0, -20($fp)
	lw         $t1, -16($fp)
	sw         $t0, 0($t1)
	#          local_5 = 20 ;
	li         $t0, 20
	sw         $t0, -24($fp)
	#          SETATTR local_3 @size local_5 ;
	lw         $t0, -24($fp)
	lw         $t1, -16($fp)
	sw         $t0, 4($t1)
	#          local_2 = GETTYPEADDR local_3 ;
	lw         $t1, -16($fp)
	lw         $t0, 8($t1)
	sw         $t0, -12($fp)
	#          local_6 = VCALL local_2 init ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_3 ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -12($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -28($fp)
	#          local_16 = local_6 ;
	lw         $t0, -28($fp)
	sw         $t0, -68($fp)
	#          LABEL label_2 ;
	label_2:

	#          RETURN local_16 ;
	lw         $v0, -68($fp)
	addu       $sp, $sp, 68
	jr         $ra
Cons_rcons:
	move       $fp, $sp
	subu       $sp, $sp, 36
	#          local_1 = ALLOCATE Cons ;
	li         $a0, 20
	li         $v0, 9
	syscall
	sw         $v0, -8($fp)
	la         $t0, vt_Cons
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
	#          local_4 = GETATTR self xcar ;
	lw         $t0, 4($fp)
	lw         $t1, 12($t0)
	sw         $t1, -20($fp)
	#          local_6 = GETATTR self xcdr ;
	lw         $t0, 4($fp)
	lw         $t1, 16($t0)
	sw         $t1, -28($fp)
	#          local_5 = GETTYPEADDR local_6 ;
	lw         $t1, -28($fp)
	lw         $t0, 8($t1)
	sw         $t0, -24($fp)
	#          local_7 = VCALL local_5 rcons ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_6 ;
	lw         $t0, -28($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -24($fp)
	ulw        $t1, 68($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -32($fp)
	#          local_8 = VCALL local_0 init ;
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
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          RETURN local_8 ;
	lw         $v0, -36($fp)
	addu       $sp, $sp, 36
	jr         $ra
Cons_print_list:
	move       $fp, $sp
	subu       $sp, $sp, 36
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 12($t0)
	sw         $t1, -8($fp)
	#          local_2 = VCALL local_0 out_int ;
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
	ulw        $t1, 16($t0)
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
	#          local_4 = LOAD data_5 ;
	la         $t0, data_5
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
	#          local_7 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 16($t0)
	sw         $t1, -32($fp)
	#          local_6 = GETTYPEADDR local_7 ;
	lw         $t1, -32($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_8 = VCALL local_6 print_list ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_7 ;
	lw         $t0, -32($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -28($fp)
	ulw        $t1, 72($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          RETURN local_8 ;
	lw         $v0, -36($fp)
	addu       $sp, $sp, 36
	jr         $ra
Nil_isNil:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          RETURN 1 ;
	li         $v0, 1
	addu       $sp, $sp, 0
	jr         $ra
Nil_rev:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 0
	jr         $ra
Nil_sort:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 0
	jr         $ra
Nil_insert:
	move       $fp, $sp
	subu       $sp, $sp, 8
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 4($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = VCALL local_0 rcons ;
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
	lw         $t0, -4($fp)
	ulw        $t1, 68($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -8($fp)
	#          RETURN local_1 ;
	lw         $v0, -8($fp)
	addu       $sp, $sp, 8
	jr         $ra
Nil_rcons:
	move       $fp, $sp
	subu       $sp, $sp, 20
	#          local_1 = ALLOCATE Cons ;
	li         $a0, 20
	li         $v0, 9
	syscall
	sw         $v0, -8($fp)
	la         $t0, vt_Cons
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
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG self ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -4($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -20($fp)
	#          RETURN local_4 ;
	lw         $v0, -20($fp)
	addu       $sp, $sp, 20
	jr         $ra
Nil_print_list:
	move       $fp, $sp
	subu       $sp, $sp, 0
	#          RETURN 1 ;
	li         $v0, 1
	addu       $sp, $sp, 0
	jr         $ra
Main_iota:
	move       $fp, $sp
	subu       $sp, $sp, 56
	#          local_0 = ALLOCATE Nil ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	la         $t0, vt_Nil
	sw         $t0, 8($v0)
	#          local_1 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 0($t1)
	#          local_2 = 12 ;
	li         $t0, 12
	sw         $t0, -12($fp)
	#          SETATTR local_0 @size local_2 ;
	lw         $t0, -12($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          SETATTR self l local_0 ;
	lw         $t0, -4($fp)
	lw         $t1, 4($fp)
	sw         $t0, 12($t1)
	#          j = 0 ;
	li         $t0, 0
	sw         $t0, -16($fp)
	#          LABEL label_3 ;
	label_3:

	#          local_4 = j < i ;
	lw         $t0, -16($fp)
	lw         $t1, 0($fp)
	slt        $t0, $t0, $t1
	sw         $t0, -20($fp)
	#          IF local_4 GOTO label_4 ;
	lw         $t0, -20($fp)
	bnez       $t0, label_4
	#          GOTO label_5 ;
	b          label_5
	#          LABEL label_4 ;
	label_4:

	#          local_6 = ALLOCATE Cons ;
	li         $a0, 20
	li         $v0, 9
	syscall
	sw         $v0, -28($fp)
	la         $t0, vt_Cons
	sw         $t0, 8($v0)
	#          local_7 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -32($fp)
	#          SETATTR local_6 @type local_7 ;
	lw         $t0, -32($fp)
	lw         $t1, -28($fp)
	sw         $t0, 0($t1)
	#          local_8 = 20 ;
	li         $t0, 20
	sw         $t0, -36($fp)
	#          SETATTR local_6 @size local_8 ;
	lw         $t0, -36($fp)
	lw         $t1, -28($fp)
	sw         $t0, 4($t1)
	#          local_5 = GETTYPEADDR local_6 ;
	lw         $t1, -28($fp)
	lw         $t0, 8($t1)
	sw         $t0, -24($fp)
	#          local_9 = GETATTR self l ;
	lw         $t0, 4($fp)
	lw         $t1, 12($t0)
	sw         $t1, -40($fp)
	#          local_10 = VCALL local_5 init ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_6 ;
	lw         $t0, -28($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG j ;
	lw         $t0, -16($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_9 ;
	lw         $t0, -40($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -24($fp)
	ulw        $t1, 76($t0)
	jalr       $t1
	addu       $sp, $sp, 12
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -44($fp)
	#          SETATTR self l local_10 ;
	lw         $t0, -44($fp)
	lw         $t1, 4($fp)
	sw         $t0, 12($t1)
	#          local_11 = j + 1 ;
	lw         $t0, -16($fp)
	li         $t1, 1
	add        $t0, $t0, $t1
	sw         $t0, -48($fp)
	#          j = local_11 ;
	lw         $t0, -48($fp)
	sw         $t0, -16($fp)
	#          GOTO label_3 ;
	b          label_3
	#          LABEL label_5 ;
	label_5:

	#          local_12 = 0 ;
	li         $t0, 0
	sw         $t0, -52($fp)
	#          local_13 = GETATTR self l ;
	lw         $t0, 4($fp)
	lw         $t1, 12($t0)
	sw         $t1, -56($fp)
	#          RETURN local_13 ;
	lw         $v0, -56($fp)
	addu       $sp, $sp, 56
	jr         $ra
Main_main:
	move       $fp, $sp
	subu       $sp, $sp, 52
	#          local_0 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -4($fp)
	#          local_1 = LOAD data_7 ;
	la         $t0, data_7
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
	#          local_6 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -28($fp)
	#          local_7 = GETTYPEADDR self ;
	lw         $t1, 0($fp)
	lw         $t0, 8($t1)
	sw         $t0, -32($fp)
	#          local_8 = VCALL local_7 in_int ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -32($fp)
	ulw        $t1, 24($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -36($fp)
	#          local_9 = VCALL local_6 iota ;
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
	lw         $t0, -28($fp)
	ulw        $t1, 80($t0)
	jalr       $t1
	addu       $sp, $sp, 8
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -40($fp)
	#          local_5 = GETTYPEADDR local_9 ;
	lw         $t1, -40($fp)
	lw         $t0, 8($t1)
	sw         $t0, -24($fp)
	#          local_10 = VCALL local_5 rev ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_9 ;
	lw         $t0, -40($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -24($fp)
	ulw        $t1, 56($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -44($fp)
	#          local_4 = GETTYPEADDR local_10 ;
	lw         $t1, -44($fp)
	lw         $t0, 8($t1)
	sw         $t0, -20($fp)
	#          local_11 = VCALL local_4 sort ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_10 ;
	lw         $t0, -44($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -20($fp)
	ulw        $t1, 60($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -48($fp)
	#          local_3 = GETTYPEADDR local_11 ;
	lw         $t1, -48($fp)
	lw         $t0, 8($t1)
	sw         $t0, -16($fp)
	#          local_12 = VCALL local_3 print_list ;
	subu       $sp, $sp, 8
	sw         $ra, 0($sp)
	sw         $fp, 4($sp)
	#          ARG local_11 ;
	lw         $t0, -48($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	lw         $t0, -16($fp)
	ulw        $t1, 72($t0)
	jalr       $t1
	addu       $sp, $sp, 4
	lw         $ra, 0($sp)
	lw         $fp, 4($sp)
	addu       $sp, $sp, 8
	sw         $v0, -52($fp)
	#          RETURN local_12 ;
	lw         $v0, -52($fp)
	addu       $sp, $sp, 52
	jr         $ra

.data
	data_1:
		.asciiz    "Main"
	data_2:
		.asciiz    "Cons"
	data_3:
		.asciiz    "Int"
	data_4:
		.asciiz    "List"
	data_5:
		.asciiz    "\n"
	data_6:
		.asciiz    "Nil"
	data_7:
		.asciiz    "How many numbers to sort? "
	data_8:
		.asciiz    "Bool"
	data_9:
		.asciiz    "String"
	data_abort:
		.asciiz    "Abort called from class "
	new_line:
		.asciiz    "\n"
	vt_Object:
		.space     360
	vt_IO:
		.space     360
	vt_Int:
		.space     360
	vt_String:
		.space     360
	vt_Bool:
		.space     360
	vt_List:
		.space     360
	vt_Cons:
		.space     360
	vt_Nil:
		.space     360
	vt_Main:
		.space     360
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
