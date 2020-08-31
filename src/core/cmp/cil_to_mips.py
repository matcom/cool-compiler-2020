import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.mips as mips
from core.cmp.utils import CountDict


USED   = 1
UNUSED = 0


class SimpleRegistersManager:
    def __init__(self, registers):
        self.registers = {reg: UNUSED for reg in registers}
            
    def get_free_reg(self):
        for reg, state in self.registers.items():
            if state == UNUSED:
                self.registers[reg] = USED
                return reg
        raise Exception("not free register")
        
    
    def free_reg(self, reg):
        self.registers[reg] = UNUSED
    
    def is_used(self, reg):
        return self.registers[reg] == USED

    def get_registers_for_save(self):
        regs = [reg for reg, state in self.registers.items() if state == USED]
        regs.extend([mips.RA_REG])
        return regs


class LabelGenerator:
    def __init__(self):
        self.data_count = 0
        self.type_count = 0
        self.code_count = 0

    def generate_type_label(self):
        self.type_count += 1        
        return f'type_{self.type_count}'
        
    def generate_data_label(self):
        self.data_count += 1
        return f'data_{self.data_count}'
    
    def generate_code_label(self):
        self.code_count += 1
        return f'L_{self.code_count}'


class CILToMIPSVisitor:
    def __init__(self, label_generator = LabelGenerator(), regiters_manager = SimpleRegistersManager()):
        self._label_generator = label_generator
        self._registers_manager = regiters_manager
        self._types = {}
        self._data_sections = {}
        self._functions = {}
        self._actual_function = None
    
    def generate_type_label(self):
        return self._label_generator.generate_type_label()
    
    def generate_data_label(self):
        return self._label_generator.generate_data_label()
    
    def generate_code_label(self):
        return self._label_generator.generate_code_label()
    
    def get_var_location(self, name):
        return self._actual_function.get_var_location(name)
    
    def register_function(self, name, function):
        self._functions[name] = function
    
    def init_function(self, function):
        self._actual_function = function
    
    def finish_functions(self):
        self._actual_function = None

    
    




def cil_to_mips_data(cil_data):
    return mips.DataNode(cil_data.name, cil_data.value)

def cil_to_mips_type(cil_type):
    return mips.MIPSType(cil_type.name, cil_type.attributes, cil_type.methods)



# class A:
    # pass
# 
# class B(A):
    # pass
# 
# class C:
    # pass
# 
# @visitor.on('param')
# def try2(param):
    # pass
# 
# @visitor.when(A)
# def try2(param):
    # print("is A")
# 
# @visitor.when(B)
# def try2(param):
    # print("is B")


#Change Name
class FunctionDivider:
    def __init__(self):
        self.mark
        
        
    def divide_basics_blocks(self, intructions):
        self.mark = True
        for instruction in instructions:
            self.mark_leaders(instruction)

        blocks = []

        for instruction in instrucctions:
            if instruction.leader:
                block.append([instruction])
            block[-1].append(instruction)
        
        return blocks

    def create_flow_graph(blocks): #graph between blocks in a same function does not include relations between functions
        graph = [[-1 for _ in range(len(blocks))] for _ in range(len(blocks)) ]
        labels = {b.name : i for i, b in enumerate(blocks) if type(b[0]) == cil.LabelNode}

        for i, block in enumerate(blocks):
            tp = type(block[-1])
            if tp == cil.GotoNode:
                graph[i][labels[block[-1].label]] = 1

            elif tp == cil.GotoIfNode:
                graph[i][labels[block[-1].label]] = 1
                graph[i][min(len(blocks)-1, i+1)] = 1

            elif tp == cil.DynamicCallNode:
                pass #analize what to do with function calls
            elif tp == cil.StaticCallNode:
                pass #analize what to do with function calls

            return graph            



    @visitor.on('instruction')
    def mark_leaders(self, instruction):
        pass

    @visitor.when(cil.LabelNode)
    def mark_leaders(self, instruction):
        instruction.leader = True
        self.mark = False

    @visitor.when(cil.GotoNode)
    def mark_leaders(self, instruction):
        self.mark = True

    @visitor.when(cil.GotoIfNode)
    def mark_leaders(self, instruction):
        self.mark = True
    
    @visitor.when(cil.DynamicCallNode)
    def mark_leaders(self, instruction):
        self.mark = True

    @visitor.when(cil.StaticCallNode)
    def mark_leaders(self, instruction):
        self.mark = True
    
    @visitor.when(cil.InstructionNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = False

     











#TEST
CIL_TYPE_1 = cil.TypeNode("myType")
CIL_TYPE_1.attributes = ["attr1", "attr2", "attr3"]
CIL_TYPE_1.methods  = [("method1", "func1"), ("method2", "func2"), ("method3", "func3"), ("method4", "func4")]
CIL_TYPE_2 = cil.TypeNode("myType2")
CIL_TYPE_2.attributes = ["attr1", "attr2"]
CIL_TYPE_2.methods  = [("method1", "func5"), ("method2", "func2"), ("method3", "func6"), ("method4", "func7")]
CIL_AST_TEST = cil.ProgramNode([],[],[])
CIL_AST_TEST.dottypes = [CIL_TYPE_1, CIL_TYPE_2]


# if __name__ == '__main__':
def test():
    conv = CILToMIPSVisitor()
    conv.visit(CIL_AST_TEST)
    for d in conv.dotdata:
        print(d)
    
