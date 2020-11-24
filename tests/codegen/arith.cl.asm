.data
st0: .asciiz "Object"
st1: .asciiz "A"
st2: .asciiz "A2I"
st3: .asciiz "0"
st4: .asciiz "1"
st5: .asciiz "2"
st6: .asciiz "3"
st7: .asciiz "4"
st8: .asciiz "5"
st9: .asciiz "6"
st10: .asciiz "7"
st11: .asciiz "8"
st12: .asciiz "9"
st13: .asciiz "0"
st14: .asciiz "1"
st15: .asciiz "2"
st16: .asciiz "3"
st17: .asciiz "4"
st18: .asciiz "5"
st19: .asciiz "6"
st20: .asciiz "7"
st21: .asciiz "8"
st22: .asciiz "9"
st23: .asciiz ""
st24: .asciiz "-"
st25: .asciiz "+"
st26: .asciiz "0"
st27: .asciiz "-"
st28: .asciiz ""
st29: .asciiz "IO"
st30: .asciiz "String"
st31: .asciiz "Bool"
st32: .asciiz "B"
st33: .asciiz "C"
st34: .asciiz "D"
st35: .asciiz "E"
st36: .asciiz "Main"
st37: .asciiz "\n\tTo add a number to "
st38: .asciiz "...enter a:\n"
st39: .asciiz "\tTo negate "
st40: .asciiz "...enter b:\n"
st41: .asciiz "\tTo find the difference between "
st42: .asciiz "and another number...enter c:\n"
st43: .asciiz "\tTo find the factorial of "
st44: .asciiz "...enter d:\n"
st45: .asciiz "\tTo square "
st46: .asciiz "...enter e:\n"
st47: .asciiz "\tTo cube "
st48: .asciiz "...enter f:\n"
st49: .asciiz "\tTo find out if "
st50: .asciiz "is a multiple of 3...enter g:\n"
st51: .asciiz "\tTo divide "
st52: .asciiz "by 8...enter h:\n"
st53: .asciiz "\tTo get a new number...enter j:\n"
st54: .asciiz "\tTo quit...enter q:\n\n"
st55: .asciiz "\n"
st56: .asciiz "Please enter a number...  "
st57: .asciiz "Class type is now A\n"
st58: .asciiz "Class type is now B\n"
st59: .asciiz "Class type is now C\n"
st60: .asciiz "Class type is now D\n"
st61: .asciiz "Class type is now E\n"
st62: .asciiz "Oooops\n"
st63: .asciiz " "
st64: .asciiz "number "
st65: .asciiz "is even!\n"
st66: .asciiz "is odd!\n"
st67: .asciiz "a"
st68: .asciiz "b"
st69: .asciiz "Oooops\n"
st70: .asciiz "c"
st71: .asciiz "d"
st72: .asciiz "e"
st73: .asciiz "f"
st74: .asciiz "g"
st75: .asciiz "number "
st76: .asciiz "is divisible by 3.\n"
st77: .asciiz "number "
st78: .asciiz "is not divisible by 3.\n"
st79: .asciiz "h"
st80: .asciiz "number "
st81: .asciiz "is equal to "
st82: .asciiz "times 8 with a remainder of "
st83: .asciiz "\n"
st84: .asciiz "j"
st85: .asciiz "q"
Objectclase: .word f0,f3,f2,f4
Aclase: .word f5,f6,f2,f4,f7,f8,f9,f10,f11,f12,f13
A2Iclase: .word f14,f15,f2,f4,f16,f17,f18,f19,f20,f21
IOclase: .word f22,f23,f2,f4,f24,f25,f26,f27
Stringclase: .word f28,f29,f2,f4,f30,f31,f32
Boolclase: .word f33,f34,f2,f4
Bclase: .word f35,f36,f2,f4,f7,f8,f9,f10,f11,f12,f37
Cclase: .word f38,f39,f2,f4,f7,f8,f9,f10,f11,f12,f41,f40
Dclase: .word f42,f43,f2,f4,f7,f8,f9,f10,f11,f12,f37,f44
Eclase: .word f45,f46,f2,f4,f7,f8,f9,f10,f11,f12,f37,f44,f47
Mainclase: .word f48,f49,f2,f4,f24,f25,f26,f27,f50,f51,f52,f53,f54,f55,f56
.text
f0:
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 4
jr $ra
f3:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st0
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f4:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
li $t1,0
addi $sp ,$sp, -4
lw $ra, 0($sp)
jal .Object.Copy
sw $ra, 0($sp)
addi $sp ,$sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f2:
addi $sp, $sp, -8
sw $ra, 0($sp)
jal .Object.abort
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f5:
addi $sp, $sp, -12
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f6:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st1
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f7:
addi $sp, $sp, -8
sw $ra, 0($sp)
lw $t0,4($a0)
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f8:
addi $sp, $sp, -16
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra
f9:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f10:
addi $sp, $sp, -36
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
move $t0,$a2
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
add $v0, $t0, $t1
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Bclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 36
jr $ra
f11:
addi $sp, $sp, -32
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
not $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 32
jr $ra
f12:
addi $sp, $sp, -88
sw $ra, 0($sp)
move $t0,$a2
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
slt $v0, $t0, $t1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl0
move $t0,$a2
move $v0, $t0
sw $v0,52($sp)
move $t0,$a1
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
sub $v0, $t0, $t1
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,80($sp)
b Lbl1
Lbl0:
move $t0,$a1
move $v0, $t0
sw $v0,24($sp)
move $t0,$a2
move $v0, $t0
sw $v0,28($sp)
lw $t0,24($sp)
lw $t1,28($sp)
sub $v0, $t0, $t1
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,80($sp)
Lbl1:
lw $t0,80($sp)
move $v0, $t0
sw $v0,84($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 88
jr $ra
f13:
addi $sp, $sp, -96
sw $ra, 0($sp)
li $t0,1
move $v0, $t0
sw $v0,8($sp)
li $t0,1
move $v0, $t0
sw $v0,16($sp)
Lbl2:
lw $t0,12($sp)
move $v0, $t0
sw $v0,20($sp)
move $t0,$a1
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
lw $t1,24($sp)
sle $v0, $t0, $t1
sw $v0,32($sp)
lw $t0,32($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1sw $v0,40($sp)
lw $t0,40($sp)
bgtz $t0, Lbl3
lw $t0,4($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
mult $t0, $t1
mflo $v0
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,60($sp)
li $t0,1
move $v0, $t0
sw $v0,64($sp)
lw $t0,60($sp)
lw $t1,64($sp)
add $v0, $t0, $t1
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,12($sp)
b Lbl2
Lbl3:
li $t0,0
move $v0, $t0
sw $v0,80($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,84($sp)
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 96
jr $ra
f14:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f15:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st2
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f16:
addi $sp, $sp, -336
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
la $v0, st3
sw $v0,12($sp)
lw $t0,4($sp)
lw $t1,12($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,20($sp)
lw $t0,20($sp)
bgtz $t0, Lbl22
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
la $v0, st4
sw $v0,36($sp)
lw $t0,28($sp)
lw $t1,36($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,44($sp)
lw $t0,44($sp)
bgtz $t0, Lbl20
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
la $v0, st5
sw $v0,60($sp)
lw $t0,52($sp)
lw $t1,60($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,68($sp)
lw $t0,68($sp)
bgtz $t0, Lbl18
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
la $v0, st6
sw $v0,84($sp)
lw $t0,76($sp)
lw $t1,84($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,92($sp)
lw $t0,92($sp)
bgtz $t0, Lbl16
move $t0,$a1
move $v0, $t0
sw $v0,100($sp)
la $v0, st7
sw $v0,108($sp)
lw $t0,100($sp)
lw $t1,108($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,116($sp)
lw $t0,116($sp)
bgtz $t0, Lbl14
move $t0,$a1
move $v0, $t0
sw $v0,124($sp)
la $v0, st8
sw $v0,132($sp)
lw $t0,124($sp)
lw $t1,132($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,140($sp)
lw $t0,140($sp)
bgtz $t0, Lbl12
move $t0,$a1
move $v0, $t0
sw $v0,148($sp)
la $v0, st9
sw $v0,156($sp)
lw $t0,148($sp)
lw $t1,156($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,164($sp)
lw $t0,164($sp)
bgtz $t0, Lbl10
move $t0,$a1
move $v0, $t0
sw $v0,172($sp)
la $v0, st10
sw $v0,180($sp)
lw $t0,172($sp)
lw $t1,180($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,188($sp)
lw $t0,188($sp)
bgtz $t0, Lbl8
move $t0,$a1
move $v0, $t0
sw $v0,196($sp)
la $v0, st11
sw $v0,204($sp)
lw $t0,196($sp)
lw $t1,204($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,212($sp)
lw $t0,212($sp)
bgtz $t0, Lbl6
move $t0,$a1
move $v0, $t0
sw $v0,220($sp)
la $v0, st12
sw $v0,228($sp)
lw $t0,220($sp)
lw $t1,228($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,236($sp)
lw $t0,236($sp)
bgtz $t0, Lbl4
move $t0,$a0
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,8($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,248($sp)
li $t0,0
move $v0, $t0
sw $v0,252($sp)
lw $t0,252($sp)
move $v0, $t0
sw $v0,256($sp)
b Lbl5
Lbl4:
li $t0,9
move $v0, $t0
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,256($sp)
Lbl5:
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
lw $t0,260($sp)
move $v0, $t0
sw $v0,264($sp)
b Lbl7
Lbl6:
li $t0,8
move $v0, $t0
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,264($sp)
Lbl7:
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
b Lbl9
Lbl8:
li $t0,7
move $v0, $t0
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,272($sp)
Lbl9:
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,280($sp)
b Lbl11
Lbl10:
li $t0,6
move $v0, $t0
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,280($sp)
Lbl11:
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
b Lbl13
Lbl12:
li $t0,5
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,288($sp)
Lbl13:
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
b Lbl15
Lbl14:
li $t0,4
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,296($sp)
Lbl15:
lw $t0,296($sp)
move $v0, $t0
sw $v0,300($sp)
lw $t0,300($sp)
move $v0, $t0
sw $v0,304($sp)
b Lbl17
Lbl16:
li $t0,3
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,304($sp)
Lbl17:
lw $t0,304($sp)
move $v0, $t0
sw $v0,308($sp)
lw $t0,308($sp)
move $v0, $t0
sw $v0,312($sp)
b Lbl19
Lbl18:
li $t0,2
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,312($sp)
Lbl19:
lw $t0,312($sp)
move $v0, $t0
sw $v0,316($sp)
lw $t0,316($sp)
move $v0, $t0
sw $v0,320($sp)
b Lbl21
Lbl20:
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,320($sp)
Lbl21:
lw $t0,320($sp)
move $v0, $t0
sw $v0,324($sp)
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
b Lbl23
Lbl22:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,328($sp)
Lbl23:
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 336
jr $ra
f17:
addi $sp, $sp, -340
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl42
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
li $t0,1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,40($sp)
lw $t0,40($sp)
bgtz $t0, Lbl40
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
li $t0,2
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl38
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
li $t0,3
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
lw $t1,80($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,88($sp)
lw $t0,88($sp)
bgtz $t0, Lbl36
move $t0,$a1
move $v0, $t0
sw $v0,100($sp)
li $t0,4
move $v0, $t0
sw $v0,104($sp)
lw $t0,100($sp)
lw $t1,104($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,112($sp)
lw $t0,112($sp)
bgtz $t0, Lbl34
move $t0,$a1
move $v0, $t0
sw $v0,124($sp)
li $t0,5
move $v0, $t0
sw $v0,128($sp)
lw $t0,124($sp)
lw $t1,128($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,136($sp)
lw $t0,136($sp)
bgtz $t0, Lbl32
move $t0,$a1
move $v0, $t0
sw $v0,148($sp)
li $t0,6
move $v0, $t0
sw $v0,152($sp)
lw $t0,148($sp)
lw $t1,152($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,160($sp)
lw $t0,160($sp)
bgtz $t0, Lbl30
move $t0,$a1
move $v0, $t0
sw $v0,172($sp)
li $t0,7
move $v0, $t0
sw $v0,176($sp)
lw $t0,172($sp)
lw $t1,176($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,184($sp)
lw $t0,184($sp)
bgtz $t0, Lbl28
move $t0,$a1
move $v0, $t0
sw $v0,196($sp)
li $t0,8
move $v0, $t0
sw $v0,200($sp)
lw $t0,196($sp)
lw $t1,200($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,208($sp)
lw $t0,208($sp)
bgtz $t0, Lbl26
move $t0,$a1
move $v0, $t0
sw $v0,220($sp)
li $t0,9
move $v0, $t0
sw $v0,224($sp)
lw $t0,220($sp)
lw $t1,224($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,232($sp)
lw $t0,232($sp)
bgtz $t0, Lbl24
move $t0,$a0
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,8($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,248($sp)
la $v0, st23
sw $v0,256($sp)
lw $t0,256($sp)
move $v0, $t0
sw $v0,260($sp)
b Lbl25
Lbl24:
la $v0, st22
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,260($sp)
Lbl25:
lw $t0,260($sp)
move $v0, $t0
sw $v0,264($sp)
lw $t0,264($sp)
move $v0, $t0
sw $v0,268($sp)
b Lbl27
Lbl26:
la $v0, st21
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,268($sp)
Lbl27:
lw $t0,268($sp)
move $v0, $t0
sw $v0,272($sp)
lw $t0,272($sp)
move $v0, $t0
sw $v0,276($sp)
b Lbl29
Lbl28:
la $v0, st20
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,276($sp)
Lbl29:
lw $t0,276($sp)
move $v0, $t0
sw $v0,280($sp)
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
b Lbl31
Lbl30:
la $v0, st19
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,284($sp)
Lbl31:
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
b Lbl33
Lbl32:
la $v0, st18
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,292($sp)
Lbl33:
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,296($sp)
move $v0, $t0
sw $v0,300($sp)
b Lbl35
Lbl34:
la $v0, st17
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,300($sp)
Lbl35:
lw $t0,300($sp)
move $v0, $t0
sw $v0,304($sp)
lw $t0,304($sp)
move $v0, $t0
sw $v0,308($sp)
b Lbl37
Lbl36:
la $v0, st16
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,308($sp)
Lbl37:
lw $t0,308($sp)
move $v0, $t0
sw $v0,312($sp)
lw $t0,312($sp)
move $v0, $t0
sw $v0,316($sp)
b Lbl39
Lbl38:
la $v0, st15
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,316($sp)
Lbl39:
lw $t0,316($sp)
move $v0, $t0
sw $v0,320($sp)
lw $t0,320($sp)
move $v0, $t0
sw $v0,324($sp)
b Lbl41
Lbl40:
la $v0, st14
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,324($sp)
Lbl41:
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
b Lbl43
Lbl42:
la $v0, st13
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,332($sp)
Lbl43:
lw $t0,332($sp)
move $v0, $t0
sw $v0,336($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 340
jr $ra
f18:
addi $sp, $sp, -216
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
li $t0,0
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,20($sp)
lw $t0,20($sp)
bgtz $t0, Lbl48
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,0
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,40($sp)
la $v0, st24
sw $v0,48($sp)
lw $t0,40($sp)
lw $t1,48($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,56($sp)
lw $t0,56($sp)
bgtz $t0, Lbl46
move $t0,$a1
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,0
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,120($sp)
la $v0, st25
sw $v0,128($sp)
lw $t0,120($sp)
lw $t1,128($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,136($sp)
lw $t0,136($sp)
bgtz $t0, Lbl44
move $t0,$a0
move $v0, $t0
sw $v0,180($sp)
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,184($sp)
lw $t0,184($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,188($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
b Lbl45
Lbl44:
move $t0,$a0
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,148($sp)
lw $t0,148($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,156($sp)
li $t0,1
move $v0, $t0
sw $v0,160($sp)
lw $t0,156($sp)
lw $t1,160($sp)
sub $v0, $t0, $t1
sw $v0,168($sp)
lw $t0,168($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,144($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,172($sp)
lw $t0,172($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,140($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,176($sp)
lw $t0,176($sp)
move $v0, $t0
sw $v0,192($sp)
Lbl45:
lw $t0,192($sp)
move $v0, $t0
sw $v0,196($sp)
lw $t0,196($sp)
move $v0, $t0
sw $v0,200($sp)
b Lbl47
Lbl46:
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
li $t0,1
move $v0, $t0
sw $v0,80($sp)
lw $t0,76($sp)
lw $t1,80($sp)
sub $v0, $t0, $t1
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
not $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,200($sp)
Lbl47:
lw $t0,200($sp)
move $v0, $t0
sw $v0,204($sp)
lw $t0,204($sp)
move $v0, $t0
sw $v0,208($sp)
b Lbl49
Lbl48:
li $t0,0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,208($sp)
Lbl49:
lw $t0,208($sp)
move $v0, $t0
sw $v0,212($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 216
jr $ra
f19:
addi $sp, $sp, -132
sw $ra, 0($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
li $t0,0
move $v0, $t0
sw $v0,28($sp)
Lbl50:
lw $t0,24($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
lw $t1,36($sp)
slt $v0, $t0, $t1
sw $v0,44($sp)
lw $t0,44($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1sw $v0,52($sp)
lw $t0,52($sp)
bgtz $t0, Lbl51
lw $t0,4($sp)
move $v0, $t0
sw $v0,56($sp)
li $t0,10
move $v0, $t0
sw $v0,60($sp)
lw $t0,56($sp)
lw $t1,60($sp)
mult $t0, $t1
mflo $v0
sw $v0,68($sp)
move $t0,$a0
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $t0,68($sp)
lw $t1,92($sp)
add $v0, $t0, $t1
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,104($sp)
li $t0,1
move $v0, $t0
sw $v0,108($sp)
lw $t0,104($sp)
lw $t1,108($sp)
add $v0, $t0, $t1
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,24($sp)
b Lbl50
Lbl51:
li $t0,0
move $v0, $t0
sw $v0,124($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,128($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 132
jr $ra
f20:
addi $sp, $sp, -116
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl54
li $t0,0
move $v0, $t0
sw $v0,28($sp)
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
slt $v0, $t0, $t1
sw $v0,40($sp)
lw $t0,40($sp)
bgtz $t0, Lbl52
la $v0, st27
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
li $t0,1
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
not $v0, $t0
sw $v0,80($sp)
lw $t0,68($sp)
lw $t1,80($sp)
mult $t0, $t1
mflo $v0
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl53
Lbl52:
move $t0,$a0
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl53:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
b Lbl55
Lbl54:
la $v0, st26
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,108($sp)
Lbl55:
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 116
jr $ra
f21:
addi $sp, $sp, -108
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl56
move $t0,$a1
move $v0, $t0
sw $v0,32($sp)
li $t0,10
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
lw $t1,36($sp)
div $t0, $t1
mflo $v0
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,64($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,68($sp)
li $t0,10
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
lw $t1,72($sp)
mult $t0, $t1
mflo $v0
sw $v0,80($sp)
lw $t0,64($sp)
lw $t1,80($sp)
sub $v0, $t0, $t1
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl57
Lbl56:
la $v0, st28
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl57:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 108
jr $ra
f22:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f23:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st29
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f24:
addi $sp, $sp, -8
sw $ra, 0($sp)
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.out_string
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
move $a1,$t0
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f25:
addi $sp, $sp, -8
sw $ra, 0($sp)
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.out_int
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
move $a1,$t0
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f26:
addi $sp, $sp, -8
sw $ra, 0($sp)
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.in_string
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f27:
addi $sp, $sp, -8
sw $ra, 0($sp)
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .IO.in_string
lw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f28:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f29:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st30
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f30:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .Str.stringlengthlw $a0, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f31:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
move $t1,$a1
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringconcatlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f32:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
move $t1,$a1
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringconcatlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f33:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Objectclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f34:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st31
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f35:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Aclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f36:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st32
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f37:
addi $sp, $sp, -36
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
move $t0,$a1
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
mult $t0, $t1
mflo $v0
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 36
jr $ra
f38:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f39:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st33
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f40:
addi $sp, $sp, -32
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
not $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 32
jr $ra
f41:
addi $sp, $sp, -48
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
move $t0,$a1
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
mult $t0, $t1
mflo $v0
sw $v0,20($sp)
move $t0,$a1
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
lw $t1,24($sp)
mult $t0, $t1
mflo $v0
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,36($sp)
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 48
jr $ra
f42:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f43:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st34
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f44:
addi $sp, $sp, -164
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
li $t0,0
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
lw $t1,16($sp)
slt $v0, $t0, $t1
sw $v0,24($sp)
lw $t0,24($sp)
bgtz $t0, Lbl64
li $t0,0
move $v0, $t0
sw $v0,48($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,48($sp)
lw $t1,52($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,60($sp)
lw $t0,60($sp)
bgtz $t0, Lbl62
li $t0,1
move $v0, $t0
sw $v0,68($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
lw $t1,72($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,80($sp)
lw $t0,80($sp)
bgtz $t0, Lbl60
li $t0,2
move $v0, $t0
sw $v0,88($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,92($sp)
lw $t0,88($sp)
lw $t1,92($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,100($sp)
lw $t0,100($sp)
bgtz $t0, Lbl58
move $t0,$a0
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,112($sp)
li $t0,3
move $v0, $t0
sw $v0,116($sp)
lw $t0,112($sp)
lw $t1,116($sp)
sub $v0, $t0, $t1
sw $v0,124($sp)
lw $t0,124($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,132($sp)
b Lbl59
Lbl58:
li $t0,1
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,132($sp)
Lbl59:
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
b Lbl61
Lbl60:
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,140($sp)
Lbl61:
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
b Lbl63
Lbl62:
move $t0, zero
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,148($sp)
Lbl63:
lw $t0,148($sp)
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
move $v0, $t0
sw $v0,156($sp)
b Lbl65
Lbl64:
move $t0,$a0
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
not $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,156($sp)
Lbl65:
lw $t0,156($sp)
move $v0, $t0
sw $v0,160($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 164
jr $ra
f45:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Dclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f46:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st35
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f47:
addi $sp, $sp, -36
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
li $t0,8
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
div $t0, $t1
mflo $v0
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 36
jr $ra
f48:
addi $sp, $sp, -12
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,IOclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,4($a0)
li $t0,0
move $v0, $t0
sw $v0,8($a0)
li $t0,0
move $v0, $t0
sw $v0,12($a0)
move $t0, zero
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,16($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f49:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st36
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f50:
addi $sp, $sp, -396
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st37
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st38
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st39
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,60($sp)
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,72($sp)
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st40
sw $v0,84($sp)
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,88($sp)
move $t0,$a0
move $v0, $t0
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st41
sw $v0,100($sp)
lw $t0,100($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,104($sp)
move $t0,$a0
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,116($sp)
move $t0,$a0
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st42
sw $v0,128($sp)
lw $t0,128($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,120($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,132($sp)
move $t0,$a0
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st43
sw $v0,144($sp)
lw $t0,144($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,136($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,148($sp)
move $t0,$a0
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,156($sp)
lw $t0,156($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,160($sp)
move $t0,$a0
move $v0, $t0
sw $v0,164($sp)
lw $t0,164($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st44
sw $v0,172($sp)
lw $t0,172($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,164($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,176($sp)
move $t0,$a0
move $v0, $t0
sw $v0,180($sp)
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st45
sw $v0,188($sp)
lw $t0,188($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,192($sp)
move $t0,$a0
move $v0, $t0
sw $v0,196($sp)
lw $t0,196($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,200($sp)
lw $t0,200($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,196($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,204($sp)
move $t0,$a0
move $v0, $t0
sw $v0,208($sp)
lw $t0,208($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st46
sw $v0,216($sp)
lw $t0,216($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,208($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,220($sp)
move $t0,$a0
move $v0, $t0
sw $v0,224($sp)
lw $t0,224($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st47
sw $v0,232($sp)
lw $t0,232($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,224($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,236($sp)
move $t0,$a0
move $v0, $t0
sw $v0,240($sp)
lw $t0,240($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,240($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,248($sp)
move $t0,$a0
move $v0, $t0
sw $v0,252($sp)
lw $t0,252($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st48
sw $v0,260($sp)
lw $t0,260($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,252($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,264($sp)
move $t0,$a0
move $v0, $t0
sw $v0,268($sp)
lw $t0,268($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st49
sw $v0,276($sp)
lw $t0,276($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,268($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,280($sp)
move $t0,$a0
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,288($sp)
lw $t0,288($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,284($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,292($sp)
move $t0,$a0
move $v0, $t0
sw $v0,296($sp)
lw $t0,296($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st50
sw $v0,304($sp)
lw $t0,304($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,296($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,308($sp)
move $t0,$a0
move $v0, $t0
sw $v0,312($sp)
lw $t0,312($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st51
sw $v0,320($sp)
lw $t0,320($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,312($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,324($sp)
move $t0,$a0
move $v0, $t0
sw $v0,328($sp)
lw $t0,328($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,332($sp)
lw $t0,332($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,328($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,336($sp)
move $t0,$a0
move $v0, $t0
sw $v0,340($sp)
lw $t0,340($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st52
sw $v0,348($sp)
lw $t0,348($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,340($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,352($sp)
move $t0,$a0
move $v0, $t0
sw $v0,356($sp)
lw $t0,356($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st53
sw $v0,364($sp)
lw $t0,364($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,356($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,368($sp)
move $t0,$a0
move $v0, $t0
sw $v0,372($sp)
lw $t0,372($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st54
sw $v0,380($sp)
lw $t0,380($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,372($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,384($sp)
move $t0,$a0
move $v0, $t0
sw $v0,388($sp)
lw $t0,388($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,388($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,392($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 396
jr $ra
f51:
addi $sp, $sp, -44
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st55
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st56
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
move $t0,$a0
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,40($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 44
jr $ra
f52:
addi $sp, $sp, -36
sw $ra, 0($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
syscall
la $t0, A2Iclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 36
jr $ra
f53:
addi $sp, $sp, -136
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,12($sp)
li $t0,0
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
lw $t1,16($sp)
slt $v0, $t0, $t1
sw $v0,24($sp)
lw $t0,24($sp)
bgtz $t0, Lbl70
li $t0,0
move $v0, $t0
sw $v0,48($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,48($sp)
lw $t1,52($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,60($sp)
lw $t0,60($sp)
bgtz $t0, Lbl68
li $t0,1
move $v0, $t0
sw $v0,68($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,68($sp)
lw $t1,72($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,80($sp)
lw $t0,80($sp)
bgtz $t0, Lbl66
move $t0,$a0
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,92($sp)
li $t0,2
move $v0, $t0
sw $v0,96($sp)
lw $t0,92($sp)
lw $t1,96($sp)
sub $v0, $t0, $t1
sw $v0,104($sp)
lw $t0,104($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
b Lbl67
Lbl66:
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,112($sp)
Lbl67:
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
b Lbl69
Lbl68:
move $t0, zero
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,120($sp)
Lbl69:
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
move $v0, $t0
sw $v0,128($sp)
b Lbl71
Lbl70:
move $t0,$a0
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
not $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,128($sp)
Lbl71:
lw $t0,128($sp)
move $v0, $t0
sw $v0,132($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 136
jr $ra
f54:
addi $sp, $sp, -236
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $v0, 1
sw $v0,24($sp)
lw $t0,24($sp)
bgtz $t0, var#548
lw $t0,4($sp)
move $v0, $t0
sw $v0,20($sp)
move $t0,$a0
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st57
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,8($sp)
var#548:
li $v0, 1
sw $v0,60($sp)
lw $t0,60($sp)
bgtz $t0, var#555
lw $t0,4($sp)
move $v0, $t0
sw $v0,56($sp)
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st58
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,8($sp)
var#555:
li $v0, 1
sw $v0,96($sp)
lw $t0,96($sp)
bgtz $t0, var#562
lw $t0,4($sp)
move $v0, $t0
sw $v0,92($sp)
move $t0,$a0
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st59
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,104($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,8($sp)
var#562:
li $v0, 1
sw $v0,132($sp)
lw $t0,132($sp)
bgtz $t0, var#569
lw $t0,4($sp)
move $v0, $t0
sw $v0,128($sp)
move $t0,$a0
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st60
sw $v0,148($sp)
lw $t0,148($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,140($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,152($sp)
lw $t0,152($sp)
move $v0, $t0
sw $v0,156($sp)
lw $t0,156($sp)
move $v0, $t0
sw $v0,8($sp)
var#569:
li $v0, 1
sw $v0,168($sp)
lw $t0,168($sp)
bgtz $t0, var#576
lw $t0,4($sp)
move $v0, $t0
sw $v0,164($sp)
move $t0,$a0
move $v0, $t0
sw $v0,176($sp)
lw $t0,176($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st61
sw $v0,184($sp)
lw $t0,184($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,176($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,188($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,8($sp)
var#576:
li $v0, 1
sw $v0,204($sp)
lw $t0,204($sp)
bgtz $t0, var#583
lw $t0,4($sp)
move $v0, $t0
sw $v0,200($sp)
move $t0,$a0
move $v0, $t0
sw $v0,212($sp)
lw $t0,212($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st62
sw $v0,220($sp)
lw $t0,220($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,212($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,224($sp)
lw $t0,224($sp)
move $v0, $t0
sw $v0,228($sp)
lw $t0,228($sp)
move $v0, $t0
sw $v0,8($sp)
var#583:
var#545:
lw $t0,8($sp)
move $v0, $t0
sw $v0,232($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 236
jr $ra
f55:
addi $sp, $sp, -52
sw $ra, 0($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
syscall
la $t0, A2Iclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,32($sp)
move $t0,$a0
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st63
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,48($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 52
jr $ra
f56:
addi $sp, $sp, -1004
sw $ra, 0($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($sp)
Lbl72:
lw $t0,892($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1sw $v0,20($sp)
lw $t0,20($sp)
bgtz $t0, Lbl73
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st64
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,36($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,48($sp)
move $t0,$a0
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl74
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st66
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl75
Lbl74:
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st65
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl75:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
move $t0,$a0
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,116($sp)
move $t0,$a0
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,124($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
move $v0, $t0
sw $v0,132($sp)
la $v0, st67
sw $v0,140($sp)
lw $t0,132($sp)
lw $t1,140($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,148($sp)
lw $t0,148($sp)
bgtz $t0, Lbl96
lw $t0,120($sp)
move $v0, $t0
sw $v0,196($sp)
la $v0, st68
sw $v0,204($sp)
lw $t0,196($sp)
lw $t1,204($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,212($sp)
lw $t0,212($sp)
bgtz $t0, Lbl94
lw $t0,120($sp)
move $v0, $t0
sw $v0,352($sp)
la $v0, st70
sw $v0,360($sp)
lw $t0,352($sp)
lw $t1,360($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,368($sp)
lw $t0,368($sp)
bgtz $t0, Lbl92
lw $t0,120($sp)
move $v0, $t0
sw $v0,412($sp)
la $v0, st71
sw $v0,420($sp)
lw $t0,412($sp)
lw $t1,420($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,428($sp)
lw $t0,428($sp)
bgtz $t0, Lbl90
lw $t0,120($sp)
move $v0, $t0
sw $v0,448($sp)
la $v0, st72
sw $v0,456($sp)
lw $t0,448($sp)
lw $t1,456($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,464($sp)
lw $t0,464($sp)
bgtz $t0, Lbl88
lw $t0,120($sp)
move $v0, $t0
sw $v0,484($sp)
la $v0, st73
sw $v0,492($sp)
lw $t0,484($sp)
lw $t1,492($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,500($sp)
lw $t0,500($sp)
bgtz $t0, Lbl86
lw $t0,120($sp)
move $v0, $t0
sw $v0,520($sp)
la $v0, st74
sw $v0,528($sp)
lw $t0,520($sp)
lw $t1,528($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,536($sp)
lw $t0,536($sp)
bgtz $t0, Lbl84
lw $t0,120($sp)
move $v0, $t0
sw $v0,652($sp)
la $v0, st79
sw $v0,660($sp)
lw $t0,652($sp)
lw $t1,660($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,668($sp)
lw $t0,668($sp)
bgtz $t0, Lbl82
lw $t0,120($sp)
move $v0, $t0
sw $v0,848($sp)
la $v0, st84
sw $v0,856($sp)
lw $t0,848($sp)
lw $t1,856($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,864($sp)
lw $t0,864($sp)
bgtz $t0, Lbl80
lw $t0,120($sp)
move $v0, $t0
sw $v0,872($sp)
la $v0, st85
sw $v0,880($sp)
lw $t0,872($sp)
lw $t1,880($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparisonlw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,888($sp)
lw $t0,888($sp)
bgtz $t0, Lbl78
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,900($sp)
lw $t0,900($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,904($sp)
lw $t0,904($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,904($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,908($sp)
lw $t0,908($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,900($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,912($sp)
lw $t0,912($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,916($sp)
b Lbl79
Lbl78:
li $t0,1
move $v0, $t0
sw $v0,896($sp)
lw $t0,896($sp)
move $v0, $t0
sw $v0,892($sp)
lw $t0,892($sp)
move $v0, $t0
sw $v0,916($sp)
Lbl79:
lw $t0,916($sp)
move $v0, $t0
sw $v0,920($sp)
lw $t0,920($sp)
move $v0, $t0
sw $v0,924($sp)
b Lbl81
Lbl80:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,868($sp)
lw $t0,868($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,924($sp)
Lbl81:
lw $t0,924($sp)
move $v0, $t0
sw $v0,928($sp)
lw $t0,928($sp)
move $v0, $t0
sw $v0,932($sp)
b Lbl83
Lbl82:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Eclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,676($sp)
lw $t0,676($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,680($sp)
lw $t0,680($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,680($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,684($sp)
lw $t0,684($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,676($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,688($sp)
lw $t0,688($sp)
move $v0, $t0
sw $v0,672($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,696($sp)
lw $t0,696($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,696($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,700($sp)
lw $t0,672($sp)
move $v0, $t0
sw $v0,704($sp)
lw $t0,704($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,704($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,708($sp)
li $t0,8
move $v0, $t0
sw $v0,712($sp)
lw $t0,708($sp)
lw $t1,712($sp)
mult $t0, $t1
mflo $v0
sw $v0,720($sp)
lw $t0,700($sp)
lw $t1,720($sp)
sub $v0, $t0, $t1
sw $v0,728($sp)
move $t0,$a0
move $v0, $t0
sw $v0,732($sp)
lw $t0,732($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st80
sw $v0,740($sp)
lw $t0,740($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,732($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,744($sp)
move $t0,$a0
move $v0, $t0
sw $v0,748($sp)
lw $t0,748($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,752($sp)
lw $t0,752($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,748($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,756($sp)
move $t0,$a0
move $v0, $t0
sw $v0,760($sp)
lw $t0,760($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st81
sw $v0,768($sp)
lw $t0,768($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,760($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,772($sp)
move $t0,$a0
move $v0, $t0
sw $v0,776($sp)
lw $t0,776($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,672($sp)
move $v0, $t0
sw $v0,780($sp)
lw $t0,780($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,776($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,784($sp)
move $t0,$a0
move $v0, $t0
sw $v0,788($sp)
lw $t0,788($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st82
sw $v0,796($sp)
lw $t0,796($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,788($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,800($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,4
syscall
la $t0, A2Iclase
sw $t0, 0($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,804($sp)
move $t0,$a0
move $v0, $t0
sw $v0,808($sp)
lw $t0,808($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,268($sp)
move $v0, $t0
sw $v0,812($sp)
lw $t0,812($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,692($sp)
move $v0, $t0
sw $v0,816($sp)
lw $t0,816($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,812($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,820($sp)
lw $t0,820($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,808($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,824($sp)
move $t0,$a0
move $v0, $t0
sw $v0,828($sp)
lw $t0,828($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st83
sw $v0,836($sp)
lw $t0,836($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,828($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,840($sp)
lw $t0,672($sp)
move $v0, $t0
sw $v0,844($sp)
lw $t0,844($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,932($sp)
Lbl83:
lw $t0,932($sp)
move $v0, $t0
sw $v0,936($sp)
lw $t0,936($sp)
move $v0, $t0
sw $v0,940($sp)
b Lbl85
Lbl84:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,540($sp)
lw $t0,540($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,544($sp)
lw $t0,544($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,544($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,548($sp)
lw $t0,548($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,540($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,552($sp)
lw $t0,552($sp)
bgtz $t0, Lbl76
move $t0,$a0
move $v0, $t0
sw $v0,600($sp)
lw $t0,600($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st77
sw $v0,608($sp)
lw $t0,608($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,600($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,612($sp)
move $t0,$a0
move $v0, $t0
sw $v0,616($sp)
lw $t0,616($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,620($sp)
lw $t0,620($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,616($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,624($sp)
move $t0,$a0
move $v0, $t0
sw $v0,628($sp)
lw $t0,628($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st78
sw $v0,636($sp)
lw $t0,636($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,628($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,640($sp)
lw $t0,640($sp)
move $v0, $t0
sw $v0,644($sp)
b Lbl77
Lbl76:
move $t0,$a0
move $v0, $t0
sw $v0,556($sp)
lw $t0,556($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st75
sw $v0,564($sp)
lw $t0,564($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,556($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,568($sp)
move $t0,$a0
move $v0, $t0
sw $v0,572($sp)
lw $t0,572($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,576($sp)
lw $t0,576($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,572($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,580($sp)
move $t0,$a0
move $v0, $t0
sw $v0,584($sp)
lw $t0,584($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st76
sw $v0,592($sp)
lw $t0,592($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,584($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,596($sp)
lw $t0,596($sp)
move $v0, $t0
sw $v0,644($sp)
Lbl77:
lw $t0,644($sp)
move $v0, $t0
sw $v0,648($sp)
lw $t0,648($sp)
move $v0, $t0
sw $v0,940($sp)
Lbl85:
lw $t0,940($sp)
move $v0, $t0
sw $v0,944($sp)
lw $t0,944($sp)
move $v0, $t0
sw $v0,948($sp)
b Lbl87
Lbl86:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,504($sp)
lw $t0,504($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,508($sp)
lw $t0,508($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,508($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,512($sp)
lw $t0,512($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,504($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Cclase
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,516($sp)
lw $t0,516($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,948($sp)
Lbl87:
lw $t0,948($sp)
move $v0, $t0
sw $v0,952($sp)
lw $t0,952($sp)
move $v0, $t0
sw $v0,956($sp)
b Lbl89
Lbl88:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,468($sp)
lw $t0,468($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,472($sp)
lw $t0,472($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,472($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,476($sp)
lw $t0,476($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,468($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bclase
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,480($sp)
lw $t0,480($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,956($sp)
Lbl89:
lw $t0,956($sp)
move $v0, $t0
sw $v0,960($sp)
lw $t0,960($sp)
move $v0, $t0
sw $v0,964($sp)
b Lbl91
Lbl90:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Cclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,432($sp)
lw $t0,432($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,436($sp)
lw $t0,436($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,436($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,440($sp)
lw $t0,440($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,432($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Aclase
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,444($sp)
lw $t0,444($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,964($sp)
Lbl91:
lw $t0,964($sp)
move $v0, $t0
sw $v0,968($sp)
lw $t0,968($sp)
move $v0, $t0
sw $v0,972($sp)
b Lbl93
Lbl92:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,372($sp)
lw $t0,372($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a0
move $v0, $t0
sw $v0,376($sp)
lw $t0,376($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,376($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,380($sp)
lw $t0,380($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,372($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,384($sp)
lw $t0,384($sp)
move $v0, $t0
sw $v0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Dclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,388($sp)
lw $t0,388($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,392($sp)
lw $t0,392($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,392($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,396($sp)
lw $t0,396($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,152($sp)
move $v0, $t0
sw $v0,400($sp)
lw $t0,400($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,400($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,404($sp)
lw $t0,404($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,388($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,408($sp)
lw $t0,408($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,972($sp)
Lbl93:
lw $t0,972($sp)
move $v0, $t0
sw $v0,976($sp)
lw $t0,976($sp)
move $v0, $t0
sw $v0,980($sp)
b Lbl95
Lbl94:
lw $t0,4($sp)
move $v0, $t0
sw $v0,216($sp)
li $v0, 1
sw $v0,236($sp)
lw $t0,236($sp)
bgtz $t0, var#648
lw $t0,216($sp)
move $v0, $t0
sw $v0,232($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,232($sp)
move $v0, $t0
sw $v0,248($sp)
lw $t0,248($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,248($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,252($sp)
lw $t0,252($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,244($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,256($sp)
lw $t0,256($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,260($sp)
lw $t0,260($sp)
move $v0, $t0
sw $v0,220($sp)
var#648:
li $v0, 1
sw $v0,272($sp)
lw $t0,272($sp)
bgtz $t0, var#656
lw $t0,216($sp)
move $v0, $t0
sw $v0,268($sp)
lw $t0,268($sp)
move $v0, $t0
sw $v0,280($sp)
lw $t0,280($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,268($sp)
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,284($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,288($sp)
lw $t0,288($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,280($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,292($sp)
lw $t0,292($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,296($sp)
move $v0, $t0
sw $v0,220($sp)
var#656:
li $v0, 1
sw $v0,308($sp)
lw $t0,308($sp)
bgtz $t0, var#664
lw $t0,216($sp)
move $v0, $t0
sw $v0,304($sp)
move $t0,$a0
move $v0, $t0
sw $v0,316($sp)
lw $t0,316($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st69
sw $v0,324($sp)
lw $t0,324($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,316($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,328($sp)
move $t0,$a0
move $v0, $t0
sw $v0,332($sp)
lw $t0,332($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,332($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,8($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,336($sp)
li $t0,0
move $v0, $t0
sw $v0,340($sp)
lw $t0,340($sp)
move $v0, $t0
sw $v0,344($sp)
lw $t0,344($sp)
move $v0, $t0
sw $v0,220($sp)
var#664:
var#645:
lw $t0,220($sp)
move $v0, $t0
sw $v0,348($sp)
lw $t0,348($sp)
move $v0, $t0
sw $v0,980($sp)
Lbl95:
lw $t0,980($sp)
move $v0, $t0
sw $v0,984($sp)
lw $t0,984($sp)
move $v0, $t0
sw $v0,988($sp)
b Lbl97
Lbl96:
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Aclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,156($sp)
lw $t0,156($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a0
move $v0, $t0
sw $v0,160($sp)
lw $t0,160($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,160($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,164($sp)
lw $t0,164($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,156($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,8
syscall
la $t0, Bclase
sw $t0, 0($v0)
sw zero, 4($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,172($sp)
lw $t0,172($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,176($sp)
lw $t0,176($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,176($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,180($sp)
lw $t0,180($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,152($sp)
move $v0, $t0
sw $v0,184($sp)
lw $t0,184($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,184($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,188($sp)
lw $t0,188($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,172($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,988($sp)
Lbl97:
lw $t0,988($sp)
move $v0, $t0
sw $v0,992($sp)
b Lbl72
Lbl73:
li $t0,0
move $v0, $t0
sw $v0,1000($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 1004
jr $ra
