from enum import Enum
from typing import List

DATA_SIZE = 4


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
    text = ".text"
    data = ".data"


Reg = Register


def autowrite(tabs: int = 1):
    def inner(func):
        """
        autowrite a instruction when execute string return function
        """

        def wrapper(*args, **kwargs):
            instruction = func(*args, **kwargs)
            args[0].write_inst(instruction, tabs)

        return wrapper

    return inner


def autowritedata(func):
    """
    autowrite() a instruction when execute string return function
    """

    def inner(*args, **kwargs):
        instructions = func(*args, **kwargs)
        if instructions is list:
            for instruction in instructions:
                args[0].write_data(instruction)
        else:
            args[0].write_data(instructions)

    return inner


class Mips:
    def __init__(self):
        self.DOTTEXT: List[str] = []
        self.DOTDATA: List[str] = []

    def write_inst(self, instruction: str, tabs: int = 0):
        tabstr = ""
        for _ in range(tabs):
            tabstr += "\t"
        self.DOTTEXT.append(f"{tabstr}{instruction}")

    def write_data(self, data: str, tabs: int = 0):
        self.DOTDATA.append(f"{data}")

    def compile(self):
        return "\n".join(
            [Directive.data.value]
            + self.DOTDATA
            + []
            + [Directive.text.value]
            + self.DOTTEXT
        )

    def push(self, register: Register):
        self.addi(Reg.sp, Reg.sp, -DATA_SIZE)
        self.store_memory(register, self.offset(Reg.sp))

    def pop(self, register: Register):
        """
        First,  load from to address `0($sp)`
        and then write `addi $sp ,  $sp ,  8`
        to restore the stack pointer
        """
        self.load_memory(register, self.offset(Reg.sp))
        self.addi(Reg.sp, Reg.sp, DATA_SIZE)

    def load_memory(self, dst: Register, address: str):
        """
        Load from a specific address a 32 bits register
        """
        self.lw(dst, address)
        # self.lw(Reg.t8, address)
        # self.sll(Reg.t8, Reg.t8, 16)
        # self.la(Reg.t7, address)
        # self.addi(Reg.t7, Reg.t7, 4)
        # self.lw(Reg.t9, self.offset(Reg.t7))
        # self.orr(dst, Reg.t8, Reg.t9)

    def store_memory(self, src: Register, address: str):
        """
        Write to a specific address a 32 bits register
        """
        self.sw(src, address)
        # self.la(Reg.t8, address)

        # self.srl(Reg.t9, src, 16)

        # self.sw(Reg.t9, self.offset(Reg.t8))  # store high bits
        # self.sw(src, self.offset(Reg.t8, 4))  # store low bits

    # Arithmetics
    @autowrite()
    def add(self, dst: Register, rl: Register, rr: Register):
        return f"add {dst}, {rl}, {rr}"

    @autowrite()
    def sub(self, dst: Register, rl: Register, rr: Register):
        return f"sub {dst}, {rl}, {rr}"

    @autowrite()
    def addi(self, dst: Register, rl: Register, value: int):
        return f"addi {dst}, {rl}, {int(value)}"

    @autowrite()
    def addu(self, dst: Register, rl: Register, rr: Register):
        return f"addu {dst}, {rl}, {rr}"

    @autowrite()
    def subu(self, dst: Register, rl: Register, rr: Register):
        return f"subu {dst}, {rl}, {rr}"

    @autowrite()
    def addiu(self, dst: Register, rl: Register, value: int):
        return f"addiu {dst}, {rl}, {int(value)}"

    @autowrite()
    def multu(self, dst: Register, rl: Register, rr: Register):
        return f"multu {dst}, {rl}, {rr}"

    @autowrite()
    def mult(self, rl: Register, rr: Register):
        return f"mult {rl}, {rr}"

    @autowrite()
    def div(self, rl: Register, rr: Register):
        return f"div {rl}, {rr}"

    # Logical:
    @autowrite()
    def andd(self, dst: Register, rl: Register, rr: Register):
        return f"and {dst}, {rl}, {rr}"

    @autowrite()
    def orr(self, dst: Register, rl: Register, rr: Register):
        return f"or {dst}, {rl}, {rr}"

    @autowrite()
    def nor(self, dst: Register, rl: Register, rr: Register):
        return f"nor {dst}, {rl}, {rr}"

    @autowrite()
    def andi(self, dst: Register, rl: Register, value: int):
        return f"andi {dst}, {rl}, {int(value)}"

    # TODO: Check this instrucction
    @autowrite()
    def ori(self, dst: Register, rl: Register, value: int):
        return f"or {dst}, {rl}, {int(value)}"

    @autowrite()
    def sll(self, dst: Register, rl: Register, value: int):
        return f"sll {dst}, {rl}, {int(value)}"

    @autowrite()
    def srl(self, dst: Register, rl: Register, value: int):
        return f"srl {dst}, {rl}, {int(value)}"

    # DataTransfer:
    @autowrite()
    def lw(self, dst: Register, address: str):
        return f"lw {dst}, {address}"

    @autowrite()
    def lb(self, dst: Register, address: str):
        return f"lb {dst}, {address}"

    @autowrite()
    def sw(self, dst: Register, address: str):
        return f"sw {dst}, {address}"

    @autowrite()
    def sb(self, dst: Register, address: str):
        return f"sb {dst}, {address}"

    @autowrite()
    def lui(self, dst: Register, value: int):
        return f"lui {dst}, {int(value)}"

    @autowrite()
    def la(self, dst: Register, label: str):
        return f"la {dst}, {label}"

    @autowrite()
    def li(self, dst: Register, value: int):
        return f"li {dst}, {int(value)}"

    @autowrite()
    def mfhi(self, dst: Register):
        return f"mfhi {dst}"

    @autowrite()
    def mflo(self, dst: Register):
        return f"mflo {dst}"

    @autowrite()
    def move(self, dst: Register, rl: Register):
        return f"move {dst},  {rl}"

    # Brancing
    @autowrite()
    def beq(self, rl: Register, rr: Register, address: str):
        return f"beq {rl},  {rr},  {address}"

    @autowrite()
    def bne(self, rl: Register, rr: Register, address: str):
        return f"bne {rl},  {rr},  {address}"

    @autowrite()
    def beqz(self, rl: Register, address: str):
        return f"beqz {rl},  {address}"

    @autowrite()
    def bgt(self, rl: Register, rr: Register, address: str):
        return f"bgt {rl}, {rr}, {address}"

    @autowrite()
    def bge(self, rl: Register, rr: Register, address: str):
        return f"bge {rl}, {rr}, {address}"

    @autowrite()
    def blt(self, rl: Register, rr: Register, address: str):
        return f"blt {rl}, {rr}, {address}"

    @autowrite()
    def ble(self, rl: Register, rr: Register, address: str):
        return f"ble {rl}, {rr}, {address}"

    # Comparison
    @autowrite()
    def slt(self, dest: Register, rl: Register, rr: Register):
        return f"slt {dest}, {rl}, {rr}"

    @autowrite()
    def slti(self, dest: Register, rl: Register, value: int):
        return f"slt {dest}, {rl}, {int(value)}"

    # Unconditional Jump

    @autowrite()
    def j(self, address: str):
        return f"j {address}"

    @autowrite()
    def jr(self, r: Register):
        return f"jr {r}"

    @autowrite()
    def jal(self, address: str):
        return f"jal {address}"

    @autowrite()
    def jalr(self, dest: Register):
        return f"jalr {dest}"

    # System Calls
    @autowrite()
    def syscall(self, code: int):
        self.li(Register.v0, code)
        return "syscall"

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

    def exit2(self):
        return self.syscall(17)

    # Utilities
    def offset(self, r: Register, offset: int = 0):
        return f"{int(offset)}({r})"

    @autowrite()
    def comment(self, text: str):
        return f"# {text}"

    @autowrite(0)
    def label(self, name: str):
        return f"{name}:"

    @autowrite()
    def empty(self):
        return ""

    # Data Section

    @autowrite()
    def data_empty(self):
        return ""

    @autowritedata
    def data_label(self, name: str):
        return f"{name}:"

    @autowritedata
    def ascii(self, string: str):
        return f'{Directive.ascii} "{string}"'

    @autowritedata
    def asciiz(self, string: str):
        return f'{Directive.asciiz} "{string}"'

    @autowritedata
    def data_comment(self, text: str):
        return f"#{text}"
