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

    def variable_index(self, var_name):
        for i, var in enumerate self.localvars:
            if var.name == var_name:
                return i
        return -1

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
        data_label = mips.TYPE_NAME_LABEL.format(len(self.types))
        mips_type  = cil_to_mips_type(node)
        mips_type.set_data_label(data_label)
        self.types.append(mips_type)
        self.dotdata.append(mips.DataNode(data_label, node.name))

    @visitor.when(cil.DataNode)
    def visit(self, node):
        self.dotdata.append(cil_to_mips_data(node))

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        self.actual_function = node
        
        registers_to_save = ['ra', 't0', 't1']
        #Saving Register
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
        self.add_instructions(mips.load_registers_from_stack(registers_to_save[-1]))

        self.actual_function_instructions = []
        self.actual_function = None

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        size      = self.types[node.vtype].size
        var_index = self.variable_index(node.dest.name) 
        offset    = var_index * mips.ATTR_SIZE
        addr      = mips.Address(mips.REGISTERS['t0'], offset)
        self.add_instructions(mips.allocate_memory(addr, size))



def cil_to_mips_data(cil_data):
    return mips.DataNode(cil_data.name, cil_data.value)

def cil_to_mips_type(cil_type):
    return mips.MIPSType(cil_type.name, cil_type.attributes, cil_type.methods)