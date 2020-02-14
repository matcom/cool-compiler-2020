import ply.lex as lex
from ply.lex import TOKEN

class Cool_Lexer(object):

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    keywords = {
        'not': 'NOT',
        'class': 'CLASS',
        'inherits': 'INHERITS',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'fi': 'FI',
        'while': 'WHILE',
        'loop': 'LOOP',
        'pool': 'POOL',
        'let': 'LET',
        'in': 'IN',
        'case': 'CASE',
        'of': 'OF',
        'new': 'NEW',
        'esac': 'ESAC',
        'isvoid': 'ISVOID'
    }

    tokens = [
        # Identifiers
        'TYPE', 'ID',

        # Built-in types
        'INT', 'STRING', 'BOOL',

        # Operators
        'PLUS', 'MUL', 'DIV', 'MINUS', 'LESS', 'LESS_EQ', 'EQ', 'INT_COMP', 'NOT', 'ASSIGN',

        # Literals
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COLON', 'SEMICOLON', 'DOT', 'COMMA', 'CAST',

        # Others
        'ARROW'] + list(keywords.values())

    # Simple rules
    t_PLUS = r'\+'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_MINUS = r'\-'
    t_LESS = r'\<'
    t_LESS_EQ = r'\<\='
    t_EQ = r'\=\='
    t_INT_COMP = r'\~'

    t_ASSIGN = r'\<\-'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COLON = r'\:'
    t_SEMICOLON = r'\;'
    t_DOT = r'\.'
    t_COMMA = r'\,'
    t_CAST = r'\@'

    t_ARROW = r'\=\>'

    @TOKEN(r'[a-z_][A-Za-z_0-9]*')
    def t_ID(self, t):
        if t.value.lower() == 'true':
            t.value = True
            t.type = 'BOOL'
        elif t.value.lower() == 'false':
            t.value = False
            t.type = 'BOOL'
        else:
            t.type = self.keywords.get(t.value.lower(), 'ID')
        return t

    @TOKEN(r'[A-Z][A-Za-z_0-9]*')
    def t_TYPE(self, t):
        t.type = self.keywords.get(t.value.lower(), 'TYPE')
        return t

    @TOKEN(r'\d+')
    def t_INT(self, t):
        t.value = int(t.value)
        return t

    @TOKEN(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t\f\r'
    t_ignore_line_comment = r'\-\-[^\n]*'

    def find_column(self, t):
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        return t.lexpos - line_start + 1

    def t_error(self, t):
        print(f'({t.lexer.lineno}, {self.find_column(t)}) - LexicographicError: "{t.value}"')
        t.lexer.skip(1)


    states = (('COMMENT','exclusive'), ('STRING', 'exclusive'))

    @TOKEN(r'\(\*')
    def t_begin_COMMENT(self, t):
        t.lexer.push_state('COMMENT')
        t.lexer.nesting_level_of_comment = 1

    @TOKEN(r'\(\*')
    def t_COMMENT_nest(self, t):
        t.lexer.nesting_level_of_comment += 1

    @TOKEN(r'\*\)')
    def t_COMMENT_end(self, t):
        t.lexer.nesting_level_of_comment -= 1
        if t.lexer.nesting_level_of_comment == 0:
            t.lexer.pop_state()

    def t_COMMENT_error(self, t):
        t.lexer.skip(1)

    @TOKEN(r'\"')
    def t_begin_STRING(self, t):
        t.lexer.push_state('STRING')
        t.lexer.string_backslashed = False
        t.lexer.stringbuf = ''
        t.lexer.newline_escaped = True

    @TOKEN(r'\n')
    def t_STRING_newline(self, t):
        t.lexer.lineno += 1
        if not t.lexer.newline_escaped:
            t.lexer.skip(1)
        elif not t.lexer.string_backslashed:
            print(f"({t.lexer.lineno - 1}, {self.find_column(t)}) - Lexicographic Error - Newline character not escaped")
            t.lexer.newline_escaped = False
            t.lexer.skip(1)
        else:
            t.lexer.string_backslashed = False

    @TOKEN(r'\"')
    def t_STRING_end(self, t):
        if t.lexer.string_backslashed:
            t.lexer.stringbuf += '"'
            t.lexer.string_backslashed = False
        else:
            t.lexer.pop_state()
            if not t.lexer.newline_escaped:
                t.lexer.skip(1)
            else:
                t.type = "STRING"
                t.value = t.lexer.stringbuf
                return t

    @TOKEN(r'[^\n]')
    def t_STRING_line(self, t):
        if not t.lexer.newline_escaped:
            t.lexer.skip(1)
        elif t.lexer.string_backslashed:
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
        else:
            if t.value == '\\':
                t.lexer.string_backslashed = True
            else:
                t.lexer.stringbuf += t.value

    def t_STRING_error(self, t):
        print(f'({t.lexer.lineno}, {self.find_column(t)}) - LexicographicError: "{t.value}"')
        t.lexer.skip(1)


if __name__ == "__main__":
    cool_lexer = Cool_Lexer()
    data = ''
    input_file = open('input.txt')
    while True:
        data_readed = input_file.read(1024)
        if not data_readed:
            break
        data += data_readed
    cool_lexer.build()

    cool_lexer.lexer.input(data)

    for token in cool_lexer.lexer:
        print(token)
