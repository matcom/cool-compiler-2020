'''
Process a source file removing coments.
Because coments in COOL can be nested, there is
no regular expresion to represet them, so we have
to preprocess the file and strip them out.
'''


def find_comments(program: str) -> str:
    '''
    This functions detects every comment in a Cool program\
    and replace it with empty lines. This is done in a way\
    so is posible for the other components of the\
    compiler to correctly detect errors on exact Line and\
    Column.\
    In Cool a comment can be of the form (*...*) or -- ending\
    with a newline. Comments can be nested, so there is no regular\
    expression to detect them.
    '''
    pairs = []
    stack = []
    line = 1
    column = 1
    program = list(program)
    iter_char = iter(enumerate(program))
    while 1:
        try:
            i, char = next(iter_char)
            column += 1
            if char == '\n':
                line += 1
                column = 1
            elif char == '(':
                i, char = next(iter_char)
                column += 1
                if char == '*':
                    stack.append(i - 1)
                elif char == '\n':
                    line += 1
                    column = 1
            elif char == '*':
                i, char = next(iter_char)
                column += 1
                if char == ')':
                    first = stack.pop()
                    pairs.append((first, i))
                elif char == '\n':
                    line += 1
                    column = 1
        except StopIteration:
            break
    assert not stack, "(%d, %d) - LexicographicError: EOF in comment" % (
        line, column)
    iter_char = iter(enumerate(program))
    column = 1
    line = 1
    while 1:
        try:
            i, char = next(iter_char)
            column += 1
            if char == '-':
                i, char = next(iter_char)
                column += 1
                if char == '-':
                    stack.append(i - 1)
                elif char == '\n':
                    if stack:
                        first = stack.pop()
                        pairs.append((first, i))
                    column = 1
                    line += 1
            elif char == '\n':
                if stack:
                    first = stack.pop()
                    pairs.append((first, i))
                column = 1
                line += 1
        except StopIteration:
            break
    while pairs:
        i, j = pairs.pop()
        for k in range(i, j + 1):
            if not program[k] == '\n':
                program[k] = ' '
    return ''.join(program)
