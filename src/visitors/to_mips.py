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

        self.code.append(".data\n")
        self.code.append("buffer: .space 2048\n")
        self.code.append("strsubstrexception: .asciiz \"{}\"\n".format("Substring index exception"))
        self.code.append("\n")



        for node in self.il_data:
            self.visit(node)
        
        self.code.append("Object_INH:\n")
        for c in self.data:
            self.code.append(c)

        self.code.append("\n.globl main\n")
        self.code.append(".text\n")
        
        self.code.append(self._loadfrom(os.path.join('code_generation/statics', 'IO.s')) + "\n")
        self.code.append(self._loadfrom(os.path.join('code_generation/statics', 'Object.s')) + "\n")
        self.code.append(self._loadfrom(os.path.join('code_generation/statics', 'String.s')) + "\n")
        self.code.append(self._loadfrom(os.path.join('code_generation/statics', 'inherit.s')) + "\n")
        
        # self.code.append("main:\n")
        # self.code.append("addi $sp, $sp, -8\n")
        # self.code.append("addi $sp, $sp, -4\n")
        # self.code.append("sw $ra, 0($sp)\n")
        # self.code.append("lw $a0, string_1\n")
        # self.code.append("li $v0, 5\n")
        # self.code.append("syscall\n")
        # self.code.append('j Main.main\n')
        
        # print('code_len', len(self.code))
        for c in self.il_code:
            # print(str(c))
            self.visit(c)

        self.code += "li $v0, 10\n"
        self.code += "syscall\n"

        # print('code_len', len(self.code))
        
        
        return self.code

    @visitor.on('node')
    def visit(self, node):
        pass
    
    #custom
    @visitor.when(CustomLineIL)
    def visit(self, node):
        self.code.append(node.statement)
    #operations

    @visitor.when(BinaryOperationIL)
    def visit(self, node):
        self.code.append("sw $a0, 0($sp)\n")
        self.code.append("addiu $sp, $sp, -4\n")
        self.code.append("lw $t1, 4($sp)\n")

        if node.symbol == '+':
            self.code.append("add $a0, $a0, $t1\n")
        elif node.symbol == '-':
            self.code.append("sub $a0, $a0, $t1\n")
        elif node.symbol == '*':
            self.code.append("mult $a0, $t1\n")
            self.code.append("mflo $a0\n")
        elif node.symbol == '/':
            self.code.append("div $a0, $t1\n")
            self.code.append("mflo $a0\n")
        elif node.symbol == '=':
            self.code.append("seq $a0, $a0, $t1\n")
        elif node.symbol == '>':
            self.code.append("li $t0, 1\n")
            self.code.append("add $t1, $t1, $t0\n")
            self.code.append("sge $a0, $a0, $t1\n")
        elif node.symbol == '>=':
            self.code.append("sge $a0, $a0, $t1\n")
        elif node.symbol == '<=':
            self.code.append("sge $a0, $t1, $a0\n")
        elif node.symbol == '<':
            self.code.append("li $t0, 1\n")
            self.code.append("add $a0, $a0, $t0\n")
            self.code.append("sge $a0, $t1, $a0\n")
        self.code.append("sw $a0, 4($sp)\n")
        self.code.append("addiu $sp, $sp, 4\n")

    @visitor.when(UnaryOperationIL)
    def visit(self, node):
        self.code.append("lw $a0, 0($sp)\n")
        
        if node.symbol == '~':
            self.code.append("not $a0, $a0\n")
        else:
            self.code.append("li $t1, 1\n")
            self.code.append("sub $a0, $t1, $a0\n")
        self.code.append("sw $a0, 4($sp)\n")
    #allocate

    @visitor.when(AllocateIL)
    def visit(self, node):
        self.code.append("li $v0, 9\n")
        self.code.append("li $a0, {}\n".format(4*node.size))
        self.code.append("syscall\n")
        self.code.append("sw $v0, {}($sp)\n".format(4*node.var))
        self.code.append("la $a1, {}_VT\n".format(node.typ))
        self.code.append("sw $a1, ($v0)\n")

    #assignment
    @visitor.when(VarToVarIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(4 * node.right))
        self.code.append("sw $a0, {}($sp)\n".format(4 * node.left))

    @visitor.when(VarToMemoIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(4*node.right))
        self.code.append("lw $t1, {}($sp)\n".format(4*node.left))
        self.code.append("sw $t1, {}($sp)\n".format(4*node.offset))

    @visitor.when(MemoToVarIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(4 * node.right))
        self.code.append("lw $t1, {}($a0)\n".format(4 * node.offset))
        self.code.append("sw $t1, {}($sp)\n".format(4 * node.left))

    @visitor.when(ConstToMemoIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(4 * node.left))
        self.code.append("li $t1, {}\n".format(node.right))
        self.code.append("sw $t1, {}($a0)\n".format(4*node.offset))

    #methods
    @visitor.when(LabelIL)
    def visit(self, node):
        self.code.append(node.label + ':\n')
        if node.func:
            self.code.append("move $fp, $sp\n")
            self.code.append("sw $ra, 0($sp)\n")
            self.code.append("addiu $sp, $sp, -4\n")


    @visitor.when(GotoIL)
    def visit(self, node):
        self.code.append("j " + node.label + "\n")

    @visitor.when(CommentIL)
    def visit(self, node):
        self.code.append(str(node) + "\n")

    @visitor.when(IfJumpIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($fp)\n".format(4 * node.var))
        self.code.append("bnez $a0, " + node.label + "\n")

    @visitor.when(HierarchyIL)
    def visit(self, node):
        self.data.append(node.node + "_INH:\n")
        self.data.append(".word {}_INH\n".format(node.parent))

    @visitor.when(VirtualTableIL)
    def visit(self, node):
        self.data.append(node.name + "_name: .asciiz " +'"'+ node.name + '"\n')
        self.data.append(node.name + "_VT:\n")
        self.data.append(".word {}_INH\n".format(node.name))
        
        for n,m in node.methods:
            self.data.append(".word " + node.name + '.' + n + "\n")

    @visitor.when(PushIL)
    def visit(self, node):
        self.code.append("li $a0, {}\n".format(node.value))
        self.code.append("sw $a0, ($sp)\n")
        self.code.append("addiu $sp, $sp, -4\n")

    @visitor.when(PopIL)
    def visit(self, node):
        self.code.append("addiu $sp, $sp, " + str(4*node.size) + "\n")


    @visitor.when(ReturnIL)
    def visit(self, node):
        # if node.sizeof == 0:
        #     size = 0
        # else:
        #     size = node.sizeof - 1
        self.code.append("lw $ra, {}($sp)\n".format(4*node.sizeof + 4))
        self.code.append("addiu $sp, $sp, {}\n".format(4*node.sizeof + 8))
        self.code.append("lw $fp, 0($sp)\n")
        self.code.append("jr $ra\n")

    @visitor.when(DispatchIL)
    def visit(self, node):
        self.code.append("#Dispatch in place\n")
        self.code.append("#obj {} offset {}  result {}\n".format(node.obj, node.offset, node.result))
#         move $t0, $sp
        # lw $t1, 4($t0)
        # addi $sp, $sp, -4
        # sw $t1, 0($sp)
#           jal Main_init
        # self.code.append("move $t0, $sp\n")
        # self.code.append("lw $t1, 4($t0)\n")
        # self.code.append("addi $sp, $sp, {}\n".format(4))
        # self.code.append("sw $t1, 0($sp)\n")
        if node.result == -1:
            # self.code.append("jalr $ra, $v0\n")
            self.code.append("jal IO.out_string\n")
        else:
            self.code.append("jal {}\n".format(node.result))
        self.code.append("sw $a0, {}($sp)\n".format(4))
        self.code.append("addi $sp, $sp, 4\n")
        # self.code.append("lw $ra, {}($sp)\n".format(4))


    @visitor.when(DispatchParentIL)
    def visit(self, node):
        self.code.append("#DispatchParent in place\n")
        self.code.append("#obj {} offset {}  result {}\n".format(node.obj, node.method, node.result))
        self.code.append("la $v0, " + str(node.method) + "\n")
        if node.result == -1:
            # self.code.append("jalr $ra, $v0\n")
            self.code.append("jal IO.out_string\n")
        else:
            self.code.append("jal {}\n".format(node.result))
        self.code.append("sw $a0, 0($sp)\n")
        self.code.append("addi $sp, $sp, -4\n")

    @visitor.when(InheritIL)
    def visit(self, node):
        self.code.append("lw $a0, {}($sp)\n".format(4 * node.child))
        self.code.append("la $a1, " + node.parent + "_VT\n")
        self.code.append("la $t0, inherit\n")
        self.code.append("jalr $ra, $t0\n")
        self.code.append("sw $v0, {}($sp)\n".format(4*node.result))

    @visitor.when(StringIL)
    def visit(self, node):
        self.code.append("{}: .asciiz \"{}\"\n".format(node.label, node.string))

    @visitor.when(PrintIL)
    def visit(self, node):
        if node.string:
            self.code.append("la $t0, _out_string\n")
        else:
            self.code.append("la $t0, _out_in\n")
        self.code.append("jalr $ra, $t0\n")

    @visitor.when(LoadLabelIL)
    def visit(self, node):
        # self.code.append("sw $a0, {}($sp)\n".format(-4 * node.var))
        self.code.append("la $a0, " + node.label + "\n")
        self.code.append("sw $a0, 0($sp)\n")
        self.code.append("addi $sp, $sp, -4\n")
