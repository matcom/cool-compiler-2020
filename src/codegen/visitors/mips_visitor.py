from codegen.cil_ast import *
from utils import visitor
from codegen.visitors.base_mips_visitor import BaseCILToMIPSVisitor
from codegen.tools import SymbolTable, AddressDescriptor, RegisterDescriptor, AddrType
from semantic.tools import VariableInfo
from semantic.types import VOID_NAME
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

        # guardo las direcciones de cada método
        self.save_meth_addr(node.dotcode)
        self.data_code.append(f"type_Void: .asciiz \"Void\"")     # guarda el nombre de Void Type                    
        # guardo las direcciones de cada tipo
        self.save_types_addr(node.dottypes)
        # visit DataNodes
        for data in node.dotdata:
            self.visit(data)
        # visit code instrunctions
        for code in node.dotcode:
            self.visit(code)
        
        self.initialize_runtime_errors()

        return self.data_code, self.code

    @visitor.when(TypeNode)
    def visit(self, node:TypeNode):
        self.obj_table.add_entry(node.name, node.methods, node.attributes)
        self.data_code.append(f"type_{node.name}: .asciiz \"{node.name}\"")     # guarda el nombre de la variable en la memoria            

    @visitor.when(DataNode)
    def visit(self, node:DataNode):
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")     

    @visitor.when(FunctionNode)
    def visit(self, node:FunctionNode):
        self.code.append('')
        self.code.append(f'{node.name}:')
        self.locals = 0     # pointer to count the ammount of locals that are pushed into the stack

        self.code.append('# Gets the params from the stack')
        self.code.append(f'move $fp, $sp')     # gets the frame pointer from the stack
        n = len(node.params)
        for i, param in enumerate(node.params, 1):     # gets the params from the stack
            self.visit(param, i, n)
        self.code.append('# Gets the frame pointer from the stack')
        for i, var in enumerate(node.localvars, len(node.params)):
            self.visit(var, i)
        self.locals = len(node.params) + len(node.localvars)
        blocks = self.get_basic_blocks(node.instructions)
        self.next_use = self.construct_next_use(blocks)

        for block in blocks:
            self.block = block
            for inst in block:
                self.inst = inst
                self.get_reg(inst)
                self.visit(inst)
            inst = block[-1]
            if not (isinstance(inst, GotoNode) or isinstance(inst, GotoIfNode) or isinstance(inst, ReturnNode) \
                or isinstance(inst, StaticCallNode) or isinstance(inst, DynamicCallNode)):
                self.empty_registers()
            # self.empty_registers()            

    @visitor.when(ParamNode)
    def visit(self, node:ParamNode, idx:int, length:int):        
        self.symbol_table.insert_name(node.name)
        self.var_address[node.name] = self.get_type(node.type)
        self.code.append(f'# Pops the register with the param value {node.name}')
        self.code.append('addiu $fp, $fp, 4')   # pops the register with the param value from stack      
        self.addr_desc.insert_var(node.name, length-idx)

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
        self.save_var_code(node.dest)

        
    @visitor.when(NotNode)
    def visit(self, node:NotNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.save_to_register(node.expr)
        self.code.append(f'# {node.dest} <- ~{node.expr}')
        self.code.append(f'not ${rdest}, ${rsrc}')
        self.code.append(f'addi ${rdest}, ${rdest}, 1')
        self.var_address[node.dest] = AddrType.INT
    
    @visitor.when(LogicalNotNode)
    def visit(self, node:LogicalNotNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.save_to_register(node.expr)
        self.code.append(f'# {node.dest} <- not {node.expr}')
        self.code.append(f'beqz ${rsrc}, false_{self.loop_idx}')
        self.code.append(f'li ${rdest}, 0')
        self.code.append(f'j end_{self.loop_idx}')
        self.code.append(f'false_{self.loop_idx}:')
        self.code.append(f'li ${rdest}, 1')
        self.code.append(f'end_{self.loop_idx}:')
        self.loop_idx += 1
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
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {node.left + node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"addi ${rdest}, ${rright}, {node.left}")
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
            elif self.is_int(node.right):
                self.code.append(f"addi ${rdest}, ${rleft}, -{node.right}")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {node.left-node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"sub $t9, $zero, {rright}")
                self.code.append(f"addi ${rdest}, {node.left}, $t9")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(StarNode)
    def visit(self, node:StarNode):
        self.code.append(f'# {node.dest} <- {node.left} * {node.right}')
        self._code_to_mult_div(node, op='mult', func_op=lambda x, y: x*y)

    @visitor.when(DivNode)
    def visit(self, node:DivNode):
        self.code.append(f'# {node.dest} <- {node.left} / {node.right}')
        self._code_to_mult_div(node, op='div', func_op=lambda x, y: int(x / y))

    def _code_to_mult_div(self, node, op:str, func_op):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_int(node.left) and self.is_int(node.right):
            try:
                self.code.append(f"li ${rdest}, {func_op(node.left, node.right)}")
            except ZeroDivisionError:
                self.code.append('la $a0, zero_error')
                self.code.append('j .raise')
        else:
            if self.is_variable(node.left):
                rleft = self.addr_desc.get_var_reg(node.left)
                if self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                elif self.is_int(node.right):
                    self.code.append(f"li $t9, {node.right}")
                    rright = 't9'
            elif self.is_int(node.left):
                # right es una variable porque falló el primer if
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                rleft = 't9'
            if op == 'div':
                self.code.append('la $a0, zero_error')
                self.code.append(f'beqz ${rright}, .raise')
            self.code.append(f"{op} ${rleft}, ${rright}")
            self.code.append(f"mflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(LessNode)
    def visit(self, node:LessNode):
        self.code.append(f'# {node.dest} <- {node.left} < {node.right}')
        self._code_to_comp(node, 'slt', lambda x, y: x < y)

    @visitor.when(LessEqNode)
    def visit(self, node:MinusNode):
        self.code.append(f'# {node.dest} <- {node.left} <= {node.right}')
        self._code_to_comp(node, 'sle', lambda x, y: x <= y)

    @visitor.when(EqualNode)
    def visit(self, node:MinusNode):
        self.code.append(f'# {node.dest} <- {node.left} = {node.right}')
        if self.is_variable(node.left) and self.is_variable(node.right) and self.var_address[node.left] == AddrType.STR and self.var_address[node.right] == AddrType.STR:
            self.compare_strings(node)
        else:
            self._code_to_comp(node, 'seq', lambda x, y: x == y)

    def _code_to_comp(self, node, op, func_op):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"{op} ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"li $t9, {node.right}")
                self.code.append(f"{op} ${rdest}, ${rleft}, $t9")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {int(func_op(node.left, node.right))}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                self.code.append(f"{op} ${rdest}, $t9, ${rright}")
        self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(GetAttribNode)
    def visit(self, node:GetAttribNode):
        self.code.append(f'# {node.dest} <- GET {node.obj} . {node.attr}')
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
            self.code.append(f'li $t9, {node.value}')
            rsrc = 't9'
        elif self.is_void(node.value):
            self.code.append(f'la $t9, type_{VOID_NAME}')
            rsrc = 't9'
        self.code.append(f'sw ${rsrc}, {attr_offset}(${rdest})') # saves the new value in the attr offset
        
    @visitor.when(AllocateNode)
    def visit(self, node:AllocateNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        size = 4*self.obj_table.size_of_entry(node.type)      # size of the table entry of the new type
        self.var_address[node.dest] = AddrType.REF
        # syscall to allocate memory of the object entry in heap
        
        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')                         # code to request memory
        self.code.append(f'li $a0, {size}')                   # argument (size)
        self.code.append('syscall')
        # in v0 is the address of the new memory
        addrs_stack = self.addr_desc.get_var_addr(node.dest)
        # self.code.append('# Save the address in the stack')
        # self.code.append(f'sw $v0, -{addrs_stack}($fp)')     # save the address in the stack (where is the local variable)

        self.code.append('# Loads the name of the variable and saves the name like the first field')
        self.code.append(f'la $t9, type_{node.type}')       # loads the name of the variable
        self.code.append(f'sw $t9, 0($v0)')                 # saves the name like the first field 

        self.code.append(f'# Saves the size of the node')
        self.code.append(f'li $t9, {size}')                 # saves the size of the node
        self.code.append(f'sw $t9, 4($v0)')                 # this is the second file of the table offset
        self.code.append(f'move ${rdest}, $v0')             # guarda la nueva dirección de la variable en el registro destino
      
        idx = self.types.index(node.type)
        self.code.append('# Adding Type Info addr')
        self.code.append('la $t8, types')
        self.code.append(f'lw $v0, {4*idx}($t8)')
        self.code.append(f'sw $v0, 8(${rdest})')
      

    @visitor.when(TypeOfNode)
    def visit(self, node:TypeOfNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# {node.dest} <- Type of {node.obj}')
        if self.is_variable(node.obj):
            rsrc = self.addr_desc.get_var_reg(node.obj)
            if self.var_address[node.obj] == AddrType.REF:
                self.code.append(f'lw ${rdest}, 0(${rsrc})')    # como en el offset 0 está el nombre del tipo this is ok
            elif self.var_address[node.obj] == AddrType.STR:
                self.code.append(f'la ${rdest}, type_String')
            elif self.var_address[node.obj] == AddrType.INT:
                self.code.append(f'la ${rdest}, type_Int')
            elif self.var_address[node.obj] == AddrType.BOOL:
                self.code.append(f'la ${rdest}, type_Bool')
        elif self.is_int(node.obj):
            self.code.append(f'la ${rdest}, type_Int')
        self.var_address[node.dest] = AddrType.STR

    @visitor.when(LabelNode)
    def visit(self, node:LabelNode):
        self.code.append(f'{node.label}:')

    @visitor.when(GotoNode)
    def visit(self, node:GotoNode):
        self.empty_registers()
        self.code.append(f'j {node.label}')

    @visitor.when(GotoIfNode)
    def visit(self, node:GotoIfNode):
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If {node.cond} goto {node.label}')
        self.empty_registers()
        self.code.append(f'bnez ${reg}, {node.label}')

    @visitor.when(GotoIfFalseNode)
    def visit(self, node:GotoIfNode):
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If not {node.cond} goto {node.label}')
        self.empty_registers()
        self.code.append(f'beqz ${reg}, {node.label}')

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
        reg = self.addr_desc.get_var_reg(node.obj)        # obtiene la instancia actual
        
        self.code.append('# Gets in a0 the actual direction of the dispatch table')
        self.code.append(f'lw $t9, 8(${reg})')          # obtiene en t9 la dirección del dispatch table
        self.code.append('lw $a0, 8($t9)')
        function = self.dispatch_table.find_full_name(node.type, node.method)       
        index = 4*self.dispatch_table.get_offset(node.type, function) + 4     # guarda el offset del me
        self.code.append(f'# Saves in t8 the direction of {function}')
        self.code.append(f'lw $t8, {index}($a0)')       # guarda en $t8 la dirección de la función a llamar 
        # Call function
        self._code_to_function_call(node.args, '$t8', node.dest, function)
        
        self.var_address[node.dest] = self.get_type(node.return_type)

    def _code_to_function_call(self, args, function, dest, function_name=None):
        self.push_register('fp')                    # pushes fp register to the stack
        self.push_register('ra')                    # pushes ra register to the stack
        self.code.append('# Push the arguments to the stack')
        for arg in reversed(args):              # push the arguments to the stack
            self.visit(arg)


        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()
        self.code.append('# This function will consume the arguments')
        
        self.code.append(f'jal {function}')         # this function will consume the arguments
        self.code.append('# Pop ra register of return function of the stack')
        self.pop_register('ra')                 # pop register ra from the stack
        self.code.append('# Pop fp register from the stack')
        self.pop_register('fp')                     # pop fp register from the stack
        if dest is not None:
            self.get_reg_var(dest)
            rdest = self.addr_desc.get_var_reg(dest)
            self.code.append('# saves the return value')
            self.code.append(f'move ${rdest}, $v0') # v0 es usado para guardar el valor de retorno

    @visitor.when(ArgNode)
    def visit(self, node:ArgNode):
        self.code.append('# The rest of the arguments are push into the stack')
        if self.is_variable(node.dest):
            self.get_reg_var(node.dest)
            reg = self.addr_desc.get_var_reg(node.dest)
            self.code.append(f'sw ${reg}, ($sp)')
        elif self.is_int(node.dest):
            self.code.append(f'li $t9, {node.dest}')
            self.code.append(f'sw $t9, ($sp)')
        self.code.append('addiu $sp, $sp, -4')
       
    @visitor.when(ReturnNode)
    def visit(self, node:ReturnNode):
        # save the return value
        if self.is_variable(node.value): 
            rdest = self.addr_desc.get_var_reg(node.value)
            self.code.append(f'move $v0, ${rdest}')
        elif self.is_int(node.value):
            self.code.append(f'li $v0, {node.value}')
        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()             # empty all used registers and saves them to memory
        self.code.append('# Removing all locals from stack')
        self.code.append(f'addiu $sp, $sp, {self.locals*4}')
        # return to the caller
        self.code.append(f'jr $ra')

        self.code.append('')

    @visitor.when(LoadNode)
    def visit(self, node:LoadNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# Saves in {node.dest} {node.msg}')
        self.var_address[node.dest] = AddrType.STR
        self.code.append(f'la ${rdest}, {node.msg}')
    
    @visitor.when(LengthNode)
    def visit(self, node: LengthNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        reg = self.addr_desc.get_var_reg(node.arg)
        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        # saving the value of reg to iterate
        self.code.append(f'move $t8, ${reg}')
        self.code.append('# Determining the length of a string')
        self.code.append(f'{loop}:')
        self.code.append(f'lb $t9, 0($t8)')
        self.code.append(f'beq $t9, $zero, {end}')
        self.code.append(f'addi $t8, $t8, 1')
        self.code.append(f'j {loop}')
        self.code.append(f'{end}:')

        self.code.append(f'sub ${rdest}, $t8, ${reg}')
        self.loop_idx += 1

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for the buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')
    

        rsrc1 = self.addr_desc.get_var_reg(node.arg1)
        if node.arg2 is not None:
            rsrc2 = self.addr_desc.get_var_reg(node.arg2)
        
        self.code.append('# Copy the first string to dest')
        var = self.save_reg_if_occupied('a1')
        self.code.append(f'move $a0, ${rsrc1}')
        self.code.append(f'move $a1, ${rdest}')
        self.push_register('ra')
        self.code.append('jal strcopier')

        if node.arg2 is not None:
            self.code.append('# Concatenate second string on result buffer')
            self.code.append(f'move $a0, ${rsrc2}')
            self.code.append(f'move $a1, $v0')
            self.code.append('jal strcopier')
        self.code.append('sb $0, 0($v0)')
        self.pop_register('ra')
        self.code.append(f'j finish_{self.loop_idx}')

        if self.first_defined['strcopier']:
            self.code.append('# Definition of strcopier')
            self.code.append('strcopier:')
            self.code.append('# In a0 is the source and in a1 is the destination')
            self.code.append(f'loop_{self.loop_idx}:')
            self.code.append('lb $t8, ($a0)')
            self.code.append(f'beq $t8, $zero, end_{self.loop_idx}')
            self.code.append('addiu $a0, $a0, 1')
            self.code.append('sb $t8, ($a1)')
            self.code.append('addiu $a1, $a1, 1')
            self.code.append(f'b loop_{self.loop_idx}')
            self.code.append(f'end_{self.loop_idx}:')
            self.code.append('move $v0, $a1')
            self.code.append('jr $ra')
            self.first_defined['strcopier'] = False
        
        self.code.append(f'finish_{self.loop_idx}:')
        self.load_var_if_occupied(var)
        self.loop_idx += 1

    @visitor.when(SubstringNode)
    def visit(self, node: SubstringNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for the buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')
    

        if self.is_variable(node.begin):
            rstart = self.addr_desc.get_var_reg(node.begin)
        elif self.is_int(node.begin):
            rstart = 't8'
            self.code.append(f'li $t8, {node.begin}')
        if self.is_variable(node.end):
            rend = self.addr_desc.get_var_reg(node.end)
            var = None
        elif self.is_int(node.end):
            var = self.save_reg_if_occupied('a3')
            rend = 'a3'
            self.code.append(f'li $a3, {node.end}')

        self.get_reg_var(node.word)
        rself = self.addr_desc.get_var_reg(node.word)

        self.code.append("# Getting the substring of a node")
        # Moves to the first position of the string
        # self.code.append(f'sll $t9, ${rstart}, 2')      # multiplicar por 4
        start = f'start_{self.loop_idx}'
        error = f'error_{self.loop_idx}'
        end_lp = f'end_len_{self.loop_idx}'

        self.code.append('# Move to the first position in the string')
        self.code.append('li $v0, 0')

        self.code.append(f'move $t8, ${rself}')
        self.code.append(f'{start}:')
        self.code.append('lb $t9, 0($t8)')
        self.code.append(f'beqz $t9, {error}')
        self.code.append('addi $v0, 1')
        self.code.append(f'bgt $v0, ${rstart}, {end_lp}')
        self.code.append(f'addi $t8, 1')
        self.code.append(f'j {start}')
        self.code.append(f'{end_lp}:')

        self.code.append('# Saving dest to iterate over him')
        self.code.append(f'move $v0, ${rdest}')

        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        # Loops moving the bytes until reaching to end
        self.code.append(f'{loop}:')
        self.code.append(f'sub $t9, $v0, ${rdest}') 

        self.code.append(f'beq $t9, ${rend}, {end}')
        self.code.append(f'lb $t9, 0($t8)')
        self.code.append(f'beqz $t9, {error}')  # if $t9 is zero error cause havent finished       
        self.code.append(f'sb $t9, 0($v0)')
        self.code.append('addi $t8, $t8, 1')
        self.code.append(f'addi $v0, $v0, 1')
        self.code.append(f'j {loop}')
        self.code.append(f'{error}:')
        self.code.append('la $a0, index_error')
        
        self.code.append('li $v0, 4')
        self.code.append(f'move $a0, ${rself}')
        self.code.append('syscall')
        
        self.code.append('li $v0, 1')
        self.code.append(f'move $a0, ${rstart}')
        self.code.append('syscall')
        
        self.code.append('li $v0, 1')
        self.code.append(f'move $a0, ${rend}')
        self.code.append('syscall')
        
        self.code.append('j .raise')
        self.code.append(f'{end}:')
        self.code.append('sb $0, 0($v0)')
        self.load_var_if_occupied(var)
        self.loop_idx += 1

    @visitor.when(OutStringNode)
    def visit(self, node: OutStringNode):
        reg = self.addr_desc.get_var_reg(node.value)
        self.code.append('# Printing a string')
        self.code.append('li $v0, 4')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')

    @visitor.when(OutIntNode)
    def visit(self, node: OutIntNode):
        if self.is_variable(node.value):
            reg = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'li $t8, ${node.value}')

        self.code.append('# Printing an int')
        self.code.append('li $v0, 1')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')
    

    @visitor.when(ReadStringNode)
    def visit(self, node: ReadStringNode):
        # self.data_code.append(f'{node.dest}: .space 20')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for the buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')
        # self.code.append(f'sb $0, 0(${rdest})')

        self.code.append('# Reading a string')
        var = self.save_reg_if_occupied('a1')
        self.code.append('# Putting buffer in a0')
        self.code.append(f'move $a0, ${rdest}')     # Get length of the string
        self.code.append('# Putting length of string in a1')
        self.code.append(f'li $a1, 356')             
        self.code.append('li $v0, 8')
        self.code.append('syscall')
        self.code.append('# Walks to eliminate the newline')
        
        start = f'start_{self.loop_idx}'
        end = f'end_{self.loop_idx}'

        self.code.append(f'move $t9, ${rdest}')
        self.code.append(f'{start}:')       # moves to the newline
        self.code.append('lb $t8, 0($t9)')
        self.code.append(f"beqz $t8, {end}")
        self.code.append('add $t9, $t9, 1')
        self.code.append(f'j {start}')
        self.code.append(f'{end}:')
        self.code.append('addiu $t9, $t9, -1')
        self.code.append('sb $0, ($t9)') # overwrites the newline with zero
        self.loop_idx += 1
        self.load_var_if_occupied(var)


    @visitor.when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Reading a int')
        self.code.append('li $v0, 5')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')


    @visitor.when(ExitNode)
    def visit(self, node: ExitNode):
        self.code.append('# Exiting the program')
        if self.is_variable(node.value):
            reg = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'li $t8, {node.value}')

        rself = self.addr_desc.get_var_reg(node.classx)
        
        'Abort called from class String'
        if self.var_address[node.classx] == AddrType.REF: 
            self.code.append('# Printing abort message')
            self.code.append('li $v0, 4')
            self.code.append(f'la $a0, abort_msg')
            self.code.append('syscall')

            self.code.append('li $v0, 4')
            self.code.append(f'lw $a0, 0(${rself})')
            self.code.append('syscall')    
            self.code.append('li $v0, 4')
            self.code.append(f'la $a0, new_line')
            self.code.append('syscall')
            
        self.code.append('li $v0, 17')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')

    @visitor.when(CopyNode)
    def visit(self, node: CopyNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.addr_desc.get_var_reg(node.source)

        self.code.append(f'lw $t9, 4(${rsrc})')             # getting the size of the object
        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')                       # code to request memory
        self.code.append(f'move $a0, $t9')                  # argument (size)
        self.code.append('syscall')

        self.code.append(f'move ${rdest}, $v0')
        
        self.code.append('# Loop to copy every field of the previous object')
        # loop to copy every field of the previous object
        self.code.append('# t8 the register to loop')
        self.code.append('li $t8, 0')
        self.code.append(f'loop_{self.loop_idx}:')
        self.code.append('# In t9 is stored the size of the object')
        self.code.append(f'bge $t8, $t9, exit_{self.loop_idx}')
        self.code.append(f'lw $a0, (${rsrc})')
        self.code.append('sw $a0, ($v0)')
        # offset in the copied element
        self.code.append('addi $v0, $v0, 4')
        # offset in the original element
        self.code.append(f'addi ${rsrc}, ${rsrc}, 4')
        self.code.append('# Increase loop counter')
        self.code.append('addi $t8, $t8, 4')
        self.code.append(f'j loop_{self.loop_idx}')
        self.code.append(f'exit_{self.loop_idx}:')
        self.loop_idx += 1

    @visitor.when(ConformsNode)
    def visit(self, node: ConformsNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        
        if self.is_variable(node.expr):
            rsrc = self.addr_desc.get_var_reg(node.expr)
            if self.var_address[node.expr] == AddrType.REF:
                self.conforms_to(rsrc, rdest, node.type)
            elif self.var_address[node.expr] == AddrType.STR:
                self.code.append(f'li ${rdest}, 0')
            elif self.var_address[node.expr] == AddrType.INT:
                self.code.append(f'li ${rdest}, 0')
            elif self.var_address[node.expr] == AddrType.BOOL:
                self.code.append(f'li ${rdest}, 0')
        elif self.is_int(node.expr):
            self.code.append(f'li ${rdest}, 0')        
     

    @visitor.when(ErrorNode)
    def visit(self, node: ErrorNode):
        self.code.append(f'la $a0, {node.type}')
        self.code.append('j .raise')

    @visitor.when(VoidConstantNode)
    def visit(self, node:VoidConstantNode):
        rdest = self.addr_desc.get_var_reg(node.out)
        self.code.append('# Initialize void node')
        self.code.append(f'li $a0, 4')                    # argument (size)
        self.code.append('li $v0, 9')                       # code to request memory
        self.code.append('syscall')
        self.code.append('# Loads the name of the variable and saves the name like the first field')
        self.code.append(f'la $t9, type_{VOID_NAME}')       # loads the name of the variable
        self.code.append('sw $t9, 0($v0)')                  # saves the name like the first field 
        self.code.append(f'move ${rdest}, $v0')
        self.var_address[node.obj] = AddrType.REF
     
    @visitor.when(BoxingNode)
    def visit(self, node:BoxingNode):
        "Node to convert a value type into object"
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Initialize new node')
        self.code.append('li $a0, 12')
        self.code.append('li $v0, 9')
        self.code.append('syscall')

        self.code.append(f'la $t9, type_{node.type}')
        self.code.append('sw $t9, 0($v0)')            # saves the name like the first field 
        self.code.append('li $t9, 12')
        self.code.append('sw $t9, 4($v0)')            # saves the size like the second field 
        self.code.append(f'move ${rdest}, $v0')
        
        self.code.append('# Saving the methods of object')
        idx = self.types.index('Object')
        self.code.append('# Adding Type Info addr')
        self.code.append('la $t8, types')
        self.code.append(f'lw $v0, {4*idx}($t8)')
        self.code.append(f'sw $v0, 8(${rdest})')
        self.var_address[node.dest] = AddrType.REF
