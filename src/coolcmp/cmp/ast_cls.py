from collections import deque
from collections import namedtuple
from collections.abc import Iterable
from coolcmp.cmp.constants import TYPE_NOT_PRIMITIVE

class ASTNode:
    def set_tracker(self, line, col):
        self.line = line
        self.col = col

    def set_static_type(self, t):
        self.static_type = t

    def get_children(self):
        if issubclass(self.__class__, Iterable):
            return list(self)

        attr_list = [ attr for attr in self.__dict__ if isinstance(getattr(self, attr), ASTNode) ]
        name_list = [ getattr(self, attr) for attr in attr_list ]

        return name_list

    def class_name(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'<{self.class_name()}>'

class Formal(ASTNode):
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return f'<Formal {self.id}>'

class NodeContainer(deque, ASTNode):
    def __repr__(self):
        return f'<NodeContainer({len(self)})>'

class Program(ASTNode):
    def __init__(self, cls_list = NodeContainer()):
        self.cls_list = cls_list

class Class(ASTNode):
    def __init__(self, type, opt_inherits=None, feature_list=NodeContainer(), can_inherit=True, reserved_attrs=[], type_obj=TYPE_NOT_PRIMITIVE):
        self.type = type
        self.opt_inherits = opt_inherits  #can be None
        self.feature_list = feature_list
        self.children = []
        self.can_inherit = can_inherit
        self.methods = {}
        self.attrs = {}
        self.reserved_attrs = [AttrTypeInfo(), AttrSizeInfo()] + reserved_attrs  #reserved attributes for the compiler, everyone has type info and size attrs
        self.type_obj = type_obj

        # data for type checker
        self.parent = None
        self.td = 0
        self.tf = 0
        self.level = 0
        self.self_type = None

    def __repr__(self):
        return f'<Class {self.type}>'

class SELF_TYPE(Class):
    def __init__(self):
        Class.__init__(self, Type('SELF_TYPE'))

    def __repr__(self):
        return f'<SELF_TYPE {self.parent.type}>'

class Feature(ASTNode): pass

class Method(Feature):
    def __init__(self, id, formal_list, type, expr=None):
        self.id = id
        self.formal_list = formal_list
        self.type = type
        self.expr = expr  #None for native methods
        self._sign = tuple([ formal.type.value for formal in self.formal_list ] + [self.type.value])

    def get_signature(self):
        return self._sign

    def __repr__(self):
        return f'<Method {self.id}{self.get_signature()}>'

class Attribute(Feature):
    def __init__(self, id, type, opt_expr_init):
        self.id = id
        self.type = type
        self.opt_expr_init = opt_expr_init  #can be None
    
    def __repr__(self):
        return f'<Attribute {self.id}>'

class Expr(ASTNode): pass

class Assignment(Expr):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def __repr__(self):
        return f'<Assignment {self.id}>'

class Dispatch(Expr):
    def __init__(self, expr, opt_type, id, expr_list = NodeContainer()):
        self.expr = expr
        self.opt_type = opt_type  #can be None
        self.id = id
        self.expr_list = expr_list

    def __repr__(self):
        return f'<Dispatch {self.id}>'

class If(Expr):
    def __init__(self, predicate, if_branch, else_branch):
        self.predicate = predicate
        self.if_branch = if_branch
        self.else_branch = else_branch

class While(Expr):
    def __init__(self, predicate, body):
        self.predicate = predicate
        self.body = body

class Block(Expr):
    def __init__(self, expr_list = NodeContainer()):
        self.expr_list = expr_list

    def __repr__(self):
        return f'<Block({len(self.expr_list)})>'

class LetVar(Expr):
    def __init__(self, id, type, opt_expr_init):
        self.id = id
        self.type = type
        self.opt_expr_init = opt_expr_init

    def __repr__(self):
        return f'<LetVar {self.id}>'

class Let(Expr):
    def __init__(self, let_list, body):
        self.let_list = let_list
        self.body = body

class CaseVar(Expr):
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return f'<CaseVar {self.id}>'

class CaseBranch(Expr):
    def __init__(self, case_var, expr):
        self.case_var = case_var
        self.expr = expr

    def set_times(self, td, tf):
        self.td = td
        self.tf = tf

class Case(Expr):
    # Case list is a NodeContainer of CaseBranch

    def __init__(self, expr, case_list = NodeContainer()):
        self.expr = expr
        self.case_list = case_list

class New(Expr):
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f'<New {self.type}>'

class UnaryOp(Expr):
    def __init__(self, expr):
        self.expr = expr

class IsVoid(UnaryOp): pass
class IntComp(UnaryOp): pass
class Not(UnaryOp): pass

class BinaryOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Plus(BinaryOp): pass
class Minus(BinaryOp): pass
class Mult(BinaryOp): pass
class Div(BinaryOp): pass

class Less(BinaryOp): pass
class LessEq(BinaryOp): pass
class Eq(BinaryOp): pass

class Terminal(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.class_name()}: {repr(self.value)}>'

class Type(Terminal): pass
class Id(Terminal): pass
class Int(Terminal): pass
class String(Terminal): pass
class Bool(Terminal): pass

#########################################
#These classes are for gen_cil.py mainly#
#########################################

class List(list, ASTNode):  #to save lists and be able to print cil ast
    def __repr__(self):
        return f'<List ({len(self)})>'

class CILCode(ASTNode):
    def __init__(self, functions, init_functions, dict_func, dict_init_func):
        self.functions = functions  #list of functions
        self.init_functions = init_functions
        self.dict_func = dict_func  #dict for functions (ie. regular functions, not init-functions)
        self.dict_init_func = dict_init_func
        self.str_literals = {}  #literals for string
        self.int_literals = {}  #literals for ints

class Function(ASTNode):
    def __init__(self, name, formals, body, locals_size):
        self.name = name  #str
        self.formals = formals #list of Reference objects
        self.body = body  #expr, None represents a native method
        self.locals_size = locals_size  #how many locals need to be saved

    def __repr__(self):
        return f'<Function {repr(self.name)}>'

class FuncInit(ASTNode):
    def __init__(self, name, attrs, attr_dict, label, reserved_attrs, type_obj):
        self.name = name
        self.attrs = attrs  #list of attrs in correct order
        self.attr_dict = attr_dict  #dict of (name, position) for attrs including reserved attrs
        self.label = label
        self.reserved_attrs = reserved_attrs
        self.type_obj = type_obj

    def __repr__(self):
        return f'<FuncInit {repr(self.name)}>'

class FunctionCall(ASTNode):
    def __init__(self, expr, opt_class, name, args):
        self.expr = expr
        self.opt_class = opt_class  #a str with name of class or None
        self.name = name  #a string with the name of the function to call
        self.args = args  #list of expressions

    def __repr__(self):
        return f'<FunctionCall {repr(self.name)}>'

class AttrDecl(Expr):  #models the declaration of an attribute
    def __init__(self, ref, type, expr, locals_size):
        self.ref = ref
        self.type = type  #str, declared type of the attr for default initialization
        self.expr = expr
        self.locals_size = locals_size  #how many locals need to be saved for initialization expr

    def __repr__(self):
        return f'<AttrDecl {self.ref}>'

class AttrTypeInfo(AttrDecl): #reserved attribute for type info, used in gen_cil
    def __init__(self):
        AttrDecl.__init__(self, Reference('_type_info'), '_reserved', None, 0)

class AttrSizeInfo(AttrDecl):  # number of bytes that object occupies
    def __init__(self):
        AttrDecl.__init__(self, Reference('_size_info'), '_reserved', None, 0)

class AttrIntLiteral(AttrDecl):
    def __init__(self):
        AttrDecl.__init__(self, Reference('_int_literal'), '_reserved', None, 0)

class AttrStringLength(AttrDecl):
    def __init__(self):
        AttrDecl.__init__(self, Reference('_string_length'), '_reserved', None, 0)

class AttrStringLiteral(AttrDecl):
    def __init__(self):
        AttrDecl.__init__(self, Reference('_string_literal'), '_reserved', None, 0)

class AttrBoolLiteral(AttrDecl):
    def __init__(self):
        AttrDecl.__init__(self, Reference('_bool_literal'), '_reserved', None, 0)

class Binding(Expr):  #models a binding between a reference and an object address
    def __init__(self, ref, expr):
        self.ref = ref
        self.expr = expr

    def __repr__(self):
        return f'<Binding>'

class Reference(Expr):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Reference {repr(self.name)}>'

class Void(Expr): pass  #represents void expr