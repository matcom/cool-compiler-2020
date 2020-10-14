from coolcmp.cmp.utils import init_logger
from coolcmp.cmp.gen_cil import GenCIL
from coolcmp.cmp.ast_cls import AttrStringLiteral, New, FunctionCall, Void
from coolcmp.cmp.constants import *

#classes for formatting
class Directive:
    def __init__(self, *args):
        self.args = args

    def __repr__(self): #separate by tabs
        res = '\t' + f'{self.args[0]}'
        
        if len(self.args) > 1:
            res += '\t' + ', '.join(map(str, self.args[1:]))

        return res

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
        self.code = [ Comment('Data Segment') ]
        self.dict_func = cil_code.dict_func
        self.dict_init_func = cil_code.dict_init_func
        self.str_literals = cil_code.str_literals
        self.int_literals = cil_code.int_literals

        self._init_ds()
        self._add_functions()
        self._add_init_functions()
        self._add_str_literals()
        self._add_int_literals()
        self._add_error_msgs()
        self._add_bools()
        self._add_static_literals()
    
    def _fix_str(self, s):
        str_bytes = [ ord(c) for c in s ]
        add = 4 - len(str_bytes) % 4

        while add > 0:
            str_bytes.append(0)
            add -= 1

        assert len(str_bytes) % 4 == 0 and str_bytes[-1] == 0
        return str_bytes

    def _init_ds(self):
        self.code.append(Directive('.data'))

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
            self.code.append(Directive('.word', init.type_obj))
            self.code.append(Directive('.word', self.str_literals[name]))
            self.code.append(Directive('.word', len(init.attrs) + len(init.reserved_attrs)))

    def _add_str_literals(self):
        for lit, label in self.str_literals.items():
            fixed_str = self._fix_str(lit)
            size = len(fixed_str)

            # the -1 is for _string_literal attr
            size += (len(self.dict_init_func['String'].reserved_attrs) - 1) * WORD

            self.code.append(Label(f'{label}:'))
            self.code.append(Directive('.word', 'String'))
            self.code.append(Directive('.word', size))
            self.code.append(Directive('.word', self.int_literals[len(lit)]))
            self.code.append(Directive('.byte', *fixed_str))

    def _add_int_literals(self):
        for lit, label in self.int_literals.items():
            size = len(self.dict_init_func['Int'].reserved_attrs) * WORD

            self.code.append(Label(f'{label}:'))
            self.code.append(Directive('.word', 'Int'))
            self.code.append(Directive('.word', size))
            self.code.append(Directive('.word', lit))

    def _add_error_msgs(self):
        for label, msg in rte_errors.items():
            self.code.append(Label(f'{label}:'))
            self.code.append(Directive('.asciiz', f'"{msg}"'))

    def _add_bools(self):
        size = len(self.dict_init_func['Bool'].reserved_attrs) * WORD

        self.code.append(Label(f'{LABEL_BOOL_TRUE}:'))
        self.code.append(Directive('.word', 'Bool'))
        self.code.append(Directive('.word', size))
        self.code.append(Directive('.word', 1))

        self.code.append(Label(f'{LABEL_BOOL_FALSE}:'))
        self.code.append(Directive('.word', 'Bool'))
        self.code.append(Directive('.word', size))
        self.code.append(Directive('.word', 0))

    def _add_static_literals(self):
        for label, msg in static_literals.items():
            self.code.append(Label(f'{label}:'))
            self.code.append(Directive('.asciiz', f'"{msg}"'))

