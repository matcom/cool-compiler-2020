from codegen.cil_ast import *
from utils import visitor
from codegen.visitors.base_mips_visitor import BaseCILToMIPSVisitor
from codegen.tools import SymbolTable, AddressDescriptor, RegisterDescriptor


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
        # visit code instrunctions
        for code in node.dotcode:
            self.visit(code)

    @visitor.when(TypeNode)
    def visit(self, node:TypeNode):
        pass

    @visitor.when(DataNode)
    def visit(self, node:DataNode):
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")        

    @visitor.when(FunctionNode)
    def visit(self, node:FunctionNode):
        for param in node.params:
            self.visit(param)
        for var in node.localvars:
            self.visit(var)
        blocks = self.get_basic_blocks(node.instructions)
        self.next_use = self.construct_next_use(blocks)
        for block in blocks:
            self.block = block
            for inst in block:
                self.code += self.get_reg(inst, self.usable_reg)
                self.visit(inst)

    @visitor.when(ParamNode)
    def visit(self, node:ParamNode):
        self.code.append('addiu $sp, $sp, -4')
        register = self.addr_desc.get_var_reg(node.name)
        self.code.append(f'sw $sp, ${register} ($sp)')

    # @visitor.when(LocalNode)
    # def visit(self, node:LocalNode):
    #     pass

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode):
        pass

    @visitor.when(NotNode)
    def visit(self, node:NotNode):
        pass

    @visitor.when(BinaryNotNode)
    def visit(self, node:BinaryNotNode):
        pass

    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode):
        pass

    @visitor.when(PlusNode)
    def visit(self, node:PlusNode):
        pass

    @visitor.when(MinusNode)
    def visit(self, node:MinusNode):
        pass

    @visitor.when(StarNode)
    def visit(self, node:StarNode):
        pass

    @visitor.when(DivNode)
    def visit(self, node:DivNode):
        pass

    @visitor.when(GetAttribNode)
    def visit(self, node:GetAttribNode):
        pass

    @visitor.when(SetAttribNode)
    def visit(self, node:SetAttribNode):
        pass

    @visitor.when(AllocateNode)
    def visit(self, node:AllocateNode):
        pass

    @visitor.when(TypeOfNode)
    def visit(self, node:TypeOfNode):
        pass

    @visitor.when(LabelNode)
    def visit(self, node:LabelNode):
        pass

    @visitor.when(GotoNode)
    def visit(self, node:GotoNode):
        pass

    @visitor.when(GotoIfNode)
    def visit(self, node:GotoIfNode):
        pass

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode):
        pass

    @visitor.when(DynamicCallNode)
    def visit(self, node:DynamicCallNode):
        pass

    @visitor.when(ArgNode)
    def visit(self, node:ArgNode):
        pass

    @visitor.when(ReturnNode)
    def visit(self, node:ReturnNode):
        pass

    @visitor.when(LoadNode)
    def visit(self, node:LoadNode):
        pass

    @visitor.when(SelfNode)
    def visit(self, node:SelfNode):
        pass