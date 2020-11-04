from ply import lexer as lexer

errors = []
reserved = {
    'class': 'CLASS',
    'else': 'ELSE',
    'false': 'FALSE',
    'fi': 'FI',
    'if': 'IF',
    'inherits': 'INHERITS',
    'in': 'IN',
    'isvoid': 'ISVOID',
    'let': 'LET',
    'loop': 'LOOP',
    'pool': 'POOL',
    'then': 'THEN',
    'while': 'WHILE',
    'case': 'CASE',
    'esac': 'ESAC',
    'new': 'NEW',
    'of': 'OF',
    'not': 'NOT',
    'true': 'TRUE',
}
tokens = [
	'NUMBER',
	'STRING',
	'PLUS',
	'MINUS',
	'DIVIDE',
	'TIMES',
	'LPAREN',
	'RPAREN',
	'ATTRIBUTEID',
	'CLASSID',
	'LBRACE',
	'RBRACE',
	'COMMA',
	'SEMICOLON',
	'COLON',
	'ASSIGNATION',
	'ARROW',
	'DOT',
	'LESS',
	'LESSEQUAL',
	'GREATER',
	'GREATEREQUAL',
	'EQUAL',
	'COMPLEMENT',
	'DISPATCH'
] + list(reserved.values())
tokens_ignore = ' \t\f\v\f'
