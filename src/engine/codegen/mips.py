from enum import Enum
from typing import Dict, List
from .cil_ast import TypeNode


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


class TypeData:
    def __init__(self, type_number: int, typex: TypeNode):
        self.type: int = type_number
        self.str: str = typex.name_dir
        self.attr_offsets: Dict[str, int] = dict()
        self.func_offsets: Dict[str, int] = dict()
        self.func_names: Dict[str, str] = dict()

        # Calculate offsets for attributes and functions
        for idx, feature in enumerate(typex.features):
            if isinstance(feature, str):
                # The plus 2 is because the two first elementes
                # in the instance are the type_int and the type_str_dir.
                # Also enumerate starts with 0
                self.attr_offsets[feature] = idx + 2
            else:
                func_name, long_name = feature
                self.func_offsets[func_name] = idx + 2
                self.func_names[func_name] = long_name


class MipsLabel(str, Enum):

    word = ".word"
    half = ".half"
    byte = ".byte"
    ascii_ = ".ascii"
    asciiz = ".asciiz"
    space = ".space"
    aling = ".align"
    text = ".text"
    data = ".data"


reg = Registers


class MipsCode:
    def __init__(self):
        self.dotdata = []
        self.dotcode = []

    # Meta Functions

    def compile(self):
        return '\n'.join([MipsLabel.data] + self.dotdata + [MipsLabel.text] + self.dotcode)

    def _write(self, line):
        self.dotcode.append(line)

    def _write_data(self, line):
        self.dotdata.append(line)

    def data_label(self, lname):
        self._write_data(f'{lname}')

    def empty_line(self):
        self._write('')

    def asciiz(self, string):
        self._write_data(f'.asciiz "{string}"')

    def push(self, register: Registers):
        self.addi(Registers.sp, Registers.sp, -8)
        self.store_memory(register, self.offset(Registers.sp))

    def pop(self, register: Registers):
        """
        First,  load from to address `0($sp)`
        and then write `addi $sp ,  $sp ,  8`
        to restore the stack pointer
        """
        self.load_memory(register, self.offset(reg.sp))
        self.addi(reg.sp, reg.sp, 8)

    def load_memory(self, dst: Registers, address: str):
        """
        Load from a specific address a 32 bits register
        """
        self.lw(reg.t8, address)
        self.sll(reg.t8, reg.t8, 16)
        self.la(reg.t7, address)
        self.addi(reg.t7, reg.t7, 4)
        self.lw(reg.t9, self.offset(reg.t7))
        self.or_(dst, reg.t8, reg.t9)

    def store_memory(self, src: Registers, address: str):
        """
        Write to a specific address a 32 bits register
        """
        self.la(reg.t8, address)

        self.srl(reg.t9, src, 16)

        self.sw(reg.t9, self.offset(reg.t8))  # store high bits
        self.sw(src, self.offset(reg.t8, 4))  # store low bits

    # System Calls

    def syscall(self, code: int):
        self.li(Registers.v0, code)
        self._write('syscall')

    def offset(self, r: Registers, offset: int = 0):
        return f"{offset}({r})"

    def comment(self, text: str):
        self._write(f"# {text}")

    def label(self, name: str):
        self._write(f"{name}:")

    def print_str(self, _str):
        return self.syscall(4)

    def print_int(self, _int):
        return self.syscall(1)

    def read_int(self):
        return self.syscall(5)

    def read_string(self):
        return self.syscall(8)

    def sbrk(self):
        return self.syscall(9)

    def exit(self):
        return self.syscall(10)

    # Arithmetic and Logical Operations
    def abs(self, rdest, rsrc):
        '''
        Absolute Value
        '''
        self._write(f'abs {rdest}, {rsrc}')

    def addiu(self, rdest, rsrc, constant):
        '''
        Addition Immediate (without overflow)
        '''
        self._write(f'addiu {rdest}, {rsrc}, {constant}')

    def addi(self, rdest, rsrc, constant):
        '''
        Addition Immediate (with overflow)
        '''
        self._write(f'addi {rdest}, {rsrc}, {constant}')

    def add(self, rdest, rsrc, src):
        '''

        Addition (with overflow)
        '''
        self._write(f'add {rdest}, {rsrc}, {src}')

    def addu(self, rdest, rsrc, src):
        '''
        Addition (without overflow)
        '''
        self._write(f'addu {rdest}, {rsrc}, {src}')

    def and_(self, rdest, rsrc1, rsrc2):
        '''
        AND
        '''
        self._write(f'and {rdest}, {rsrc1}, {rsrc2}')

    def andi(self, rdest, rsrc, constant):
        '''
        ANDI Inmediate
        '''
        self._write(f'andi {rdest}, {rsrc}, {constant}')

    def div(self, rdest_src, rsrc1, rsrc2=None):
        '''
        Divide (signed)
        '''
        if rsrc2 is None:
            self._write(f'div {rdest_src}, {rsrc1}')
        else:
            self._write(f'div {rdest_src}, {rsrc1}, {rsrc2}')

    def divu(self, rdest_src, rsrc1, rsrc2=None):
        '''
        Divide (unsigned)
        '''
        if rsrc2 is None:
            self._write(f'divu {rdest_src}, {rsrc1}')
        else:
            self._write(f'divu {rdest_src}, {rsrc1}, {rsrc2}')

    def mult(self, rdest, rsrc1):
        '''
        Multiply
        '''
        self._write(f'mult {rdest}, {rsrc1}')

    def neg(self, rdest, rsrc):
        '''
        Negate Value (with overflow)
        '''
        self._write(f'neg {rdest}, {rsrc}')

    def negu(self, rdest, rsrc):
        '''
        Negate Value (without overflow)
        '''
        self._write(f'negu {rdest}, {rsrc}')

    def not_(self, rdest, rsrc):
        '''
        Not
        '''
        self._write(f'or {rdest}, {rsrc}')

    def or_(self, rdest, rsrc1, src2):
        '''
        Or
        '''
        self._write(f'or {rdest}, {rsrc1}, {src2}')

    def nor(self, rdest, rsrc1, src2):
        '''
        Nor
        '''
        self._write(f'nor {rdest}, {rsrc1}, {src2}')

    def ori(self, rdest, rsrc1, constant):
        '''
        Or Immediate
        '''
        self._write(f'ori {rdest}, {rsrc1}, {constant}')

    def rem(self, rdest, rsrc1, src2):
        '''
        Remainder
        '''
        self._write(f'rem {rdest}, {rsrc1}, {src2}')

    def remu(self, rdest, rsrc1, src2):
        '''
        Unsigned Remainder
        '''
        self._write(f'remu {rdest}, {rsrc1}, {src2}')

    def sub(self, rdest, rsrc1, src2):
        '''
        Substract (with overflow)
        '''
        self._write(f'sub {rdest}, {rsrc1}, {src2}')

    def subu(self, rdest, rsrc1, src2):
        '''
        Substract (without overflow)
        '''
        self._write(f'subu {rdest}, {rsrc1}, {src2}')

    def sll(self, dst, rl, value: int):
        self._write(f"sll {dst}, {rl}, {value}")

    # Constant Manipulating
    def li(self, rdest, constant):
        '''
        Load Immediate 
        '''
        self._write(f'li {rdest}, {int(constant)}')

    # Comparison Instructions
    def seq(self, rdest, rsrc1, src2):
        '''
        Set Equal
        '''
        self._write(f'seq {rdest}, {rsrc1}, {src2}')

    def sge(self, rdest, rsrc1, src2):
        '''
        Set Greater Than Equal er Than Equal Unsigned 
        '''
        self._write(f'sge {rdest}, {rsrc1}, {src2}')

    def sle(self, rdest, rsrc1, src2):
        '''
        Set Less Than Equal Than Equal Unsigned 
        '''
        self._write(f'sle {rdest}, {rsrc1}, {src2}')

    def slt(self, rdest, rsrc1, src2):
        '''
        Set Less Than
        '''
        self._write(f'slt {rdest}, {rsrc1}, {src2}')

    def slti(self, rdest, rsrc1, value):
        '''
        Set Less Than Immediate
        '''
        self._write(f'slti {rdest}, {rsrc1}, {value}')

    def srl(self, rdest, rsrc1, src2):
        '''
        Shift Right Logical
        '''
        self._write(f'srl {rdest}, {rsrc1}, {src2}')

        # Branch and Jump

    def b(self, label):
        '''
        Branch instruction
        '''
        self._write(f'b {label}')

    def beq(self, rsrc1, src2, label):
        '''
        Branch on Equal
        '''
        self._write(f'beq {rsrc1}, {src2}, {label}')

    def beqz(self, rsrc1, src2, label):
        '''
        Branch on Equal Zero
        '''
        self._write(f'beqz {rsrc1}, {src2}, {label}')

    def bne(self, rsrc1, src2, label):
        '''
        Branch on Not Equal Zero
        '''
        self._write(f'bne {rsrc1}, {src2}, {label}')

    def j(self, label):
        '''
        Jump
        '''
        self._write(f'j {label}')

    def jal(self, label):
        '''
        Jump and Link
        '''
        self._write(f'jal {label}')

    def jr(self, rsrc):
        '''
        Jump Registers
        '''
        self._write(f'jr {rsrc}')

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
        self._write(f'lb {rdest}, {address}')

    def lw(self, reg, address):
        '''
        Load Word
        '''
        self._write(f'lw {reg}, {address}')

    def ld(self, rdest, address):
        '''
        Load Double-Word
        '''
        self._write(f'la {rdest}, {address}')

    # Store Instructions
    def sb(self, rsrc, address):
        '''
        Store Byte
        '''
        self._write(f'sb {rsrc}, {address}')

    def sw(self, rsrc, address):
        '''
        Store Word
        '''
        self._write(f'sw {rsrc}, {address}')

    def sd(self, rsrc, address):
        '''
        Store Double-Word
        '''
        self._write(f'sd {rsrc}, {address}')

    # Data Movement Instructions
    def move(self, rdest, rsrc):
        '''
        Move
        '''
        self._write(f'move {rdest}, {rsrc}')

    def mfhi(self, rdest):
        '''
        Move from `hi`
        '''
        self._write(f'mfhi {rdest}')

    def mflo(self, rdest):
        '''
        Move from `lo`
        '''
        self._write(f'mflo {rdest}')
