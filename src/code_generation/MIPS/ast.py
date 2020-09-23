import re


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
        data_text = '\n'.join([f'\t{str(d)}' for d in self.data])
        return f'\n.data\n{data_text}\n'


class MIPSLabel:
    def __init__(self, name):
        self.name = name
        self.callee_saved_reg = set()
        self.caller_saved_reg = set()

    def __str__(self):
        return f'{self.name}:\n'


class MIPSFunction:
    def __init__(self, name, params, locals):
        self.name = name
        self.ADDR = {}
        self.init_instructions = []
        self.instructions = []
        self.end_instructions = []
        self.caller_saved_reg = set()
        self.callee_saved_reg = set()

        self.init_instructions.append(MoveInstruction('$fp', '$sp'))

        self.params_count = len(params)
        # Store first 4 arguments in $a0 - $a3 registers
        i = 0
        while i < self.params_count and i < 4:
            p = params[i]
            self.ADDR[p.id] = f'$a{i}'
            i += 1
        # Save the rest on the stack
        if i < self.params_count:
            for j, p in enumerate(params[i:]):
                self.ADDR[p.id] = f'{j * 4}($fp)'

        for i, l in enumerate(locals, 1):
            self.ADDR[str(l)] = f'-{i * 4}($fp)'

        self.fp_shift = len(locals)
        self.init_instructions.append(
            Comment(f'{self.fp_shift} LOCALS = {self.fp_shift * 4} bytes'))
        self.fp_shift += 1
        self.init_instructions.append(SwInstruction(
            '$ra', f'-{self.fp_shift * 4}($fp)'))

    def append_instruction(self, instruction):
        """
        Add new instruction to function block. For a correct operation, the
        instructions must be addes continuisly, in the same order that they
        were declared in CIL.
        """
        # Update used registers
        self.__update_callee_saved_reg__(instruction.callee_saved_reg)
        self.__update_caller_saved_reg__(instruction.caller_saved_reg)
        # Update function instrcutions
        self.instructions.append(instruction)

    def end(self):
        """
        It points the end of the CIL function, and adds the last necessary
        actions.
        """
        self.init_instructions.append(SubuInstruction(
            '$sp', '$sp', f'{self.fp_shift * 4}'))
        self.end_instructions.append(AdduInstruction(
            '$sp', '$sp', f'{self.fp_shift * 4}'))

    def get_address(self, id):
        """
        Return thememory address where it store the \"id\" identifier of CIL
        """
        try:
            return self.ADDR[id]
        except KeyError:
            raise Exception(f'Unsaved id {id}')

    def __update_callee_saved_reg__(self, registers: set):
        diff = registers.difference(self.callee_saved_reg)
        for reg in diff:
            self.fp_shift += 1
            self.init_instructions.append(SwInstruction(
                f'${reg}', f'-{self.fp_shift * 4}($fp)'))
            self.end_instructions.append(SwInstruction(
                f'-{self.fp_shift * 4}($fp)', f'${reg}'))
        self.callee_saved_reg.update(diff)

    def __update_caller_saved_reg__(self, registers: set):
        self.caller_saved_reg.update(registers)

    def __str__(self):
        instructions = self.init_instructions + \
            self.instructions + self.end_instructions
        return '\n'.join([f'{self.name}:']+[f'\t{str(i)}' for i in instructions])


class MIPSDataItem:
    def __init__(self, label, instruction):
        self.label = label
        self.instruction = instruction

    def __str__(self):
        return f'{self.label}:\n\t\t{str(self.instruction)}'


class Instruction:
    def __init__(self, name, *arguments):
        self.name = name
        self.arguments = arguments
        self.caller_saved_reg = set()
        self.callee_saved_reg = set()
        patterns = [re.compile(r'\$(?P<register>..)'),
                    re.compile(r'[0-9]+\(\$(?P<register>..)\)')]
        caller_pattern = re.compile(r't[0-9]')
        callee_pattern = re.compile(r's[0-7]')
        for a in self.arguments:
            for p in patterns:
                match = p.match(str(a))
                if match:
                    reg = match.group('register')
                    if caller_pattern.match(reg):
                        self.caller_saved_reg.add(reg)
                    elif callee_pattern.match(reg):
                        self.callee_saved_reg.add(reg)
                    break

    def __str__(self):
        if len(self.arguments) == 0:
            return f"{self.name}"
        elif len(self.arguments) == 3:
            return f"{'{:10}'.format(self.name)} {self.arguments[0]}, {self.arguments[1]}, {self.arguments[2]}"
        elif len(self.arguments) == 2:
            return f"{'{:10}'.format(self.name)} {self.arguments[0]}, {self.arguments[1]}"
        elif len(self.arguments) == 1:
            return f"{'{:10}'.format(self.name)} {self.arguments[0]}"


class Comment(Instruction):
    def __init__(self, text):
        super().__init__('#', (text))


# ===============
# Data Directives
# ===============

class AsciizInst(Instruction):
    def __init__(self, *arguments):
        super().__init__(".asciiz", *arguments)


class SpaceInst(Instruction):
    def __init__(self, *arguments):
        super().__init__(".space", *arguments)


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


class LaInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('la', *arguments)


class LbInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('lb', *arguments)


class SbInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sb', *arguments)

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


class BeqzInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('beqz', *arguments)


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
