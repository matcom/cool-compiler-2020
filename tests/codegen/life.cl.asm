.data
st0: .asciiz "Object"
st1: .asciiz "IO"
st2: .asciiz "String"
st3: .asciiz "Bool"
st4: .asciiz "Board"
st5: .asciiz "CellularAutomaton"
st6: .asciiz "\n"
st7: .asciiz "\n"
st8: .asciiz "\n"
st9: .asciiz " "
st10: .asciiz " "
st11: .asciiz " "
st12: .asciiz " "
st13: .asciiz " "
st14: .asciiz " "
st15: .asciiz " "
st16: .asciiz " "
st17: .asciiz " "
st18: .asciiz " "
st19: .asciiz " "
st20: .asciiz " "
st21: .asciiz " "
st22: .asciiz " "
st23: .asciiz "X"
st24: .asciiz "X"
st25: .asciiz "X"
st26: .asciiz "X"
st27: .asciiz "X"
st28: .asciiz "X"
st29: .asciiz "X"
st30: .asciiz "X"
st31: .asciiz "X"
st32: .asciiz "X"
st33: .asciiz "X"
st34: .asciiz "-"
st35: .asciiz "-"
st36: .asciiz "\nPlease chose a number:\n"
st37: .asciiz "\t1: A cross\n"
st38: .asciiz "\t2: A slash from the upper left to lower right\n"
st39: .asciiz "\t3: A slash from the upper right to lower left\n"
st40: .asciiz "\t4: An X\n"
st41: .asciiz "\t5: A greater than sign \n"
st42: .asciiz "\t6: A less than sign\n"
st43: .asciiz "\t7: Two greater than signs\n"
st44: .asciiz "\t8: Two less than signs\n"
st45: .asciiz "\t9: A 'V'\n"
st46: .asciiz "\t10: An inverse 'V'\n"
st47: .asciiz "\t11: Numbers 9 and 10 combined\n"
st48: .asciiz "\t12: A full grid\n"
st49: .asciiz "\t13: A 'T'\n"
st50: .asciiz "\t14: A plus '+'\n"
st51: .asciiz "\t15: A 'W'\n"
st52: .asciiz "\t16: An 'M'\n"
st53: .asciiz "\t17: An 'E'\n"
st54: .asciiz "\t18: A '3'\n"
st55: .asciiz "\t19: An 'O'\n"
st56: .asciiz "\t20: An '8'\n"
st57: .asciiz "\t21: An 'S'\n"
st58: .asciiz "Your choice => "
st59: .asciiz "\n"
st60: .asciiz " XX  XXXX XXXX  XX  "
st61: .asciiz "    X   X   X   X   X    "
st62: .asciiz "X     X     X     X     X"
st63: .asciiz "X   X X X   X   X X X   X"
st64: .asciiz "X     X     X   X   X    "
st65: .asciiz "    X   X   X     X     X"
st66: .asciiz "X  X  X  XX  X      "
st67: .asciiz " X  XX  X  X  X     "
st68: .asciiz "X   X X X   X  "
st69: .asciiz "  X   X X X   X"
st70: .asciiz "X X X X X X X X"
st71: .asciiz "XXXXXXXXXXXXXXXXXXXXXXXXX"
st72: .asciiz "XXXXX  X    X    X    X  "
st73: .asciiz "  X    X  XXXXX  X    X  "
st74: .asciiz "X     X X X X   X X  "
st75: .asciiz "  X X   X X X X     X"
st76: .asciiz "XXXXX   X   XXXXX   X   XXXX"
st77: .asciiz "XXX    X   X  X    X   XXXX "
st78: .asciiz " XX X  XX  X XX "
st79: .asciiz " XX X  XX  X XX X  XX  X XX "
st80: .asciiz " XXXX   X    XX    X   XXXX "
st81: .asciiz "                         "
st82: .asciiz "Would you like to continue with the next generation? \n"
st83: .asciiz "Please use lowercase y or n for your answer [y]: "
st84: .asciiz "\n"
st85: .asciiz "n"
st86: .asciiz "\n\n"
st87: .asciiz "Would you like to choose a background pattern? \n"
st88: .asciiz "Please use lowercase y or n for your answer [n]: "
st89: .asciiz "y"
st90: .asciiz "Main"
st91: .asciiz "Welcome to the Game of Life.\n"
st92: .asciiz "There are many initial states to choose from. \n"
Objectclase: .word f0,f3,f2,f4
IOclase: .word f5,f6,f2,f4,f7,f8,f9,f10
Stringclase: .word f11,f12,f2,f4,f13,f14,f15
Boolclase: .word f16,f17,f2,f4
Boardclase: .word f18,f19,f2,f4,f7,f8,f9,f10,f20,f21
CellularAutomatonclase: .word f22,f23,f2,f4,f7,f8,f9,f10,f20,f21,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41
Mainclase: .word f42,f43,f2,f4,f7,f8,f9,f10,f20,f21,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f44
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
li $t0,0
move $v0, $t0
sw $v0,8($a0)
li $t0,0
move $v0, $t0
sw $v0,12($a0)
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
addi $sp, $sp, -12
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
lw $t0, 0($a0)
lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f21:
addi $sp, $sp, -264
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,32($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,16($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,20($sp)
li $t0,15
move $v0, $t0
sw $v0,24($sp)
lw $t0,20($sp)
lw $t1,24($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,32($sp)
lw $t0,32($sp)
bgtz $t0, Lbl10
lw $t0,4($sp)
move $v0, $t0
sw $v0,60($sp)
li $t0,16
move $v0, $t0
sw $v0,64($sp)
lw $t0,60($sp)
lw $t1,64($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,72($sp)
lw $t0,72($sp)
bgtz $t0, Lbl8
lw $t0,4($sp)
move $v0, $t0
sw $v0,88($sp)
li $t0,20
move $v0, $t0
sw $v0,92($sp)
lw $t0,88($sp)
lw $t1,92($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,100($sp)
lw $t0,100($sp)
bgtz $t0, Lbl6
lw $t0,4($sp)
move $v0, $t0
sw $v0,116($sp)
li $t0,21
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,128($sp)
lw $t0,128($sp)
bgtz $t0, Lbl4
lw $t0,4($sp)
move $v0, $t0
sw $v0,144($sp)
li $t0,25
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
bgtz $t0, Lbl2
lw $t0,4($sp)
move $v0, $t0
sw $v0,172($sp)
li $t0,28
move $v0, $t0
sw $v0,176($sp)
lw $t0,172($sp)
lw $t1,176($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,184($sp)
lw $t0,184($sp)
bgtz $t0, Lbl0
li $t0,5
move $v0, $t0
sw $v0,200($sp)
lw $t0,200($sp)
move $v0, $t0
sw $v0,36($sp)
li $t0,5
move $v0, $t0
sw $v0,204($sp)
lw $t0,204($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,208($sp)
lw $t0,208($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,212($sp)
b Lbl1
Lbl0:
li $t0,7
move $v0, $t0
sw $v0,188($sp)
lw $t0,188($sp)
move $v0, $t0
sw $v0,36($sp)
li $t0,4
move $v0, $t0
sw $v0,192($sp)
lw $t0,192($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,196($sp)
lw $t0,196($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,212($sp)
Lbl1:
lw $t0,212($sp)
move $v0, $t0
sw $v0,216($sp)
lw $t0,216($sp)
move $v0, $t0
sw $v0,220($sp)
b Lbl3
Lbl2:
li $t0,5
move $v0, $t0
sw $v0,160($sp)
lw $t0,160($sp)
move $v0, $t0
sw $v0,36($sp)
li $t0,5
move $v0, $t0
sw $v0,164($sp)
lw $t0,164($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,168($sp)
lw $t0,168($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,220($sp)
Lbl3:
lw $t0,220($sp)
move $v0, $t0
sw $v0,224($sp)
lw $t0,224($sp)
move $v0, $t0
sw $v0,228($sp)
b Lbl5
Lbl4:
li $t0,3
move $v0, $t0
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,36($sp)
li $t0,7
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,228($sp)
Lbl5:
lw $t0,228($sp)
move $v0, $t0
sw $v0,232($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,236($sp)
b Lbl7
Lbl6:
li $t0,4
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,36($sp)
li $t0,5
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,236($sp)
Lbl7:
lw $t0,236($sp)
move $v0, $t0
sw $v0,240($sp)
lw $t0,240($sp)
move $v0, $t0
sw $v0,244($sp)
b Lbl9
Lbl8:
li $t0,4
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,36($sp)
li $t0,4
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,244($sp)
Lbl9:
lw $t0,244($sp)
move $v0, $t0
sw $v0,248($sp)
lw $t0,248($sp)
move $v0, $t0
sw $v0,252($sp)
b Lbl11
Lbl10:
li $t0,3
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
move $v0, $t0
sw $v0,36($sp)
li $t0,5
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
move $v0, $t0
sw $v0,44($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,252($sp)
Lbl11:
lw $t0,252($sp)
move $v0, $t0
sw $v0,256($sp)
move $t0,$a0
move $v0, $t0
sw $v0,260($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 264
jr $ra
f22:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,Boardclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,16($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f23:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st5
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f24:
addi $sp, $sp, -28
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
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,16($sp)
lw $t0,16($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,36($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 28
jr $ra
f25:
addi $sp, $sp, -144
sw $ra, 0($sp)
li $t0,0
move $v0, $t0
sw $v0,8($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,16($sp)
move $t0,$a0
move $v0, $t0
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st6
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,20($sp)
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
sw $v0,32($sp)
Lbl12:
lw $t0,4($sp)
move $v0, $t0
sw $v0,36($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,40($sp)
lw $t0,36($sp)
lw $t1,40($sp)
slt $v0, $t0, $t1
sw $v0,48($sp)
lw $t0,48($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1
sw $v0,56($sp)
lw $t0,56($sp)
bgtz $t0, Lbl13
move $t0,$a0
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,16($a0)
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,68($sp)
lw $t0,68($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($a0)
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,60($sp)
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
sw $v0,80($sp)
move $t0,$a0
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st7
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,84($sp)
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
sw $v0,96($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,100($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,104($sp)
lw $t0,100($sp)
lw $t1,104($sp)
add $v0, $t0, $t1
sw $v0,112($sp)
lw $t0,112($sp)
move $v0, $t0
sw $v0,4($sp)
b Lbl12
Lbl13:
li $t0,0
move $v0, $t0
sw $v0,120($sp)
move $t0,$a0
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st8
sw $v0,132($sp)
lw $t0,132($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,124($sp)
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
sw $v0,136($sp)
move $t0,$a0
move $v0, $t0
sw $v0,140($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 144
jr $ra
f26:
addi $sp, $sp, -12
sw $ra, 0($sp)
lw $t0,16($a0)
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
lw $t0, 0($a0)
lw $t0,16($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f27:
addi $sp, $sp, -64
sw $ra, 0($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
move $t0,$a1
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl14
lw $t0,16($a0)
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,52($sp)
lw $t0,52($sp)
move $v0, $t0
sw $v0,56($sp)
b Lbl15
Lbl14:
la $v0, st9
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,56($sp)
Lbl15:
lw $t0,56($sp)
move $v0, $t0
sw $v0,60($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 64
jr $ra
f28:
addi $sp, $sp, -72
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl16
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
sub $v0, $t0, $t1
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,64($sp)
b Lbl17
Lbl16:
la $v0, st10
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,64($sp)
Lbl17:
lw $t0,64($sp)
move $v0, $t0
sw $v0,68($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 72
jr $ra
f29:
addi $sp, $sp, -72
sw $ra, 0($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
add $v0, $t0, $t1
sw $v0,20($sp)
lw $t0,4($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl18
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
add $v0, $t0, $t1
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,64($sp)
b Lbl19
Lbl18:
la $v0, st11
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,64($sp)
Lbl19:
lw $t0,64($sp)
move $v0, $t0
sw $v0,68($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 72
jr $ra
f30:
addi $sp, $sp, -108
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
li $t0,1
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
add $v0, $t0, $t1
sw $v0,16($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
div $t0, $t1
mflo $v0
sw $v0,28($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
mult $t0, $t1
mflo $v0
sw $v0,40($sp)
move $t0,$a1
move $v0, $t0
sw $v0,44($sp)
li $t0,1
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
add $v0, $t0, $t1
sw $v0,56($sp)
lw $t0,40($sp)
lw $t1,56($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl20
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
add $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl21
Lbl20:
la $v0, st12
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl21:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 108
jr $ra
f31:
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
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,16($sp)
lw $t0,16($sp)
bgtz $t0, Lbl24
move $t0,$a1
move $v0, $t0
sw $v0,28($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
div $t0, $t1
mflo $v0
sw $v0,40($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
mult $t0, $t1
mflo $v0
sw $v0,52($sp)
move $t0,$a1
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,64($sp)
lw $t0,64($sp)
bgtz $t0, Lbl22
move $t0,$a0
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
sub $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,92($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,96($sp)
lw $t0,96($sp)
move $v0, $t0
sw $v0,100($sp)
b Lbl23
Lbl22:
la $v0, st14
sw $v0,72($sp)
lw $t0,72($sp)
move $v0, $t0
sw $v0,100($sp)
Lbl23:
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
b Lbl25
Lbl24:
la $v0, st13
sw $v0,24($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,108($sp)
Lbl25:
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 116
jr $ra
f32:
addi $sp, $sp, -128
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl28
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
div $t0, $t1
mflo $v0
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
mult $t0, $t1
mflo $v0
sw $v0,64($sp)
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,76($sp)
lw $t0,76($sp)
bgtz $t0, Lbl26
move $t0,$a0
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,92($sp)
li $t0,1
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
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
b Lbl27
Lbl26:
la $v0, st16
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,112($sp)
Lbl27:
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
b Lbl29
Lbl28:
la $v0, st15
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,120($sp)
Lbl29:
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 128
jr $ra
f33:
addi $sp, $sp, -152
sw $ra, 0($sp)
move $t0,$a1
move $v0, $t0
sw $v0,4($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,8($sp)
lw $t0,4($sp)
lw $t1,8($sp)
sub $v0, $t0, $t1
sw $v0,16($sp)
li $t0,0
move $v0, $t0
sw $v0,20($sp)
lw $t0,16($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl32
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
li $t0,1
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
add $v0, $t0, $t1
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
div $t0, $t1
mflo $v0
sw $v0,64($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
mult $t0, $t1
mflo $v0
sw $v0,76($sp)
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
add $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,76($sp)
lw $t1,92($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,100($sp)
lw $t0,100($sp)
bgtz $t0, Lbl30
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,116($sp)
li $t0,1
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
add $v0, $t0, $t1
sw $v0,128($sp)
lw $t0,128($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl31
Lbl30:
la $v0, st18
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl31:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
b Lbl33
Lbl32:
la $v0, st17
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,144($sp)
Lbl33:
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 152
jr $ra
f34:
addi $sp, $sp, -152
sw $ra, 0($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
add $v0, $t0, $t1
sw $v0,20($sp)
lw $t0,4($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl36
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
li $t0,1
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
add $v0, $t0, $t1
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
div $t0, $t1
mflo $v0
sw $v0,64($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
mult $t0, $t1
mflo $v0
sw $v0,76($sp)
move $t0,$a1
move $v0, $t0
sw $v0,80($sp)
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,80($sp)
lw $t1,84($sp)
add $v0, $t0, $t1
sw $v0,92($sp)
lw $t0,76($sp)
lw $t1,92($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,100($sp)
lw $t0,100($sp)
bgtz $t0, Lbl34
move $t0,$a0
move $v0, $t0
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,116($sp)
li $t0,1
move $v0, $t0
sw $v0,120($sp)
lw $t0,116($sp)
lw $t1,120($sp)
add $v0, $t0, $t1
sw $v0,128($sp)
lw $t0,128($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl35
Lbl34:
la $v0, st20
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl35:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,140($sp)
move $v0, $t0
sw $v0,144($sp)
b Lbl37
Lbl36:
la $v0, st19
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,144($sp)
Lbl37:
lw $t0,144($sp)
move $v0, $t0
sw $v0,148($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 152
jr $ra
f35:
addi $sp, $sp, -128
sw $ra, 0($sp)
lw $t0,12($a0)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a1
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,12($sp)
lw $t0,8($sp)
lw $t1,12($sp)
add $v0, $t0, $t1
sw $v0,20($sp)
lw $t0,4($sp)
lw $t1,20($sp)
slt $v0, $t0, $t1
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl40
move $t0,$a1
move $v0, $t0
sw $v0,40($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,44($sp)
lw $t0,40($sp)
lw $t1,44($sp)
div $t0, $t1
mflo $v0
sw $v0,52($sp)
lw $t0,8($a0)
move $v0, $t0
sw $v0,56($sp)
lw $t0,52($sp)
lw $t1,56($sp)
mult $t0, $t1
mflo $v0
sw $v0,64($sp)
move $t0,$a1
move $v0, $t0
sw $v0,68($sp)
lw $t0,64($sp)
lw $t1,68($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,76($sp)
lw $t0,76($sp)
bgtz $t0, Lbl38
move $t0,$a0
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,92($sp)
li $t0,1
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
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,112($sp)
b Lbl39
Lbl38:
la $v0, st22
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,112($sp)
Lbl39:
lw $t0,112($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
b Lbl41
Lbl40:
la $v0, st21
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,120($sp)
Lbl41:
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 128
jr $ra
f36:
addi $sp, $sp, -412
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
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
lw $t0, 0($a0)
lw $t0,56($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
la $v0, st23
sw $v0,20($sp)
lw $t0,12($sp)
lw $t1,20($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,28($sp)
lw $t0,28($sp)
bgtz $t0, Lbl42
li $t0,0
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
move $v0, $t0
sw $v0,40($sp)
b Lbl43
Lbl42:
li $t0,1
move $v0, $t0
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,40($sp)
Lbl43:
lw $t0,40($sp)
move $v0, $t0
sw $v0,44($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
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
lw $t0, 0($a0)
lw $t0,60($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,56($sp)
la $v0, st24
sw $v0,64($sp)
lw $t0,56($sp)
lw $t1,64($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,72($sp)
lw $t0,72($sp)
bgtz $t0, Lbl44
li $t0,0
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
move $v0, $t0
sw $v0,84($sp)
b Lbl45
Lbl44:
li $t0,1
move $v0, $t0
sw $v0,76($sp)
lw $t0,76($sp)
move $v0, $t0
sw $v0,84($sp)
Lbl45:
lw $t0,84($sp)
move $v0, $t0
sw $v0,88($sp)
lw $t0,44($sp)
lw $t1,88($sp)
add $v0, $t0, $t1
sw $v0,96($sp)
move $t0,$a0
move $v0, $t0
sw $v0,100($sp)
lw $t0,100($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,100($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,64($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,108($sp)
la $v0, st25
sw $v0,116($sp)
lw $t0,108($sp)
lw $t1,116($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,124($sp)
lw $t0,124($sp)
bgtz $t0, Lbl46
li $t0,0
move $v0, $t0
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl47
Lbl46:
li $t0,1
move $v0, $t0
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl47:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
lw $t0,96($sp)
lw $t1,140($sp)
add $v0, $t0, $t1
sw $v0,148($sp)
move $t0,$a0
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
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
lw $t0, 0($a0)
lw $t0,68($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,160($sp)
la $v0, st26
sw $v0,168($sp)
lw $t0,160($sp)
lw $t1,168($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,176($sp)
lw $t0,176($sp)
bgtz $t0, Lbl48
li $t0,0
move $v0, $t0
sw $v0,184($sp)
lw $t0,184($sp)
move $v0, $t0
sw $v0,188($sp)
b Lbl49
Lbl48:
li $t0,1
move $v0, $t0
sw $v0,180($sp)
lw $t0,180($sp)
move $v0, $t0
sw $v0,188($sp)
Lbl49:
lw $t0,188($sp)
move $v0, $t0
sw $v0,192($sp)
lw $t0,148($sp)
lw $t1,192($sp)
add $v0, $t0, $t1
sw $v0,200($sp)
move $t0,$a0
move $v0, $t0
sw $v0,204($sp)
lw $t0,204($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,208($sp)
lw $t0,208($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,204($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,76($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,212($sp)
la $v0, st27
sw $v0,220($sp)
lw $t0,212($sp)
lw $t1,220($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,228($sp)
lw $t0,228($sp)
bgtz $t0, Lbl50
li $t0,0
move $v0, $t0
sw $v0,236($sp)
lw $t0,236($sp)
move $v0, $t0
sw $v0,240($sp)
b Lbl51
Lbl50:
li $t0,1
move $v0, $t0
sw $v0,232($sp)
lw $t0,232($sp)
move $v0, $t0
sw $v0,240($sp)
Lbl51:
lw $t0,240($sp)
move $v0, $t0
sw $v0,244($sp)
lw $t0,200($sp)
lw $t1,244($sp)
add $v0, $t0, $t1
sw $v0,252($sp)
move $t0,$a0
move $v0, $t0
sw $v0,256($sp)
lw $t0,256($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,260($sp)
lw $t0,260($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,256($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,72($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,264($sp)
la $v0, st28
sw $v0,272($sp)
lw $t0,264($sp)
lw $t1,272($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,280($sp)
lw $t0,280($sp)
bgtz $t0, Lbl52
li $t0,0
move $v0, $t0
sw $v0,288($sp)
lw $t0,288($sp)
move $v0, $t0
sw $v0,292($sp)
b Lbl53
Lbl52:
li $t0,1
move $v0, $t0
sw $v0,284($sp)
lw $t0,284($sp)
move $v0, $t0
sw $v0,292($sp)
Lbl53:
lw $t0,292($sp)
move $v0, $t0
sw $v0,296($sp)
lw $t0,252($sp)
lw $t1,296($sp)
add $v0, $t0, $t1
sw $v0,304($sp)
move $t0,$a0
move $v0, $t0
sw $v0,308($sp)
lw $t0,308($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,312($sp)
lw $t0,312($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,308($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,80($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,316($sp)
la $v0, st29
sw $v0,324($sp)
lw $t0,316($sp)
lw $t1,324($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,332($sp)
lw $t0,332($sp)
bgtz $t0, Lbl54
li $t0,0
move $v0, $t0
sw $v0,340($sp)
lw $t0,340($sp)
move $v0, $t0
sw $v0,344($sp)
b Lbl55
Lbl54:
li $t0,1
move $v0, $t0
sw $v0,336($sp)
lw $t0,336($sp)
move $v0, $t0
sw $v0,344($sp)
Lbl55:
lw $t0,344($sp)
move $v0, $t0
sw $v0,348($sp)
lw $t0,304($sp)
lw $t1,348($sp)
add $v0, $t0, $t1
sw $v0,356($sp)
move $t0,$a0
move $v0, $t0
sw $v0,360($sp)
lw $t0,360($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
move $v0, $t0
sw $v0,364($sp)
lw $t0,364($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,360($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,84($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,368($sp)
la $v0, st30
sw $v0,376($sp)
lw $t0,368($sp)
lw $t1,376($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,384($sp)
lw $t0,384($sp)
bgtz $t0, Lbl56
li $t0,0
move $v0, $t0
sw $v0,392($sp)
lw $t0,392($sp)
move $v0, $t0
sw $v0,396($sp)
b Lbl57
Lbl56:
li $t0,1
move $v0, $t0
sw $v0,388($sp)
lw $t0,388($sp)
move $v0, $t0
sw $v0,396($sp)
Lbl57:
lw $t0,396($sp)
move $v0, $t0
sw $v0,400($sp)
lw $t0,356($sp)
lw $t1,400($sp)
add $v0, $t0, $t1
sw $v0,408($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 412
jr $ra
f37:
addi $sp, $sp, -136
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
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
lw $t0, 0($a0)
lw $t0,88($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,12($sp)
li $t0,3
move $v0, $t0
sw $v0,16($sp)
lw $t0,12($sp)
lw $t1,16($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,24($sp)
lw $t0,24($sp)
bgtz $t0, Lbl62
move $t0,$a0
move $v0, $t0
sw $v0,36($sp)
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a1
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
lw $t0, 0($a0)
lw $t0,88($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
li $t0,2
move $v0, $t0
sw $v0,48($sp)
lw $t0,44($sp)
lw $t1,48($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,56($sp)
lw $t0,56($sp)
bgtz $t0, Lbl60
la $v0, st35
sw $v0,116($sp)
lw $t0,116($sp)
move $v0, $t0
sw $v0,120($sp)
b Lbl61
Lbl60:
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
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,52($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,68($sp)
la $v0, st32
sw $v0,76($sp)
lw $t0,68($sp)
lw $t1,76($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,84($sp)
lw $t0,84($sp)
bgtz $t0, Lbl58
la $v0, st34
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,104($sp)
b Lbl59
Lbl58:
la $v0, st33
sw $v0,92($sp)
lw $t0,92($sp)
move $v0, $t0
sw $v0,104($sp)
Lbl59:
lw $t0,104($sp)
move $v0, $t0
sw $v0,108($sp)
lw $t0,108($sp)
move $v0, $t0
sw $v0,120($sp)
Lbl61:
lw $t0,120($sp)
move $v0, $t0
sw $v0,124($sp)
lw $t0,124($sp)
move $v0, $t0
sw $v0,128($sp)
b Lbl63
Lbl62:
la $v0, st31
sw $v0,32($sp)
lw $t0,32($sp)
move $v0, $t0
sw $v0,128($sp)
Lbl63:
lw $t0,128($sp)
move $v0, $t0
sw $v0,132($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 136
jr $ra
f38:
addi $sp, $sp, -108
sw $ra, 0($sp)
li $t0,0
move $v0, $t0
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
lw $t0, 0($a0)
lw $t0,48($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,20($sp)
Lbl64:
lw $t0,4($sp)
move $v0, $t0
sw $v0,28($sp)
lw $t0,12($sp)
move $v0, $t0
sw $v0,32($sp)
lw $t0,28($sp)
lw $t1,32($sp)
slt $v0, $t0, $t1
sw $v0,40($sp)
lw $t0,40($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1
sw $v0,48($sp)
lw $t0,48($sp)
bgtz $t0, Lbl65
lw $t0,24($sp)
move $v0, $t0
sw $v0,52($sp)
lw $t0,52($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
move $t0,$a0
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,4($sp)
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,92($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,52($sp)
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
sw $v0,68($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,24($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,72($sp)
li $t0,1
move $v0, $t0
sw $v0,76($sp)
lw $t0,72($sp)
lw $t1,76($sp)
add $v0, $t0, $t1
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,4($sp)
b Lbl64
Lbl65:
li $t0,0
move $v0, $t0
sw $v0,92($sp)
lw $t0,24($sp)
move $v0, $t0
sw $v0,100($sp)
lw $t0,100($sp)
move $v0, $t0
sw $v0,96($sp)
move $t0,$a0
move $v0, $t0
sw $v0,104($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 108
jr $ra
f39:
addi $sp, $sp, -1080
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st36
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
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st37
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
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
sw $v0,36($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st38
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
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
sw $v0,52($sp)
move $t0,$a0
move $v0, $t0
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st39
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,56($sp)
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
sw $v0,68($sp)
move $t0,$a0
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st40
sw $v0,80($sp)
lw $t0,80($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,72($sp)
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
sw $v0,84($sp)
move $t0,$a0
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st41
sw $v0,96($sp)
lw $t0,96($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,88($sp)
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
sw $v0,100($sp)
move $t0,$a0
move $v0, $t0
sw $v0,104($sp)
lw $t0,104($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st42
sw $v0,112($sp)
lw $t0,112($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,104($sp)
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
sw $v0,116($sp)
move $t0,$a0
move $v0, $t0
sw $v0,120($sp)
lw $t0,120($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st43
sw $v0,128($sp)
lw $t0,128($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,120($sp)
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
sw $v0,132($sp)
move $t0,$a0
move $v0, $t0
sw $v0,136($sp)
lw $t0,136($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st44
sw $v0,144($sp)
lw $t0,144($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,136($sp)
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
sw $v0,148($sp)
move $t0,$a0
move $v0, $t0
sw $v0,152($sp)
lw $t0,152($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st45
sw $v0,160($sp)
lw $t0,160($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,152($sp)
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
sw $v0,164($sp)
move $t0,$a0
move $v0, $t0
sw $v0,168($sp)
lw $t0,168($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st46
sw $v0,176($sp)
lw $t0,176($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,168($sp)
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
sw $v0,180($sp)
move $t0,$a0
move $v0, $t0
sw $v0,184($sp)
lw $t0,184($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st47
sw $v0,192($sp)
lw $t0,192($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,184($sp)
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
sw $v0,196($sp)
move $t0,$a0
move $v0, $t0
sw $v0,200($sp)
lw $t0,200($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st48
sw $v0,208($sp)
lw $t0,208($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,200($sp)
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
sw $v0,212($sp)
move $t0,$a0
move $v0, $t0
sw $v0,216($sp)
lw $t0,216($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st49
sw $v0,224($sp)
lw $t0,224($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,216($sp)
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
sw $v0,228($sp)
move $t0,$a0
move $v0, $t0
sw $v0,232($sp)
lw $t0,232($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st50
sw $v0,240($sp)
lw $t0,240($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,232($sp)
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
sw $v0,244($sp)
move $t0,$a0
move $v0, $t0
sw $v0,248($sp)
lw $t0,248($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st51
sw $v0,256($sp)
lw $t0,256($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,248($sp)
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
sw $v0,260($sp)
move $t0,$a0
move $v0, $t0
sw $v0,264($sp)
lw $t0,264($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st52
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
move $t0,$a0
move $v0, $t0
sw $v0,280($sp)
lw $t0,280($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st53
sw $v0,288($sp)
lw $t0,288($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,280($sp)
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
sw $v0,292($sp)
move $t0,$a0
move $v0, $t0
sw $v0,296($sp)
lw $t0,296($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st54
sw $v0,304($sp)
lw $t0,304($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,296($sp)
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
sw $v0,308($sp)
move $t0,$a0
move $v0, $t0
sw $v0,312($sp)
lw $t0,312($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st55
sw $v0,320($sp)
lw $t0,320($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,312($sp)
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
sw $v0,324($sp)
move $t0,$a0
move $v0, $t0
sw $v0,328($sp)
lw $t0,328($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st56
sw $v0,336($sp)
lw $t0,336($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,328($sp)
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
sw $v0,340($sp)
move $t0,$a0
move $v0, $t0
sw $v0,344($sp)
lw $t0,344($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st57
sw $v0,352($sp)
lw $t0,352($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,344($sp)
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
sw $v0,356($sp)
move $t0,$a0
move $v0, $t0
sw $v0,360($sp)
lw $t0,360($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st58
sw $v0,368($sp)
lw $t0,368($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,360($sp)
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
sw $v0,372($sp)
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
lw $t0, 0($a0)
lw $t0,28($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,380($sp)
lw $t0,380($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,384($sp)
lw $t0,384($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st59
sw $v0,392($sp)
lw $t0,392($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,384($sp)
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
sw $v0,396($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,400($sp)
li $t0,1
move $v0, $t0
sw $v0,404($sp)
lw $t0,400($sp)
lw $t1,404($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,412($sp)
lw $t0,412($sp)
bgtz $t0, Lbl106
lw $t0,4($sp)
move $v0, $t0
sw $v0,424($sp)
li $t0,2
move $v0, $t0
sw $v0,428($sp)
lw $t0,424($sp)
lw $t1,428($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,436($sp)
lw $t0,436($sp)
bgtz $t0, Lbl104
lw $t0,4($sp)
move $v0, $t0
sw $v0,448($sp)
li $t0,3
move $v0, $t0
sw $v0,452($sp)
lw $t0,448($sp)
lw $t1,452($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,460($sp)
lw $t0,460($sp)
bgtz $t0, Lbl102
lw $t0,4($sp)
move $v0, $t0
sw $v0,472($sp)
li $t0,4
move $v0, $t0
sw $v0,476($sp)
lw $t0,472($sp)
lw $t1,476($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,484($sp)
lw $t0,484($sp)
bgtz $t0, Lbl100
lw $t0,4($sp)
move $v0, $t0
sw $v0,496($sp)
li $t0,5
move $v0, $t0
sw $v0,500($sp)
lw $t0,496($sp)
lw $t1,500($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,508($sp)
lw $t0,508($sp)
bgtz $t0, Lbl98
lw $t0,4($sp)
move $v0, $t0
sw $v0,520($sp)
li $t0,6
move $v0, $t0
sw $v0,524($sp)
lw $t0,520($sp)
lw $t1,524($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,532($sp)
lw $t0,532($sp)
bgtz $t0, Lbl96
lw $t0,4($sp)
move $v0, $t0
sw $v0,544($sp)
li $t0,7
move $v0, $t0
sw $v0,548($sp)
lw $t0,544($sp)
lw $t1,548($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,556($sp)
lw $t0,556($sp)
bgtz $t0, Lbl94
lw $t0,4($sp)
move $v0, $t0
sw $v0,568($sp)
li $t0,8
move $v0, $t0
sw $v0,572($sp)
lw $t0,568($sp)
lw $t1,572($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,580($sp)
lw $t0,580($sp)
bgtz $t0, Lbl92
lw $t0,4($sp)
move $v0, $t0
sw $v0,592($sp)
li $t0,9
move $v0, $t0
sw $v0,596($sp)
lw $t0,592($sp)
lw $t1,596($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,604($sp)
lw $t0,604($sp)
bgtz $t0, Lbl90
lw $t0,4($sp)
move $v0, $t0
sw $v0,616($sp)
li $t0,10
move $v0, $t0
sw $v0,620($sp)
lw $t0,616($sp)
lw $t1,620($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,628($sp)
lw $t0,628($sp)
bgtz $t0, Lbl88
lw $t0,4($sp)
move $v0, $t0
sw $v0,640($sp)
li $t0,11
move $v0, $t0
sw $v0,644($sp)
lw $t0,640($sp)
lw $t1,644($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,652($sp)
lw $t0,652($sp)
bgtz $t0, Lbl86
lw $t0,4($sp)
move $v0, $t0
sw $v0,664($sp)
li $t0,12
move $v0, $t0
sw $v0,668($sp)
lw $t0,664($sp)
lw $t1,668($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,676($sp)
lw $t0,676($sp)
bgtz $t0, Lbl84
lw $t0,4($sp)
move $v0, $t0
sw $v0,688($sp)
li $t0,13
move $v0, $t0
sw $v0,692($sp)
lw $t0,688($sp)
lw $t1,692($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,700($sp)
lw $t0,700($sp)
bgtz $t0, Lbl82
lw $t0,4($sp)
move $v0, $t0
sw $v0,712($sp)
li $t0,14
move $v0, $t0
sw $v0,716($sp)
lw $t0,712($sp)
lw $t1,716($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,724($sp)
lw $t0,724($sp)
bgtz $t0, Lbl80
lw $t0,4($sp)
move $v0, $t0
sw $v0,736($sp)
li $t0,15
move $v0, $t0
sw $v0,740($sp)
lw $t0,736($sp)
lw $t1,740($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,748($sp)
lw $t0,748($sp)
bgtz $t0, Lbl78
lw $t0,4($sp)
move $v0, $t0
sw $v0,760($sp)
li $t0,16
move $v0, $t0
sw $v0,764($sp)
lw $t0,760($sp)
lw $t1,764($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,772($sp)
lw $t0,772($sp)
bgtz $t0, Lbl76
lw $t0,4($sp)
move $v0, $t0
sw $v0,784($sp)
li $t0,17
move $v0, $t0
sw $v0,788($sp)
lw $t0,784($sp)
lw $t1,788($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,796($sp)
lw $t0,796($sp)
bgtz $t0, Lbl74
lw $t0,4($sp)
move $v0, $t0
sw $v0,808($sp)
li $t0,18
move $v0, $t0
sw $v0,812($sp)
lw $t0,808($sp)
lw $t1,812($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,820($sp)
lw $t0,820($sp)
bgtz $t0, Lbl72
lw $t0,4($sp)
move $v0, $t0
sw $v0,832($sp)
li $t0,19
move $v0, $t0
sw $v0,836($sp)
lw $t0,832($sp)
lw $t1,836($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,844($sp)
lw $t0,844($sp)
bgtz $t0, Lbl70
lw $t0,4($sp)
move $v0, $t0
sw $v0,856($sp)
li $t0,20
move $v0, $t0
sw $v0,860($sp)
lw $t0,856($sp)
lw $t1,860($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,868($sp)
lw $t0,868($sp)
bgtz $t0, Lbl68
lw $t0,4($sp)
move $v0, $t0
sw $v0,880($sp)
li $t0,21
move $v0, $t0
sw $v0,884($sp)
lw $t0,880($sp)
lw $t1,884($sp)
move $s0, $a0
move $s1, $a1
move $a0, $t0
move $a1, $t1
jal .Int.igual
move $a0, $s0
move $a1, $s1
sw $v0,892($sp)
lw $t0,892($sp)
bgtz $t0, Lbl66
la $v0, st81
sw $v0,908($sp)
lw $t0,908($sp)
move $v0, $t0
sw $v0,912($sp)
b Lbl67
Lbl66:
la $v0, st80
sw $v0,900($sp)
lw $t0,900($sp)
move $v0, $t0
sw $v0,912($sp)
Lbl67:
lw $t0,912($sp)
move $v0, $t0
sw $v0,916($sp)
lw $t0,916($sp)
move $v0, $t0
sw $v0,920($sp)
b Lbl69
Lbl68:
la $v0, st79
sw $v0,876($sp)
lw $t0,876($sp)
move $v0, $t0
sw $v0,920($sp)
Lbl69:
lw $t0,920($sp)
move $v0, $t0
sw $v0,924($sp)
lw $t0,924($sp)
move $v0, $t0
sw $v0,928($sp)
b Lbl71
Lbl70:
la $v0, st78
sw $v0,852($sp)
lw $t0,852($sp)
move $v0, $t0
sw $v0,928($sp)
Lbl71:
lw $t0,928($sp)
move $v0, $t0
sw $v0,932($sp)
lw $t0,932($sp)
move $v0, $t0
sw $v0,936($sp)
b Lbl73
Lbl72:
la $v0, st77
sw $v0,828($sp)
lw $t0,828($sp)
move $v0, $t0
sw $v0,936($sp)
Lbl73:
lw $t0,936($sp)
move $v0, $t0
sw $v0,940($sp)
lw $t0,940($sp)
move $v0, $t0
sw $v0,944($sp)
b Lbl75
Lbl74:
la $v0, st76
sw $v0,804($sp)
lw $t0,804($sp)
move $v0, $t0
sw $v0,944($sp)
Lbl75:
lw $t0,944($sp)
move $v0, $t0
sw $v0,948($sp)
lw $t0,948($sp)
move $v0, $t0
sw $v0,952($sp)
b Lbl77
Lbl76:
la $v0, st75
sw $v0,780($sp)
lw $t0,780($sp)
move $v0, $t0
sw $v0,952($sp)
Lbl77:
lw $t0,952($sp)
move $v0, $t0
sw $v0,956($sp)
lw $t0,956($sp)
move $v0, $t0
sw $v0,960($sp)
b Lbl79
Lbl78:
la $v0, st74
sw $v0,756($sp)
lw $t0,756($sp)
move $v0, $t0
sw $v0,960($sp)
Lbl79:
lw $t0,960($sp)
move $v0, $t0
sw $v0,964($sp)
lw $t0,964($sp)
move $v0, $t0
sw $v0,968($sp)
b Lbl81
Lbl80:
la $v0, st73
sw $v0,732($sp)
lw $t0,732($sp)
move $v0, $t0
sw $v0,968($sp)
Lbl81:
lw $t0,968($sp)
move $v0, $t0
sw $v0,972($sp)
lw $t0,972($sp)
move $v0, $t0
sw $v0,976($sp)
b Lbl83
Lbl82:
la $v0, st72
sw $v0,708($sp)
lw $t0,708($sp)
move $v0, $t0
sw $v0,976($sp)
Lbl83:
lw $t0,976($sp)
move $v0, $t0
sw $v0,980($sp)
lw $t0,980($sp)
move $v0, $t0
sw $v0,984($sp)
b Lbl85
Lbl84:
la $v0, st71
sw $v0,684($sp)
lw $t0,684($sp)
move $v0, $t0
sw $v0,984($sp)
Lbl85:
lw $t0,984($sp)
move $v0, $t0
sw $v0,988($sp)
lw $t0,988($sp)
move $v0, $t0
sw $v0,992($sp)
b Lbl87
Lbl86:
la $v0, st70
sw $v0,660($sp)
lw $t0,660($sp)
move $v0, $t0
sw $v0,992($sp)
Lbl87:
lw $t0,992($sp)
move $v0, $t0
sw $v0,996($sp)
lw $t0,996($sp)
move $v0, $t0
sw $v0,1000($sp)
b Lbl89
Lbl88:
la $v0, st69
sw $v0,636($sp)
lw $t0,636($sp)
move $v0, $t0
sw $v0,1000($sp)
Lbl89:
lw $t0,1000($sp)
move $v0, $t0
sw $v0,1004($sp)
lw $t0,1004($sp)
move $v0, $t0
sw $v0,1008($sp)
b Lbl91
Lbl90:
la $v0, st68
sw $v0,612($sp)
lw $t0,612($sp)
move $v0, $t0
sw $v0,1008($sp)
Lbl91:
lw $t0,1008($sp)
move $v0, $t0
sw $v0,1012($sp)
lw $t0,1012($sp)
move $v0, $t0
sw $v0,1016($sp)
b Lbl93
Lbl92:
la $v0, st67
sw $v0,588($sp)
lw $t0,588($sp)
move $v0, $t0
sw $v0,1016($sp)
Lbl93:
lw $t0,1016($sp)
move $v0, $t0
sw $v0,1020($sp)
lw $t0,1020($sp)
move $v0, $t0
sw $v0,1024($sp)
b Lbl95
Lbl94:
la $v0, st66
sw $v0,564($sp)
lw $t0,564($sp)
move $v0, $t0
sw $v0,1024($sp)
Lbl95:
lw $t0,1024($sp)
move $v0, $t0
sw $v0,1028($sp)
lw $t0,1028($sp)
move $v0, $t0
sw $v0,1032($sp)
b Lbl97
Lbl96:
la $v0, st65
sw $v0,540($sp)
lw $t0,540($sp)
move $v0, $t0
sw $v0,1032($sp)
Lbl97:
lw $t0,1032($sp)
move $v0, $t0
sw $v0,1036($sp)
lw $t0,1036($sp)
move $v0, $t0
sw $v0,1040($sp)
b Lbl99
Lbl98:
la $v0, st64
sw $v0,516($sp)
lw $t0,516($sp)
move $v0, $t0
sw $v0,1040($sp)
Lbl99:
lw $t0,1040($sp)
move $v0, $t0
sw $v0,1044($sp)
lw $t0,1044($sp)
move $v0, $t0
sw $v0,1048($sp)
b Lbl101
Lbl100:
la $v0, st63
sw $v0,492($sp)
lw $t0,492($sp)
move $v0, $t0
sw $v0,1048($sp)
Lbl101:
lw $t0,1048($sp)
move $v0, $t0
sw $v0,1052($sp)
lw $t0,1052($sp)
move $v0, $t0
sw $v0,1056($sp)
b Lbl103
Lbl102:
la $v0, st62
sw $v0,468($sp)
lw $t0,468($sp)
move $v0, $t0
sw $v0,1056($sp)
Lbl103:
lw $t0,1056($sp)
move $v0, $t0
sw $v0,1060($sp)
lw $t0,1060($sp)
move $v0, $t0
sw $v0,1064($sp)
b Lbl105
Lbl104:
la $v0, st61
sw $v0,444($sp)
lw $t0,444($sp)
move $v0, $t0
sw $v0,1064($sp)
Lbl105:
lw $t0,1064($sp)
move $v0, $t0
sw $v0,1068($sp)
lw $t0,1068($sp)
move $v0, $t0
sw $v0,1072($sp)
b Lbl107
Lbl106:
la $v0, st60
sw $v0,420($sp)
lw $t0,420($sp)
move $v0, $t0
sw $v0,1072($sp)
Lbl107:
lw $t0,1072($sp)
move $v0, $t0
sw $v0,1076($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 1080
jr $ra
f40:
addi $sp, $sp, -100
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st82
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
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st83
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
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
sw $v0,36($sp)
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
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,44($sp)
lw $t0,44($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st84
sw $v0,56($sp)
lw $t0,56($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,48($sp)
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
sw $v0,60($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,64($sp)
la $v0, st85
sw $v0,72($sp)
lw $t0,64($sp)
lw $t1,72($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,80($sp)
lw $t0,80($sp)
bgtz $t0, Lbl108
move $t0, $zero
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,92($sp)
b Lbl109
Lbl108:
li $t0,1
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,92($sp)
Lbl109:
lw $t0,92($sp)
move $v0, $t0
sw $v0,96($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 100
jr $ra
f41:
addi $sp, $sp, -100
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,8($sp)
lw $t0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st86
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
move $t0,$a0
move $v0, $t0
sw $v0,24($sp)
lw $t0,24($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st87
sw $v0,32($sp)
lw $t0,32($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,24($sp)
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
sw $v0,36($sp)
move $t0,$a0
move $v0, $t0
sw $v0,40($sp)
lw $t0,40($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st88
sw $v0,48($sp)
lw $t0,48($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,40($sp)
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
sw $v0,52($sp)
move $t0,$a0
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
lw $t0, 0($a0)
lw $t0,24($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,64($sp)
la $v0, st89
sw $v0,72($sp)
lw $t0,64($sp)
lw $t1,72($sp)
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
move $a0, $t0
move $a1, $t1
jal .Str.stringcomparison
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
sw $v0,80($sp)
lw $t0,80($sp)
bgtz $t0, Lbl110
li $t0,1
move $v0, $t0
sw $v0,88($sp)
lw $t0,88($sp)
move $v0, $t0
sw $v0,92($sp)
b Lbl111
Lbl110:
move $t0, $zero
move $v0, $t0
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,92($sp)
Lbl111:
lw $t0,92($sp)
move $v0, $t0
sw $v0,96($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 100
jr $ra
f42:
addi $sp, $sp, -8
sw $ra, 0($sp)
move $t0,$a0
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $t0,CellularAutomatonclase
lw $t0,0($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal $t0
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,4($sp)
li $t0,0
move $v0, $t0
sw $v0,20($a0)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
f43:
addi $sp, $sp, -12
sw $ra, 0($sp)
la $v0, st90
sw $v0,8($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 12
jr $ra
f44:
addi $sp, $sp, -164
sw $ra, 0($sp)
move $t0,$a0
move $v0, $t0
sw $v0,12($sp)
lw $t0,12($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st91
sw $v0,20($sp)
lw $t0,20($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,12($sp)
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
sw $v0,24($sp)
move $t0,$a0
move $v0, $t0
sw $v0,28($sp)
lw $t0,28($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
la $v0, st92
sw $v0,36($sp)
lw $t0,36($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,28($sp)
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
sw $v0,40($sp)
Lbl112:
move $t0,$a0
move $v0, $t0
sw $v0,44($sp)
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,44($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,108($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,48($sp)
lw $t0,48($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1
sw $v0,56($sp)
lw $t0,56($sp)
bgtz $t0, Lbl113
move $t0, $zero
move $v0, $t0
sw $v0,60($sp)
lw $t0,60($sp)
move $v0, $t0
sw $v0,4($sp)
move $t0,$a0
move $v0, $t0
sw $v0,64($sp)
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,64($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,100($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,68($sp)
lw $t0,68($sp)
move $v0, $t0
sw $v0,8($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0,20
syscall
la $t0, CellularAutomatonclase
sw $t0, 0($v0)
sw $zero, 4($v0)
sw $zero, 8($v0)
sw $zero, 12($v0)
sw $zero, 16($v0)
lw $a0, 0($sp)
addi $sp, $sp, 4
sw $v0,76($sp)
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,8($sp)
move $v0, $t0
sw $v0,80($sp)
lw $t0,80($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,76($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,40($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,84($sp)
lw $t0,84($sp)
move $v0, $t0
sw $v0,72($sp)
lw $t0,72($sp)
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
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,92($sp)
Lbl114:
lw $t0,4($sp)
move $v0, $t0
sw $v0,96($sp)
lw $t0,96($sp)
addi $v0 ,$t0, 1
li $t1, 2
rem $v0, $v0, $t1
sw $v0,104($sp)
lw $t0,104($sp)
bgtz $t0, Lbl115
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
lw $t0, 0($a0)
lw $t0,104($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,112($sp)
lw $t0,112($sp)
bgtz $t0, Lbl116
li $t0,1
move $v0, $t0
sw $v0,132($sp)
lw $t0,132($sp)
move $v0, $t0
sw $v0,4($sp)
lw $t0,4($sp)
move $v0, $t0
sw $v0,136($sp)
b Lbl117
Lbl116:
lw $t0,72($sp)
move $v0, $t0
sw $v0,116($sp)
lw $t0,116($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0,116($sp)
addi $sp, $sp, -4
sw $a0, 0($sp)
move $a0,$t0
lw $t0, 0($a0)
lw $t0,96($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,120($sp)
lw $t0,72($sp)
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
lw $t0, 0($a0)
lw $t0,44($t0)
addi $sp, $sp, -4
sw $ra, 0($sp)
jalr $t0, $ra
lw $ra, 0($sp)
addi $sp, $sp, 4
sw $v0,128($sp)
lw $t0,128($sp)
move $v0, $t0
sw $v0,136($sp)
Lbl117:
lw $t0,136($sp)
move $v0, $t0
sw $v0,140($sp)
b Lbl114
Lbl115:
li $t0,0
move $v0, $t0
sw $v0,148($sp)
b Lbl112
Lbl113:
li $t0,0
move $v0, $t0
sw $v0,156($sp)
move $t0,$a0
move $v0, $t0
sw $v0,160($sp)
lw $v0, 0($sp)
lw $ra, 0($sp)
addi $sp, $sp, 164
jr $ra
