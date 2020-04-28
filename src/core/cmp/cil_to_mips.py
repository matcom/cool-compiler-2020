import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.mips as mips

class BaseCILToMIPSVisitor:
    def __init__(self):
        self.types = {}
        self.dottext = []
        self.dotdata = []
        self.actual_function = None
        self.actual_function_instructions = []
    
    @property
    def localvars(self):
        return self.actual_function.localvars
    
    @property
    def params(self):
        return self.actual_function.parmas
    
    @property
    def cil_instructions(self)
        return self.actual_function.instructions

    def add_instructions(self, instructions):
        self.actual_function_instructions.extend(instructions)

class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        for type_node in node.dottypes:
            self.visit(type_node)
        
        for data_node in node.dotdata:
            self.visit(data_node)

        for function_node in node.dotcode:
            self.visit(function_node)
        
        return mips.ProgramNode(dottext, dotdata)

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        self.types.append(cil_to_mips_type(node))

    @visitor.when(cil.DataNode)
    def visit(self, node):
        self.dotdata.append(cil_to_mips_data(node))

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        self.actual_function = node
        
        registers_to_save = ['ra', 't0', 't1']
        #Saving Register
        # self.add_instructions(mips.save_register(mips.REGISTERS['ra']))
        # self.add_instructions(mips.save_register(mips.REGISTERS['t0']))
        # self.add_instructions(mips.save_register(mips.REGISTERS['t1']))
        self.add_instructions(mips.save_registers(registers_to_save))
        
        #Argument received to params
        self.add_instructions(mips.MoveNode(mips.REGISTERS['t1'], mips.REGISTERS['t2']))
        
        #Allocating memory for local variables
        addr     = mips.Address(mips.REGISTERS['t0'], 0)
        var_size = len(self.localvars) * mips.ATTR_SIZE
        self.add_instructions(mips.allocate_memory(addr, var_size))

        #function_body
        for instruction in self.cil_isntructions:
            self.visit(instruction)

        #Loading saved register
        # self.add_instructions(mips.load_reg_from_stack(mips.REGISTERS['t1']))
        # self.add_instructions(mips.load_reg_from_stack(mips.REGISTERS['t0']))
        # self.add_instructions(mips.load_reg_from_stack(mips.REGISTERS['ra']))
        self.add_instructions(mips.load_registers_from_stack(registers_to_save[-1]))

        self.actual_function_instructions = []
        self.actual_function = None




def cil_to_mips_data(cil_data):
    return mips.DataNode(cil_data.name, cil_data.value)

def cil_to_mips_type(cil_type):
    return mips.MIPSType(cil_type.name, cil_type.attributes, cil_type.methods)