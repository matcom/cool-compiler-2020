def get_token(node):
    for attr in ['tid', 'token', 'ttype', 'symbol']:
        if hasattr(node, attr):
            return getattr(node, attr)
    raise Exception(f'{node} has no token')
