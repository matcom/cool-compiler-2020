import ply.lex as lex
from ply.lex import TOKEN


class Lexer():
    def __init__(self,
                 debug=False,
                 lextab="lextab",
                 optimize=False,
                 outputdir="",
                 debuglog=None,
                 errorlog=None):

        self.build(debug=debug, lextab=lextab, optimize=optimize, outputdir=outputdir, debuglog=debuglog,
                       errorlog=errorlog)

    @property
    def syntax_tokens(self):
        """
        COOL Syntax Tokens.
        :return: Tuple.
        """
        return (
            # Identifiers
            "ID", "TYPE",

            # Primitive Types
            "INTEGER", "STRING", "BOOLEAN",

            # Literals
            "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", "COMMA", "DOT", "SEMICOLON", "AT",

            # Operators
            "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQ", "LT", "LTEQ", "ASSIGN", "INT_COMP", "NOT",

            # Special Operators
            "ARROW"
        )

    @property
    def keywords(self):
        """
        Map of COOL reserved keywords.
        :return: dict.
        """
        return {
            "case": "CASE",
            "class": "CLASS",
            "else": "ELSE",
            "esac": "ESAC",
            "fi": "FI",
            "if": "IF",
            "in": "IN",
            "inherits": "INHERITS",
            "isvoid": "ISVOID",
            "let": "LET",
            "loop": "LOOP",
            "new": "NEW",
            "of": "OF",
            "pool": "POOL",
            "self": "SELF",
            "then": "THEN",
            "while": "WHILE"
        }

    @property
    def builtin_types(self):
        """
        A map of the built-in types.
        :return dict
        """
        return {
            "Bool": "BOOL_TYPE",
            "Int": "INT_TYPE",
            "IO": "IO_TYPE",
            "Main": "MAIN_TYPE",
            "Object": "OBJECT_TYPE",
            "String": "STRING_TYPE",
            "SELF_TYPE": "SELF_TYPE"
        }

    # Ignore rule for single line comments
    t_ignore_SINGLE_LINE_COMMENT = r"\-\-[^\n]*"

    # SIMPLE TOKENS
    t_LPAREN = r'\('        # (
    t_RPAREN = r'\)'        # )
    t_LBRACE = r'\{'        # {
    t_RBRACE = r'\}'        # }
    t_COLON = r'\:'         # :
    t_COMMA = r'\,'         # ,
    t_DOT = r'\.'           # .
    t_SEMICOLON = r'\;'     # ;
    t_AT = r'\@'            # @
    t_MULTIPLY = r'\*'      # *
    t_DIVIDE = r'\/'        # /
    t_PLUS = r'\+'          # +
    t_MINUS = r'\-'         # -
    t_INT_COMP = r'~'       # ~
    t_LT = r'\<'            # <
    t_EQ = r'\='            # =
    t_LTEQ = r'\<\='        # <=
    t_ASSIGN = r'\<\-'      # <-
    t_NOT = r'not'          # not
    t_ARROW = r'\=\>'       # =>

    @TOKEN(r"(true|false)")
    def t_BOOLEAN(self, token):
        """
        The Bool Primitive Type Token Rule.
        """
        token.value = True if token.value == "true" else False
        return token

    @TOKEN(r"\d+")
    def t_INTEGER(self, token):
        """
        The Integer Primitive Type Token Rule.
        """
        token.value = int(token.value)
        return token

    @TOKEN(r"[A-Z][a-zA-Z_0-9]*")
    def t_TYPE(self, token):
        """
        The Type Token Rule.
        """
        token.type = self.builtin_types.get(token.value, 'TYPE')
        return token

    @TOKEN(r"[a-z_][a-zA-Z_0-9]*")
    def t_ID(self, token):
        """
        The Identifier Token Rule.
        """
        # Check for reserved words
        token.type = self.keywords.get(token.value, 'ID')
        return token

    @TOKEN(r"\n+")
    def t_newline(self, token):
        """
        The Newline Token Rule.
        """
        token.lexer.lineno += len(token.value)

    # Ignore Whitespace Character Rule
    t_ignore = ' \t\r\f'

    # To tokenize input portions who depend on a context/state
    # Examples of such inputs are COOL's string literals and multiple line comments
    # Strings depends on a previous existences of " char as well as comments with (*

    @property
    def states(self):
        return (
            ('STRING',  'exclusive'),
            ('COMMENT', 'exclusive'),
        )

    # STATE OF STRING RECOGNITION
    @TOKEN(r"\"")
    def t_start_string_state(self, token):
        """
        Starts the recognition of a COOL string literal.
        """
        token.lexer.push_state('STRING')
        token.lexer.backslashed = False
        token.lexer.string = ""

    @TOKEN(r"\n")
    def t_STRING_newline(self, token):
        token.lineno += 1
        if not token.lexer.backslashed:
            print("Newline not escaped inside a string")
            token.lexer.skip(1)
        else:
            token.lexer.backslashed = False

    @TOKEN(r"\"")
    def t_STRING_end(self, token):
        
        if not token.lexer.backslashed:
            token.lexer.pop_state()
            token.value = token.lexer.string
            token.type = "STRING"
            return token
        else:
            token.lexer.string += '"'
            token.lexer.backslashed = False

    @TOKEN(r"[^\n]")  # Matches any single character not in brackets
    def t_STRING_anything(self, token):
        
        if token.lexer.backslashed:
            if token.value == 'b':
                token.lexer.string += '\b'
            elif token.value == 't':
                token.lexer.string += '\t'
            elif token.value == 'n':
                token.lexer.string += '\n'
            elif token.value == 'f':
                token.lexer.string += '\f'
            elif token.value == '\\':
                token.lexer.string += '\\'
            else:
                token.lexer.string += token.value
            token.lexer.backslashed = False
        else:
            if token.value != '\\':
                token.lexer.string += token.value
            else:
                token.lexer.backslashed = True


    # STRING ignored characters
    t_STRING_ignore = ''

    # STRING error handler
    def t_STRING_error(self, token):
        print("Illegal character! Line: {0}, character: {1}".format(
            token.lineno, token.value[0]))
        token.lexer.skip(1)

    # STATE OF MULTIPLE LINE COMMENT RECOGNITION
    @TOKEN(r'\(\*')
    def t_start_comment_state(self, token):
        token.lexer.push_state("COMMENT")
        token.lexer.comment_count = 0

    @TOKEN(r'\(\*')
    def t_COMMENT_begin_another_comment(self, token):
        token.lexer.comment_count += 1

    @TOKEN(r'\*\)')
    def t_COMMENT_end(self, token):
        
        if token.lexer.comment_count == 0:
            token.lexer.pop_state()
        else:
            token.lexer.comment_count -= 1

    # COMMENT ignored characters
    t_COMMENT_ignore = ''

    # COMMENT error handler
    def t_COMMENT_error(self, token):
        token.lexer.skip(1)

    def t_error(self, token):
        """
        Error Handling and Reporting Rule.
        """
        print("Illegal character! Line: {0}, character: {1}".format(token.lineno, token.value[0]))
        token.lexer.skip(1)

    def build(self,**kwargs):
        self.last_token = None
        self.reserved = self.keywords.keys()
        self.tokens = self.syntax_tokens + tuple(self.keywords.values())
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self,source_code):
        self.lexer.input(source_code)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def clone(self):
        return self.lexer.clone()

    def __iter__(self):
        return self

    def __next__(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    def next(self):
        return self.__next__()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: ./lexer.py program.cl")
        exit()
    elif not str(sys.argv[1]).endswith(".cl"):
        print("Cool program source code files must end with .cl extension.")
        print("Usage: ./lexer.py program.cl")
        exit()

    input_file = sys.argv[1]
    with open(input_file, encoding="utf-8") as file:
        cool_program_code = file.read()
    
    lexer = Lexer()
    lexer.input(cool_program_code)
    for token in lexer:
        print(token)