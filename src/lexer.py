from ply import lex as lex

# para devolver los errores que se encuentren cuando se analice el texto de entrada
errors = []

# la llave es como aparecen las palabras clave en el codigo en COOL y el valor es
# el tipo de token que se genera
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

# aqui estan los demas tipos de tokens que no corresponden a palabras clave
tokens = [
             'NUMBER',
             'STRING',
             'PLUS',
             'MINUS',
             'TIMES',
             'DIVIDE',
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

# estos son caracteres que se van a ignorar en la entrada
t_ignore = ' \t\r\v\f'


# aqui se leen las lineas que a partir de los -- y se ignoran hasta el siguiente \n
def t_INLINECOMMENT(t):
    r'--.*'
    pass


# por aqui comienza la maquina de estado para leer los comentarios multilinea
def t_start_comment(t):
    r'\(\*'
    t.lexer.push_state("COMMENT")
    t.lexer.counter = 1
    t.lexer.star = False
    t.lexer.lparen = False


# por aqui comienza la maquina de estado para leer valores de cadenas
def t_start_string(t):
    r'"'
    t.lexer.push_state("STRING")
    t.lexer.string_backslashed = False
    t.lexer.stringbuf = ""
    t.lexer.string_containsNull = False
    t.lexer.string_nullrow = 0
    t.lexer.string_nullcol = 0


# las siguientes cuatro funciones forman los tokens de operaciones aritmeticas a medida
# que aparecen los correspondientes simbolos en la entrada
def t_PLUS(t):
    r'\+'
    t.value = '+'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_MINUS(t):
    r'-'
    t.value = '-'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_TIMES(t):
    r'\*'
    t.value = '*'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_DIVIDE(t):
    r'/'
    t.value = '/'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


###################################################################################


# las siguientes funciones forman los tokens de diferentes simbolos del lenguaje
def t_LPAREN(t):
    r'\('
    t.value = '('
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_RPAREN(t):
    r'\)'
    t.value = ')'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_LBRACE(t):
    r'\{'
    t.value = '{'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_RBRACE(t):
    r'\}'
    t.value = '}'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_COMMA(t):
    r','
    t.value = ','
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_SEMICOLON(t):
    r';'
    t.value = ';'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_COLON(t):
    r':'
    t.value = ':'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_ASSIGNATION(t):
    r'<-'
    t.value = '<-'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_ARROW(t):
    r'=>'
    t.value = '=>'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_DOT(t):
    r'\.'
    t.value = '.'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


######################################################################################

# aqui se forman los tokens que corresponden a operaciones de comparacion
# las funciones de LESSEQUAL y LESS tienen que definirse en este orden sino
# habra problemas ya que el simbolo de LESS es un prefijo de LESSEQUAL, igualmente
# pasa con GREATER y GREATEREQUAL
def t_LESSEQUAL(t):
    r'<='
    t.value = '<='
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_LESS(t):
    r'<'
    t.value = '<'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_GREATEREQUAL(t):
    r'>='
    t.value = '>='
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_GREATER(t):
    r'>'
    t.value = '>'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


def t_EQUAL(t):
    r'='
    t.value = '='
    t.colno = find_column(t.lexer.lexdata, t)
    return t


##########################################################################


# a continuacion la funcion que forma los tokens de los simbolos de operaciones
# de complemento de entero
def t_COMPLEMENT(t):
    r'~'
    t.value = '~'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


# simbolo del tipo de dispatch alternativo
def t_DISPATCH(t):
    r'@'
    t.value = '@'
    t.colno = find_column(t.lexer.lexdata, t)
    return t


# aqui se forman los tokens de numeros que aparecen en la entrada
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.colno = find_column(t.lexer.lexdata, t)
    return t


# esto define las diferentes maquinas de estado
states = (
    ('STRING', 'exclusive'),
    ('COMMENT', 'exclusive'),
)


# cuando estamos leyendo un string si recivimos un \n entonces debe haber un \ antes
# (pues una cadena no puede saltarse de la linea) sino se devuelve un error
def t_STRING_newline(t):
    r'\n'
    global errors
    t.lexer.lineno += 1
    if not t.lexer.string_backslashed:
        errors.append(
            "(%s, %s) - LexicographicError: Unterminated string constant" % (t.lineno, find_column(t.lexer.lexdata, t)))
        t.lexer.pop_state()
    else:
        t.lexer.string_backslashed = False


# si estamos leyendo un comentario multilinea y encontramos el fin del codigo 
# devolvemos un error
def t_COMMENT_eof(t):
    r'\$'
    global errors
    s = t.lexer.lexdata
    lineCount = s.count('\n') + 1
    posCount = 1
    i = len(s) - 1
    while i >= 0 and s[i] != '\n':
        posCount += 1
        i -= 1
    errors.append("(%s, %s) - LexicographicError: EOF in comment" % (lineCount, find_column(t.lexer.lexdata, t) - 1))


# si se encuentra un * y antes se habia leido un ( entoces aumenta en uno la cantidad
# de comentarios multilinea abiertos, sino marcamos que avimos un * por si el siguientes
# caracter es )
def t_COMMENT_star(t):
    r'\*'
    if (t.lexer.lparen):
        t.lexer.lparen = False
        t.lexer.counter += 1
    else:
        t.lexer.star = True


# si se encuentra un ( recordarlo por si aparece un *, y si habia un * antes marcar
# que ya no lo hay
def t_COMMENT_lparen(t):
    r'\('
    t.lexerlparen = True
    if (t.lexer.star):
        t.lexer.start = False


# se devuelve un error si se encuentra un fin de fichero cuando se esta leyendo
# una cadena de caracteres
def t_STRING_eof(t):
    r'\$'
    global errors
    errors.append("(%s, %s) - LexicographicError: EOF in string constant" %
                  (t.lineno, find_column(t.lexer.lexdata, t) - 1))
    t.lexer.pop_state()


# si se encuentra un ) ver si antes habia un *, en este caso disminuir en uno
# la cantidad de indexaciones de comentarios multilinea, si la cantidad actual
# se hace 0 entonces significa que ya terminamos de leer el comentario multilinea
# y salimos de la maquina de estado para continuar tokenizando con lo siguientes
# que se lea
def t_COMMENT_rparen(t):
    r'\)'
    if t.lexer.star:
        t.lexer.star = False
        t.lexer.counter -= 1
        if t.lexer.counter == 0:
            t.lexer.pop_state()


# finalizamos la cadena cuando volvemos a encontrar otro " y se comprueba si se
# detecto algun \0 para devolver el error, al final se sale de la maquina de estado
def t_STRING_end(t):
    r'"'
    global errors
    if not t.lexer.string_backslashed:
        t.lexer.pop_state()
        if t.lexer.string_containsNull:
            errors.append("(%s, %s) - LexicographicError: String contains null character" % (
                t.lexer.string_nullrow, t.lexer.string_nullcol))
            t.lexer.skip(1)
        else:
            t.value = t.lexer.stringbuf
            t.type = "STRING"
            t.colno = find_column(t.lexer.lexdata, t)
            return t
    else:
        t.lexer.stringbuf += '"'
        t.lexer.string_backslashed = False


# cuando estamos leyendo un comentario multilinea todo lo que veamos lo ignoramos
def t_COMMENT_anything(t):
    r'(.|\n)'
    pass


# cuando estamos leyendo una cadena de caracteres comprobamos cuando aparecen caracteres
# especiales, y agragamos todo a la cadena actual que estamos leyendo
def t_STRING_anything(t):
    r'[^\n]'
    if t.lexer.string_backslashed:
        if t.value == 'b':
            t.lexer.stringbuf += '\b'
        elif t.value == 't':
            t.lexer.stringbuf += '\t'
        elif t.value == 'n':
            t.lexer.stringbuf += '\n'
        elif t.value == 'f':
            t.lexer.stringbuf += '\f'
        elif t.value == '\\':
            t.lexer.stringbuf += '\\'
        elif t.value == '0':
            t_STRING_error(t)
        else:
            t.lexer.stringbuf += t.value
        t.lexer.string_backslashed = False
    else:
        if t.value != '\\':
            t.lexer.stringbuf += t.value
        else:
            t.lexer.string_backslashed = True


t_STRING_ignore = ''


# si se esta leyendo una cadena y se encuentra un \0 se guarda el error y se sigue
# leyendo
def t_STRING_error(t):
    t.lexer.string_containsNull = True
    t.lexer.string_nullrow = t.lineno
    t.lexer.string_nullcol = find_column(t.lexer.lexdata, t) - 1


t_COMMENT_ignore = ''


# para cuando se encuentran caracteres que dan error como \0 se ignoran
def t_COMMENT_error(t):
    t.lexer.counter = 0
    t.lexer.star = False
    t.lexer.lparen = False


# aunque estemos leyendo un comentario se anotan los finales de linea pues despues
# sera necesario en el retorno de errores
def t_COMMENT_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# para cuando se encuentran fines de linea en el codigo
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# aqui se forman los tokens de identificadoes de atributos y de palabras clave,
# notar que como se especifica en COOL los identificadores comienzan con minusculas
def t_ATTRIBUTEID(t):
    r'[a-z][a-zA-Z_0-9]*'
    if reserved.get(t.value.lower()) is None:
        t.type = 'ATTRIBUTEID'
    else:
        t.type = reserved.get(t.value.lower())
    t.colno = find_column(t.lexer.lexdata, t)
    return t


# aqui se forman los tokens de nombres de tipos y de valores booleanos que se encuentran
# en la entrada, pues ambos empiezan en mayusculas
def t_CLASSID(t):
    r'[A-Z][a-zA-Z_0-9]*'
    if reserved.get(t.value.lower()) is None or reserved.get(t.value.lower()) == 'TRUE' or reserved.get(
            t.value.lower()) == 'FALSE':
        t.type = 'CLASSID'
    else:
        t.type = reserved.get(t.value.lower())
    t.colno = find_column(t.lexer.lexdata, t)
    return t


# para devolver la columna de un simbolo pues lexpos es el valor de offset dentro de la
# cadena con el codigo de entrada, entonces hay que buscar el \n proximo por la izquierda
# del simbolo en cuestion y contar la cantidad de caracteres
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# si se encuentran errores de simbolos de entrada que no se han definido en las anteriores
# expresiones regulares, y no es el simbolo de final del texto, entonces retornar el error
# correspondiente
def t_error(t):
    global errors
    if not (t.value[0] == '$' and t.lexpos + 1 == len(t.lexer.lexdata)):
        errors.append(
            '(%s, %s) - LexicographicError: ERROR "%s"' % (t.lineno, find_column(t.lexer.lexdata, t), t.value[0]))
    t.lexer.skip(1)


# esto es para ejecutar el lexer desde compiler.py
def make_lexer(data):
    global errors
    errors = []

    data = data + '$'
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
    lexer.lineno = 1
    return lexer, errors


lexer = lex.lex()
