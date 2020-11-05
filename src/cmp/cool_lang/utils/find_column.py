def find_column(input, lexpos):
    line_start = input.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1
