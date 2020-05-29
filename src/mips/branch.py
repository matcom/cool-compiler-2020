from mips.instruction import UnconditionalJumpNode, UnaryJumpNode, BinaryJumpNode


class B(UnconditionalJumpNode):
    """
    Mueve el flujo de ejecucion hacia LABEL, incondicionalmente.
    """
    pass


class BEQ(BinaryJumpNode):
    """
    Salta hacia label si $src1 es identico a $src2.
    """
    pass


class BNE(BinaryJumpNode):
    """
    Salta hacia label si $src1 != $src2.
    """
    pass


class BGE(BinaryJumpNode):
    """
    Salta hacia label si $src1 >= $src2.
    Operacion con signo.
    """
    pass


class BGEU(BinaryJumpNode):
    """
    Salta hacia label si $src1 >= $src2.
    Operacion sin signo.
    """
    pass


class BGT(BinaryJumpNode):
    """
    Salta hacia label si $src1 > $src2.
    Operacion con signo.
    """
    pass


class BGTU(BinaryJumpNode):
    """
    Salta hacia label si $src1 > $src2.
    Operacion sin signo.
    """
    pass


class BLE(BinaryJumpNode):
    """
    Salta hacia label si $src1 <= $src2.
    Operacion con signo.
    """
    pass


class BLEU(BinaryJumpNode):
    """
    Salta hacia label si $src1 <= $src2.
    Operacion sin signo.
    """
    pass


class BLT(BinaryJumpNode):
    """
    Salta hacia label si $src1 < $src2.
    Operacion con signo.
    """
    pass


class BLTU(BinaryJumpNode):
    """
    Salta hacia label si $src1 < $src2.
    Operacion sin signo.
    """
    pass
