from code_generation.CIL import ast as cil
from code_generation.MIPS import ast as mips
from .utilities import *

__METHOD_MAPPING__ = {}
__BUFFSIZE__ = 1024
__DATA__ = []


def program_to_mips_visitor(program: cil.ProgramNode):
    global __METHOD_MAPPING__, __DATA__

    # Initialize Types Codes
    init_types(program.types)
    vt_code = build_virtual_tables(program)

    # filling method mapping
    for t in program.types:
        for m in t.methods:
            __METHOD_MAPPING__[(t.type, m)] = t.methods[m]

    __DATA__ = [mips.MIPSDataItem(d.id, mips.AsciizInst(d.val))
                for d in program.data]

    functions = [function_to_mips_visitor(
        f) for f in program.built_in_code + program.code]
    text_section = mips.MIPSTextSection(functions)
    data_section = mips.MIPSDataSection(vt_code + __DATA__)
    return mips.MIPSProgram(data_section, text_section)


def build_virtual_tables(program: cil.ProgramNode):
    code = [mips.MIPSDataItem(f'vt_{t.type}', mips.SpaceInst(t.size_vt)) for t in program.types]
    return code


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
        save_address(param.id, f'{(len(function.params)-1-i)*4}($sp)')

    code = save_callee_registers()

    code += allocate_stack(len(function.locals)*4)
    for i, local in enumerate(function.locals):
        save_address(local.id, f'{(len(function.locals)-1-i)*4}($sp)')

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


def print_to_mips_visitor(p: cil.PrintNode):
    addr=get_address(p.str)
    code = [mips.Comment(str(p)), mips.MoveInstruction(
        '$a0',addr)]
    if p.str == 'int':
        code += [
            mips.LiInstruction('$v0', 1),
            mips.SyscallInstruction(),
        ]
    elif p.str == 'str':
        code += [
            mips.LiInstruction('$v0', 4),
            mips.SyscallInstruction(),
        ]

    return code


def return_to_mips_visitor(ret: cil.ReturnNode):
    code = [mips.Comment(str(ret))]
    if type(ret.ret_value) is int:
        code.append(mips.LiInstruction('$v0', ret.ret_value))
    else:
        val = get_address(ret.ret_value)
        code.append(mips.LwInstruction('$v0', val))
    return code

def read_to_mips_visitor(read:cil.ReadNode):
    __DATA__.append(mips.MIPSDataItem(read.result.id, mips.SpaceInst(__BUFFSIZE__)))
    save_address(read.result, read.result.id)
    code = [ 
            mips.Comment(str(read)), 
            mips.LaInstruction('$a0', read.result),
            mips.LiInstruction('$a1', __BUFFSIZE__),
            mips.LiInstruction('$v0', 8), 
            mips.SyscallInstruction()
    ]
    return code


def substring_to_mips_visitor(ss:cil.SubStringNode):
    addr=get_address(ss.str)
    i=get_address(ss.i)
    l=get_address(ss.len)
    __DATA__.append(mips.MIPSDataItem(ss.result.id, mips.SpaceInst(__BUFFSIZE__)))
    save_address(ss.result, ss.result.id)
    code = [
        mips.Comment(str(ss)),
        mips.LaInstruction('$t0', addr), 
        mips.LaInstruction('$t1', ss.result.id),
        mips.LwInstruction('$t4', i),
        mips.LwInstruction('$t2', l),
        mips.AdduInstruction('$t0', '$t0', '$t4'),
        mips.MIPSLabel('substring_loop'),
        mips.BeqzInstruction('$t2', 'end_substring_loop'),
        mips.LbInstruction('$t3', '($t0)'),
        mips.SbInstruction('$t3', '($t1)'), 
        mips.SubuInstruction('$t2', '$t2', 1),
        mips.AdduInstruction('$t0', '$t0', 1),
        mips.AdduInstruction('$t1', '$t1', 1),
        mips.BInstruction('substring_loop'),
        mips.MIPSLabel('end_substring_loop')
    ]
    return code

