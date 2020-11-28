class VirtualTable:

    def __init__(self):
        self.classes = {}
        self.methods = {}
        self.attributes = {}

    def add_method(self, A, B, args):
        
        if not A in self.classes:
            self.classes[A] = []
        if not A in self.attributes:
            self.attributes[A] = []
        if not A in self.methods:
            self.methods[A] = []
            self.methods[A].append((B, args))
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

    def get_index(self, c):
        # print('classes', self.classes.keys())
        return len(self.attributes[c]) + 1

    def add_attr(self, claSS, args):
        if not claSS in self.attributes:
            self.attributes[claSS] = []
        for arg in args:
            self.attributes[claSS].append(a)

    def get_method_id(self, claSS, method):
        if claSS in self.methods.keys():
            for i in range(len(self.methods[claSS])):
                b, args = self.methods[claSS][i]
                if b == method:
                    return claSS + '.' + method
        print('VT: class: {} method: {}'.format(claSS, method))
        return -1

    def get_attributes(self, claSS):
        return self.attributes[claSS]

    def get_attributes_id(self, claSS, attr):
        attrs = self.attributes[claSS]
        for i in range(len(attrs)):
            if attr == attrs[i]:
                return i + 1
        return -1



