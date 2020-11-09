import ply.yacc as yacc
from lexer import tokens

start = 'program'
errors = []

def GetPosition(p, x):
	return (p.lineno(x), p.lexpos(x))

def p_program(p):
	'''program : class_list'''
	p[0] = ProgramNode(p[1])

def p_class_list(p):
	'''clas_list : class_definition class_list | class_definition'''
	if(len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = [p[1]] + p[2]

def p_class_definition(p):
	'''class_definition : CLASS CLASSID LBRACE class_feature_list RBRACE SEMICOLON
		            | CLASS CLASSID INHERITS CLASSID LBRACE class_feature_list RBRACE SEMICOLON'''
	if(len(p) == 7):
		p[0] = ClassNode(p[2], p[4], None, [GetPosition(p, 2)])
	else:
		p[0] = ClassNode(p[2], p[6], p[4], [GetPosition(p, 2), GetPosition(p, 4)])

def p_empty(p):
	'empty :'
	pass

def p_class_feature_list(p):
	'''class_feature_list : feature class_feature_list | empty'''
	if(len(p) == 3):
		p[0] = [p[1]] + p[2]
	else
		p[0] = []

def p_feature(p):
	'''feature : attribute_feature
                | function_feature'''
    	p[0] = p[1]

def p_attributte_feature(p):
	'''feature : attribute_feature : ATTRIBUTEID COLON CLASSID SEMICOLON 
		   | ATTRIBUTEDID COLON CLASSID ASSIGNATION expression SEMICOLON'''
	if(len(p) == 5):
		p[0] = AttributeFeatureNode(p[1], p[3], None, [GetPosition(p, 1), GetPosition(p, 3)])
	else:
		p[0] = AttributeFeatureNode(p[1], p[3], p[5], [GetPosition(p, 1), GetPosition(p, 3)])

def p_function_feature(p):
	'''function_feature : ATTRIBUTEID LPAREN parameters_list RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON
			    | ATTRIBUTEID LPAREN RPAREN COLON CLASSID LBRACE expression RBRACE SEMICOLON'''
	if(len(p) == 10):
		p[0] = FunctionFeatureNode(p[1], [], p[5], p[7], [GetPosition(p, 1), GetPosition(p, 5)])
    else:
        	p[0] = FunctionFeatureNode(p[1], p[3], p[6], p[8], [GetPosition(p, 1), GetPosition(p, 6)])

def p_paremeter_list(p):
	'''paremeter_list : parameter COMMA parameters_list | parameter'''
	if(len(p) == 2):
        	p[0] = [p[1]]
    	else:
        	p[0] = [p[1]] + p[3]

def p_parameter(p):
	'''parameter : ATTRIBUTEID COLON CLASSID'''
	p[0] = ParameterNode(p[1], p[3], GetPosition(p, 1), GetPosition(p, 3)])

def p_expression_list(p):
	'''expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''
    	if(len(p) == 3):
        	p[0] = [p[1]]
    	else:
        	p[0] = [p[1]] + p[3]

		
