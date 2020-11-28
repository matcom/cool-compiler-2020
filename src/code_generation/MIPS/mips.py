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
    MIPS if z is str:
        lw $a0, shift(z)
        li $v0, 4
        syscall 
    MIPS if z is int:
        lw $a0, 4($sp)
        li $v0, 4
        syscall 
    """

    offset = CURRENT_FUNCTION.offset(p.str)
    code = [mips.Comment(str(p)),
            mips.LwInstruction('$a0', f'{offset}(fp)')]
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
    MIPS:
        lw $v0, shift(x)
    """
    offset = CURRENT_FUNCTION.offset[str(ret.ret_value)]
    return [
        mips.Comment(str(ret)),
        mips.LwInstruction('$v0', f'{offset}($fp)')
    ]


def read_to_mips_visitor(read: cil.ReadNode):
    """
    CIL:
        x = READ ;
    MIPS:

        .data
            x:  .space 1024
        .text
            la   $a0, x
            li   $a1, 1024
            li   $v0, 8
            syscall
            sw   $a0, shift(x)


    """
    offset = CURRENT_FUNCTION.offset(str(read.result))
    __DATA__.append(mips.MIPSDataItem(read.result, mips.SpaceInst(1024)))

    return [
        mips.LaInstruction('$a0', str(read.result)),
        mips.LiInstruction('$a1', 1024),
        mips.LiInstruction('$v0', 8),
        mips.SyscallInstruction(),
        mips.SwInstruction('$a0', f'{offset}($fp)')
    ]


