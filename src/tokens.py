keywords = [
        'CLASS',
        'ELSE',
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
        'OF'
    ]

operators = [
        'PLUS',
        'MINUS',
        'MULT',
        'DIV',
        'LESS',
        'LESSEQUAL',
        'EQUAL',
        'INT_COMPLEMENT',
        'NOT'
    ]

specials= [
        'OCUR',
        'CCUR',
        'OPAR',
        'CPAR',
        'DOT',
        'SEMI',
        'COLON',
        'COMMA',
        'AT',
        'ASSIGN',
        'RARROW'
     ]

     #list of token names
tokens = [
        'INTEGER',
        'STRING',
        'BOOL',
        'TYPE',
        'OBJECT',
        'SPECIAL'
     ] + operators + keywords + specials