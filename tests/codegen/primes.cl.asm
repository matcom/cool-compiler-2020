.data
st0: .asciiz "Object"
st1: .asciiz "IO"
st2: .asciiz "String"
st3: .asciiz "Bool"
st4: .asciiz "2 is trivially prime.\n"
st5: .asciiz " is prime.\n"
st6: .asciiz "halt"
st7: .asciiz "continue"
st8: .asciiz "Main"
Objectclase: .word f0,f3,f2,f4
IOclase: .word f5,f6,f2,f4,f7,f8,f9,f10
Stringclase: .word f11,f12,f2,f4,f13,f14,f15
Boolclase: .word f16,f17,f2,f4
Mainclase: .word f18,f19,f2,f4,f7,f8,f9,f10,f20
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
f8:
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
f9:
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
f10:
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
f11:
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
f12:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st2
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f13:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -8
sw $a0, 0($sp)
sw $ra, 4($sp)
move $a0, $t0
jal .Str.stringlength
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
move $t1,$a1
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringconcat
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f15:
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
jal .Str.stringconcat
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f16:
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
f17:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st3
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f18:
addi $sp, $sp, -344
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
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st4
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
li $t0,2
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,244($sp)
lw $t0,244($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
move $v0, $t0
sw $v0,48($sp)
li $t0,0
move $v0, $t0
sw $v0,68($sp)
li $t0,500
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,16($a0)
Lbl0:
move $t0, $zero
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1
sw $v0,44($sp)
lw $t0,44($sp)
bgtz $t0, Lbl1
lw $t0,48($sp)
move $v0, $t0
sw $v0,52($sp)
li $t0,1
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
add $v0, $t0, $t1
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,48($sp)
li $t0,2
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,68($sp)
Lbl2:
lw $t0,48($sp)
move $v0, $t0
sw $v0,76($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
mult $t0, $t1
mflo $v0
sw $v0,92($sp)
lw $t0,76($sp)
lw $t1,92($sp)
slt $v0, $t0, $t1
sw $v0,100($sp)
lw $t0,100($sp)
bgtz $t0, Lbl6
lw $t0,48($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
div $t0, $t1
mflo $v0
sw $v0,128($sp)
lw $t0,112($sp)
lw $t1,128($sp)
mult $t0, $t1
mflo $v0
sw $v0,136($sp)
lw $t0,108($sp)
lw $t1,136($sp)
sub $v0, $t0, $t1
sw $v0,144($sp)
li $t0,0
move $v0, $t0
sw $v0,148($sp)
lw $t0,144($sp)
lw $t1,148($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,156($sp)
lw $t0,156($sp)
bgtz $t0, Lbl4
move $t0, $zero
move $v0, $t0
sw $v0,164($sp)
lw $t0,164($sp)
move $v0, $t0
sw $v0,168($sp)
b Lbl5
Lbl4:
li $t0,1
move $v0, $t0
sw $v0,160($sp)
lw $t0,160($sp)
move $v0, $t0
sw $v0,168($sp)
Lbl5:
lw $t0,168($sp)
move $v0, $t0
sw $v0,172($sp)
lw $t0,172($sp)
move $v0, $t0
sw $v0,176($sp)
b Lbl7
Lbl6:
li $t0,1
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,176($sp)
Lbl7:
lw $t0,176($sp)
move $v0, $t0
sw $v0,180($sp)
lw $t0,180($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1
sw $v0,188($sp)
lw $t0,188($sp)
bgtz $t0, Lbl3
lw $t0,68($sp)
move $v0, $t0
sw $v0,192($sp)
li $t0,1
move $v0, $t0
sw $v0,196($sp)
lw $t0,192($sp)
lw $t1,196($sp)
add $v0, $t0, $t1
sw $v0,204($sp)
lw $t0,204($sp)
move $v0, $t0
sw $v0,68($sp)
b Lbl2
Lbl3:
li $t0,0
move $v0, $t0
sw $v0,212($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,216($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,220($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,224($sp)
lw $t0,220($sp)
lw $t1,224($sp)
mult $t0, $t1
mflo $v0
sw $v0,232($sp)
lw $t0,216($sp)
lw $t1,232($sp)
slt $v0, $t0, $t1
sw $v0,240($sp)
lw $t0,240($sp)
bgtz $t0, Lbl8
li $t0,0
move $v0, $t0
sw $v0,280($sp)
lw $t0,280($sp)
move $v0, $t0
sw $v0,284($sp)
b Lbl9
Lbl8:
lw $t0,48($sp)
move $v0, $t0
sw $v0,248($sp)
lw $t0,248($sp)
move $v0, $t0
sw $v0,244($sp)
move $t0,$a0
move $v0, $t0
sw $v0,252($sp)
lw $t0,252($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,244($sp)
move $v0, $t0
sw $v0,256($sp)
lw $t0,256($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,252($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,20($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,260($sp)
move $t0,$a0
move $v0, $t0
sw $v0,264($sp)
lw $t0,264($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st5
sw $v0,272($sp)
lw $t0,272($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,264($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,276($sp)
lw $t0,276($sp)
move $v0, $t0
sw $v0,284($sp)
Lbl9:
lw $t0,284($sp)
move $v0, $t0
sw $v0,288($sp)
lw $t0,16($a0)
move $v0, $t0
sw $v0,292($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,292($sp)
lw $t1,296($sp)
sle $v0, $t0, $t1
sw $v0,304($sp)
lw $t0,304($sp)
bgtz $t0, Lbl10
la $v0, st7
sw $v0,324($sp)
lw $t0,324($sp)
move $v0, $t0
sw $v0,328($sp)
b Lbl11
Lbl10:
la $v0, st6
sw $v0,312($sp)
lw $t0,312($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,312($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,8($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,316($sp)
lw $t0,316($sp)
move $v0, $t0
sw $v0,328($sp)
Lbl11:
lw $t0,328($sp)
move $v0, $t0
sw $v0,332($sp)
b Lbl0
Lbl1:
li $t0,0
move $v0, $t0
sw $v0,340($sp)
lw $t0,340($sp)
move $v0, $t0
sw $v0,20($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 344
jr $ra
f19:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st8
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f20:
addi $sp, $sp, -8
sw $ra, 0($sp)
li $t0,0
move $v0, $t0
sw $v0,4($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
