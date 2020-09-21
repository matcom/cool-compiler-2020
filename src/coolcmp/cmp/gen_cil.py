from coolcmp.cmp.utils import init_logger
from coolcmp.cmp.cil_ast import *
from coolcmp.cmp.my_ast import *
from coolcmp.cmp.environment import Environment

class GenCIL:  #in this model Type, Let, LetVar, CaseVar, Class doesnt exists (ie, they are not generated)
    def __init__(self, cls_refs):
        self.logger = init_logger('GenCIL')
        self.cur_table = List()
        self.cls_refs = cls_refs
        self.attrs = List()
        self.cil_code = CILCode(List(), List())
        self.pos = -1
        self.cur_env = None  #environment for locals only

    @staticmethod
    def get_default_value(_type: str):
        expr = Void()

        if _type == 'Bool':
            expr = Bool('false')

        elif _type == 'String':
            expr = String('""')
        
        elif _type == 'Int':
            expr = Int('0')

        return expr

    def _get_declaration_expr(self, node):
        expr = GenCIL.get_default_value(node.type.value)

        if node.opt_expr_init:
            expr = self.visit(node.opt_expr_init)

        return expr

    def visit(self, node):
        if isinstance(node, Class):
            self.logger.debug('.' * 200)

        self.logger.debug(f'On {node}')

        fn = getattr(self, 'visit_' + node.__class__.__name__)
        res = fn(node)

        if isinstance(node, Class):
            self.logger.debug('.' * 200)

        return res

    def visit_Class(self, node):
        old_table = self.cur_table
        self.cur_table = List(old_table[:])

        old_attrs = self.attrs
        self.attrs = List(old_attrs[:])

        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        self.attr_dict = {}
        self.attr_dict['self'] = 0  #self is attr number 0

        p = 1
        for decl in self.attrs:  #declarations of attributes from inheritance
            self.attr_dict[decl.ref.name] = p
            p += 1

        for name, _ in node.attrs.items():  #own attributes
            self.attr_dict[name] = p
            p += 1

        for feature in node.feature_list:
            self.visit(feature)

        func_init = FuncInit(node.type.value, self.attrs, self.attr_dict, self.cur_table)
        self.cil_code.init_functions.append(func_init)

        self.logger.debug(func_init)
        self.logger.debug(f'FunctionTable: {self.cur_table}')
        self.logger.debug(f'Attrs: {self.attrs}')

        for cls in node.children:
            self.visit(cls)

        self.pos -= self.cur_env.definitions  #undo
        self.cur_env = old_env

        self.cur_table = old_table
        self.attrs = old_attrs

    def visit_Formal(self, node):
        self.pos += 1  #do
        self.cur_env.define(node.id.value, self.pos)

        return self.visit(node.id)

    def visit_Method(self, node):
        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        assert self.pos == -1

        formals = List([ self.visit(formal) for formal in node.formal_list ])
        body = self.visit(node.expr) if node.expr else None  #if method is not native visit body, else None

        new_func = Function(node.id.value, formals, body)

        self.cil_code.functions.append(new_func)

        for i, func in enumerate(self.cur_table):
            if func.name == node.id.value:  #can happen at most once
                self.cur_table[i] = new_func
                break

        else:
            self.cur_table.append(new_func)

        self.pos -= self.cur_env.definitions  #undo
        self.cur_env = old_env

    def visit_Attribute(self, node):
        dec = AttrDecl(self.visit(node.id), node.type.value, self._get_declaration_expr(node))
        self.attrs.append(dec)

    def visit_Dispatch(self, node):
        expr = self.visit(node.expr)
        opt_class = node.opt_type  #can be none or a str

        if opt_class:
            opt_class = opt_class.value

        name = node.id.value
        args = List([ self.visit(e) for e in node.expr_list ])

        return FunctionCall(expr, opt_class, name, args)

    def visit_SELF_TYPE(self, node): pass

    def visit_Assignment(self, node):
        return Binding(self.visit(node.id), self.visit(node.expr))

    def visit_If(self, node):
        pred, if_branch, else_branch = self.visit(node.predicate), self.visit(node.if_branch), self.visit(node.else_branch)
        return If(pred, if_branch, else_branch)

    def visit_While(self, node):
        pred, body = self.visit(node.predicate), self.visit(node.body)
        return While(pred, body)

    def visit_Block(self, node):
        return Block(List([ self.visit(expr) for expr in node.expr_list ]))  #now block has a list arg

    def visit_LetVar(self, node):
        expr = self._get_declaration_expr(node)

        self.pos += 1  #do
        self.cur_env.define(node.id.value, self.pos)

        ref = self.visit(node.id)

        return Binding(ref, expr)

    def visit_Let(self, node):
        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        exprs = [ self.visit(let_var) for let_var in node.let_list ]
        exprs.append(self.visit(node.body))

        self.pos -= self.cur_env.definitions  #undo
        self.cur_env = old_env

        return Block(List(exprs))

    def visit_CaseVar(self, node):
        self.pos += 1  #do
        self.cur_env.define(node.id.value, self.pos)

        cls = self.cls_refs[node.type.value]

        return self.visit(node.id), cls.td, cls.tf, cls.level

    def visit_CaseBranch(self, node):
        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        ref, td, tf, level = self.visit(node.case_var)
        expr = self.visit(node.expr)

        branch = CaseBranch(ref, expr)
        branch.set_times(td, tf)
        branch.level = level

        self.pos -= self.cur_env.definitions  #undo
        self.cur_env = old_env

        return branch

    def visit_Case(self, node):
        expr = self.visit(node.expr)
        branches = List([ self.visit(branch) for branch in node.case_list ])
        branches.sort(key=lambda x: x.level, reverse=True)  #sort by greater level

        return Case(expr, branches)

    def visit_New(self, node):
        return New(node.type.value)  #now attr of new is a string

    def visit_IsVoid(self, node):
        return IsVoid(self.visit(node.expr))

    def visit_IntComp(self, node):
        return IntComp(self.visit(node.expr))

    def visit_Not(self, node):
        return Not(self.visit(node.expr))

    def visit_Plus(self, node):
        return Plus(self.visit(node.left), self.visit(node.right))

    def visit_Minus(self, node):
        return Minus(self.visit(node.left), self.visit(node.right))

    def visit_Mult(self, node):
        return Mult(self.visit(node.left), self.visit(node.right))

    def visit_Div(self, node):
        return Div(self.visit(node.left), self.visit(node.right))

    def visit_Less(self, node):
        return Less(self.visit(node.left), self.visit(node.right))

    def visit_LessEq(self, node):
        return LessEq(self.visit(node.left), self.visit(node.right))

    def visit_Eq(self, node):
        return Eq(self.visit(node.left), self.visit(node.right))

    def visit_Id(self, node):
        ref = Reference(node.value)
        to = self.cur_env.get(ref.name)

        if to is None:  #must be an attr variable
            assert ref.name in self.attr_dict
            ref.refers_to = ('attr', self.attr_dict[ref.name])

        else:
            ref.refers_to = ('local', to)  #local variable (ie. formal, let_var or case_var)

        self.logger.debug(f'{ref} refers to: {ref.refers_to}')

        return ref

    def visit_Int(self, node):
        return Int(node.value)

    def visit_Bool(self, node):
        return Bool(node.value)

    def visit_String(self, node):
        return String(node.value)