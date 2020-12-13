import ply.yacc as yacc
from lexer import tokens
from ast import *

# no terminal de entrada de la gramatica
start = 'program'

# para devolver los errores que se encuentran
errors = []


# para devolver la columna de los simbolos
def find_column(p, lex_pos):
    line_start = p.lexer.lexdata.rfind('\n', 0, lex_pos) + 1
    return (lex_pos - line_start) + 1


# para mandar la posicion de los simbolos a los nodos del AST
def GetPosition(p, x):
    return p.lineno(x), find_column(p, p.lexpos(x))


# no terminal de la entrada de la gramatica, el programa consiste en una lista de clases
# devuelve un nodo ProgramNode
def p_program(p):
    '''program : class_list'''
    p[0] = ProgramNode(p[1], GetPosition(p, 1))


# no terminal de lista de clases y sus producciones
# devuelve una lista con ClassNode
def p_class_list(p):
    '''class_list : class_definition class_list
                    | class_definition'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


# no terminal de estructura de una clases
# devuelve un ClassNode
def p_class_definition(p):
    '''class_definition : CLASS CLASSID LBRACE class_feature_list RBRACE SEMICOLON
                        | CLASS CLASSID INHERITS CLASSID LBRACE class_feature_list RBRACE SEMICOLON'''
    if len(p) == 7:
        p[0] = ClassNode(p[2], p[4], None, [GetPosition(p, 2)])
    else:
        p[0] = ClassNode(p[2], p[6], p[4], [GetPosition(p, 4)])


# para el simbolo vacio
def p_empty(p):
    'empty :'
    pass


# no terminal de lista de caracteristicas de la clase (atributos y metodos)
# devuelve una lista de FeatureNode
def p_class_feature_list(p):
    '''class_feature_list : feature class_feature_list
                            | empty'''

    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


# no terminal de una caracteristica y sus producciones
# devuelve lo que devuelva el no terminal de la caracteristica correspondiente
def p_feature(p):
    '''feature : attribute_feature
                | function_feature'''
    p[0] = p[1]


# no terminal de la caracteristica de atributo
# devuelve un nodo de tipo AttributeFeatureNode
def p_attribute_feature(p):
    '''attribute_feature : ATTRIBUTEID COLON CLASSID SEMICOLON
                            | ATTRIBUTEID COLON CLASSID ASSIGNATION expression SEMICOLON'''
    if len(p) == 5:
        p[0] = AttributeFeatureNode(p[1], p[3], None, [GetPosition(p, 1)])
    else:
        p[0] = AttributeFeatureNode(p[1], p[3], p[5], [GetPosition(p, 1)])


# no terminal de la caracteristica de metodos
# devuelve un nodo FunctionFeatureNode
def p_function_feature(p):
    '''function_feature : ATTRIBUTEID LPAREN parameters_list RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON
                        | ATTRIBUTEID LPAREN RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON'''
    if len(p) == 10:
        p[0] = FunctionFeatureNode(p[1], [], p[5], p[7], [GetPosition(p, 1)])
    else:
        p[0] = FunctionFeatureNode(p[1], p[3], p[6], p[8], [GetPosition(p, 1)])


# no terminal de la lista de parametros de un metodo
# devuelve una lista de ParameterNode
def p_parameter_list(p):
    '''parameters_list : parameter COMMA parameters_list
                        | parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# no teminal de un parametro de una funcion
# devuelve un nodo ParameterNode
def p_parameter(p):
    '''parameter : ATTRIBUTEID COLON CLASSID'''
    p[0] = ParameterNode(p[1], p[3], [GetPosition(p, 3)])


# no teminal de una expresion en COOL
# devuelve un nodo de tipo ExpressionNode
def p_expression(p):
    '''expression : not_form
                    | mixed_expression'''
    p[0] = p[1]


# no teminal de una expresion de tipo not
# devuelve un nodo NotNode
def p_not_form(p):
    '''not_form : NOT mixed_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = NotNode(p[2], [GetPosition(p, 1)])


# no terminal para expresiones de comparacion
# devuelve el correspondiente nodo, y si lo que corresponde no es una operacion
# de comparacion entonces se devuelve lo que devuelva la produccion correspondiente
def p_mixed_expression(p):
    '''mixed_expression : mixed_expression LESSEQUAL arithmetic_expression
                        | mixed_expression LESS arithmetic_expression
                        | mixed_expression EQUAL expression
                        | arithmetic_expression'''
    if len(p) > 2:
        if p[2] == "<":
            p[0] = LessNode(p[1], p[3], [GetPosition(p, 2)])
        else:
            if p[2] == "=":
                p[0] = EqualNode(p[1], p[3], [GetPosition(p, 2)])
            else:
                p[0] = LessEqualNode(p[1], p[3], [GetPosition(p, 2)])
    else:
        p[0] = p[1]


# no teminal de las operaciones de suma y resta
# devuelve el correspondiente nodo y sino lo que devuelva la ultima produccion
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


# no teminal de las operaciones de multiplicacion y division
# devuelve el correspondiente nodo y sino lo que devuelva la ultima produccion
def p_term(p):
    '''term : term TIMES isvoid_form
            | term DIVIDE isvoid_form
            | isvoid_form'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == "*":
            p[0] = TimesNode(p[1], p[3], [GetPosition(p, 2)])
        else:
            p[0] = DivideNode(p[1], p[3], [GetPosition(p, 2)])


