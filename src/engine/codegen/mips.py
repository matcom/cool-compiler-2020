from enum import Enum


class Registers:
    zero = '$zero'  # Constant 0
    at = '$at'  # Reserved for assembler
    v0 = '$v0'  # Expression evaluation and
    v1 = '$v1'  # results of a function
    a0 = '$a0'  # Argument 1
    a1 = '$a1'  # Argument 2
    a2 = '$a2'  # Argument 3
    a3 = '$a3'  # Argument 4
    t0 = '$t0'  # Temporary(not preserved across call)
    t1 = '$t1'  # Temporary(not preserved across call)
    t2 = '$t2'  # Temporary(not preserved across call)
    t3 = '$t3'  # Temporary(not preserved across call)
    t4 = '$t4'  # Temporary(not preserved across call)
    t5 = '$t5'  # Temporary(not preserved across call)
    t6 = '$t6'  # Temporary(not preserved across call)
    t7 = '$t7'  # Temporary(not preserved across call)
    s0 = '$s0'  # Saved temporary(preserved across call)
    s1 = '$s1'  # Saved temporary(preserved across call)
    s2 = '$s2'  # Saved temporary(preserved across call)
    s3 = '$s3'  # Saved temporary(preserved across call)
    s4 = '$s4'  # Saved temporary(preserved across call)
    s5 = '$s5'  # Saved temporary(preserved across call)
    s6 = '$s6'  # Saved temporary(preserved across call)
    s7 = '$s7'  # Saved temporary(preserved across call)
    t8 = '$t8'  # Temporary(not preserved across call)
    t9 = '$t9'  # Temporary(not preserved across call)
    k0 = '$k0'  # Reserved for OS kernel
    k1 = '$k1'  # Reserved for OS kernel
    gp = '$gp'  # Pointer to global area
    sp = '$sp'  # Stack pointer
    fp = '$fp'  # Frame pointer
    ra = '$ra'  # Return address(used by function call)


class ArithmOperations(Enum):
    Add = 1
    Sub = 2
    Mul = 3
    Div = 4

# class MipsLabel:


