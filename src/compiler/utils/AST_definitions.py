class Node:
    @property
    def clsname(self):
        return str(self.__class__.__name__)

    def to_tuple(self):
        return tuple([
            ("node_class_name", self.clsname)
        ])

    def to_readable(self):
        return "{}".format(self.clsname)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.to_readable())


class NodeProgram(Node):
    def __init__(self, class_list):
        self.class_list = class_list

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname), 
            ("classes", self.class_list)
        ])

    def to_readable(self):
        return "{}(classes={})".format(self.clsname, self.class_list)


class NodeClassTuple(Node, tuple):
    def __init__(self, classes):
        self.classes = classes

    

class NodeClass(Node):
    def __init__(self, idName, body, parent):
        self.idName = idName
        self.body = body
        self.parent = parent

    def to_readable(self):
        return "{}(name='{}', parent={}, features={})".format(
            self.clsname, self.idName, self.parent, self.body)



#No se si poner aqui una clase para heredar , que sea feature_class.
#Tengo que ver si a futuro necesito iterar por los elementos de una clase
#de manera abstracta.
class NodeClassMethod(Node):
    def __init__(self, idName, formal_params, return_type, body):
        self.idName = idName
        self.formal_params = formal_params
        self.return_type = return_type
        self.body = body

#Yo puedo crear un bosquejo inicial, 
# y después reutilizarlo en lo subsiguiente?
class NodeAttr(Node):
    def __init__(self, idName, attr_type, expr):
        self.idName = idName
        self.attr_type = attr_type
        self.expr = expr


