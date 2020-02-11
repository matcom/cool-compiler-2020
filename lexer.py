from sly import Lexer

class CommentState(Lexer):
    pass

class Cool_Lexer(Lexer):

    literals = {'+', '-', '*', '/', '~', '<', '(', ')', '{', '}', ',', ';', ':', '.'}

    #A set wich contains all the posible token type names
    tokens = {
        TYPE, ID, INT, STRING, BOOL, LESS_EQ, EQ, CLASS, INHERITS, IF,
        THEN, ELSE, FI, WHILE, LOOP, POOL, LET, IN, CASE, OF, ESAC, NEW,
        ISVOID, ASSIGN, CAST, ARROW, NOT
        }

    #Match rules

    EQ = r'\=\='
    LESS_EQ = r'\<\='
    ASSIGN = r'\<\-'
    ARROW = r'\=\>'
    TYPE = r'[A-Z][a-z_A-Z0-9]*'

    #Identifiers
    ID = r'[a-z_][A-Za-z_0-9]*'

    #Keywords
    ID['not'] =  NOT
    ID['class'] =  CLASS
    ID['inherits'] = INHERITS
    ID['if'] = IF
    ID['then'] = THEN
    ID['else'] = ELSE
    ID['fi'] = FI
    ID['while'] = WHILE
    ID['loop'] = LOOP
    ID['pool'] = POOL
    ID['let'] = LET
    ID['in'] = IN
    ID['case'] = CASE
    ID['of'] = OF
    ID['new'] = NEW
    ID['esac'] = ESAC
    ID['isvoid'] = ISVOID


    @_(r'\d+')
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'(false|true)')
    def BOOL(self, t):
        t.value = True if t.value == 'true' else False
        return t

    ignore_linecomment = r'\-\-[^\n]*'

    #The COMMENT state
    @_(r'\(\*')
    def COMMENT_start(self, t):
        self.push_state(CommentState)
        self.comment_count = 0

    @_(r'\(\*')
    def COMMENT_start_another(self, t):
        self.comment_count += 1

    @_(r'\*\)')
    def COMMENT_end(self, t):
        if self.comment_count == 0:
            self.pop_state()
        self.comment_count -= 1

    #ignore_comment = ''

    def COMMENT_error(self, t):
        self.index += 1

    ignore = ' \t\f\r'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def find_column(self, token):
        last_nl = self.text.rfind('\n', 0, token.index)
        if last_nl < 0:
            last_nl = 0
        column = (token.index - last_nl) + 1
        return column

    def error(self, t):
        print(f'{(self.lineno, self.find_column(t))} - LexicographicError - Bad character: {t.value[0]}')
        self.index += 1




if __name__ == "__main__":
    lexer = Cool_Lexer()
    program_file = open('test.txt')
    program_code = ""
    while True:
        data = program_file.read(1024)
        if not data:
            break
        program_code += data
    for token in lexer.tokenize(program_code):
        print(token)
