.text
.globl main

entry:
# Save method direction in the methods array
la $t9, entry
la $v0, methods
sw $t9, 0($v0)
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
li $a0, 32
syscall
# I save the offset of every one of the methods of this type
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_abort_Object in t9
lw $t9, 28($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 0($v0)
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_type_name_Object in t9
lw $t9, 32($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 4($v0)
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_copy_Object in t9
lw $t9, 36($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 8($v0)
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_out_string_IO in t9
lw $t9, 0($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 12($v0)
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_out_int_IO in t9
lw $t9, 4($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 16($v0)
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_in_string_IO in t9
lw $t9, 8($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 20($v0)
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_in_int_IO in t9
lw $t9, 12($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 24($v0)
# Save the direction of methods
la $t8, methods
# Save the direction of the method function_main_Main in t9
lw $t9, 48($t8)
# Save the direction of the method in his position in the dispatch table
sw $t9, 28($v0)
sw $v0, 8($t0)
lw $t1, -4($fp)
# Static Dispatch of the method main
addiu $sp, $sp, -4
sw $fp, ($sp)
addiu $sp, $sp, -4
sw $ra, ($sp)
# Push the arguments to the stack
# The 3 first registers are saved in a0-a3
move $a0, $t0
# Empty all used registers and saves them to memory
sw $t0, -0($fp)
sw $t1, -4($fp)
# This function will consume the arguments
jal function_main_Main
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -4($fp)
# saves the return value
move $t0, $v0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
li $v0, 0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
jr $ra


function_Main_Main:
# Save method direction in the methods array
la $t9, function_Main_Main
la $v0, methods
sw $t9, 16($v0)
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_Main_Main_internal_0 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Moving self to local_Main_Main_internal_0
move $t0, $a0
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t0
# Empty all used registers and saves them to memory
sw $t0, -4($fp)
sw $a0, -0($fp)
jr $ra


function_main_Main:
# Save method direction in the methods array
la $t9, function_main_Main
la $v0, methods
sw $t9, 32($v0)
# Gets the params from the stack
# The 3 firsts registers are saved in a0-a3
# Gets the frame pointer from the stack
move $fp, $sp
# Updates stack pointer pushing local_main_Main_test1_0 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_1 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_2 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_3 to the stack
addiu $sp, $sp, -4
# Updates stack pointer pushing local_main_Main_internal_4 to the stack
addiu $sp, $sp, -4
lw $t0, -4($fp)
# Moving 0 to local_main_Main_test1_0
li $t0, 0
lw $t1, -8($fp)
# local_main_Main_internal_1 <- 1 + 2
li $t1, 3
lw $t2, -12($fp)
# Find the actual name in the dispatch table
# Gets in t9 the actual direction of the dispatch table
lw $t9, 8($a0)
# Saves in t9 the direction of function_out_int_IO
lw $t8, 4($t9)
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
sw $t2, -12($fp)
sw $a0, -0($fp)
# This function will consume the arguments
jal $t8
# Pop fp register from the stack
addiu $sp, $sp, 4
lw $fp, ($sp)
lw $t0, -12($fp)
# saves the return value
move $t0, $v0
lw $t1, -16($fp)
# Moving local_main_Main_internal_2 to local_main_Main_internal_3
move $t1, $t0
lw $t2, -20($fp)
# Moving local_main_Main_internal_3 to local_main_Main_internal_4
move $t2, $t1
# Pop ra register of return function of the stack
addiu $sp, $sp, 4
lw $ra, ($sp)
move $v0, $t2
# Empty all used registers and saves them to memory
sw $t0, -12($fp)
sw $t1, -16($fp)
sw $t2, -20($fp)
jr $ra

.data
type_String: .asciiz "String"
type_Int: .asciiz "Int"
type_Bool: .asciiz "Bool"
type_Object: .asciiz "Object"
type_IO: .asciiz "IO"
type_Main: .asciiz "Main"
methods: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0