# no terminal de la operacion isvoid
# devuelve un nodo IsVoidNode, sino lo que devuelva la ultima produccion
def p_isvoid_form(p):
    '''isvoid_form : ISVOID expression
                    | complement_form'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = IsVoidNode(p[2], [GetPosition(p, 1)])


# no terminal de la operacion de complemento de entero
# devuelve un nodo ComplementNode, sino lo que devuelva la ultima produccion
def p_complement_form(p):
    '''complement_form : COMPLEMENT expression
                        | program_atom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ComplementNode(p[2], [GetPosition(p, 1)])


######### a partir de aqui todas son producciones del no terminal program_atom ########


# producciones para constantes booleanas
def p_program_atom_boolean(p):
    '''program_atom : TRUE
                    | FALSE'''
    p[0] = ConstantBoolNode(p[1], [GetPosition(p, 1)])


# produccion para constantes de cadenas de caracteres
def p_program_atom_string(p):
    '''program_atom : STRING'''
    p[0] = ConstantStringNode(p[1], [GetPosition(p, 1)])


# produccion para constantes enteras
def p_program_atom_int(p):
    '''program_atom : NUMBER'''
    p[0] = ConstantNumericNode(p[1], [GetPosition(p, 1)])


# produccion para identificadores que se encuentran
def p_program_atom_id(p):
    '''program_atom : ATTRIBUTEID'''
    p[0] = VariableNode(p[1], [GetPosition(p, 1)])


# produccion para expresiones encerradas por parentesis
def p_program_atom_parentesis(p):
    '''program_atom : LPAREN expression RPAREN'''
    p[0] = p[2]


# produccion para expressiones new
def p_program_atom_new(p):
    '''program_atom : NEW CLASSID'''
    p[0] = NewStatementNode(p[2], [GetPosition(p, 1)])


# producciones para expressiones de llamado de metodos de la clase actual
def p_program_atom_member(p):
    '''program_atom : member_call'''
    p[0] = p[1]


def p_member_call(p):
    '''member_call : ATTRIBUTEID LPAREN RPAREN
                    | ATTRIBUTEID LPAREN argument_list RPAREN'''
    if len(p) == 4:
        p[0] = FunctionCallStatement(VariableNode("self", p.lineno), None, p[1], [], [GetPosition(p, 1)])
    else:
        p[0] = FunctionCallStatement(VariableNode("self", p.lineno), None, p[1], p[3], [GetPosition(p, 1)])


# producciones para lista de argumentos
def p_argument_list(p):
    '''argument_list : expression
                    | expression COMMA argument_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# produccion para expressiones de llamados de funcion de una instancia determinada
def p_program_atom_function(p):
    '''program_atom : program_atom function_call'''
    p[0] = FunctionCallStatement(p[1], (p[2])[0], (p[2])[1], (p[2])[2], p[1].lineNumber)


# producciones de lo que viene a partir de la instancia en un llamado de funcion
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


# produccion para expressiones de asignacion
def p_program_atom_assign(p):
    '''program_atom : ATTRIBUTEID ASSIGNATION expression'''
    p[0] = AssignStatementNode(p[1], p[3], [GetPosition(p, 1)])


# produccion para expressiones de tipo case
def p_program_atom_case(p):
    '''program_atom : CASE expression OF case_body ESAC'''
    p[0] = CaseStatementNode(p[2], p[4], GetPosition(p, 1))


# producciones para las ramas de las expresiones case
def p_case_body(p):
    '''case_body : ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON case_body
                | ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON'''
    if (len(p) == 7):
        p[0] = [CaseBranchNode(p[1], p[3], p[5], [GetPosition(p, 3)])]
    else:
        p[0] = [CaseBranchNode(p[1], p[3], p[5], [GetPosition(p, 3)])] + p[7]


# produccion para expressiones let
def p_program_atom_let(p):
    '''program_atom : LET let_body IN expression'''
    p[0] = LetStatementNode(p[2], p[4], [GetPosition(p, 1)])


# producciones para las asignaciones e inicializaciones de las expreciones let
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


# produccion para expressiones block
def p_program_atom_block(p):
    '''program_atom : LBRACE expression_list RBRACE'''
    p[0] = BlockStatementNode(p[2], [GetPosition(p, 1)])


# producciones de listas de expresiones para la expresion block
def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# produccion para expressiones while
def p_program_atom_while(p):
    '''program_atom : WHILE expression LOOP expression POOL'''
    p[0] = LoopStatementNode(p[2], p[4], [GetPosition(p, 2)])


# produccion para expressiones condicionales
def p_program_atom_if(p):
    '''program_atom : IF expression THEN expression ELSE expression FI'''
    p[0] = ConditionalStatementNode(p[2], p[4], p[6], [GetPosition(p, 1)])


# devolver los errores cuando se encuentren
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


# para ejecutar el parser desde compiler.py
def make_parser(code):
    global errors
    errors = []
    result = parser.parse(code)
    return result, errors