def read_int_to_mips_visitor(read:cil.ReadIntNode):
    addr=get_address(read.result)
    code = [ 
            mips.Comment(str(read)), 
            mips.LiInstruction('$v0', 5), 
            mips.SyscallInstruction(),
            mips.SwInstruction('$v0', addr)
    ]
    return code


def length_to_mips_visitor(length: cil.LengthNode):
    val= get_address(length.str)
    result_val= get_address(length.result)

    code = [
        mips.Comment(str(length)),
        mips.LbInstruction('$t0', val),
        mips.LiInstruction('$t1', 0),
        mips.MIPSLabel('length_loop'),
        mips.BeqzInstruction('$t0', 'end_length_loop'),
        mips.AdduInstruction('$t0', '$t0', 1),
        mips.AdduInstruction('$t1', '$t1', 1),
        mips.BInstruction('length_loop'),
        mips.MIPSLabel('end_length_loop'),
        mips.SwInstruction('$t1', result_val)
    ]
    return code

def concat_to_mips_visitor(concat:cil.ConcatNode):
    __DATA__.append(mips.MIPSDataItem(concat.result.id, mips.SpaceInst(2 * __BUFFSIZE__)))
    save_address(concat.result, concat.result.id)
    a = get_address(concat.str_a)
    b = get_address(concat.str_b)
    
    code = [
        mips.Comment(str(concat)),
        mips.LwInstruction('$t0', a),
        mips.SwInstruction('$t0', concat.result),
        mips.LbInstruction('$t1', concat.result),
        mips.MIPSLabel('length_loop'),
        mips.BeqzInstruction('$t1', 'end_length_loop'),
        mips.AdduInstruction('$t1', '$t1', 1),
        mips.BInstruction('length_loop'),
        mips.MIPSLabel('end_length_loop'),
        mips.LwInstruction('$t2', b),
        mips.SwInstruction('$t2', '($t1)')
    ]

    return code


def load_to_mips_visitor(load: cil.LoadNode):
    save_address(load.result, load.addr)
    return []


def arg_to_mips_visitor(arg: cil.ArgNode):
    '''
    Converts an Arg CIL node to a piece of MIPS code:\n
    1) Allocates a 4-bytes space in stack\n
    2) Pushes the arg value in the stack\n
    '''
    addr= get_address(arg.val)
    return [mips.Comment(str(arg))] + allocate_stack(4) + push_stack(addr)


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
    address = get_address(allocate.result)
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
    x_addr = get_address( copy.result)
    y_addr = get_address( copy.val)
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

    x_addr = get_address( getattr.result)
    y_addr = get_address( getattr.obj)
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
    x_addr = get_address(setattr.val)
    y_addr = get_address(setattr.obj)
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

    x_addr = get_address(plus.result)
    y_addr = get_address(plus.left)
    z_addr = get_address(plus.right)
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
    x_addr = get_address(minus.result)
    y_addr = get_address(minus.left)
    z_addr = get_address(minus.right)
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
    x_addr = get_address(star.result)
    y_addr = get_address(star.left)
    z_addr = get_address(star.right)
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
    x_addr = get_address(div.result)
    y_addr = get_address(div.left)
    z_addr = get_address(div.right)
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

    x_addr = get_address(lesseq.result)
    y_addr = get_address(lesseq.left)
    z_addr = get_address(lesseq.right)
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

    x_addr = get_address(less.result)
    y_addr = get_address(less.left)
    z_addr = get_address(less.right)
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
    x_addr = get_address(notn.result)
    y_addr = get_address(notn.value)
    return [
        mips.Comment(str(notn)),
        mips.LwInstruction('$t1', y_addr),
        mips.NotInstruction('$t0', '$t1'),
        mips.SwInstruction('$t0', x_addr)
    ]


__visitors__ = {
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
    cil.PrintNode: print_to_mips_visitor,
    cil.ReturnNode: return_to_mips_visitor,
    cil.ReadNode: read_to_mips_visitor, 
    cil.ReadIntNode: read_int_to_mips_visitor, 
    cil.LengthNode: length_to_mips_visitor, 
    cil.ConcatNode: concat_to_mips_visitor, 
    cil.LoadNode:load_to_mips_visitor, 
    cil.SubStringNode:substring_to_mips_visitor
}
