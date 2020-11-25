from enum import Enum


class Register(str, Enum):
    # stores value 0; cannot be modified
    zero = "$zero"
    # used for system calls and procedure return values
    v0 = "$v0"
    v1 = "$v1"
    # used for passing arguments to procedures
    a0 = "$a0"
    a1 = "$a1"
    a2 = "$a2"
    a3 = "$a3"
    # used for local storage; calling procedure saves these
    t0 = "$t0"
    t1 = "$t1"
    t2 = "$t2"
    t3 = "$t3"
    t4 = "$t4"
    t5 = "$t5"
    t6 = "$t6"
    t7 = "$t7"
    t8 = "$t8"
    t9 = "$t9"
    # used for local storage; called procedure saves these
    s0 = "$s0"
    s1 = "$s1"
    s2 = "$s2"
    s3 = "$s3"
    s4 = "$s4"
    s5 = "$s5"
    s6 = "$s6"
    s7 = "$s7"
    sp = "$sp"  # stack pointer
    fp = "$fp"  # frame pointer; primarily used during stack manipulations
    ra = "$ra"  # used to store return address in procedure call
    gp = "$gp"  # pointer to area storing global data (data segment)
    at = "$at"  # reserved for use by the assembler
    # reserved for use by OS kernel
    k0 = "$k0"
    k1 = "$k1"


class Directive(str, Enum):
    word = ".word"
    half = ".half"
    byte = ".byte"
    ascii = ".ascii"
    asciiz = ".asciiz"
    space = ".space"
    aling = ".align"


syscall = "syscall"
Reg = Register


