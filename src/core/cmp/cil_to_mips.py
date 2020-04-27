import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.mips as mips

class BaseCILToMIPSVisitor:
    pass

class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        pass

    @visitor.when(cil.)    