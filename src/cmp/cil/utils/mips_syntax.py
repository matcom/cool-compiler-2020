from enum import Enum
class Register(str,Enum):
    # stores value 0; cannot be modified
    zero="$zero" 
    # used for system calls and procedure return values
    v0="$v0"
    v1="$v1"
    # used for passing arguments to procedures
    a0="$a0"
    a1="$a1"
    a2="$a2"
    a3="$a3"
    # used for local storage; calling procedure saves these
    t0="$t0"
    t1="$t1"
    t2="$t2"
    t3="$t3"
    t4="$t4"
    t5="$t5"
    t6="$t6"
    t7="$t7"
    t8="$t8"
    t9="$t9"
    # used for local storage; called procedure saves these
    s0="$s0"
    s1="$s1"
    s2="$s2"
    s3="$s3"
    s4="$s4"
    s5="$s5"
    s6="$s6"
    s7="$s7"
    sp="$sp" # stack pointer
    fp="$fp" # frame pointer; primarily used during stack manipulations
    ra="$ra" # used to store return address in procedure call
    gp="$gp" # pointer to area storing global data (data segment)
    at="$at" # reserved for use by the assembler
    # reserved for use by OS kernel
    k0="$k0" 
    k1="$k1"

class Directive(str,Enum):
    word= ".word"
    half = ".half"
    byte = ".byte"
    ascii = ".ascii"
    asciiz = ".asciiz"
    space = ".space"
    aling = ".align"


syscall = "syscall"

class Mips:
    
# Arithmetics

    @staticmethod
    def add( dst:Register,rl:Register,rr:Register):
        return f"add {dst},{rl},{rr}"
    
    @staticmethod
    def sub( dst:Register,rl:Register,rr:Register):
        return f"sub {dst},{rl},{rr}"
    
    @staticmethod
    def addi( dst:Register,rl:Register,value:int):
        return f"addi {dst},{rl},{value}"
    
    @staticmethod
    def addu( dst:Register,rl:Register,rr:Register):
        return f"addu {dst},{rl},{rr}"
    
    @staticmethod
    def subu( dst:Register,rl:Register,rr:Register):
        return f"subu {dst},{rl},{rr}"

    @staticmethod
    def addiu( dst:Register,rl:Register,value:int):
        return f"addiu {dst},{rl},{value}"
    
    @staticmethod
    def mul( dst:Register,rl:Register,rr:Register):
        return f"mul {dst},{rl},{rr}"

    @staticmethod
    def mult( rl:Register,rr:Register):
        return f"mult {rl},{rr}"

    @staticmethod
    def div( rl:Register,rr:Register):
        return f"div {rl},{rr}"


# Logical:
    
    @staticmethod
    def and( dst:Register,rl:Register,rr:Register):
        return f"and {dst},{rl},{rr}"
    
    @staticmethod
    def or( dst:Register,rl:Register,rr:Register):
        return f"or {dst},{rl},{rr}"
    
    @staticmethod
    def andi( dst:Register,rl:Register,value:int):
        return f"andi {dst},{rl},{value}"

    #TODO: Check this instrucction
    @staticmethod
    def ori( dst:Register,rl:Register,value:int):
        return f"or {dst},{rl},{value}"

    @staticmethod
    def sll( dst:Register,rl:Register,value:int):
        return f"sll {dst},{rl},{value}"
    
    @staticmethod
    def srl( dst:Register,rl:Register,value:int):
        return f"srl {dst},{rl},{value}"

# DataTransfer:

    @staticmethod
    def lw( dst:Register, address : str):
        return f"lw {dst},{address}"

    @staticmethod
    def sw( dst:Register, address : str):
        return f"sw {dst},{address}"

    @staticmethod
    def lui( dst:Register, value : int):
        return f"lw {dst},{value}"

    @staticmethod
    def la( dst:Register, label : str):
        return f"la {dst},{label}"

    @staticmethod
    def li( dst:Register, value : int):
        return f"li {dst},{value}"
    
    @staticmethod
    def mfhi( dst:Register):
        return f"mfhi {dst}"
    
    @staticmethod
    def mflo( dst:Register):
        return f"mflo {dst}"
    
    @staticmethod
    def move( dst:Register , rl:Register):
        return f"move {dst},{rl}"
     
# Brancing 

    @staticmethod
    def beq(rl:Register, rr :Register,address:str):
        return f"beq {rl},{rr},{address}"
    
    @staticmethod
    def bne(rl:Register, rr :Register,address:str):
        return f"bne {rl},{rr},{address}"
    
    @staticmethod
    def bgt(rl:Register, rr :Register,address:str):
        return f"bgt {rl},{rr},{address}"
    
    @staticmethod
    def bge(rl:Register, rr :Register,address:str):
        return f"bge {rl},{rr},{address}"
    
    @staticmethod
    def blt(rl:Register, rr :Register,address:str):
        return f"blt {rl},{rr},{address}"
    
    @staticmethod
    def ble(rl:Register, rr :Register,address:str):
        return f"ble {rl},{rr},{address}"
    
# Comparison

    @staticmethod
    def slt(dest:Register,rl:Register, rr :Register):
        return f"slt {dest},{rl},{rr}"

    @staticmethod
    def slti(dest:Register,rl:Register, value:int):
        return f"slt {dest},{rl},{value}"

        
# Unconditional Jump

    @staticmethod
    def j(address:str):
        return f"j {address}"

    @staticmethod
    def jr(r:Register):
        return f"jr {r}"
    
    @staticmethod
    def jal(address:str):
        return f"jal {address}"

# System Calls
    @staticmethod
    def syscall(code:int):
        return [
            Mips.li(Register.v0,1),
            syscall   
        ] 
    
    @staticmethod
    def print_int():
        return syscall(1)
    
    @staticmethod
    def print_string():
        return syscall(4)

    @staticmethod
    def read_int():
        return syscall(5)
    
    @staticmethod
    def read_string():
        return syscall(8)
    
    @staticmethod
    def sbrk():
        return syscall(9)
    
    @staticmethod
    def exit():
        return syscall(10)

    @staticmethod
    def print_char():
        return syscall(11)

    @staticmethod
    def read_char():
        return syscall(12)
    
    
# Data Section

    @staticmethod
    def ascii(string:str):
        return f"{Directive.ascii} \"{string}\""
        
    @staticmethod
    def asciiz(string:str):
        return f"{Directive.asciiz} \"{string}\""