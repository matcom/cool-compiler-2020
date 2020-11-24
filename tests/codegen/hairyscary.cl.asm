.data
st0: .asciiz "Object"
st1: .asciiz "Main"
st2: .asciiz "do nothing"
st3: .asciiz "IO"
st4: .asciiz "String"
st5: .asciiz "Bool"
st6: .asciiz "Bazz"
st7: .asciiz "Foo"
st8: .asciiz "Razz"
st9: .asciiz "Bar"
Objectclase: .word f0,f3,f2,f4
Mainclase: .word f5,f6,f2,f4,f7
IOclase: .word f8,f9,f2,f4,f10,f11,f12,f13
Stringclase: .word f14,f15,f2,f4,f16,f17,f18
Boolclase: .word f19,f20,f2,f4
Bazzclase: .word f21,f22,f2,f4,f10,f11,f12,f13,f23,f24
Fooclase: .word f25,f26,f2,f4,f10,f11,f12,f13,f23,f27
Razzclase: .word f28,f29,f2,f4,f10,f11,f12,f13,f23,f27
Barclase: .word f30,f31,f2,f4,f10,f11,f12,f13,f23,f27
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
addi $sp, $sp, -24
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
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,16
syscall
la $t0, Bazzclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,24
syscall
la $t0, Fooclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,8($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,32
syscall
la $t0, Razzclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
sw zero, 24($v0)
sw zero, 28($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,12($a0)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
sw zero, 24($v0)
sw zero, 28($v0)
sw zero, 32($v0)
sw zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,16($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 24
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
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st2
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f8:
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
f9:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st3
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f10:
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
f11:
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
f12:
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
f13:
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
la $v0, st4
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f16:
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
f17:
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
f18:
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
f19:
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
f20:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st5
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f21:
addi $sp, $sp, -120
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
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
move $v0, $t0
sw $v0,4($a0)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
li $v0, 1
sw $v0,32($sp)
lw $t0,32($sp)
bgtz $t0, var#22
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,24
syscall
la $t0, Fooclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,16($sp)
var#22:
li $v0, 1
sw $v0,52($sp)
lw $t0,52($sp)
bgtz $t0, var#27
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
sw zero, 24($v0)
sw zero, 28($v0)
sw zero, 32($v0)
sw zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,16($sp)
var#27:
li $v0, 1
sw $v0,72($sp)
lw $t0,72($sp)
bgtz $t0, var#32
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,32
syscall
la $t0, Razzclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
sw zero, 24($v0)
sw zero, 28($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,16($sp)
var#32:
li $v0, 1
sw $v0,92($sp)
lw $t0,92($sp)
bgtz $t0, var#37
lw $t0,12($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,16($sp)
var#37:
var#19:
lw $t0,16($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,8($a0)
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,12($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 120
jr $ra
f22:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st6
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f23:
addi $sp, $sp, -20
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
li $t0,0
move $v0, $t0
sw $v0,16($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra
f24:
addi $sp, $sp, -36
sw $ra, 0($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,8($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,16($sp)
li $t0,1
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
add $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 36
jr $ra
f25:
addi $sp, $sp, -144
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bazzclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
li $v0, 1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, var#60
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
sw zero, 24($v0)
sw zero, 28($v0)
sw zero, 32($v0)
sw zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,12($sp)
var#60:
li $v0, 1
sw $v0,48($sp)
lw $t0,48($sp)
bgtz $t0, var#65
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,32
syscall
la $t0, Razzclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
sw zero, 24($v0)
sw zero, 28($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,12($sp)
var#65:
li $v0, 1
sw $v0,68($sp)
lw $t0,68($sp)
bgtz $t0, var#70
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,12($sp)
var#70:
var#57:
lw $t0,12($sp)
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,16($a0)
lw $t0,16($a0)
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,88($sp)
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
lw $t0,8($a0)
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,96($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,100($sp)
lw $t0,92($sp)
lw $t1,100($sp)
add $v0, $t0, $t1
sw $v0,108($sp)
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,116($sp)
lw $t0,108($sp)
lw $t1,116($sp)
add $v0, $t0, $t1
sw $v0,124($sp)
move $t0,$a0
move $v0, $t0
sw $v0,128($sp)
lw $t0,128($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,128($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,132($sp)
lw $t0,124($sp)
lw $t1,132($sp)
add $v0, $t0, $t1
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,20($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 144
jr $ra
f26:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st7
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f27:
addi $sp, $sp, -36
sw $ra, 0($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,8($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,16($sp)
li $t0,2
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
add $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,12($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,32($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 36
jr $ra
f28:
addi $sp, $sp, -140
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Fooclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
li $v0, 1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, var#101
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,40
syscall
la $t0, Barclase
sw $t0, 0($v0)
sw zero, 4($v0)
sw zero, 8($v0)
sw zero, 12($v0)
sw zero, 16($v0)
sw zero, 20($v0)
sw zero, 24($v0)
sw zero, 28($v0)
sw zero, 32($v0)
sw zero, 36($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,12($sp)
var#101:
li $v0, 1
sw $v0,48($sp)
lw $t0,48($sp)
bgtz $t0, var#106
lw $t0,8($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,12($sp)
var#106:
var#98:
lw $t0,12($sp)
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,24($a0)
lw $t0,16($a0)
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Bazzclase
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,72($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,80($sp)
lw $t0,72($sp)
lw $t1,80($sp)
add $v0, $t0, $t1
sw $v0,88($sp)
lw $t0,24($a0)
move $v0, $t0
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,88($sp)
lw $t1,96($sp)
add $v0, $t0, $t1
sw $v0,104($sp)
move $t0,$a0
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,112($sp)
lw $t0,104($sp)
lw $t1,112($sp)
add $v0, $t0, $t1
sw $v0,120($sp)
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
lw $t0,120($sp)
lw $t1,128($sp)
add $v0, $t0, $t1
sw $v0,136($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,28($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 140
jr $ra
f29:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st8
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f30:
addi $sp, $sp, -24
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Razzclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,32($a0)
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
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
lw $t0,20($sp)
move $v0, $t0
sw $v0,36($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 24
jr $ra
f31:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st9
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
