def find_column(lexer, token):
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos)
    return (token.lexpos - line_start) 
