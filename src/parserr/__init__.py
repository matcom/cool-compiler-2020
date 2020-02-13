
def setup():
    import os
    from sys import path
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path.append(BASE)

if __name__ == '__main__':
    setup()
