from code_generation.CIL import ast as cil
from code_generation.MIPS import ast as mips
from .utilities import *

__METHOD_MAPPING__ = {}
__ADDRS__ = {}


def program_to_mips_visitor(program: cil.ProgramNode):
    global __METHOD_MAPPING__

    # Initialize Types Codes
    init_types(program.types)

    # filling method mapping
    for t in program.types:
        for m in t.methods:
            __METHOD_MAPPING__[(t, m)] = t.methods[m]

    data = [mips.MIPSDataItem(d.id, mips.AsciizInst(d.val))
            for d in program.data]
    data_section = mips.MIPSDataSection(data)
    # continue
    functions = [function_to_mips_visitor(
        f) for f in program.built_in_code + program.code]
    text_section = mips.MIPSTextSection(functions)
    return mips.MIPSProgram(data_section, text_section)


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
    for i, param in enumerate(function.params):
        __ADDRS__[param.id] = f'{(len(function.params)-1-i)*4}($sp)'

    code = save_callee_registers()

    code += allocate_stack(len(function.locals)*4)
    for i, local in enumerate(function.locals):
        __ADDRS__[local.id] = f'{(len(function.locals)-1-i)*4}($sp)'

    for inst in function.body:
        code += instruction_to_mips_visitor(inst)

    code += restore_stack(len(function.params)*4)
    code += restore_callee_registers()
    code += restore_stack(len(function.locals)*4)
    code.append(mips.JrInstruction('$ra'))
    return mips.MIPSFunction(function.name, code)


def instruction_to_mips_visitor(inst):
    '''
    Resolves visitor for each type
    '''
    try:
        return __visitors__[type(inst)](inst)
    except KeyError:
        print(f'There is no visitor for {type(inst)}')
        return []


def vcall_to_mips_visitor(vcall: cil.VCAllNode):
    '''
    Converts an VCall CIL node to a piece of MIPS code:\n
    1) Saves caller registers\n
    2) Jumps to function label and sets the value of ra\n
    3) Restore caller registers\n
    4) Takes the result from v0
    '''
    return [mips.Comment(str(vcall))]+save_caller_registers() + [mips.JalInstruction(__METHOD_MAPPING__[(vcall.type, vcall.method)])] + restore_caller_registers() + [mips.MoveInstruction('$v0', __ADDRS__[vcall.result])]


def arg_to_mips_visitor(arg: cil.ArgNode):
    '''
    Converts an Arg CIL node to a piece of MIPS code:\n
    1) Allocates a 4-bytes space in stack\n
    2) Pushes the arg value in the stack\n
    '''
    return [mips.Comment(str(arg))] + allocate_stack(4) + push_stack(__ADDRS__[arg.val])


def allocate_to_mips_visitor(allocate: cil.AllocateNode):
    """
    CIL:
        x  = ALLOCATE T
    MIPS:
        li      $a0, [syze(T)]
        li      $v0, 9
        syscall
        sw      $v0, [addr(x)]
    """
    size = get_type(allocate.type).size_mips
    address = __ADDRS__[allocate.result]
    code = [
        mips.Comment(str(allocate)),
        mips.LiInstruction('$a0', size),
        mips.LiInstruction('$v0', 9),
        mips.SyscallInstruction(),
        mips.SwInstruction('$v0', address)
    ]
    return code


def copy_to_mips_visitor(copy: cil.CopyNode):
    """
    CIL:
        x = COPY y
    MIPS:
        lw  $t0, [addr(y)]
        sw  $t0, [addr(x)]
    """
    x_addr = __ADDRS__[copy.result]
    y_addr = __ADDRS__[copy.val]
    return [
        mips.Comment(str(copy)),
        mips.LwInstruction('$t0', y_addr),
        mips.SwInstruction('$t0', x_addr)
    ]


def getattr_to_mips_visitor(getattr: cil.GetAttrNode):
    """
    CIL:
        x = GETATTR y attr
    MIPS:
        lw  $t0, [addr(y)]
        lw  $t1, [attr_shift($t0)]
        sw  $t1, [addr(x)]
    """

    x_addr = __ADDRS__[getattr.result]
    y_addr = __ADDRS__[getattr.obj]
    attr_shift = (getattr.attr_index + 1) * 4
    return [
        mips.Comment(str(getattr)),
        mips.LwInstruction('$t0', y_addr),
        mips.LwInstruction('$t1', f'{attr_shift}($t0)'),
        mips.SwInstruction('$t1', x_addr)
    ]


def setattr_to_mips_visitor(setattr: cil.SetAttrNode):
    """
    CIL:
        SETATTR y attr x
    MIPS:
        lw  $t0, [addr(x)]
        lw  $t1, [addr(y)]
        sw  $t0, [attr_shift($t0)]
    """
    x_addr = __ADDRS__[setattr.val]
    y_addr = __ADDRS__[setattr.obj]
    attr_shift = (setattr.attr_index + 1) * 4
    return [
        mips.Comment(str(setattr)),
        mips.LwInstruction('$t0', x_addr),
        mips.LwInstruction('$t1', y_addr),
        mips.SwInstruction('$t0', f'{attr_shift}($t0)')
    ]


