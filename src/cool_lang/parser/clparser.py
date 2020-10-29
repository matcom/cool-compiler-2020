import ply.yacc as yacc
from ..ast import *
from ..errors import SyntacticError
from ..lexer import COOL_TOKENS
from ..utils import find_column


class COOL_PARSER:
    def __init__(self):
        self.start = 'program'
        self.tokens = COOL_TOKENS
        self.parser = None
        self.code = None
        self.result = None
        self.errors = []

        self.precedence = (
            ('right', 'ASSIGN'),
            ('right', 'NOT'),
            ('nonassoc', 'LESSEQUAL', 'EQUAL', 'LESS'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'STAR', 'DIV'),
            ('right', 'ISVOID'),
            ('right', 'INT_COMPLEMENT'),
            ('left', 'ARROB'),
            ('left', 'DOT'),
        )

    # Parser related methods

    def p_empty(self, p):
        'empty :'
        p[0] = []

    def p_program(self, p):
        'program : class_list'
        p[0] = ProgramNode(p[1], p[1][0].line, p[1][0].column)

    def p_class_list_simple(self, p):
        'class_list : def_class'
        p[0] = [p[1]]

    def p_class_list_multi(self, p):
        'class_list : def_class class_list'
        p[0] = [p[1]] + p[2]

    def p_def_class(self, p):
        'def_class : CLASS TYPE OBRA feature_list CBRA SEMICOLON'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = ClassDeclarationNode(p[2], p[4], None, line, column)

    def p_def_class_heritance(self, p):
        'def_class : CLASS TYPE INHERITS TYPE OBRA feature_list CBRA SEMICOLON'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = ClassDeclarationNode(p[2], p[6], p[4], line, column)

    def p_feature_list(self, p):
        'feature_list : feature feature_list'
        p[0] = [p[1]] + p[2]

    def p_feature_list_empty(self, p):
        'feature_list : empty'
        p[0] = p[1]

    def p_feature_declaration(self, p):
        'feature : ID COLON TYPE SEMICOLON'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = AttrDeclarationNode(p[1], p[3], None, line, column)

    def p_feature_assign(self, p):
        'feature : ID COLON TYPE ASSIGN expr SEMICOLON'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = AttrDeclarationNode(p[1], p[3], p[5], line, column)

    def p_feature_function(self, p):
        'feature : ID OPAR CPAR COLON TYPE OBRA expr CBRA SEMICOLON'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = FuncDeclarationNode(p[1], [], p[5], p[7], line, column)

    def p_feature_function_params(self, p):
        'feature : ID OPAR params_list CPAR COLON TYPE OBRA expr CBRA SEMICOLON'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8], line, column)

    def p_params_list_simple(self, p):
        'params_list : param'
        p[0] = [p[1]]

    def p_params_list_multi(self, p):
        'params_list : param COMMA params_list'
        p[0] = [p[1]] + p[3]

    def p_param(self, p):
        'param : ID COLON TYPE'
        p[0] = ParamDeclarationNode(p[1], p[3])
    
    def p_expr_list_simple(self, p):
        'expr_list : expr SEMICOLON'
        p[0] = [p[1]]

    def p_expr_list_multi(self, p):
        'expr_list : expr SEMICOLON expr_list'
        p[0] = [p[1]] + p[3]

    def p_let_list_declaration_simple(self, p):
        'let_list : ID COLON TYPE'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = [LetNode(p[1], p[3], None, line=line, column=column)]

    def p_let_list_declaration_multi(self, p):
        'let_list : ID COLON TYPE COMMA let_list'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = [LetNode(p[1], p[3], None, line=line, column=column)] + p[5]

    def p_let_list_assign_simple(self, p):
        'let_list : ID COLON TYPE ASSIGN expr'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = [LetNode(p[1], p[3], p[5], line=line, column=column)]

    def p_let_list_assign_multi(self, p):
        'let_list : ID COLON TYPE ASSIGN expr COMMA let_list'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = [LetNode(p[1], p[3], p[5], line=line, column=column)] + p[7]

    def p_case_list_simple(self, p):
        'case_list : ID COLON TYPE ACTION expr SEMICOLON'
        p[0] = [CaseNode(p[1], p[3], p[5])]

    def p_case_list_multi(self, p):
        'case_list : ID COLON TYPE ACTION expr SEMICOLON case_list'
        p[0] = [CaseNode(p[1], p[3], p[5])] + p[7]

    def p_expr(self, p):
        'expr : comp_expr'
        p[0] = p[1]

    def p_comp_expr_le(self, p):
        'comp_expr : comp_expr LESSEQUAL not_arith'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = LessEqualNode(p[1], p[3], line, column)

    def p_comp_expr_e(self, p):
        'comp_expr : comp_expr EQUAL not_arith'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = EqualNode(p[1], p[3], line, column)

    def p_comp_expr_l(self, p):
        'comp_expr : comp_expr LESS not_arith'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = LessNode(p[1], p[3], line, column)

    def p_comp_expr_s(self, p):
        'comp_expr : not_arith'
        p[0] = p[1]

    def p_not_arith_not(self, p):
        'not_arith : NOT comp_expr'
        p[0] = NotNode(p[2])

    def p_not_arith(self, p):
        'not_arith : arith'
        p[0] = p[1]

    def p_arith_plus(self, p):
        'arith : arith PLUS term'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = PlusNode(p[1], p[3], line, column)

    def p_arith_minus(self, p):
        'arith : arith MINUS term'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = MinusNode(p[1], p[3], line, column)

    def p_arith_simple(self, p):
        'arith : term'
        p[0] = p[1]

    def p_term_star(self, p):
        'term : term STAR vfactor'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = StarNode(p[1], p[3], line, column)

    def p_term_div(self, p):
        'term : term DIV vfactor'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = DivNode(p[1], p[3], line, column)

    def p_term_simple(self, p):
        'term : vfactor'
        p[0] = p[1]
    
    def p_vfactor_is(self, p):
        'vfactor : ISVOID factor'
        p[0] = IsVoidNode(p[2])

    def p_vfactor(self, p):
        'vfactor : factor'
        p[0] = p[1]

    def p_factor_int_comp(self, p):
        'factor : INT_COMPLEMENT atom'
        p[0] = ComplementNode(p[2])

    def p_factor_atom(self, p):
        'factor : atom'
        p[0] = p[1]

    def p_atom_if_else(self, p):
        'atom : IF expr THEN expr ELSE expr FI'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = IfThenElseNode(p[2], p[4], p[6], line, column)

    def p_atom_while(self, p):
        'atom : WHILE expr LOOP expr POOL'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = WhileLoopNode(p[2], p[4], line, column)

    def p_atom_multi(self, p):
        'atom : OBRA expr_list CBRA'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = BlockNode(p[2], line, column)

    def p_atom_let_in(self, p):
        'atom : LET let_list IN expr'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = LetInNode(p[2], p[4], line, column)

    def p_atom_case(self, p):
        'atom : CASE expr OF case_list ESAC'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = CaseOfNode(p[2], p[4], line, column)

    def p_atom_assign(self, p):
        'atom : ID ASSIGN expr'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = AssignNode(p[1], p[3], line, column)

    def p_atom_func_call(self, p):
        'atom : atom func_call'
        line = p[1].line
        column = p[1].column
        p[0] = FunctionCallNode(p[1], *p[2], line, column)

    def p_atom_member_call(self, p):
        'atom : member_call'
        p[0] = p[1]

    def p_atom_new(self, p):
        'atom : NEW TYPE'
        line = p.lineno(2)
        column = find_column(self.code, p.lexpos(2))
        p[0] = NewNode(p[2], line, column)

    def p_atom_par(self, p):
        'atom : OPAR expr CPAR'
        p[0] = p[2]

    def p_atom_var(self, p):
        'atom : ID'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = IdNode(p[1], line, column)

    def p_atom_int(self, p):
        'atom : NUMBER'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = IntegerNode(p[1], line, column)

    def p_atom_bool(self, p):
        'atom : BOOL'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = BoolNode(p[1], line, column)

    def p_atom_str(self, p):
        'atom : STRING'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = StringNode(p[1], line, column)

    def p_func_call_simple(self, p):
        'func_call : DOT ID OPAR CPAR'
        p[0] = (p[2], [], None)

    def p_func_call_multi(self, p):
        'func_call : DOT ID OPAR arg_list CPAR'
        p[0] = (p[2], p[4], None)

    def p_func_call_simple_at(self, p):
        'func_call : ARROB TYPE DOT ID OPAR CPAR'
        p[0] = (p[4], [], p[2])

    def p_func_call_multi_at(self, p):
        'func_call : ARROB TYPE DOT ID OPAR arg_list CPAR'
        p[0] = (p[4], p[6], p[2])
    
    def p_arg_list_simple(self, p):
        'arg_list : expr'
        p[0] = [p[1]]

    def p_arg_list_multi(self, p):
        'arg_list : expr COMMA arg_list'
        p[0] = [p[1]] + p[3]

    def p_member_call_simple(self, p):
        'member_call : ID OPAR CPAR'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = MemberCallNode(p[1], [], line, column)

    def p_member_call_multi(self, p):
        'member_call : ID OPAR arg_list CPAR'
        line = p.lineno(1)
        column = find_column(self.code, p.lexpos(1))
        p[0] = MemberCallNode(p[1], p[3], line, column)

    def p_error(self, p):
        line = p.lineno
        column = find_column(self.code, p.lexpos)
        self.errors.append(SyntacticError(line, column, f'Syntactic error!!! in token: {p}'))
        raise SyntaxError(SyntacticError(line, column, f'Syntactic error!!! in token: {p}'))

    # Non parser related methods

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, write_tables=False)

    def parse(self, lexer):
        self.code = lexer.code
        if self.parser is None:
            self.build()
        try:
            result = self.parser.parse(lexer=lexer)
            self.result = result
        except SyntaxError:
            return False
        return True
