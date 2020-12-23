def dfs_visit(G, v, t, c, d):
    t += 1
    d[v] = t
    c[v] = 1
    for u in G[v]:
        if not G.__contains__(u):
            continue
        if c[u] == 0:
            if dfs_visit(G, u, t, c, d):
                return True
        elif c[u] == 1:
            return True
    c[v] = 2
    return False

def dfs(G, classes):
    '''retorna true si hay ciclo'''
    color = {}
    d = {}
    for c in classes:
        color[c] = 0
        d[c] = -1
    time = 0
    for v in G.keys():
        if color[v] == 0:
            if dfs_visit(G, v, time, color, d):
                return True
    return False

