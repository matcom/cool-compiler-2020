from json import load
from cil.nodes import TypeNode
from cil.nodes import CilNode, FunctionNode
from mips import load_store
import mips.instruction as instrNodes
import mips.branch as branchNodes
import mips.comparison as cmpNodes
import mips.arithmetic as arithNodes
from mips.instruction import a0, fp, ra, sp, v0
import mips.load_store as lsNodes
from typing import List, Optional, Type, Union
import time
import cil.nodes as cil
from travels.ctcill import CilDisplayFormatter


class AbstractDirective(instrNodes.MipsNode):
    def __init__(self, addr: str = None):
        self.addr = addr

    def __str__(self):
        raise NotImplementedError()


class DotDataDirective(AbstractDirective):
    def __str__(self):
        return '.data' if self.addr is None else f'.data {self.addr}'


class DotTextDirective(AbstractDirective):
    def __str__(self):
        return '.text' if self.addr is None else f'.text {self.addr}'


class DotGlobalDirective(AbstractDirective):
    def __str__(self):
        assert self.addr is not None
        return f'.global {self.addr}'


class BaseCilToMipsVisitor:
    """
    Clase base para un visitor que transforma un AST de CIL en un AST de MIPS, a partir del cual se obtendra
    luego el programa mips que se guardara en el archivo de salida.

        Un programa de mips contiene varias directivas:

        .data  <addr>
            Esta seccion son ensamblados en la seccion de datos del programa. Por defecto,
            comienza en la proxima direccion disponible en el segmento de datos. Si el argumento
            addr esta presente, entonces comienza en addr.

        .text <addr>
            Los elementos de esta seccion son ensamblados en el segmento de texto. Por defecto, comienza en la proxima
            direccion disponible en el segmento de texto, a menos que el argumento opcional <addr> este presente, en cuyo
            caso, la proxima direccion es addr. (En SPIM, lo unico que se puede ensamblar en la seccion de texto son
            instrucciones y palabras, por medio de la directiva .word).

        .kdata <addr>
            Es igual a la seccion .data, pero solo es usado por el Sistema Operativo.

        .ktext <addr>
            Es igual a la seccion .text, pero solo es usado por el Sistema Operativo.

        .extern sym size
            Declara el label sym como global y declara que tiene size bytes de longitud (esta informacion es util para
            el assembler).

        .globl sym
            Declara el label sym como global.
        """
    def __init__(self):
        # Un programa de MIPS es una lista de Instrucciones de MIPS.
        self.program: List[instrNodes.MipsNode] = []
        # Necesitamos saber si estamos construyendo un tipo, para poder acceder
        # a nombres de funciones, atributos, etc.
        self.current_type: Optional[cil.TypeNode] = None

        # Necesitamos acceso a las variables locales y parametros de la funcion que estamos
        # construyendo
        self.current_function: Optional[cil.FunctionNode] = None

        # Llevar un record de los registros que hemos utilizado en la funcion actual
        # Cada funcion es libre de usar los registros t0 -- t9 (temporales, estos registros)
        # no guardan valores de retornos ni son utilizados como confiables, solo se usan para
        # almacenar valores intermedios y valores de variables, para evitar accesos a memoria.
        self.used_registers = [False] * 32

        # Necesitamos acceso a los tipos del programa
        self.types: List[TypeNode] = []

        # Construir el header del programa.
        self.__program_header()

        self.__cil_display_formatter = CilDisplayFormatter()

    # Metodos Publicos
    def register_instruction(self, node: instrNodes.MipsNode):
        self.program.append(node)
        return node

    # Metodos Privados
    def __program_header(self):
        date = time.asctime()
        coolc = 'Code generated by PyCoolc.'
        ad = 'Adrian Gonzalez'
        ep = 'Eliane Puerta'
        la = 'Liset Alfaro'
        institution = 'School of Math and Computer Science, University of Havana'
        self.comment(coolc)
        self.comment(f'{ep}, {la}, {ad} --- {date}')
        self.comment(institution)
        self.comment("\n")

    # Funcion de ayuda para obtener la direccion de memoria de un parametro o una variable
    def get_location_address(self, node: Union[cil.ParamNode,
                                               cil.LocalNode]) -> str:
        """
        Devuelve el offset del parametro o variable local que estamos buscando, accediendo a este en el stack. Offset es positivo si se trata de un parametro, negativo en caso de una variable local.
        """
        assert self.current_function is not None
        index = -1
        if isinstance(node, cil.ParamNode):
            # Buscar el indice del parametro al que corresponde
            for i, param in enumerate(self.current_function.params):
                if param.name == node.name:
                    index = i
                    break

            assert index > -1

            return f"{index * 4}($fp)"
        else:
            # Buscar el indice de la variable local
            for i, local_var in enumerate(self.current_function.localvars):
                if local_var.name == node.name:
                    index = i
                    break

            assert index > -1
            index += 1
            return f"-{index * 4}($fp)"

    def get_available_register(self) -> Optional[int]:
        """
        Obtiene un registro disponible.
        """
        for register in instrNodes.TEMP_REGISTERS:
            if not self.used_registers[register]:
                self.used_registers[register] = True
                return register
        return None

    def add_source_line_comment(self, source: CilNode):
        """
        Muestra en el archivo mips un comentario con la linea que se esta transcribiendo.
        """
        self.register_instruction(
            instrNodes.LineComment(self.__cil_display_formatter.visit(source)))

    def cil_func_signature(self, func: FunctionNode):
        """
        Genera un comentario en el archivo mips que indica la signatura de la funcion que se esta creando.
        """
        self.register_instruction(
            instrNodes.LineComment(f"{func.name} implementation."))
        self.register_instruction(instrNodes.LineComment("@Params:"))
        for i, param in enumerate(func.params):
            if i < 4:
                self.register_instruction(
                    instrNodes.LineComment(f"\t$a{i} = {param}"))
            else:
                self.register_instruction(
                    instrNodes.LineComment(f"\t{(i-4) * 4}($fp) = {param}"))

    def operate(self, dest, left, right, operand: Type):
        """
        Realiza la operacion indicada por operand entre left y right
        y la guarda en dest.
        """
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
                self.register_instruction(operand(reg, reg, right_reg))
            else:
                # rigth es una constante
                self.register_instruction(operand(reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False
        else:
            # left es una constante
            reg = self.get_available_register()
            right_reg = self.get_available_register()
            assert right_reg is not None
            assert reg is not None
            self.register_instruction(lsNodes.LI(reg, left))
            if not isinstance(right, int):
                self.register_instruction(lsNodes.LW(right_reg, right))
                self.register_instruction(operand(reg, reg, right_reg))
            else:
                self.register_instruction(operand(reg, reg, right, True))
            self.register_instruction(lsNodes.SW(reg, dest))
            self.used_registers[reg] = self.used_registers[right_reg] = False

    def create_type_array(self, types: List[TypeNode]):
        """
        Crea en la seccion .data una secuencia de labels que referencian
        los distintos tipos del programa, de modo que se puedan referenciar en 
        mips como mismo se referenciarian en una lista.
        """
        self.register_instruction(DotDataDirective())

        # Generar por cada tipo, un label que lo identifique, en el mismo orden que aparecen
        # en la lista de tipos.
        for t in types:
            self.register_instruction(instrNodes.Label(t.name))

    def allocate_memory(self, bytes_num: int):
        """
        Reserva @bytes_num bytes en heap y devuelve la direccion de memoria asignada
        en $v0.
        """
        self.register_instruction(
            instrNodes.LineComment(f"Allocating {bytes_num} of memory"))

        # Cargar la cantidad de bytes en el registro $a0
        self.register_instruction(load_store.LI(a0, bytes_num))

        # $v0 = 9 (syscall 9 = sbrk)
        self.register_instruction(load_store.LI(v0, 9))

        # syscall
        self.register_instruction(instrNodes.SYSCALL())
        # la direccion del espacio en memoria esta ahora en v0

    def conditional_jump(self, node, condition, value=0, const=True):
        """
        Realiza un salto condicional en dependencia de la condicion especificada 
        en @condition y toma por valor de comparacion @value. @const indica si @value
        debe tomarse como una constante o como un registro.
        """
        addr = self.get_location_address(node.variable)
        reg = self.get_available_register()

        assert reg is not None, "Out of registers"

        self.add_source_line_comment(node)

        self.register_instruction(lsNodes.LW(reg, addr))
        # Comparar y saltar
        self.register_instruction(condition(reg, value, node.label, const))

        self.used_registers[reg] = False

    def allocate_stack_frame(self, node: FunctionNode):
        """
        Crea el marco de pila necesario para ejecutar la funcion representada por @node.
        """
        # Crear el marco de pila para la funcion
        locals_count = len(node.localvars)
        self.register_instruction(
            instrNodes.LineComment(
                f"Allocate stack frame for function {node.name}."))

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

    def deallocate_stack_frame(self, node: FunctionNode):
        """
        Deshace el marco de pila creado por un llamado a @allocate_stack_frame anterior.
        Esta funcion solo es un espejo de lo que realiza @allocate_stack_frame.
        """
        locals_count = len(node.localvars)
        self.register_instruction(
            instrNodes.LineComment(
                f"Deallocate stack frame for function {node.name}."))

        # Calcular cuantos bytes fueron reservados
        if locals_count * 4 < 24:  # MIPS fuerza a un minimo de 32 bytes por stack frame
            ret = 32
        else:
            ret = locals_count * 4 + 8

        # restaurar ra y fp
        self.comment("Restore $ra")
        self.register_instruction(lsNodes.LW(ra, "8($sp)"))
        self.comment("Restore $fp")
        self.register_instruction(lsNodes.LW(fp, "4($sp)"))

        # restaurar el Stack Pointer
        self.register_instruction(
            instrNodes.LineComment("Restore Stack pointer $sp"))
        self.register_instruction(arithNodes.ADDU(sp, sp, ret, True))

    def get_method_index(self, method: str):
        """
        Devuelve el indice de un metodo en las tablas virtuales.
        Los metodos, ocupan el mismo indice en todas las vtables que aparezcan.
        """
        for typ in self.types:
            for i, (methodName, _) in enumerate(typ.methods):
                if methodName == method:
                    return i
        return 0

    def comment(self, message: str):
        self.register_instruction(instrNodes.LineComment(message))