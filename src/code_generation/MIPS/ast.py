
class MIPSProgram:
    def __init__(self, data_section, text_section):
        self.data = data_section
        self.text = text_section

    def __str__(self):
        return f'{self.text}{self.data}'


class MIPSTextSection:
    def __init__(self, fucntions):
        self.fucntions = fucntions

    def __str__(self):
        functions_text = '\n'.join([str(f) for f in self.fucntions])
        return f'\n.text\n{functions_text}\n'


class MIPSDataSection:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        data_text = '\n'.join([str(d) for d in self.data])
        return f'\n.data\n{data_text}\n'


class MIPSFunction:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    def __str__(self):
        return '\n'.join([f'# FUNCTION: {self.name}']+[str(i) for i in self.instructions])


class MIPSDataItem:
    def __init__(self, label, instruction):
        self.label = label
        self.instruction = instruction

    def __str__(self):
        return f'{self.label}: {str(self.instruction)}'


class Instruction:
    def __init__(self, name, *arguments):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        if len(self.arguments) == 0:
            return f"\t{self.name}"
        elif len(self.arguments) == 3:
            return f"\t{'{:10}'.format(self.name)} {self.arguments[0]}, {self.arguments[1]}, {self.arguments[2]}"
        elif len(self.arguments) == 2:
            return f"\t{'{:10}'.format(self.name)} {self.arguments[0]}, {self.arguments[1]}"
        elif len(self.arguments) == 1:
            return f"\t{'{:10}'.format(self.name)} {self.arguments[0]}"


class Comment(Instruction):
    def __init__(self, text):
        super().__init__('#', (text))


# ===============
# Data Directives
# ===============

class AsciizInst(Instruction):
    def __init__(self, *arguments):
        super().__init__(".asciiz", *arguments)


# =============================
# Load, Store and Data Movement
# =============================

class MoveInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('move', *arguments)


class SwInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sw', *arguments)


class LwInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('lw', *arguments)


class LiInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('li', *arguments)


# =======================
# Arithmetic Instructions
# =======================

class SubInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sub', *arguments)


class SubuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('subu', *arguments)


class AddInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('add', *arguments)


class AdduInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('addu', *arguments)


class MultInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('mult', *arguments)


class MultuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('multu', *arguments)


class DivInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('div', *arguments)


class DivuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('divu', *arguments)


class NegInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('neg', *arguments)


class NeguInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('negu', *arguments)


class NorInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('nor', *arguments)


class NotInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('not', *arguments)


class OrInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('or', *arguments)


class RemInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('rem', *arguments)


class RemuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('remu', *arguments)


class RolInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('rol', *arguments)


class RorInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('ror', *arguments)


class SllInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sll', *arguments)


class SraInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sra', *arguments)


class SrlInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('srl', *arguments)


class XorInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('xor', *arguments)


class AbsInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('abs', *arguments)


# =======================
# Comparison Instructions
# =======================

class SeqInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('seq', *arguments)


class SneInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sne', *arguments)


class SgeInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sge', *arguments)


class SgeuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sgeu', *arguments)


class SgtInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sgt', *arguments)


class SgtuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sgtu', *arguments)


class SleInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sle', *arguments)


class SleuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sleu', *arguments)


class SltInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('slt', *arguments)


class SltuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sltu', *arguments)


# ============================
# Branch and Jump Instructions
# ============================

class BInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('b', *arguments)


class BeqInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('beq', *arguments)


class BneInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bne', *arguments)


class BgeInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bge', *arguments)


class BgeuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bgeu', *arguments)


class BgtInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bgt', *arguments)


class BgtuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bgtu', *arguments)


class BleInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('ble', *arguments)


class BleuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bleu', *arguments)


class BltInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('blt', *arguments)


class BltuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bltu', *arguments)


class JInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('j', *arguments)


class JrInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('jr', *arguments)


class JalInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('jal', *arguments)


class JalrInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('jalr', *arguments)
# ==================
# Exception Handling
# ==================


class SyscallInstruction(Instruction):
    def __init__(self):
        super().__init__('syscall')
