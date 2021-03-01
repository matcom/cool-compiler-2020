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
        'OF',
        'NOT'
    ]

operators = [
        'PLUS',
        'MINUS',
        'MULT',
        'DIV',
        'LESS',
        'LESSEQUAL',
        'EQUAL',
        'INT_COMPLEMENT'
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
        'LARROW',
        'RARROW'
     ]

     #list of token names
tokens = [
        'INTEGER',
        'STRING',
        'BOOL',
        'TYPE',
        'OBJECT'
     ] + operators + keywords + specials