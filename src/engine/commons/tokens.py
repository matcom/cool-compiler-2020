####### Tokens #######

keywords = (
    'CLASS',
    'ELSE',
    ### false case is independently treated
    'FI',
    'IF',
    'IN',
    'INHERITS',
    'ISVOID',
    'LET',
    'LOOP',
    'POOL',
    'THEN',
    'WHILE',
    'CASE',
    'ESAC',
    'NEW',
    'OF',
    'NOT'
    ### true case is independently treated
)

literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',']
# ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',']
terminals = {
    r'\(': 'OPAR',
    r'\)': 'CPAR',
    r'\{': 'OCURL',
    r'\}': 'CCURL',
    r'\:': 'COLON',
    r'\,': 'COMMA',
    r'\.': 'DOT',
    r'\;': 'SEMI',
    r'\@': 'AT',
    r'\*': 'STAR',
    r'\/': 'DIV',
    r'\+': 'PLUS',
    r'\-': 'MINUS',
    'class': 'CLASS',
    'else': 'ELSE',
    'fi': 'FI',
    'if': 'IF',
    'in': 'IN',
    'inherits': 'INHERITS',
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
}

tokens = (
	# Identifiers
	'TYPE', 'ID',
	# Primitive data types
	'INTEGER', 'STRING', 'BOOL',
	# Special keywords
	'ACTION',
	# Operators
	'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT',
)


class Token:
    """
    Basic token class.

    Parameters
    ----------
    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    """

    def __init__(self, lex, token_type, line=0, column=0):
        self.lex = lex
        self.token_type = token_type
        self.line = line
        self.column = column

    @property
    def type(self):
        return self.type

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)
