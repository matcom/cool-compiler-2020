from coolcmp.cmp.utils import init_logger
from coolcmp.cmp.gen_cil import GenCIL
from coolcmp.cmp.ast_cls import New, FunctionCall, Plus

WORD = 4

LABEL_FUNC_PREF = '_st_'

LABEL_EXIT = '_exit'
LABEL_RESERVE_MEMORY = '_reserve_memory'
LABEL_RUNTIME_DISPATCH = '_runtime_dispatch'
LABEL_PRINT_ERROR_EXIT = '_print_error_exit'
LABEL_MAIN = 'main'
LABEL_START_LOOP = '_loop_'
LABEL_END_LOOP = '_end_loop_'

LABEL_DISPATCH_VOID = '_err_dispatch_void'
LABEL_CASE_VOID = '_err_case_void'
LABEL_CASE_NO_BRANCH = '_err_case_no_branch'
LABEL_DIV_BY_0 = '_err_div_by_0'
LABEL_SUBSTR_RANGE = '_err_substr_range'
LABEL_HEAP_OVERFLOW = '_err_heap_overflow'

rte_errors = {
    LABEL_DISPATCH_VOID: 'Dispatch on void',
    LABEL_CASE_VOID: 'Case on void',
    LABEL_CASE_NO_BRANCH: 'Case without a matching branch',
    LABEL_DIV_BY_0: 'Division by zero',
    LABEL_SUBSTR_RANGE: 'Substring out of range',
    LABEL_HEAP_OVERFLOW: 'Heap overflow'
}

#classes for formatting
class Directive:
    def __init__(self, *args):
        self.args = args

    def __repr__(self): #separate by tabs
        return '\t' + '\t'.join(map(str, self.args))

class Ins:
    def __init__(self, *ins):
        self.ins = ins

    def __repr__(self):
        res = '\t' + f'{self.ins[0]}'

        if len(self.ins) > 1:
            res += ' '
            res += ', '.join(map(str, self.ins[1:]))

        return res

class Label:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return self.label

class Comment:
    def __init__(self, c):
        self.c = c

    def __repr__(self):
        return f'# {self.c}'

class DataSegment:
    def __init__(self, cil_code):
        self.code = ['#Data Segment']
        self.dict_func = cil_code.dict_func
        self.dict_init_func = cil_code.dict_init_func
        self.cases = cil_code.cases
        self.str_literals = cil_code.str_literals
        
        self._init_ds()
        self._add_functions()
        self._add_init_functions()
        self._add_cases()
        self._add_str_literals()
        self._add_error_msgs()

    def _init_ds(self):
        self.code.append(Directive('.data'))
        self.code.append(Directive('.align 2'))

    def _add_functions(self):
        for name, lst in self.dict_func.items():
            self.code.append(f'{LABEL_FUNC_PREF}{name}:')

            for func in lst:
                self.code.append(Directive('.word', func.td))
                self.code.append(Directive('.word', func.tf))
                self.code.append(Directive('.word', func.label))

    def _add_init_functions(self):
        for name, init in self.dict_init_func.items():
            self.code.append(Label(f'{name}:'))
            self.code.append(Directive('.word', init.td))
            self.code.append(Directive('.word', init.tf))
            self.code.append(Directive('.word', init.label))
            self.code.append(Directive('.asciiz', f'"{name}"'))

    def _add_cases(self):
        for case in self.cases:
            self.code.append(Label(f'{case.label}:'))

            for branch in case.case_list:
                self.code.append(Directive('.word', branch.td))
                self.code.append(Directive('.word', branch.tf))

    def fix_string(self, s):  #TODO: Possibly fix this
        res = ''

        assert s[-1] != '\\'

        i = 0
        while i < len(s):
            if s[i] in ['\t', '\b', '\n', '\f']:
                res += s[i]

            elif s[i] == '\\':
                res += s[i + 1]
                i += 1

            else: res += s[i]

            i += 1

        return res

    def _add_str_literals(self):
        #TODO: Implement this!
        # for lit in self.str_literals:
        #     lit.value = self.fix_string(lit.value)

        #     self.code.append(Label(f'{lit.label}:'))
        #     self.code.append(Directive('.asciiz', f"{repr(lit.value)}"))
        pass

    def _add_error_msgs(self):
        for label, msg in rte_errors.items():
            self.code.append(Label(f'{label}:'))
            self.code.append(Directive('.asciiz', f'"{msg}\\n"'))

