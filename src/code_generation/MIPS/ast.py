class Instruction:
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        if self.arguments is None:
            return f"{self.name}"
        elif len(self.arguments) == 3:
            return f"{self.name} {self.arguments[0]}, {self.arguments[1]}, {self.arguments[2]}"
        elif len(self.arguments) == 2:
            return f"{self.name} {self.arguments[0]}, {self.arguments[1]}"
        elif len(self.arguments) == 1:
            return f"{self.name} {self.arguments[0]}"


# ===============
# Data Directives
# ===============

class AsciizInst(Instruction):
    def __init__(self, arguments):
        super().__init__(".asciiz", arguments)
        


# ============================
# Jump and Branch Instructions
# ============================

class JalInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('jal', arguments)
        

# =============================
# Load, Store and Data Movement
# =============================
        
class MoveInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('move', arguments)
        
class SwInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('sw', arguments)
        
class LwInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('lw', arguments)
        
        

# =======================
# Arithmetic Instructions
# =======================
        
class SubInstruction(Instruction):
    def __init__(self, arguments, signed = True):
        super().__init__('sub', arguments) if signed else super().__init__('subu', arguments)
        
class AddInstruction(Instruction):
    def __init__(self, arguments, signed = True):
        super().__init__('add', arguments) if signed else super().__init__('addu', arguments)

class MultInstruction(Instruction):
    def __init__(self, arguments, signed = True):
        super().__init__('mult', arguments) if signed else super().__init__('multu', arguments)

class DivInstruction(Instruction):
     def __init__(self, arguments, signed = True):
        super().__init__('div', arguments) if signed else super().__init__('divu', arguments)

class NegInstruction(Instruction):
    def __init__(self, arguments, signed = True):
        super().__init__('neg', arguments) if signed else super().__init__('negu', arguments)

class NorInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('nor', arguments)

class NotInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('not', arguments)

class OrInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('or', arguments)

class RemInstruction(Instruction):
    def __init__(self, arguments, signed = True):
        super().__init__('rem', arguments) if signed else super().__init__('remu', arguments)

class RolInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('rol', arguments)

class RorInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('ror', arguments)

class SllInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('sll', arguments)

class SraInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('sra', arguments)
    
class SrlInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('srl', arguments)

class XorInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('xor', arguments)

class AbsInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('abs', arguments)