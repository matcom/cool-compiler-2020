
from abstract.semantics import Type
from cil.nodes import (
    AbortNode,
    AllocateBoolNode,
    AllocateIntNode,
    BitwiseNotNode,
    CharToCharStringCompare,
    CompareSTRType,
    CompareStringLengthNode,
    CompareType,
    ConcatString,
    EqualToCilNode,
    GetValue,
    JumpIfGreater,
    LocalNode,
    MinusNodeComp,
    PureMinus,
    ReferenceEqualNode,
)
from mips.arithmetic import ADD, ADDU, DIV, MUL, NOR, NOT, SUB, SUBU
from mips.baseMipsVisitor import (
    BaseCilToMipsVisitor,
    DotDataDirective,
    DotTextDirective,
    locate_attribute_in_type_hierarchy,
)
import cil.nodes as cil
from mips.branch import BEQ, BEQZ, BGT, BGTU, J
from mips.instruction import (
    FixedData,
    Label,
    MOVE,
    REG_TO_STR,
    SYSCALL,
    a0,
    s0,
    sp,
    ra,
    v0,
    a1,
    zero,
    s1,
    at,
    v1,
    a2,
)
import mips.branch as branchNodes
from functools import singledispatchmethod

from mips.load_store import LA, LB, LI, LW, SB, SW


