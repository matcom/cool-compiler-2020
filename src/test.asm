.text
.globl main
# Save method directions in the methods array
la $v0, methods
la $t9, function_abort_Object
sw $t9, 0($v0)
la $t9, function_type_name_Object
sw $t9, 4($v0)
la $t9, function_copy_Object
sw $t9, 8($v0)
la $t9, function_out_string_IO
sw $t9, 12($v0)
la $t9, function_out_int_IO
sw $t9, 16($v0)
la $t9, function_in_int_IO
sw $t9, 20($v0)
la $t9, function_in_string_IO
sw $t9, 24($v0)
la $t9, function_length_String
sw $t9, 28($v0)
la $t9, function_concat_String
sw $t9, 32($v0)
la $t9, function_substr_String
sw $t9, 36($v0)
la $t9, function_main_Main
sw $t9, 40($v0)
la $t9, function_Test_Test
sw $t9, 44($v0)
la $t9, function_testing1_Test
sw $t9, 48($v0)
la $t9, function_testing2_Test
sw $t9, 52($v0)
la $t9, function_testing3_Test
sw $t9, 56($v0)
la $t9, function_testing4_Test
sw $t9, 60($v0)
la $t9, function_Alpha_Alpha
sw $t9, 64($v0)
la $t9, function_print_Alpha
sw $t9, 68($v0)

function_abort_Object:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_abort_self_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Moving self to local_abort_self_0
move $t0, $a0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_type_name_Object:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_type_name_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
local_type_name_result_0 <- Type of self
la $t0, 0($a0)
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_copy_Object:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_copy_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_out_string_IO:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_out_string_self_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_out_string_word_1 to the stack
addiu $sp, $sp, -4
lw $t0, -8($fp)
# Moving self to local_out_string_self_0
move $t0, $a0
lw $t1, -12($fp)
# Saves in local_out_string_word_1 word
la $t1, word
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -8($fp)
sw $t1, -12($fp)
sw $a0, -0($fp)
sw $a1, -4($fp)
jr $ra


function_out_int_IO:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_out_int_self_0 to the stack
addiu $sp, $sp, -4
lw $t0, -8($fp)
# Moving self to local_out_int_self_0
move $t0, $a0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -8($fp)
sw $a0, -0($fp)
sw $a1, -4($fp)
jr $ra


function_in_int_IO:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_in_int_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_in_string_IO:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_in_string_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_length_String:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_length_word_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_length_result_1 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Saves in local_length_word_0 self
la $t0, self
lw $t1, -8($fp)
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t1
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $t1, -8($fp)
sw $a0, -0($fp)
jr $ra


function_concat_String:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_concat_word_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_concat_word_1 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_concat_result_2 to the stack
addiu $sp, $sp, -4
lw $t0, -8($fp)
# Saves in local_concat_word_0 self
la $t0, self
lw $t1, -12($fp)
# Saves in local_concat_word_1 word
la $t1, word
lw $t2, -16($fp)
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t2
# Empty all used registers and saves them to memory
sw $t0, -8($fp)
sw $t1, -12($fp)
sw $t2, -16($fp)
sw $a0, -0($fp)
sw $a1, -4($fp)
jr $ra


function_substr_String:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_substr_word_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_substr_result_1 to the stack
addiu $sp, $sp, -4
lw $t0, -12($fp)
# Saves in local_substr_word_0 self
la $t0, self
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -12($fp)
sw $a0, -0($fp)
sw $a1, -4($fp)
sw $a2, -8($fp)
jr $ra


