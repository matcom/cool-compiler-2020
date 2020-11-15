from .node_il import NodeIL

class LabelIL(NodeIL):
    
    def __init__(self, first, second, func):
        self.label = first + '_' + second
        self.first = first
        self.second = second
        self.func = func

    def __str__(self):
        return 'label {}:'.format(self.label)

class LoadLabelIL(NodeIL):
    def __init__(self, var, label):
        self.var = var
        self.label = label
    
    def __str__(self):
        return "load: {} to {}".format(self.label, str(self.var))

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
    
    def __init__(self, value = 0, case = 1):
        self.value = value
        self.case = case
    
    def __str__(self):
        if self.value:
            return 'push {}'.format(self.value)
        return 'push'    

class ReturnIL(NodeIL):
    
    def __str__(self):
        return 'return\n'

class StringIL(NodeIL):
    
    def __init__(self, label, string):
        self.label = label
        self.string = string
    
    def __str__(self):
        return "{}: {}".format(self.label,self.string)

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
    
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
    
    def __str__(self):
        return "type {} descendant of {}".format(self.node, self.parent)

class InheritIL(NodeIL):
    
    def __init__(self, child, parent, result):
        self.child = child
        self.parent = parent
        self.result = result
    
    def __str__(self):
        return "child {} inherits parent {}".format(self.child, self.parent)

class VirtualTableIL(NodeIL):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def __str__(self):
        to_return = ''
        to_return += 'VirtualTable: ' + self.name + '\n'
        to_return += '------Methods---------\n'
        for m in self.methods:
            to_return += m + '\n'
        return to_return

class DispatchIL(NodeIL):
    
    def __init__(self, obj, offset, result):
        self.obj = obj
        self.offset = offset
        self.result = result
    
    def __str__(self):
        return "dispatch: object({}).method({}) to {}".format(self.obj,self.offset,self.result)

class DispatchParentIL(ILNode):
    
    def __init__(self, obj, method, result):
        self.method = method
        self.result = result
        self.obj = obj


    def __str__(self):
        return "dispatch_parent: method {} with_obj {} in {}".format(self.method, self.obj, self.result)
