from code_generation.CIL import ast as cil
from code_generation.MIPS import ast as mips
from .utilities import *

__BUFFSIZE__ = 1024
__DATA__ = []
CURRENT_FUNCTION = None
__VT__ = {}


def program_to_mips_visitor(program: cil.ProgramNode):
    global __DATA__, __VT__

    # Build Virtual Table
    q = program.types.copy()
    t = q.pop(0)
    if t.type != 'SELF_TYPE':
        raise Exception("unexpected first type")

    while len(q):
        t = q.pop(0)
        for method, type_impl in t.methods.items():
            if type_impl == t.type:
                __VT__[(t.type, method)] = f'{type_impl}_{method}'
            else:
                try:
                    __VT__[(t.type, method)] = __VT__[(type_impl, method)]
                except KeyError:
                    q.append(t)

    # Initialize Types
    init_types(program.types)

    # Build .data section
    # vt_space_code = reserve_virtual_tables_space(program)
    __DATA__ = [mips.MIPSDataItem(d.id, mips.AsciizInst(d.val))
                for d in program.data]
    data_section = mips.MIPSDataSection(__DATA__)

    # Build .text section
    functions = [function_to_mips_visitor(f)
                 for f in program.built_in_code + program.code]
    text_section = mips.MIPSTextSection(functions)
    return mips.MIPSProgram(data_section, text_section)


def reserve_virtual_tables_space(program: cil.ProgramNode):
    """
    Each virtual table has a space in the .data section. The 
    space is 4 bytes for each function, where the address of 
    the real function is stored.
    """
    code = [mips.MIPSDataItem(f'vt_{t.type}', mips.SpaceInst(t.size_vt))
            for t in program.types[1:]]
    return code


def function_to_mips_visitor(function):
    """
    Convert a CIL function to a block of MIPS code.
    1- Initialize function context
    2- Set CURRENT_FUNCTION for the use of other functions
    3- Add each CIL instruction to function.
    4- Mark as ended the CIL function
    """
    global CURRENT_FUNCTION
    # 1
    f = mips.MIPSFunction(function.name, function.params, function.locals)
    # 2
    CURRENT_FUNCTION = f
    # 3
    for cil_inst in function.body:
        for mips_inst in instruction_to_mips_visitor(cil_inst):
            CURRENT_FUNCTION.append_instruction(mips_inst)
    # 4
    f.end()
    return f


def instruction_to_mips_visitor(inst):
    """
    Resolves visitor for each type
    """
    try:
        return __visitors__[type(inst)](inst)
    except KeyError:
        print(f'There is no visitor for {type(inst)}')
    return []


def print_to_mips_visitor(p: cil.PrintNode):
    """
    CIL:
        PRINT z;
    MIPS if z is int:
        move    $a0, addr(z)
        li      $v0, 1
        syscall
    MIPS if z is str:
        move    $a0, addr(z)
        li      $v0, 4
        syscall
    """
    addr_z = CURRENT_FUNCTION.get_address(p.str)
    code = [mips.Comment(str(p)),
            mips.MoveInstruction('$a0', addr_z)]  # move  $a0, addr(z)
    if p.str == 'int':
        code.append(mips.LiInstruction('$v0', 1))  # li    $v0, 1
    elif p.str == 'str':
        code.append(mips.LiInstruction('$v0', 4))  # li    $v0, 4
    code.append(mips.SyscallInstruction())  # syscall
    return code


def return_to_mips_visitor(ret: cil.ReturnNode):
    """
    CIL:
        RETURN x;
    MIPS if x is int:
        li  $v0, x
    MIPS ix x is not int:
        lw  $v0, addr(x)
    """
    code = [mips.Comment(str(ret))]
    if type(ret.ret_value) is int:
        code.append(mips.LiInstruction('$v0', ret.ret_value))  # li  $v0, x
    else:
        addr_x = CURRENT_FUNCTION.get_address(str(ret.ret_value))
        code.append(mips.LwInstruction('$v0', addr_x))  # lw  $v0, addr(x)
    return code


def read_to_mips_visitor(read: cil.ReadNode):
    __DATA__.append(mips.MIPSDataItem(
        read.result.id, mips.SpaceInst(__BUFFSIZE__)))
    save_address(read.result, read.result.id)
    code = [
        mips.Comment(str(read)),
        mips.LaInstruction('$a0', read.result),
        mips.LiInstruction('$a1', __BUFFSIZE__),
        mips.LiInstruction('$v0', 8),
        mips.SyscallInstruction()
    ]
    return code


def substring_to_mips_visitor(ss: cil.SubStringNode):
    addr = CURRENT_FUNCTION.get_address(ss.str)
    i = CURRENT_FUNCTION.get_address(ss.i)
    l = CURRENT_FUNCTION.get_address(ss.len)
    __DATA__.append(mips.MIPSDataItem(
        ss.result.id, mips.SpaceInst(__BUFFSIZE__)))
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


def read_int_to_mips_visitor(read: cil.ReadIntNode):
    addr = CURRENT_FUNCTION.get_address(str(read.result))
    code = [
        mips.Comment(str(read)),
        mips.LiInstruction('$v0', 5),
        mips.SyscallInstruction(),
        mips.SwInstruction('$v0', addr)
    ]
    return code


