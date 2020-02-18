#(Row, Col) - ErrorType: Message
ERROR_FORMAT = "(%d, %d) - %s: %s"

#This is bad
LEX_ERRORS = []
PARSER_ERRORS = []

# Compute column.
#     input is the input text string
#     lexpos is a lex position in token instance
def find_column(input, lexpos):
    line_start = input.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1