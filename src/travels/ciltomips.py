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
        self.register_instruction(
            instrNodes.LineComment("syscall code 10 is for exit"))
        self.register_instruction(lsNodes.LI(v0, 10))
        self.register_instruction(instrNodes.SYSCALL())

    @visit.register
    def _(self, node: cil.TypeNode):  # noqa: F811
        # registrar el tipo actual que estamos construyendo
        self.current_type = node

        # Los tipos los definiremos en la seccion .data
        self.register_instruction(DotDataDirective())

        # Construir la VTABLE para este tipo.
        self.register_instruction(
            instrNodes.LineComment(f" **** VTABLE for type {node.name} ****"))

        # Los punteros a funciones estaran definidos en el orden en que aparecen declaradas en las clases
        # de modo que la VTABLE sea indexable y podamos efectuar VCALL en O(1).
        self.register_instruction(
            instrNodes.FixedData(f'{node.name}_vtable',
                                 ", ".join(x[1] for x in node.methods)))

        self.register_instruction((instrNodes.LineComment(
            f" **** Type RECORD for type {node.name} ****")))
        # Declarar la direccion de memoria donde comienza el tipo
        self.register_instruction(instrNodes.Label(self.current_type.name))
        # Declarar los atributos: Si los atributos son de tipo string, guardarlos como asciiz
        # de lo contrario son o numeros o punteros y se inicializan como .words
        for attrib in self.current_type.attributes:
            if attrib.name == "String":
                self.register_instruction(
                    instrNodes.FixedData(f'{node.name}_attrib_{attrib.name}',
                                         r"", 'asciiz'))
            else:
                self.register_instruction(
                    instrNodes.FixedData(f'{node.name}_attrib_{attrib.name}',
                                         0))

        # Registrar un puntero a la VTABLE del tipo.
        self.register_instruction(
            instrNodes.FixedData(f'{node.name}_vtable_pointer',
                                 f"{node.name}_vtable"))
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
        ret = 0
        self.current_function = node
        # El codigo referente a cada funcion debe ir en la seccion de texto.
        self.register_instruction(DotTextDirective())
        # Documentar la signatura de la funcion (parametros que recibe, valor que devuelve)
        self.register_instruction(
            instrNodes.LineComment(f"{node.name} implementation."))
        self.register_instruction(instrNodes.LineComment("@Params:"))
        for i, param in enumerate(node.params):
            if i < 4:
                self.register_instruction(
                    instrNodes.LineComment(f"\t$a{i} = {param}"))
            else:
                self.register_instruction(
                    instrNodes.LineComment(f"\t{(i-4) * 4}($fp) = {param}"))
        # Direccion de memoria de la funcion.
        self.register_instruction(instrNodes.Label(node.name))
        # Crear el marco de pila para la funcion
        locals_count = len(node.localvars)
        self.register_instruction(
            instrNodes.LineComment("Allocate stack frame for function."))
        # Salvar primero espacio para las variables locales
        if locals_count * 4 < 24:  # MIPS fuerza a un minimo de 32 bytes por stack frame
            self.register_instruction(arithNodes.SUBU(sp, sp, 32, True))
            ret = 32
        else:
            self.register_instruction(
                arithNodes.SUBU(sp, sp, locals_count * 4 + 8, True))
            ret = locals_count * 4 + 8

        # Salvar ra y fp
        self.register_instruction(lsNodes.SW(ra, "8($sp)"))
        self.register_instruction(lsNodes.SW(fp, "4($sp)"))
        # mover fp al inicio del frame
        self.register_instruction(arithNodes.ADDU(fp, sp, ret, True))

        for instruction in node.instructions:
            self.visit(instruction)

        self.current_function = None

    @visit.register
    def _(self, node: cil.LabelNode):
        self.register_instruction(instrNodes.Label(node.label))

    @visit.register
    def _(self, node: cil.ParamNode):
        return self.get_location_address(node)

    @visit.register
    def _(self, node: cil.LocalNode):
        return self.get_location_address(node)

    @visit.register
    def _(self, node: cil.AssignNode):
        assert self.current_function is not None
        # Una asignacion simplemente consiste en mover un resultado de un lugar a otro
        dest = self.visit(node.dest)
        source = self.visit(node.source)

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
            # Source es una direccion de memoria
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

        if isinstance(left, str):
            # left es una direccion de memoria
            reg = self.get_available_register()
            assert reg is not None
            right_reg = self.get_available_register()
            assert right_reg is not None
            self.register_instruction(lsNodes.LW(reg, left))
            if not isinstance(right, int):
                # right no es una constante
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.ADD(reg, reg, right_reg))
            else:
                # rigth es una constante
                self.register_instruction(arithNodes.ADD(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False
        else:
            # left es una constante
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            self.register_instruction(lsNodes.LI(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.ADD(reg, reg, right_reg))
            else:
                self.register_instruction(arithNodes.ADD(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False

    @visit.register
    def _(self, node: cil.MinusNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.x)
        right = self.visit(node.y)

        if isinstance(left, str):
            # left es una direccion de memoria
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            self.register_instruction(lsNodes.LW(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.SUB(reg, reg, right_reg))
            else:
                self.register_instruction(arithNodes.SUB(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False
        else:
            # left es una constante
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            self.register_instruction(lsNodes.LI(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.SUB(reg, reg, right_reg))
            else:
                self.register_instruction(arithNodes.SUB(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False

    @visit.register
    def _(self, node: cil.StarNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.x)
        right = self.visit(node.y)

        if isinstance(left, str):
            # left es una direccion de memoria
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            self.register_instruction(lsNodes.LW(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.MUL(reg, reg, right_reg))
            else:
                self.register_instruction(arithNodes.MUL(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False
        else:
            # left es una constante
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            self.register_instruction(lsNodes.LI(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.MUL(reg, reg, right_reg))
            else:
                self.register_instruction(arithNodes.MUL(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False

    @visit.register
    def _(self, node: cil.DivNode):
        assert self.current_function is not None
        dest = self.visit(node.dest)
        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(left, str):
            # left es una direccion de memoria
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            self.register_instruction(lsNodes.LW(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.DIV(reg, reg, right_reg))
            else:
                self.register_instruction(arithNodes.DIV(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False
        else:
            # left es una constante
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            self.register_instruction(lsNodes.LI(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(arithNodes.DIV(reg, reg, right_reg))
            else:
                self.register_instruction(arithNodes.DIV(
                    reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False

    @visit.register
    def _(self, node: cil.GetAttributeNode):
        pass

    @visit.register
    def _(self, node: cil.SetAttributeNode):
        pass

    @visit.register
    def _(self, node: cil.AllocateNode):
        pass

    @visit.register
    def _(self, node: cil.TypeOfNode):
        pass

    @visit.register
    def _(self, node: cil.JumpIfGreaterThanZeroNode):
        pass

    @visit.register
    def _(self, node: cil.IfZeroJump):
        pass

    @visit.register
    def _(self, node: cil.NotZeroJump):
        pass

    @visit.register
    def _(self, node: cil.UnconditionalJump):
        pass

    @visit.register
    def _(self, node: cil.StaticCallNode):
        pass

    @visit.register
    def _(self, node: cil.DynamicCallNode):
        pass

    @visit.register
    def _(self, node: cil.ArgNode):
        pass

    @visit.register
    def _(self, node: cil.ReturnNode):
        pass

    @visit.register
    def _(self, node: cil.LoadNode):
        pass

    @visit.register
    def _(self, node: cil.LengthNode):
        pass

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
