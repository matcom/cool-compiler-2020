""" Lexer module for COOL Language """

from pipeline import State
from tools.utils import find_column
from tools.cmp_errors import LexicographicError
import ply.lex as lex

class CoolLexer(State):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.lexer = lex.lex(module=self, **kwargs)
        self.balance = 0

    def input(self, raw):
        return self.lexer.input(raw)

    def token(self):
        return self.lexer.token()

    def lineno(self):
        return self.lexer.lineno

    def lexpos(self):
        return self.lexer.lexpos

    def run(self, inputx):
        self.lexer.input(inputx)
        toks = []
        while True:
            t = self.lexer.token()
            if not t:
                break
            toks.append(t)
        return toks

    states = (
        ('comments', 'exclusive'),
        ('str', 'exclusive')
    )

    #       Comments Multiline State
    # ------------------------------------

    def t_comments(self, t):
        r'\(\*'
        self.balance = 1
        t.lexer.begin('comments')

    def t_comments_open(self, t):
        r'\(\*'
        self.balance += 1

    def t_comments_close(self, t):
        r'\*\)'
        self.balance -= 1

        if self.balance == 0:
            t.lexer.begin('INITIAL')

    def t_comments_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_comments_ignore = ' \t\v\f\r'

    # Skip tokens inside comments using error method
    def t_comments_error(self, t):
        t.lexer.skip(1)

    def t_comments_eof(self, t):
        if self.balance > 0:
            self.errors.append(LexicographicError(t.lineno, find_column(t.lexer.lexdata, t.lexpos), "EOF in comment"))

    #          String Matching State 
    # ---------------------------------------

    def t_str(self, t):
        r'\"'
        t.lexer.str_start = t.lexer.lexpos
        t.lexer.begin('str')

    def t_str_end(self, t):
        r'\"'
        t.value = t.lexer.lexdata[t.lexer.str_start:t.lexer.lexpos - 1]
        t.type = 'STRING'
        t.lexer.begin('INITIAL')           
        return t

    t_str_ignore = ''

    def t_str_newline(self, t):
        r'\\\n'
        t.lexer.lineno += 1

    def t_str_consume(self, t):
        r'([^\n\"\\]|\\.)+'
        fnil = t.value.rfind('\0')
        if  fnil != -1:
            self.errors.append(LexicographicError(t.lineno, find_column(t.lexer.lexdata, t.lexpos) + fnil, "String contains null character"))

    def t_str_error(self, t):
        if t.value[0] == '\n':
            self.errors.append(LexicographicError(t.lineno, find_column(t.lexer.lexdata, t.lexpos), "Unterminated string constant"))
            t.lexer.lineno += 1
            t.lexer.skip(1)
            t.lexer.begin('INITIAL')
        else:
            pass

    def t_str_eof(self, t):
        self.errors.append(LexicographicError(t.lineno, find_column(t.lexer.lexdata, t.lexpos), "EOF in string constant")) 

    #              Initial State
    # ---------------------------------------

    # COOL Keywords
    reserved = {
        'class' : 'CLASS',
        'inherits' : 'INHERITS',
        'if' : 'IF',
        'then' : 'THEN',
        'else' : 'ELSE',
        'fi' : 'FI',
        'while': 'WHILE',
        'loop' : 'LOOP',
        'pool' : 'POOL',
        'let' : 'LET',
        'in' : 'IN',
        'case' : 'CASE',
        'of' : 'OF',
        'esac' : 'ESAC',
        'new' : 'NEW',
        'isvoid' : 'ISVOID',
        'not' : 'NOT',
    }

    # Tokens
    tokens = [
        'INTEGER',             # int
        'STRING',              # string
        'BOOL',                # bool
        'PLUS',                # +
        'MINUS',               # -
        'STAR',                # *
        'DIVIDE',              # /
        'BITNOT',              # ~
        'LESS',                # <
        'LESSQ',               # <=
        'EQUALS',              # =
        'WITH',                # =>
        'ASSIGN',              # <-
        'LPAREN',              # (
        'RPAREN',              # )
        'LBRACE',              # {
        'RBRACE',              # }
        'SEMI',                # ;
        'COLON',               # :
        'COMMA',               # ,
        'DOT',                 # .
        'ARROBA',              # @
        'TYPEID',
        'ID',
        'ERROR'
    ] + list(reserved.values())

    #Regular Expressions for Tokens

    # VARS
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_STAR = r'\*'
    t_DIVIDE = r'/'
    t_BITNOT = r'~'
    t_LESS = r'<'
    t_LESSQ = r'<='
    t_EQUALS = r'='
    t_WITH = r'=>'
    t_ASSIGN = r'<-'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEMI = r'\;'
    t_COLON = r'\:'
    t_COMMA = r'\,'
    t_DOT = r'\.'
    t_ARROBA = r'@'

    # METHODS
    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_BOOL(self, t):
        r'(t[Rr][Uu][Ee]|f[Aa][Ll][Ss][Ee])'
        t.value = (t.value.lower() == 'true')
        return t

    def t_TYPEID(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        key = t.value.lower()
        t.type = self.reserved.get(key, 'TYPEID')
        return t

    def t_ID(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        key = t.value.lower() 
        t.type = self.reserved.get(key, 'ID') 
        return t

    # OTHER RULES

    # Line Comments rule
    def t_COMMENT(self, t):
        r"\-\-[^\n]*"
        pass

    # Track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Ignored characters
    t_ignore = ' \t\r\f'

    #Error handling rule
    def t_error(self, t):
        self.errors.append(LexicographicError(t.lineno, find_column(t.lexer.lexdata, t.lexpos), f"ERROR {t.value[0]}"))
        # Generate Error Token
        t.value = t.value[0]
        t.type = 'ERROR'
        t.lexer.skip(1)
        return t