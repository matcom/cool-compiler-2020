
.text
main:
	move       $fp, $sp
	#          3 LOCALS = 12 bytes
	sw         $ra, -16($fp)
	subu       $sp, $sp, 16
	#          local_2 = LOAD data_1 ;
	la         $t0, data_1
	sw         $t0, -4($fp)
	#          __main__ = ALLOCATE Main ;
	li         $a0, 12
	li         $v0, 9
	syscall
	sw         $v0, -8($fp)
	#          SETATTR __main__ @type local_2 ;
	lw         $t0, -4($fp)
	lw         $t1, -8($fp)
	sw         $t0, 4($t1)
	#          ARG __main__ ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          main_result = VCALL Main main ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        Main_main
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	addu       $sp, $sp, 16
	jr         $ra
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
	jr         $ra
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
	jr         $ra
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
	jr         $ra
IO_in_int:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          int = READINT ;
	li         $v0, 5
	syscall
	sw         $v0, -4($fp)
	#          RETURN int ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
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
	jr         $ra
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
	jr         $ra
String_length:
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
	jr         $ra
String_concat:
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
	jr         $ra
String_substr:
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
	jr         $ra
List_isNil:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List abort ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        Object_abort
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN ;
	li         $v0, 0
	addu       $sp, $sp, 4
	jr         $ra
List_cons:
	move       $fp, $sp
	#          2 LOCALS = 8 bytes
	sw         $ra, -12($fp)
	subu       $sp, $sp, 12
	#          local_0 = ALLOCATE Cons ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_1 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_1 = 16 ;
	li         $t0, 16
	sw         $t0, -8($fp)
	#          SETATTR local_0 @size local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_1 = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -8($fp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG hd ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Cons init ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        Cons_init
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
List_car:
	move       $fp, $sp
	#          2 LOCALS = 8 bytes
	sw         $ra, -12($fp)
	subu       $sp, $sp, 12
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List abort ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        Object_abort
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          local_1 = ALLOCATE Int ;
	li         $a0, 8
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_2 = LOAD data_3 ;
	la         $t0, data_3
	sw         $t0, -8($fp)
	#          SETATTR local_1 @type local_2 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_2 = 8 ;
	li         $t0, 8
	sw         $t0, -8($fp)
	#          SETATTR local_1 @size local_2 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          RETURN local_1 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
List_cdr:
	move       $fp, $sp
	#          2 LOCALS = 8 bytes
	sw         $ra, -12($fp)
	subu       $sp, $sp, 12
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List abort ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        Object_abort
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          local_1 = ALLOCATE List ;
	li         $a0, 8
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_2 = LOAD data_4 ;
	la         $t0, data_4
	sw         $t0, -8($fp)
	#          SETATTR local_1 @type local_2 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_2 = 8 ;
	li         $t0, 8
	sw         $t0, -8($fp)
	#          SETATTR local_1 @size local_2 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          RETURN local_1 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
List_rev:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List cdr ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        List_cdr
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_sort:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List cdr ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        List_cdr
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_insert:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List cdr ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        List_cdr
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_rcons:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List cdr ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        List_cdr
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
List_print_list:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List abort ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        Object_abort
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
Cons_isNil:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          RETURN ;
	li         $v0, 0
	addu       $sp, $sp, 4
	jr         $ra
