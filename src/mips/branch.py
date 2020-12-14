from mips.instruction import UnconditionalJumpNode, UnaryJumpNode, BinaryJumpNode, UnconditionalJumpRegisterNode


class B(UnconditionalJumpNode):
    """
    Mueve el flujo de ejecucion hacia LABEL, incondicionalmente.
    """
    pass


class J(UnconditionalJumpNode):
    """
    Salta hacia label.
    """
    pass


class JAL(UnconditionalJumpNode):
    """
    Salta hacia label y almacena la direccion de la proxima instruccion en $ra.
    """
    pass


class JR(UnconditionalJumpRegisterNode):
    """
    Salta a la ubicacion apuntada por $src1.
    """
    pass


class JALR(UnconditionalJumpRegisterNode):
    """
    Salta a la ubicacion apuntada por $src1 y almacena la direccion de la proxima instruccion en $ra.
    """


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


class BEQZ(UnaryJumpNode):
    """
    Saltar hacia label si $src1 = 0.
    """
    pass


class BNEZ(UnaryJumpNode):
    """
    Saltar hacia label si $src1 != 0.
    """
    pass


class BGEZ(UnaryJumpNode):
    """
    Saltar hacia label si $src1 >= 0.
    """
    pass


class BGTZ(UnaryJumpNode):
    """
    Saltar hacia label si $src1 > 0.
    """
    pass


class BLEZ(UnaryJumpNode):
    """
    Saltar hacia label si $src1 <= 0.
    """
    pass


class BLTZ(UnaryJumpNode):
    """
    Saltar hacia label si $src1 < 0.
    """
    pass


class BGEZAL(UnaryJumpNode):
    """
    Si $src1 >= 0 entonces pone la direccion de la proxima instruccion en $ra y salta a label.
    """
    pass


class BGTZAL(UnaryJumpNode):
    """
    Si $src1 > 0 entonces pone la direccion de la proxima instruccion en $ra y salta a label.
    """
    pass


class BLTZAL(UnaryJumpNode):
    """
    Si $src1 < 0 entonces pone la direccion de la proxima instruccion en $ra y salta a label.
    """
    pass