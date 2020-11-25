import visitor

class MipsNode:
    pass

class MipsProgramNode(MipsNode):
    def __init__(self, dotdata, dotcode):
        self.dotdata = dotdata
        self.dotcode = dotcode

# string
class MipsStringNode(MipsNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class MipsWordNode(MipsNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

# jumps
class MipsJumpNode(MipsNode):
    def __init__(self, label):
        self.label = label

class MipsJumpAtAddressNode(MipsJumpNode):
    pass

class MipsJRNode(MipsJumpNode):
    pass

# stack
class MipsLWNode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest

class MipsLINode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest

class MipsLANode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest

class MipsSWNode(MipsNode):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest



# syscall
class MipsSyscallNode(MipsNode):
    pass


# move
class MipsMoveNode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest


# arithmetic
class MipsAddNode(MipsNode):
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

class MipsAddiuNode(MipsNode):
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

# label
class MipsLabelNode(MipsNode):
    def __init__(self, name):
        self.name = name

class MipsCommentNode(MipsNode):
    def __init__(self, comment):
        self.comment = '\n #' + comment + '\n'

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(MipsProgramNode)
        def visit(self, node):
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.data\n{dotdata}\n\n.text\n{dotcode}'

        @visitor.when(MipsStringNode)
        def visit(self, node):
            return f'{node.name}:     .asciiz      "{node.value}"'

        @visitor.when(MipsWordNode)
        def visit(self, node):
            return f'{node.name}:     .word     {node.value}'

        # jumps
        @visitor.when(MipsJumpNode)
        def visit(self, node):
            return f'j {node.label}'

        @visitor.when(MipsJumpAtAddressNode)
        def visit(self, node):
            return f'jal {node.label}'

        @visitor.when(MipsJRNode)
        def visit(self, node):
            return f'jr {node.label}'

        # stack
        @visitor.when(MipsLWNode)
        def visit(self, node):
            return f'lw {node.dest}, {node.src}'

        @visitor.when(MipsLINode)
        def visit(self, node):
            return f'li {node.dest}, {node.src}'

        @visitor.when(MipsLANode)
        def visit(self, node):
            return f'la {node.dest}, {node.src}'

        @visitor.when(MipsSWNode)
        def visit(self, node):
            return f'sw {node.src}, {node.dest}'


        # syscall
        @visitor.when(MipsSyscallNode)
        def visit(self, node):
            return 'syscall'


        # move
        @visitor.when(MipsMoveNode)
        def visit(self, node):
            return f'move {node.dest}, {node.src}'


        # arithmetic
        @visitor.when(MipsAddNode)
        def visit(self, node):
            return f'add {node.param1}, {node.param2}, {node.param3}'

        @visitor.when(MipsAddiuNode)
        def visit(self, node):
            return f'addiu {node.param1}, {node.param2}, {node.param3}'


        # label
        @visitor.when(MipsLabelNode)
        def visit(self, node):
            return f'{node.name}:'
        
        @visitor.when(MipsCommentNode)
        def visit(self, node):
            return node.comment

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))