# TODO: Check
def substring_to_mips_visitor(ss: cil.SubStringNode):
    str_offset = CURRENT_FUNCTION.offset[ss.str]
    i_offset = CURRENT_FUNCTION.offset[ss.i]
    len_offset = CURRENT_FUNCTION.offset[ss.len]
    __DATA__.append(mips.MIPSDataItem(
        ss.result.id, mips.SpaceInst(__BUFFSIZE__)))
    save_address(ss.result, ss.result.id)
    return [
        mips.Comment(str(ss)),
        mips.LwInstruction('$t0', f'{str_offset}($fp)'),
        mips.LaInstruction('$t1', ss.result.id),
        mips.LwInstruction('$t4', f'{i_offset}($fp)'),
        mips.LwInstruction('$t2', f'{len_offset}($fp)'),
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


# TODO: Check
def read_int_to_mips_visitor(read: cil.ReadIntNode):
    addr = CURRENT_FUNCTION.get_address(str(read.result))
    code = [
        mips.Comment(str(read)),
        mips.LiInstruction('$v0', 5),
        mips.SyscallInstruction(),
        mips.SwInstruction('$v0', addr)
    ]
    return code


# TODO: Check
def length_to_mips_visitor(length: cil.LengthNode):
    val = CURRENT_FUNCTION[length.str]
    result_val = CURRENT_FUNCTION[str(length.result)]

    code = [
        mips.Comment(str(length)),
        mips.LbInstruction('$t0', val()),
        mips.LiInstruction('$t1', 0),
        mips.MIPSLabel('length_loop'),
        mips.BeqzInstruction('$t0', 'end_length_loop'),
        mips.AdduInstruction('$t0', '$t0', 1),
        mips.AdduInstruction('$t1', '$t1', 1),
        mips.BInstruction('length_loop'),
        mips.MIPSLabel('end_length_loop'),
        mips.SwInstruction('$t1', result_val())
    ]
    return code


# TODO: Check
def concat_to_mips_visitor(concat: cil.ConcatNode):
    __DATA__.append(mips.MIPSDataItem(concat.result.id,
                                      mips.SpaceInst(2 * __BUFFSIZE__)))
    save_address(concat.result, concat.result.id)
    a = CURRENT_FUNCTION[concat.str_a]
    b = CURRENT_FUNCTION[concat.str_b]

    code = [
        mips.Comment(str(concat)),
        mips.LwInstruction('$t0', a()),
        mips.SwInstruction('$t0', concat.result),
        mips.LbInstruction('$t1', concat.result),
        mips.MIPSLabel('length_loop'),
        mips.BeqzInstruction('$t1', 'end_length_loop'),
        mips.AdduInstruction('$t1', '$t1', 1),
        mips.BInstruction('length_loop'),
        mips.MIPSLabel('end_length_loop'),
        mips.LwInstruction('$t2', b()),
        mips.SwInstruction('$t2', '($t1)')
    ]

    return code


def load_to_mips_visitor(load: cil.LoadNode):
    offset = CURRENT_FUNCTION.offset[load.result]
    return [
        mips.Comment(str(load)),
        mips.LaInstruction('$t0', load.addr),
        mips.SwInstruction('$t0', f'{offset}($sp)')
    ]


def arg_to_mips_visitor(arg: cil.ArgNode):
    '''
    Converts an Arg CIL node to a piece of MIPS code:\n
    1) Allocates a 4-bytes space in stack\n
    2) Pushes the arg value in the stack\n
    '''
    addr = CURRENT_FUNCTION[str(arg.val)]
    location = CURRENT_FUNCTION.location[str(arg.val)]
    mips_code = [mips.Comment(str(arg))]
    if CURRENT_FUNCTION.args_count < 4:
        mips_code.append(mips.LwInstruction(
            f'$a{CURRENT_FUNCTION.args_count}', addr()))
    else:
        mips_code += allocate_stack(4) + push_stack(addr(), '($sp)')
        pass
    CURRENT_FUNCTION.args_count += 1
    return [mips.Comment(str(arg))] + allocate_stack(4) + push_stack(addr, '($sp)')


def allocate_to_mips_visitor(allocate: cil.AllocateNode):
    """
    CIL:
        x  = ALLOCATE T
    MIPS:
        li      $a0, [size(T)]
        li      $v0, 9
        syscall
        sw      $v0, [addr(x)]
    """
    size = get_type(allocate.type).size_mips
    address = CURRENT_FUNCTION[str(allocate.result)]
    code = [
        mips.Comment(str(allocate)),
        mips.LiInstruction('$a0', size),
        mips.LiInstruction('$v0', 9),
        mips.SyscallInstruction(),
        mips.SwInstruction('$v0', address())
    ]
    return code


def type_of_to_mips_visitor(typeof: cil.TypeOfNode):
    """
    CIL:
        t  = TYPEOF x
    MIPS:
        lw $t0, [addr(x)]
        sw ($t0), [addr(t)]
    """
    x_addr = CURRENT_FUNCTION[str(typeof.var)]
    t_addr = CURRENT_FUNCTION[str(typeof.result)]
    return [
        mips.Comment(str(typeof)),
        mips.LwInstruction('$t0', x_addr()),
        mips.SwInstruction('$t0', t_addr())
    ]


# def copy_to_mips_visitor(copy: cil.CopyNode):
#     """
#     CIL:
#         x = COPY y
#     MIPS:
#         lw  $t0, [addr(y)]
#         sw  $t0, [addr(x)]
#     """
#     x_addr = CURRENT_FUNCTION.get_address(str(copy.result))
#     y_addr = CURRENT_FUNCTION.get_address(copy.val)
#     return [
#         mips.Comment(str(copy)),
#         mips.LwInstruction('$t0', y_addr),
#         mips.LwInstruction('$t1', '4($t0)'),
#         mips.MoveInstruction('$a0', '$t1'),
#         mips.LiInstruction('$v0', 9),
#         mips.SyscallInstruction(),
#         mips.SwInstruction('$v0', x_addr),
#         mips.LiInstruction('$t2', '0'),
#         mips.MIPSLabel('length_loop'),
#         mips.BeqInstruction('$t1', '$t2', 'end_length_loop'),

#         mips.MoveInstruction('$t3', x_addr),
#         mips.AdduInstruction('$t3', '$t3', '$t2'),
#         mips.MoveInstruction(x_addr, '$t3'),

#         mips.AdduInstruction('$t2', '$t2', 4),
#         mips.BInstruction('length_loop'),
#         mips.MIPSLabel('end_length_loop'),
#     ]


def getattr_to_mips_visitor(getattr: cil.GetAttrNode):
    """
    CIL:
        x = GETATTR y attr
    MIPS:
        lw  $t0, [addr(y)]
        lw  $t1, [attr_shift($t0)]
        sw  $t1, [addr(x)]
    """

    x_addr = CURRENT_FUNCTION[str(getattr.result)]
    y_addr = CURRENT_FUNCTION[str(getattr.obj)]
    attr_shift = (getattr.attr_index + 1) * 4
    return [
        mips.Comment(str(getattr)),
        mips.LwInstruction('$t0', y_addr()),
        mips.LwInstruction('$t1', f'{attr_shift}($t0)'),
        mips.SwInstruction('$t1', x_addr())
    ]


def setattr_to_mips_visitor(setattr: cil.SetAttrNode):
    """
    CIL:
        SETATTR y attr x
    MIPS:
        lw  $t0, [addr(x)]
        lw  $t1, [addr(y)]
        sw  $t0, [attr_shift($t1)]
    """

    x_addr = CURRENT_FUNCTION[str(setattr.val)]
    y_addr = CURRENT_FUNCTION[str(setattr.obj)]
    attr_shift = (setattr.attr_index + 1) * 4
    return [
        mips.Comment(str(setattr)),
        mips.LwInstruction('$t0', x_addr()),
        mips.LwInstruction('$t1', y_addr()),
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

    x_addr = CURRENT_FUNCTION[str(plus.result)]
    y_addr = CURRENT_FUNCTION[str(plus.left)]
    z_addr = CURRENT_FUNCTION[str(plus.right)]
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
        3 - If any arguments were passed on the stack (instead of in $a0-$a3), pop
            them off of the stack.
        4 - Restore the caller-saved registers.
        5 - Extract the return value, if any, from register $v0.
    """
    CURRENT_FUNCTION.args_count = 0
    t = get_type(vcall.type)
    instructios = []
    instructios.append(mips.Comment(str(vcall)))
    # 1
    size = len(CURRENT_FUNCTION.caller_saved_reg) * 4
    instructios.extend(allocate_stack(size))
    s = size
    for reg in CURRENT_FUNCTION.caller_saved_reg:
        s -= 4
        instructios.extend(push_stack(f'${reg}', f'{s}($sp)'))
    # 2
    instructios.append(mips.JalInstruction(__VT__[(vcall.type, vcall.method)]))
    # 4
    s = size
    for reg in CURRENT_FUNCTION.caller_saved_reg:
        s -= 4
        instructios.extend(peek_stack(f'${reg}', f'{s}($sp)'))
    instructios.extend(free_stack(size))
    return instructios


def assign_to_mips_visitor(assign: cil.AssignNode):
    """
    CIL:
        x = y
    MIPS:
        lw $t0, [y_addr]
        sw $t0, [x_addr]
    """
    y_addr = CURRENT_FUNCTION.get_address(assign.val.id)
    x_addr = CURRENT_FUNCTION.get_address(assign.result.id)

    return [
        mips.Comment(str(assign)),
        mips.LwInstruction('$t0', y_addr),
        mips.SwInstruction('$t0', x_addr)
    ]


__visitors__ = {
    cil.ArgNode: arg_to_mips_visitor,
    cil.AllocateNode: allocate_to_mips_visitor,
    # cil.CopyNode: copy_to_mips_visitor,
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
    cil.VCAllNode: vcal_to_mips_visitor,
    cil.AssignNode: assign_to_mips_visitor,
    cil.TypeOfNode: type_of_to_mips_visitor
}
