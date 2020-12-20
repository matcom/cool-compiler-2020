def replace_tabs(_input, tabstop= 4):
    result = ''
    for c in _input:
        if c =='\t':
            result += ' ' * 4
        else:
            result += c
    return result