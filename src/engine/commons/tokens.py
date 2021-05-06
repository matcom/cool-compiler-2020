####### Tokens #######

keywords = (
    'CLASS',
    'ELSE',
    # false case is independently treated
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
    # true case is independently treated
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
