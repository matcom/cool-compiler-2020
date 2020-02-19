from .attribute_dict import AttributeDict
from ..errors import LexicographicError


def process(file_path):
    data = []
    comments = []
    errors = []
    line = 1
    column = 0
    count = 0
    with open(file_path) as file:
        while True:
            char = file.read(1)
            count += 1
            column += 1
            if char == '':
                break
            elif char == '-':
                nchar = file.read(1)
                count += 1
                column += 1
                if nchar == '-':
                    comment = '--' + file.readline()[:-1]
                    count += 1 + len(comment)
                    comments.append(AttributeDict({
                        'line': line,
                        'column': column - 1,
                        'text': comment
                    }))
                    data.append('\n')
                    line += 1
                    column = 0
                else:
                    data.append(char + nchar)
            elif char == '(':
                nchar = file.read(1)
                count += 1
                column += 1
                if nchar == '*':
                    comment = ['(*']
                    sline = line
                    scolumn = column - 1
                    balance = 1
                    while True:
                        if balance == 0:
                            break
                        char = file.read(1)
                        count += 1
                        column += 1
                        if char == '':
                            break
                        elif char == '(':
                            nchar = file.read(1)
                            if nchar == '*':
                                comment.append('(*')
                                count += 1
                                column += 1
                                balance += 1
                            else:
                                file.seek(count)
                        elif char == '*':
                            nchar = file.read(1)
                            if nchar == ')':
                                comment.append('*)')
                                count += 1
                                column += 1
                                balance -= 1
                            else:
                                file.seek(count)
                        else:
                            if char == '\n':
                                line += 1
                                column = 0
                            comment.append(char)
                    if balance != 0:
                        errors.append(LexicographicError(sline, scolumn))
                    comments.append(AttributeDict({
                        'line': sline,
                        'column': scolumn,
                        'text': ''.join(comment)
                    }))
                else:
                    data.append(char + nchar)
            else:
                if char == '\n':
                    line += 1
                    column = 0
                data.append(char)
    return AttributeDict({
        'data': ''.join(data),
        'comments': comments,
        'errors': errors
    })
