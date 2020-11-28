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


class MipsCode:
    def __init__(self):
        pass

    def print_str(self, _str):
        '''
        $v0
        $a0
        '''
        code = [
            'li $v0, 4   # system call code for print_str',
            f'la $a0, {_str} # address of string to print' ,
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
            f'la $a0, {_int}  # address of string to print' ,
            'syscall     # print the string',
        ]
        return code

    def abs(self, rdest, rsrc):
        '''
        Absolute Value
        '''
        return f'abs {rdest}, {rsrc}'

    def lw(self, reg, memory, offset):
        return f'lw {reg},{offset}({reg})'

    def addiu(self, rdest, rsrc, constant):
        '''
        Addition Immediate (without overflow)
        '''
        return f'addiu {rdest}, {offset}, {constant}'

    def add(self, rdest, rsrc, src):
        '''
        
        '''
