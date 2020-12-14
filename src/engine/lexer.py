import ply.lex as lex
from .errors import LexicographicError
from .cp import Token, Grammar

def find_column(lexer, token):
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos)
    return token.lexpos - line_start


class CoolLexer:
    def __init__(self):
        self.CoolGrammar = None
        self.build()
        self.last_token = None # dont touch

    ####### Tokens #######

    keywords = [
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
    ]

    literals = ['+', '-', '*', '/', ':', ';',
                '(', ')', '{', '}', '@', '.', ',']

    tokens = [
        # Identifiers
        'TYPE', 'ID',
        # Primitive data types
        'INTEGER', 'STRING', 'BOOL',
        # Special keywords
        'ACTION',
        # Operators
        'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT',
        'OPAR','CPAR','OCURL','CCURL','COLON','COMMA',
        'DOT', 'SEMI', 'AT','STAR','DIV','PLUS','MINUS'
    ] + list(keywords)
    
    t_ASSIGN = r'\<\-'       # <-
    t_LESS = r'\<'           # <
    t_LESSEQUAL = r'\<\='    # <=
    t_EQUAL = r'\='          # =
    t_INT_COMPLEMENT = r'\~' # ~
    t_ACTION = r'\=\>'       # =>

    t_OPAR = r'\('  # (
    t_CPAR = r'\)'  # )
    t_OCURL = r'\{' # {
    t_CCURL = r'\}' # }
    t_COLON = r'\:' # :
    t_COMMA = r'\,' # ,
    t_DOT = r'\.'   # .
    t_SEMI = r'\;'  # ;
    t_AT = r'\@'    # @
    t_STAR = r'\*'  # *
    t_DIV = r'\/'   # /
    t_PLUS = r'\+'  # +
    t_MINUS = r'\-' # -
   
    ####### Extra Methods #######

    def iskeyword(self, t):
        d = t.value.upper()
        if d in self.keywords:
            t.type = d

    def addline(self, t):
        t.lexer.lineno += len(t.value)

    def find_position(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lineno, (token.lexpos - line_start) + 1)

    def lexer_error(self, t, message):
        self.lexer.errors.append(LexicographicError(
            *self.find_position(t.lexer.lexdata, t), message))

    ##### TOKEN RULES #####

    t_ignore = ' \t\f\r\v'
    t_ignore_single_comment = r'\-\-[^\n]*'

    # count line number
    def t_INITIAL_comment_newline(self, t):
        r'\n+'
        self.addline(t)

    def t_BOOL(self, t):
        r't[rR][uU][eE]|f[aA][lL][sS][eE]'
        d = t.value.lower()
        t.value = True if d == 'true' else False
        return t

    def t_INTEGER(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_TYPE(self, t):
        r'[A-Z][A-Za-z0-9_]*'
        self.iskeyword(t)
        return t

    def t_ID(self, t):
        r'[a-z][A-Za-z0-9_]*'
        self.iskeyword(t)
        return t

    def t_error(self, t):
        self.lexer_error(t, f'ERROR "{t.value}"')
        t.lexer.skip(1)

    
    states = (
        ('string', 'exclusive'),
        ('comment', 'exclusive')
    )

    def t_comment(self, t):
        r'\(\*'
        t.lexer.comments = 1
        #t.lexer.unterminated_slash = False
        t.lexer.begin('comment')

    t_comment_ignore = ''

    def t_comment_opar(self, t):
        r'\(\*'
        t.lexer.comments += 1

    def t_comment_cpar(self, t):
        r'\*\)'
        t.lexer.comments -= 1
        if not t.lexer.comments:
            t.lexer.begin('INITIAL')

    def t_comment_eof(self, t):
        self.lexer_error(t, 'EOF in comment')

    def t_comment_error(self, t):
        #print(t.value, 'error en comment')
        t.lexer.skip(1)

    def t_comment_literals(self, t):
        r'\+|\-|\*|\:|\;|\(|\)|\{|\}|\@|\.|\,|\/|\<|\<\-|\<\=|\=|\~|\=|>'

    # string state
    def t_string(self, t):
        r'\"'
        t.lexer.begin('string')
        t.lexer.string = ''

    t_string_ignore = ''

    def t_string_error(self, t):
        #print(t.value, 'error en string ')
        t.lexer.skip(1)

    def t_string_end(self, t):
        r'\"'
        if not t.lexer.unterminated_slash:
            t.value = t.lexer.string
            t.type = 'STRING'
            t.lexer.begin('INITIAL')
            t.lexer.string = ''
            return t
        else:
            t.lexer.string += '"'
            t.lexer.unterminated_slash = False

    def t_string_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        if not t.lexer.unterminated_slash:
            self.lexer_error(t, 'Unterminated string constant')
        else:
            t.lexer.unterminated_slash = False
            t.lexer.string += '\n'

    def t_string_null(self, t):
        r'\0'
        self.lexer_error(t, 'String contains null character')

    def t_string_slash(self, t):
        r'\\'
        if t.lexer.unterminated_slash:
            t.lexer.string += '\\'
            t.lexer.unterminated_slash = False
        else:
            t.lexer.unterminated_slash = True

    def t_string_eof(self, t):
        self.lexer_error(t, 'EOF in string constant')

    def t_string_all(self, t):
        r'[^\n]'
        if t.lexer.unterminated_slash:
            spec = {'b': '\b', 't': '\t', 'f': '\f', 'n': '\n', '\\':'\\'}
            if t.value in ['b', 't', 'f', 'n', '\\']:
                t.lexer.string += spec[t.value]
            else:
                t.lexer.string += t.value
            t.lexer.unterminated_slash = False
        else:
            t.lexer.string += t.value

    def build(self):
        self.lexer = lex.lex(debug=0, module=self)
        self.lexer.errors = []
        self.lexer.unterminated_slash = False
        self.lexer.string = ''

        ###### CoolGrammar ######
        CoolGrammar = Grammar()
        # terminals
        CoolGrammar.Terminals('class inherits')
        CoolGrammar.Terminals('if then else fi')
        CoolGrammar.Terminals('while loop pool')
        CoolGrammar.Terminals('let in')
        CoolGrammar.Terminals('case of esac')
        CoolGrammar.Terminals('; : , . @ ( ) { } assign action')
        CoolGrammar.Terminals('+ - * / isvoid int_complement')
        CoolGrammar.Terminals('not less lessequal equal')
        CoolGrammar.Terminals('new id type integer string bool')

        self.CoolGrammar = CoolGrammar
        tokens_dict = dict()

        for tok in self.tokens + self.literals:
            if tok not in tokens_dict:
                tokens_dict[tok] = CoolGrammar[tok.lower()]

    ###### TOKENIZER ######

    def token(self):
        if not (self.last_token is None) and self.last_token.token_type==self.CoolGrammar.EOF:
            return None
        token = self.lexer.token()
        if token is None: 
            self.last_token = Token('$', self.CoolGrammar.EOF)
            return None
        else:
            self.last_token = Token(token.value, token.type, *self.find_position(self.lexer.lexdata, token))            
            return self.last_token

    def reset(self):
        self.last_token = None
        
    def tokenize(self, code):
        tokens = []
        self.lexer.input(code)
        while True:
            token = self.token()
            if token is None:
                break
            tokens.append(token)

        # tokens.append(Token('$', self.CoolGrammar.EOF))

        return tokens, self.lexer.errors
    
    def __iter__(self):
        return self

    def __next__(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    def next(self):
        return self.__next__()
