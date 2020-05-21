import ply.yacc as yacc
from .lexer import Cool_Lexer
from .ast import *
import sys

class Parser:
    def p_program_1(self, p):
        "program : class SEMICOLON program"

        p[3].class_list.appendleft(p[1])
        p[0] = p[3]

    def p_program_2(self, p):
        "program : class SEMICOLON"

        p[0] = Program(Deque([p[1]]))

    def p_class(self, p):
        "class : CLASS TYPE inherits LBRACE feature_list RBRACE"

        p[0] = Class(p[2], p[3], p[5])

    def p_inherits(self, p):
        """
        inherits : INHERITS TYPE
        |	 epsilon
        """

        p[0] = (p[2] if len(p) == 3 else None)

    def p_feature_list(self, p):
        """
        feature_list : feature SEMICOLON feature_list
        |	 epsilon
        """

        if len(p) == 4:
            p[3].appendleft(p[1])
            p[0] = p[3]

        else: p[0] = Deque()

    def p_feature(self, p):
        """
        feature : ID LPAREN formal_params RPAREN COLON TYPE LBRACE expr RBRACE
        |	 attribute
        """

        if len(p) == 10:
            p[0] = Method(p[1], p[3], p[6], p[8])

        else: p[0] = p[1]

    def p_formal_params_1(self, p):
        "formal_params : formal_list"
        
        p[0] = p[1]

    def p_formal_params_2(self, p):
        "formal_params : epsilon"

        p[0] = Deque()

    def p_formal(self, p):
        "formal : ID COLON TYPE"

        p[0] = Formal(p[1], p[3])

    def p_formal_list(self, p):
        "formal_list : formal formal_list_helper"

        p[2].appendleft(p[1])
        p[0] = p[2]

    def p_formal_list_helper(self, p):
        """
        formal_list_helper : COMMA formal formal_list_helper
        |	 epsilon
        """

        if len(p) == 4:
            p[3].appendleft(p[2])
            p[0] = p[3]

        else: p[0] = Deque()

    def p_expr_list_semicolon(self, p):
        """
        expr_list_semicolon : expr SEMICOLON expr_list_semicolon 
        |	 expr SEMICOLON 
        """

        if len(p) == 4:
            p[3].appendleft(p[1])
            p[0] = p[3]

        else: p[0] = Deque([p[1]])

    def p_expr_params_1(self, p):
        "expr_params : expr_list_comma"
        
        p[0] = p[1]

    def p_expr_params_2(self, p):
        "expr_params : epsilon"

        p[0] = Deque()

    def p_expr_list_comma(self, p):
        "expr_list_comma : expr expr_list_comma_helper"

        p[2].appendleft(p[1])
        p[0] = p[2]

    def p_expr_list_comma_helper(self, p):
        """
        expr_list_comma_helper : COMMA expr expr_list_comma_helper
        |	 epsilon
        """

        if len(p) == 4:
            p[3].appendleft(p[2])
            p[0] = p[3]

        else: p[0] = Deque()

    def p_attribute(self, p):
        "attribute : formal opt_expr_init"

        p[0] = Attribute(p[1], p[2])

    def p_attribute_list(self, p):
        "attribute_list : attribute attribute_list_helper"

        p[2].appendleft(p[1])
        p[0] = p[2]

    def p_attribute_list_helper(self, p):
        """
        attribute_list_helper : COMMA attribute attribute_list_helper
        |	 epsilon
        """

        if len(p) == 4:
            p[3].appendleft(p[2])
            p[0] = p[3]

        else: p[0] = Deque()

    def p_opt_expr_init(self, p):
        """
        opt_expr_init : ASSIGN expr
        |	 epsilon
        """

        if len(p) == 3:
            p[0] = p[2]

        else: p[0] = None

    def p_case_list(self, p):
        """
        case_list : formal ARROW expr SEMICOLON case_list
        |	 formal ARROW expr SEMICOLON
        """

        if len(p) == 6:
            p[5].appendleft((p[1], p[3]))
            p[0] = p[5]

        else: p[0] = Deque([(p[1], p[3])])

    def p_expr_assignment(self, p):
        "expr : ID ASSIGN expr"

        p[0] = Assignment(p[1], p[3])

    def p_expr_dispatch_1(self, p):
        "expr : expr CAST TYPE DOT ID LPAREN expr_params RPAREN"

        p[0] = Dispatch(p[1], p[3], p[5], p[7])

    def p_expr_dispatch_2(self, p):
        "expr : expr DOT ID LPAREN expr_params RPAREN"

        p[0] = Dispatch(p[1], None, p[3], p[5])

    def p_expr_self_dispatch(self, p):
        "expr : ID LPAREN expr_params RPAREN"

        p[0] = SelfDispatch(p[1], p[3])

    def p_expr_if(self, p):
        "expr : IF expr THEN expr ELSE expr FI"

        p[0] = If(p[2], p[4], p[6])

    def p_expr_while(self, p):
        "expr : WHILE expr LOOP expr POOL"

        p[0] = While(p[2], p[4])

    def p_expr_block(self, p):
        "expr : LBRACE expr_list_semicolon RBRACE"

        p[0] = Block(p[2])

    #### SHIFT/REDUCE conflict with the let is intended
    def p_expr_let(self, p):
        "expr : LET attribute_list IN expr"

        p[0] = Let(p[2], p[4])

    def p_expr_case(self, p):
        "expr : CASE expr OF case_list ESAC"

        p[0] = Case(p[2], p[4])

    def p_expr_new(self, p):
        "expr : NEW TYPE"

        p[0] = New(p[2])

    def p_expr_unary_isvoid(self, p):
        "expr : ISVOID expr"

        p[0] = IsVoid(p[2])

    def p_expr_unary_intcomp(self, p):
        "expr : INT_COMP expr"

        p[0] = IntComp(p[2])

    def p_expr_unary_not(self, p):
        "expr : NOT expr"

        p[0] = Not(p[2])

    def p_expr_binary_plus(self, p):
        "expr : expr PLUS expr"

        p[0] = Plus(p[1], p[3])

    def p_expr_binary_minus(self, p):
        "expr : expr MINUS expr"

        p[0] = Minus(p[1], p[3])

    def p_expr_binary_mul(self, p):
        "expr : expr MUL expr"

        p[0] = Mult(p[1], p[3])

    def p_expr_binary_div(self, p):
        "expr : expr DIV expr"

        p[0] = Div(p[1], p[3])
    
    def p_expr_binary_less(self, p):
        "expr : expr LESS expr"

        p[0] = Less(p[1], p[3])

    def p_expr_binary_lesseq(self, p):
        "expr : expr LESS_EQ expr"

        p[0] = LessEq(p[1], p[3])

    def p_expr_binary_eq(self, p):
        "expr : expr EQ expr"

        p[0] = Eq(p[1], p[3])

    def p_expr_paren(self, p):
        "expr : LPAREN expr RPAREN"

        p[0] = p[2]

    def p_expr_id(self, p):
        "expr : ID"

        p[0] = p[1]

    def p_expr_int(self, p):
        "expr : INT"

        p[0] = Int(p[1])

    def p_expr_string(self, p):
        "expr : STRING"

        p[0] = String(p[1])

    def p_expr_bool(self, p):
        "expr : BOOL"

        p[0] = Bool(p[1])

    def p_epsilon(self, p):
        """
        epsilon :
        """

    def build(self):
        self.lexer = Cool_Lexer()
        self.lexer.build()

        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.errors = []

    def find_column(self, t):
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        return t.lexpos - line_start + 1

    def p_error(self, p):
        if not p:
            self.errors.append(f"(0, 0) - SyntacticError: ERROR at or near EOF")

        else:
            line_number = p.lineno
            column = self.find_column(p)

            # (<línea>,<columna>) - <tipo_de_error>: <texto_del_error>
            self.errors.append(f"({line_number}, {column}) - SyntacticError: ERROR at or near \"{p.value}\"")

    precedence = (
        ("right", "ASSIGN"),
        ("right", "NOT"),
        ("nonassoc", "LESS", "LESS_EQ", "EQ"),
        ("left", "PLUS", "MINUS"),
        ("left", "MUL", "DIV"),
        ("right", "ISVOID"),
        ("right", "INT_COMP"),
        ("right", "CAST"),
        ("left", "DOT")
    )
