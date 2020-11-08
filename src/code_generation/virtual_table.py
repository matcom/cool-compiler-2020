class VirtualTable:

    def __init__(self):
        self.classes = {}
        self.methods = {}
        self.attributes = {}

    def add_method(self, A, B, args):
        
        if not A in self.methods:
            self.methods[A] = []
            self.methos[A].append((B, args))
        else:
            add = True
            for name, arguments in self.methods[A]:
                if name == B:
                    if len(args) == len(arguments):
                        differs = False
                        for i in range(0, len(args)):
                            if arg[i] != arguments[i]:
                                differs = True
                                break
                        if not differs:
                            add = False
            if add:
                self.methods[A].append((B, args))                        

        

    def add_attr(self, claSS, args):
        if not claSS in self.attributes:
            self.attributes[claSS] = []
        for arg in args:
            self.attributes[claSS].append(a)

    def get_method_id(self, claSS, method):
        pass

    def get_attributes(self, claSS):
        return self.attributes[claSS]

    def get_attributes_id(self, claSS, attr):
        pass