class MipsCode:
    def __init__(self):
        pass
    # Data Segmente

    # IO
    def print_str(self, _str):
        '''
        $v0
        $a0
        '''
        code = [
            'li $v0, 4   # system call code for print_str',
            f'la $a0, {_str} # address of string to print',
            'syscall     # print the string',
        ]
        return code

    def print_int(self, _int):
        '''
        $v0
        $a0
        '''
        code = [
            'li $v0, 1   # system call code for print_int',
            f'la $a0, {_int}  # address of string to print',
            'syscall     # print the string',
        ]
        return code

    # Arithmetic and Logical Operations
    def abs(self, rdest, rsrc):
        '''
        Absolute Value
        '''
        return f'abs {rdest}, {rsrc}'

    def addiu(self, rdest, rsrc, constant):
        '''
        Addition Immediate (without overflow)
        '''
        return f'addiu {rdest}, {rsrc}, {constant}'

    def addi(self, rdest, rsrc, constant):
        '''
        Addition Immediate (with overflow)
        '''
        return f'addi {rdest}, {rsrc}, {constant}'

    def add(self, rdest, rsrc, src):
        '''

        Addition (with overflow)
        '''
        return f'add {rdest}, {rsrc}, {src}'

    def addu(self, rdest, rsrc, src):
        '''
        Addition (without overflow)
        '''
        return f'addu {rdest}, {rsrc}, {src}'

    def and_(self, rdest, rsrc1, rsrc2):
        '''
        AND
        '''
        return f'and {rdest}, {rsrc1}, {rsrc2}'

    def andi(self, rdest, rsrc, constant):
        '''
        ANDI Inmediate
        '''
        return f'andi {rdest}, {rsrc}, {constant}'

    def div(self, rdest_src, rsrc1, rsrc2=None):
        '''
        Divide (signed)
        '''
        if rsrc2 is None:
            return f'div {rdest_src}, {rsrc1}'
        else:
            return f'div {rdest_src}, {rsrc1}, {rsrc2}'

    def divu(self, rdest_src, rsrc1, rsrc2=None):
        '''
        Divide (unsigned)
        '''
        if rsrc2 is None:
            return f'divu {rdest_src}, {rsrc1}'
        else:
            return f'divu {rdest_src}, {rsrc1}, {rsrc2}'

    def mult(self, rdest, rsrc1):
        '''
        Multiply
        '''
        return f'mult {rdest}, {rsrc1}'

    def neg(self, rdest, rsrc):
        '''
        Negate Value (with overflow)
        '''
        return f'neg {rdest}, {rsrc}'

    def negu(self, rdest, rsrc):
        '''
        Negate Value (without overflow)
        '''
        return f'negu {rdest}, {rsrc}'

    def not_(self, rdest, rsrc):
        '''
        Not
        '''
        return 'or {rdest}, {rsrc}'

    def or_(self, rdest, rsrc1, src2):
        '''
        Or
        '''
        return 'or {rdest}, {rsrc1}, {rsrc2}'

    def nor(self, rdest, rsrc1, src2):
        '''
        Nor
        '''
        return 'nor {rdest}, {rsrc1}, {rsrc2}'

    def ori(self, rdest, rsrc1, constant):
        '''
        Or Immediate
        '''
        return 'ori {rdest}, {rsrc1}, {constant}'

    def rem(self, rdest, rsrc1, src2):
        '''
        Remainder
        '''
        return f'rem {rdest}, {rsrc1}, {src2}'

    def remu(self, rdest, rsrc1, src2):
        '''
        Unsigned Remainder
        '''
        return f'remu {rdest}, {rsrc1}, {src2}'

    def sub(self, rdest, rsrc1, src2):
        '''
        Substract (with overflow)
        '''
        return f'sub {rdest}, {rsrc1}, {src2}'

    def subu(self, rdest, rsrc1, src2):
        '''
        Substract (without overflow)
        '''
        return f'subu {rdest}, {rsrc1}, {src2}'

    # Constant Manipulating
    def li(self, rdest, constant):
        '''
        Load Immediate 
        '''
        return f'li {rdest}, {constant}'

    # Comparison Instructions
    def seq(self, rdest, rsrc1, src2):
        '''
        Set Equal
        '''
        return f'seq {rdest}, {rsrc1}, {src2}'

    def sge(self, rdest, rsrc1, src2):
        '''
        Set Greater Than Equal er Than Equal Unsigned 
        '''
        return f'sge {rdest}, {rsrc1}, {src2}'

    def sle(self, rdest, rsrc1, src2):
        '''
        Set Less Than Equal Than Equal Unsigned 
        '''
        return f'sle {rdest}, {rsrc1}, {src2}'

    def slt(self, rdest, rsrc1, src2):
        '''
        Set Less Than
        '''
        return f'slt {rdest}, {rsrc1}, {src2}'
    # Branch and Jump

    def b(self, label):
        '''
        Branch instruction
        '''
        return f'b {label}'

    def beq(self, rsrc1, src2, label):
        '''
        Branch on Equal
        '''
        return f'beq {rsrc1}, {src2}, {label}'

    def beqz(self, rsrc1, src2, label):
        '''
        Branch on Equal Zero
        '''
        return f'beqz {rsrc1}, {src2}, {label}'

    def bne(self, rsrc1, src2, label):
        '''
        Branch on Not Equal Zero
        '''
        return f'bne {rsrc1}, {src2}, {label}'

    def j(self, label):
        '''
        Jump
        '''
        return f'j {label}'

    def jal(self, label):
        '''
        Jump and Link
        '''
        return f'jal {label}'

    def jr(self, rsrc):
        '''
        Jump Register
        '''
        return f'jr {rsrc}'

    # Load Instructions
    def la(self, rdest, address):
        '''
        Load Address
        '''
        return f'la {rdest}, {address}'

    def lb(self, rdest, address):
        '''
        Load Byte
        '''
        return f'la {rdest}, {address}'

    def lw(self, reg, memory, offset):
        '''
        Load Word
        '''
        return f'lw {reg}, {offset}({reg})'

    def ld(self, rdest, address):
        '''
        Load Double-Word
        '''
        return f'la {rdest}, {address}'

    # Store Instructions
    def sb(self, rsrc, address):
        '''
        Store Byte
        '''
        return f'sb {rsrc}, {address}'

    def sw(self, rsrc, address):
        '''
        Store Word
        '''
        return f'sw {rsrc}, {address}'

    def sd(self, rsrc, address):
        '''
        Store Double-Word
        '''
        return f'sd {rsrc}, {address}'

    # Data Movement Instructions
    def move(self, rdest, rsrc):
        '''
        Move
        '''
        return f'move {rdest}, {rsrc}'

    def mfhi(self, rdest):
        '''
        Move from `hi`
        '''
        return f'mfhi {rdest}'

    def mflo(self, rdest):
        '''
        Move from `lo`
        '''
        return f'mflo {rdest}'

    def syscall(self):
        '''
        Syscall
        '''
        return 'syscall'










