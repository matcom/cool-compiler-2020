import visitor

class MipsNode:
    pass

class MipsProgramNode(MipsNode):
    def __init__(self, dotdata, dotcode):
        self.dotdata = dotdata
        self.dotcode = dotcode

# string
class MipsStringNode(MipsNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class MipsWordNode(MipsNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

# jumps
class MipsJumpNode(MipsNode):
    def __init__(self, label):
        self.label = label

class MipsJumpAtAddressNode(MipsJumpNode):
    pass

class MipsJRNode(MipsJumpNode):
    pass

# stack
class MipsLWNode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest

class MipsLINode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest

class MipsLANode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest

class MipsSWNode(MipsNode):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


# syscall
class MipsSyscallNode(MipsNode):
    pass


# move
class MipsMoveNode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest


# arithmetic
class MipsAddNode(MipsNode):
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

class MipsAddiuNode(MipsNode):
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

# label
class MipsLabelNode(MipsNode):
    def __init__(self, name):
        self.name = name

class MipsCommentNode(MipsNode):
    def __init__(self, comment):
        self.comment = '\n #' + comment + '\n'

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(MipsProgramNode)
        def visit(self, node):
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotdata += '''
            _error1:    .asciiz     "Halt program because abort"
            _buffer:    .space      1024
             '''    
            
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)
            dotcode += '''\n

function_Ctr_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_Ctr_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_type_name_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            lw $a0, 4($fp)   
            lw  $a0 0($a0)      
            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra

function_abort_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            la $a0, _error1
            li $v0, 4
            syscall
            li $v0, 10
            syscall

function_copy_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 4($fp)
            lw $a0, 0($a0)
            la $t0, Int_name

            bne $a0, $t0, not_int
            lw $a0, 4($fp)
            lw $a0, 8($a0)
            j end

        not_int:
            lw $a0, 4($fp)
            lw $a0, 0($a0)
            la $t0, Bool_name

            bne $a0, $t0, not_bool
            lw $a0, 4($fp)
            lw $a0, 8($a0)
            j end

        not_bool:
            lw $a0, 4($fp)
            lw $a0, 0($a0)
            la $t0, String_name

            bne $a0, $t0, not_string
            lw $a0, 4($fp)
            lw $a0, 8($a0)
            j end
        
        not_string:
            lw $a0, 4($fp)
            move $t2, $a0 
            lw $a0, 4($a0)
            move $t1, $a0

            li $v0, 9
            syscall

            move $a0, $v0

        copy:
            lw $t0, 0($t2)
            sw $t0, 0($a0)
            addiu $a0, $a0, 4
            addiu $t2, $t2, 4
            addiu $t1, $t1, -4
            bne $t1, $zero, copy
            
            move $a0, $v0

        end:
            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_length_at_String:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $s0, 4($fp)
            li $a0, -1

        length:
            lb $t0, ($s0)
            addiu $a0, $a0, 1
            addiu $s0, $s0, 1
            bne $t0, $zero, length
            
            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_concat_at_String:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $s1, 4($fp)
            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $s1, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String
            
            sw $a0, 0($sp)
            addiu $sp, $sp, -4

            lw $s1, 8($fp)
            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $s1, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String

            lw $t7, 4($sp)
            addiu $sp, $sp, 4

            move $t6, $a0
            add $a0, $t7, $t6
            addiu $a0, $a0, 1

            li $v0, 9
            syscall

            move $t0, $v0

            lw $s1, 4($fp)
        copy_self:
            lb $t5, ($s1)
            beq $t5, $zero, end_copy_self
            sb $t5, ($t0)
            addiu $s1, $s1, 1
            addiu $t0, $t0, 1
            j copy_self

        end_copy_self:
            lw $s1, 8($fp)

        copy_given:
            lb $t5, ($s1)
            sb $t5, ($t0)
            addiu $s1, $s1, 1
            addiu $t0, $t0, 1
            bne $t5, $zero, copy_given


            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 16
            lw $fp, 0($sp)
            jr $ra 


function_substr_at_String:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 12($fp)
            addiu $a0, $a0, 1
            li $v0, 9
            syscall

            move $t0, $v0

            lw $s1, 4($fp)
            lw $t1, 8($fp)
            add $s1, $s1, $t1

            lw $t1, 12($fp)

        substr:
            lb $t5, ($s1)
            sb $t5, ($t0)
            addiu $s1, $s1, 1
            addiu $t0, $t0, 1
            addiu $t1, $t1, -1
            bne $t1, $zero, substr

            sb $zero, ($t0)
            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 20
            lw $fp, 0($sp)
            jr $ra 


function_out_string_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 8($fp)
            li $v0, 4
            syscall

            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 16
            lw $fp, 0($sp)
            jr $ra 

function_out_int_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 8($fp)
            li $v0, 1
            syscall

            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 16
            lw $fp, 0($sp)
            jr $ra 

function_in_int_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 4($fp)
            li $v0, 5
            syscall

            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_in_string_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            la $a0, _buffer
            li $a1, 1024

            li $v0, 8
            syscall

            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $a0, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String

            addiu $a0, $a0, 1
            li $v0, 9
            syscall

            move $t0, $v0
            la $a0, _buffer

        IO_copy:
            lb $t1, ($a0)
            sb $t1, ($t0)
            addiu $a0, $a0, 1
            addiu $t0, $t0, 1
            bne $t1, $zero, IO_copy

            addiu $t0, $t0, -2
            sb $zero, ($t0)

            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

            '''

            return f'.data\n{dotdata}\n\n.text\n{dotcode}'

        @visitor.when(MipsStringNode)
        def visit(self, node):
            return f'\t\t\t{node.name}:     .asciiz      "{node.value}"'

        @visitor.when(MipsWordNode)
        def visit(self, node):
            return f'\t\t\t{node.name}:     .word     {node.value}'

        # jumps
        @visitor.when(MipsJumpNode)
        def visit(self, node):
            return f'\t\t\tj {node.label}'

        @visitor.when(MipsJumpAtAddressNode)
        def visit(self, node):
            return f'\t\t\tjal {node.label}'

        @visitor.when(MipsJRNode)
        def visit(self, node):
            return f'\t\t\tjr {node.label}'

        # stack
        @visitor.when(MipsLWNode)
        def visit(self, node):
            return f'\t\t\tlw {node.dest}, {node.src}'

        @visitor.when(MipsLINode)
        def visit(self, node):
            return f'\t\t\tli {node.dest}, {node.src}'

        @visitor.when(MipsLANode)
        def visit(self, node):
            return f'\t\t\tla {node.dest}, {node.src}'

        @visitor.when(MipsSWNode)
        def visit(self, node):
            return f'\t\t\tsw {node.src}, {node.dest}'


        # syscall
        @visitor.when(MipsSyscallNode)
        def visit(self, node):
            return '\t\t\tsyscall'


        # move
        @visitor.when(MipsMoveNode)
        def visit(self, node):
            return f'\t\t\tmove {node.dest}, {node.src}'


        # arithmetic
        @visitor.when(MipsAddNode)
        def visit(self, node):
            return f'\t\t\tadd {node.param1}, {node.param2}, {node.param3}'

        @visitor.when(MipsAddiuNode)
        def visit(self, node):
            return f'\t\t\taddiu {node.param1}, {node.param2}, {node.param3}'


        # label
        @visitor.when(MipsLabelNode)
        def visit(self, node):
            return f'{node.name}:'
        
        @visitor.when(MipsCommentNode)
        def visit(self, node):
            return node.comment

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))