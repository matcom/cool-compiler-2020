from coolcmp.cmp.my_ast import ASTNode, Expr

class List(list, ASTNode):  #to save lists and be able to print cil ast
    def __repr__(self):
        return f'<List ({len(self)})>'

class CILCode(ASTNode):
    def __init__(self, functions, init_functions, dict_func, dict_init_func, cases):
        self.functions = functions  #list of functions
        self.init_functions = init_functions
        self.dict_func = dict_func  #dict for functions (ie. regular functions, not init-functions)
        self.dict_init_func = dict_init_func
        self.cases = cases

class Function(ASTNode):
    def __init__(self, name, formals, body, locals_size):
        self.name = name  #str
        self.formals = formals #list of Reference objects
        self.body = body  #expr, None represents a native method
        self.locals_size = locals_size  #how many locals need to be saved

    def __repr__(self):
        return f'<Function {repr(self.name)}>'

class FuncInit(ASTNode):
    def __init__(self, name, attrs, attr_dict, label, reserved_attrs):
        self.name = name
        self.attrs = attrs  #list of attrs in correct order
        self.attr_dict = attr_dict  #dict of (name, position) for attrs including self
        self.label = label
        self.reserved_attrs = reserved_attrs

    def __repr__(self):
        return f'<FuncInit {repr(self.name)}>'

#classes for IntInit and StringInit funcs
class IntInit(FuncInit): pass
class StringInit(FuncInit): pass
class BoolInit(FuncInit): pass

class FunctionCall(ASTNode):
    def __init__(self, expr, opt_class, name, args):
        self.expr = expr
        self.opt_class = opt_class  #a str with name of class or None
        self.name = name  #a string with the name of the function to call
        self.args = args  #list of expressions

class AttrDecl(Expr):  #models the declaration of an attribute
    def __init__(self, ref, type, expr, locals_size):
        self.ref = ref
        self.type = type  #str, declared type of the attr for default initialization
        self.expr = expr
        self.locals_size = locals_size  #how many locals need to be saved for initialization expr

    def __repr__(self):
        return f'<AttrDecl {self.ref}>'

class AttrTypeInfoDecl(AttrDecl): #reserved attribute for type info, used in gen_cil
    def __init__(self):
        AttrDecl.__init__(self, Reference('_type_info'), '_reserved', None, 0)

class AttrIntLiteralDecl(AttrDecl): #reserved attribute for int value
    def __init__(self):
        AttrDecl.__init__(self, Reference('_int_value'), '_reserved', None, 0)

class AttrStringLiteralDecl(AttrDecl): #reserved attribute for string value
    def __init__(self):
        AttrDecl.__init__(self, Reference('_string_value'), '_reserved', None, 0)

class AttrBoolLiteralDecl(AttrDecl): #reserved attribute for bool value
    def __init__(self):
        AttrDecl.__init__(self, Reference('_bool_value'), '_reserved', None, 0)

class Binding(Expr):  #models a binding between a reference and an object address
    def __init__(self, ref, expr):
        self.ref = ref
        self.expr = expr

    def __repr__(self):
        return f'<Binding {self.ref}>'

class Reference(Expr):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Reference {repr(self.name)}>'

class Void(Expr): pass  #represents void expr