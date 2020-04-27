import core.cmp.visitor as visitor
import core.cmp.cil as cil
import core.cmp.mips as mips

class BaseCILToMIPSVisitor:
    def __init__(self):
        self.types = {}
        self.dottext = []
        self.dotdata = []
    


class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        for type_node in node.dottypes:
            self.visit(type_node)
        
        for data_node in node.dotdata:
            self.visit(data_node)

        for function_node in node.dotcode:
            self.visit(function_node)
        
        return mips.ProgramNode(dottext, dotdata)

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        self.types.append(cil_to_mips_type(node))

    @visitor.when(cil.DataNode)
    def visit(self, node):
        self.dotdata.append(cil_to_mips_data(node))

    @visitor.when(cil.FunctionNode)
    def visit(self, node):



def cil_to_mips_data(cil_data):
    return mips.DataNode(cil_data.name, cil_data.value)

def cil_to_mips_type(cil_type):
    return mips.MIPSType(cil_type.name, cil_type.attributes, cil_type.methods)