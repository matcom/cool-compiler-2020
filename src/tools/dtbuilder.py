

class DerivationTreeNode(object):

    def __init__(self, value, parent=None, h=0):
        self.value = value
        self.children = []
        self.parent = parent
        self._h = h

    # required property to do a pprint of the tree
    @property
    def Deep(self):
        """
        Devuelve la distancia de este nodo al nodo raiz, o el
        nivel en que se encuentra dicho nodo
        """
        return self._h

    def add_node(self, body, count):
        """
        Agrega el cuerpo de una producion a los hijos del nodo cabecera.
        """
        for x in body:
            count += 1
            self.children.append(DerivationTreeNode(x, parent=self, h=count))
        return count

    def graph(self):
        # realizar un recorrido en bfs por el arbol para formar el grafo
        import pydot
        from queue import Queue
        G = pydot.Dot(rankdir='TD', margin=0.1)
        q = Queue()
        q.put(self)
        while not q.empty():
            node = q.get()
            pydotNode = pydot.Node(id(node), label=str(node.value), shape='circle', style='bold')
            G.add_node(pydotNode)
            for child in node.children:
                child_node = pydot.Node(id(child), label=str(child.value), shape='circle', style='bold')
                G.add_node(child_node)
                G.add_edge(pydot.Edge(pydotNode, child_node))
                q.put(child)
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass


def build_derivation_tree(parse: list):
    """
    Dado un conjunto de producciones que generan una cadena,
    devuelve un arbol de derivacion correspondiente a dicho conjunto.
    Este metodo construye el arbol para parsers que produzcan una derivacion extrema
    izquierda, para parsers que producen derivaciones extremas derechas, utilizar
    build_right_derivation_tree()
    """
    count = 0
    q = []
    head = parse[0].Left
    root = DerivationTreeNode(head)
    q.append(root)
    i = 0
    while q:
        node: DerivationTreeNode = q.pop()
        if node.value.IsNonTerminal:
            _, body = parse[i]
            i += 1
            count = node.add_node(body, count)
            for child in node.children[::-1]:
                q.append(child)
    return root


def build_right_derivation_tree(parse: list):
    """
    Dado un conjunto de producciones que generan una cadena,
    devuelve un arbol de derivacion correspondiente a dicho conjunto.
    Este metodo construye el arbol para parsers que produzcan una derivacion extrema
    derecha, para parsers que producen derivaciones extremas izquierdas, utilizar
    build_derivation_tree()
    """
    count = 0
    q = []
    head = parse[0].Left
    root = DerivationTreeNode(head)
    q.append(root)
    i = 0
    while q:
        node: DerivationTreeNode = q.pop()
        if node.value.IsNonTerminal:
            _, body = parse[i]
            i += 1
            count = node.add_node(body, count)
            for child in node.children:
                q.append(child)
    return root
