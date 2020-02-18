def process(file_path):
    comments = []
    data = []
    line = 0
    with open(file_path) as file:
        while True:
            char = file.read(1)
            if char == '':
                break
            if char == '-':
                nchar = file.read(1)
                if nchar == '-':
                    comment = file.readline()[:-1]
                    comments.append((line, comment))
                    data.append('\n')
                    line += 1
                else:
                    data.append(char); data.append(nchar)
            if char == '(':
                nchar = file.read(1)
                if nchar == '*':
                    comment = ['(*']
                    sline = line
                    balance = 1
                    while True:
                        pass
                    comments.append((sline, ''.join(comment)))
                else:
                    data.append(char); data.append(nchar)
            else:
                if char == '\n':
                    line += 1
                data.append(char)
    data = ''.join(data)
    return data, comments