class GenMIPS:
    def __init__(self, code, cil_code):
        self.logger = init_logger('GenMIPS')

        self.str_literals = cil_code.str_literals
        self.int_literals = cil_code.int_literals

        self.dict_init_func = cil_code.dict_init_func
        self.regs = [ f'$t{i}' for i in range(10) ]  #temporals
        self.loops = 0  #keep counter of loops labels
        self.branches = 0 #keep counter of branches

        self.code = code
        self.code.append(Comment('Text Segment'))
        self.code.append(Directive('.text'))
        
        # entry point
        self._main()

        #utility functions
        self._exit()
        self._print_error_exit()
        self._reserve_memory_label()
        self._runtime_dispatch()
        self._eq_function()

    def sR(self):
        return self.regs[9] #register for self

    def tR(self, i):
        assert 0 <= i < 9
        return self.regs[i]

    def aR(self):  #register used to pass a reference to some object
        return '$a3'

    def rR(self):  #register used to return a reference to some object
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
        self.code.append(Ins('move', self.tR(1), self.tR(0)))
        
        loop_label = f'{LABEL_START_LOOP}{self.loops}'

        #setting up the loop
        #pointer to current address of i-th func is in $t0
        self.code.append(Ins('move', self.tR(0), self.aR()))

        #move 3 steps back (so when it enters the loop it will be fine)
        self.code.append(Ins('subu', self.tR(0), self.tR(0), 3 * WORD))

        self.code.append(Label(f'{loop_label}:'))  #start of the loop

        #update pointer by 3 * WORD (because there are 3 "fields")
        self.code.append(Ins('addu', self.tR(0), self.tR(0), 3 * WORD))

        #load td of function to $t3
        self.code.append(Ins('lw', self.tR(3), f'0({self.tR(0)})'))

        #load tf of function to $t4
        self.code.append(Ins('lw', self.tR(4), f'{WORD}({self.tR(0)})'))

        # now we have the following:
        # $t1 - holds discovery time for the class of dispatch
        # $t3 - holds discovery time of current function
        # $t4 - holds discovery time of current function
        # we need to check that $t3 <= $t1 <= $t4 (this means that class where current function
        # is defined is ancestor of class of my expr)
        # so we check the opposite instead:
        # if $t3 > $t1 or $t1 > $t4 jump to loop_label, else we found it!!

        self.code.append(Ins('bgt', self.tR(3), self.tR(1), loop_label))
        self.code.append(Ins('bgt', self.tR(1), self.tR(4), loop_label))

        self.code.append(Label(f'{LABEL_END_LOOP}{self.loops}:'))
        self.loops += 1

        # load func_label to jump to result_reg
        self.code.append(Ins('lw', self.rR(), f'{2 * WORD}({self.tR(0)})'))

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

    def _print_mips(self):
        # assumes that message was passed at $a0
        self.code.append(Ins('li', '$v0', 4))
        self.code.append(Ins('syscall'))

    def _print_error_exit(self):
        # the error msg was passed at $a0
        self.code.append(Label(f'{LABEL_PRINT_ERROR_EXIT}:'))
        self._print_mips()

        self.code.append(Ins('la', '$a0', LABEL_ENDL))
        self._print_mips()

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
    def native_abort(self, formals):
        self.code.append(Ins('la', '$a0', LABEL_ABORT_STR))
        self._print_mips()

        self.code.append(Ins('la', '$a0', LABEL_SPACE))
        self._print_mips()

        # load address of _type_info attr at $t0
        self.code.append(Ins('lw', self.tR(0), f'0({self.sR()})'))

        # save string object of type at $t0
        self.code.append(Ins('lw', self.tR(0), f'{4 * WORD}({self.tR(0)})'))

        # get id of attribute _string_literal
        idx = self.dict_init_func['String'].attr_dict['_string_literal']

        # save the string adress to $a0
        self.code.append(Ins('la', '$a0', f'{idx * WORD}({self.tR(0)})'))
        self._print_mips()

        self.code.append(Ins('la', '$a0', LABEL_ENDL))
        self._print_mips()

        # exit program with code 0
        self.code.append(Ins('jal', LABEL_EXIT))

    def native_type_name(self, formals):
        # load address of _type_info attr at $t0
        self.code.append(Ins('lw', self.tR(0), f'0({self.sR()})'))

        # save string object of type at result_reg
        self.code.append(Ins('lw', self.rR(), f'{4 * WORD}({self.tR(0)})'))

    def _copy_bool(self):
        # return self (Bool is singleton :) ) 
        self.code.append(Ins('move', self.rR(), self.sR()))

    def _copy_string(self):
        self.code.append(Comment('On String copy'))

        finit = self.dict_init_func['String']

        for attr in finit.reserved_attrs:
            idx = finit.attr_dict[attr.ref.name]

            if isinstance(attr, AttrStringLiteral):
                # size of attrs, not counting StringLiteral
                attrs_sz = (len(finit.reserved_attrs) - 1) * WORD

                # save size at $t2
                self.code.append(Ins('lw', self.tR(2), f'{WORD}({self.sR()})'))

                # with this, we obtain number of bytes (with padding) of the string (the values)
                self.code.append(Ins('sub', self.tR(2), self.tR(2), attrs_sz))

                loop_starts = f'{LABEL_START_LOOP}{self.loops}'
                self.loops += 1

                loop_ends = f'{LABEL_END_LOOP}{self.loops}'
                self.loops += 1

                # iterator over original object
                self.code.append(Ins('la', self.tR(0), f'{idx * WORD}({self.sR()})'))

                # iterator over new object
                self.code.append(Ins('la', self.tR(1), f'{idx * WORD}($v0)'))
                
                self.code.append(Label(f'{loop_starts}:'))

                # consumed all bytes, get out
                self.code.append(Ins('beqz', self.tR(2), loop_ends))
                self.code.append(Ins('sub', self.tR(2), self.tR(2), 1))

                self.code.append(Ins('lb', self.tR(3), f'({self.tR(0)})'))
                self.code.append(Ins('sb', self.tR(3), f'({self.tR(1)})'))

                self.code.append(Ins('addu', self.tR(0), self.tR(0), 1))
                self.code.append(Ins('addu', self.tR(1), self.tR(1), 1))

                self.code.append(Ins('b', loop_starts))

                self.code.append(Label(f'{loop_ends}:'))

            else:
                self.code.append(Ins('lw', self.tR(0), f'{idx * WORD}({self.sR()})'))
                self.code.append(Ins('sw', self.tR(0), f'{idx * WORD}($v0)'))

        self.code.append(Comment('Ended String copy'))

    def native_copy(self, formals):
        not_bool_branch = f'{LABEL_BRANCH}{self.branches}'
        self.branches += 1

        bool_out_branch = f'{LABEL_BRANCH}{self.branches}'
        self.branches += 1

        not_string_branch = f'{LABEL_BRANCH}{self.branches}'
        self.branches += 1

        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        # load address of _type_info attr at $t0
        self.code.append(Ins('lw', self.tR(0), f'0({self.sR()})'))

        # save type_obj (it has position 3) at $t4
        self.code.append(Ins('lw', self.tR(4), f'{3 * WORD}({self.tR(0)})'))
        
        # check if it's not Bool
        self.code.append(Ins('bne', self.tR(4), TYPE_BOOL, not_bool_branch))

        # bool has a different copy semantics (because it's implemented as a singleton)
        self._copy_bool()
        self.code.append(Ins('b', bool_out_branch)) # get out

        self.code.append(Label(f'{not_bool_branch}:'))

        # save number of attrs at $t0
        self.code.append(Ins('lw', self.tR(0), f'{5 * WORD}({self.tR(0)})'))

        # save size of object (in bytes) at $a0, it will be at position 1 (the attr)
        self.code.append(Ins('lw', '$a0', f'{WORD}({self.sR()})'))
        self.code.append(Ins('jal', LABEL_RESERVE_MEMORY))
        
        # check if it's not String
        self.code.append(Ins('bne', self.tR(4), TYPE_STRING, not_string_branch))

        # string has a different copy semantics (well string is complicated :facepalm:)
        # yet it will use $v0 reference to store copy of string!
        self._copy_string()
        self.code.append(Ins('b', loop_ends))  # get out

        self.code.append(Label(f'{not_string_branch}:'))

        # iterator over attrs of self
        self.code.append(Ins('la', self.tR(1), f'({self.sR()})'))

        # interator over attrs of newly created object
        self.code.append(Ins('la', self.tR(2), '($v0)'))

        self.code.append(Label(f'{loop_starts}:'))

        # as $t1 has i-th attr of self and $t2 has i-th attr of $v0 object
        # then load content of $t1 and store it on $t2
        self.code.append(Ins('lw', self.tR(3), f'({self.tR(1)})'))
        self.code.append(Ins('sw', self.tR(3), f'({self.tR(2)})'))

        self.code.append(Ins('addu', self.tR(1), self.tR(1), WORD))
        self.code.append(Ins('addu', self.tR(2), self.tR(2), WORD))
        self.code.append(Ins('sub', self.tR(0), self.tR(0), 1))

        self.code.append(Ins('beqz', self.tR(0), loop_ends))
        self.code.append(Ins('b', loop_starts))

        self.code.append(Label(f'{loop_ends}:'))

        self.code.append(Ins('move', self.rR(), '$v0'))

        # if it was bool then get out, result is saved at result_reg
        self.code.append(Label(f'{bool_out_branch}:'))

    # from String
    def native_length(self, formals):
        # get id of attribute _string_length
        idx = self.dict_init_func['String'].attr_dict['_string_length']
        self.code.append(Ins('lw', self.rR(), f'{idx * WORD}({self.sR()})'))

    def _concat_iterate_str(self):
        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        self.code.append(Label(f'{loop_starts}:'))

        # load byte
        self.code.append(Ins('lb', self.tR(2), f'({self.tR(1)})'))

        # if 0, get out
        self.code.append(Ins('beqz', self.tR(2), loop_ends))

        # save byte
        self._allocate_stack(1)
        self.code.append(Ins('sb', self.tR(2), '0($sp)'))

        # add 1 to total of bytes
        self.code.append(Ins('add', self.tR(0), self.tR(0), 1))

        # move one byte
        self.code.append(Ins('addu', self.tR(1), self.tR(1), 1))
        self.code.append(Ins('b', loop_starts))

        self.code.append(Label(f'{loop_ends}:'))

    def native_concat(self, formals):
        # formal s:String
        idx = formals[0].refers_to[1]

        # reference of String is saved at $t3, negative offset because stack
        self.code.append(Ins('lw', self.tR(3), f'{-idx * WORD}($fp)'))

        # save old $fp
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$fp', '0($sp)'))

        # set frame pointer to first position of string
        self.code.append(Ins('subu', '$fp', '$sp', 1))

        # total of bytes
        self.code.append(Ins('li', self.tR(0), 0))

        # get address of string literal
        idx = self.dict_init_func['String'].attr_dict['_string_literal']
        # idx positive, because it's from heap
        self.code.append(Ins('la', self.tR(1), f'{idx * WORD}({self.sR()})'))

        # iterate and push it to stack
        self.code.append(Comment('Iterating over self string'))
        self._concat_iterate_str()
        self.code.append(Comment('Ended iterating over self string'))

        #####################################################
        # iterating formal now

        # load address of _string_literal of formal
        # idx positive, because it's from heap
        self.code.append(Ins('la', self.tR(1), f'{idx * WORD}({self.tR(3)})'))
        
        self.code.append(Comment('Iterating over formal string'))
        self._concat_iterate_str()
        self.code.append(Comment('Ended iterating over formal string'))

        # adding padding now, this uses $t0 as a register keeping total of bytes
        self._send_string()

        # get old $fp from stack
        self.code.append(Ins('lw', '$fp', '0($sp)'))
        self._deallocate_stack(WORD)

        # result is saved at $result_reg, so I wont save it here

    def native_substr(self, formals):
        # formals: i:Int (index), l:Int (length)

        int_idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # load index
        formal_idx = formals[0].refers_to[1]
        self.code.append(Ins('lw', self.tR(1), f'{-formal_idx * WORD}($fp)'))
        # save index value to $t1
        self.code.append(Ins('lw', self.tR(1), f'{int_idx * WORD}({self.tR(1)})'))

        # load length
        formal_idx = formals[1].refers_to[1]
        self.code.append(Ins('lw', self.tR(2), f'{-formal_idx * WORD}($fp)'))
        # save length value to $t2
        self.code.append(Ins('lw', self.tR(2), f'{int_idx * WORD}({self.tR(2)})'))

        # check if index < 0
        self.code.append(Ins('la', '$a0', LABEL_SUBSTR_NEG_INDEX))
        self.code.append(Ins('bltz', self.tR(1), LABEL_PRINT_ERROR_EXIT))

        # check if length < 0
        self.code.append(Ins('la', '$a0', LABEL_SUBSTR_NEG_LENGTH))
        self.code.append(Ins('bltz', self.tR(2), LABEL_PRINT_ERROR_EXIT))

        # save length of string (no padding) in $t3
        idx = self.dict_init_func['String'].attr_dict['_string_length']
        self.code.append(Ins('lw', self.tR(3), f'{idx * WORD}({self.sR()})'))
        # save value in $t3
        self.code.append(Ins('lw', self.tR(3), f'{int_idx * WORD}({self.tR(3)})'))

        # check if index > $t3
        self.code.append(Ins('la', '$a0', LABEL_SUBSTR_TOO_LONG_INDEX))
        self.code.append(Ins('bgt', self.tR(1), self.tR(3), LABEL_PRINT_ERROR_EXIT))

        # set $t4 to $t1(index) + $t2(length formal)
        self.code.append(Ins('add', self.tR(4), self.tR(1), self.tR(2)))

        # we represent interval as [$t1, $t1 + $t2), $t4 now has $t1 + $t2

        # check if $t4 > $t3 (string_size)
        self.code.append(Ins('la', '$a0', LABEL_SUBSTR_TOO_LONG_LENGTH))
        self.code.append(Ins('bgt', self.tR(4), self.tR(3), LABEL_PRINT_ERROR_EXIT))

        # get address of string literal
        idx = self.dict_init_func['String'].attr_dict['_string_literal']
        # idx positive, because it's from heap
        # now $t3 will have address to beginning of string
        self.code.append(Ins('la', self.tR(3), f'{idx * WORD}({self.sR()})'))

        # add to $t3 the index (this sets $t3 in correct address)
        self.code.append(Ins('addu', self.tR(3), self.tR(3), self.tR(1)))

        # set $t4 to $t3 + length 
        self.code.append(Ins('addu', self.tR(4), self.tR(3), self.tR(2)))

        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        # save old $fp
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$fp', '0($sp)'))

        # set frame pointer to first position of string
        self.code.append(Ins('subu', '$fp', '$sp', 1))

        # total of bytes
        self.code.append(Ins('li', self.tR(0), 0))

        self.code.append(Label(f'{loop_starts}:'))

        # if equal, get out
        self.code.append(Ins('beq', self.tR(3), self.tR(4), loop_ends))
        
        # load byte
        self.code.append(Ins('lb', self.tR(5), f'({self.tR(3)})'))

        # save byte
        self._allocate_stack(1)
        self.code.append(Ins('sb', self.tR(5), '0($sp)'))

        # add 1 to total of bytes
        self.code.append(Ins('add', self.tR(0), self.tR(0), 1))

        # move one byte
        self.code.append(Ins('addu', self.tR(3), self.tR(3), 1))
        self.code.append(Ins('b', loop_starts))

        self.code.append(Label(f'{loop_ends}:'))

        # adding padding now, this uses $t0 as a register keeping total of bytes
        self._send_string()

        # get old $fp from stack
        self.code.append(Ins('lw', '$fp', '0($sp)'))
        self._deallocate_stack(WORD)

        # result is saved at $result_reg, so I wont save it here

    # from IO
    def native_out_string(self, formals):
        # formal x:String
        idx = formals[0].refers_to[1]

        # reference of String is saved at $a0, negative offset because stack
        self.code.append(Ins('lw', '$a0', f'{-idx * WORD}($fp)'))

        # get id of attribute _string_literal
        idx = self.dict_init_func['String'].attr_dict['_string_literal']

        # save the string adress to $a0
        self.code.append(Ins('la', '$a0', f'{idx * WORD}($a0)'))
        self._print_mips()

        # the result of the body of this native function is current self
        self.code.append(Ins('move', self.rR(), self.sR()))
    
    def native_out_int(self, formals):
        # formal x:Int
        idx = formals[0].refers_to[1]

        # reference of Int is saved at $a0, negative offset because stack
        self.code.append(Ins('lw', '$a0', f'{-idx * WORD}($fp)'))

        # get id of attribute _int_literal
        idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # save the int value to $a0
        self.code.append(Ins('lw', '$a0', f'{idx * WORD}($a0)'))

        self.code.append(Ins('li', '$v0', 1))
        self.code.append(Ins('syscall'))

        # the result of the body of this native function is current self
        self.code.append(Ins('move', self.rR(), self.sR()))

    def _send_string(self):
        # send a string to init function
        # it pads the string so that lenght will be mult of 4 and have at least a 0 at the end
        # it assumes that $t0 has total of bytes of the string
        # this also undoes str on stack and its size too

        loop_st_pad = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_nd_pad = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        # compute $t0 % 4
        self.code.append(Ins('and', self.tR(1), self.tR(0), 3))
        self.code.append(Ins('li', self.tR(2), 4))

        # compute 4 - remainder
        self.code.append(Ins('sub', self.tR(1), self.tR(2), self.tR(1)))

        self.code.append(Label(f'{loop_st_pad}:'))

        # if $t1 == 0 get out
        self.code.append(Ins('beqz', self.tR(1), loop_nd_pad))

        # save byte
        self._allocate_stack(1)
        self.code.append(Ins('sb', '$zero', '0($sp)'))

        # add 1 to total bytes
        self.code.append(Ins('add', self.tR(0), self.tR(0), 1))

        # decrease $t1 by 1
        self.code.append(Ins('sub', self.tR(1), self.tR(1), 1))

        self.code.append(Ins('b', loop_st_pad))

        self.code.append(Label(f'{loop_nd_pad}:'))

        # save total of bytes (including padding)
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.tR(0), '0($sp)'))

        # initialize
        self.code.append(Ins('jal', self.dict_init_func['String'].label))

        # load total of bytes
        self.code.append(Ins('lw', self.tR(0), '0($sp)'))
        self._deallocate_stack(WORD)

        # deallocate $t0 bytes (same amount you allocated)
        self.code.append(Ins('addu', '$sp', '$sp', self.tR(0)))

    def native_in_string(self, formals):
        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        # save old $fp
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$fp', '0($sp)'))

        # set frame pointer to first position of string
        self.code.append(Ins('subu', '$fp', '$sp', 1))

        # total of bytes
        self.code.append(Ins('li', self.tR(0), 0))

        self.code.append(Label(f'{loop_starts}:'))

        self.code.append(Ins('li', '$v0', 12))
        self.code.append(Ins('syscall'))

        # if it's '\n' then break
        self.code.append(Ins('beq', '$v0', '0xa', loop_ends))

        # save byte
        self._allocate_stack(1)
        self.code.append(Ins('sb', '$v0', '0($sp)'))

        # add 1
        self.code.append(Ins('add', self.tR(0), self.tR(0), 1))
        self.code.append(Ins('b', loop_starts))

        self.code.append(Label(f'{loop_ends}:'))

        # adding padding now, for this use $t0 as register keeping total of bytes
        self._send_string()

        # get old $fp from stack
        self.code.append(Ins('lw', '$fp', '0($sp)'))
        self._deallocate_stack(WORD)

        # result is saved at $result_reg, so I wont save it here

    def native_in_int(self, formals):
        self.code.append(Ins('li', '$v0', 5))
        self.code.append(Ins('syscall'))
        self.code.append(Ins('move', self.aR(), '$v0'))
        
        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Int'].label))

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
        self.code.append(Ins('sw', self.tR(8), '0($sp)'))

        # save $ra
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$ra', '0($sp)'))

        if node.body:
            self.visit(node.body)

        else:  # native function
            fn = getattr(self, 'native_' + node.name)
            fn(node.formals)

        # #get $ra from stack
        self.code.append(Ins('lw', '$ra', '0($sp)'))
        self._deallocate_stack(WORD)

        # set self, as old saved self
        self.code.append(Ins('lw', self.sR(), '0($sp)'))
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
            self.code.append(Ins('sw', self.rR(), f'0($sp)'))

        self.visit(node.expr)

        # if result == 0, then a dispatch on void ocurred
        # save in $a0 error msg in the case an error occurs
        self.code.append(Ins('la', '$a0', LABEL_DISPATCH_VOID))
        self.code.append(Ins('beqz', self.rR(), LABEL_PRINT_ERROR_EXIT))

        # save old self to later recover within function
        # temp register 8 wont be modified
        self.code.append(Ins('move', self.tR(8), self.sR()))

        #save reference to expr e0
        self.code.append(Ins('move', self.sR(), self.rR()))

        if node.opt_class:  #static dispatch
            # save td from opt_class
            self.code.append(Ins('lw', self.tR(0), f'{node.opt_class}'))

        else:
            #load address of _type_info attr at $t0
            self.code.append(Ins('lw', self.tR(0), f'0({self.sR()})'))

            #save td at $t0
            self.code.append(Ins('lw', self.tR(0), f'0({self.tR(0)})'))

        # either way $t0 has the correct td for the dispatch

        #save at arg_reg the address where functions with name {LABEL_FUNC_PREF}{node.name} are
        self.code.append(Ins('la', self.aR(), f'{LABEL_FUNC_PREF}{node.name}'))

        #transfer control to runtime_dispatch subprogram
        self.code.append(Ins('jal', LABEL_RUNTIME_DISPATCH))

        # in result_reg the label to jump is saved
        # at this point, self_reg should still have node.expr address
        # jump!
        self.code.append(Ins('jalr', self.rR()))

    def native_Bool(self, node):
        self.code.append(Label(f'{node.label}:'))

        # initialize Bool(false) at first
        self.code.append(Ins('la', self.rR(), LABEL_BOOL_FALSE))

        # if arg_reg = 0, then go to LABEL_END_BOOL and finish
        # else initialize Bool(true)
        self.code.append(Ins('beqz', self.aR(), LABEL_BOOL_END))
        self.code.append(Ins('la', self.rR(), LABEL_BOOL_TRUE))

        self.code.append(Label(f'{LABEL_BOOL_END}:'))
        self.code.append(Ins('jr', '$ra'))  #jump back to caller
        # either way, result reg has the address of correct Bool object

    def native_Int(self, node):
        self.code.append(Label(f'{node.label}:'))

        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$ra', '0($sp)'))

        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.sR(), '0($sp)'))

        # Int only has reserved attrs
        self.code.append(Ins('li', '$a0', WORD * len(node.reserved_attrs)))
        self.code.append(Ins('jal', LABEL_RESERVE_MEMORY))

        #saves address of object (ie. self), it is needed in the next visit calls
        self.code.append(Ins('move', self.sR(), '$v0'))

        # to initialize attr size_info
        self.size_info = WORD * len(node.reserved_attrs)

        for attr in node.reserved_attrs:  #visiting reserved_attrs
            self.attr_idx = node.attr_dict[attr.ref.name]
            self.static_data_label = node.name

            self.visit(attr)

        self.code.append(Ins('move', self.rR(), self.sR()))

        self.code.append(Ins('lw', self.sR(), '0($sp)'))
        self._deallocate_stack(WORD)

        self.code.append(Ins('lw', '$ra', '0($sp)'))
        self._deallocate_stack(WORD)

        self.code.append(Ins('jr', '$ra'))

    def visit_AttrIntLiteral(self, node):
        #store int value passed in arg_reg in attr_idx position of attrs
        self.code.append(Ins('sw', self.aR(), f'{self.attr_idx * WORD}({self.sR()})'))

    def native_String(self, node):
        self.code.append(Label(f'{node.label}:'))

        # load size at arg_reg
        self.code.append(Ins('lw', self.tR(6), '0($sp)'))

        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$ra', '0($sp)'))

        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.sR(), '0($sp)'))

        # size of attrs, not counting StringLiteral, since its size is $arg_reg
        attrs_sz = (len(node.reserved_attrs) - 1) * WORD

        # save total of bytes at $t7
        self.code.append(Ins('move', self.tR(7), self.tR(6)))
        self.code.append(Ins('add', self.tR(6), self.tR(6), attrs_sz))

        self.code.append(Ins('move', '$a0', self.tR(6)))
        self.code.append(Ins('jal', LABEL_RESERVE_MEMORY))

        # saves address of object (ie. self), it is needed in the next visit calls
        self.code.append(Ins('move', self.sR(), '$v0'))

        # set to -1 since strings are special :)
        self.size_info = -1

        for attr in node.reserved_attrs:  #visiting reserved_attrs
            self.attr_idx = node.attr_dict[attr.ref.name]
            self.static_data_label = node.name

            self.visit(attr)

        self.code.append(Ins('move', self.rR(), self.sR()))

        self.code.append(Ins('lw', self.sR(), '0($sp)'))
        self._deallocate_stack(WORD)

        self.code.append(Ins('lw', '$ra', '0($sp)'))
        self._deallocate_stack(WORD)

        self.code.append(Ins('jr', '$ra'))

    def visit_AttrStringLength(self, node):
        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        # set $t0
        self.code.append(Ins('move', self.tR(0), '$fp'))
        self.code.append(Ins('li', self.aR(), 0))

        self.code.append(Label(f'{loop_starts}:'))

        # get it from stack
        self.code.append(Ins('lb', self.tR(1), f'({self.tR(0)})'))

        # if 0 get out
        self.code.append(Ins('beqz', self.tR(1), loop_ends))

        # move 1 byte towards top of stack (here we substract because it's stack)
        self.code.append(Ins('subu', self.tR(0), self.tR(0), 1))

        # add one to length
        self.code.append(Ins('add', self.aR(), self.aR(), 1))

        self.code.append(Ins('b', loop_starts))

        self.code.append(Label(f'{loop_ends}:'))

        # create int object with length
        self.code.append(Ins('jal', self.dict_init_func['Int'].label))

        # save string length
        self.code.append(Ins('sw', self.rR(), f'{self.attr_idx * WORD}({self.sR()})'))

    def visit_AttrStringLiteral(self, node):
        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        # setting special attributes
        # $t0 pointer to address of current byte on stack
        # $t1 has current byte
        # $t2 pointer to address of current byte on heap

        # set $t0
        self.code.append(Ins('move', self.tR(0), '$fp'))

        # set $t2
        self.code.append(Ins('la', self.tR(2), f'{self.attr_idx * WORD}({self.sR()})'))

        self.code.append(Label(f'{loop_starts}:'))

        # if consumed all bytes, get out
        self.code.append(Ins('beqz', self.tR(7), loop_ends))

        # substract 1
        self.code.append(Ins('sub', self.tR(7), self.tR(7), 1))

        # get it from stack
        self.code.append(Ins('lb', self.tR(1), f'({self.tR(0)})'))

        # save it on heap
        self.code.append(Ins('sb', self.tR(1), f'({self.tR(2)})'))
        
        # move 1 byte towards top of stack (here we substract because it's stack)
        self.code.append(Ins('subu', self.tR(0), self.tR(0), 1))

        # move 1 byte (here we add because it's heap)
        self.code.append(Ins('addu', self.tR(2), self.tR(2), 1))

        self.code.append(Ins('b', loop_starts))

        self.code.append(Label(f'{loop_ends}:'))

    def visit_FuncInit(self, node):
        if node.type_obj != TYPE_NOT_PRIMITIVE:
            # dispatch to native func init
            fn = getattr(self, 'native_' + node.name)
            fn(node)
            return

        self.code.append(Label(f'{node.label}:'))

        self._allocate_stack(WORD)  #for $ra
        self.code.append(Ins('sw', '$ra', '0($sp)'))  #save $ra at top of stack

        #save self_reg on stack since it gets modified and we need it after
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.sR(), '0($sp)'))

        tot_attrs = len(node.attrs) + len(node.reserved_attrs)  #always > 0

        self.code.append(Ins('li', '$a0', WORD * tot_attrs))  #number is saved in $a0
        self.code.append(Ins('jal', LABEL_RESERVE_MEMORY))  #transfer control to reserve memory func

        #saves address of object (ie. self), it is needed in the next visit calls
        self.code.append(Ins('move', self.sR(), '$v0'))

        # to initialize attr size_info
        self.size_info = WORD * tot_attrs

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
        self.code.append(Ins('move', self.rR(), self.sR()))

        #load old saved self (it was on top of the stack) to self_reg
        self.code.append(Ins('lw', self.sR(), '0($sp)'))
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
        self.code.append(Ins('sw', self.rR(), f'{self.attr_idx * WORD}({self.sR()})'))

    def visit_AttrTypeInfo(self, node):
        #save reference for static data of the type named {self.static_data_label}

        assert self.attr_idx == 0
        self.code.append(Ins('la', self.tR(0), self.static_data_label))
        self.code.append(Ins('sw', self.tR(0), f'{self.attr_idx * WORD}({self.sR()})'))

    def visit_AttrSizeInfo(self, node):
        assert self.attr_idx == 1

        if self.size_info == -1:
            # it's a string :), size is passed at $t6
            self.code.append(Ins('sw', self.tR(6), f'{self.attr_idx * WORD}({self.sR()})'))

        else:
            self.code.append(Ins('li', self.tR(0), self.size_info))
            self.code.append(Ins('sw', self.tR(0), f'{self.attr_idx * WORD}({self.sR()})'))

    def visit_Binding(self, node):
        self.visit(node.expr)

        if node.ref.refers_to[0] == 'attr':  # attrs
            # get attr number {node.refers_to[1]} of self
            self.code.append(Ins('la', self.tR(0), f'{node.ref.refers_to[1] * WORD}({self.sR()})'))

        else:  # locals (including formals)
            # get it from stack (negative offset from $fp)
            self.code.append(Ins('la', self.tR(0), f'{-node.ref.refers_to[1] * WORD}($fp)'))

        # in result reg we have the body (the object) and we saved it at address $t0
        self.code.append(Ins('sw', self.rR(), f'({self.tR(0)})'))
        # also, result_reg has the result of Binding expr
    
    def visit_If(self, node):
        else_branch = f'{LABEL_BRANCH}{self.branches}'
        self.branches += 1

        out_branch = f'{LABEL_BRANCH}{self.branches}'
        self.branches += 1

        self.visit(node.predicate)

        self.code.append(Ins('la', self.tR(0), LABEL_BOOL_FALSE))

        # if predicate (saved at result_reg) is false, go to else branch
        self.code.append(Ins('beq', self.tR(0), self.rR(), else_branch))

        # generate if branch
        self.visit(node.if_branch)

        # get out
        self.code.append(Ins('b', out_branch))

        # else branch
        self.code.append(Label(f'{else_branch}:'))

        # generate else branch
        self.visit(node.else_branch)

        # finished if
        self.code.append(Label(f'{out_branch}:'))
        # result is saved at result_reg, so I dont save it here

    def visit_While(self, node):
        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        # start of loop
        self.code.append(Label(f'{loop_starts}:'))

        self.visit(node.predicate)

        self.code.append(Ins('la', self.tR(0), LABEL_BOOL_FALSE))

        # if predicate (saved at result_reg) is false, go to end of loop
        self.code.append(Ins('beq', self.tR(0), self.rR(), loop_ends))

        self.visit(node.body)

        # repeat
        self.code.append(Ins('b', loop_starts))

        # end loop
        self.code.append(Label(f'{loop_ends}:'))

        # while retuns void, result is saved at result_reg
        self.visit(Void())

    def visit_Block(self, node):
        for expr in node.expr_list:
            self.visit(expr)

        # result is the result of last expr (which is saved at result reg)

    def visit_Let(self, node):
        for binding in node.let_list:
            self.visit(binding)

        self.visit(node.body)
        # result is saved at result_reg

    def visit_Case(self, node):
        self.visit(node.expr)
        
        # if result_reg is 0 then it's a case on a void expr
        self.code.append(Ins('la', '$a0', LABEL_CASE_VOID))
        self.code.append(Ins('beqz', self.rR(), LABEL_PRINT_ERROR_EXIT))

        # load address of _type_info attr at $t0
        self.code.append(Ins('lw', self.tR(0), f'0({self.rR()})'))

        # save td at $t0
        self.code.append(Ins('lw', self.tR(0), f'0({self.tR(0)})'))

        next_label = []

        for _ in node.case_list:
            next_label.append(f'{LABEL_BRANCH}{self.branches}')
            self.branches += 1

        ok_label = []
        for _ in node.case_list:
            ok_label.append(f'{LABEL_BRANCH}{self.branches}')
            self.branches += 1

        get_out_label = f'{LABEL_BRANCH}{self.branches}'
        self.branches += 1

        for i, branch in enumerate(node.case_list):
            self.code.append(Ins('li', self.tR(1), branch.td))
            self.code.append(Ins('li', self.tR(2), branch.tf))

            # now we check that $t1 <= $t0 <= $t2, so we check $t1 > $t0 or $t0 > $t2 instead

            self.code.append(Ins('bgt', self.tR(1), self.tR(0), next_label[i]))
            self.code.append(Ins('bgt', self.tR(0), self.tR(2), next_label[i]))
            self.code.append(Ins('b', ok_label[i]))
            self.code.append(Label(f'{next_label[i]}:'))

        # if code gets to here then it means that there was no valid branch to select
        self.code.append(Ins('la', '$a0', LABEL_CASE_NO_BRANCH))
        self.code.append(Ins('b', LABEL_PRINT_ERROR_EXIT))

        for i, branch in enumerate(node.case_list):
            # set label
            self.code.append(Label(f'{ok_label[i]}:'))

            # type(branch.case_var) == Reference
            # bind reference to expr0
            refers_to = branch.case_var.refers_to
            assert refers_to[0] == 'local'

            # get it from stack (negative offset from $fp)
            self.code.append(Ins('la', self.tR(3), f'{-refers_to[1] * WORD}($fp)'))

            # in result reg we have the body (the object) and we saved it at address $t3
            self.code.append(Ins('sw', self.rR(), f'({self.tR(3)})'))

            self.visit(branch.expr)
            # result is saved at result reg

            # get out!
            self.code.append(Ins('b', get_out_label))

        self.code.append(Label(f'{get_out_label}:'))
        # result was saved at result_reg

    def visit_New(self, node):
        if node.type == 'SELF_TYPE':
            # load address of _type_info attr at $t0
            self.code.append(Ins('lw', self.tR(0), f'0({self.sR()})'))

            # save label_init at $t0
            self.code.append(Ins('lw', self.tR(0), f'{2 * WORD}({self.tR(0)})'))

        else:
            # save address of label to jump at $t0
            self.code.append(Ins('la', self.tR(0), self.dict_init_func[node.type].label))

        if node.type == 'Int':
            # in this case we load address of obj at result_reg and return
            # int initializes with 0
            self.code.append(Ins('la', self.rR(), self.int_literals[0]))
            return

        elif node.type == 'Bool':
            # bool initializes by default with 0
            self.code.append(Ins('li', self.aR(), 0))

        elif node.type == 'String':
            # in this case we load address of obj at result_reg and return
            # string initializes with empty string
            self.code.append(Ins('la', self.rR(), self.str_literals['']))
            return

        # either way $t0 has address of label to jump
        self.code.append(Ins('jalr', self.tR(0))) # jump!
        # in result_reg is the result of New

    def visit_IsVoid(self, node):
        self.visit(node.expr)

        # assume it is true
        self.code.append(Ins('li', self.aR(), 1))
        
        # compare
        self.code.append(Ins('beqz', self.rR(), f'{LABEL_BRANCH}{self.branches}'))

        # if it enters here is false
        self.code.append(Ins('li', self.aR(), 0))

        self.code.append(Label(f'{LABEL_BRANCH}{self.branches}:'))

        # increase number of branches
        self.branches += 1

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Bool'].label))

    def visit_IntComp(self, node):
        self.visit(node.expr)

        # get id of attribute _int_literal
        idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # get the int value and save it at arg_reg
        self.code.append(Ins('lw', self.aR(), f'{idx * WORD}({self.rR()})'))
        self.code.append(Ins('neg', self.aR(), self.aR()))

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Int'].label))

    def visit_Not(self, node):
        self.visit(node.expr)

        # get id of attribute _bool_literal
        idx = self.dict_init_func['Bool'].attr_dict['_bool_literal']

        # get the bool value and save it at arg_reg
        self.code.append(Ins('lw', self.aR(), f'{idx * WORD}({self.rR()})'))
        self.code.append(Ins('xor', self.aR(), self.aR(), 1))

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Bool'].label))

    def _binary_op_load(self, node):
        self.visit(node.left)

        # save result at stack
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', self.rR(), '0($sp)'))

        self.visit(node.right)

        # save left side on $t0
        self.code.append(Ins('lw', self.tR(0), '0($sp)'))
        self._deallocate_stack(WORD)

        # save right side on $t1
        self.code.append(Ins('move', self.tR(1), self.rR()))

    def _binary_op_int(self, node, ops):
        # load LHS to $t0 and RHS to $t1
        self._binary_op_load(node)

        # get id of attribute _int_literal
        idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # get the int value
        self.code.append(Ins('lw', self.tR(0), f'{idx * WORD}({self.tR(0)})'))
        self.code.append(Ins('lw', self.tR(1), f'{idx * WORD}({self.tR(1)})'))

        # do operations
        self.code.extend(ops)

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Int'].label))

    def visit_Plus(self, node):
        # do $arg_reg := $t0 + $t1, to send the value to init function
        op = Ins('add', self.aR(), self.tR(0), self.tR(1))
        self._binary_op_int(node, [op])

    def visit_Minus(self, node):
        # do $arg_reg := $t0 - $t1, to send the value to init function
        op = Ins('sub', self.aR(), self.tR(0), self.tR(1))
        self._binary_op_int(node, [op])

    def visit_Mult(self, node):
        # do $arg_reg := $t0 * $t1, to send the value to init function
        # note that here only lowest 32 bits are saved
        op = Ins('mul', self.aR(), self.tR(0), self.tR(1))
        self._binary_op_int(node, [op])

    def visit_Div(self, node):
        # do $arg_reg := $t0 / $t1, to send the value to init function
        # note that here only lowest 32 bits are saved

        ops = [
            Ins('la', '$a0', LABEL_DIV_BY_0),
            Ins('beqz', self.tR(1), LABEL_PRINT_ERROR_EXIT),
            Ins('div', self.aR(), self.tR(0), self.tR(1))
        ]

        self._binary_op_int(node, ops)

    def _do_binary_comparison(self, ins_to_use):
        # assume it is true
        self.code.append(Ins('li', self.aR(), 1))
        
        # compare
        self.code.append(Ins(ins_to_use, self.tR(0), self.tR(1), f'{LABEL_BRANCH}{self.branches}'))

        # if it enters here is false
        self.code.append(Ins('li', self.aR(), 0))

        self.code.append(Label(f'{LABEL_BRANCH}{self.branches}:'))

        # increase number of branches
        self.branches += 1

    def _binary_op_bool(self, node, ins_to_use):  # used for le and leq
        # load LHS to $t0 and RHS to $t1
        self._binary_op_load(node)

        # get id of attribute _int_literal
        idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # get the int value
        self.code.append(Ins('lw', self.tR(0), f'{idx * WORD}({self.tR(0)})'))
        self.code.append(Ins('lw', self.tR(1), f'{idx * WORD}({self.tR(1)})'))

        self._do_binary_comparison(ins_to_use)

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Bool'].label))

    def visit_Less(self, node):
        # use blt instruction
        self._binary_op_bool(node, 'blt')

    def visit_LessEq(self, node):
        # use ble instruction
        self._binary_op_bool(node, 'ble')

    def _eq_not_primitive(self):
        # code when types are not primitive
        self.code.append(Label(f'{LABEL_EQ_NOT_PRIMITIVE}:'))

        self._do_binary_comparison('beq')
        self.code.append(Ins('b', LABEL_EQ_END))

    def _eq_int(self):
        # code when types are int
        self.code.append(Label(f'{LABEL_EQ_BRANCH_INT}:'))

        # get id of attribute _int_literal
        idx = self.dict_init_func['Int'].attr_dict['_int_literal']

        # get the int value
        self.code.append(Ins('lw', self.tR(0), f'{idx * WORD}({self.tR(0)})'))
        self.code.append(Ins('lw', self.tR(1), f'{idx * WORD}({self.tR(1)})'))

        self._do_binary_comparison('beq')
        self.code.append(Ins('b', LABEL_EQ_END))

    def _eq_bool(self):
        # code when types are bool
        self.code.append(Label(f'{LABEL_EQ_BRANCH_BOOL}:'))

        # as bool are singleton objects, it suffices to compare their addresses

        self._do_binary_comparison('beq')
        self.code.append(Ins('b', LABEL_EQ_END))

    def _eq_string(self):
        self.code.append(Comment('On String equality function'))

        # code when types are string
        self.code.append(Label(f'{LABEL_EQ_BRANCH_STRING}:'))

        # let's load address where both string start
        idx = self.dict_init_func['String'].attr_dict['_string_literal']
        self.code.append(Ins('la', self.tR(2), f'{idx * WORD}({self.tR(0)})'))
        self.code.append(Ins('la', self.tR(3), f'{idx * WORD}({self.tR(1)})'))

        loop_starts = f'{LABEL_START_LOOP}{self.loops}'
        self.loops += 1

        loop_ends = f'{LABEL_END_LOOP}{self.loops}'
        self.loops += 1

        self.code.append(Label(f'{loop_starts}:'))

        # load bytes
        self.code.append(Ins('lb', self.tR(0), f'({self.tR(2)})'))
        self.code.append(Ins('lb', self.tR(1), f'({self.tR(3)})'))

        # if any it's zero, get out
        self.code.append(Ins('beqz', self.tR(0), loop_ends))
        self.code.append(Ins('beqz', self.tR(1), loop_ends))

        # do comparison with $t0 and $t1, result is at $arg_reg
        self._do_binary_comparison('beq')

        # chars are distinct, get out
        self.code.append(Ins('beqz', self.aR(), loop_ends))

        self.code.append(Ins('addu', self.tR(2), self.tR(2), 1))
        self.code.append(Ins('addu', self.tR(3), self.tR(3), 1))

        self.code.append(Ins('b', loop_starts))

        self.code.append(Label(f'{loop_ends}:'))

        # check again, if they are different then 0
        # else they must be both equal to 0, so 1
        self._do_binary_comparison('beq')

        self.code.append(Comment('Ended String equality function'))

    def _eq_function(self):
        self.code.append(Label(f'{LABEL_EQ_FUNCTION}:'))

        # save $ra
        self._allocate_stack(WORD)
        self.code.append(Ins('sw', '$ra', '0($sp)'))
        
        # both objects ($t0 and $t1) will have the same type_obj value (typechecker enforces this)

        # load address of _type_info attr at $t8
        self.code.append(Ins('lw', self.tR(8), f'0({self.tR(0)})'))

        # save type_obj (it has position 3) at $t8
        self.code.append(Ins('lw', self.tR(8), f'{3 * WORD}({self.tR(8)})'))
        
        self.code.append(Ins('beq', self.tR(8), TYPE_NOT_PRIMITIVE, LABEL_EQ_NOT_PRIMITIVE))
        self.code.append(Ins('beq', self.tR(8), TYPE_INT, LABEL_EQ_BRANCH_INT))
        self.code.append(Ins('beq', self.tR(8), TYPE_BOOL, LABEL_EQ_BRANCH_BOOL))
        self.code.append(Ins('beq', self.tR(8), TYPE_STRING, LABEL_EQ_BRANCH_STRING))

        self._eq_not_primitive()
        self._eq_int()
        self._eq_bool()
        self._eq_string()

        # end branch
        self.code.append(Label(f'{LABEL_EQ_END}:'))

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Bool'].label))

        # load $ra
        self.code.append(Ins('lw', '$ra', '0($sp)'))
        self._deallocate_stack(WORD)

        # jump to caller
        self.code.append(Ins('jr', '$ra'))

    def visit_Eq(self, node):
        # load LHS and RHS
        self._binary_op_load(node)

        self.code.append(Ins('jal', LABEL_EQ_FUNCTION))
        # result is saved at result_reg

    def visit_Reference(self, node):
        if node.name == 'self':
            # save self at return register
            self.code.append(Ins('move', self.rR(), self.sR()))

        elif node.refers_to[0] == 'attr':  # attrs
            # get attr number {node.refers_to[1]} of self
            self.code.append(Ins('lw', self.rR(), f'{node.refers_to[1] * WORD}({self.sR()})'))

        else:  # locals (including formals)
            # get it from stack (negative offset from $fp)
            self.code.append(Ins('lw', self.rR(), f'{-node.refers_to[1] * WORD}($fp)'))

    def visit_Int(self, node):
        # return int_literal object
        self.code.append(Ins('la', self.rR(), self.int_literals[int(node.value)]))

    def visit_String(self, node):
        # return string_literal object
        self.code.append(Ins('la', self.rR(), self.str_literals[node.value]))

    def visit_Bool(self, node):
        # send value to initialize and jump to init function

        value = 1 if node.value == 'true' else 0
        self.code.append(Ins('li', self.aR(), value))

        # note that this saves result in result_reg, so I dont save it here
        self.code.append(Ins('jal', self.dict_init_func['Bool'].label))

    def visit_Void(self, node):
        # load address 0 (it doesnt exists) to void
        self.code.append(Ins('li', self.rR(), 0))