from mips.instruction import ComparisonNode


class SEQ(ComparisonNode):
    """
    $dest <-- 1 si $src1 = $src2, 0 en otro caso.
    """
    pass


class SNE(ComparisonNode):
    """
    $dest <-- 1 si $src1 != $src2, 0 en otro caso.
    """
    pass


class SGE(ComparisonNode):
    """
    $dest <-- 1 si $src1 >= $src2, 0 en otro caso.
    Operacion con signo.
    """
    pass


class SGEU(ComparisonNode):
    """
    $dest <-- 1 si $src1 >= $src2, 0 en otro caso.
    Operacion sin signo.
    """
    pass


class SGT(ComparisonNode):
    """
    $dest <-- 1 si $src1 > $src2, 0 en otro caso.
    Operacion con signo.
    """
    pass


class SGTU(ComparisonNode):
    """
    $dest <-- 1 si $src1 > $src2, 0 en otro caso.
    Operacion sin signo.
    """
    pass


class SLE(ComparisonNode):
    """
    $dest <-- 1 si $src1 <= $src2, 0 en otro caso.
    Operacion con signo.
    """
    pass


class SLEU(ComparisonNode):
    """
    $dest <-- 1 si $src1 <= $src2, 0 en otro caso.
    Operacion sin signo.
    """
    pass


class SLT(ComparisonNode):
    """
    $dest <-- 1 si $src1 < $src2, 0 en otro caso.
    Operacion con signo.
    """
    pass


class SLTU(ComparisonNode):
    """
    $dest <-- 1 si $src1 < $src2, 0 en otro caso.
    Operacion sin signo.
    """
    pass
