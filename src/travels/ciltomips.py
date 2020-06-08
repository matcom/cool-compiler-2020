from mips.baseMipsVisitor import (BaseCilToMipsVisitor, DotDataDirective,
                                  DotGlobalDirective, DotTextDirective,
                                  instrNodes, arithNodes, cmpNodes,
                                  branchNodes, lsNodes)
import typecheck.visitor as visitor
import cil.nodes as cil


class CilToMipsVisitor(BaseCilToMipsVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.CilProgramNode)
    def visit(self, node: cil.CilProgramNode):
        # El programa de CIL se compone por las 3 secciones
        # .TYPES, .DATA y .CODE

        # Visitar cada nodo de la seccion .TYPES
        for type_node in node.dottypes:
            self.visit(type_node)

        # Visitar cada nodo de la seccion .DATA
        for data_node in node.dotdata:
            self.visit(data_node)

        # Visitar cada nodo de la seccion .CODE
        for code_node in node.dotcode:
            self.visit(code_node)