

class CILNode:
    pass


class CILProgramNode(CILNode):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode


class CILTypeNode(CILNode):
    def __init__(self, cinfo, attrs, methods):
        self.cinfo = cinfo
        self.attrs = attrs
        self.methods = methods

class CILSaveState(CILNode):
    pass

class CILDataNode(CILNode):
    def __init__(self, vname, value):
        self.vname = vname
        self.value = value


class CILFunctionNode(CILNode):
    def __init__(self, finfo, arguments, localvars, instructions):
        self.finfo = finfo
        self.arguments = arguments
        self.localvars = localvars
        self.instructions = instructions


class CILParamNode(CILNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILLocalNode(CILNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILInstructionNode(CILNode):
    pass


class CILAssignNode(CILInstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class CILArithmeticNode(CILInstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class CILPlusNode(CILArithmeticNode):
    pass


class CILMinusNode(CILArithmeticNode):
    pass


class CILStarNode(CILArithmeticNode):
    pass


class CILDivNode(CILArithmeticNode):
    pass


class CILGetAttribNode(CILInstructionNode):
    def __init__(self, dest, source, nattr):
        self.dest = dest
        self.source = source
        self.nattr = nattr


class CILSetAttribNode(CILInstructionNode):
    def __init__(self, dest, nattr, source):
        self.dest = dest
        self.nattr = nattr
        self.source = source


class CILGetIndexNode(CILInstructionNode):
    def __init__(self, dest, array, index):
        self.dest = dest
        self.array = array
        self.index = index


class CILSetIndexNode(CILInstructionNode):
    def __init__(self, array, index, source):
        self.array = array
        self.index = index
        self.source = source


class CILAllocateNode(CILInstructionNode):
    def __init__(self, dest, cinfo):
        self.dest = dest
        self.cinfo = cinfo


class CILArrayNode(CILInstructionNode):
    def __init__(self, dest, size):
        self.dest = dest
        self.size = size


class CILTypeOfNode(CILInstructionNode):
    def __init__(self, dest, var):
        self.dest = dest
        self.var = var


class CILLabelNode(CILInstructionNode):
    def __init__(self, name):
        self.name = name


class CILGotoNode(CILInstructionNode):
    def __init__(self, label):
        self.label = label


class CILGotoIfNode(CILInstructionNode):
    def __init__(self, vinfo, label):
        self.vinfo = vinfo
        self.label = label


class CILStaticCallNode(CILInstructionNode):
    def __init__(self, dest, meth_name):
        self.dest = dest
        self.meth_name = meth_name


class CILDynamicCallNode(CILInstructionNode):
    def __init__(self, dest, ctype, meth_name):
        self.dest = dest
        self.ctype = ctype
        self.meth_name = meth_name


class CILArgNode(CILInstructionNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILReturnNode(CILInstructionNode):
    def __init__(self, value=None):
        self.value = value


class CILLoadNode(CILInstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class CILLengthNode(CILInstructionNode):
    def __init__(self, dest, array):
        self.dest = dest
        self.array = array


class CILConcatNode(CILInstructionNode):
    def __init__(self, dest, array1, array2):
        self.dest = dest
        self.array1 = array1
        self.array2 = array2


class CILPrefixNode(CILInstructionNode):
    def __init__(self, dest, array, n):
        self.dest = dest
        self.array = array
        self.n = n


class CILSubstringNode(CILInstructionNode):
    def __init__(self, dest, array, i, l):
        self.dest = dest
        self.array = array
        self.i = i
        self.l = l


class CILToStrNode(CILInstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class CILReadNode(CILInstructionNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILReadIntNode(CILReadNode):
    pass


class CILReadStrNode(CILReadNode):
    pass


class CILPrintNode(CILInstructionNode):
    def __init__(self, vinfo):
        self.vinfo = vinfo


class CILPrintIntNode(CILPrintNode):
    pass


class CILPrintStrNode(CILPrintNode):
    pass


class CILParentNode(CILInstructionNode):
    def __init__(self, dest, ntype):
        self.dest = dest
        self.ntype = ntype


class CILErrorNode(CILInstructionNode):
    def __init__(self, num = 1):
        self.num = num


class CILLessThan(CILInstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class CILTypeName(CILInstructionNode):
    def __init__(self, dest, nclass):
        self.dest = dest
        self.nclass = nclass

class CILReturnFinal(CILInstructionNode):
    pass