from codegen.cil_ast import *
from utils import visitor
from codegen.visitors.base_mips_visitor import BaseCILToMIPSVisitor
from codegen.tools import SymbolTable, AddressDescriptor, RegisterDescriptor
from semantic.tools import VariableInfo

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
 
    @visitor.when(TypeNode)
    def visit(self, node:TypeNode):
        self.obj_table.add_entry(node.name, node.methods, node.attributes)
        self.data_code.append(f"type_{node.name}: .asciiz \"{node.name}\"")     # guarda el nombre de la variable en la memoria            

    @visitor.when(DataNode)
    def visit(self, node:DataNode):
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")    

    @visitor.when(FunctionNode)
    def visit(self, node:FunctionNode, index:int):
        self.code.append(f'{node.name}:')
        
        # guardo la dirección del método en el array de métodos
        self.code.append(f'la $t9, {node.name}')
        self.code.append(f'la $v0, methods')
        self.code.append(f'sw $t9, {4*index}($v0)')

        self.code.append(f'move $fp, $sp')          # gets the frame pointer from the stack
        for i, param in enumerate(node.params):     # gets the params from the stack
            self.visit(param, i)
        for i, var in enumerate(node.localvars):
            self.visit(var, i+len(node.params))
        blocks = self.get_basic_blocks(node.instructions)
        self.next_use = self.construct_next_use(blocks)

        for block in blocks:
            self.block = block
            for inst in block:
                self.get_reg(inst)
                self.visit(inst)

    @visitor.when(ParamNode)
    def visit(self, node:ParamNode, idx:int):        
        self.symbol_table.insert_name(node.name)
        if idx <= 3:                                # los primeros 3 registros se guardan en a0-a3  
            self.addr_desc.insert_var(node.name, None, f'$a{idx}')
            self.reg_desc.insert_register(f'a{idx}', node.name)
        else:
            self.code.append('addiu $sp, $sp, 4')   # pops the register with the param value from stack      
            self.addr_desc.insert_var(node.name, idx)

    @visitor.when(LocalNode)
    def visit(self, node:LocalNode, idx:int):
        self.symbol_table.insert_name(node.name)              # inserts the var in the symbol table, local by default
        self.addr_desc.insert_var(node.name, idx)   # saves the address relative from the actual fp
        self.code.append(f'addiu $sp, $sp, -4')     # updates stack pointers (pushing this value)

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.source):
            rsrc = self.addr_desc.get_var_reg(node.source)
            self.code.append(f'move ${rdest}, ${rsrc}') 
        elif self.is_int(node.source):
            self.code.append(f'li ${rdest}, ${node.source}')
        elif isinstance(node.source, str):  # esto nunca se debe ejecutar (se llama a load node)
            self.code.append(f'la ${rdest}, {self.strings[node.source]}')

    @visitor.when(NotNode)
    def visit(self, node:NotNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rscr = self.save_to_register(node.expr)
        self.code.append(f'not {rdest}, {rsrc}')


    @visitor.when(PlusNode)
    def visit(self, node:PlusNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
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

    @visitor.when(MinusNode)
    def visit(self, node:MinusNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
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

    @visitor.when(StarNode)
    def visit(self, node:StarNode):
        self._code_to_mult_div(node, op='mult')

    @visitor.when(DivNode)
    def visit(self, node:DivNode):
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

    @visitor.when(LessNode)
    def visit(self, node:LessNode):
        self._code_to_comp(node, op='slt')

    @visitor.when(LessEqNode)
    def visit(self, node:MinusNode):
        self._code_to_comp(node, op='sle')

    @visitor.when(EqualNode)
    def visit(self, node:MinusNode):
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


    @visitor.when(GetAttribNode)
    def visit(self, node:GetAttribNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        self.code.append(f'lw ${rdest}, {attr_offset}(${rsrc})')


    @visitor.when(SetAttribNode)
    def visit(self, node:SetAttribNode):
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
        # syscall to allocate memory of the object entry in heap
        self.code.append('li $v0, 9')                         # code to request memory
        self.code.append(f'li $a0, {size}')                   # argument (size)
        self.code.append('syscall')
        # in v0 is the address of the new memory
        addrs_stack = self.addr_desc.get_var_addr(node.dest)
        self.code.append(f'sw $v0, -{addrs_stack}(fp)')     # save the address in the stack (where is the local variable)

        self.code.append(f'la $t9, type_{node.type}')       # loads the name of the variable
        self.code.append(f'sw $t9, 0($v0)')                 # saves the name like the first field 

        self.code.append(f'li $t9, {size}')                 # saves the size of the node
        self.code.append(f'sw $t9, 4($v0)')                 # this is the second file of the table offset
        self.code.append(f'move ${rdest}, $v0')             # guarda la nueva dirección de la variable en el registro destino

        self.create_dispatch_table(node.type)               # memory of dispatch table in v0
        self.code.append(f'sw $v0, 8(${rdest})')            # save a pointer of the dispatch table in the 3th position
       
    def create_dispatch_table(self, type_name):
        # Get methods of the dispatch table
        methods = self.dispatch_table.get_methods(type_name)
        # Allocate the dispatch table in the heap
        self.code.append('li $v0, 9')                       # code to request memory
        dispatch_table_size = 4*len(methods)
        self.code.append(f'li $a0, {dispatch_table_size}')
        self.code.append('syscall')                         # Memory of the dispatch table in v0
        
        for i, meth in enumerate(methods):
            # guardo el offset de cada uno de los métodos de este tipo
            offset = 4*self.methods.index(meth)
            self.code.append(f'la $t8, methods')            # cargo la dirección de methods
            self.code.append(f'lw $t9, {offset}($t8)')      # cargo la dirección del método en t9
            self.code.append(f'sw $t9, {4*i}($v0)')         # guardo la direccion del metodo en su posicion en el dispatch table        


    @visitor.when(TypeOfNode)
    def visit(self, node:TypeOfNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.obj):
            rsrc = self.addr_desc.get_var_reg(node.obj)
            # TODO: Falta comprobar si el tipo de la variable es por valor, en ese caso la información del nodo no estará en la primera posicion
            # De todas formas todavía falta la implementacion de los tipos built in
            self.code.append(f'la ${rdest}, 0(${rsrc})')    # como en el offset 0 está el nombre del tipo this is ok
        elif self.is_int(node.obj):
            # TODO: hacer algo para identificar el tipo int 
            pass

    @visitor.when(LabelNode)
    def visit(self, node:LabelNode):
        self.code.append(f'{node.label}')

    @visitor.when(GotoNode)
    def visit(self, node:GotoNode):
        self.code.append(f'j {node.label}')

    @visitor.when(GotoIfNode)
    def visit(self, node:GotoIfNode):
        reg = self.save_to_register(node.cond)
        self.code.append(f'bnez ${reg}, {node.label}')

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode):
        function = self.dispatch_table.find_full_name(node.type, node.function)
        self._code_to_function_call(node.args, function, node.dest)

    @visitor.when(DynamicCallNode)
    def visit(self, node:DynamicCallNode):
        # Find the actual name of the method in the dispatch table
        reg = self.addr_desc.get_var_reg('self')        # obtiene la instancia actual
        self.code.append(f'lw $t9, 8(${reg})')          # obtiene en t9 la dirección del dispatch table
        function = self.dispatch_table.find_full_name(node.type, node.method)       
        index = self.dispatch_table.get_offset(node.type, function)      # guarda el offset del me
        self.code.append(f'lw $t8, {index}($t9)')       # guarda en $t8 la dirección de la función a llamar 
        # Call function
        self._code_to_function_call(node.args, '$t8', node.dest)

    def _code_to_function_call(self, args, function, dest):
        self.empty_registers()                      # empty all used registers and saves them to memory
        self.push_register('fp')                    # pushes fp register to the stack
        self.push_register('ra')                    # pushes ra register to the stack
        for i, arg in enumerate(args):              # push the arguments to the stack
            self.visit(arg, i)

        self.code.append(f'jal {function}')         # this function will consume the arguments

        self.pop_register('fp')                     # pop fp register from the stack
        if dest is not None:
            rdest = self.addr_desc.get_var_reg(dest)
            self.code.append(f'move ${rdest}, $v0') # v0 es usado para guardar el valor de retorno

    @visitor.when(ArgNode)
    def visit(self, node:ArgNode, idx):
        if idx <= 3:        # los primeros 3 registros se guardan en a0-a2
            reg = f'a{idx}'
            if self.is_variable(node.dest):
                rdest = self.addr_desc.get_var_reg(node.dest)
                self.code.append(f'move ${reg}, ${rdest}')
            elif self.is_int(node.dest):
                self.code.append(f'li ${reg}, {node.dest}')
        else: 
            self.code.append('addiu $sp, $sp, -4')
            if self.is_variable(node.dest):
                reg = self.addr_desc.get_var_reg(node.dest)
                self.code.append(f'sw ${reg}, ($sp)')
            elif self.is_int(node.dest):
                self.code.append(f'li $t9, {node.dest}')
                self.code.append(f'sw $t9, ($sp)')
       
    @visitor.when(ReturnNode)
    def visit(self, node:ReturnNode):
        self.pop_register('ra')                 # pop register ra from the stack
        # save the return value
        if self.is_variable(node.value): 
            rdest = self.addr_desc.get_var_reg(node.value)
            self.code.append(f'move $v0, {rdest}')
        elif self.is_int(node.value):
            self.code.append(f'li $v0, {node.value}')
        # return to the caller
        self.code.append(f'jr $ra')

    @visitor.when(LoadNode)
    def visit(self, node:LoadNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'la ${rdest}, {node.msg}')