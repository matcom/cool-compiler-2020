class Instruction:
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        if self.arguments is None:
            return f"{name}"
        elif len(self.arguments) == 3:
            return f"{name} {self.arguments[0]}, {self.arguments[1]}, {self.arguments[2]}"
        elif len(self.arguments) == 2:
            return f"{name} {self.arguments[0]}, {self.arguments[1]}"
        elif len(self.arguments) == 1:
            return f"{name} {self.arguments[0]}"


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
        
class SubuInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('subu', arguments)
        
class AdduInstruction(Instruction):
    def __init__(self, arguments):
        super().__init__('addu', arguments)