function_main_Main:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_main_Main_internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_1 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Saving content of a0 to memory to use that register
sw $a0, -0($fp)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
li $a0, 16
syscall
# Save the address in the stack
sw $v0, -4($fp)
# Loads the name of the variable and saves the name like the first field
la $t9, type_Alpha
sw $t9, 0($v0)
# Saves the size of the node
li $t9, 16
sw $t9, 4($v0)
move $t0, $v0
# Allocate dispatch table in the heap
li $v0, 9
li $a0, 36
syscall
# I save the offset of every one of the methods of this type
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_abort_Object in t9
lw $t9, 0($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 0($v0)
# Save the direction of the method function_type_name_Object in t9
lw $t9, 4($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 4($v0)
# Save the direction of the method function_copy_Object in t9
lw $t9, 8($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 8($v0)
# Save the direction of the method function_out_string_IO in t9
lw $t9, 12($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 12($v0)
# Save the direction of the method function_out_int_IO in t9
lw $t9, 16($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 16($v0)
# Save the direction of the method function_in_string_IO in t9
lw $t9, 24($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 20($v0)
# Save the direction of the method function_in_int_IO in t9
lw $t9, 20($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 24($v0)
# Save the direction of the method function_print_Alpha in t9
lw $t9, 68($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 28($v0)
# Save the direction of the method function_Alpha_Alpha in t9
lw $t9, 64($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 32($v0)
sw $v0, 8($t0)
# Restore the variable of a0
lw $a0, -0($fp)
# Static Dispatch of the method Alpha
addiu $sp, $sp, -4
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
# Push the arguments to the stack
# The 3 first registers are saved in a0-a3
move $a0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
# This function will consume the arguments
jal function_Alpha_Alpha
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -8($fp)
# Static Dispatch of the method print
addiu $sp, $sp, -4
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
# Push the arguments to the stack
# The 3 first registers are saved in a0-a3
lw $t1, -4($fp)
move $a0, $t1
# Empty all used registers and saves them to memory
sw $t0, -8($fp)
sw $t1, -4($fp)
# This function will consume the arguments
jal function_print_Alpha
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -8($fp)
# saves the return value
move $t0, $v0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -8($fp)
jr $ra


function_Test_Test:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_Test_Test_test3_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_Test_Test_internal_1 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_Test_Test_internal_2 to the stack
addiu $sp, $sp, -4
# self . test1 <- SET 0
sw $t9, 0
sw $t9, 12($a0)
lw $t0, -4($fp)
# local_Test_Test_test3_0 <- GET self . Test
lw $t0, 20($a0)
# self . test2 <- SET local_Test_Test_test3_0
sw $t0, 16($a0)
lw $t1, -8($fp)
# Saves in local_Test_Test_internal_1 data_0
la $t1, data_0
# self . test3 <- SET local_Test_Test_internal_1
sw $t1, 20($a0)
lw $t2, -12($fp)
# Moving self to local_Test_Test_internal_2
move $t2, $a0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t2
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $t1, -8($fp)
sw $t2, -12($fp)
sw $a0, -0($fp)
jr $ra


function_testing1_Test:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_testing1_Test_internal_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# local_testing1_Test_internal_0 <- 2 - 2
li $t0, 0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_testing2_Test:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_testing2_Test_count_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing2_Test_pow_1 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing2_Test_internal_2 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing2_Test_internal_3 to the stack
addiu $sp, $sp, -4
lw $t0, -12($fp)
# Moving 0 to local_testing2_Test_count_0
li $t0, 0
lw $t1, -16($fp)
# Moving 1 to local_testing2_Test_pow_1
li $t1, 1
# Moving 0 to local_testing2_Test_count_0
li $t0, 0
lw $t2, -20($fp)
# Moving 0 to local_testing2_Test_internal_2
li $t2, 0
lw $t3, -24($fp)
# Moving local_testing2_Test_internal_2 to local_testing2_Test_internal_3
move $t3, $t2
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t3
# Empty all used registers and saves them to memory
sw $t0, -12($fp)
sw $t1, -16($fp)
sw $t2, -20($fp)
sw $t3, -24($fp)
sw $a0, -0($fp)
sw $a1, -4($fp)
sw $a2, -8($fp)
jr $ra


function_testing3_Test:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_testing3_Test_internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing3_Test_internal_1 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Saving content of a0 to memory to use that register
sw $a0, -0($fp)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
li $a0, 16
syscall
# Save the address in the stack
sw $v0, -4($fp)
# Loads the name of the variable and saves the name like the first field
la $t9, type_Alpha
sw $t9, 0($v0)
# Saves the size of the node
li $t9, 16
sw $t9, 4($v0)
move $t0, $v0
# Allocate dispatch table in the heap
li $v0, 9
li $a0, 36
syscall
# I save the offset of every one of the methods of this type
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_abort_Object in t9
lw $t9, 0($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 0($v0)
# Save the direction of the method function_type_name_Object in t9
lw $t9, 4($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 4($v0)
# Save the direction of the method function_copy_Object in t9
lw $t9, 8($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 8($v0)
# Save the direction of the method function_out_string_IO in t9
lw $t9, 12($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 12($v0)
# Save the direction of the method function_out_int_IO in t9
lw $t9, 16($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 16($v0)
# Save the direction of the method function_in_string_IO in t9
lw $t9, 24($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 20($v0)
# Save the direction of the method function_in_int_IO in t9
lw $t9, 20($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 24($v0)
# Save the direction of the method function_print_Alpha in t9
lw $t9, 68($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 28($v0)
# Save the direction of the method function_Alpha_Alpha in t9
lw $t9, 64($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 32($v0)
sw $v0, 8($t0)
# Restore the variable of a0
lw $a0, -0($fp)
# Static Dispatch of the method Alpha
addiu $sp, $sp, -4
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
# Push the arguments to the stack
# The 3 first registers are saved in a0-a3
move $a0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
# This function will consume the arguments
jal function_Alpha_Alpha
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -0($fp)
lw $t1, -8($fp)
# Find the actual name in the dispatch table
# Gets in t9 the actual direction of the dispatch table
lw $t9, 8($t0)
# Saves in t9 the direction of function_testing2_Test
lw $t8, 4($t9)
addiu $sp, $sp, -4
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
# Push the arguments to the stack
# The 3 first registers are saved in a0-a3
# The 3 first registers are saved in a0-a3
lw $t2, -4($fp)
move $a1, $t2
# The 3 first registers are saved in a0-a3
li $a2, 2
# Empty all used registers and saves them to memory
sw $t0, -0($fp)
sw $t1, -8($fp)
sw $t2, -4($fp)
# This function will consume the arguments
jal $t8
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -8($fp)
# saves the return value
move $t0, $v0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -8($fp)
jr $ra


function_testing4_Test:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_testing4_Test_internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing4_Test_internal_1 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing4_Test_internal_2 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing4_Test_internal_3 to the stack
addiu $sp, $sp, -4
lw $t0, -16($fp)
# local_testing4_Test_internal_3 <- 1 + 2
li $t0, 3
lw $t1, -12($fp)
# local_testing4_Test_internal_2 <- local_testing4_Test_internal_3 + 3
addi $t1, $t0, 3
lw $t2, -8($fp)
# local_testing4_Test_internal_1 <- local_testing4_Test_internal_2 + 4
addi $t2, $t1, 4
lw $t3, -4($fp)
# local_testing4_Test_internal_0 <- local_testing4_Test_internal_1 + 5
addi $t3, $t2, 5
# self . test1 <- SET local_testing4_Test_internal_0
sw $t3, 12($a0)
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t3
# Empty all used registers and saves them to memory
sw $t0, -16($fp)
sw $t1, -12($fp)
sw $t2, -8($fp)
sw $t3, -4($fp)
sw $a0, -0($fp)
jr $ra


function_Alpha_Alpha:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_Alpha_Alpha_internal_0 to the stack
addiu $sp, $sp, -4
# self . x <- SET 0
sw $t9, 0
sw $t9, 12($a0)
lw $t0, -4($fp)
# Moving self to local_Alpha_Alpha_internal_0
move $t0, $a0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_print_Alpha:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_print_Alpha_internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_print_Alpha_internal_1 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Saves in local_print_Alpha_internal_0 data_1
la $t0, data_1
lw $t1, -8($fp)
# Find the actual name in the dispatch table
# Gets in t9 the actual direction of the dispatch table
lw $t9, 8($a0)
# Saves in t9 the direction of function_out_string_IO
lw $t8, 3($t9)
addiu $sp, $sp, -4
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
# Push the arguments to the stack
# The 3 first registers are saved in a0-a3
# The 3 first registers are saved in a0-a3
move $a1, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $t1, -8($fp)
sw $a0, -0($fp)
# This function will consume the arguments
jal $t8
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -8($fp)
# saves the return value
move $t0, $v0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -8($fp)
jr $ra

.data
type_String: .asciiz "String"
type_Int: .asciiz "Int"
type_Bool: .asciiz "Bool"
type_Object: .asciiz "Object"
type_IO: .asciiz "IO"
type_Object: .asciiz "Object"
type_IO: .asciiz "IO"
type_String: .asciiz "String"
type_Int: .asciiz "Int"
type_Bool: .asciiz "Bool"
type_Main: .asciiz "Main"
type_Test: .asciiz "Test"
type_Alpha: .asciiz "Alpha"
data_0: .asciiz "1"
data_1: .asciiz "reached!!
"
methods: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0