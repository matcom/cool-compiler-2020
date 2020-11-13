from codegen.cil_ast import *
from utils import visitor
from codegen.visitors.base_mips_visitor import BaseCILToMIPSVisitor
from codegen.tools import SymbolTable, AddressDescriptor, RegisterDescriptor, AddrType
from semantic.tools import VariableInfo
from pprint import pprint

class CILToMIPSVistor(BaseCILToMIPSVisitor):
    '''
    Registers:
    v0-v1: Used for expression evaluations and to hold the integer type 
        function results. Also used to pass the static link when calling 
        nested procedures.
    a0-a3: Used to pass the first 4 words of integer type actual 
        arguments, their values are not preserved across procedure 
        calls.
    t0-t7: Temporary registers used for expression evaluations; their 
        values aren’t preserved across procedure calls.
    s0-s7: Saved registers. Their values must be preserved across 
        procedure calls.
    t8-t9: Temporary registers used for expression evaluations; their 
        values aren’t preserved across procedure calls.
    k0-k1: Reserved for the operating system kernel.
    gp: Contains the global pointer.
    sp: Contains the stack pointer.
    fp: Contains the frame pointer (if needed); otherwise a saved register.
    ra: Contains the return address and is used for expression evaluation. 
        Register $ra only needs to be saved if the callee itself makes a call.

    '''
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        #? Quizá tenga que cambiar el orden en que estas cosas se visitan
        # visit TypeNodes
        for type_ in node.dottypes:
            self.visit(type_)
        # visit DataNodes
        for data in node.dotdata:
            self.visit(data)
        # guardo las direcciones de cada método
        self.save_meth_addr(node.dotcode)
        # visit code instrunctions
        for i, code in enumerate(node.dotcode):
            self.visit(code, 4*i)
        return self.data_code, self.code

    @visitor.when(TypeNode)
    def visit(self, node:TypeNode):
        self.obj_table.add_entry(node.name, node.methods, node.attributes)
        self.data_code.append(f"type_{node.name}: .asciiz \"{node.name}\"")     # guarda el nombre de la variable en la memoria            

    @visitor.when(DataNode)
    def visit(self, node:DataNode):
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")    

    @visitor.when(FunctionNode)
    def visit(self, node:FunctionNode, index:int):
        self.code.append('')
        self.code.append(f'{node.name}:')
        
        # guardo la dirección del método en el array de métodos
        self.code.append('# Save method direction in the methods array')
        self.code.append(f'la $t9, {node.name}')
        self.code.append(f'la $v0, methods')
        self.code.append(f'sw $t9, {4*index}($v0)')

        self.code.append('# Gets the params from the stack')
        n = len(node.params)
        for i, param in enumerate(node.params):     # gets the params from the stack
            self.visit(param, i, n)
        self.code.append('# Gets the frame pointer from the stack')
        self.code.append(f'move $fp, $sp')          # gets the frame pointer from the stack
        for i, var in enumerate(node.localvars, len(node.params)):
            self.visit(var, i)
        blocks = self.get_basic_blocks(node.instructions)
        self.next_use = self.construct_next_use(blocks)

        for block in blocks:
            self.block = block
            for inst in block:
                self.get_reg(inst)
                self.visit(inst)

    @visitor.when(ParamNode)
    def visit(self, node:ParamNode, idx:int, length:int):        
        self.symbol_table.insert_name(node.name)
        self.var_address[node.name] = self.get_type(node.type)
        if idx <= 3:                                # los primeros 3 registros se guardan en a0-a3  
            self.code.append('# The 3 firsts registers are saved in a0-a3')
            addr = idx if length <= 3 else length - 4 + idx
            self.addr_desc.insert_var(node.name, addr, f'a{idx}')
            self.reg_desc.insert_register(f'a{idx}', node.name)
        else:
            self.code.append('# Pops the register with the param value')
            self.code.append('addiu $sp, $sp, 4')   # pops the register with the param value from stack      
            self.addr_desc.insert_var(node.name, length-idx-1)

    @visitor.when(LocalNode)
    def visit(self, node:LocalNode, idx:int):
        self.symbol_table.insert_name(node.name)    # inserts the var in the symbol table, local by default
        self.addr_desc.insert_var(node.name, idx)   # saves the address relative from the actual fp
        self.code.append(f'# Updates stack pointer pushing {node.name} to the stack')
        self.code.append(f'addiu $sp, $sp, -4')     # updates stack pointers (pushing this value)

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# Moving {node.source} to {node.dest}')
        if self.is_variable(node.source):
            rsrc = self.addr_desc.get_var_reg(node.source)
            self.code.append(f'move ${rdest}, ${rsrc}') 
            self.var_address[node.dest] = self.var_address[node.source]
        elif self.is_int(node.source):
            self.code.append(f'li ${rdest}, {node.source}')
            self.var_address[node.dest] = AddrType.INT
        # elif isinstance(node.source, str):  # esto nunca se debe ejecutar (se llama a load node)
        #     self.code.append(f'la ${rdest}, {self.strings[node.source]}')

    @visitor.when(NotNode)
    def visit(self, node:NotNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rscr = self.save_to_register(node.expr)
        self.code.append(f'# {node.dest} <- not {node.expr}')
        self.code.append(f'not {rdest}, {rsrc}')
        self.var_address[node.dest] = AddrType.BOOL


    @visitor.when(PlusNode)
    def visit(self, node:PlusNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# {node.dest} <- {node.left} + {node.right}')
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"add ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"addi ${rdest}, ${rleft}, {node.right}")
        elif self.is_int(node.right):
            if self.is_int(node.left):
                self.code.append(f"li ${rdest}, {node.left + node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"addi ${rdest}, ${node.left}, ${rright}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(MinusNode)
    def visit(self, node:MinusNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# {node.dest} <- {node.left} - {node.right}')
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"sub ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.left):
                self.code.append(f"addi ${rdest}, ${rleft}, -{node.right}")
        elif self.is_int(node.right):
            if self.is_int(node.left):
                self.code.append(f"li ${rdest}, {node.left-node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"sub $t9, $zero, {rright}")
                self.code.append(f"addi ${rdest}, $t9, {node.left}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(StarNode)
    def visit(self, node:StarNode):
        self.code.append(f'# {node.dest} <- {node.left} * {node.right}')
        self._code_to_mult_div(node, op='mult')

    @visitor.when(DivNode)
    def visit(self, node:DivNode):
        self.code.append(f'# {node.dest} <- {node.left} / {node.right}')
        self._code_to_mult_div(node, op='div')

    def _code_to_mult_div(self, node, op:str):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"{op} ${rleft}, ${rright}")
                self.code.append(f"mflo ${rdest}")
            elif self.is_int(node.left):
                self.code.append(f"li $t9, {node.right}")
                self.code.append(f"{op} ${rleft}, $t9")
                self.code.append(f"mflo ${rdest}")
        elif self.is_int(node.right):
            if self.is_int(node.left):
                self.code.append(f"li ${rdest}, {node.left / node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                self.code.append(f"{op} ${rright}, $t9")
                self.code.append(f"mflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(LessNode)
    def visit(self, node:LessNode):
        self.code.append(f'# {node.dest} <- {node.left} < {node.right}')
        self._code_to_comp(node, op='slt')

    @visitor.when(LessEqNode)
    def visit(self, node:MinusNode):
        self.code.append(f'# {node.dest} <- {node.left} <= {node.right}')
        self._code_to_comp(node, op='sle')

    @visitor.when(EqualNode)
    def visit(self, node:MinusNode):
        self.code.append(f'# {node.dest} <- {node.left} = {node.right}')
        self._code_to_comp(node, op='seq')

    def _code_to_comp(self, node, op):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"{op} ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.left):
                self.code.append(f"li $t9, {node.right}")
                self.code.append(f"{op} ${rdest}, ${rleft}, $t9")
        elif self.is_int(node.right):
            if self.is_int(node.left):
                self.code.append(f"li ${rdest}, {int(node.left <= node.right)}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                self.code.append(f"{op} ${rdest}, $t9, {rright}")
        self.var_address[node.dest] = AddrType.BOOL


    @visitor.when(GetAttribNode)
    def visit(self, node:GetAttribNode):
        self.code.append(f'# {node.dest} <- GET {node.obj} . {node.type_name}')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.var_address[node.dest] = self.get_type(node.attr_type)
        rsrc = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        self.code.append(f'lw ${rdest}, {attr_offset}(${rsrc})')


    @visitor.when(SetAttribNode)
    def visit(self, node:SetAttribNode):
        self.code.append(f'# {node.obj} . {node.attr} <- SET {node.value}')
        rdest = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        if self.is_variable(node.value):
            rsrc = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            self.code.append(f'sw $t9, {node.value}')
            rsrc = 't9'
        self.code.append(f'sw ${rsrc}, {attr_offset}(${rdest})') # saves the new value in the attr offset


    @visitor.when(AllocateNode)
    def visit(self, node:AllocateNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        size = 4*self.obj_table.size_of_entry(node.type)      # size of the table entry of the new type
        self.var_address[node.dest] = AddrType.REF
        # syscall to allocate memory of the object entry in heap
        var = self.reg_desc.get_content('a0')
        if var is not None:
            self.code.append('# Saving content of a0 to memory to use that register')
            self.save_var_code(var)
        
        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')                         # code to request memory
        self.code.append(f'li $a0, {size}')                   # argument (size)
        self.code.append('syscall')
        # in v0 is the address of the new memory
        addrs_stack = self.addr_desc.get_var_addr(node.dest)
        self.code.append('# Save the address in the stack')
        self.code.append(f'sw $v0, -{addrs_stack}($fp)')     # save the address in the stack (where is the local variable)

        self.code.append('# Loads the name of the variable and saves the name like the first field')
        self.code.append(f'la $t9, type_{node.type}')       # loads the name of the variable
        self.code.append(f'sw $t9, 0($v0)')                 # saves the name like the first field 

        self.code.append(f'# Saves the size of the node')
        self.code.append(f'li $t9, {size}')                 # saves the size of the node
        self.code.append(f'sw $t9, 4($v0)')                 # this is the second file of the table offset
        self.code.append(f'move ${rdest}, $v0')             # guarda la nueva dirección de la variable en el registro destino

        self.create_dispatch_table(node.type)               # memory of dispatch table in v0
        self.code.append(f'sw $v0, 8(${rdest})')            # save a pointer of the dispatch table in the 3th position
       
        if var is not None:
            self.code.append('# Restore the variable of a0')
            self.load_var_code(var)
      
    def create_dispatch_table(self, type_name):
        # Get methods of the dispatch table
        methods = self.dispatch_table.get_methods(type_name)
        # Allocate the dispatch table in the heap
        self.code.append('# Allocate dispatch table in the heap')
        self.code.append('li $v0, 9')                       # code to request memory
        dispatch_table_size = 4*len(methods)
        self.code.append(f'li $a0, {dispatch_table_size}')
        self.code.append('syscall')                         # Memory of the dispatch table in v0
        
        self.code.append(f'# I save the offset of every one of the methods of this type')
        for i, meth in enumerate(methods):
            # guardo el offset de cada uno de los métodos de este tipo
            offset = 4*self.methods.index(meth)
            self.code.append('# Save the direction of methods')
            self.code.append('la $t8, methods')             # cargo la dirección de methods
            self.code.append(f'# Save the direction of the method {meth} in t9')
            self.code.append(f'lw $t9, {offset}($t8)')      # cargo la dirección del método en t9
            self.code.append('# Save the direction of the method in his position in the dispatch table')
            self.code.append(f'sw $t9, {4*i}($v0)')         # guardo la direccion del metodo en su posicion en el dispatch table        


    @visitor.when(TypeOfNode)
    def visit(self, node:TypeOfNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'{node.dest} <- Type of {node.obj}')
        if self.is_variable(node.obj):
            rsrc = self.addr_desc.get_var_reg(node.obj)
            if self.var_address[node.obj] == AddrType.REF:
                self.code.append(f'la ${rdest}, 0(${rsrc})')    # como en el offset 0 está el nombre del tipo this is ok
            elif self.var_address[node.obj] == AddrType.STR:
                self.code.append(f'la ${rdest}, type_String')
            elif self.var_address[node.obj] == AddrType.INT:
                self.code.append(f'la ${rdest}, type_Int')
            elif self.var_address[node.obj] == AddrType.BOOL:
                self.code.append(f'la ${rdest}, type_Bool')
        elif self.is_int(node.obj):
            self.code.append(f'la ${rdest}, type_Int')

    @visitor.when(LabelNode)
    def visit(self, node:LabelNode):
        self.code.append(f'{node.label}')

    @visitor.when(GotoNode)
    def visit(self, node:GotoNode):
        self.code.append(f'j {node.label}')

    @visitor.when(GotoIfNode)
    def visit(self, node:GotoIfNode):
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If {node.cond} goto {node.label}')
        self.code.append(f'bnez ${reg}, {node.label}')

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode):
        function = self.dispatch_table.find_full_name(node.type, node.function)
        self.code.append(f'# Static Dispatch of the method {node.function}')
        self._code_to_function_call(node.args, function, node.dest)

        self.var_address[node.dest] = self.get_type(node.return_type)

    @visitor.when(DynamicCallNode)
    def visit(self, node:DynamicCallNode):
        # Find the actual name of the method in the dispatch table
        self.code.append('# Find the actual name in the dispatch table')
        reg = self.addr_desc.get_var_reg('self')        # obtiene la instancia actual
        self.code.append('# Gets in t9 the actual direction of the dispatch table')
        self.code.append(f'lw $t9, 8(${reg})')          # obtiene en t9 la dirección del dispatch table
        function = self.dispatch_table.find_full_name(node.type, node.method)       
        index = self.dispatch_table.get_offset(node.type, function)      # guarda el offset del me
        self.code.append(f'# Saves in t9 the direction of {function}')
        self.code.append(f'lw $t8, {index}($t9)')       # guarda en $t8 la dirección de la función a llamar 
        # Call function
        self._code_to_function_call(node.args, '$t8', node.dest)
        
        self.var_address[node.dest] = self.get_type(node.return_type)

    def _code_to_function_call(self, args, function, dest):
        self.push_register('fp')                    # pushes fp register to the stack
        self.push_register('ra')                    # pushes ra register to the stack
        self.code.append('# Push the arguments to the stack')
        for i, arg in enumerate(args):              # push the arguments to the stack
            self.visit(arg, i)

        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()                      # empty all used registers and saves them to memory
        self.code.append('# This function will consume the arguments')
        self.code.append(f'jal {function}')         # this function will consume the arguments
        self.code.append('# Pop fp register from the stack')
        self.pop_register('fp')                     # pop fp register from the stack
        if dest is not None:
            self.get_reg_var(dest)
            rdest = self.addr_desc.get_var_reg(dest)
            self.code.append('# saves the return value')
            self.code.append(f'move ${rdest}, $v0') # v0 es usado para guardar el valor de retorno

    @visitor.when(ArgNode)
    def visit(self, node:ArgNode, idx):
        if idx <= 3:        # los primeros 3 registros se guardan en a0-a3
            reg = f'a{idx}'
            self.code.append('# The 3 first registers are saved in a0-a3')
            if self.is_variable(node.dest):
                rdest = self.addr_desc.get_var_reg(node.dest)
                self.code.append(f'move ${reg}, ${rdest}')
            elif self.is_int(node.dest):
                self.code.append(f'li ${reg}, {node.dest}')
        else: 
            self.code.append('# The rest of the arguments are push into the stack')
            self.code.append('addiu $sp, $sp, -4')
            if self.is_variable(node.dest):
                reg = self.addr_desc.get_var_reg(node.dest)
                self.code.append(f'sw ${reg}, ($sp)')
            elif self.is_int(node.dest):
                self.code.append(f'li $t9, {node.dest}')
                self.code.append(f'sw $t9, ($sp)')
       
    @visitor.when(ReturnNode)
    def visit(self, node:ReturnNode):
        self.code.append('# Pop ra register of return function of the stack')
        self.pop_register('ra')                 # pop register ra from the stack
        # save the return value
        if self.is_variable(node.value): 
            rdest = self.addr_desc.get_var_reg(node.value)
            self.code.append(f'move $v0, ${rdest}')
        elif self.is_int(node.value):
            self.code.append(f'li $v0, {node.value}')
        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()                      # empty all used registers and saves them to memory
        # return to the caller
        self.code.append(f'jr $ra')

        self.code.append('')

    @visitor.when(LoadNode)
    def visit(self, node:LoadNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'Saves in {node.dest} {node.msg}')
        self.var_address[node.dest] = AddrType.STR
        self.code.append(f'la ${rdest}, {node.msg}')