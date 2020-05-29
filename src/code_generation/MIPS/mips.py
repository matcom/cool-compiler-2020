from code_generation.CIL import ast as cil
from . import ast as mips
from .utilities import *

__METHOD_MAPPING__ = {}
__ADDRS__ = {}


def program_to_mips_visitor(program: cil.ProgramNode):
    global __METHOD_MAPPING__

    # Initialize Types Codes
    init_types_codes(program.types)

    # filling method mapping
    for t in program.types:
        for m in t.methods:
            __METHOD_MAPPING__[(t, m)] = t.methods[m]

    data_section = [mips.AsciizInst(d.val) for d in program.data]
    # continue
    text_section = []

    for function in program.built_in_code + program.code:
        text_section += function_to_mips_visitor(function)



def function_to_mips_visitor(function):
    '''
    Converts a function CIL to a piece of MIPS code:\n
    1) Assigns the right stack address to each param id\n
    2) Saves callee registers\n
    3) Assigns and allocates a chunk in the stack for each local\n
    4) Appends MIPS translation of each instruction in CIL body\n
    5) Restores param's space in stack\n
    6) Restores callee registers\n
    7) Restores local's stack space\n
    8) Jumps to the next instruction which address is in ra register\n
    '''
    for i,param in enumerate(function.params):
        __ADDRS__[param.id]=(len(function.params)-1-i)*4
              
    code=save_callee_registers()
    
    code+=allocate_stack(len(function.locals)*4)
    for i,local in enumerate(function.locals):
        __ADDRS__[local.id]=(len(function.locals)-1-i)*4
    
    for inst in function.body:
        code += instruction_to_mips_visitor(inst)
        
    
    code+=restore_stack(len(function.params)*4)
    code += restore_callee_registers()
    code += restore_stack(len(function.locals)*4)
    code.append(mips.JrInstruction('$ra'))    
    return code


def instruction_to_mips_visitor(inst):
    '''
    Resolves visitor for each type
    '''
    try:
        return __visitors__[type(inst)]
    except KeyError:
        raise Exception(f'There is no visitor for {type(inst)}')



def vcall_to_mips_visitor(vcall: cil.VCAllNode):
    '''
    Converts an VCall CIL node to a piece of MIPS code:\n
    1) Saves caller registers\n
    2) Jumps to function label and sets the value of ra\n
    3) Restore caller registers\n
    4) Takes the result from v0
    '''
    return save_caller_registers() + [mips.JalInstruction([__METHOD_MAPPING__[(vcall.type, vcall.method)]])] + restore_caller_registers() + [mips.MoveInstruction(['$v0', __ADDRS__[vcall.result]])]


def arg_to_mips_visitor(arg: cil.ArgNode):
    '''
    Converts an Arg CIL node to a piece of MIPS code:\n
    1) Allocates a 4-bytes space in stack\n
    2) Pushes the arg value in the stack\n
    '''
    return allocate_stack(4) + push_stack(__ADDRS__[arg.val])


def allocate_to_mips_visitor(allocate: cil.AllocateNode):
    """
    CIL:
        x  = ALLOCATE T
    MIPS:
        li      $a0, [syze(T)]
        li      $v0, 9
        syscall
        move    [addr(x)], $v0
    """
    size = get_type_size(allocate.type)
    address = __ADDRS__[allocate.result]
    code = [
        mips.LiInstruction(('$a0', size)),
        mips.LiInstruction(('$v0', 9)),
        mips.SyscallInstruction(),
        mips.MoveInstruction((address, '$v0'))
    ]
    return code


def copy_to_mips_visitor(copy: cil.CopyNode):
    """
    CIL:
        x = COPY y
    MIPS:
        move [addr(x)], [addr(y)]
    """
    x_addr = __ADDRS__[copy.result]
    y_addr = __ADDRS__[copy.val]
    return [mips.MoveInstruction((x_addr, y_addr))]


__visitors__ = {
    cil.VCAllNode: vcall_to_mips_visitor,
    cil.ArgNode: arg_to_mips_visitor,
    cil.AllocateNode: allocate_to_mips_visitor,
    cil.CopyNode: copy_to_mips_visitor
}
