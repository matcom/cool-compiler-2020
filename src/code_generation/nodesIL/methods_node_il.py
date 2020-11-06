from .node_il import NodeIL

class LabelIL(NodeIL):
    
    def __init__(self, first, second, func):
        self.label = first + '_' + second
        self.first = first
        self.second = second
        self.func = func

    def __str__(self):
        return 'label {}:'.format(self.label)

class GotoIL(NodeIL):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return "goto {}".format(self.label)

class IfJumpIL(NodeIL):
    
    def __init__(self, var, label):
        self.var = var
        self.label = label

    def __str__(self):
        return 'if {} goto {}'.format(self.var, self.label)

class PopIL(NodeIL):
    
    def __init__(self, size):
        self.size = size
    
    def __str__(self):
        return 'pop {}'.format(self.size)

class PushIL(NodeIL):
    
    def __init__(self, value):
        self.value(value)
    
    def __str__(self):
        return 'push {}'.format(self.value)

class ReturnIL(NodeIL):
    
    def __str__(self):
        return 'return\n'

class StringIL(NodeIL):
    
    def __init__(self):
        pass
    
    def __str__(self):
        pass

class PrintIL(NodeIL):
    
    def __init__(self, string):
        self.string = string
    
    def __str__(self):
        return 'print {}'.format(self.string)

class CommentIL(NodeIL):
    
    def __init__(self, text):
        self.text = text
    
    def __str__(self):
        return '#' + self.text

class HierarchyIL(NodeIL):
    def __init__(self):
        pass
    
    def __str__(self):
        pass

class InheritIL(NodeIL):
    def __init__(self):
        pass
    
    def __str__(self):
        pass

class VirtualTableIL(NodeIL):
    def __init__(self):
        pass

    def __str__(self):
        pass

class DispatchIL(NodeIL):
    def __init__(self):
        pass
    
    def __str__(self):
        pass

class DispatchParentIL(ILNode):
    def __init__(self):
        pass


    def __str__(self):
        pass