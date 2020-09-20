from coolcmp.cmp.my_ast import ASTNode, Expr

class List(list, ASTNode):  #to save lists and be able to print cil ast
    def __repr__(self):
        return f'<List ({len(self)})>'

class CILCode(ASTNode):
    def __init__(self, functions, init_functions):
        self.functions = functions  #list of functions
        self.init_functions = init_functions

class Function(ASTNode):
    def __init__(self, name, formals, body):
        self.name = name  #str
        self.formals = formals #list of Reference objects
        self.body = body  #expr

    def __repr__(self):
        return f'<Function {repr(self.name)}>'

class FuncInit(ASTNode):
    def __init__(self, name, attrs, func_table):
        self.name = name
        self.attrs = attrs  #list of attrs in correct order
        self.func_table = func_table  #ref to FunctionTable object

    def __repr__(self):
        return f'<FuncInit {repr(self.name)}>'

class FunctionCall(ASTNode):
    def __init__(self, expr, opt_class, name, args):
        self.expr = expr
        self.opt_class = opt_class  #a str with name of class or None
        self.name = name  #a string with the name of the function to call
        self.args = args  #list of expressions

class Declaration(Expr):  #models a "declaration" of a reference, that will bind to some object's address
    def __init__(self, ref, expr):
        self.ref = ref
        self.expr = expr

    def __repr__(self):
        return f'<Declaration {self.ref}>'

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