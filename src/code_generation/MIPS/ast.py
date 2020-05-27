class Node:
    pass

class BinaryNode(Node):
    def __init__(self, des, src1, src2):
        self.des=des
        self.src1=src1
        self.src2=src2

class AdduNode(BinaryNode):
    def __str__(self):
        return f'addu {self.des}, {self.src1}, {self.src2}'
    
    
class MuloNode(BinaryNode):
    def __str__(self):
        return f'mulo {self.des}, {self.src1}, {self.src2}'
    

class DivuNode(BinaryNode):
    def __str__(self):
        return f'divu {self.des}, {self.src1}, {self.src2}'
    
    
class SubuNode(BinaryNode):
    def __str__(self):
        return f'subu {self.des}, {self.src1}, {self.src2}'
    

class SeqNode(BinaryNode):
    def __str__(self):
        return f'seq {self.des}, {self.src1}, {self.src2}'
    

class SneNode(BinaryNode):
    def __str__(self):
        return f'sne {self.des}, {self.src1}, {self.src2}'


class SgeuNode(BinaryNode):
    def __str__(self):
        return f'sgeu {self.des}, {self.src1}, {self.src2}'


class SgtuNode(BinaryNode):
    def __str__(self):
        return f'sgtu {self.des}, {self.src1}, {self.src2}'


class SleuNode(BinaryNode):
    def __str__(self):
        return f'sleu {self.des}, {self.src1}, {self.src2}'


class SltuNode(BinaryNode):
    def __str__(self):
        return f'sltu {self.des}, {self.src1}, {self.src2}'


class BNode(Node):
    def __init__(self, lab):
        self.lab=lab
        
    def __str__(self):
        return f'b {self.lab}'


class BeqzNode(Node):
    def __init__(self,src, lab):
        self.src=src
        self.lab=lab
        
    def __str__(self):
        return f'beqz {self.src}, {self.lab}'

        
class JNode(Node):
    def __init__(self, lab):
        self.lab=lab
        
    def __str__(self):
        return f'j {self.lab}'
        
class JrNode(Node):
    def __init__(self, src):
        self.src=src
    
    def __str__(self):
        return f'jr {self.src}'

class AddressNode(Node):
    pass

class ConstAddrNode(AddressNode):
    def __init__(self, const):
        self.const=const
        
    def __str__(self):
        return self.const
        
class RegAddrNode(AddressNode):
    def __init__(self, reg, const=None):
        self.const=const
        self.reg=reg 
    
    def __str__(self):
        if self.const:
            return f'{self.const}({self.reg})'
        else:
            return f'({self.reg})'
        
class SymbolAddrNode(AddressNode):
    def __init__(self, symbol, const=None, reg=None):
        self.symbol=symbol  
        self.const=const
        self.reg=reg
        
    def __str__(self):
        if self.const and self.reg:
            return f'{self.symbol} + {self.const}({self.reg})'
        if self.const:
            return f'{self.symbol} + {self.const}'
        return self.symbol
        
class LoadAddrNode(Node):
    def __init__(self, des, addr):
        self.des=des
        self.addr=addr

class LaNode(LoadAddrNode):
    def __str__(self):
        return f'la {self.des}, {self.addr}'
    
        
class LbuNode(LoadAddrNode):
    def __str__(self):
        return f'lbu {self.des}, {self.addr}'

class LhuNode(LoadAddrNode):
    def __str__(self):
        return f'lhu {self.des}, {self.addr}'

class LwNode(LoadAddrNode):
    def __str__(self):
        return f'lw {self.des}, {self.addr}'

class Ulhu(LoadAddrNode):
    def __str__(self):
        return f'ulhu {self.des}, {self.addr}'

class Ulw(LoadAddrNode):
    def __str__(self):
        return f'ulw {self.des}, {self.addr}'

class LoadConstNode(Node):
    def __init__(self, des, const):
        self.des=des
        self.const=const
        
class LuiNode(LoadConstNode):
    def __str__(self):
        return f'lui {self.des}, {self.const}'

class LiNode(LoadConstNode):
    def __str__(self):
        return f'li {self.des}, {self.const}'

class Move(Node):
    def __init__(self, src, des):
        self.des=des
        self.src=src
        
    def __str__(self):
        return f'move {self.des}, {self.src}'

class UnaryNode(Node):
    def __init__(self, des, src):
        self.des=des
        self.src=src
        
class NotNode(UnaryNode):
    def __str__(self):
        return f'la {self.des}, {self.src}'

class SyscallNode(Node):
    def __str__(self):
        return 'syscall'


       