.text
.globl main
main:
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

entry:
# Gets the params from the stack
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local__internal_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local__internal_1 to the stack
addiu $sp, $sp, -4
lw $t0, -0($fp)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
li $a0, 12
syscall
# Save the address in the stack
sw $v0, -0($fp)
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
lw $t1, -4($fp)
# Static Dispatch of the method main
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
addiu $sp, $sp, -4
# Push the arguments to the stack
# The 3 first registers are saved in a0-a3
move $a0, $t0
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
move $a0, $t0
li $v0, 1
syscall

li $v0, 0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 8
jr $ra


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
# Exiting the program
li $t8, 0
li $v0, 17
move $a0, $t8
syscall
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_type_name_Object:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_type_name_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# local_type_name_result_0 <- Type of self
la $t0, 0($a0)
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_copy_Object:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_copy_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
lw $t9, 4($a0)
# Syscall to allocate memory of the object entry in heap
li $v0, 9
# Saving content of a0 to memory to use that register
sw $a0, -0($fp)
move $a0, $t9
syscall
move $t0, $v0
# Loop to copy every field of the previous object
# t8 the register to loop
li $t8, 0
loop_0:
# In t9 is stored the size of the object
bgt $t8, $t9, exit_0
addi $v0, $v0, 4
addi $a0, $a0, 4
lw $a0, ($a0)
sw $a0, ($v0)
# Increase loop counter
addi $t8, $t8, 4
j loop_0
exit_0:
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_out_string_IO:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_out_string_self_0 to the stack
addiu $sp, $sp, -4
lw $t0, -8($fp)
# Moving self to local_out_string_self_0
move $t0, $a0
# Printing a string
li $v0, 4
# Saving content of a0 to memory to use that register
sw $a0, -0($fp)
move $a0, $a1
syscall
# Restore the variable of self
lw $a0, -0($fp)
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
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
# Printing an int
li $v0, 1
# Saving content of a0 to memory to use that register
sw $a0, -0($fp)
move $a0, $a1
syscall
# Restore the variable of self
lw $a0, -0($fp)
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_in_int_IO:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
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
addiu $sp, $sp, 4
jr $ra


function_in_string_IO:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_in_string_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Reading a string
li $v0, 8
# Saving content of a0 to memory to use that register
sw $a0, -0($fp)
# Putting buffer in a0
move $a0, $t0
# Putting length of string in a1
li $a1, 20
syscall
move $t0, $v0
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_length_String:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_length_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
move $t8, $a0
# Determining the length of a string
loop_1:
lb $t9, 0($t8)
beq $t9, $zero, end_1
addi $t8, $t8, 1
j loop_1
end_1:
sub $t0, $t8, $a0
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_concat_String:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_concat_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -8($fp)
# Copy the first string to dest
# Saving content of a0 to memory to use that register
sw $a0, -0($fp)
# Saving content of a1 to memory to use that register
sw $a1, -4($fp)
move $a0, $a0
move $a1, $t0
jal strcopier
# Concatenate second string on result buffer
move $a0, $a1
move $a1, $v0
jal strcopier
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
# Restore the variable of self
lw $a0, -0($fp)
# Restore the variable of word
lw $a1, -4($fp)
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_substr_String:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_substr_result_0 to the stack
addiu $sp, $sp, -4
lw $t0, -12($fp)
# Getting the substring of a node
sll $t9, $a1, 2
add $t8, $a0, $t9
# Saving dest to iterate over him
move $v0, $t0
loop_3:
sub $t9, $v0, $t0
srl $t9, $t9, 2
beq $t9, $a2, end_3
lb $t9, 0($t8)
sb $t9, 0($v0)
addi $t8, $t8, 1
addi $v0, $v0, 1
j loop_3
end_3:
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra


function_main_Main:
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_main_Main_internal_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# local_main_Main_internal_0 <- 1 + 2
li $t0, 3
move $v0, $t0
# Empty all used registers and saves them to memory
# Removing all locals from stack
addiu $sp, $sp, 4
jr $ra

.data
type_Object: .asciiz "Object"
type_IO: .asciiz "IO"
type_String: .asciiz "String"
type_Int: .asciiz "Int"
type_Bool: .asciiz "Bool"
type_Main: .asciiz "Main"
methods: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
local_in_string_result_0: .space 20
local_substr_result_0: .space 20