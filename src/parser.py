import ply.yacc as yacc
from lexer import Cool_Lexer
import sys


class Parser:
    def p_program(self, p):
        """
        program : class SEMICOLON program
        |	 class SEMICOLON
        """

    def p_class(self, p):
        """
        class : CLASS TYPE inherits LBRACE class_feature RBRACE
        """

    def p_inherits(self, p):
        """
        inherits : INHERITS TYPE
        |	 epsilon
        """

    def p_class_feature(self, p):
        """
        class_feature : feature SEMICOLON class_feature
        |	 epsilon
        """

    def p_feature(self, p):
        """
        feature : ID LPAREN formal_params RPAREN COLON TYPE LBRACE expr RBRACE
        |	 simple_attribute
        """

    def p_formal_params(self, p):
        """
        formal_params : formal_list
        |	 epsilon
        """

    def p_formal_list(self, p):
        """
        formal_list : ID COLON TYPE formal_list_helper
        """

    def p_formal_list_helper(self, p):
        """
        formal_list_helper : COMMA ID COLON TYPE formal_list_helper
        |	 epsilon
        """

    def p_expr_list_semicolon(self, p):
        """
        expr_list_semicolon : expr SEMICOLON expr_list_semicolon
        |	 expr SEMICOLON
        """

    def p_expr_params(self, p):
        """
        expr_params : expr_list_comma
        |	 epsilon
        """

    def p_expr_list_comma(self, p):
        """
        expr_list_comma : expr expr_list_comma_helper
        """

    def p_expr_list_comma_helper(self, p):
        """
        expr_list_comma_helper : COMMA expr expr_list_comma_helper
        |	 epsilon
        """

    def p_cast(self, p):
        """
        cast : CAST TYPE
        |	 epsilon
        """

    def p_simple_attribute(self, p):
        """
        simple_attribute : ID COLON TYPE assignation
        """

    def p_compound_attribute(self, p):
        """
        compound_attribute : simple_attribute compound_attribute_helper
        """

    def p_compound_attribute_helper(self, p):
        """
        compound_attribute_helper : COMMA simple_attribute compound_attribute_helper
        |	 epsilon
        """

    def p_assignation(self, p):
        """
        assignation : ASSIGN expr
        |	 epsilon
        """

    def p_case_list(self, p):
        """
        case_list : ID COLON TYPE ARROW expr SEMICOLON case_list
        |	 ID COLON TYPE ARROW expr SEMICOLON
        """

    def p_expr(self, p):
        """
        expr : ID ASSIGN expr
        |	 expr cast DOT ID LPAREN expr_params RPAREN
        |	 ID LPAREN expr_params RPAREN
        |	 IF expr THEN expr ELSE expr FI
        |	 WHILE expr LOOP expr POOL
        |	 LBRACE expr_list_semicolon RBRACE
        |	 LET compound_attribute IN expr
        |	 CASE expr OF case_list ESAC
        |	 NEW TYPE
        |	 ISVOID expr
        |	 expr PLUS expr
        |	 expr MINUS expr
        |	 expr MUL expr
        |	 expr DIV expr
        |	 INT_COMP expr
        |	 expr LESS expr
        |	 expr LESS_EQ expr
        |	 expr EQ expr
        |	 NOT expr
        |	 LPAREN expr RPAREN
        |	 ID
        |	 INT
        |	 STRING
        |	 BOOL
        """

    def p_epsilon(self, p):
        """
        epsilon :
        """

    def build(self):
        self.lexer = Cool_Lexer()
        self.lexer.build()

        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def find_column(self, t):
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        return t.lexpos - line_start + 1

    def p_error(self, p):
        if not p:
            print(f"(0, 0) - SyntacticError: ERROR at or near EOF")

        else:
            line_number = p.lineno
            column = self.find_column(p)

            # (<línea>,<columna>) - <tipo_de_error>: <texto_del_error>
            print(f"({line_number}, {column}) - SyntacticError: ERROR at or near \"{p.value}\"")

        exit(1)

    precedence = (
        ("right", "ASSIGN"),
        ("left", "NOT"),
        ("nonassoc", "LESS", "LESS_EQ", "EQ"),
        ("left", "PLUS", "MINUS"),
        ("left", "MUL", "DIV"),
        ("left", "ISVOID"),
        ("left", "INT_COMP"),
        ("left", "CAST"),
        ("left", "DOT")
    )


if __name__ == "__main__":
    parser_obj = Parser()
    parser_obj.build()

    with open(sys.argv[1]) as f:
        inp = ""

        for line in f:
            inp += line

        parser_obj.parser.parse(inp)
