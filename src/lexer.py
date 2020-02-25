import ply.lex as lex
import re

class CoolLexer:

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
        'ASSIGN',
        'LESS',
        'LESSEQUAL',
        'EQUAL',
        'INT_COMPLEMENT',
        'NOT'
    ]

     #list of token names
    tokens = [
        'INTEGER',
        'STRING',
        'BOOL',
        'TYPE',
        'OBJECT',
        'SPECIAL'
     ] + operators + keywords

    #list of errors
    errors = []

    #regular expression rule for comment
    def t_comment(self, t):
        r'--.*'
        pass
    
    #regular expresion rule for operations
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MULT = r'\*'
    t_DIV = r'\/'
    t_ASSIGN = r'<-'
    t_LESS = r'<'
    t_LESSEQUAL = r'<='
    t_EQUAL = r'='
    t_INT_COMPLEMENT = r'~'
    t_NOT = r'[Nn][Oo][Tt]'

    #regular expresion rule for keywords
    def check_keyword(self, t):
        t_upper = t.value.upper()

        if t_upper in self.keywords:
            t.type = t.upper

        return t

    #regular expresion rule for bool
    def t_BOOL(self, t):
        r't[Rr][Uu][Ee]|f[Aa][Ll][Ss][Ee]'
        
        t.value = True if t.value.upper() == "TRUE" else False
        return t

    #regular expresion rule for integer
    def t_INTEGER(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    #regular expresion rule for type
    def t_TYPE(self, t):
        r'[A-Z][0-9A-Za-z_]*|self|SELF_TYPE'
        return t

    #regular expresion rule for object
    def t_OBJECT(self, t):
        r'[a-z][0-9A-Za-z_]*'
        return t

    #regular expresion rule for special
    def t_SPECIAL(self, t):
        r'\(|\)|{|}|\.|;|,|:|@|=>'
        return t

    #others regular expresions
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        pass
        
    def t_skip(self, t):
        r'[ \t\r\f]+'
        pass

    #regular expresion rules for string
    states = (
        ("STRING", "exclusive"),
    )

    def t_start_string(self, t):
        r"\""
        t.lexer.push_state("STRING")
        t.lexer.string_backslashed = False
        t.lexer.stringbuf = ""

    def t_STRING_newline(self, t):
        r"\n"
        t.lexer.lineno += 1
        if not t.lexer.string_backslashed:
            self.errors.append("({0}, {1}) - LexicographicError: 'Unterminated string constant'".format(t.lineno, self.find_column(self.data, t)))
            t.lexer.pop_state()
        else:
            t.lexer.string_backslashed = False

    def t_STRING_null(self, t):
        r"\0"
        self.errors.append("({0}, {1}) - LexicographicError: 'Null character in string'".format(t.lineno, self.find_column(self.data, t)))
        t.lexer.skip(1)

    def t_STRING_end(self, t):
        r"\""
        if not t.lexer.string_backslashed:
            t.lexer.pop_state()
            t.value = t.lexer.stringbuf
            t.type = "STRING"
            return t
        else:
            t.lexer.stringbuf += '"'
            t.lexer.string_backslashed = False

    def t_STRING_anything(self, t):
        r"[^\n]"
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
            else:
                t.lexer.stringbuf += t.value
            t.lexer.string_backslashed = False
        else:
            if t.value != '\\':
                t.lexer.stringbuf += t.value
            else:
                t.lexer.string_backslashed = True

    # STRING ignored characters
    t_STRING_ignore = ''

    # STRING error handler
    def t_STRING_error(self, t):
        self.errors.append("({0}, {1}) - LexicographicError: 'ERROR at or near {2}'".format(t.lineno, self.find_column(self.data, t), t.value[:10]))
        t.lexer.skip(1)

    def t_STRING_eof(self, t):
        self.errors.append("({0}, {1}) - LexicographicError: 'EOF in string'".format(t.lineno, self.find_column(self.data, t)))
        t.lexer.pop_state()
    

    #regular expresion rule for error
    def t_error(self, t):
        self.errors.append("({0}, {1}) - LexicographicError: ' UNKNOW character {2}'".format(t.lineno, self.find_column(self.data, t), t.value[0]))
        t.lexer.skip(1)
        pass


    #build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.data = data
        self.lexer.input(self.pre_proc(data))

        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            tokens.append(tok)
        
        return (tokens, self.errors)

    #### utils
    def find_column(self, text, token):
        line_start = text.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def pre_proc(self, text):
        text_ret = ''
        comments = 0
        idx = 0

        lineno = 1
        last_nidx = 0

        while idx < len(text):
            if text[idx] == '\n':
                lineno = lineno + 1
                last_nidx = idx

            if text[idx] == '(' and idx + 1 < len(text) and text[idx+1] == '*':
                comments = comments+1
                idx = idx + 1
                text_ret = text_ret + '  '

            elif text[idx] == '*' and idx+1 < len(text) and text[idx+1] == ')' and comments > 0:
                comments = comments - 1
                idx = idx + 1
                text_ret = text_ret + '  '

            elif comments == 0:
                text_ret = text_ret + text[idx]

            else:
                if text[idx] == '\n':
                    text_ret = text_ret + '\n'
                else:
                    text_ret = text_ret + ' '

            idx = idx +1
        
        if comments > 0:
            self.errors.append("({0}, {1}) - LexicographicError: 'EOF in comment'".format(lineno, idx - last_nidx))

        return text_ret