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

    @visitor.when(cil.CilProgramNode)  # type: ignore
    def visit(self, node: cil.CilProgramNode):  # noqa: F811
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

        # registrar instrucciones para terminar la ejecucion
        self.register_instruction(instrNodes.LineComment("syscall code 10 is for exit"))
        self.register_instruction(lsNodes.LI(instrNodes.v0, 10))
        self.register_instruction(instrNodes.SYSCALL())

    @visitor.when(cil.TypeNode)  # type: ignore
    def visit(self, node: cil.TypeNode):  # noqa: F811
        # registrar el tipo actual que estamos construyendo
        self.current_type = node

        # Los tipos los definiremos en la seccion .data
        self.register_instruction(DotDataDirective())
        # Declarar la direccion de memoria donde comienza el tipo
        self.register_instruction(instrNodes.Label(self.current_type.name))
        # 