class CilToMipsVisitor(BaseCilToMipsVisitor):
    @singledispatchmethod
    def visit(self, node):
        pass

    @visit.register
    def _(self, node: cil.CilProgramNode):
        # El programa de CIL se compone por las 3 secciones
        # .TYPES, .DATA y .CODE

        self.types = node.dottypes

        # Los tipos los definiremos en la seccion .data
        self.register_instruction(DotDataDirective())
        self.register_instruction(FixedData("dummy", 0))

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

        # El codigo referente a cada funcion debe ir en la seccion de texto.
        self.register_instruction(DotTextDirective())

        self.define_entry_point()

        # Visitar cada nodo de la seccion .CODE
        for code_node in node.dotcode:
            self.visit(code_node)

    @visit.register
    def _(self, node: cil.TypeNode):  # noqa: F811
        # registrar el tipo actual que estamos construyendo
        self.current_type = node

        # Construir la VTABLE para este tipo.
        self.comment(f" **** VTABLE for type {node.name} ****")

        # Los punteros a funciones estaran definidos en el orden en que aparecen declaradas en las clases
        # de modo que la VTABLE sea indexable y podamos efectuar VCALL en O(1).
        self.register_instruction(
            FixedData(f"{node.name}_vtable", ", ".join(x[1] for x in node.methods))
        )
        self.comment("Function END")

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
        self.register_instruction(Label(f"{node.name}_start"))

        # Registrar un puntero a la VTABLE del tipo.
        self.register_instruction(
            FixedData(f"{node.name}_vtable_pointer", f"{node.name}_vtable")
        )
        self.comment("Function END")

        # Declarar los atributos: Si los atributos son de tipo string, guardarlos como asciiz
        # de lo contrario son o numeros o punteros y se inicializan como .words
        # for attrib in node.attributes:
        #     if attrib.type.name == "String":
        #         self.register_instruction(
        #             FixedData(f"{node.name}_attrib_{attrib.name}", r'""', "asciiz")
        #         )
        #     else:
        #         self.register_instruction(
        #             FixedData(f"{node.name}_attrib_{attrib.name}", 0)
        #         )

        # Registrar la direccion de memoria donde termina el tipo para calcular facilmente
        # sizeof
        self.register_instruction(Label(f"{node.name}_end"))

        self.current_type = None

    @visit.register
    def _(self, node: cil.DataNode):
        if isinstance(node.value, str):
            self.register_instruction(
                FixedData(node.name, f"{node.value}", type_="asciiz")
            )
        elif isinstance(node.value, dict):
            # Lo unico que puede ser un diccionario es la TDT. Me parece..... mehh !!??
            # La TDT contiene para cada par (typo1, tipo2), la distancia entre tipo1 y tipo2
            # en caso de que tipo1 sea ancestro de tipo2, -1 en otro caso. Para hacerla accesible en O(1)
            # podemos representarlas como la concatenacion de los nombres de tipo1 y tipo2 (Al final en cada
            # programa los tipos son unicos).
            # for (type1, type2), distance in node.value.items():
            #     self.register_instruction(
            #         FixedData(f"__{type1}_{type2}_tdt_entry__", distance)
            #     )
            for t1 in self.mips_types:
                array = ", ".join(
                    str(x) for x in [node.value[t1, t] for t in self.mips_types]
                )
                self.register_instruction(FixedData(f"{t1}__TDT", array))
        elif isinstance(node.value, int):
            self.register_instruction(FixedData(node.name, node.value))

    @visit.register
    def _(self, node: cil.FunctionNode):
        self.current_function = node

        # Documentar la signatura de la funcion (parametros que recibe, valor que devuelve)
        self.cil_func_signature(node)

        # Direccion de memoria de la funcion.
        self.register_instruction(Label(node.name))

        # Crear el marco de pila de la funcion.
        self.allocate_stack_frame(node)

        for instruction in node.instructions:
            self.visit(instruction)

        self.current_function = None

        self.comment("Function END\n\n")

    @visit.register
    def _(self, node: cil.InitSelfNode):
        src = self.visit(node.src)
        assert src is not None

        self.register_instruction(LW(s1, src))

    @visit.register
    def _(self, node: cil.LabelNode):
        self.register_instruction(Label(node.label))

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
                self.register_instruction(LI(reg, source))
                self.register_instruction(SW(reg, dest))
                self.used_registers[reg] = False
            else:
                # Si no hay registro temporal disponible entonces tenemos que hacer
                # dos instrucciones mas pues hay que salvar el registro s0
                # utlizarlo para hacer la transaccion y luego restaurarlo.
                self.register_instruction(SW(s0, "0($sp)"))
                self.register_instruction(LI(s0, source))
                self.register_instruction(SW(s0, dest))
                self.register_instruction(LI(s0, "0($sp)"))

        elif isinstance(source, str):
            # Source es una direccion de memoria (Puede ser un label, en caso de que sea un tipo)
            reg1 = self.get_available_register()
            assert reg1 is not None
            self.register_instruction(LW(reg1, source))
            self.register_instruction(SW(reg1, dest))
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

        self.operate(dest, left, right, ADD)

    @visit.register
    def _(self, node: cil.MinusNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.x)
        right = self.visit(node.y)

        assert left is not None and right is not None

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        self.operate(dest, left, right, SUB)

    @visit.register
    def _(self, node: cil.StarNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.x)
        right = self.visit(node.y)

        assert left is not None and right is not None

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        self.operate(dest, left, right, MUL)

    @visit.register
    def _(self, node: cil.DivNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        assert left is not None and right is not None

        # Agregar la linea que vamos a traducir.
        self.add_source_line_comment(source=node)

        self.operate(dest, left, right, DIV)

    @visit.register
    def _(self, node: cil.GetAttributeNode):
        # Registrar la linea que estamos traduciendo
        self.add_source_line_comment(node)

        # Localizar el atributo
        offset = self.locate_attribute(node.attrname, node.itype.attributes)

        dest = self.visit(node.dest)
        reg = self.get_available_register()
        assert reg is not None and dest is not None

        # Cargar el atributo en un registro temporal para
        # luego moverlo hacia dest. El objeto self siempre
        # esta en el registro s1
        self.register_instruction(LW(reg, f"{offset}($s1)"))

        self.register_instruction(SW(reg, dest))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: cil.SetAttributeNode):
        # registrar la linea que estamos traduciendo
        self.add_source_line_comment(node)

        # Localizar el atributo
        offset = self.locate_attribute(node.attrname, node.itype.attributes)

        source = self.visit(node.source)
        reg = self.get_available_register()

        assert reg is not None
        assert source is not None

        # Cargar el valor de source en un registro temporal
        # y luego moverlo a la direccion de memoria del
        # atributo
        if isinstance(source, int):
            self.register_instruction(LI(reg, source))
        else:
            self.register_instruction(LW(reg, source))
        self.register_instruction(SW(reg, f"{offset}($s1)"))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: AllocateBoolNode):
        dest = self.visit(node.dest)
        assert dest is not None

        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)
        reg = self.get_available_register()

        assert reg is not None

        self.comment("Allocating string for type Bool")

        # Inicializar la instancia
        self.register_instruction(LA(reg, "String"))
        self.register_instruction(SW(reg, "0($v0)"))

        self.register_instruction(LA(reg, "String_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        self.register_instruction(LA(reg, "Bool"))
        self.register_instruction(SW(reg, "12($v0)"))

        self.register_instruction(LI(reg, 4))
        self.register_instruction(SW(reg, "16($v0)"))

        # devolver la instancia
        self.register_instruction(MOVE(reg, v0))

        size = 16

        self.allocate_memory(size)

        # Almacenar el string al tipo BOOL
        self.register_instruction(SW(reg, f"0($v0)"))

        self.register_instruction(LA(reg, "Bool_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "Bool") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        self.register_instruction(LI(reg, node.value))
        self.register_instruction(SW(reg, "12($v0)"))

        # devolver la instancia
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: AllocateIntNode):
        dest = self.visit(node.dest)
        value = self.visit(node.value)
        assert dest is not None

        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)
        reg = self.get_available_register()

        assert reg is not None

        self.comment("Allocating string for type Int")

        # Inicializar la instancia
        self.register_instruction(LA(reg, "String"))
        self.register_instruction(SW(reg, "0($v0)"))

        self.register_instruction(LA(reg, "String_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        self.register_instruction(LA(reg, "Int"))
        self.register_instruction(SW(reg, "12($v0)"))

        self.register_instruction(LI(reg, 3))
        self.register_instruction(SW(reg, "16($v0)"))

        # devolver la instancia
        self.register_instruction(MOVE(reg, v0))

        size = 16

        self.allocate_memory(size)

        # Almacenar el string al tipo BOOL
        self.register_instruction(SW(reg, f"0($v0)"))

        self.register_instruction(LA(reg, "Int_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "Int") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        if isinstance(node.value, int):
            self.register_instruction(LI(reg, value))
        else:
            self.register_instruction(LW(reg, value))
        self.register_instruction(SW(reg, "12($v0)"))

        # devolver la instancia
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: cil.AllocateStringNode):
        dest = self.visit(node.dest)
        assert dest is not None

        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)
        reg = self.get_available_register()

        assert reg is not None

        self.comment("Allocating string")

        # Inicializar la instancia
        self.register_instruction(LA(reg, "String"))
        self.register_instruction(SW(reg, "0($v0)"))

        self.register_instruction(LA(reg, "String_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        self.register_instruction(LA(reg, node.value.name))
        self.register_instruction(SW(reg, "12($v0)"))

        self.register_instruction(LI(reg, node.length))
        self.register_instruction(SW(reg, "16($v0)"))

        # devolver la instancia
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg] = False

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

        num_bytes = 12  # inicialmente necesita al menos 3 punteros
        dest = self.visit(node.dest)

        instance_type = node.itype

        assert dest is not None

        self.add_source_line_comment(node)

        num_bytes += len(instance_type.attributes) * 4

        reg = self.get_available_register()
        temp = self.get_available_register()
        assert reg is not None and temp is not None, "Out of registers."

        # Inicializar la instancia

        # Crear el string referente al nombre del tipo
        length = len(instance_type.name)

        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)
        self.comment("Allocating string for type name")

        # Inicializar la instancia
        self.register_instruction(LA(reg, "String"))
        self.register_instruction(SW(reg, "0($v0)"))

        self.register_instruction(LA(reg, "String_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        self.register_instruction(LA(reg, instance_type.name))
        self.register_instruction(SW(reg, "12($v0)"))

        self.register_instruction(LI(reg, length))
        self.register_instruction(SW(reg, "16($v0)"))

        self.register_instruction(MOVE(reg, v0))

        # Reservar memoria para la instancia
        self.allocate_memory(num_bytes)

        # Cargar el puntero al tipo de la instancia
        self.register_instruction(SW(dest=reg, src="0($v0)"))

        # Cargar el puntero a la VTABLE
        self.register_instruction(LA(dest=reg, src=f"{instance_type.name}_start"))
        self.register_instruction(SW(dest=reg, src="4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = (
            next(i for i, t in enumerate(self.mips_types) if t == instance_type.name)
            * 4
        )
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        self.register_instruction(MOVE(temp, v0))

        # Cada atributo puede hacer referencia a atributos anteriormente
        # definidos, o sea que tenemos que salvar self
        self.push_register(s1)
        self.register_instruction(MOVE(s1, v0))

        # Los atributos comienzan en el indice 8($v0)
        for i, attribute in enumerate(instance_type.attributes):
            attrib_type_name = locate_attribute_in_type_hierarchy(
                attribute, instance_type
            )
            # llamar la funcion de inicializacion del atributo
            # Salvar el registro temp
            self.push_register(temp)
            self.register_instruction(
                branchNodes.JAL(f"__{attrib_type_name}__attrib__{attribute.name}__init")
            )
            # Restaurar el valor del registro temp
            self.pop_register(temp)
            # El valor de retorno viene en v0
            self.register_instruction(
                SW(dest=v0, src=f"{12 + i*4}(${REG_TO_STR[temp]})")
            )

        # Restaurar self
        self.pop_register(s1)

        # mover la direccion que almacena la instancia hacia dest
        self.register_instruction(SW(temp, dest))

        self.used_registers[reg] = False
        self.used_registers[temp] = False

    @visit.register
    def _(self, node: cil.TypeOffsetNode):
        local_addr = self.visit(node.variable)
        return_addr = self.visit(node.dest)
        reg = self.get_available_register()
        reg2 = self.get_available_register()

        assert reg is not None, "Out of registers"
        assert reg2 is not None, "Out of registers"

        self.add_source_line_comment(node)

        self.register_instruction(LW(reg, local_addr))
        self.comment("Load pointer to type offset")
        self.register_instruction(LW(reg2, f"8(${REG_TO_STR[reg]})"))
        self.register_instruction(SW(reg2, return_addr))

        self.used_registers[reg] = False
        self.used_registers[reg2] = False

    @visit.register
    def _(self, node: JumpIfGreater):
        left = self.visit(node.left)
        right = self.visit(node.rigt)
        reg1 = self.get_available_register()
        reg2 = self.get_available_register()

        assert left is not None
        assert right is not None
        assert reg1 is not None
        assert reg2 is not None

        self.comment(f"Update min if {reg1} < {reg2}")
        self.register_instruction(LW(reg1, left))
        self.register_instruction(LW(reg2, right))
        self.register_instruction(BGTU(reg1, reg2, node.label))

        self.used_registers[reg1] = False
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
    def _(self, node: BitwiseNotNode):
        dest = self.visit(node.dest)
        src = self.visit(node.src)

        reg = self.get_available_register()

        assert reg is not None
        assert src is not None
        assert dest is not None

        self.register_instruction(LW(reg, src))
        # cargar el valor
        self.register_instruction(LW(reg, f"12(${REG_TO_STR[reg]})"))
        self.register_instruction(NOT(reg, reg))
        self.register_instruction(ADD(reg, reg, 1, True))
        self.register_instruction(SW(reg, dest))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: cil.NotNode):
        self.add_source_line_comment(node)
        # Hay que cambiar lo que hay en dest, si es 1 poner 0
        # y si es 0 poner 1
        dest = self.visit(node.src)
        assert dest is not None
        reg = self.get_available_register()
        assert reg is not None

        self.comment("Load value in register")
        self.register_instruction(LW(reg, dest))

        # a nor 0 = not (a or 0) = not a
        self.comment("a nor 0 = not (a or 0) = not a")
        self.register_instruction(NOR(reg, reg, zero))

        self.comment("Store negated value")
        self.register_instruction(SW(reg, dest))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: cil.StaticCallNode):

        # Registrar un comentario con la linea fuente
        self.add_source_line_comment(node)
        dest = self.visit(node.dest)
        self_ptr = self.visit(node.obj)

        assert dest is not None
        assert self_ptr is not None

        # obtener el indice que le corresponde a la funcion que estamos llamando,
        # Recordar que nuestra invariante garantiza que todo metodo con el mismo
        # nombre ocupa el mismo indice en cada VTABLE
        i = self.get_method_index(node.function)

        # Reservar registros para operaciones intermedias
        reg2 = self.get_available_register()
        reg3 = self.get_available_register()
        assert reg2 is not None and reg3 is not None, "out of registers"

        # Actualizar el puntero a self en s1
        self.comment("Save new self pointer in $s1")
        self.register_instruction(LW(s1, self_ptr))

        # Cargar el puntero a la VTABLE del tipo referenciado en TYPE
        self.comment("Get pointer to type's VTABLE")
        self.register_instruction(LA(reg2, f"{node.type_.name}_vtable"))

        # Cargar el puntero a la funcion correspondiente en el tercer registro
        self.comment("Get pointer to function address")
        self.register_instruction(LW(reg3, f"{i * 4}(${REG_TO_STR[reg2]})"))

        # saltar hacia la direccion de memoria correspondiente a la funcion
        self.comment("Call function. Result is on $v0")
        self.register_instruction(branchNodes.JALR(reg3))

        # El resultado viene en $v0
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg2] = False
        self.used_registers[reg3] = False

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
        assert reg1 is not None, "out of registers"

        # Actualizar el puntero a self en s1
        self.comment("Save new self pointer in $s1")
        self.register_instruction(LW(s1, type_src))

        # Cargar el puuntero al tipo en el primer registro
        self.comment("Get pointer to type")
        self.register_instruction(LW(reg1, f"4($s1)"))

        # Cargar el puntero a la VTABLE en el segundo registro
        self.comment("Get pointer to type's VTABLE")
        self.register_instruction(LW(reg1, f"0(${REG_TO_STR[reg1]})"))

        # Cargar el puntero a la funcion correspondiente en el tercer registro
        self.comment("Get pointer to function address")
        self.register_instruction(LW(reg1, f"{i * 4}(${REG_TO_STR[reg1]})"))

        # saltar hacia la direccion de memoria correspondiente a la funcion
        self.comment("Call function. Result is on $v0")
        self.register_instruction(branchNodes.JALR(reg1))

        # El resultado viene en $v0
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg1] = False

    @visit.register
    def _(self, node: cil.SaveSelf):
        self.push_register(s1)

    @visit.register
    def _(self, node: cil.RestoreSelf):
        self.pop_register(s1)

    @visit.register
    def _(self, node: cil.ArgNode):
        # Pasar los argumentos en la pila. #TODO: Pasarlos en registros
        self.add_source_line_comment(node)
        src = self.visit(node.name)
        reg = self.get_available_register()
        assert src is not None and reg is not None

        if isinstance(src, int):
            self.register_instruction(LI(reg, src))
        else:
            self.register_instruction(LW(reg, src))

        self.comment("Push arg into stack")
        self.register_instruction(SUBU(sp, sp, 4, True))
        self.register_instruction(SW(reg, "0($sp)"))

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
                self.register_instruction(LW(v0, src))
            elif isinstance(val, int):
                # val es una constante
                self.register_instruction(LI(v0, val))
            else:
                # val es un str que representa la direccion
                # de un hardcoded string en la seccion .DATA
                self.register_instruction(LW(v0, val))

        # Liberar el marco de pila
        assert self.current_function is not None
        self.deallocate_stack_frame(self.current_function)

        # Liberar el espacio de los argumentos de la funcion
        self.deallocate_args(self.current_function)

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
        self.register_instruction(LA(reg, node.message.name))
        self.register_instruction(SW(reg, dest))

        self.used_registers[reg] = False

    ##          NODOS REFERENTES A OPERACIONES BUILT-IN DE COOL   ##

    @visit.register
    def _(self, node: cil.SubstringNode):
        dest = self.visit(node.dest)
        assert dest is not None
        l = self.visit(node.l)
        r = self.visit(node.r)
        assert l is not None
        assert r is not None

        reg = self.get_available_register()
        reg2 = self.get_available_register()
        temp = self.get_available_register()
        size_reg = self.get_available_register()
        assert reg is not None
        assert reg2 is not None
        assert temp is not None
        assert size_reg is not None

        # Cargar el string sobre el que se llama substr
        self.register_instruction(LW(reg, "12($s1)"))

        # Hacer que reg apunte al inicio del substr
        if isinstance(l, int):
            self.register_instruction(ADDU(reg, reg, l, True))
        else:
            self.register_instruction(LW(temp, l))
            # Cargar el valor
            self.register_instruction(LW(temp, f"12(${REG_TO_STR[temp]})"))
            self.register_instruction(ADDU(reg, reg, temp))

        if isinstance(r, int):
            self.register_instruction(LI(a0, r))
        else:
            self.register_instruction(LW(a0, r))
            # cargar el valor
            self.register_instruction(LW(a0, f"12($a0)"))

        self.register_instruction(MOVE(size_reg, a0))
        self.register_instruction(MOVE(reg2, a0))
        # Agregar un byte mas para el fin de cadena
        self.register_instruction(ADDU(a0, a0, 1, True))

        # $v0 = 9 (syscall 9 = sbrk)
        self.register_instruction(LI(v0, 9))
        self.register_instruction(SYSCALL())

        self.register_instruction(MOVE(temp, v0))

        # Mientras reg != reg2 : Copiar a v0
        self.register_instruction(Label("substr_loop"))
        self.register_instruction(BEQZ(reg2, "substr_end"))
        # Copiar un byte
        self.register_instruction(LB(a0, f"0(${REG_TO_STR[reg]})"))
        self.register_instruction(SB(a0, f"0(${REG_TO_STR[temp]})"))
        # Mover el puntero temp y el puntero reg
        self.register_instruction(ADDU(reg, reg, 1, True))
        self.register_instruction(ADDU(temp, temp, 1, True))
        # Restar del contador
        self.register_instruction(SUBU(reg2, reg2, 1, True))
        # Saltar al ciclo while
        self.register_instruction(J("substr_loop"))
        # Salir del ciclo
        self.register_instruction(Label("substr_end"))
        # Agregar el null al final de la cadena
        self.register_instruction(SB(zero, f"0(${REG_TO_STR[temp]})"))

        # v0 contiene el substr
        self.register_instruction(MOVE(reg2, v0))
        # Crear la instancia de str
        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)

        self.comment("Allocating string")

        # Inicializar la instancia
        self.register_instruction(LA(reg, "String"))
        self.register_instruction(SW(reg, "0($v0)"))

        self.register_instruction(LA(reg, "String_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        # Copiar el str en v0 al atributo value de la instancia
        self.register_instruction(SW(reg2, "12($v0)"))

        self.register_instruction(SW(size_reg, "16($v0)"))

        # devolver la instancia
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg] = False
        self.used_registers[reg2] = False
        self.used_registers[temp] = False
        self.used_registers[size_reg] = False

    @visit.register
    def _(self, node: ConcatString):
        self.add_source_line_comment(node)
        # Obtener los strings a concatenar
        dest = self.visit(node.dest)
        s = self.visit(node.s)
        assert s is not None
        assert dest is not None

        reg = self.get_available_register()
        reg2 = self.get_available_register()
        temp = self.get_available_register()
        size_reg = self.get_available_register()
        byte = self.get_available_register()

        assert (
            reg is not None
            and reg2 is not None
            and temp is not None
            and size_reg is not None
            and byte is not None
        )

        # Get Strings length
        self.comment("Get first string length from self")
        self.register_instruction(LW(reg, f"16($s1)"))

        # Obtener el segundo string
        self.comment("Get second string length from param")
        self.register_instruction(LW(v0, s))
        self.register_instruction(LW(reg2, "16($v0)"))

        self.comment("Save new string length in a0 for memory allocation")
        self.register_instruction(ADDU(a0, reg, reg2))
        self.register_instruction(MOVE(size_reg, a0))

        # Obtener el primer string desde self
        self.comment("Get first string from self")
        self.register_instruction(LW(reg, f"12($s1)"))

        # Obtener el segundo string
        self.comment("Get second string from param")
        self.register_instruction(LW(reg2, "12($v0)"))

        # Reservar memoria para el nuevo buffer
        # $v0 = 9 (syscall 9 = sbrk)
        self.register_instruction(ADDU(a0, a0, 4, True))
        self.register_instruction(LI(v0, 9))
        self.register_instruction(SYSCALL())

        # mover v0 a un puntero temporal que podamos mover
        self.register_instruction(MOVE(temp, v0))

        # Hacer 0 el registro byte
        self.register_instruction(MOVE(byte, zero))

        # while [reg] != 0: copy to temp
        self.register_instruction(Label("concat_loop1"))
        self.comment(f"Compare {REG_TO_STR[reg]} with \\0")
        self.register_instruction(LB(byte, f"0(${REG_TO_STR[reg]})"))
        self.register_instruction(BEQZ(byte, "concat_loop1_end"))
        # Copiar el byte hacia temp y aumentar en 1
        self.comment("Copy 1 byte")
        self.register_instruction(SB(byte, f"0(${REG_TO_STR[temp]})"))
        self.register_instruction(ADDU(temp, temp, 1, True))
        self.register_instruction(ADDU(reg, reg, 1, True))
        self.register_instruction(J("concat_loop1"))

        self.register_instruction(Label("concat_loop1_end"))

        # Copiar el segundo string
        self.comment("Copy second string")
        # while [reg2] != 0: copy to temp
        self.register_instruction(Label("concat_loop2"))
        self.comment(f"Compare {REG_TO_STR[reg2]} with \\0")
        self.register_instruction(LB(byte, f"0(${REG_TO_STR[reg2]})"))
        self.register_instruction(BEQZ(byte, "concat_loop2_end"))
        # Copiar el byte hacia temp y aumentar en 1
        self.comment("Copy 1 byte")
        self.register_instruction(SB(byte, f"0(${REG_TO_STR[temp]})"))
        self.register_instruction(ADDU(temp, temp, 1, True))
        self.register_instruction(ADDU(reg2, reg2, 1, True))
        self.register_instruction(J("concat_loop2"))

        self.register_instruction(Label("concat_loop2_end"))
        # Agregar el caracter null al final
        self.register_instruction(SB(zero, f"0(${REG_TO_STR[temp]})"))

        # v0 contiene el string concatenado
        self.comment("v0 contains resulting string")
        self.register_instruction(MOVE(reg2, v0))

        # Crear la instancia de str
        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)

        self.comment("Allocating string")

        # Inicializar la instancia
        self.register_instruction(LA(reg, "String"))
        self.register_instruction(SW(reg, "0($v0)"))

        self.register_instruction(LA(reg, "String_start"))
        self.register_instruction(SW(reg, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg, offset))
        self.register_instruction(SW(reg, "8($v0)"))

        # Copiar el str en v0 al atributo value de la instancia
        self.register_instruction(SW(reg2, "12($v0)"))

        self.register_instruction(SW(size_reg, "16($v0)"))

        # devolver la instancia
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg] = False
        self.used_registers[reg2] = False
        self.used_registers[temp] = False
        self.used_registers[size_reg] = False
        self.used_registers[byte] = False

    @visit.register
    def _(self, node: AbortNode):
        # Cargar el puntero al tipo de self
        src = self.visit(node.src)
        self.register_instruction(LA(a0, node.abortion.name))
        # Print abortion
        self.register_instruction(LI(v0, 4))
        self.register_instruction(SYSCALL())

        self.register_instruction(LW(a0, src))
        self.register_instruction(LI(v0, 4))
        self.register_instruction(SYSCALL())

        self.register_instruction(LA(a0, node.nl.name))
        self.register_instruction(LI(v0, 4))
        self.register_instruction(SYSCALL())

        self.register_instruction(LI(v0, 10))
        self.register_instruction(SYSCALL())

    @visit.register
    def _(self, node: cil.ReadNode):
        dest = self.visit(node.dest)

        assert dest is not None
        size = 1024  # Max string length in COOL
        reg = self.get_available_register()
        reg2 = self.get_available_register()
        length = self.get_available_register()
        temp = self.get_available_register()
        assert reg is not None
        assert length is not None
        assert temp is not None
        assert reg2 is not None

        # Declarar un buffer para el string
        self.allocate_memory(size)
        self.register_instruction(MOVE(reg, v0))

        # Mover la direccion del buffer a0
        self.register_instruction(MOVE(a0, v0))
        # declarar el espacio disponible en el buffer
        self.register_instruction(LI(a1, size))
        # syscall 8 = read_int
        self.register_instruction(LI(v0, 8))
        self.register_instruction(SYSCALL())

        # reg contiene el string.
        # Crear la instancia del tipo string.
        # Primero calcular el length del string
        self.register_instruction(MOVE(length, zero))
        self.register_instruction(MOVE(temp, zero))
        self.register_instruction(MOVE(reg2, reg))

        self.register_instruction(LB(temp, f"0(${REG_TO_STR[reg2]})"))
        self.register_instruction(BEQZ(temp, "end_loop"))

        self.register_instruction(Label("read_length_loop"))
        # while [reg2] != 0: length ++
        self.register_instruction(LB(temp, f"0(${REG_TO_STR[reg2]})"))
        self.register_instruction(BEQZ(temp, "end_read_length_loop"))
        self.register_instruction(ADDU(reg2, reg2, 1, True))
        self.register_instruction(ADDU(length, length, 1, True))
        self.register_instruction(J("read_length_loop"))
        self.register_instruction(Label("end_read_length_loop"))

        # Remove new line
        self.register_instruction(SUBU(reg2, reg2, 1, True))
        self.register_instruction(SB(zero, f"0(${REG_TO_STR[reg2]})"))
        self.register_instruction(SUBU(length, length, 1, True))

        self.register_instruction(Label("end_loop"))

        # length contiene el length del string
        # Crear la instancia

        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)

        self.comment("Allocating string")

        # Inicializar la instancia
        self.register_instruction(LA(reg2, "String"))
        self.register_instruction(SW(reg2, "0($v0)"))

        self.register_instruction(LA(reg2, "String_start"))
        self.register_instruction(SW(reg2, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg2, offset))
        self.register_instruction(SW(reg2, "8($v0)"))

        self.register_instruction(SW(reg, "12($v0)"))

        self.register_instruction(SW(length, "16($v0)"))

        # devolver la instancia
        self.register_instruction(SW(v0, dest))

        self.used_registers[reg] = False
        self.used_registers[reg2] = False
        self.used_registers[temp] = False
        self.used_registers[length] = False

    @visit.register
    def _(self, node: cil.TypeName):
        dest = self.visit(node.dest)
        assert dest is not None

        # Cargar el puntero al objeto que se esta llamando
        reg = self.get_available_register()
        assert reg is not None

        self.register_instruction(LW(reg, f"0($s1)"))
        self.register_instruction(SW(reg, dest))

        self.used_registers[reg] = False

    @visit.register
    def _(self, node: cil.PrintIntNode):
        # El valor a imprimir se encuentra en la direccion
        # de memoria src
        self.add_source_line_comment(node)
        src = self.visit(node.src)
        assert src is not None

        # En mips, syscall 1 se usa para imprimir el entero
        # almacenado en $a0
        # Cargar el entero en $a0
        self.register_instruction(LW(v0, src))
        # Cargar el valor
        self.register_instruction(LW(a0, f"12($v0)"))
        # syscall 1 = print_int
        self.register_instruction(LI(v0, 1))
        self.register_instruction(SYSCALL())

    @visit.register
    def _(self, node: cil.ReadIntNode):
        dest = self.visit(node.dest)
        assert dest is not None

        self.add_source_line_comment(node)

        # Cargar syscall read_int en $v0
        self.register_instruction(LI(v0, 5))
        self.register_instruction(SYSCALL())

        # Crear la instancia a Int
        self.register_instruction(MOVE(a2, v0))

        size = 20

        # Reservar memoria para el tipo
        self.allocate_memory(size)
        reg2 = self.get_available_register()

        assert reg2 is not None

        self.comment("Allocating string for type Int")

        # Inicializar la instancia
        self.register_instruction(LA(reg2, "String"))
        self.register_instruction(SW(reg2, "0($v0)"))

        self.register_instruction(LA(reg2, "String_start"))
        self.register_instruction(SW(reg2, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "String") * 4
        self.register_instruction(LI(reg2, offset))
        self.register_instruction(SW(reg2, "8($v0)"))

        self.register_instruction(LA(reg2, "Int"))
        self.register_instruction(SW(reg2, "12($v0)"))

        self.register_instruction(LI(reg2, 3))
        self.register_instruction(SW(reg2, "16($v0)"))

        # devolver la instancia
        self.register_instruction(MOVE(reg2, v0))

        size = 16

        self.allocate_memory(size)

        # Almacenar el string al tipo Int
        self.register_instruction(SW(reg2, f"0($v0)"))

        self.register_instruction(LA(reg2, "Int_start"))
        self.register_instruction(SW(reg2, "4($v0)"))

        # Cargar el offset del tipo
        self.comment("Load type offset")
        offset = next(i for i, t in enumerate(self.mips_types) if t == "Int") * 4
        self.register_instruction(LI(reg2, offset))
        self.register_instruction(SW(reg2, "8($v0)"))

        self.register_instruction(SW(a2, "12($v0)"))

        # Almacenar el numero leido en dest
        self.register_instruction(SW(v0, dest))
        self.used_registers[reg2] = False

    @visit.register
    def _(self, node: cil.PrintNode):
        src = self.visit(node.src)
        assert src is not None

        self.add_source_line_comment(node)

        self.register_instruction(LW(v0, src))

        # Cargar la direccion del string en a0
        self.register_instruction(LW(a0, "12($v0)"))
        # syscall 4 = print_string
        self.register_instruction(LI(v0, 4))
        self.register_instruction(SYSCALL())

    @visit.register
    def _(self, node: cil.TdtLookupNode):
        # Cargar el valor que esta en offset en la tabla del tipo
        self.add_source_line_comment(node)
        dest = self.visit(node.dest)
        offset_addr = self.visit(node.j)
        tdt_table = self.get_available_register()
        offset = self.get_available_register()

        assert offset is not None
        assert tdt_table is not None
        assert offset_addr is not None
        assert dest is not None

        # Cargar la tabla referente al tipo
        self.comment(f"Load TDT pointer to type {node.i}")
        self.register_instruction(LA(tdt_table, f"{node.i}__TDT"))

        self.register_instruction(LW(offset, offset_addr))

        # mover el puntero offset bytes
        self.register_instruction(ADDU(tdt_table, tdt_table, offset))

        self.comment("Save distance")
        self.register_instruction(LW(offset, f"0(${REG_TO_STR[tdt_table]})"))
        self.register_instruction(SW(offset, dest))

        self.used_registers[tdt_table] = False
        self.used_registers[offset] = False

    @visit.register
    def _(self, node: int):
        return node

    @visit.register
    def _(self, node: cil.SelfNode):
        dest = self.visit(node.dest)
        assert dest is not None
        # El puntero a self siempre se guarda en el registro $s1
        self.add_source_line_comment(node)
        self.register_instruction(SW(s1, dest))

    @visit.register
    def _(self, node: GetValue):
        dest = self.visit(node.dest)
        src = self.visit(node.src)

        assert dest is not None
        assert src is not None
        self.comment(f"Obtain value from {src}")
        self.register_instruction(LW(v0, src))
        self.register_instruction(LW(v0, f"12($v0)"))
        self.register_instruction(SW(v0, dest))

    @visit.register
    def _(self, node: CompareType):
        dest = self.visit(node.dest)
        src = self.visit(node.src)

        assert dest is not None
        assert src is not None
        self.comment(f"Comparing {src} type with {node.type}")
        # Cargar el puntero al tipo que queremos comparar
        self.register_instruction(LA(v0, node.type))

        # Cargar el puntero al string del tipo
        self.register_instruction(LW(a0, src))
        self.register_instruction(LW(a0, f"0($a0)"))
        # Cargar el valor del string
        self.register_instruction(LW(a0, f"12($a0)"))
        # Restar y devolver
        self.register_instruction(SUB(a0, a0, v0))
        self.register_instruction(SW(a0, dest))

    @visit.register
    def _(self, node: CompareSTRType):
        dest = self.visit(node.dest)
        src = self.visit(node.src)

        assert dest is not None
        assert src is not None
        self.comment(f"Comparing {src} type with String")
        # Cargar el puntero al tipo que queremos comparar
        self.register_instruction(LA(v0, "String"))

        # Cargar el puntero al string del tipo
        self.register_instruction(LW(a0, src))
        self.register_instruction(LW(a0, f"0($a0)"))
        # Restar y devolver
        self.register_instruction(SUB(a0, a0, v0))
        self.register_instruction(SW(a0, dest))

    @visit.register
    def _(self, node: CompareStringLengthNode):
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        assert dest is not None
        assert left is not None
        assert right is not None

        # Cargar ambos strings
        self.comment("Load strings for comparison")
        self.register_instruction(LW(v0, left))
        self.register_instruction(LW(v1, right))

        self.comment("Compare lengths")
        self.register_instruction(LW(v0, f"16($v0)"))
        self.register_instruction(LW(v1, f"16($v1)"))
        self.register_instruction(SUB(v0, v0, v1))

        # Return result
        self.register_instruction(SW(v0, dest))

    @visit.register
    def _(self, node: CharToCharStringCompare):
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        assert dest is not None
        assert left is not None
        assert right is not None

        self.register_instruction(MOVE(a2, zero))

        # Cargar ambos strings
        self.comment("Load strings for comparison")
        self.register_instruction(LW(v0, left))
        self.register_instruction(LW(v1, right))

        # Cargar los punteros a los strings
        self.comment("Load strings pointers")
        self.register_instruction(LW(v0, "12($v0)"))
        self.register_instruction(LW(v1, f"12($v1)"))

        self.comment(f"Compare loop, while [v0] != \\0")
        self.register_instruction(Label(node.while_label))
        self.register_instruction(LB(a0, f"0($v0)"))
        self.comment("If EOS => break")
        self.register_instruction(BEQZ(a0, node.end_label))
        self.register_instruction(LB(a1, f"0($v1)"))
        self.comment("Move strings pointers")
        self.register_instruction(ADDU(v0, v0, 1, True))
        self.register_instruction(ADDU(v1, v1, 1, True))
        self.comment("Compare chars")
        self.register_instruction(SUB(a0, a0, a1))
        self.register_instruction(BEQZ(a0, node.while_label))
        self.comment("False")
        self.register_instruction(LI(a2, 1))
        self.register_instruction(Label(node.end_label))

        # Guardar el resultado
        self.comment("Store result")
        self.register_instruction(SW(a2, dest))

    @visit.register
    def _(self, node: ReferenceEqualNode):
        # Comparar por referencias es simplemente
        # cargar los punteros y restar
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        assert dest is not None
        assert left is not None
        assert right is not None

        self.comment("Load pointers and SUB")
        self.register_instruction(LW(a0, left))
        self.register_instruction(LW(a1, right))
        self.register_instruction(SUB(a0, a0, a1))

        self.register_instruction(SW(a0, dest))

    @visit.register
    def _(self, node: MinusNodeComp):
        # operate por valor sin devolver una instancia de int
        # Comparar por referencias es simplemente
        # cargar los punteros y restar
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        assert dest is not None
        assert left is not None
        assert right is not None

        # Load pointers
        self.register_instruction(LW(a0, left))
        self.register_instruction(LW(a1, right))

        self.comment("Load values")
        self.register_instruction(LW(a0, "12($a0)"))
        self.register_instruction(LW(a1, "12($a1)"))

        self.comment("SUB and store")
        self.register_instruction(SUB(a0, a0, a1))
        self.register_instruction(SW(a0, dest))


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
        return self.to_str()

    def to_str(self) -> str:
        program = ""
        indent = 0
        for instr in self.program:
            line = str(instr)
            if ".data" in line or ".text" in line:
                indent = 0
            program += "\n" + " " * (3 * indent) + line
            if "#" not in line and (":" in line and "end" not in line):
                if "word" not in line and "asciiz" not in line and "byte" not in line:
                    indent += 1
            if "# Function END" in line or "label_END" in line:
                indent = 0
        return program
