class State(object):
    def __init__(self, name):
        self.name = name
        self.stop = False
        self.errors = []

    def run(self, inputx):
        # Put errors in self.errors and use pipeline report function to print errors
        pass