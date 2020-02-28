tokens_collection = ( 
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

class keyword(str):    
    def __eq__(self, other: str):
        val = str(self)        
        if val != 'true' and val != 'false':
            return val  == other.lower()
        return val[0] == other[0] and val[1:] == other.lower()[1:]

basic_keywords = {
    "case": keyword("case"),
    "class": keyword("class"),
    "else": keyword("else"),
    "esac": keyword("esac"),
    "fi": keyword("fi"),
    "if": keyword("if"),
    "in": keyword("in"),
    "inherits": keyword("inherits"),
    "isvoid": keyword("isvoid"),
    "let": keyword("let"),
    "loop": keyword("loop"),
    "new": keyword("new"),
    "of": keyword("of"),
    "pool": keyword("pool"),
    "self": keyword("self"),
    "then": keyword("then"),
    "while": keyword("while"),
    "true": keyword("true"),
    "false": keyword("false") 
}


