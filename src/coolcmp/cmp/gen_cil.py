from coolcmp.cmp.utils import init_logger
from coolcmp.cmp.ast_cls import *
from coolcmp.cmp.environment import Environment
from collections import defaultdict
from coolcmp.cmp.constants import LABEL_INT_LITERAL, LABEL_STR_LITERAL

class GenCIL:  #in this model Type, Let, LetVar, CaseVar, Class doesnt exists (ie, they are not generated)
    def __init__(self, cls_refs):
        self.logger = init_logger('GenCIL')
        self.cls_refs = cls_refs
        self.attrs = List()  #to hold attributes
        self.cil_code = CILCode(List(), List(), defaultdict(lambda: []), {})
        self.pos = -1
        self.max_idx = -1
        self.cur_env = None  #environment for locals only
        self.cur_cls = None

        # save empty string literal
        self._save_str_literal('')

        # save 0 int literal
        self._save_int_literal(0)

    @staticmethod
    def get_default_value(_type: str):
        expr = Void()

        if _type == 'Bool':
            expr = Bool('false')

        elif _type == 'String':
            expr = String('')
        
        elif _type == 'Int':
            expr = Int('0')

        return expr

    def _save_str_literal(self, value: str):
        if value not in self.cil_code.str_literals:
            label = f'{LABEL_STR_LITERAL}{len(self.cil_code.str_literals)}'
            self.cil_code.str_literals[value] = label

            # save length int literal
            self._save_int_literal(len(value))

    def _save_int_literal(self, value: int):
        if value not in self.cil_code.int_literals:
            label = f'{LABEL_INT_LITERAL}{len(self.cil_code.int_literals)}'
            self.cil_code.int_literals[value] = label

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
        old_attrs = self.attrs
        self.attrs = List(old_attrs[:])

        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        old_cls = self.cur_cls
        self.cur_cls = node

        # let's save each class type as a String object in data segment
        self._save_str_literal(node.type.value)

        #own attrs
        own_attrs = [feature for feature in node.feature_list if isinstance(feature, Attribute)]

        self.attr_dict = {}

        #filling attr_dict, it is needed so that references know what attr they are refering to
        p = 0

        #I ensure that _type_info attr will always be at position 0 in "attr table"
        assert node.reserved_attrs[0].ref.name == '_type_info'

        for attr in node.reserved_attrs:  #reserved attributes
            self.attr_dict[attr.ref.name] = p
            p += 1

        for decl in self.attrs:  #declarations of attributes from inheritance, these are instance of AttrDecl
            self.attr_dict[decl.ref.name] = p
            p += 1

        for attr in own_attrs:  #own attributes, note that these are instance of Attribute right now
            self.attr_dict[attr.id.value] = p
            p += 1

        for feature in node.feature_list:
            self.visit(feature)

        func_init = FuncInit(node.type.value, self.attrs, self.attr_dict, f'{node.type.value}_Init', List(node.reserved_attrs), node.type_obj)
        
        #needed for static data segment of the type
        func_init.td = self.cur_cls.td
        func_init.tf = self.cur_cls.tf

        self.cil_code.init_functions.append(func_init)
        self.cil_code.dict_init_func[func_init.name] = func_init

        self.logger.debug(func_init)
        self.logger.debug(f'Attrs: {list(self.attrs)}')

        for cls in node.children:
            self.visit(cls)

        self.pos -= self.cur_env.definitions  #undo
        self.cur_env = old_env
        self.attrs = old_attrs
        self.cur_cls = old_cls

    def visit_Formal(self, node):
        self.pos += 1  #do
        self.max_idx = max(self.max_idx, self.pos)
        self.cur_env.define(node.id.value, self.pos)

        return self.visit(node.id)

    def visit_Method(self, node):
        old_env = self.cur_env
        self.cur_env = Environment(old_env)

        assert self.pos == -1
        assert self.max_idx == -1

        formals = List([ self.visit(formal) for formal in node.formal_list ])
        body = self.visit(node.expr) if node.expr else None  #if method is not native visit body, else None

        new_func = Function(node.id.value, formals, body, self.max_idx + 1)

        #needed for fast dispatch
        new_func.td = self.cur_cls.td
        new_func.tf = self.cur_cls.tf
        new_func.level = self.cur_cls.level
        new_func.label = f'{self.cur_cls.type.value}.{new_func.name}'

        self.logger.debug(f'{new_func}, td={new_func.td}, tf={new_func.tf}, level={new_func.level}, locals_size={new_func.locals_size}, label={new_func.label}')

        self.cil_code.functions.append(new_func)
        self.cil_code.dict_func[new_func.name].append(new_func)

        self.max_idx = -1
        self.pos -= self.cur_env.definitions  #undo
        self.cur_env = old_env

    def visit_Attribute(self, node):
        assert self.pos == -1
        assert self.max_idx == -1

        ref = self.visit(node.id)
        expr = self._get_declaration_expr(node)

        dec = AttrDecl(ref, node.type.value, expr, self.max_idx + 1)
        self.attrs.append(dec)

        self.max_idx = -1

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
        self.max_idx = max(self.max_idx, self.pos)
        self.cur_env.define(node.id.value, self.pos)

        ref = self.visit(node.id)

        return Binding(ref, expr)

    def visit_Let(self, node):
        old_env = self.cur_env
        self.cur_env = Environment(old_env)
        
        lets = [ self.visit(let_var) for let_var in node.let_list ]
        body = self.visit(node.body)

        self.pos -= self.cur_env.definitions  #undo
        self.cur_env = old_env

        return Let(List(lets), body)

    def visit_CaseVar(self, node):
        self.pos += 1  #do
        self.max_idx = max(self.max_idx, self.pos)
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

        case = Case(expr, branches)

        return case

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

        if ref.name == 'self':  #ignore self for now, it will be always saved in some fixed register at CG
            return ref

        to = self.cur_env.get(ref.name)

        if to is None:  #must be an attr variable
            assert ref.name in self.attr_dict
            ref.refers_to = ('attr', self.attr_dict[ref.name])

        else:
            ref.refers_to = ('local', to)  #local variable (ie. formal, let_var or case_var)

        self.logger.debug(f'{ref} refers to: {ref.refers_to}')

        return ref

    def visit_Int(self, node):
        ref = Int(node.value)
        self._save_int_literal(int(ref.value))
        return ref

    def visit_Bool(self, node):
        return Bool(node.value)

    def visit_String(self, node):
        ref = String(node.value)
        self._save_str_literal(ref.value)
        return ref