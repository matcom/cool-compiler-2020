.text
.globl main
main:
# Save types directions in the types array
la $t9, types
# Save space to locate the type info
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_String
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 0($t9)
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_Int
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 4($t9)
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_Object
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 8($t9)
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_Bool
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 12($t9)
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_IO
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 16($t9)
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_Main
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 20($t9)
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_Test
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 24($t9)
# Allocating memory
li $v0, 9
li $a0, 8
syscall
# Filling table methods
la $t8, type_Alpha
sw $t8, 0($v0)
# Copying direction to array
sw $v0, 28($t9)
# Copying parents
lw $v0, 0($t9)
li $t8, 0
sw $t8, 4($v0)
lw $v0, 4($t9)
li $t8, 0
sw $t8, 4($v0)
lw $v0, 8($t9)
li $t8, 0
sw $t8, 4($v0)
lw $v0, 12($t9)
li $t8, 0
sw $t8, 4($v0)
lw $v0, 16($t9)
lw $t8, 8($t9)
sw $t8, 4($v0)
lw $v0, 20($t9)
lw $t8, 8($t9)
sw $t8, 4($v0)
lw $v0, 24($t9)
lw $t8, 8($t9)
sw $t8, 4($v0)
lw $v0, 28($t9)
lw $t8, 16($t9)
sw $t8, 4($v0)
# Save method directions in the methods array
la $v0, methods
la $t9, entry
sw $t9, 0($v0)
la $t9, function_abort_Object
sw $t9, 4($v0)
la $t9, function_type_name_Object
sw $t9, 8($v0)
la $t9, function_copy_Object
sw $t9, 12($v0)
la $t9, function_out_string_IO
sw $t9, 16($v0)
la $t9, function_out_int_IO
sw $t9, 20($v0)
la $t9, function_in_int_IO
sw $t9, 24($v0)
la $t9, function_in_string_IO
sw $t9, 28($v0)
la $t9, function_length_String
sw $t9, 32($v0)
la $t9, function_concat_String
sw $t9, 36($v0)
la $t9, function_substr_String
sw $t9, 40($v0)
la $t9, function_main_Main
sw $t9, 44($v0)
la $t9, function_Test_Test
sw $t9, 48($v0)
la $t9, function_testing1_Test
sw $t9, 52($v0)
la $t9, function_testing2_Test
sw $t9, 56($v0)
la $t9, function_testing3_Test
sw $t9, 60($v0)
la $t9, function_testing4_Test
sw $t9, 64($v0)
la $t9, function_Alpha_Alpha
sw $t9, 68($v0)
la $t9, function_print_Alpha
sw $t9, 72($v0)

