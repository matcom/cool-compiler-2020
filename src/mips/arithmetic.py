from mips.instruction import ArithmeticNode, BinaryNode


class ADD(ArithmeticNode):
    """
    dest = src1 + src2 (Con signo).
    """
    pass


class ADDU(ArithmeticNode):
    """
    dest = src1 + src2 (Sin signo).
    """
    pass


class AND(ArithmeticNode):
    """
    dest = src1 AND src2 bit a bit.
    """
    pass


class DIV(ArithmeticNode):
    """
    dest = src1 / src2.
    El resto que almacenado en el registro hi.
    Esta operacion es con signo.
    """
    pass


class DIVU(ArithmeticNode):
    """
    dest = src1 / src2. Sin signo
    """
    pass


class ABS(BinaryNode):
    """
    dest almacena el valor absoluto de src1.
    """
    pass


class MUL(ArithmeticNode):
    """
    dest = src1 * src2.
    """
    pass


class MULO(ArithmeticNode):
    """
    dest = src1 * src2 con overflow.
    """
    pass


class MULT(BinaryNode):
    """
    Multiplica $dest y $src1 dejando los primeros 4 bytes en registro lo
    y el resto en hi. Operacion con signo.
    """
    pass


class MULTU(BinaryNode):
    """
    Multiplica $dest y $src1 dejando los primeros 4 bytes en registro lo
    y el resto en hi. Operacion sin signo.
    """
    pass


class NEG(BinaryNode):
    """
    $dest almacena el negativo de $src1.
    """
    pass


class NEGU(BinaryNode):
    """
    Almacena el negativo sin signo de $src1 en $dest
    """
    pass


class NOR(ArithmeticNode):
    """
    Almacena en $dest el resultado de aplicar la operacion logica NOR bit a bit entre $src1 y $src2
    """
    pass


class NOT(BinaryNode):
    """
    Almacena en $dest la negacion logica de $src1.
    """
    pass


class OR(ArithmeticNode):
    """
    Almacena en $dest el resultado de hacer OR bit a bit entre $src1 y $src2.
    """
    pass


class REM(ArithmeticNode):
    """
    Almacena en $dest el resto de dividir $src1 entre $src2.
    Operacion con signo.
    """
    pass


class REMU(ArithmeticNode):
    """
    Almacena en $dest el resti de dividir $src1 entre $src2.
    Operacion sin signo.
    """
    pass


class ROL(ArithmeticNode):
    """
    Almacena en $dest el resultado de rotar a la izquierda el contenido de $src1 por
    $src2 bits.
    """
    pass


class ROR(ArithmeticNode):
    """
    Almacena en $dest el resultado de rotar a la derecha el contenido de $src1 por
    $src2 bits.
    """
    pass


class SLL(ArithmeticNode):
    """
    Almacena en $dest lo que halla en $src1 shifteado a la izquierda $src2 bits.
    """
    pass


class SRA(ArithmeticNode):
    """
    Right Shift aritmetico.
    """
    pass


class SRL(ArithmeticNode):
    """
    Right Shift logico.
    """
    pass


class SUB(ArithmeticNode):
    """
    $dest = src1 - src2.
    Operacion con signo.
    """
    pass


class SUBU(ArithmeticNode):
    """
    $dest = $src1 - $src2.
    Operacion sin signo.
    """
    pass


class XOR(ArithmeticNode):
    """
    $dest = $src1 XOR $src2 bit a bit.
    """
    pass
