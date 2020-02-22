import ply.yacc as yacc
from ..lexer import COOL_TOKENS
from ..errors import SyntacticError

class COOL_PARSER:
    def __init__(self):
        self.start = 'program'
        self.tokens = COOL_TOKENS
        self.parser = None
        self.result = None
        self.errors = []

    # Parser related methods

    def p_empty(self, p):
        'empty :'
        pass

    def p_program(self, p):
        'program : class_list'
        pass

    def p_class_list_simple(self, p):
        'class_list : def_class'
        pass

    def p_class_list_multi(self, p):
        'class_list : def_class class_list'
        pass

    def p_def_class(self, p):
        'def_class : CLASS TYPE OBRA feature_list CBRA SEMICOLON'
        pass

    def p_def_class_heritance(self, p):
        'def_class : CLASS TYPE INHERITS TYPE OBRA feature_list CBRA SEMICOLON'
        pass

    def p_feature_list(self, p):
        'feature_list : feature feature_list'
        pass

    def p_feature_list_empty(self, p):
        'feature_list : empty'
        pass

    def p_feature_declaration(self, p):
        'feature : ID COLON TYPE SEMICOLON'
        pass

    def p_feature_assign(self, p):
        'feature : ID COLON TYPE ASSIGN expr SEMICOLON'
        pass

    def p_feature_function(self, p):
        'feature : ID OPAR CPAR COLON TYPE OBRA expr CBRA SEMICOLON'
        pass

    def p_feature_function_params(self, p):
        'feature : ID OPAR params_list CPAR COLON TYPE OBRA expr CBRA SEMICOLON'
        pass

    def p_params_list_simple(self, p):
        'params_list : param'
        pass

    def p_params_list_multi(self, p):
        'params_list : param COMMA params_list'
        pass

    def p_param(self, p):
        'param : ID COLON TYPE'
        pass
    
    def p_expr_if_else(self, p):
        'expr : IF expr THEN expr ELSE expr FI'
        pass

    def p_expr_while(self, p):
        'expr : WHILE expr LOOP expr POOL'
        pass

    def p_expr_multi(self, p):
        'expr : OBRA expr_list CBRA'
        pass

    def p_expr_let_in(self, p):
        'expr : LET let_list IN expr'
        pass

    def p_expr_case(self, p):
        'expr : CASE expr OF case_list ESAC'
        pass

    def p_expr_assign(self, p):
        'expr : ID ASSIGN expr'
        pass

    def p_expr_truth(self, p):
        'expr : truth_expr'
        pass

    def p_expr_list_simple(self, p):
        'expr_list : expr SEMICOLON'
        pass

    def p_expr_list_multi(self, p):
        'expr : expr SEMICOLON expr_list'
        pass

    def p_let_list_declaration_simple(self, p):
        'let_list : ID COLON TYPE'
        pass

    def p_let_list_declaration_multi(self, p):
        'let_list : ID COLON TYPE COMMA let_list'
        pass

    def p_let_list_assign_simple(self, p):
        'let_list : ID COLON TYPE ASSIGN expr'
        pass

    def p_let_list_assign_multi(self, p):
        'let_list : ID COLON TYPE ASSIGN expr COMMA let_list'
        pass

    def p_case_list_simple(self, p):
        'case_list : ID COLON TYPE ACTION expr SEMICOLON'
        pass

    def p_case_list_multi(self, p):
        'case_list : ID COLON TYPE ACTION expr SEMICOLON case_list'
        pass

    def p_truth_expr_not(self, p):
        'truth_expr : NOT truth_expr'
        pass

    def p_truth_expr_cmp(self, p):
        'truth_expr : comp_expr'
        pass

    def p_comp_expr_le(self, p):
        'comp_expr : comp_expr LESSEQUAL arith'
        pass

    def p_comp_expr_e(self, p):
        'comp_expr : comp_expr EQUAL arith'
        pass

    def p_comp_expr_l(self, p):
        'comp_expr : comp_expr LESS arith'
        pass

    def p_comp_expr_s(self, p):
        'comp_expr : arith'
        pass
    
    def p_arith_plus(self, p):
        'arith : arith PLUS term'
        pass

    def p_arith_minus(self, p):
        'arith : arith MINUS term'
        pass

    def p_arith_simple(self, p):
        'arith : term'
        pass

    def p_term_star(self, p):
        'term : term STAR vfactor'
        pass

    def p_term_div(self, p):
        'term : term DIV vfactor'
        pass

    def p_term_simple(self, p):
        'term : vfactor'
        pass
    
    def p_vfactor_is(self, p):
        'vfactor : ISVOID factor'
        pass

    def p_vfactor(self, p):
        'vfactor : factor'
        pass

    def p_factor_int_comp(self, p):
        'factor : INT_COMPLEMENT atom'
        pass

    def p_factor_atom(self, p):
        'factor : atom'
        pass

    def p_atom_func_call(self, p):
        'atom : atom func_call'
        pass

    def p_atom_member_call(self, p):
        'atom : member_call'
        pass

    def p_atom_new(self, p):
        'atom : NEW TYPE'
        pass

    def p_atom_par(self, p):
        'atom : OPAR expr CPAR'
        pass

    def p_atom_var(self, p):
        'atom : ID'
        pass

    def p_atom_int(self, p):
        'atom : NUMBER'
        pass

    def p_atom_bool(self, p):
        'atom : BOOL'
        pass

    def p_atom_str(self, p):
        'atom : STRING'
        pass

    def p_func_call_simple(self, p):
        'func_call : DOT ID OPAR CPAR'
        pass

    def p_func_call_multi(self, p):
        'func_call : DOT ID OPAR arg_list CPAR'
        pass

    def p_func_call_simple_at(self, p):
        'func_call : ARROB TYPE DOT ID OPAR CPAR'
        pass

    def p_func_call_multi_at(self, p):
        'func_call : ARROB TYPE DOT ID OPAR arg_list CPAR'
        pass
    
    def p_arg_list_simple(self, p):
        'arg_list : expr'
        pass

    def p_arg_list_multi(self, p):
        'arg_list : expr COMMA arg_list'
        pass

    def p_member_call_simple(self, p):
        'member_call : ID OPAR CPAR'
        pass

    def p_member_call_multi(self, p):
        'member_call : ID OPAR arg_list CPAR'
        pass

    # Non parser related methods

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self)

    def parse(self, tokens):
        if self.parser is None:
            self.build()
        try:
            result = self.parser.parse(tokens)
        except Exception as e:
            print(f"The result is {result}.")
            print(e)
            return False
        return True

