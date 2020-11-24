.data
st0: .asciiz "Object"
st1: .asciiz "IO"
st2: .asciiz "String"
st3: .asciiz "Bool"
st4: .asciiz "Main"
st5: .asciiz "enter a string\n"
st6: .asciiz "that was a palindrome\n"
st7: .asciiz "that was not a palindrome\n"
Objectclase: .word f0,f3,f2,f4
IOclase: .word f5,f6,f2,f4,f7,f8,f9,f10
Stringclase: .word f11,f12,f2,f4,f13,f14,f15
Boolclase: .word f16,f17,f2,f4
Mainclase: .word f18,f19,f2,f4,f7,f8,f9,f10,f20,f21
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
jal .Str.stringlengthlw $a0, 0($sp)
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
jal .Str.stringconcatlw $a0, 0($sp)
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
jal .Str.stringconcatlw $a0, 0($sp)
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
addi $sp, $sp, -8
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
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f19:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st4
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f20:
addi $sp, $sp, -176
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
bgtz $t0, Lbl4
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
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
li $t0,1
move $v0, $t0
sw $v0,36($sp)
lw $t0,32($sp)
lw $t1,36($sp)
move s0, $a0
move s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,44($sp)
lw $t0,44($sp)
bgtz $t0, Lbl2
move $t0,$a1
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,0
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,64($sp)
move $t0,$a1
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
li $t0,1
move $v0, $t0
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,64($sp)
lw $t1,96($sp)
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
sw $v0,104($sp)
lw $t0,104($sp)
bgtz $t0, Lbl0
li $t0,1
move $v0, $t0
sw $v0,148($sp)
lw $t0,148($sp)
move $v0, $t0
sw $v0,152($sp)
b Lbl1
Lbl0:
move $t0,$a0
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
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
move $t0,$a1
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
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
sw $v0,124($sp)
li $t0,2
move $v0, $t0
sw $v0,128($sp)
lw $t0,124($sp)
lw $t1,128($sp)
sub $v0, $t0, $t1
sw $v0,136($sp)
lw $t0,136($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,140($sp)
lw $t0,140($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,108($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,144($sp)
lw $t0,144($sp)
move $v0, $t0
sw $v0,152($sp)
Lbl1:
lw $t0,152($sp)
move $v0, $t0
sw $v0,156($sp)
lw $t0,156($sp)
move $v0, $t0
sw $v0,160($sp)
b Lbl3
Lbl2:
move $t0, zero
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,160($sp)
Lbl3:
lw $t0,160($sp)
move $v0, $t0
sw $v0,164($sp)
lw $t0,164($sp)
move $v0, $t0
sw $v0,168($sp)
b Lbl5
Lbl4:
move $t0, zero
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,168($sp)
Lbl5:
lw $t0,168($sp)
move $v0, $t0
sw $v0,172($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 176
jr $ra
f21:
addi $sp, $sp, -92
sw $ra, 0($sp)
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
not $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st5
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
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,48($sp)
lw $t0,48($sp)
bgtz $t0, Lbl6
move $t0,$a0
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st7
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
b Lbl7
Lbl6:
move $t0,$a0
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st6
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, $a0lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,64($sp)
lw $t0,64($sp)
move $v0, $t0
sw $v0,84($sp)
Lbl7:
lw $t0,84($sp)
move $v0, $t0
sw $v0,88($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 92
jr $ra