def length_to_mips_visitor(length: cil.LengthNode):
    val = CURRENT_FUNCTION.get_address(length.str)
    result_val = CURRENT_FUNCTION.get_address(str(length.result))

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


def concat_to_mips_visitor(concat: cil.ConcatNode):
    __DATA__.append(mips.MIPSDataItem(concat.result.id,
                                      mips.SpaceInst(2 * __BUFFSIZE__)))
    save_address(concat.result, concat.result.id)
    a = CURRENT_FUNCTION.get_address(concat.str_a)
    b = CURRENT_FUNCTION.get_address(concat.str_b)

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
    addr = CURRENT_FUNCTION.get_address(str(arg.val))
    return [mips.Comment(str(arg))] + allocate_stack(4) + push_stack(addr, '($sp)')


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
    address = CURRENT_FUNCTION.ADDR[allocate.result]
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
    x_addr = CURRENT_FUNCTION.get_address(str(copy.result))
    y_addr = CURRENT_FUNCTION.get_address(copy.val)
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

    x_addr = CURRENT_FUNCTION.get_address(str(getattr.result))
    y_addr = CURRENT_FUNCTION.get_address(getattr.obj)
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
    x_addr = CURRENT_FUNCTION.get_address(str(setattr.val))
    y_addr = CURRENT_FUNCTION.get_address(str(setattr.obj))
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

    x_addr = CURRENT_FUNCTION.get_address(str(plus.result))
    y_addr = CURRENT_FUNCTION.get_address(str(plus.left))
    z_addr = CURRENT_FUNCTION.get_address(str(plus.right))
    instructions = [
        mips.Comment(str(plus))
    ]
    if not is_register(y_addr):
        instructions.append(mips.LwInstruction('$t1', y_addr))
        y_addr = '$t1'
    if not is_register(z_addr):
        instructions.append(mips.LwInstruction('$t2', z_addr))
        z_addr = '$t2'
    if is_register(x_addr):
        instructions.append(mips.AddInstruction(x_addr, y_addr, z_addr))
    else:
        instructions.append(mips.AddInstruction('$t0', y_addr, z_addr))
        instructions.append(mips.SwInstruction('$t0', x_addr))

    return instructions


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
    x_addr = CURRENT_FUNCTION.get_address(str(minus.result))
    y_addr = CURRENT_FUNCTION.get_address(str(minus.left))
    z_addr = CURRENT_FUNCTION.get_address(str(minus.right))
    instructions = [
        mips.Comment(str(minus))
    ]
    if not is_register(y_addr):
        instructions.append(mips.LwInstruction('$t1', y_addr))
        y_addr = '$t1'
    if not is_register(z_addr):
        instructions.append(mips.LwInstruction('$t2', z_addr))
        z_addr = '$t2'
    if is_register(x_addr):
        instructions.append(mips.SubInstruction(x_addr, y_addr, z_addr))
    else:
        instructions.append(mips.SubInstruction('$t0', y_addr, z_addr))
        instructions.append(mips.SwInstruction('$t0', x_addr))

    return instructions


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
    x_addr = CURRENT_FUNCTION.get_address(star.result)
    y_addr = CURRENT_FUNCTION.get_address(star.left)
    z_addr = CURRENT_FUNCTION.get_address(star.right)
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
    x_addr = CURRENT_FUNCTION.get_address(div.result)
    y_addr = CURRENT_FUNCTION.get_address(div.left)
    z_addr = CURRENT_FUNCTION.get_address(div.right)
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

    x_addr = CURRENT_FUNCTION.get_address(lesseq.result)
    y_addr = CURRENT_FUNCTION.get_address(lesseq.left)
    z_addr = CURRENT_FUNCTION.get_address(lesseq.right)
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

    x_addr = CURRENT_FUNCTION.get_address(less.result)
    y_addr = CURRENT_FUNCTION.get_address(less.left)
    z_addr = CURRENT_FUNCTION.get_address(less.right)
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
    x_addr = CURRENT_FUNCTION.get_address(notn.result)
    y_addr = CURRENT_FUNCTION.get_address(notn.value)
    return [
        mips.Comment(str(notn)),
        mips.LwInstruction('$t1', y_addr),
        mips.NotInstruction('$t0', '$t1'),
        mips.SwInstruction('$t0', x_addr)
    ]


def vcal_to_mips_visitor(vcall: cil.VCAllNode):
    """
    CIL:
        result = VCALL [type] [method]
    MIPS:
        1 - Save any of the caller-saved registers ($t0 - $t9) which are used by the
            caller.
        2 - Execute a jal (or jalr) to jump to the function.
        3 - Restore the caller-saved registers.
        4 - If any arguments were passed on the stack (instead of in $a0-$a3), pop
            them off of the stack.
        5 - Extract the return value, if any, from register $v0.
    """
    t = get_type(vcall.type)
    return [
        # 2
        mips.JalInstruction(__VT__[(vcall.type, vcall.method)])
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
    cil.LoadNode: load_to_mips_visitor,
    cil.SubStringNode: substring_to_mips_visitor,
    cil.VCAllNode: vcal_to_mips_visitor
}
