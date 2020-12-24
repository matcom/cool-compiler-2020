###################################################################
###############             CIL TREE             ##################
###################################################################
#The cilnodes have inside all that they need to transform to misp
class CilNode:
    def __init__(self, code=""):
        self.code = code

class CilClassNode(CilNode):
    def __init__(self, name, attrs=None, funcs=None, size=-1, code=""):
        super().__init__(code)
        self.name = name
        self.attr_order = []
        self.attrs = attrs # [<var_name>] -> CilIdNode
        self.funcs = funcs # ["A_f"] -> CilFuncNode

class CilFuncDeclNode(CilNode):
    def __init__(self, label, body=None, formals=None, local_vars=None, retvalue=0, code = ""):
        super().__init__(code)
        self.label = label
        self.formals = formals
        self.locals = local_vars #List of instructions locals
        self.body = body #List of instructions
        self.retvalue = retvalue #rreturn value

class CilFormalNode(CilNode):
    def __init__(self, name, code=""):
        super().__init__(code)
        self.name = name

class CilParamNode(CilNode):
    def __init__(self, name, code=""):
        super().__init__(code)
        self.name = name

class CilBackupNode(CilNode):
    def __init__(self, name, code=""):
        super().__init__(code)
        self.name = name

class CilRestoreNode(CilNode):
    def __init__(self, name, code=""):
        super().__init__(code)
        self.name = name

class CilGetAttrNode(CilNode):
    def __init__(self, instance, attr, result, code=""):
        super().__init__(code)
        self.instance = instance
        self.attr = attr
        self.result = result

class CilCallNode(CilNode):
    def __init__(self, func_label, value, code=""):
        super().__init__(code)
        self.func_label = func_label
        self.value = value

class CilCondNode(CilNode):
        def __init__(self, condvar, goto_label, code = ""):
            super().__init__(code)
            self.condvar = condvar
            self.goto_label = goto_label

class CilGoToNode(CilNode):
        def __init__(self, label, code=""):
            super().__init__(code)
            self.label = label

class CilLabelNode(CilNode):
        def __init__(self, name, code=""):
            super().__init__(code)
            self.name = name + ":"

class CilLoopNode(CilNode):
        def __init__(self, condvar, label, code=""):
            super().__init__(code)
            self.condvar = condvar
            self.label = label

class CilDeclNode(CilNode):
    def __init__(self, local_name, value, code=""):
        super().__init__(code)
        self.local_name = local_name
        self.value = value

class CilAssignNode(CilNode):
    def __init__(self, lvalue, expr=None, code=""):
        super().__init__(code)
        self.lvalue = lvalue
        self.expr = expr

# ########################################################################################
# #####################   UNOPS  ########################################################
# ########################################################################################
class CilUnOpNode(CilNode):
    # op param is just for building self.code
    def __init__(self, operand, result, op=None):
        self.operand = operand
        self.result = result
        self.op = op
        self.code = result + " = " + op + " " + str(operand)

class CilBooleanNotNode(CilUnOpNode):
    def __init__(self, operand, result):
        super().__init__(operand, result, "not")

class CilIsVoidNode(CilUnOpNode):
    def __init__(self, operand, result):
        super().__init__(operand, result, "isvoid")

class CilBinaryNotNode(CilUnOpNode):
    def __init__(self, operand, result):
        super().__init__(operand, result, "~")

# ########################################################################################
# #####################   BINOPS  ########################################################
# ########################################################################################

class CilBinOpNode(CilNode):
    # op param is just for building self.code
    def __init__(self, left, right, result, op=None):
        self.left = left
        self.right =right
        self.result = result
        self.op = op
        self.code = result + " = " + str(left) + " " + op + " " + str(right)

class CilSumNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, "+")

class CilMinusNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, "-")

class CilMultNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, "*")

class CilDivNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, "/")

class CilCmpLessNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, "<")

class CilCmpLessEqNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, "<=")

class CilCmpEqRefNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, add_result, "==")

class CilCmpEqNode(CilBinOpNode):
    def __init__(self, left, right, result):
        super().__init__(left, right, result, "=")

# ########################################################################################
# #####################   TERMINALS  #####################################################
# ########################################################################################

class CilStringNode(CilNode):
    # Ex: .data <str_label>: .asciiz "Hello World!"
    def __init__(self, label, addr):
        self.label = label
        self.addr = addr

class CilAllocateNode(CilNode):
    def __init__(self, typename, value, code=""):
        self.code = "ALLOCATE {}".format(typename)
        self.typename = typename
        self.value = value

class CilSetAttrNode(CilNode):
    def __init__(self, instance, attr, value, code=""):
        self.code = "SETATTR {} {} {}".format(instance, attr, value)
        self.instance = instance
        self.attr = attr
        self.value = value

