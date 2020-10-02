"""
Este modulo ofrece wrappers a las instrucciones de mips de modo que se puedan
parametrizar y sea facil su uso a la hora de escribir en ensamblador.
"""

# **********************  REGISTROS *********************************

zero = 0  # Siempre almacena la constante 0.
at = 1  # Reservado para el assembler.

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

TEMP_REGISTERS = (t0, t1, t2, t3, t4, t5, t6, t7, t8, t9)
ARGS_REGISTERS = (a0, a1, a2, a3)

REG_TO_STR = {
    v0: "v0",
    v1: "v1",
    s0: "s0",
    s1: "s1",
    s2: "s2",
    s3: "s3",
    s4: "s4",
    s5: "s5",
    s6: "s6",
    s7: "s7",
    sp: "sp",
    fp: "fp",
    ra: "ra",
    gp: "gp",
    t0: "t0",
    t1: "t1",
    t2: "t2",
    t3: "t3",
    t4: "t4",
    t5: "t5",
    t6: "t6",
    t7: "t7",
    t8: "t8",
    t9: "t9",
    a0: "a0",
    a1: "a1",
    a2: "a2",
    a3: "a3"
}


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
            return f'{self.action} ${REG_TO_STR[self.dest]}, ${REG_TO_STR[self.src1]}, {self.src2}'
        return f'{self.action} ${REG_TO_STR[self.dest]}, ${REG_TO_STR[self.src1]}, ${REG_TO_STR[self.src2]}'


class BinaryNode(MipsNode):
    def __init__(self, dest: int, src1: int):
        self.dest = dest
        self.src1 = src1
        self.action = self.__class__.__name__.lower().replace('_', "")

    def __str__(self):
        return f'{self.action} ${REG_TO_STR[self.dest]}, ${REG_TO_STR[self.src1]}'


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
            return f'{self.action} ${REG_TO_STR[self.dest]}, ${REG_TO_STR[self.src1]}, {self.src2}'
        return f'{self.action} ${REG_TO_STR[self.dest]}, ${REG_TO_STR[self.src1]}, ${REG_TO_STR[self.src2]}'


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
        return f'{self.action} ${REG_TO_STR[self.src1]}'


class UnaryJumpNode(MipsNode):
    def __init__(self, src1: int, label: str):
        self.src1 = src1
        self.label = label
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        return f'{self.action} ${REG_TO_STR[self.src1]}, {self.label}'


class BinaryJumpNode(MipsNode):
    def __init__(self, src1: int, src2: int, label: str, const_src2=False):
        self.src1 = src1
        self.src2 = src2
        self.label = label
        self.const_src2 = const_src2
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        if self.const_src2:
            return f'{self.action} ${REG_TO_STR[self.src1]}, {self.src2}, {self.label}'
        return f'{self.action} ${REG_TO_STR[self.src1]}, ${REG_TO_STR[self.src2]}, {self.label}'


# ********************   INSTRUCCIONES PARA ALMACENAR Y CARGAR DATOS EN REGISTROS  ************
class AbstractLoadNode(MipsNode):
    def __init__(self, dest: int, src):
        self.dest = dest
        self.src = src
        self.action = self.__class__.__name__.lower()

    def __str__(self):
        return f'{self.action} ${REG_TO_STR[self.dest]}, {self.src}'


class MOVE(BinaryNode):
    """
    Copia el contenido de $src1 en $dest.
    """
    pass


# ********************    MANEJO DE EXCEPCIONES   *************************
class RFE(MipsNode):
    """
    Retorna de una excepcion.
    """
    def __str__(self):
        return "rfe"


class SYSCALL(MipsNode):
    """
    Realiza una llamada a sistema.
    """
    def __str__(self):
        return "syscall"


class BREAK(MipsNode):
    """
    Usado por el debugger.
    """
    def __init__(self, const: int):
        self.const = const

    def __str__(self):
        return f'break {self.const}'


class NOP(MipsNode):
    """
    Instruccion que no hace nada, salvo consumir un ciclo del reloj.
    """
    def __str__(self):
        return "nop"


class LineComment(MipsNode):
    """
    Representa un comentario en una linea
    """
    def __init__(self, string: str):
        self.text = string

    def __str__(self):
        return f'# {self.text}'


class Label(MipsNode):
    """
    Representa un label. (almacena una direccion de memoria a la cual se puede referenciar)
    """
    def __init__(self, label: str):
        self.label = label

    def __str__(self):
        return f"{self.label}: "


class FixedData(MipsNode):
    """
    Representa un dato en la seccion .data.
    Por ejemplo: 
        msg:    .asciiz "Hello World!\n"
    """
    def __init__(self, name: str, value, type_="word"):
        assert type_ in ("word", "asciiz", "byte", "space")
        self.name = name
        self.value = value
        self.type = type_

    def __str__(self):
        return f"{self.name}:   .{self.type}    {self.value}"