class GenMIPS:
    def __init__(self, code, cil_code):
        self.logger = init_logger('GenMIPS')

        self.dict_init_func = cil_code.dict_init_func
        self.regs = [ f'$t{i}' for i in range(10) ]  #temporals
        self.loops = 0  #keep counter of loops labels

        self.code = code
        self.code.append('#Text Segment')
        self.code.append(Directive('.text'))
        
        # entry point
        self._main()

        #utility functions
        self._exit()
        self._print_error_exit()
        self._reserve_memory_label()
        self._runtime_dispatch()

    def get_self_reg(self):
        return self.regs[9] #register for self

    def get_temp_reg(self, i):
        assert 0 <= i < 9
        return self.regs[i]

    def get_arg_reg(self):  #register used to pass a reference to some object
        return '$a3'

    def get_result_reg(self):  #register used to return a reference to some object
        return '$v1'

    def visit(self, node):
        self.logger.debug(f'On {node}')
        self.code.append(Comment(f'On {node}'))

        fn = getattr(self, 'visit_' + node.__class__.__name__)
        res = fn(node)

        self.code.append(Comment(f'Ended {node}'))
        self.code.append(Comment('.' * 50))

        return res

    def _exit(self):
        self.code.append(Label(f'{LABEL_EXIT}:'))
        self.code.append(Ins('li', '$v0', 10))
        self.code.append(Ins('syscall'))

    def _reserve_memory_label(self):
        #when called ensure that memory to save is loaded into $a0
        self.code.append(Label(f'{LABEL_RESERVE_MEMORY}:'))
        self.code.append(Ins('li', '$v0', 9))
        self.code.append(Ins('syscall'))  #address is at $v0
        self.code.append(Ins('jr', '$ra'))  # jump back

    def _runtime_dispatch(self):
        #finding at runtime the correct function to dispatch (using discovery and finishing time)
        #NOTE: passed correct td in $t0 and passed func_row_address in arg_reg

        self.code.append(Label(f'{LABEL_RUNTIME_DISPATCH}:'))
        
        # save at $t1 contents of $t0 (which has correct td)
        self.code.append(Ins('move', self.get_temp_reg(1), self.get_temp_reg(0)))
        
        loop_label = f'{LABEL_START_LOOP}{self.loops}'

        #setting up the loop
        #pointer to current address of i-th func is in $t0
        self.code.append(Ins('move', self.get_temp_reg(0), self.get_arg_reg()))

        #move 3 steps back (so when it enters the loop it will be fine)
        self.code.append(Ins('subu', self.get_temp_reg(0), self.get_temp_reg(0), 3 * WORD))

        self.code.append(Label(f'{loop_label}:'))  #start of the loop

        #update pointer by 3 * WORD (because there are 3 "fields")
        self.code.append(Ins('addu', self.get_temp_reg(0), self.get_temp_reg(0), 3 * WORD))

        #load td of function to $t3
        self.code.append(Ins('lw', self.get_temp_reg(3), f'0({self.get_temp_reg(0)})'))

        #load tf of function to $t4
        self.code.append(Ins('lw', self.get_temp_reg(4), f'{WORD}({self.get_temp_reg(0)})'))

        # now we have the following:
        # $t1 - holds discovery time for the class of dispatch
        # $t3 - holds discovery time of current function
        # $t4 - holds discovery time of current function
        # we need to check that $t3 <= $t1 <= $t4 (this means that class where current function
        # is defined is ancestor of class of my expr)
        # so we check the opposite instead:
        # if $t3 > $t1 or $t1 > $t4 jump to loop_label, else we found it!!

        self.code.append(Ins('bgt', self.get_temp_reg(3), self.get_temp_reg(1), loop_label))
        self.code.append(Ins('bgt', self.get_temp_reg(1), self.get_temp_reg(4), loop_label))

        self.code.append(Label(f'{LABEL_END_LOOP}{self.loops}:'))
        self.loops += 1

        # load func_label to jump to result_reg
        self.code.append(Ins('lw', self.get_result_reg(), f'{2 * WORD}({self.get_temp_reg(0)})'))

        self.code.append(Ins('jr', '$ra'))  # jump back

    def _allocate_stack(self, mem):
        if mem > 0:
            self.code.append(Ins('subu', '$sp', '$sp', mem))

    def _deallocate_stack(self, mem):
        if mem > 0:
            self.code.append(Ins('addu', '$sp', '$sp', mem))

    def _main(self):
        self.code.append(Label(f'{LABEL_MAIN}:'))
        self.visit(FunctionCall(New('Main'), None, 'main', []))
        self.code.append(Ins('jal', LABEL_EXIT))

    def _print_error_exit(self):
        # the error msg was passed at $a0
        self.code.append(Label(f'{LABEL_PRINT_ERROR_EXIT}:'))
        self.code.append(Ins('li', '$v0', 4))
        self.code.append(Ins('syscall'))

        # exit program with code 1 (indicating that an error ocurred)
        self.code.append(Ins('li', '$a0', 1))
        self.code.append(Ins('li', '$v0', 17))
        self.code.append(Ins('syscall'))

    def visit_CILCode(self, node):
        for init in node.init_functions:
            self.visit(init)

        for func in node.functions:
            self.visit(func)
    
    # native functions:
    # REMEMBER TO ADD RESULT FOR NATIVE FUNCTIONS TOO

    # from Object
    def native_abort(self): pass
    def native_type_name(self): pass
    def native_copy(self): pass

    # from String
    def native_length(self): pass
    def native_concat(self): pass
    def native_substr(self): pass

    # from IO
    def native_out_string(self): pass
    
    def native_out_int(self):
        # this has one formal and it should be at 0($fp)

        # reference of Int is in $a0
        self.code.append(Ins('lw', '$a0', '0($fp)'))

        # get id of attribute _int_literal
        idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # save the int value to $a0
        self.code.append(Ins('lw', '$a0', f'{idx * WORD}($a0)'))

        self.code.append(Ins('li', '$v0', 1))
        self.code.append(Ins('syscall'))

        # the result of the body of this native function is current self
        self.code.append(Ins('move', self.get_result_reg(), self.get_self_reg()))

    def native_in_string(self): pass
    def native_in_int(self): pass

    def visit_Function(self, node):
        self.code.append(Label(f'{node.label}:'))

        # save space for locals, formals are already in stack
        to_add = node.locals_size - len(node.formals)
        self._allocate_stack(to_add * WORD)

        # save old $fp
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$fp', '0($sp)'))

        # set $fp at the first formal, so 0($fp) will refer to first formal from left to right
        # till now stack looks from bottom to top like:
        # ..., formals, locals, old_$fp
        # the amount of entries saved in this function is node.locals_size + 1 ($fp register)
        # so adding WORD * node.locals_size from $sp sets $fp at first formal as needed
        
        self.code.append(Ins('addu', '$fp', '$sp', WORD * node.locals_size))

        # save previous self, current self is in self_reg
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.get_temp_reg(8), '0($sp)'))

        # save $ra
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$ra', '0($sp)'))

        if node.body:
            self.visit(node.body)

        else:  # native function
            fn = getattr(self, 'native_' + node.name)
            fn()

        # #get $ra from stack
        self.code.append(Ins('lw', '$ra', '0($sp)'))
        self._deallocate_stack(WORD)

        # set self, as old saved self
        self.code.append(Ins('lw', self.get_self_reg(), '0($sp)'))
        self._deallocate_stack(WORD)

        # get $fp from stack
        self.code.append(Ins('lw', '$fp', '0($sp)'))
        self._deallocate_stack(WORD)

        # deallocating all locals (including formals)
        self._deallocate_stack(WORD * node.locals_size)

        self.code.append(Ins('jr', '$ra'))  # jump back

        # in the end, the result is in the result_reg

    def visit_FunctionCall(self, node):
        for arg in node.args:
            self.visit(arg)

            # allocate space for result, this is deallocated inside the function
            self._allocate_stack(WORD)

            # add result to top of stack
            self.code.append(Ins('sw', self.get_result_reg(), f'0($sp)'))

        self.visit(node.expr)

        # if result == 0, then a dispatch on void ocurred
        # save in $a0 error msg in the case an error occurs
        self.code.append(Ins('la', '$a0', LABEL_DISPATCH_VOID))
        self.code.append(Ins('beqz', self.get_result_reg(), LABEL_PRINT_ERROR_EXIT))

        # save old self to later recover within function
        # temp register 8 wont be modified
        self.code.append(Ins('move', self.get_temp_reg(8), self.get_self_reg()))

        #save reference to expr e0
        self.code.append(Ins('move', self.get_self_reg(), self.get_result_reg()))

        if node.opt_class:  #static dispatch
            # save td from opt_class
            self.code.append(Ins('lw', self.get_temp_reg(0), f'{node.opt_class}'))

        else:
            #load address of _type_info attr at $t0
            self.code.append(Ins('lw', self.get_temp_reg(0), f'0({self.get_self_reg()})'))

            #save td at $t0
            self.code.append(Ins('lw', self.get_temp_reg(0), f'0({self.get_temp_reg(0)})'))

        # either way $t0 has the correct td for the dispatch

        #save at arg_reg the address where functions with name {LABEL_FUNC_PREF}{node.name} are
        self.code.append(Ins('la', self.get_arg_reg(), f'{LABEL_FUNC_PREF}{node.name}'))

        #transfer control to runtime_dispatch subprogram
        self.code.append(Ins('jal', LABEL_RUNTIME_DISPATCH))

        # in result_reg the label to jump is saved
        # at this point, self_reg should still have node.expr address
        # jump!
        self.code.append(Ins('jalr', self.get_result_reg()))

    def visit_FuncInit(self, node):
        self.code.append(Label(f'{node.label}:'))

        self._allocate_stack(WORD)  #for $ra
        self.code.append(Ins('sw', '$ra', '0($sp)'))  #save $ra at top of stack

        #save self_reg on stack since it gets modified and we need it after
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.get_self_reg(), '0($sp)'))

        tot_attrs = len(node.attrs) + len(node.reserved_attrs)  #always > 0

        self.code.append(Ins('li', '$a0', WORD * tot_attrs))  #number is saved in $a0
        self.code.append(Ins('jal', LABEL_RESERVE_MEMORY))  #transfer control to reserve memory func

        #saves address of object (ie. self), it is needed in the next visit calls
        self.code.append(Ins('move', self.get_self_reg(), '$v0'))

        for attr in node.reserved_attrs:  #visiting reserved_attrs
            self.attr_idx = node.attr_dict[attr.ref.name]
            self.static_data_label = node.name

            self.visit(attr)

        for decl in node.attrs:  #initialize with default value first
            self.attr_idx = node.attr_dict[decl.ref.name]
            self.default = GenCIL.get_default_value(decl.type)  #use default initialization

            self.visit(decl)

        for decl in node.attrs:
            self.attr_idx = node.attr_dict[decl.ref.name]
            self.default = None  #use expr initialization

            self.visit(decl)

        # result is self (like, the address of newly created object)
        self.code.append(Ins('move', self.get_result_reg(), self.get_self_reg()))

        #load old saved self (it was on top of the stack) to self_reg
        self.code.append(Ins('lw', self.get_self_reg(), '0($sp)'))
        self._deallocate_stack(WORD)

        self.code.append(Ins('lw', '$ra', '0($sp)'))  #get $ra from stack
        self._deallocate_stack(WORD)

        self.code.append(Ins('jr', '$ra'))  #jump back to caller

    def visit_AttrDecl(self, node):
        if self.default:  #default initialization, no additional memory is needed
            self.visit(self.default)
        
        else:
            self._allocate_stack(WORD * node.locals_size)  #for locals

            # save old $fp
            self._allocate_stack(WORD)
            self.code.append(Ins('sw', '$fp', '0($sp)'))

            # set $fp to first local
            self.code.append(Ins('addu', '$fp', '$sp', WORD * node.locals_size))
            
            self.visit(node.expr)

            # get $fp from stack
            self.code.append(Ins('lw', '$fp', '0($sp)'))
            self._deallocate_stack(WORD)

            self._deallocate_stack(WORD * node.locals_size)

        #store result at {self.attr_idx}-th attribute
        self.code.append(Ins('sw', self.get_result_reg(), f'{self.attr_idx * WORD}({self.get_self_reg()})'))

    def visit_AttrTypeInfo(self, node):
        #save reference for static data of the type named {self.static_data_label}

        assert self.attr_idx == 0
        self.code.append(Ins('la', self.get_temp_reg(0), self.static_data_label))
        self.code.append(Ins('sw', self.get_temp_reg(0), f'{self.attr_idx * WORD}({self.get_self_reg()})'))

    def visit_AttrIntLiteral(self, node):
        #store int value passed in arg_reg in attr_idx position of attrs
        self.code.append(Ins('sw', self.get_arg_reg(), f'{self.attr_idx * WORD}({self.get_self_reg()})'))

    def visit_AttrStringLiteral(self, node): pass
    def visit_AttrBoolLiteral(self, node): pass

    def visit_Binding(self, node): pass
    def visit_If(self, node): pass
    def visit_While(self, node): pass

    def visit_Block(self, node):
        for expr in node.expr_list:
            self.visit(expr)

        # result is the result of last expr (which is saved at result reg)

    def visit_Case(self, node): pass

    def visit_New(self, node):
        if node.type == 'SELF_TYPE':
            # load address of _type_info attr at $t0
            self.code.append(Ins('lw', self.get_temp_reg(0), f'0({self.get_self_reg()})'))

            # save label_init at $t0
            self.code.append(Ins('lw', self.get_temp_reg(0), f'{2 * WORD}({self.get_temp_reg(0)})'))

        else:
            # save addres of label to jump at $t0
            self.code.append(Ins('la', self.get_temp_reg(0), self.dict_init_func[node.type].label))

        # fill this, remember that each attribute of these classes expect the value in arg_reg
        if node.type == 'Int':
            # send 0 as value to initialize
            self.code.append(Ins('li', self.get_arg_reg(), 0))

        elif node.type == 'String':
            pass

        elif node.type == 'Bool':
            pass

        # either way $t0 has address of label to jump
        self.code.append(Ins('jalr', self.get_temp_reg(0))) # jump!
        # in result_reg is the result of New

    def visit_IsVoid(self, node): pass
    def visit_IntComp(self, node): pass
    def visit_Not(self, node): pass

    def visit_Plus(self, node):
        self.visit(node.left)

        # save result at stack
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.get_result_reg(), '0($sp)'))

        self.visit(node.right)

        # save left side on $t0
        self.code.append(Ins('lw', self.get_temp_reg(0), '0($sp)'))
        self._deallocate_stack(WORD)

        # save right side on $t1
        self.code.append(Ins('move', self.get_temp_reg(1), self.get_result_reg()))

        # get id of attribute _int_literal
        idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # get the int value
        self.code.append(Ins('lw', self.get_temp_reg(0), f'{idx * WORD}({self.get_temp_reg(0)})'))
        self.code.append(Ins('lw', self.get_temp_reg(1), f'{idx * WORD}({self.get_temp_reg(1)})'))

        # do $arg_reg := $t0 + $t1, to send the value to init function
        self.code.append(Ins('add', self.get_arg_reg(), self.get_temp_reg(0), self.get_temp_reg(1)))

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Int'].label))

    def visit_Minus(self, node): pass
    def visit_Mult(self, node): pass
    def visit_Div(self, node): pass

    def visit_Less(self, node): pass
    def visit_LessEq(self, node): pass
    def visit_Eq(self, node): pass

    def visit_Reference(self, node):
        if node.name == 'self':
            # save self at return register
            self.code.append(Ins('move', self.get_result_reg(), self.get_self_reg()))

        elif node.refers_to[0] == 'attr':  # attrs
            # get attr number {node.refers_to[1]} of self
            self.code.append(Ins('lw', self.get_result_reg(), f'{node.refers_to[1] * WORD}({self.get_self_reg()})'))

        else:  # locals (including formals)
            # get it from stack (negative offset from $fp)
            self.code.append(Ins('lw', self.get_result_reg(), f'{-node.refers_to[1] * WORD}($fp)'))

    def visit_Int(self, node):
        # send in arg_reg the integer, note that literals dont have any attributes
        # and is guaranteed for them that argument_reg will always have found the literal

        # send value to initialize and jump to init function
        self.code.append(Ins('li', self.get_arg_reg(), node.value))

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Int'].label))

    def visit_String(self, node): pass
    def visit_Bool(self, node): pass

    def visit_Void(self, node):
        # load address 0 (it doesnt exists) to void
        self.code.append(Ins('li', self.get_result_reg(), 0))