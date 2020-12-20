import ply.yacc as yacc
from lexer import tokens
from ast_hierarchy import *

start = 'program'

errors = []

def findCol(p, lexPos):
    lineStart = p.lexer.lexdata.rfind('\n', 0, lexPos) + 1
    return (lexPos - lineStart) + 1

def GetPos(p, x):
    return p.lineno(x), findCol(p, p.lexpos(x))

def p_program(p):
    '''program : classList'''
    p[0] = ProgramNode(p[1], GetPos(p, 1))

def p_classList(p):
    '''classList : classDefinition classList
                    | classDefinition'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_classDefinition(p):
    '''classDefinition : CLASS CLASSID LBRACE classFeatureList RBRACE SEMICOLON
                        | CLASS CLASSID INHERITS CLASSID LBRACE classFeatureList RBRACE SEMICOLON'''
    if len(p) == 7:
        p[0] = ClassNode(p[2], p[4], None, [GetPos(p, 2)])
    else:
        p[0] = ClassNode(p[2], p[6], p[4], [GetPos(p, 4)])

def p_empty(p):
    'empty :'
    pass

def p_classFeatureList(p):
    '''classFeatureList : feature classFeatureList
                            | empty'''

    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_feature(p):
    '''feature : attributeFeature
                | functionFeature'''
    p[0] = p[1]

def p_attributeFeature(p):
    '''attributeFeature : ATTRIBUTEID COLON CLASSID SEMICOLON
                            | ATTRIBUTEID COLON CLASSID ASSIGNATION expression SEMICOLON'''
    if len(p) == 5:
        p[0] = AttributeFeatureNode(p[1], p[3], None, [GetPos(p, 1)])
    else:
        p[0] = AttributeFeatureNode(p[1], p[3], p[5], [GetPos(p, 1)])

def p_functionFeature(p):
    '''functionFeature : ATTRIBUTEID LPAREN parameterList RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON
                        | ATTRIBUTEID LPAREN RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON'''
    if len(p) == 10:
        p[0] = FunctionFeatureNode(p[1], [], p[5], p[7], [GetPos(p, 1)])
    else:
        p[0] = FunctionFeatureNode(p[1], p[3], p[6], p[8], [GetPos(p, 1)])

def p_parameterList(p):
    '''parameterList : parameter COMMA parameterList
                        | parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parameter(p):
    '''parameter : ATTRIBUTEID COLON CLASSID'''
    p[0] = ParameterNode(p[1], p[3], [GetPos(p, 3)])

def p_expression(p):
    '''expression : notForm
                    | mixedExpression'''
    p[0] = p[1]

def p_notForm(p):
    '''notForm : NOT mixedExpression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = NotNode(p[2], [GetPos(p, 1)])

def p_mixedExpression(p):
    '''mixedExpression : mixedExpression LESSEQUAL arithmeticExpression
                        | mixedExpression LESS arithmeticExpression
                        | mixedExpression EQUAL expression
                        | arithmeticExpression'''
    if len(p) > 2:
        if p[2] == "<":
            p[0] = LessNode(p[1], p[3], [GetPos(p, 2)])
        else:
            if p[2] == "=":
                p[0] = EqualNode(p[1], p[3], [GetPos(p, 2)])
            else:
                p[0] = LessEqualNode(p[1], p[3], [GetPos(p, 2)])
    else:
        p[0] = p[1]

def p_arithmeticExpression(p):
    '''arithmeticExpression : arithmeticExpression PLUS term
                             | arithmeticExpression MINUS term
                             | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == "+":
            p[0] = PlusNode(p[1], p[3], [GetPos(p, 2)])
        else:
            p[0] = MinusNode(p[1], p[3], [GetPos(p, 2)])

def p_term(p):
    '''term : term TIMES isvoidForm
            | term DIVIDE isvoidForm
            | isvoidForm'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == "*":
            p[0] = TimesNode(p[1], p[3], [GetPos(p, 2)])
        else:
            p[0] = DivideNode(p[1], p[3], [GetPos(p, 2)])

def p_isvoidForm(p):
    '''isvoidForm : ISVOID expression
                    | complementForm'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = IsVoidNode(p[2], [GetPos(p, 1)])

