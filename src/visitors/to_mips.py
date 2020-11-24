import os
from code_generation import *
import visitors.visitor as visitor

class MIPS:
    def __init__(self, il_code, il_data,):
        self.code = []
        self.data = []
        self.il_code = il_code
        self.il_data = il_data

    def _loadfrom(self, file):
        fd = open(file)
        return fd.read()

    def start(self):
        code = ""
        code += ".data\n"
        code += "buffer:\n"
        code += ".space 65536\n"
        code += "\n"

        for node in self.il_data:
            self.visit(node)

        for c in self.data:
            code += (c)

        code += "\n.globl main\n"
        code += ".text\n"

        code += self._loadfrom(os.path.join('code_generation/statics', 'IO.s'))
        code += self._loadfrom(os.path.join('code_generation/statics', 'Object.s'))
        code += self._loadfrom(os.path.join('code_generation/statics', 'String.s'))
        code += self._loadfrom(os.path.join('code_generation/statics', 'inherit.s'))

        for c in self.il_code:
            self.visit(c)

        code += "li $v0, 10\n"
        code += "syscall\n"

        return code

    @visitor.on('node')
    def visit(self, node):
        pass

    #operations

    @visitor.when(BinaryOperationIL)
    def visit(self, node):
        self.code.append("lw $a0, " + str(node.leftOp) + "\n")
        self.code.append("lw $a1, {}($sp)".format(-4 * node.rightOp))

        if node.symbol == '+':
            self.code.append("add $a0, $a0, $a1\n")
        elif node.symbol == '-':
            self.code.append("sub $a0, $a0, $a1\n")
        elif node.symbol == '*':
            self.code.append("mult $a0, $a1\n")
            self.code.append("mflo $a0\n")
        elif node.symbol == '/':
            self.code.append("div $a0, $a1\n")
            self.code.append("mflo $a0\n")
        elif node.symbol == '=':
            self.code.append("seq $a0, $a0, $a1\n")
        elif node.symbol == '>':
            self.code.append("li $a2, 1\n")
            self.code.append("add $a1, $a1, $a2\n")
            self.code.append("sge $a0, $a0, $a1\n")
        elif node.symbol == '>=':
            self.code.append("sge $a0, $a0, $a1\n")
        elif node.symbol == '<=':
            self.code.append("add $a0, $a1, $a0\n")
        elif node.symbol == '<':
            self.code.append("li $a2, 1\n")
            self.code.append("add $a0, $a0, $a2\n")
            self.code.append("sge $a0, $a1, $a0\n")
        self.code.append("sw $a0, {}($sp)\n".format(-4*node.var))

    @visitor.when(UnaryOperationIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4*node.op))
        
        if node.symbol == '~':
            self.code.append("not $a0, $a0\n")
        else:
            self.code.append("li $a1, 1\n")
            self.code.append("sub $a0, $a1, $a0\n")
        self.code.append("sw $a0, {}($sp)\n".format(-4 * node.var))
    #allocate

    @visitor.when(AllocateIL)
    def visit(self, node):
        self.code.append("li $v0, 9\n")
        self.code.append("li $a0, {}\n".format(4*node.size))
        self.code.append("syscall\n")
        self.code.append("sw $v0, {}($sp)\n".format(-4*node.var))
        self.code.append("la $a1, {}_VT\n".format(node.typ))
        self.code.append("sw $a1, ($v0)\n")

    #assignment
    @visitor.when(VarToVarIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4 * node.right))
        self.code.append("sw $a0, {}($sp)\n".format(-4 * node.left))

    @visitor.when(VarToMemoIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4*node.right))
        self.code.append("lw $a1, {}($sp)\n".format(-4*node.left))
        self.code.append("sw $a0, {}($a1)\n".format(4*node.offset))

    @visitor.when(MemoToVarIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4 * node.right))
        self.code.append("lw $a1, {}($a0)\n".format(4*node.offset))
        self.code.append("sw $a1, {}($sp)\n".format(-4*node.left))

    @visitor.when(ConstToMemoIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4 * node.left))
        self.code.append("li $a1, {}\n".format(node.right))
        self.code.append("sw $a1, {}($a0)\n".format(4*node.offset))

    #methods
    @visitor.when(LabelIL)
    def visit(self, node):
        self.code.append(node.label + ':\n')
        if node.func:
            self.code.append("sw $ra, ($sp)\n")
            self.code.append("addiu $sp, $sp, 4\n")


    @visitor.when(GotoIL)
    def visit(self, node):
        self.code.append("j " + node.label + "\n")

    @visitor.when(CommentIL)
    def visit(self, node):
        self.code.append(str(node))

    @visitor.when(IfJumpIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4 * node.var))
        self.code.append("bnez $a0, " + node.label + "\n")

    @visitor.when(HierarchyIL)
    def visit(self, node):
        self.data.append(node.node + "_INH:\n")
        self.data.append(".word {}_INH\n".format(node.parent))

    @visitor.when(VirtualTableIL)
    def visit(self, node):
        self.data.append(node.name + "_VT:\n")
        self.data.append(".word {}_INH\n".format(node.name))
        
        for m in node.methods:
            self.data.append(".word " + str(m) + "\n")

    @visitor.when(PushIL)
    def visit(self, node):
        self.code.append("li $a0, {}\n".format(node.value))
        self.code.append("sw $a0, ($sp)\n")
        self.code.append("addiu $sp, $sp, 4\n")

    @visitor.when(PopIL)
    def visit(self, node):
        self.code.append("addiu $sp, $sp, " + str(-4*node.size) + "\n")


    @visitor.when(ReturnIL)
    def visit(self, node):
        self.code.append("lw $v0, -4($sp)\n")
        self.code.append("addiu $sp, $sp, -4\n")
        self.code.append("lw $ra, -4($sp)\n")
        self.code.append("addiu $sp, $sp, -4\n")
        self.code.append("jr $ra\n")

    @visitor.when(DispatchIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4 * node.obj))
        self.code.append("lw $a0, ($a0)\n")
        self.code.append("addiu $a0, $a0, {}\n".format(-4 * node.offset))
        self.code.append("lw $v0, ($a0)\n")
        self.code.append("jalr $ra, $v0\n")
        self.code.append("sw $v0, {}($sp)\n".format(-4 * node.result))


    @visitor.when(DispatchParentIL)
    def visit(self, node):
        self.code.append("la $v0, " + node.method + "\n")
        self.code.append("jalr $ra, $v0\n")
        self.code.append("sw $v0, {}($sp)".format(-4 * node.result))

    @visitor.when(InheritIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(-4 * node.child))
        self.code.append("la $a1, " + node.parent + "\n")
        self.code.append("la $t0, inherit\n")
        self.code.append("jalr $ra, $t0\n")
        self.code.append("sw $v0, {}($sp)\n".format(-4*node.result))

    @visitor.when(StringIL)
    def visit(self, node):
        self.data.append("{}: .asciiz {}\n".format(node.label, node.string))

    @visitor.when(PrintIL)
    def visit(self, node):
        if node.string:
            self.code.append("la $t0, _out_string\n")
        else:
            self.code.append("la $t0, _out_in\n")
        self.code.append("jalr $ra, $t0\n")

    @visitor.when(LoadLabelIL)
    def visit(self, node):
        self.code.append("la $a0, " + node.label + "\n")
        self.code.append("sw $a0, {}($sp)\n".format(-4 * node.var))