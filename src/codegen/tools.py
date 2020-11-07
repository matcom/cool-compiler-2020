from typing import List
from enum import Enum


class Scope(Enum):
	''' Scope of a variable'''
	GLOBAL = 1
	LOCAL = 2


class SymbolTabEntry:
    def __init__(self, name, size=4, data_type="Int", scope=Scope.LOCAL, is_live=False, next_use=None):
        self.is_live = is_live
        self.next_use = next_use
        self.data_type = data_type
        self.scope = scope
        self.size = size
        self.name = name


class SymbolTable:
    def __init__(self, entries:List[SymbolTabEntry]=None):
        values = entries if entries is not None else []
        self.entries = {v.name: v for v in values}

    def lookup(self, entry_name: str) -> SymbolTabEntry:
        if entry_name != None:
            if entry_name in self.entries.keys():
                return self.entries[s]
           
    def insert(self, entry: SymbolTabEntry):
        self.entries[entry.name] = entry

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

    def get_var_reg(self, name):
        return self.vars[name][1]

    def set_var_reg(self, name, reg):
        self.vars[name][1] = reg

    def get_var_stack(self, name):
        return self.vars[name][2]

    def set_var_stack(self, name, stack_pos):
        self.vars[name][1] = stack_pos

    def get_var_storage(self, name):
        return self.vars[name]

class RegisterDescriptor:
    'Stores the contents of each register'
    def __init__(self, registers: List[str]):
        self.registers = {reg: None for reg in registers}

    def insert_register(self, register:str, content:str):
        self.registers[register] = content

    def get_content(self, register: str):
        return self.registers[register]

    def find_empty_reg(self):
        for k, v in self.registers.items():
            if v == None:
                return k
