
.text
main:
	move       $fp, $sp
	#          2 LOCALS = 8 bytes
	sw         $ra, -12($fp)
	subu       $sp, $sp, 12
	#          __main__ = ALLOCATE Main ;
	li         $a0, 8
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          ARG __main__ ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          main_result = VCALL Main main ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        Main_main
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	addu       $sp, $sp, 12
IO_out_int:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          PRINT int ;
	lw         $a0, 4($fp)
	li         $v0, 1
	syscall
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 4
IO_out_string:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          PRINT str ;
	lw         $a0, 4($fp)
	li         $v0, 4
	syscall
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 4
IO_in_string:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	la         $a0, str
	li         $a1, 1024
	li         $v0, 8
	syscall
	sw         $a0, -4($fp)
	#          RETURN str ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
IO_in_int:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          int = READINT ;
	li         $v0, 5
	syscall
	sw         $v0, -4
	#          RETURN int ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
Object_type_name:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          type = TYPEOF self ;
	lw         $t0, 0($fp)
	sw         $t0, -4($fp)
	#          RETURN type ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
Object_copy:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
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
	addu       $sp, $sp, 8
length_String:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
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
	addu       $sp, $sp, 8
concat_String:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          concat_result = CONCAT self x ;
	la         $t0, 0
	la         $t1, 0
	la         $t2, 0
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
	addu       $sp, $sp, 8
substr_String:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          substring_result = SUBSTRING self i l;
	lw         $t0, 0($fp)
	la         $t1, substring_result
	lw         $t4, 4($fp)
	lw         $t2, 8($fp)
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
	addu       $sp, $sp, 8
Main_main:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          local_0 = LOAD data_1 ;
	la         $t0, data_1
	sw         $t0, -4($fp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Main out_string ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        IO_out_string
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8

.data
	data_1:
		.asciiz    "Hello, World.\n"
	str:
		.space     1024
	concat_result:
		.space     2048
	substring_result:
		.space     1024
