inherit:
beq $a0, $a1, inherit_true
beq $a0, $zero, inherit_false
lw $a0, ($a0)
j inherit
inherit_true:
li $v0, 1
jr $ra
inherit_false:
li $v0, 0
jr $ra