def p_complementForm(p):
    '''complementForm : COMPLEMENT expression
                        | programAtom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ComplementNode(p[2], [GetPos(p, 1)])

def p_programAtomBoolean(p):
    '''programAtom : TRUE
                    | FALSE'''
    p[0] = ConstantBoolNode(p[1], [GetPos(p, 1)])

def p_programAtomString(p):
    '''programAtom : STRING'''
    p[0] = ConstantStringNode(p[1], [GetPos(p, 1)])

def p_programAtomInt(p):
    '''programAtom : NUMBER'''
    p[0] = ConstantNumericNode(p[1], [GetPos(p, 1)])

def p_programAtomId(p):
    '''programAtom : ATTRIBUTEID'''
    p[0] = VariableNode(p[1], [GetPos(p, 1)])

def p_programAtomParentesis(p):
    '''programAtom : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_programAtomNew(p):
    '''programAtom : NEW CLASSID'''
    p[0] = NewStatementNode(p[2], [GetPos(p, 1)])


def p_programAtomMember(p):
    '''programAtom : memberCall'''
    p[0] = p[1]

def p_memberCall(p):
    '''memberCall : ATTRIBUTEID LPAREN RPAREN
                    | ATTRIBUTEID LPAREN argumentList RPAREN'''
    if len(p) == 4:
        p[0] = FunctionCallStatement(VariableNode("self", p.lineno), None, p[1], [], [GetPos(p, 1)])
    else:
        p[0] = FunctionCallStatement(VariableNode("self", p.lineno), None, p[1], p[3], [GetPos(p, 1)])

def p_argumentList(p):
    '''argumentList : expression
                    | expression COMMA argumentList'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_programAtomFunction(p):
    '''programAtom : programAtom functionCall'''
    p[0] = FunctionCallStatement(p[1], (p[2])[0], (p[2])[1], (p[2])[2], p[1].lineNumber)

def p_functionCall(p):
    '''functionCall : DOT ATTRIBUTEID LPAREN argumentList RPAREN
                    | DOT ATTRIBUTEID LPAREN RPAREN
                    | DISPATCH CLASSID DOT ATTRIBUTEID LPAREN argumentList RPAREN
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

def p_programAtomAssign(p):
    '''programAtom : ATTRIBUTEID ASSIGNATION expression'''
    p[0] = AssignStatementNode(VariableNode(p[1],GetPos(p,1)), p[3], [GetPos(p, 1)])

def p_programAtomCase(p):
    '''programAtom : CASE expression OF caseBody ESAC'''
    p[0] = CaseStatementNode(p[2], p[4], GetPos(p, 1))

def p_caseBody(p):
    '''caseBody : ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON caseBody
                | ATTRIBUTEID COLON CLASSID ARROW expression SEMICOLON'''
    if (len(p) == 7):
        p[0] = [CaseBranchNode(p[1], p[3], p[5], [GetPos(p, 3)])]
    else:
        p[0] = [CaseBranchNode(p[1], p[3], p[5], [GetPos(p, 3)])] + p[7]

# produccion para expressiones let
def p_programAtomLet(p):
    '''programAtom : LET letBody IN expression'''
    p[0] = LetStatementNode(p[2], p[4], [GetPos(p, 1)])

def p_letBody(p):
    '''letBody : ATTRIBUTEID COLON CLASSID
                | ATTRIBUTEID COLON CLASSID ASSIGNATION expression
                | ATTRIBUTEID COLON CLASSID COMMA letBody
                | ATTRIBUTEID COLON CLASSID ASSIGNATION expression COMMA letBody'''
    if len(p) == 4:
        p[0] = [AttributeFeatureNode(p[1], p[3], None, [GetPos(p, 3)])]
    else:
        if len(p) == 8:
            p[0] = [AttributeFeatureNode(p[1], p[3], p[5], [GetPos(p, 3)])] + p[7]
        else:
            if p[4] == "<-":
                p[0] = [AttributeFeatureNode(p[1], p[3], p[5], [GetPos(p, 3)])]
            else:
                p[0] = [AttributeFeatureNode(p[1], p[3], None, [GetPos(p, 3)])] + p[5]

def p_programAtomBlock(p):
    '''programAtom : LBRACE expressionList RBRACE'''
    p[0] = BlockStatementNode(p[2], [GetPos(p, 1)])

def p_expressionList(p):
    '''expressionList : expression SEMICOLON expressionList
                        | expression SEMICOLON'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_programAtomWhile(p):
    '''programAtom : WHILE expression LOOP expression POOL'''
    p[0] = LoopStatementNode(p[2], p[4], [GetPos(p, 2)])

def p_programAtomIf(p):
    '''programAtom : IF expression THEN expression ELSE expression FI'''
    p[0] = ConditionalStatementNode(p[2], p[4], p[6], [GetPos(p, 1)])

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

def parse(code):
    global errors
    errors = []
    result = parser.parse(code)
    return result, errors
