import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.mips as mips
from core.cmp.utils import CountDict



class RegistersManager:
    def __init__(self):
        pass
    
    def getReg(self, instruction):
        pass

class StoreLocation:
    pass

class Register(StoreLocation):
    def __init__(self, name):
        self._name = name
        self._registerDescriptor = RegisterDescriptor()
    
    @property
    def name(self):
        return self._name
    
    @property
    def get_register_descriptor(self):
        return self._registerDescriptor

class RegisterDescriptor:
    def __init__(self):
        #ListVariables
        pass

class MemoryLocation(StoreLocation):
    pass

class HeapLocation(MemoryLocation):
    pass

class StackLocation(MemoryLocation):
    pass


class AddressDescriptor():
    def __init__(self):
        #List locations
        pass

class SymbolTable:
    def __init__(self):
        #Dict name: AddressDescriptor
        pass


class BaseCILToMIPSVisitor:
    def __init__(self):
        self.types = {}
        self.dottext = []
        self.dotdata = []
        self.actual_function = None
        self.actual_function_instructions = []
        self.types_dict = CountDict()
        self.funcs_dict = CountDict()
        self.str_consts = CountDict()
        self.int_consts = CountDict()
        self.symbol_table = SymbolTable()

            
    @property
    def localvars(self):
        return self.actual_function.localvars
    
    @property
    def params(self):
        return self.actual_function.parmas
    
    @property
    def cil_instructions(self):
        return self.actual_function.instructions

    def variable_index(self, var_name):
        for i, var in enumerate(self.localvars):
            if var.name == var_name:
                return i
        return -1

    def add_instructions(self, instructions):
        self.actual_function_instructions.extend(instructions)

    def get_str_const(self, string):
        try:
            str_const = self.str_consts.get(string)
        except:
            name   = f'str_const_{len(self.str_consts)}'
            str_const = mips.StringConst(name, string)
            self.dotdata.append(str_const)
            self.str_consts.add(string, str_const)
        
        return str_const.label
        
    def new_type(self, name, attributes, methods):
        label = f'type_{len(self.types_dict)}'
        name  = self.get_str_const(name)
        size  = (len(attributes) * mips.ATTR_SIZE) + mips.TYPE_METADATA_SIZE

        new_type = mips.MIPSType(label, name, size, methods)
        self.types_dict.add(name, new_type)
        func_names = []
        for _, func_name in methods:
            new_func_name = f'func_{len(self.funcs_dict)}'
            try:
                new_func_name = self.funcs_dict.get(func_name)
            except:
                self.funcs_dict.add(func_name, new_func_name)
            func_names.append(new_func_name)

        self.dotdata.append(mips.TypeDesc(label, name, size, func_names))   

    def register_basic_types_names(self):
        self.types_dict.add("String", "string_type")
        self.types_dict.add("Int", "int_type")
        self.types_dict.add("Bool", "bool_type")
        self.types_dict.add("Object", "object_type")
   
        





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
# 
        # for function_node in node.dotcode:
            # self.visit(function_node)
        # 
        # return mips.ProgramNode(dottext, dotdata)

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        self.new_type(node.name, node.attributes, node.methods)


    @visitor.when(cil.DataNode)
    def visit(self, node):
        self.get_str_const(node.string)

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        self.actual_function = node
        
        #registers_to_save = ['ra', 't0', 't1']
        ## Saving Register
        #self.add_instructions(mips.save_registers(registers_to_save))
        #
        ## Argument received to params
        #self.add_instructions(mips.MoveNode(mips.REGISTERS['t1'], mips.REGISTERS['t2']))
        #
        ## Allocating memory for local variables
        #addr     = mips.Address(mips.REGISTERS['t0'], 0)
        #var_size = len(self.localvars) * mips.ATTR_SIZE
        #self.add_instructions(mips.allocate_memory(addr, var_size))

        ## function_body
        #for instruction in self.cil_isntructions:
        #    self.visit(instruction)

        ## Loading saved register
        #self.add_instructions(mips.load_registers_from_stack(registers_to_save[-1]))

        #self.actual_function_instructions = []
        #self.actual_function = None

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

    def create_flow_graph(blocks) #graph between blocks in a same function does not include relations between functions
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
    
