"""
Este modulo ofrece wrappers a las instrucciones de mips de modo que se puedan
parametrizar y sea facil su uso a la hora de escribir en ensamblador.
"""

# **********************  REGISTROS *********************************

zero = 0   # Siempre almacena la constante 0.
at = 1     # Reservado para el assembler.

# Registros para almacenar resultados
v0 = 2
v1 = 3

# Registros para almacenar argumentos
a0 = 4
a1 = 5
a2 = 6
a3 = 7

# Registros temporales
t0 = 8
t1 = 9
t2 = 10
t3 = 11
t4 = 12
t5 = 13
t6 = 14
t7 = 15
t8 = 24
t9 = 25

# Saved Registers
s0 = 16
s1 = 17
s2 = 18
s3 = 19
s4 = 20
s5 = 21
s6 = 22
s7 = 23

# Registros del kernel
k0 = 26
k1 = 27

# Global Data Pointer
gp = 28

# Stack Pointer
sp = 29

# Frame Pointer
fp = 30

# Direccion de retorno
ra = 31


class MipsNode:
    pass


#  **********************   INSTRUCCIONES ARITMETICAS  *****************************
class ArithmeticNode(MipsNode):
    def __init__(self, dest: int, src1: int, src2: int, const_src2=False):
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.action = self.__class__.__name__.lower()
        self.const_src2 = const_src2
        if '_' in self.action:
            self.action = self.action.replace('_', "")

    def __str__(self):
        if self.const_src2:
            return f'{self.action} ${self.dest}, ${self.src1}, {self.src2}'
        return f'{self.action} ${self.dest}, ${self.src1}, ${self.src2}'


class BinaryNode(MipsNode):
    def __init__(self, dest: int, src1: int):
        self.dest = dest
        self.src1 = src1
        self.action = self.__class__.__name__.lower().replace('_', "")

    def __str__(self):
        return f'{self.action} ${self.dest}, ${self.src1}'


# *************************   INSTRUCCIONES DE COMPARACION  ******************
class ComparisonNode(MipsNode):
    def __init__(self, dest: int, src1: int, src2: int, const_src2=False):
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.action = self.__class__.__name__.lower()
        self.const_src2 = const_src2

    def __str__(self):
        if self.const_src2:
            return f'{self.action} ${self.dest}, ${self.src1}, {self.src2}'
        return f'{self.action} ${self.dest}, ${self.src1}, ${self.src2}'


# ************************   INSTRUCCIONES DE SALTO  *********************
class UnconditionalJumpNode(MipsNode):
    def __init__(self, label: str):
        self.label = label
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        return f'{self.action} {self.label}'


class UnconditionalJumpRegisterNode(MipsNode):
    def __init__(self, src1: int):
        self.src1 = src1
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        return f'{self.action} ${self.src1}'


class UnaryJumpNode(MipsNode):
    def __init__(self, src1: int, label: str):
        self.src1 = src1
        self.label = label
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        return f'{self.action} ${self.src1}, {self.label}'


class BinaryJumpNode(MipsNode):
    def __init__(self, src1: int, src2: int, label: str, const_src2=False):
        self.src1 = src1
        self.src2 = src2
        self.label = label
        self.const_src2 = const_src2
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        if self.const_src2:
            return f'{self.action} ${self.src1}, {self.src2}, {self.label}'
        return f'{self.action} ${self.src1}, ${self.src2}, {self.label}'


class AbstractLoadNode(MipsNode):
    def __init__(self, dest: int, src: int):
        self.dest = dest
        self.src = src
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        return f'{self.action} {self.dest}, {self.}'