def plus_to_mips_visitor(plus: cil.PlusNode):
    """
    CIL:
        x = y + z
    MIPS:
        lw  $t1, [addr(y)]
        lw  $t2, [addr(z)]
        add $t0, $t1, $t2
        sw  $t0, [addr(x)]
    """

    x_addr = __ADDRS__[plus.result]
    y_addr = __ADDRS__[plus.left]
    z_addr = __ADDRS__[plus.right]
    return [
        mips.Comment(str(plus)),
        mips.LwInstruction('$t1', y_addr),
        mips.LwInstruction('$t2', z_addr),
        mips.AddInstruction('$t0', '$t1', '$t2'),
        mips.SwInstruction('$t0', x_addr)
    ]


def minus_to_mips_visitor(minus: cil.MinusNode):
    """
    CIL:
        x = y - z
    MIPS:
        lw  $t1, [addr(y)]
        lw  $t2, [addr(z)]
        sub $t0, $t1, $t2
        sw  $t0, [addr(x)]
    """
    x_addr = __ADDRS__[minus.result]
    y_addr = __ADDRS__[minus.left]
    z_addr = __ADDRS__[minus.right]
    return [
        mips.Comment(str(minus)),
        mips.LwInstruction('$t1', y_addr),
        mips.LwInstruction('$t2', z_addr),
        mips.SubInstruction('$t0', '$t1', '$t2'),
        mips.SwInstruction('$t0', x_addr)
    ]


def star_to_mips_visitor(star: cil.StarNode):
    """
    CIL:
        x = y * z
    MIPS:
        lw  $t1, [addr(y)]
        lw  $t2, [addr(z)]
        mult $t0, $t1, $t2
        sw  $t0, [addr(x)]
    """
    x_addr = __ADDRS__[star.result]
    y_addr = __ADDRS__[star.left]
    z_addr = __ADDRS__[star.right]
    return [
        mips.Comment(str(star)),
        mips.LwInstruction('$t1', y_addr),
        mips.LwInstruction('$t2', z_addr),
        mips.MultInstruction('$t0', '$t1', '$t2'),
        mips.SwInstruction('$t0', x_addr)
    ]


def div_to_mips_visitor(div: cil.DivNode):
    """
    CIL:
        x = y / z
    MIPS:
        lw  $t1, [addr(y)]
        lw  $t2, [addr(z)]
        div $t0, $t1, $t2
        sw  $t0, [addr(x)]
    """
    x_addr = __ADDRS__[div.result]
    y_addr = __ADDRS__[div.left]
    z_addr = __ADDRS__[div.right]
    return [
        mips.Comment(str(div)),
        mips.LwInstruction('$t1', y_addr),
        mips.LwInstruction('$t2', z_addr),
        mips.DivInstruction('$t0', '$t1', '$t2'),
        mips.SwInstruction('$t0', x_addr)
    ]


def lesseq_to_mips_visitor(lesseq: cil.LessEqNode):
    """
    CIL:
        x = y <= z
    MIPS:
        lw  $t1, [addr(y)]
        lw  $t2, [addr(z)]
        sle $t0, $t1, $t2
        sw  $t0, [addr(x)]
    """

    x_addr = __ADDRS__[lesseq.result]
    y_addr = __ADDRS__[lesseq.left]
    z_addr = __ADDRS__[lesseq.right]
    return [
        mips.Comment(str(lesseq)),
        mips.LwInstruction('$t1', y_addr),
        mips.LwInstruction('$t2', z_addr),
        mips.SleInstruction('$t0', '$t1', '$t2'),
        mips.SwInstruction('$t0', x_addr)
    ]


def less_to_mips_visitor(less: cil.LessNode):
    """
    CIL:
        x = y < z
    MIPS:
        lw  $t1, [addr(y)]
        lw  $t2, [addr(z)]
        slt $t0, $t1, $t2
        sw  $t0, [addr(x)]
    """

    x_addr = __ADDRS__[less.result]
    y_addr = __ADDRS__[less.left]
    z_addr = __ADDRS__[less.right]
    return [
        mips.Comment(str(less)),
        mips.LwInstruction('$t1', y_addr),
        mips.LwInstruction('$t2', z_addr),
        mips.SleInstruction('$t0', '$t1', '$t2'),
        mips.SwInstruction('$t0', x_addr)
    ]


def not_to_mips_visitor(notn: cil.NotNode):
    """
    CIL:
        x = ~ y
    MIPS:
        lw  $t1, [addr(y)]
        not $t0, $t1
        sw  $t0, [addr(x)]
    """
    x_addr = __ADDRS__[notn.result]
    y_addr = __ADDRS__[notn.value]
    return [
        mips.Comment(str(notn)),
        mips.LwInstruction('$t1', y_addr),
        mips.NotInstruction('$t0', '$t1'),
        mips.SwInstruction('$t0', x_addr)
    ]


__visitors__ = {
    cil.VCAllNode: vcall_to_mips_visitor,
    cil.ArgNode: arg_to_mips_visitor,
    cil.AllocateNode: allocate_to_mips_visitor,
    cil.CopyNode: copy_to_mips_visitor,
    cil.GetAttrNode: getattr_to_mips_visitor,
    cil.SetAttrNode: setattr_to_mips_visitor,
    cil.PlusNode: plus_to_mips_visitor,
    cil.MinusNode: minus_to_mips_visitor,
    cil.StarNode: star_to_mips_visitor,
    cil.DivNode: div_to_mips_visitor,
    cil.LessEqNode: lesseq_to_mips_visitor,
    cil.LessNode: less_to_mips_visitor,
    cil.NotNode: not_to_mips_visitor,
}
