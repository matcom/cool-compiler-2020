from typing import List, Dict
from enum import Enum
from collections import OrderedDict
import re

class SymbolTabEntry:
    def __init__(self, name, is_live=False, next_use=None):
        self.name = name
        self.is_live = is_live
        self.next_use = next_use

class SymbolTable:
    def __init__(self, entries:List[SymbolTabEntry]=None):
        values = entries if entries is not None else []
        self.entries = {v.name: v for v in values}

    def lookup(self, entry_name: str) -> SymbolTabEntry:
        if entry_name != None:
            if entry_name in self.entries.keys():
                return self.entries[entry_name]
           
    def insert(self, entry: SymbolTabEntry):
        self.entries[entry.name] = entry

    def insert_name(self, name):
        self.entries[name] = SymbolTabEntry(name)

    def __getitem__(self, item):
        return self.entries[item]

    def __iter__(self):
        return iter(self.entries)


class NextUseEntry:
	"""For each line : for all three variables involved their next use and is live information"""
	def __init__(self, in1, in2, out, in1nextuse, in2nextuse, outnextuse, in1islive, in2islive, outislive):
		self.in1 = in1
		self.in2 = in2
		self.out = out
		self.in1nextuse = in1nextuse
		self.in2nextuse = in2nextuse
		self.outnextuse = outnextuse
		self.in1islive = in1islive
		self.in2islive = in2islive
		self.outislive = outislive

class AddrType(Enum):
    REF = 1,
    STR = 2,
    BOOL = 3,
    INT = 4

class AddressDescriptor:
    'Stores the location of each variable'
    def __init__(self):
        self.vars = {}

    def insert_var(self, name, address, register=None, stack=None):
        self.vars[name] = [address, register, stack]

    def get_var_addr(self, name):
        return self.vars[name][0]

    def set_var_addr(self, name, addr):
        self.vars[name][0] = addr

    def get_var_reg(self, var):
        return self.vars[var][1]

    def set_var_reg(self, name, reg):
        self.vars[name][1] = reg

    def get_var_stack(self, name):
        return self.vars[name][2]

    def set_var_stack(self, name, stack_pos):
        self.vars[name][1] = stack_pos

    def get_var_storage(self, name):
        return self.vars[name]

class RegisterType(Enum):
    TEMP = 0
    GLOBAL = 1
    ARG = 2
    RETURN = 3

class RegisterDescriptor:
    'Stores the contents of each register'
    def __init__(self):
        registers = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'a0', 'a1', 'a2', 'a3', \
                    's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 'v1']
        self.registers = {reg: None for reg in registers}

    def insert_register(self, register:str, content:str):
        self.registers[register] = content

    def get_content(self, register: str):
        return self.registers[register]

    def find_empty_reg(self):
        for k, v in self.registers.items():
            if v is None:
                return k

    def used_registers(self):
        return [(k, v) for k, v in self.registers.items() if v is not None]

    def empty_registers(self):
        for k in self.registers:
            self.registers[k] = None


class DispatchTable:
    def __init__(self):
        self.classes = OrderedDict()
        self.regex = re.compile(r'function_(.+)_\w+')
        
    def add_class(self, type_name, methods):
        self.classes[type_name] = methods

    def get_offset(self, type_name, method):
        return self.classes[type_name].index(method)

    def find_full_name(self, type_name, mth_name):
        for meth in self.classes[type_name]:
            # format of methods: 'function_{method_name}_{type_name}' 
            name = self.regex.search(meth).groups()[0]
            if name == mth_name:
                return meth
        return None

    def get_methods(self, type_name):
        "Returns all the methods of a specific type"
        return self.classes[type_name]

    def __len__(self):
        return len(self.classes)


class ObjTabEntry:
    def __init__(self, name, methods, attrs):   
        self.class_tag: str = name
        self.size: int = 3 + len(attrs)
        self.dispatch_table_size = len(methods)
        self.dispatch_table_entry = methods
        self.attrs = attrs
    
    @property
    def class_tag_offset(self):
        return 0

    @property
    def size_offset(self):
        return 1

    @property
    def dispatch_ptr_offset(self):
        return 2

    def attr_offset(self, attr):
        return self.attrs.index(attr) + 3

    def method_offset(self, meth):
        "Method offset in dispatch table"
        return self.dispatch_table_entry.index(meth)


class ObjTable:
    def __init__(self, dispatch_table: DispatchTable):
        self.objects: Dict[str, ObjTabEntry] = self.initialize_built_in()
        self.dispatch_table = dispatch_table

    def initialize_built_in(self):
        object_methods = [
            'function_abort_Object', 
            'function_type_name_Object', 
            'function_copy_Object']
        io_methods = [
            'function_out_string_IO',
            'function_out_int_IO',
            'function_in_string_IO',
            'function_in_int_IO']
        str_methods = [
            'function_length_String', 
            'function_concat_String', 
            'function_substr_String' ]
        return {
            'Int': ObjTabEntry('Int', [], []), 
            'Bool': ObjTabEntry('Bool', [], []),
            'IO': ObjTabEntry('IO', io_methods, []),
            'String': ObjTabEntry('String', str_methods, []),
            'Object': ObjTabEntry('Object', object_methods, [])
        }

    def add_entry(self, name, methods, attrs):
        methods = [y for x, y in methods]
        attrs = [x for x, y in attrs]
        self.objects[name] = ObjTabEntry(name, methods, attrs)
        # Adding the methods in the dispatch table
        self.dispatch_table.add_class(name, methods)

    def size_of_entry(self, name):
        return self.objects[name].size

    def __getitem__(self, item) -> ObjTabEntry:
        return self.objects[item]

    def __iter__(self):
        return iter(self.objects.values())