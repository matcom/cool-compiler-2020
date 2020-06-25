from mips.baseMipsVisitor import (BaseCilToMipsVisitor, DotDataDirective,
                                  DotGlobalDirective, DotTextDirective,
                                  instrNodes, arithNodes, cmpNodes,
                                  branchNodes, lsNodes)
import typecheck.visitor as visitor
import cil.nodes as cil
from typing import List
from mips.instruction import (
    a0, a1, a2, a3, at, 
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9,
    s0, s1, s2, s3, s4, s5, s6, s7, sp,
    ra, fp, k0, k1, gp, v0, v1, zero
)


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
        self.register_instruction(lsNodes.LI(v0, 10))
        self.register_instruction(instrNodes.SYSCALL())

    @visitor.when(cil.TypeNode)  # type: ignore
    def visit(self, node: cil.TypeNode):  # noqa: F811
        # registrar el tipo actual que estamos construyendo
        self.current_type = node

        # Los tipos los definiremos en la seccion .data
        self.register_instruction(DotDataDirective())

        # Construir la VTABLE para este tipo.
        self.register_instruction(instrNodes.LineComment(f" **** VTABLE for type {node.name} ****"))
        
        # Los punteros a funciones estaran definidos en el orden en que aparecen declaradas en las clases
        # de modo que la VTABLE sea indexable y podamos efectuar VCALL en O(1).
        self.register_instruction(instrNodes.FixedData(f'{node.name}_vtable', ", ".join(x[1] for x in node.methods)))
        
        self.register_instruction((instrNodes.LineComment(f" **** Type RECORD for type {node.name} ****")))
        # Declarar la direccion de memoria donde comienza el tipo
        self.register_instruction(instrNodes.Label(self.current_type.name))
        # Declarar los atributos: Si los atributos son de tipo string, guardarlos como asciiz
        # de lo contrario son o numeros o punteros y se inicializan como .words
        for attrib in self.current_type.attributes:
            if attrib.name == "String":
                self.register_instruction(instrNodes.FixedData(f'{node.name}_attrib_{attrib.name}', r"", 'asciiz'))
            else:
                self.register_instruction(instrNodes.FixedData(f'{node.name}_attrib_{attrib.name}', 0))
        
        # Registrar un puntero a la VTABLE del tipo.
        self.register_instruction(instrNodes.FixedData(f'{node.name}_vtable_pointer', f"{node.name}_vtable"))
        # Registrar la direccion de memoria donde termina el tipo para calcular facilmente
        # sizeof
        self.register_instruction(instrNodes.Label(f"{node.name}_end"))

        self.current_type = None

    @visitor.when(cil.DataNode)  #type: ignore
    def visit(self, node: cil.DataNode):
        # Registrar los DataNode en la seccion .data
        self.register_instruction(DotDataDirective())
        if isinstance(node.value, str):
            self.register_instruction(instrNodes.FixedData(node.name, rf"{node.value}", type_='asciiz'))
        elif isinstance(node.value, dict):
            # Lo unico que puede ser un diccionario es la TDT. Me parece..... mehh !!??
            # La TDT contiene para cada par (typo1, tipo2), la distancia entre tipo1 y tipo2
            # en caso de que tipo1 sea ancestro de tipo2, -1 en otro caso. Para hacerla accesible en O(1)
            # podemos representarlas como la concatenacion de los nombres de tipo1 y tipo2 (Al final en cada
            # programa los tipos son unicos).
            for (type1, type2), distance in node.value.items():
                self.register_instruction(instrNodes.FixedData(f"__{type1}_{type2}_tdt_entry__", distance))
        elif isinstance(node.value, int):
            self.register_instruction(instrNodes.FixedData(node.name, node.value))

    @visitor.when(cil.FunctionNode)  # type: ignore
    def visit(self, node: cil.FunctionNode):
        ret = 0
        self.current_function = node
        # El codigo referente a cada funcion debe ir en la seccion de texto.
        self.register_instruction(DotTextDirective())
        # Documentar la signatura de la funcion (parametros que recibe, valor que devuelve)
        self.register_instruction(instrNodes.LineComment(f"{node.name} implementation."))
        self.register_instruction(instrNodes.LineComment("@Params:"))
        for i, param in enumerate(node.params):
            if i < 4:
                self.register_instruction(instrNodes.LineComment(f"\t$a{i} = {param}"))
            else:
                self.register_instruction(instrNodes.LineComment(f"\t{(i-4) * 4}($fp) = {param}"))
        # Direccion de memoria de la funcion.
        self.register_instruction(instrNodes.Label(node.name))
        # Crear el marco de pila para la funcion
        locals_count = len(node.localvars)
        self.register_instruction(instrNodes.LineComment("Allocate stack frame for function."))
        # Salvar primero espacio para las variables locales
        if locals_count * 4 < 24:  # MIPS fuerza a un minimo de 32 bytes por stack frame
            self.register_instruction(arithNodes.SUBU(sp, sp, 32, True))
            ret = 32
        else:
            self.register_instruction(arithNodes.SUBU(sp, sp, locals_count * 4 + 8, True))
            ret = locals_count * 4 + 8
        
        # Salvar ra y fp
        self.register_instruction(lsNodes.SW(ra, "8($sp)"))
        self.register_instruction(lsNodes.SW(fp, "4($sp)"))
        # mover fp al inicio del frame
        self.register_instruction(arithNodes.ADDU(fp, sp, ret, True))

        for instruction in node.instructions:
            self.visit(instruction)
        
        self.current_function = None

    @visitor.when(cil.LabelNode)  #type: ignore
    def visit(self, node: cil.LabelNode):
        self.register_instruction(instrNodes.Label(node.label))


class MipsCodeGenerator(CilToMipsVisitor):
    """
    Clase que complete el pipeline entre un programa en CIL y un programa en MIPS.
    El Generador visita el AST del programa en CIL para obtener el conjunto de nodos
    correspondientes a cada instruccion de MIPS y luego devuelve una version en texto
    plano del AST de MIPS, la cual se puede escribir a un archivo de salida y debe estar
    lista para ejecutarse en SPIM.
    """
    def __call__(self, ast: cil.CilProgramNode) -> str:
        self.visit(ast)
        return "".join(str(x) for x in self.program)