class Mips:
    def __init__(self):
        self.DOTTEXT = []
        self.DOTDATA = []

    def autowrite(func):
        """
        Autowrite a instruction when execute string return function
        """
        def inner(*args, **kwargs):
            instructions = func(*args, **kwargs)
            if instructions is list:
                for instruction in instructions:
                    args[0].write_inst(instruction)
            else:
                args[0].write_inst(instructions)
        return inner

    def autowritedata(func):
        """
        Autowrite a instruction when execute string return function
        """
        def inner(*args, **kwargs):
            instructions = func(*args, **kwargs)
            if instructions is list:
                for instruction in instructions:
                    args[0].write_data(instruction)
            else:
                args[0].write_data(instructions)
        return inner

    def write_inst(self, instruction: str, tabs=0):
        self.DOTTEXT.append(f'{instruction}')

    def write_data(self, data: str, tabs=0):
        self.DOTDATA.append(f'{data}')

    def compile(self):
        return '\n'.join(['.data'] + self.DOTDATA + ['.text'] + self.DOTTEXT)

    def push(self, register: Register):
        self.addi(Register.sp, Register.sp, -8)
        self.store_memory(register, self.offset(Register.sp))

    def pop(self, register: Register):
        """
        First, load from to address `0($sp)`
        and then write `addi $sp , $sp , 8`
        to restore the stack pointer
        """
        self.load_memory(register, self.offset(Reg.sp))
        self.addi(Reg.sp, Reg.sp, 8)

    def load_memory(self, register: Register, address: str):
        """
        Load from a specific address a 32 bits register
        """
        self.lw(Reg.t0, address)
        self.sll(Reg.t0, Reg.t0, 16)
        self.lw(Reg.t1, f"{address} + 4")
        self.orr(register, Reg.t0, Reg.t1)

    def store_memory(self, register: Register, address: str):
        """
        Write to a specific address a 32 bits register
        """
        self.sw(Reg.t1, f"{address} + 4")
        self.srl(Reg.t1, Reg.t1, 16)
        self.sw(Reg.t0, address)
        self.orr(register, Reg.t0, Reg.t1)

    # Arithmetics
    @autowrite
    def add(self, dst: Register, rl: Register, rr: Register):
        return f"add {dst},{rl},{rr}"

    @autowrite
    def sub(self, dst: Register, rl: Register, rr: Register):
        return f"sub {dst},{rl},{rr}"

    @autowrite
    def addi(self, dst: Register, rl: Register, value: int):
        return f"addi {dst},{rl},{value}"

    @autowrite
    def addu(self, dst: Register, rl: Register, rr: Register):
        return f"addu {dst},{rl},{rr}"

    @autowrite
    def subu(self, dst: Register, rl: Register, rr: Register):
        return f"subu {dst},{rl},{rr}"

    @autowrite
    def addiu(self, dst: Register, rl: Register, value: int):
        return f"addiu {dst},{rl},{value}"

    @autowrite
    def mul(self, dst: Register, rl: Register, rr: Register):
        return f"mul {dst},{rl},{rr}"

    @autowrite
    def mult(self, rl: Register, rr: Register):
        return f"mult {rl},{rr}"

    @autowrite
    def div(self, rl: Register, rr: Register):
        return f"div {rl},{rr}"

    # Logical:
    @autowrite
    def andd(self, dst: Register, rl: Register, rr: Register):
        return f"and {dst},{rl},{rr}"

    @autowrite
    def orr(self, dst: Register, rl: Register, rr: Register):
        return f"or {dst},{rl},{rr}"

    @autowrite
    def andi(self, dst: Register, rl: Register, value: int):
        return f"andi {dst},{rl},{value}"

    # TODO: Check this instrucction
    @autowrite
    def ori(self, dst: Register, rl: Register, value: int):
        return f"or {dst},{rl},{value}"

    @autowrite
    def sll(self, dst: Register, rl: Register, value: int):
        return f"sll {dst},{rl},{value}"

    @autowrite
    def srl(self, dst: Register, rl: Register, value: int):
        return f"srl {dst},{rl},{value}"

    # DataTransfer:
    @autowrite
    def lw(self, dst: Register, address: str):
        return f"lw {dst},{address}"

    @autowrite
    def sw(self, dst: Register, address: str):
        return f"sw {dst},{address}"

    @autowrite
    def lui(self, dst: Register, value: int):
        return f"lw {dst},{value}"

    @autowrite
    def la(self, dst: Register, label: str):
        return f"la {dst},{label}"

    @autowrite
    def li(self, dst: Register, value: int):
        return f"li {dst},{value}"

    @autowrite
    def mfhi(self, dst: Register):
        return f"mfhi {dst}"

    @autowrite
    def mflo(self, dst: Register):
        return f"mflo {dst}"

    @autowrite
    def move(self, dst: Register, rl: Register):
        return f"move {dst},{rl}"

    # Brancing
    @autowrite
    def beq(self, rl: Register, rr: Register, address: str):
        return f"beq {rl},{rr},{address}"

    @autowrite
    def bne(self, rl: Register, rr: Register, address: str):
        return f"bne {rl},{rr},{address}"

    @autowrite
    def bgt(self, rl: Register, rr: Register, address: str):
        return f"bgt {rl},{rr},{address}"

    @autowrite
    def bge(self, rl: Register, rr: Register, address: str):
        return f"bge {rl},{rr},{address}"

    @autowrite
    def blt(self, rl: Register, rr: Register, address: str):
        return f"blt {rl},{rr},{address}"

    @autowrite
    def ble(self, rl: Register, rr: Register, address: str):
        return f"ble {rl},{rr},{address}"

    # Comparison
    @autowrite
    def slt(self, dest: Register, rl: Register, rr: Register):
        return f"slt {dest},{rl},{rr}"

    @autowrite
    def slti(self, dest: Register, rl: Register, value: int):
        return f"slt {dest},{rl},{value}"

    # Unconditional Jump

    @autowrite
    def j(self, address: str):
        return f"j {address}"

    @autowrite
    def jr(self, r: Register):
        return f"jr {r}"

    @autowrite
    def jal(self, address: str):
        return f"jal {address}"

    # System Calls
    @autowrite
    def syscall(self, code: int):
        return [
            self.li(Register.v0, 1),
            self.syscall
        ]

    def print_int(self):
        return self.syscall(1)

    def print_string(self):
        return self.syscall(4)

    def read_int(self):
        return self.syscall(5)

    def read_string(self):
        return self.syscall(8)

    def sbrk(self):
        return self.syscall(9)

    def exit(self):
        return self.syscall(10)

    def print_char(self):
        return self.syscall(11)

    def read_char(self):
        return self.syscall(12)

    # Data Section

    @autowritedata
    def ascii(self, string: str):
        return f'{Directive.ascii} "{string}"'

    @autowrite
    def asciiz(self, string: str):
        return f'{Directive.asciiz} "{string}"'

    # Utilities
    def offset(self, r: Register, offset: int = 0):
        return f"{offset}({r})"

    @autowritedata
    def var_label(self, name: str):
        return f"{name}:"

    @autowrite
    def label(self, name: str):
        return f"{name}:"

    @autowrite
    def empty_line(self):
        return ""
