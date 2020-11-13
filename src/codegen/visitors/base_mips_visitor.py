from codegen.cil_ast import *
from codegen.tools import *
from semantic.tools import VariableInfo
from semantic.types import Attribute
from typing import List

class BaseCILToMIPSVisitor:
    def __init__(self):
        self.code: list = ['.text', '.globl main']
        self.initialize_data_code()
        self.initialize_built_in_types()
        self.symbol_table = SymbolTable()
        # temp registers: t9, voy a usarlo para llevarlo de temporal en expresiones aritmeticas 
        # Not sure if i should only use local registers
        self.reg_desc = RegisterDescriptor()
        self.addr_desc = AddressDescriptor()
        
        self.dispatch_table: DispatchTable = DispatchTable()
        self.obj_table: ObjTable = ObjTable(self.dispatch_table)
        self.initialize_methods()
        # Will hold the type of any of the vars
        self.var_address = {'self': AddrType.REF}

    def initialize_methods(self):
        self.methods = [] 
        # Built in methods added
        for entry in self.obj_table:
            entry: ObjTabEntry
            self.methods.extend(entry.dispatch_table_entry)

    def initialize_data_code(self):
        self.data_code = ['.data'] 
    
    def initialize_built_in_types(self):
        self.data_code.append(f"type_String: .asciiz \"String\"")     # guarda el nombre de la variable en la memoria            
        self.data_code.append(f"type_Int: .asciiz \"Int\"")     # guarda el nombre de la variable en la memoria            
        self.data_code.append(f"type_Bool: .asciiz \"Bool\"")     # guarda el nombre de la variable en la memoria            
        self.data_code.append(f"type_Object: .asciiz \"Object\"")     # guarda el nombre de la variable en la memoria            
        self.data_code.append(f"type_IO: .asciiz \"IO\"")     # guarda el nombre de la variable en la memoria            
        

    def get_basic_blocks(self, instructions: List[InstructionNode]):
        leaders = self.find_leaders(instructions)
        blocks = [instructions[leaders[i-1]:leaders[i]] for i in range(1, len(leaders))]
        return blocks


    def find_leaders(self, instructions: List[InstructionNode]):
        "Returns the positions in the block that are leaders"
        leaders = {0, len(instructions)}
        for i, inst in enumerate(instructions):
            if isinstance(inst, GotoNode) or isinstance(inst, GotoIfNode) or isinstance(inst, ReturnNode) \
                or isinstance(inst, StaticCallNode) or isinstance(inst, DynamicCallNode):
                leaders.add(i+1)
            elif isinstance(inst, LabelNode) or isinstance(inst, FunctionNode):
                leaders.add(i)
        return sorted(list(leaders))

    def is_variable(self, expr):
        return isinstance(expr, str)

    def is_int(self, expr):
        return isinstance(expr, int)

    def add_entry_symb_tab(self, name):
        "Method to add a entry in the symbol table. (Local)"
        self.symbol_table.insert(name)

    def construct_next_use(self, basic_blocks: List[List[InstructionNode]]):
        next_use = {}
        for basic_block in basic_blocks:
            #Flush Symbol table's nextuse islive information
            for x in self.symbol_table:
                self.symbol_table[x].is_live = False
                self.symbol_table[x].next_use = None

            for inst in reversed(basic_block):
                in1 = inst.in1 if self.is_variable(inst.in1) else None
                in2 = inst.in2 if self.is_variable(inst.in2) else None
                out = inst.out if self.is_variable(inst.out) else None
        
                in1nextuse = None
                in2nextuse = None
                outnextuse = None
                in1islive = False
                in2islive = False
                outislive = False

                entry_in1 = self.symbol_table.lookup(in1)
                entry_in2 = self.symbol_table.lookup(in2)
                entry_out = self.symbol_table.lookup(out)
                if out is not None:
                    if entry_out is not None:
                        outnextuse = entry_out.next_use
                        outislive = entry_out.is_live
                    else:
                        # Esto no debería pasar
                        entry_out = SymbolTabEntry(out)
                    entry_out.next_use = None
                    entry_out.is_live = False
                    self.symbol_table.insert(entry_out)
                if in1 is not None:
                    if entry_in1 is not None:
                        in1nextuse = entry_in1.next_use
                        in1islive = entry_in1.is_live
                    else:
                        # Esto no debería pasar
                        entry_in1 = SymbolTabEntry(out)
                    entry_in1.next_use = inst.index
                    entry_in1.is_live = True
                    self.symbol_table.insert(entry_in1)
                if in2 is not None:
                    if entry_in2 is not None:
                        in2nextuse = entry_in2.next_use
                        in2islive = entry_in2.is_live
                    else:
                        # Esto no debería pasar
                        entry_in2 = SymbolTabEntry(in2)
                    entry_in2.next_use = inst.index
                    entry_in2.is_live = True
                    self.symbol_table.insert(entry_in2)

                n_entry = NextUseEntry(in1, in2, out, in1nextuse, in2nextuse, outnextuse, in1islive, in2islive, outislive)
                next_use[inst.index] = n_entry
        return next_use

    def get_reg(self, inst: InstructionNode):
        if self.is_variable(inst.in1):
            self.get_reg_var(inst.in1)
        if self.is_variable(inst.in2):
            self.get_reg_var(inst.in2) 
        
        # Comprobar si se puede usar uno de estos registros tambien para el destino
        nu_entry = self.next_use[inst.index]
        if nu_entry.in1islive and nu_entry.in1nextuse < inst.index:
            update_register(inst.out, in1_reg)
            return  
        if nu_entry.in2islive and nu_entry.in2nextuse < inst.index:
            update_register(inst.out, in2_reg)
            return 
        # Si no buscar un registro para z por el otro procedimiento
        if self.is_variable(inst.out):
            self.get_reg_var(inst.out) 


    def get_reg_var(self, var):
        curr_inst = self.block[0]
        register = self.addr_desc.get_var_reg(var)
        if register is not None:   # ya la variable está en un registro
            return 

        var_st = self.symbol_table.lookup(var)
        register = self.reg_desc.find_empty_reg()
        if register is not None:
            self.update_register(var, register)
            self.load_var_code(var)
            return 

        # Choose a register that requires the minimal number of load and store instructions
        score = {}          # keeps the score of each variable (the amount of times a variable in a register is used) 
        for inst in self.block[1:]:
            inst: InstructionNode
            if inst.in1 and inst.in1 != curr_inst.in1 and curr_inst.in2 != inst.in1 and curr_inst.out != inst.in1:
                _update_score(score, inst.in1) 
            if inst.in2 and inst.in2 != curr_inst.in1 and curr_inst.in2 != inst.in2 and curr_inst.out != inst.in2:
                _update_score(score, inst.in2)
            if inst.out and inst.out != curr_inst.in1 and inst.out != curr_inst.in2 and inst.out != curr_inst.out:
                _update_score(score, inst.out)
        # Chooses the one that is used less
        n_var = min(score, key=lambda x: score[x])
    
        register, memory, _ = self.addr_desc.get_var_storage(n_var)

        update_register(var, register)
        self.load_var_code(var)


    def _update_score(self, score, var):
        if self.addr_desc.get_var_reg(var) is None:
            return
        try:
            score[var]+= 1
        except:
            score[var] = 1

    def update_register(self, var, register):
        content = self.reg_desc.get_content(register)
        if content is not None:
            self.save_var_code(content)
            self.addr_desc.set_var_reg(content, None)
        self.reg_desc.insert_register(register, var)
        self.addr_desc.set_var_reg(var, register)

    def save_var_code(self, var):
        "Code to save a variable to memory"
        memory, register, _= self.addr_desc.get_var_storage(var)
        self.code.append(f"sw ${register}, -{memory}($fp)")

    def load_var_code(self, var):
        "Code to load a variable from memory"
        memory, register, _ = self.addr_desc.get_var_storage(var)
        self.code.append(f'lw ${register}, -{memory}($fp)')
       
    def load_used_reg(self, registers):
        "Loads the used variables in there registers"
        for reg in used_reg:
            self.code.append('addiu $sp, $sp, 4')
            self.code.append(f'lw ${reg}, ($sp)')

    def empty_registers(self):
        "Empty all used registers and saves there values to memory"
        registers = self.reg_desc.used_registers()
        for reg, var in registers: 
            self.save_var_code(var)
            self.addr_desc.set_var_reg(var, None)
            self.reg_desc.insert_register(reg, None)     

    def push_register(self, register):
        "Pushes the register to the stack"
        self.code.append('addiu $sp, $sp, -4')
        self.code.append(f'sw ${register}, ($sp)')    

    def pop_register(self, register):
        "Popes the register from the stack"
        self.code.append('addiu $sp, $sp, 4')   
        self.code.append(f'lw ${register}, ($sp)')    

    def save_to_register(self, expr):
        "Aditional code to save an expression into a register. Returns the register"
        if self.is_int(expr):
            self.code.append(f'li $t9, {expr}')
            return 't9'
        elif self.is_variable(expr):
            return self.addr_desc.get_var_reg(expr.name)

    def get_attr_offset(self, attr_name:str, type_name:str):
        return self.obj_table[type_name].attr_offset(attr_name)

    def get_method_offset(self, type_name, method_name):
        self.obj_table[type_name].method_offset(method_name)

    def save_meth_addr(self, func_nodes: List[FunctionNode]):
        self.methods += [funct.name for funct in func_nodes]
        words = 'methods: .word ' + ', '.join(map(lambda x: '0', self.methods))
        self.data_code.append(words)

    def get_type(self, xtype):
        'Return the var address type according to its static type'
        if xtype == 'Int':
            return AddrType.INT
        elif xtype == 'Bool':
            return AddrType.BOOL
        elif xtype == 'String':
            return AddrType.STR
        return AddrType.REF