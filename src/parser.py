import ply.yacc as yacc
from lexer import tokens
from ast import *

start = 'program'
errors = []


def find_column(p, lex_pos):
    line_start = p.lexer.lexdata.rfind('\n', 0, lex_pos) + 1
    return (lex_pos - line_start) + 1


def GetPosition(p, x):
    return p.lineno(x), find_column(p, p.lexpos(x))


def p_program(p):
    '''program : class_list'''
    p[0] = ProgramNode(p[1], GetPosition(p, 1))


def p_class_list(p):
    '''class_list : class_definition class_list
                    | class_definition'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_class_definition(p):
    '''class_definition : CLASS CLASSID LBRACE class_feature_list RBRACE SEMICOLON
                        | CLASS CLASSID INHERITS CLASSID LBRACE class_feature_list RBRACE SEMICOLON'''
    if len(p) == 7:
        p[0] = ClassNode(p[2], p[4], None, [GetPosition(p, 2)])
    else:
        p[0] = ClassNode(p[2], p[6], p[4], [GetPosition(p, 4)])


def p_empty(p):
    'empty :'
    pass


def p_class_feature_list(p):
    '''class_feature_list : feature class_feature_list
                            | empty'''

    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_feature(p):
    '''feature : attribute_feature
                | function_feature'''
    p[0] = p[1]


def p_attribute_feature(p):
    '''attribute_feature : ATTRIBUTEID COLON CLASSID SEMICOLON
                            | ATTRIBUTEID COLON CLASSID ASSIGNATION expression SEMICOLON'''
    if len(p) == 5:
        p[0] = AttributeFeatureNode(p[1], p[3], None, [GetPosition(p, 1)])
    else:
        p[0] = AttributeFeatureNode(p[1], p[3], p[5], [GetPosition(p, 1)])


def p_function_feature(p):
    '''function_feature : ATTRIBUTEID LPAREN parameters_list RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON
                        | ATTRIBUTEID LPAREN RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON'''
    if len(p) == 10:
        p[0] = FunctionFeatureNode(p[1], [], p[5], p[7], [GetPosition(p, 1)])
    else:
        p[0] = FunctionFeatureNode(p[1], p[3], p[6], p[8], [GetPosition(p, 1)])


def p_parameter_list(p):
    '''parameters_list : parameter COMMA parameters_list
                        | parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_parameter(p):
    '''parameter : ATTRIBUTEID COLON CLASSID'''
    p[0] = ParameterNode(p[1], p[3], [GetPosition(p, 3)])


def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_let_body(p):
    '''let_body : ATTRIBUTEID COLON CLASSID
                | ATTRIBUTEID COLON CLASSID ASSIGNATION expression
                | ATTRIBUTEID COLON CLASSID COMMA let_body
                | ATTRIBUTEID COLON CLASSID ASSIGNATION expression COMMA let_body'''
    if len(p) == 4:
        p[0] = [AttributeFeatureNode(p[1], p[3], None, [GetPosition(p, 3)])]
    else:
        if len(p) == 8:
            p[0] = [AttributeFeatureNode(p[1], p[3], p[5], [GetPosition(p, 3)])] + p[7]
        else:
            if p[4] == "<-":
                p[0] = [AttributeFeatureNode(p[1], p[3], p[5], [GetPosition(p, 3)])]
            else:
                p[0] = [AttributeFeatureNode(p[1], p[3], None, [GetPosition(p, 3)])] + p[5]


def p_case_body(p):
    '''case_body : ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON case_body
                | ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON'''
    if (len(p) == 7):
        p[0] = [CaseBranchNode(p[1], p[3], p[5], [GetPosition(p, 3)])]
    else:
        p[0] = [CaseBranchNode(p[1], p[3], p[5], [GetPosition(p, 3)])] + p[7]


def p_expression(p):
    '''expression : arithmetic_expression_form'''
    p[0] = p[1]


def p_arithmetic_expression_form(p):
    '''arithmetic_expression_form : NOT mixed_expression
                                    | mixed_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = NotNode(p[2], [GetPosition(p, 2)])


def p_mixed_expression(p):
    '''mixed_expression : mixed_expression LESSEQUAL arithmetic_expression
                        | mixed_expression LESS arithmetic_expression
                        | mixed_expression EQUAL arithmetic_expression
                        | arithmetic_expression'''
    if len(p) > 2:
        if p[2] == "<":
            p[0] = LessNode(p[1], p[3], [GetPosition(p, 3)])
        else:
            if p[2] == "=":
                p[0] = EqualNode(p[1], p[3], [GetPosition(p, 2)])
            else:
                p[0] = LessEqualNode(p[1], p[3], [GetPosition(p, 2)])
    else:
        p[0] = p[1]


def p_arithmetic_expression(p):
    '''arithmetic_expression : arithmetic_expression PLUS term
                            | arithmetic_expression MINUS term
                            | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == "+":
            p[0] = PlusNode(p[1], p[3], [GetPosition(p, 2)])
        else:
            p[0] = MinusNode(p[1], p[3], [GetPosition(p, 2)])


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == "*":
            p[0] = TimesNode(p[1], p[3], GetPosition(p, 3))
        else:
            p[0] = DivideNode(p[1], p[3], [GetPosition(p, 3)])