entry:
# Gets the params from the stack
move $fp, $sp
# Gets the frame pointer from the stack
# Updates stack pointer pushing local__internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local__internal_1 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
li $a0, 12
syscall
# Loads the name of the variable and saves the name like the first field
la $t9, type_Main
sw $t9, 0($v0)
# Saves the size of the node
li $t9, 12
sw $t9, 4($v0)
move $t0, $v0
# Allocate dispatch table in the heap
li $v0, 9
li $a0, 16
syscall
# I save the offset of every one of the methods of this type
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_abort_Object in t9
lw $t9, 4($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 0($v0)
# Save the direction of the method function_type_name_Object in t9
lw $t9, 8($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 4($v0)
# Save the direction of the method function_copy_Object in t9
lw $t9, 12($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 8($v0)
# Save the direction of the method function_main_Main in t9
lw $t9, 44($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 12($v0)
sw $v0, 8($t0)
# Adding Type Info addr
la $t8, types
lw $v0, 20($t8)
sw $v0, 12($t0)
lw $t1, -4($fp)
# Static Dispatch of the method main
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
addiu $sp, $sp, -4
# Push the arguments to the stack
# The rest of the arguments are push into the stack
sw $t0, ($sp)
addiu $sp, $sp, -4
# Empty all used registers and saves them to memory
sw $t0, -0($fp)
sw $t1, -4($fp)
# This function will consume the arguments
jal function_main_Main
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -4($fp)
# saves the return value
move $t0, $v0
li $v0, 0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_abort_Object:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_abort_self_0 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
lw $t1, -4($fp)
# Moving self to local_abort_self_0
move $t1, $t0
sw $t1, -4($fp)
# Exiting the program
li $t8, 0
li $v0, 17
move $a0, $t8
syscall
move $v0, $t1
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_type_name_Object:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_type_name_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
lw $t1, -4($fp)
# local_type_name_result_0 <- Type of self
lw $t1, 0($t0)
move $v0, $t1
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_copy_Object:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_copy_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
lw $t1, -4($fp)
lw $t9, 4($t0)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
move $a0, $t9
syscall
move $t1, $v0
# Loop to copy every field of the previous object
# t8 the register to loop
li $t8, 0
loop_0:
# In t9 is stored the size of the object
bge $t8, $t9, exit_0
lw $a0, ($t0)
sw $a0, ($v0)
addi $v0, $v0, 4
addi $t0, $t0, 4
# Increase loop counter
addi $t8, $t8, 4
j loop_0
exit_0:
move $v0, $t1
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_out_string_IO:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Pops the register with the param value word
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_out_string_self_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
lw $t1, -8($fp)
# Moving self to local_out_string_self_0
move $t1, $t0
sw $t1, -8($fp)
lw $t2, -0($fp)
# Printing a string
li $v0, 4
move $a0, $t2
syscall
move $v0, $t1
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 12
jr $ra


function_out_int_IO:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Pops the register with the param value number
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_out_int_self_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
lw $t1, -8($fp)
# Moving self to local_out_int_self_0
move $t1, $t0
sw $t1, -8($fp)
lw $t2, -0($fp)
# Printing an int
li $v0, 1
move $a0, $t2
syscall
move $v0, $t1
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 12
jr $ra


function_in_int_IO:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_in_int_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Reading a int
li $v0, 5
syscall
move $t0, $v0
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_in_string_IO:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_in_string_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Copying buffer memory address
la $t0, local_in_string_result_0
# Reading a string
li $v0, 8
# Putting buffer in a0
move $a0, $t0
# Putting length of string in a1
li $a1, 20
syscall
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_length_String:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_length_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
lw $t1, -4($fp)
move $t8, $t0
# Determining the length of a string
loop_1:
lb $t9, 0($t8)
beq $t9, $zero, end_1
addi $t8, $t8, 1
j loop_1
end_1:
sub $t1, $t8, $t0
move $v0, $t1
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_concat_String:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Pops the register with the param value word
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_concat_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
lw $t1, -0($fp)
lw $t2, -8($fp)
la $t2, local_concat_result_0
# Copy the first string to dest
move $a0, $t0
move $a1, $t2
sw $ra, ($sp)
addiu $sp, $sp, -4
jal strcopier
# Concatenate second string on result buffer
move $a0, $t1
move $a1, $v0
jal strcopier
addiu $sp, $sp, 4
lw $ra, ($sp)
j finish_2
# Definition of strcopier
strcopier:
# In a0 is the source and in a1 is the destination
loop_2:
lb $t8, ($a0)
beq $t8, $zero, end_2
addiu $a0, $a0, 1
sb $t8, ($a1)
addiu $a1, $a1, 1
b loop_2
end_2:
move $v0, $a1
jr $ra
finish_2:
move $v0, $t2
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 12
jr $ra


function_substr_String:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Pops the register with the param value begin
addiu $fp, $fp, 4
# Pops the register with the param value end
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_substr_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
lw $t1, -0($fp)
lw $t2, -12($fp)
la $t2, local_substr_result_0
lw $t3, -8($fp)
# Getting the substring of a node
# Move to the first position in the string
li $v0, 0
move $t8, $t3
start_3:
lb $t9, 0($t8)
beqz $t9, error_3
addi $v0, 1
addi $t8, 1
blt $v0, $t0, start_3
# Saving dest to iterate over him
move $v0, $t2
loop_3:
sub $t9, $v0, $t2
beq $t9, $t1, end_3
lb $t9, 0($t8)
beqz $t9, error_3
sb $t9, 0($v0)
addi $t8, $t8, 1
addi $v0, $v0, 1
j loop_3
error_3:
la $a0, index_error
j .raise
end_3:
move $v0, $t2
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 16
jr $ra


function_main_Main:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_main_Main_internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_1 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_2 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_3 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
li $a0, 16
syscall
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
lw $t9, 4($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 0($v0)
# Save the direction of the method function_type_name_Object in t9
lw $t9, 8($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 4($v0)
# Save the direction of the method function_copy_Object in t9
lw $t9, 12($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 8($v0)
# Save the direction of the method function_out_string_IO in t9
lw $t9, 16($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 12($v0)
# Save the direction of the method function_out_int_IO in t9
lw $t9, 20($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 16($v0)
# Save the direction of the method function_in_string_IO in t9
lw $t9, 28($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 20($v0)
# Save the direction of the method function_in_int_IO in t9
lw $t9, 24($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 24($v0)
# Save the direction of the method function_print_Alpha in t9
lw $t9, 72($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 28($v0)
# Save the direction of the method function_Alpha_Alpha in t9
lw $t9, 68($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 32($v0)
sw $v0, 8($t0)
# Adding Type Info addr
la $t8, types
lw $v0, 28($t8)
sw $v0, 12($t0)
# Static Dispatch of the method Alpha
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
addiu $sp, $sp, -4
# Push the arguments to the stack
# The rest of the arguments are push into the stack
sw $t0, ($sp)
addiu $sp, $sp, -4
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
# This function will consume the arguments
jal function_Alpha_Alpha
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -4($fp)
lw $t1, -12($fp)
# local_main_Main_internal_2 <- Type of local_main_Main_internal_0
lw $t1, 0($t0)
lw $t2, -16($fp)
# Saves in local_main_Main_internal_3 data_0
la $t2, data_0
# local_main_Main_internal_2 <- local_main_Main_internal_2 = local_main_Main_internal_3
move $t8, $t1
move $t9, $t2
loop_4:
lb $a0, ($t8)
lb $a1, ($t9)
beqz $a0, check_4
beqz $a1, mismatch_4
seq $v0, $a0, $a1
beqz $v0, mismatch_4
addi $t8, $t8, 1
addi $t9, $t9, 1
j loop_4
mismatch_4:
li $v0, 0
j end_4
check_4:
bnez $a1, mismatch_4
li $v0, 1
end_4:
move $t1, $v0
# If not local_main_Main_internal_2 goto continue__38
beqz $t1, continue__38
la $a0, dispatch_error
j .raise
continue__38:
lw $t3, -8($fp)
# Static Dispatch of the method print
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
addiu $sp, $sp, -4
# Push the arguments to the stack
# The rest of the arguments are push into the stack
sw $t0, ($sp)
addiu $sp, $sp, -4
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $t1, -12($fp)
sw $t2, -16($fp)
sw $t3, -8($fp)
# This function will consume the arguments
jal function_print_Alpha
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -8($fp)
# saves the return value
move $t0, $v0
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 20
jr $ra


function_Test_Test:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_Test_Test_test3_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_Test_Test_internal_1 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_Test_Test_internal_2 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
# self . test1 <- SET 0
li $t9, 0
sw $t9, 16($t0)
lw $t1, -4($fp)
# local_Test_Test_test3_0 <- GET self . test3
lw $t1, 24($t0)
# self . test2 <- SET local_Test_Test_test3_0
sw $t1, 20($t0)
lw $t2, -8($fp)
# Saves in local_Test_Test_internal_1 data_1
la $t2, data_1
# self . test3 <- SET local_Test_Test_internal_1
sw $t2, 24($t0)
lw $t3, -12($fp)
# Moving self to local_Test_Test_internal_2
move $t3, $t0
sw $t3, -12($fp)
move $v0, $t3
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 16
jr $ra


function_testing1_Test:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_testing1_Test_internal_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# local_testing1_Test_internal_0 <- 2 - 2
li $t0, 0
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_testing2_Test:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Pops the register with the param value a
addiu $fp, $fp, 4
# Pops the register with the param value b
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
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
sw $t0, -12($fp)
lw $t1, -16($fp)
# Moving 1 to local_testing2_Test_pow_1
li $t1, 1
sw $t1, -16($fp)
# Moving 0 to local_testing2_Test_count_0
li $t0, 0
sw $t0, -12($fp)
lw $t2, -20($fp)
# Moving 0 to local_testing2_Test_internal_2
li $t2, 0
sw $t2, -20($fp)
lw $t3, -24($fp)
# Moving local_testing2_Test_internal_2 to local_testing2_Test_internal_3
move $t3, $t2
sw $t3, -24($fp)
move $v0, $t3
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 28
jr $ra


function_testing3_Test:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_testing3_Test_internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_testing3_Test_internal_1 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
li $a0, 16
syscall
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
lw $t9, 4($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 0($v0)
# Save the direction of the method function_type_name_Object in t9
lw $t9, 8($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 4($v0)
# Save the direction of the method function_copy_Object in t9
lw $t9, 12($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 8($v0)
# Save the direction of the method function_out_string_IO in t9
lw $t9, 16($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 12($v0)
# Save the direction of the method function_out_int_IO in t9
lw $t9, 20($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 16($v0)
# Save the direction of the method function_in_string_IO in t9
lw $t9, 28($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 20($v0)
# Save the direction of the method function_in_int_IO in t9
lw $t9, 24($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 24($v0)
# Save the direction of the method function_print_Alpha in t9
lw $t9, 72($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 28($v0)
# Save the direction of the method function_Alpha_Alpha in t9
lw $t9, 68($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 32($v0)
sw $v0, 8($t0)
# Adding Type Info addr
la $t8, types
lw $v0, 28($t8)
sw $v0, 12($t0)
# Static Dispatch of the method Alpha
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
addiu $sp, $sp, -4
# Push the arguments to the stack
# The rest of the arguments are push into the stack
sw $t0, ($sp)
addiu $sp, $sp, -4
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
# This function will consume the arguments
jal function_Alpha_Alpha
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -0($fp)
lw $t1, -8($fp)
# Find the actual name in the dispatch table
# Gets in t9 the actual direction of the dispatch table
lw $t9, 8($t0)
# Saves in t8 the direction of function_testing2_Test
lw $t8, 16($t9)
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
addiu $sp, $sp, -4
# Push the arguments to the stack
# The rest of the arguments are push into the stack
li $t9, 2
sw $t9, ($sp)
addiu $sp, $sp, -4
# The rest of the arguments are push into the stack
lw $t2, -4($fp)
sw $t2, ($sp)
addiu $sp, $sp, -4
# The rest of the arguments are push into the stack
sw $t0, ($sp)
addiu $sp, $sp, -4
# Empty all used registers and saves them to memory
sw $t0, -0($fp)
sw $t1, -8($fp)
sw $t2, -4($fp)
# This function will consume the arguments
jal $t8
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -8($fp)
# saves the return value
move $t0, $v0
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 12
jr $ra


function_testing4_Test:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
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
lw $t4, -0($fp)
# self . test1 <- SET local_testing4_Test_internal_0
sw $t3, 16($t4)
move $v0, $t3
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 20
jr $ra


function_Alpha_Alpha:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_Alpha_Alpha_internal_0 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
# self . x <- SET 0
li $t9, 0
sw $t9, 16($t0)
lw $t1, -4($fp)
# Moving self to local_Alpha_Alpha_internal_0
move $t1, $t0
sw $t1, -4($fp)
move $v0, $t1
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


function_print_Alpha:
# Gets the params from the stack
move $fp, $sp
# Pops the register with the param value self
addiu $fp, $fp, 4
# Gets the frame pointer from the stack
# Updates stack pointer pushing local_print_Alpha_internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_print_Alpha_internal_1 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Saves in local_print_Alpha_internal_0 data_2
la $t0, data_2
lw $t1, -0($fp)
lw $t2, -8($fp)
# Find the actual name in the dispatch table
# Gets in t9 the actual direction of the dispatch table
lw $t9, 8($t1)
# Saves in t8 the direction of function_out_string_IO
lw $t8, 12($t9)
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
addiu $sp, $sp, -4
# Push the arguments to the stack
# The rest of the arguments are push into the stack
sw $t0, ($sp)
addiu $sp, $sp, -4
# The rest of the arguments are push into the stack
sw $t1, ($sp)
addiu $sp, $sp, -4
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $t1, -0($fp)
sw $t2, -8($fp)
# This function will consume the arguments
jal $t8
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -8($fp)
# saves the return value
move $t0, $v0
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 12
jr $ra

# Raise exception method
.raise:
li $v0, 4
syscall
li $v0, 17
li $a0, 1
syscall
.data
type_Object: .asciiz "Object"
type_IO: .asciiz "IO"
type_String: .asciiz "String"
type_Int: .asciiz "Int"
type_Bool: .asciiz "Bool"
type_Main: .asciiz "Main"
type_Test: .asciiz "Test"
type_Alpha: .asciiz "Alpha"
type_Void: .asciiz "Void"
types: .word 0, 0, 0, 0, 0, 0, 0, 0
data_0: .asciiz "Void"
data_1: .asciiz "1"
data_2: .asciiz "reached!!
"
methods: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
local_in_string_result_0: .space 20
local_concat_result_0: .space 20
local_substr_result_0: .space 20
zero_error: .asciiz "Division by zero error
"
case_void_error: .asciiz "Case on void error
"
dispatch_error: .asciiz "Dispatch on void error
"
case_error: .asciiz "Case statement without a matching branch error
"
index_error: .asciiz "Substring out of range error
"
heap_error: .asciiz "Heap overflow error
"