Cons_init:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          SETATTR self xcar hd ;
	lw         $t0, 4($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          SETATTR self xcdr tl ;
	lw         $t0, 8($fp)
	lw         $t1, 0($fp)
	sw         $t0, 8($t1)
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 4
	jr         $ra
Cons_car:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          local_0 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -4($fp)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
Cons_cdr:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          local_0 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 8($t0)
	sw         $t1, -4($fp)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
Cons_rev:
	move       $fp, $sp
	#          2 LOCALS = 8 bytes
	sw         $ra, -12($fp)
	subu       $sp, $sp, 12
	#          local_0 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 8($t0)
	sw         $t1, -4($fp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List rev ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        List_rev
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          local_2 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -8($fp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_2 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List rcons ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        List_rcons
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
Cons_sort:
	move       $fp, $sp
	#          2 LOCALS = 8 bytes
	sw         $ra, -12($fp)
	subu       $sp, $sp, 12
	#          local_0 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 8($t0)
	sw         $t1, -4($fp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List sort ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        List_sort
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          local_2 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -8($fp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_2 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List insert ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        List_insert
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
Cons_insert:
	move       $fp, $sp
	#          3 LOCALS = 12 bytes
	sw         $ra, -16($fp)
	subu       $sp, $sp, 16
	#          local_0 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -4($fp)
	#          local_1 = i < local_0 ;
	lw         $t1, 4
	lw         $t2, -4
	sle        $t0, $t1, $t2
	sw         $t0, -8
	#          IF local_1 GOTO label_1 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_1
	#          local_0 = ALLOCATE Cons ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_1 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_1 = 16 ;
	li         $t0, 16
	sw         $t0, -8($fp)
	#          SETATTR local_0 @size local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_9 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -12($fp)
	#          local_1 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 8($t0)
	sw         $t1, -8($fp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_1 = VCALL List insert ;
	subu       $sp, $sp, 12
	sw         $t1, 8($sp)
	sw         $t0, 4($sp)
	sw         $t2, 0($sp)
	jal        List_insert
	lw         $t1, 8($sp)
	lw         $t0, 4($sp)
	lw         $t2, 0($sp)
	addu       $sp, $sp, 12
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_9 ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Cons init ;
	subu       $sp, $sp, 12
	sw         $t1, 8($sp)
	sw         $t0, 4($sp)
	sw         $t2, 0($sp)
	jal        Cons_init
	lw         $t1, 8($sp)
	lw         $t0, 4($sp)
	lw         $t2, 0($sp)
	addu       $sp, $sp, 12
	#          local_9 = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -12($fp)
	#          GOTO label_2 ;
	b          label_2
	#          LABEL label_1 ;
	label_1:

	#          local_0 = ALLOCATE Cons ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_1 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_1 = 16 ;
	li         $t0, 16
	sw         $t0, -8($fp)
	#          SETATTR local_0 @size local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Cons init ;
	subu       $sp, $sp, 12
	sw         $t1, 8($sp)
	sw         $t0, 4($sp)
	sw         $t2, 0($sp)
	jal        Cons_init
	lw         $t1, 8($sp)
	lw         $t0, 4($sp)
	lw         $t2, 0($sp)
	addu       $sp, $sp, 12
	#          local_9 = local_0 ;
	lw         $t0, -4($fp)
	sw         $t0, -12($fp)
	#          LABEL label_2 ;
	label_2:

	#          RETURN local_9 ;
	lw         $v0, -12($fp)
	addu       $sp, $sp, 16
	jr         $ra
Cons_rcons:
	move       $fp, $sp
	#          3 LOCALS = 12 bytes
	sw         $ra, -16($fp)
	subu       $sp, $sp, 16
	#          local_0 = ALLOCATE Cons ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_1 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_1 = 16 ;
	li         $t0, 16
	sw         $t0, -8($fp)
	#          SETATTR local_0 @size local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_3 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -12($fp)
	#          local_1 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 8($t0)
	sw         $t1, -8($fp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_1 = VCALL List rcons ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        List_rcons
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_3 ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Cons init ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        Cons_init
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 16
	jr         $ra
Cons_print_list:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          local_0 = GETATTR self xcar ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -4($fp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_1 = VCALL Cons out_int ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        IO_out_int
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          local_0 = LOAD data_5 ;
	la         $t0, data_5
	sw         $t0, -4($fp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_3 = VCALL Cons out_string ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        IO_out_string
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          local_0 = GETATTR self xcdr ;
	lw         $t0, 0($fp)
	lw         $t1, 8($t0)
	sw         $t1, -4($fp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List print_list ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        List_print_list
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
Nil_isNil:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          RETURN ;
	li         $v0, 0
	addu       $sp, $sp, 4
	jr         $ra
Nil_rev:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 4
	jr         $ra
Nil_sort:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          RETURN self ;
	lw         $v0, 0($fp)
	addu       $sp, $sp, 4
	jr         $ra
Nil_insert:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Nil rcons ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        Nil_rcons
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8
	jr         $ra
Nil_rcons:
	move       $fp, $sp
	#          2 LOCALS = 8 bytes
	sw         $ra, -12($fp)
	subu       $sp, $sp, 12
	#          local_0 = ALLOCATE Cons ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_1 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_1 = 16 ;
	li         $t0, 16
	sw         $t0, -8($fp)
	#          SETATTR local_0 @size local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG i ;
	lw         $t0, 4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Cons init ;
	subu       $sp, $sp, 8
	sw         $t0, 4($sp)
	sw         $t1, 0($sp)
	jal        Cons_init
	lw         $t0, 4($sp)
	lw         $t1, 0($sp)
	addu       $sp, $sp, 8
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 12
	jr         $ra
Nil_print_list:
	move       $fp, $sp
	#          0 LOCALS = 0 bytes
	sw         $ra, -4($fp)
	subu       $sp, $sp, 4
	#          RETURN ;
	li         $v0, 0
	addu       $sp, $sp, 4
	jr         $ra
Main_iota:
	move       $fp, $sp
	#          3 LOCALS = 12 bytes
	sw         $ra, -16($fp)
	subu       $sp, $sp, 16
	#          local_0 = ALLOCATE Nil ;
	li         $a0, 8
	li         $v0, 9
	syscall
	sw         $v0, -4($fp)
	#          local_1 = LOAD data_6 ;
	la         $t0, data_6
	sw         $t0, -8($fp)
	#          SETATTR local_0 @type local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          local_1 = 8 ;
	li         $t0, 8
	sw         $t0, -8($fp)
	#          SETATTR local_0 @size local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, -4($fp)
	sw         $t0, 4($t1)
	#          SETATTR self l local_0 ;
	lw         $t0, -4($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          local_0 = 0 ;
	li         $t0, 0
	sw         $t0, -4($fp)
	#          LABEL label_3 ;
	label_3:

	#          local_1 = local_0 < i ;
	lw         $t1, -4
	lw         $t2, 4
	sle        $t0, $t1, $t2
	sw         $t0, -8
	#          IF local_1 GOTO label_4 ;
	lw         $t0, -8($fp)
	bnez       $t0, label_4
	#          GOTO label_5 ;
	b          label_5
	#          LABEL label_4 ;
	label_4:

	#          local_1 = ALLOCATE Cons ;
	li         $a0, 16
	li         $v0, 9
	syscall
	sw         $v0, -8($fp)
	#          local_6 = LOAD data_2 ;
	la         $t0, data_2
	sw         $t0, -12($fp)
	#          SETATTR local_1 @type local_6 ;
	lw         $t0, -12($fp)
	lw         $t1, -8($fp)
	sw         $t0, 4($t1)
	#          local_6 = 16 ;
	li         $t0, 16
	sw         $t0, -12($fp)
	#          SETATTR local_1 @size local_6 ;
	lw         $t0, -12($fp)
	lw         $t1, -8($fp)
	sw         $t0, 4($t1)
	#          local_6 = GETATTR self l ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -12($fp)
	#          ARG local_1 ;
	lw         $t0, -8($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_6 ;
	lw         $t0, -12($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_1 = VCALL Cons init ;
	subu       $sp, $sp, 12
	sw         $t1, 8($sp)
	sw         $t0, 4($sp)
	sw         $t2, 0($sp)
	jal        Cons_init
	lw         $t1, 8($sp)
	lw         $t0, 4($sp)
	lw         $t2, 0($sp)
	addu       $sp, $sp, 12
	#          SETATTR self l local_1 ;
	lw         $t0, -8($fp)
	lw         $t1, 0($fp)
	sw         $t0, 4($t1)
	#          local_1 = local_0 + 1 ;
	lw         $t0, -4($fp)
	li         $t1, 1
	add        $t2, $t0, $t1
	sw         $t2, -8($fp)
	#          GOTO label_3 ;
	b          label_3
	#          LABEL label_5 ;
	label_5:

	#          local_0 = GETATTR self l ;
	lw         $t0, 0($fp)
	lw         $t1, 4($t0)
	sw         $t1, -4($fp)
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 16
	jr         $ra
Main_main:
	move       $fp, $sp
	#          1 LOCALS = 4 bytes
	sw         $ra, -8($fp)
	subu       $sp, $sp, 8
	#          local_0 = LOAD data_7 ;
	la         $t0, data_7
	sw         $t0, -4($fp)
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_1 = VCALL Main out_string ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        IO_out_string
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Main in_int ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        IO_in_int
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          ARG self ;
	lw         $t0, 0($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL Main iota ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        Main_iota
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List rev ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        List_rev
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List sort ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        List_sort
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          ARG local_0 ;
	lw         $t0, -4($fp)
	subu       $sp, $sp, 4
	sw         $t0, ($sp)
	#          local_0 = VCALL List print_list ;
	subu       $sp, $sp, 4
	sw         $t0, 0($sp)
	jal        List_print_list
	lw         $t0, 0($sp)
	addu       $sp, $sp, 4
	#          RETURN local_0 ;
	lw         $v0, -4($fp)
	addu       $sp, $sp, 8

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
	str:
		.space     1024
	concat_result:
		.space     2048
	substring_result:
		.space     1024
