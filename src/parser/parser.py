import ply.yacc as yacc


def p_program(p):
    """
    program : class SEMICOLON program
    |	 class SEMICOLON
    """


def p_class(p):
    """
    class : CLASS TYPE inherits LBRACE class_feature RBRACE
    """


def p_inherits(p):
    """
    inherits : INHERITS TYPE
    |	 epsilon
    """


def p_class_feature(p):
    """
    class_feature : feature SEMICOLON class_feature
    |	 epsilon
    """


def p_feature(p):
    """
    feature : ID LPAREN formal_params RPAREN COLON TYPE LBRACE expr RBRACE
    |	 simple_attribute
    """


def p_formal_params(p):
    """
    formal_params : formal_list
    |	 epsilon
    """


def p_formal_list(p):
    """
    formal_list : ID COLON TYPE formal_list_helper
    """


def p_formal_list_helper(p):
    """
    formal_list_helper : COMMA ID COLON TYPE formal_list_helper
    |	 epsilon
    """


def p_expr_list_semicolon(p):
    """
    expr_list_semicolon : expr SEMICOLON expr_list_semicolon
    |	 expr SEMICOLON
    """


def p_expr_params(p):
    """
    expr_params : expr_list_comma
    |	 epsilon
    """


def p_expr_list_comma(p):
    """
    expr_list_comma : expr expr_list_comma_helper
    """


def p_expr_list_comma_helper(p):
    """
    expr_list_comma_helper : COMMA expr expr_list_comma_helper
    |	 epsilon
    """


def p_cast(p):
    """
    cast : @TYPE
    |	 epsilon
    """


def p_simple_attribute(p):
    """
    simple_attribute : ID COLON TYPE assignation
    """


def p_compound_attribute(p):
    """
    compound_attribute : simple_attribute compound_attribute_helper
    """


def p_compound_attribute_helper(p):
    """
    compound_attribute_helper : COMMA simple_attribute compound_attribute_helper
    |	 epsilon
    """


def p_assignation(p):
    """
    assignation : ASSIGN expr
    |	 epsilon
    """


def p_case_list(p):
    """
    case_list : ID COLON TYPE ARROW expr SEMICOLON case_list
    """


def p_expr(p):
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


def p_epsilon(p):
    """
    epsilon :
    """
