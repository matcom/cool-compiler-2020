import ply.lex as lex
from ply.lex import TOKEN

class Cool_Lexer(object):

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


    literals = {'+', '-', '*', '/', '~', '<', '(', ')', '{', '}', ',', ';', ':', '.', '@'}


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

    tokens = ['TYPE', 'ID', 'INT', 'STRING', 'BOOL', 'LESS_EQ', 'EQ', 'ASSIGN', 'ARROW'] + list(keywords.values())

    @TOKEN(r'[a-z_][A-Za-z_0-9]*')
    def t_ID(self, t):
        t.type = self.keywords.get(t.value, 'ID')
        return t

    @TOKEN(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t\f\r'

    def find_column(self, t):
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        return t.lexpos - line_start + 1


    def t_error(self, t):
        print(f"({t.lexer.lineno}, {self.find_column(t)}) - LexicographicError: Illegal character")
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