def p_factor(p):
    '''factor : ISVOID factor_extra
                | factor_extra'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = IsVoidNode(p[2], [GetPosition(p, 1)])


def p_factor_extra(p):
    '''factor_extra : COMPLEMENT program_atom
                    | program_atom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ComplementNode(p[2], [GetPosition(p, 2)])


def p_program_atom_boolean(p):
    '''program_atom : TRUE
                    | FALSE'''
    p[0] = ConstantBoolNode(p[1], [GetPosition(p, 1)])


def p_program_atom_string(p):
    '''program_atom : STRING'''
    p[0] = ConstantStringNode(p[1], [GetPosition(p, 1)])


def p_program_atom_int(p):
    '''program_atom : NUMBER'''
    p[0] = ConstantNumericNode(p[1], [GetPosition(p, 1)])


def p_program_atom_id(p):
    '''program_atom : ATTRIBUTEID'''
    p[0] = VariableNode(p[1], [GetPosition(p, 1)])


def p_program_atom_parentesis(p):
    '''program_atom : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_program_atom_new(p):
    '''program_atom : NEW CLASSID'''
    p[0] = NewStatementNode(p[2], [GetPosition(p, 2)])


def p_program_atom_member(p):
    '''program_atom : member_call'''
    p[0] = p[1]


def p_program_atom_function(p):
    '''program_atom : program_atom function_call'''
    p[0] = FunctionCallStatement(p[1], (p[2])[0], (p[2])[1], (p[2])[2], [GetPosition(p, 2)])


def p_program_atom_assign(p):
    '''program_atom : ATTRIBUTEID ASSIGNATION expression'''
    p[0] = AssignStatementNode(p[1], p[3], [GetPosition(p, 2)])


def p_program_atom_case(p):
    '''program_atom : CASE expression OF case_body ESAC'''
    p[0] = CaseStatementNode(p[2], p[4], GetPosition(p, 1))


def p_program_atom_let(p):
    '''program_atom : LET let_body IN expression'''
    p[0] = LetStatementNode(p[2], p[4], [GetPosition(p, 1)])


def p_program_atom_block(p):
    '''program_atom : LBRACE expression_list RBRACE'''
    p[0] = BlockStatementNode(p[2], [GetPosition(p, 1)])


def p_program_atom_while(p):
    '''program_atom : WHILE expression LOOP expression POOL'''
    p[0] = LoopStatementNode(p[2], p[4], [GetPosition(p, 2)])


def p_program_atom_if(p):
    '''program_atom : IF expression THEN expression ELSE expression FI'''
    p[0] = ConditionalStatementNode(p[2], p[4], p[6], [GetPosition(p, 1)])


def p_function_call(p):
    '''function_call : DOT ATTRIBUTEID LPAREN argument_list RPAREN
                    | DOT ATTRIBUTEID LPAREN RPAREN
                    | DISPATCH CLASSID DOT ATTRIBUTEID LPAREN argument_list RPAREN
                    | DISPATCH CLASSID DOT ATTRIBUTEID LPAREN RPAREN'''

    if len(p) == 5:
        p[0] = [None, p[2], []]
    else:
        if len(p) == 6:
            p[0] = [None, p[2], p[4]]
        else:
            if len(p) == 7:
                p[0] = [p[2], p[4], []]
            else:
                p[0] = [p[2], p[4], p[6]]


def p_argument_list(p):
    '''argument_list : expression
                    | expression COMMA argument_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_member_call(p):
    '''member_call : ATTRIBUTEID LPAREN RPAREN
                    | ATTRIBUTEID LPAREN argument_list RPAREN'''
    if len(p) == 4:
        p[0] = FunctionCallStatement(VariableNode("self", p.lineno), None, p[1], [], [GetPosition(p, 1)])
    else:
        p[0] = FunctionCallStatement(VariableNode("self", p.lineno), None, p[1], p[3], [GetPosition(p, 1)])


def p_error(p):
    global errors
    if p is None:
        errors.append("(0, 0) - SyntacticError: ERROR at or near EOF")
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
        errors.append("(%s, %s) - SyntacticError: ERROR at or near %s " % (p.lineno, p.colno, word))
    else:
        errors.append("(%s, %s) - SyntacticError: ERROR at or near \"%s\"" % (p.lineno, p.colno, word))
    pass


parser = yacc.yacc(debug=1)


def make_parser(code):
    global errors
    errors = []
    result = parser.parse(code)
    return result, errors
