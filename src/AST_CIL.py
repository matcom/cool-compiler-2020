class Node:
    pass

class Program(Node):
    def __init__(self):
        self.type_section = []
        self.data_section = {} #data[string] = tag
        self.code_section = []

class Type(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = {}
    def to_string(self):
        return "type {} \n attributes {}\n methods {}\n".format(self.name, self.attributes, self.methods)

class Data(Node):
    def __init__(self, vname, value):
        self.vname = vname
        self.value = value

class Function(Node):
    def __init__(self, fname):
        self.fname = fname
        self.params = []
        self.localvars = []
        self.instructions = []


class Param(Node):
    def __init__(self, vinfo):
        self.vinfo = vinfo
    def to_string(self):
        return "PARAM {}".format(self.vinfo)

class Local(Node):
    def __init__(self, vinfo):
        self.vinfo = vinfo
    def to_string(self):
        return "LOCAL {}".format(self.vinfo)


class Instruction(Node):
    pass

class Assign(Instruction):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source
    def to_string(self):
        return "ASSIGN {} {}\n".format(self.dest, self.source)

class Arithmetic(Instruction):
    pass

class Plus(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} + {}".format(self.dest, self.left, self.right)

class Minus(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} - {}".format(self.dest, self.left, self.right)


class Star(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} * {}".format(self.dest, self.left, self.right)
    

class Div(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} / {}".format(self.dest, self.left, self.right)

class GetAttrib(Instruction):
    def __init__(self, dest, instance, attribute):
        self.dest = dest
        self.instance = instance
        self.attribute = attribute
    def to_string(self):
        return "{} = GETATTR {} {}".format(self.dest, self.instance, self.attribute)

class SetAttrib(Instruction):
    def __init__(self, instance, attribute, src):
        self.instance = instance
        self.attribute = attribute
        self.src = src
    def to_string(self):
        return "SETATTR {} {} {}".format(self.instance, self.attribute, self.src)


class Allocate(Instruction):
    def __init__(self, dest, ttype):
        self.dest = dest
        self.ttype = ttype

    def to_string(self):
        return "{} = ALLOCATE {}".format(self.dest, self.ttype)


class Array(Instruction):
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src

class TypeOf(Instruction):
    def __init__(self, dest, var):
        self.dest = dest
        self.var = var
    def to_string(self):
        return "{} = TYPEOF {}".format(self.dest, self.var)


class Label(Instruction):
    def __init__(self, name):
        self.name = name
    
    def to_string(self):
        return "LABEL {}".format(self.name)


class Goto(Instruction):
    def __init__(self, name):
        self.name = name    
    
    def to_string(self):
        return "GOTO {}".format(self.name)

class GotoIf(Instruction):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label
    def to_string(self):
        return "IF {} GOTO {}".format(self.condition, self.label)


class Call(Instruction):
    def __init__(self, dest, func):
        self.dest = dest
        self.func = func

    def to_string(self):
        return "{} = CALL {}".format(self.dest, self.func)


class VCall(Instruction):
    def __init__(self, dest, ttype, func):
        self.dest = dest
        self.ttype = ttype
        self.func = func
    def to_string(self):
        return "{} = VCALL {} {}".format(self.dest, self.ttype, self.func)


class Arg(Instruction):
    def __init__(self, vinfo):
        self.vinfo = vinfo
    def to_string(self):
        return "ARG {}".format(self.vinfo)


class Return(Instruction):
    def __init__(self, value=None):
        self.value = value

    def to_string(self):
        return "RETURN {}".format(self.value)


class Load(Instruction):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg
    def to_string(self):
        return "{} = LOAD {}".format(self.dest, self.msg)


class Length(Instruction):
    def __init__(self, dest, str_addr):
        self.dest = dest
        self.str_addr = str_addr
    def to_string(self):
        return "{} = LENGTH {}".format(self.dest, self.str_addr)

class Concat(Instruction):
    def __init__(self, dest, head, tail):
        self.dest = dest
        self.head = head
        self.tail = tail
    
    def to_string(self):
        return "{} = CONCAT {} {}".format(self.dest, self.head, self.tail)


class Prefix(Instruction):
    def __init__(self, dest, str_addr, pos):
        self.dest = dest
        self.str_addr = str_addr
        self.pos = pos

class Substring(Instruction):
    def __init__(self, dest, str_addr, pos):
        self.dest = dest
        self.str_addr = str_addr
        self.pos = pos

class ToStr(Instruction):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

class Read(Instruction):
    def __init__(self, dest):
        self.dest = dest

class Print(Instruction):
    def __init__(self, str_addr):
        self.str_addr = str_addr

class IsVoid(Instruction):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj

class LowerThan(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr

class LowerEqualThan(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr

class EqualThan(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr

class EqualStrThanStr(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr