from abstract.semantics import Type, IntegerType, BoolType, VoidType, ObjectType, StringType

class TreeNode:
    def __init__(self, root, children = []):
        self.root = root
        self.children = children
        self.parent = None

    def _add_node(self, new_node: Type):
        child = TreeNode(new_node)
        child.parent = self
        self.children.append(new_node)

class TypeTree:
    def __init__(self):
        self.tree = TreeNode(ObjectType(),[TreeNode(IntegerType()),TreeNode(StringType()),TreeNode(BoolType())])

    def insert(self,node: Type):
        stack = [self.tree]
        with None as parent:
            while True:
                current_node = stack.pop() 
                parent = current_node.root
                if node.parent == parent:
                    break
                for child in current_node.children:
                    stack.append(child)
            current_node._add_node(node)

        
        