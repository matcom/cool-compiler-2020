import itertools


def find_column(lexer, token):
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos)
    return (token.lexpos - line_start) 

def path_to_objet(typex):
    path = []
    c_type = typex

    while c_type:
        path.append(c_type)
        c_type = c_type.parent

    path.reverse()
    return path

def get_common_basetype(types):
    paths = [path_to_objet(typex) for typex in types]
    tuples = zip(*paths)

    for i, t in enumerate(tuples):
        gr = itertools.groupby(t)
        if len(list(gr)) > 1:
            return paths[0][i-1]

    return paths[0][-1]