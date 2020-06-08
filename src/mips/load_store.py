from mips.instruction import AbstractLoadNode


class LA(AbstractLoadNode):
    """
    Carga la direccion de un label (indicado por src).
    """
    pass


class LB(AbstractLoadNode):
    """
    Carga el byte desde src en $dest.
    Operacion con signo. 
    """
    pass


class LBU(AbstractLoadNode):
    """
    Carga el byte desde src en $dest.
    Operacion sin signo.
    """
    pass


class LH(AbstractLoadNode):
    """
    Carga media palabra (2 bytes) desde src en $dest.
    Operacion con signo.
    """
    pass


class LHU(AbstractLoadNode):
    """
    Carga media palabra (2 bytes) desde src en $dest.
    Operacion sin signo.
    """
    pass


class LI(AbstractLoadNode):
    """
    Carga la constante src en $dest.
    """
    pass


class LUI(AbstractLoadNode):
    """
    Carga la constante src en los dos bytes superiores de $dest, y setea los 2 bytes inferiores
    a 0.
    """
    pass


class LW(AbstractLoadNode):
    """
    Carga los 4 bytes a partir de src en $dest.
    """
    pass


class ULH(AbstractLoadNode):
    """
    Carga 2 bytes empezando en src en $dest
    """
    pass


class SB(AbstractLoadNode):
    """
    Almacena el primer byte del registro $dest en addr.
    """
    pass


class SH(AbstractLoadNode):
    """
    Almacena los primeros dos bytes del registro $dest en addr.
    """
    pass


class SW(AbstractLoadNode):
    """
    Almacena los 4 bytes del registro $dest en addr.
    """
    pass


class SWL(AbstractLoadNode):
    """
    Almacena los ultimos dos bytes del registro $dest en addr (esta direccion esta probablemente desalineada).
    """
    pass


class USW(AbstractLoadNode):
    """
    Almacena los 4 bytes del registro $dest en addr (esta direccion esta probablemente desalineada).
    """
    pass