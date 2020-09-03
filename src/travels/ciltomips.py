from abstract.semantics import Type
from cil.nodes import LocalNode
from mips.baseMipsVisitor import (BaseCilToMipsVisitor, DotDataDirective,
                                  DotGlobalDirective, DotTextDirective,
                                  instrNodes, arithNodes, cmpNodes,
                                  branchNodes, lsNodes)
import cil.nodes as cil
from mips.instruction import (a0, a1, a2, a3, at, t0, t1, t2, t3, t4, t5, t6,
                              t7, t8, t9, s0, s1, s2, s3, s4, s5, s6, s7, sp,
                              ra, fp, k0, k1, gp, v0, v1, zero, TEMP_REGISTERS)
from functools import singledispatchmethod


class CilToMipsVisitor(BaseCilToMipsVisitor):
    @singledispatchmethod
    def visit(self, node):
        pass

    @visit.register
    def _(self, node: cil.CilProgramNode):
        # El programa de CIL se compone por las 3 secciones
        # .TYPES, .DATA y .CODE

        self.types = node.dottypes

        # Generar los tipos
        self.create_type_array(node.dottypes)

        self.comment("\n\n")

        # Visitar cada nodo de la seccion .TYPES
        for type_node in node.dottypes:
            self.visit(type_node)
            self.comment("\n\n")

        # Visitar cada nodo de la seccion .DATA
        for data_node in node.dotdata:
            self.visit(data_node)
            self.comment("\n\n")

        # Visitar cada nodo de la seccion .CODE
        for code_node in node.dotcode:
            self.visit(code_node)

        # registrar instrucciones para terminar la ejecucion
        self.comment("syscall code 10 is for exit")
        self.register_instruction(lsNodes.LI(v0, 10))
        self.register_instruction(instrNodes.SYSCALL())

    @visit.register
    def _(self, node: cil.TypeNode):  # noqa: F811
        # registrar el tipo actual que estamos construyendo
        self.current_type = node

        # Los tipos los definiremos en la seccion .data
        self.register_instruction(DotDataDirective())

        # Construir la VTABLE para este tipo.
        self.comment(f" **** VTABLE for type {node.name} ****")

        # Los punteros a funciones estaran definidos en el orden en que aparecen declaradas en las clases
        # de modo que la VTABLE sea indexable y podamos efectuar VCALL en O(1).
        self.register_instruction(
            instrNodes.FixedData(f'{node.name}_vtable',
                                 ", ".join(x[1] for x in node.methods)))

        self.comment("\n\n")

        # FORMA DE UN TIPO EN ASSEMBLY
        ##################################### Type address
        #           VTABLE_POINTER          #
        ##################################### Type address + 4
        #         ATTRIBUTE_LIST            #
        #            ..........             #
        #            ..........             #
        ##################################### Type_end

        self.comment(f" **** Type RECORD for type {node.name} ****")
        # Declarar la direccion de memoria donde comienza el tipo
        self.register_instruction(
            instrNodes.Label(f"{self.current_type.name}_start"))

        # Registrar un puntero a la VTABLE del tipo.
        self.register_instruction(
            instrNodes.FixedData(f'{node.name}_vtable_pointer',
                                 f"{node.name}_vtable"))

        # Declarar los atributos: Si los atributos son de tipo string, guardarlos como asciiz
        # de lo contrario son o numeros o punteros y se inicializan como .words
        for attrib in self.current_type.attributes:
            if attrib.type.name == "String":
                self.register_instruction(
                    instrNodes.FixedData(f'{node.name}_attrib_{attrib.name}',
                                         r"", 'asciiz'))
            else:
                self.register_instruction(
                    instrNodes.FixedData(f'{node.name}_attrib_{attrib.name}',
                                         0))

        # Registrar la direccion de memoria donde termina el tipo para calcular facilmente
        # sizeof
        self.register_instruction(instrNodes.Label(f"{node.name}_end"))

        self.current_type = None

    @visit.register
    def _(self, node: cil.DataNode):
        # Registrar los DataNode en la seccion .data
        self.register_instruction(DotDataDirective())
        if isinstance(node.value, str):
            self.register_instruction(
                instrNodes.FixedData(node.name,
                                     f"{node.value}",
                                     type_='asciiz'))
        elif isinstance(node.value, dict):
            # Lo unico que puede ser un diccionario es la TDT. Me parece..... mehh !!??
            # La TDT contiene para cada par (typo1, tipo2), la distancia entre tipo1 y tipo2
            # en caso de que tipo1 sea ancestro de tipo2, -1 en otro caso. Para hacerla accesible en O(1)
            # podemos representarlas como la concatenacion de los nombres de tipo1 y tipo2 (Al final en cada
            # programa los tipos son unicos).
            for (type1, type2), distance in node.value.items():
                self.register_instruction(
                    instrNodes.FixedData(f"__{type1}_{type2}_tdt_entry__",
                                         distance))
        elif isinstance(node.value, int):
            self.register_instruction(
                instrNodes.FixedData(node.name, node.value))

    @visit.register
    def _(self, node: cil.FunctionNode):
        self.current_function = node
        # El codigo referente a cada funcion debe ir en la seccion de texto.
        self.register_instruction(DotTextDirective())

        # Documentar la signatura de la funcion (parametros que recibe, valor que devuelve)
        self.cil_func_signature(node)

        # Direccion de memoria de la funcion.
        self.register_instruction(instrNodes.Label(node.name))

        # Crear el marco de pila de la funcion.
        self.allocate_stack_frame(node)

        for instruction in node.instructions:
            self.visit(instruction)

        self.current_function = None

        self.comment("\n\n")

    @visit.register
    def _(self, node: cil.LabelNode):
        self.register_instruction(instrNodes.Label(node.label))

    @visit.register
    def _(self, node: cil.ParamNode):
        label = self.get_location_address(node)

        # Agregar la linea que vamos a traducir.
        self.comment(f"PARAM {node.name} --> {label}")

        return label

    @visit.register
    def _(self, node: cil.LocalNode):
        label = self.get_location_address(node)

        # Agregar la linea que vamos a traducir.
        self.comment(f"LOCAL {node.name} --> {label}")

        return label

    @visit.register
    def _(self, node: Type):
        return node.name

    @visit.register
    def _(self, node: cil.AssignNode):
        assert self.current_function is not None
        # Una asignacion simplemente consiste en mover un resultado de un lugar a otro
        dest = self.visit(node.dest)
        source = self.visit(node.source)

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        # Puede que se asigne una constante o lo que hay en alguna direccion de memoria
        if isinstance(source, int):
            reg = self.get_available_register()
            if reg is not None:
                # Si tenemos registro temporal disponible entonces movemos
                # lo que hay en la direccion de memoria source a reg y luego
                # asignamos el valor de reg a dest.
                self.register_instruction(lsNodes.LI(reg, source))
                self.register_instruction(lsNodes.SW(reg, dest))
                self.used_registers[reg] = False
            else:
                # Si no hay registro temporal disponible entonces tenemos que hacer
                # dos instrucciones mas pues hay que salvar el registro s0
                # utlizarlo para hacer la transaccion y luego restaurarlo.
                self.register_instruction(lsNodes.SW(s0, "0($sp)"))
                self.register_instruction(lsNodes.LI(s0, source))
                self.register_instruction(lsNodes.SW(s0, dest))
                self.register_instruction(lsNodes.LI(s0, "0($sp)"))

        elif isinstance(source, str):
            # Source es una direccion de memoria (Puede ser un label, en caso de que sea un tipo)
            reg1 = self.get_available_register()
            assert reg1 is not None
            self.register_instruction(lsNodes.LW(reg1, source))
            self.register_instruction(lsNodes.SW(reg1, dest))
            self.used_registers[reg1] = False

    @visit.register
    def _(self, node: cil.PlusNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        assert left is not None and right is not None

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        self.operate(dest, left, right, arithNodes.ADD)

    @visit.register
    def _(self, node: cil.MinusNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.x)
        right = self.visit(node.y)

        assert left is not None and right is not None

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        self.operate(dest, left, right, arithNodes.SUB)

    @visit.register
    def _(self, node: cil.StarNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.x)
        right = self.visit(node.y)

        assert left is not None and right is not None

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        self.operate(dest, left, right, arithNodes.MUL)

    @visit.register
    def _(self, node: cil.DivNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        assert left is not None and right is not None

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        self.operate(dest, left, right, arithNodes.DIV)

    @visit.register
    def _(self, node: cil.GetAttributeNode):
        pass

    @visit.register
    def _(self, node: cil.SetAttributeNode):
        pass

    @visit.register
    def _(self, node: cil.AllocateNode):
        # Cada instancia debe almacenar lo siguiente:
        # - Un puntero a la vTable de su tipo
        # - Espacio para cada atributo
        # - Un puntero a su tipo en el array de tipos, de modo que sea facil calcular typeof

        #################################  address
        #          TYPE_POINTER         #
        #################################  address + 4
        #          VTABLE_POINTER       #
        #################################  address  + 8
        #           ATTRIBUTE_1         #
        #################################  address + 12
        #           ATTRIBUTE_2         #
        #################################
        #               ...             #
        #               ...             #
        #               ...             #
        #################################

        num_bytes = 8  # inicialmente necesita al menos dos punteros
        dest = self.visit(node.dest)

        instance_type = node.itype

        assert dest is not None

        self.add_source_line_comment(node)

        num_bytes += len(instance_type.attributes) * 4

        # Reservar memoria para la instancia
        self.allocate_memory(num_bytes)

        reg = self.get_available_register()
        assert reg is not None, "Out of registers."

        # Inicializar la instancia

        # Cargar el puntero al tipo de la instancia
        self.register_instruction(lsNodes.LA(dest=reg, src=instance_type.name))
        self.register_instruction(lsNodes.SW(dest=reg, src="0($v0)"))

        # Cargar el puntero a la VTABLE
        self.register_instruction(
            lsNodes.LA(dest=reg, src=f"{instance_type.name}_start"))
        self.register_instruction(lsNodes.SW(dest=reg, src="4($v0)"))

        # TODO: Manejar los atributos

        # mover la direccion que almacena la instancia hacia dest
        self.register_instruction(lsNodes.SW(v0, dest))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: cil.TypeOfNode):
        local_addr = self.get_location_address(node=node.variable)
        return_addr = self.get_location_address(node=node.dest)
        reg = self.get_available_register()
        reg2 = self.get_available_register()

        assert reg is not None, "Out of registers"
        assert reg2 is not None, "Out of registers"

        self.add_source_line_comment(node)

        self.register_instruction(lsNodes.LW(reg, local_addr))
        self.comment("Load pointer to type")
        self.register_instruction(lsNodes.LW(reg2, f"4(${reg})"))
        self.register_instruction(lsNodes.SW(reg2, return_addr))

        self.used_registers[reg] = False
        self.used_registers[reg2] = False

    @visit.register
    def _(self, node: cil.JumpIfGreaterThanZeroNode):
        self.add_source_line_comment(node)
        self.conditional_jump(node, branchNodes.BGT)

    @visit.register
    def _(self, node: cil.IfZeroJump):
        self.add_source_line_comment(node)
        self.conditional_jump(node, branchNodes.BEQ)

    @visit.register
    def _(self, node: cil.NotZeroJump):
        self.add_source_line_comment(node)
        self.conditional_jump(node, branchNodes.BNE)

    @visit.register
    def _(self, node: cil.UnconditionalJump):
        self.add_source_line_comment(node)
        self.register_instruction(branchNodes.J(node.label))

    @visit.register
    def _(self, node: cil.StaticCallNode):

        # Registrar un comentario con la linea fuente
        self.add_source_line_comment(node)
        dest = self.visit(node.dest)

        assert dest is not None

        # Saltar hacia la direccion de memoria correspondiente a la funcion
        self.register_instruction(branchNodes.JAL(node.function))

        # EL resultado viene en v0
        self.register_instruction(lsNodes.SW(v0, dest))

    @visit.register
    def _(self, node: cil.DynamicCallNode):
        type_src = self.visit(node.xtype)
        dest = self.visit(node.dest)

        assert type_src is not None and dest is not None

        # Generar el comentario de la linea fuente
        self.add_source_line_comment(node)

        # obtener el indice que le corresponde a la funcion que estamos llamando
        i = self.get_method_index(node.method)

        # Reservar registros para operaciones intermedias
        reg1 = self.get_available_register()
        reg2 = self.get_available_register()
        reg3 = self.get_available_register()
        assert reg1 is not None and reg2 is not None and reg3 is not None, "out of registers"

        # Cargar el puuntero al tipo en el primer registro
        self.comment("Get pointer to type")
        self.register_instruction(lsNodes.LW(reg1, type_src))

        # Cargar el puntero a la VTABLE en el segundo registro
        self.comment("Get pointer to type's VTABLE")
        self.register_instruction(lsNodes.LW(reg2, f"0(${reg1})"))

        # Cargar el puntero a la funcion correspondiente en el tercer registro
        self.comment("Get pointer to function address")
        self.register_instruction(lsNodes.LW(reg3, f"{i * 4}(${reg2})"))

        # saltar hacia la direccion de memoria correspondiente a la funcion
        self.comment("Call function. Result is on $v0")
        self.register_instruction(branchNodes.JALR(reg3))

        # El resultado viene en $v0
        self.register_instruction(lsNodes.SW(v0, dest))

        self.used_registers[reg1] = False
        self.used_registers[reg2] = False
        self.used_registers[reg3] = False

    @visit.register
    def _(self, node: cil.ArgNode):
        # Pasar los argumentos en la pila. #TODO: Pasarlos en registros
        self.add_source_line_comment(node)
        src = self.visit(node.name)
        reg = self.get_available_register()
        assert src is not None and reg is not None

        if isinstance(src, int):
            self.register_instruction(lsNodes.LI(reg, src))
        else:
            self.register_instruction(lsNodes.LW(reg, src))

        self.comment("Push arg into stack")
        self.register_instruction(arithNodes.SUBU(sp, sp, 4, True))
        self.register_instruction(lsNodes.SW(reg, "0($sp)"))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: cil.ReturnNode):
        # Generar dos formas de codigo en dependencia de si se devuelve un valor  o no
        self.add_source_line_comment(node)
        val = node.value
        if val is not None:
            if isinstance(val, LocalNode):
                src = self.get_location_address(val)
                # almacenar el resultado en $v0
                self.register_instruction(lsNodes.LW(v0, src))
            else:
                # val es una constante
                self.register_instruction(lsNodes.LI(v0, val))

        # Liberar el marco de pila
        assert self.current_function is not None
        self.deallocate_stack_frame(self.current_function)

        # salir del llamado de la funcion
        self.register_instruction(branchNodes.JR(ra))

    @visit.register
    def _(self, node: cil.LoadNode):
        dest = self.visit(node.dest)
        assert dest is not None

        # message es un string, asi que solo hay que cargar el puntero a dicho string
        reg = self.get_available_register()
        assert reg is not None, "Out of registers"
        self.add_source_line_comment(node)
        self.register_instruction(lsNodes.LW(reg, node.message.name))
        self.register_instruction(lsNodes.SW(reg, dest))

        self.used_registers[reg] = False

    ##          NODOS REFERENTES A OPERACIONES BUILT-IN DE COOL   ##

    @visit.register
    def _(self, node: cil.LengthNode):
        pass

    @visit.register
    def _(self, node: cil.ConcatNode):
        pass

    @visit.register
    def _(self, node: cil.PrefixNode):
        pass

    @visit.register
    def _(self, node: cil.ToStrNode):
        pass

    @visit.register
    def _(self, node: cil.ReadNode):
        pass

    @visit.register
    def _(self, node: cil.PrintNode):
        pass

    @visit.register
    def _(self, node: cil.TdtLookupNode):
        # Los nodos TDT siempre tienen
        pass

    @visit.register
    def _(self, node: int):
        return node


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
        return "\n".join(str(x) for x in self.program)
