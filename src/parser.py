import ply.yacc as yacc
from lexer import tokens
start = 'program'

def p_program(p):
    'program : class_list'
    pass


def p_class_list(p):
    '''class_list : class_definition class_list
                    | class_definition'''
    pass


def p_class_definition(p):
    '''class_definition : CLASS CLASSID LBRACE class_feature_list RBRACE SEMICOLON
                        | CLASS CLASSID INHERITS CLASSID LBRACE class_feature_list RBRACE SEMICOLON'''
    pass


def p_empty(p):
    'empty :'
    pass


def p_class_feature_list(p):
    '''class_feature_list : feature class_feature_list
                            | empty'''
    pass


def p_feature(p):
    '''feature : attribute_feature
                | function_feature'''
    pass


def p_attribute_feature(p):
    '''attribute_feature : ATTRIBUTEID COLON CLASSID SEMICOLON
                            | ATTRIBUTEID COLON CLASSID ASSIGNATION expression SEMICOLON'''
    pass


def p_function_feature(p):
    '''function_feature : ATTRIBUTEID LPAREN parameters_list RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON
                        | ATTRIBUTEID LPAREN RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON'''
    pass


def p_parameter_list(p):
    '''parameters_list : parameter COMMA parameters_list
                        | parameter'''
    pass


def p_parameter(p):
    '''parameter : ATTRIBUTEID COLON CLASSID'''
    pass


def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''
    pass


def p_let_body(p):
    '''let_body : ATTRIBUTEID COLON CLASSID
                | ATTRIBUTEID COLON CLASSID ASSIGNATION expression
                | ATTRIBUTEID COLON CLASSID COMMA let_body
                | ATTRIBUTEID COLON CLASSID ASSIGNATION expression COMMA let_body'''
    pass


def p_case_body(p):
    '''case_body : ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON case_body
                | ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON'''
    pass


def p_expression(p):
    '''expression : mixed_expression'''
    pass


def p_mixed_expression(p):
    '''mixed_expression : mixed_expression LESSEQUAL arithmetic_expression_form
                        | mixed_expression LESS arithmetic_expression_form
                        | mixed_expression EQUAL arithmetic_expression_form
                        | arithmetic_expression_form'''
    pass


def p_arithmetic_expression_form(p):
    '''arithmetic_expression_form : NOT arithmetic_expression
                                    | arithmetic_expression'''


def p_arithmetic_expression(p):
    '''arithmetic_expression : arithmetic_expression PLUS term
                            | arithmetic_expression MINUS term
                            | term'''


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    pass


def p_factor(p):
    '''factor : ISVOID factor_extra
                | factor_extra'''
    pass


def p_factor_extra(p):
    '''factor_extra : COMPLEMENT program_atom
                    | program_atom'''
    pass


def p_program_atom_boolean(p):
    '''program_atom : TRUE
                    | FALSE'''
    pass


def p_program_atom_string(p):
    '''program_atom : STRING'''
    pass


def p_program_atom_int(p):
    '''program_atom : NUMBER'''
    pass


def p_program_atom_id(p):
    '''program_atom : ATTRIBUTEID'''
    pass


def p_program_atom_parentesis(p):
    '''program_atom : LPAREN expression RPAREN'''
    pass


def p_program_atom_new(p):
    '''program_atom : NEW CLASSID'''
    pass


def p_program_atom_member(p):
    '''program_atom : member_call'''
    pass


def p_program_atom_function(p):
    '''program_atom : program_atom function_call'''
    pass


def p_program_atom_assign(p):
    '''program_atom : ATTRIBUTEID ASSIGNATION expression'''
    pass


def p_program_atom_case(p):
    '''program_atom : CASE expression OF case_body ESAC'''
    pass


def p_program_atom_let(p):
    '''program_atom : LET let_body IN expression'''
    pass


def p_program_atom_block(p):
    '''program_atom : LBRACE expression_list RBRACE'''
    pass


def p_program_atom_while(p):
    '''program_atom : WHILE expression LOOP expression POOL'''
    pass


def p_program_atom_if(p):
    '''program_atom : IF expression THEN expression ELSE expression FI'''
    pass


def p_function_call(p):
    '''function_call : DOT ATTRIBUTEID LPAREN argument_list RPAREN
                    | DOT ATTRIBUTEID LPAREN RPAREN
                    | DISPATCH CLASSID DOT ATTRIBUTEID LPAREN argument_list RPAREN
                    | DISPATCH CLASSID DOT ATTRIBUTEID LPAREN RPAREN'''
    pass


def p_argument_list(p):
    '''argument_list : expression
                    | expression COMMA argument_list'''
    pass


def p_member_call(p):
    '''member_call : ATTRIBUTEID LPAREN RPAREN
                    | ATTRIBUTEID LPAREN argument_list RPAREN'''


def p_error(p):
    if p == None:
        print("(0, 0) - SyntacticError: ERROR at or near EOF")
        return
    word = p.value
    w = False
    if p.type == 'ASSIGNATION':
        word = 'ASSIGN'
        w = True
    if p.type == 'ESAC':
        word = 'ESAC'
        w = True
    if p.type == 'NEW':
        word = 'NEW'
        w = True
    if p.type == 'CLASS':
        word = 'CLASS'
        w = True
    if w:
        print("(%s, %s) - SyntacticError: ERROR at or near %s "% (p.lineno, p.colno, word))
    else: 
        print("(%s, %s) - SyntacticError: ERROR at or near \"%s\"" % (p.lineno, p.colno, word))
    pass


parser = yacc.yacc()


def make_parser(code):
    result = parser.parse(code)
    return result
