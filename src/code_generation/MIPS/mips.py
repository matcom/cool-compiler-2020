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
    # revisar que save_callee_registers no tiene valor de retorno
    code = save_callee_registers()
    for i, param in enumerate(function.params):
        __ADDRS__[param.id] = (len(function.params)-1-i)*4

    code += allocate_stack(len(function.locals)*4)
    for i, local in enumerate(function.locals):
        __ADDRS__[local.id] = (len(function.locals)-1-i)*4

    for inst in function.body:
        code += instruction_to_mips_visitor(inst)

    code += restore_callee_registers()
    code += restore_stack(len(function.locals)*4)


def instruction_to_mips_visitor(inst):
    try:
        return __visitors__[type(inst)]
    except KeyError:
        raise Exception(f'There is no visitor for {type(inst)}')


def vcall_to_mips_visitor(vcall: cil.VCAllNode):
    return save_caller_registers() + [mips.JalInstruction([__METHOD_MAPPING__[(vcall.type, vcall.method)]])] + restore_caller_registers() + [mips.MoveInstruction(['$v0', __ADDRS__[vcall.result]])]


def arg_to_mips_visitor(arg: cil.ArgNode):
    return allocate_stack(4) + push_stack(__ADDRS__[arg.val])


__visitors__ = {
    cil.VCAllNode: vcall_to_mips_visitor,
    cil.ArgNode: arg_to_mips_visitor
}
