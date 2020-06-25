import mips.instruction as instrNodes
import mips.branch as branchNodes
import mips.comparison as cmpNodes
import mips.arithmetic as arithNodes
import mips.load_store as lsNodes
from typing import List, Optional
import time
import cil.nodes as cil


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

        # Construir el header del programa.
        self.__program_header()

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
        self.register_instruction(instrNodes.LineComment(coolc))
        self.register_instruction(instrNodes.LineComment(f'{ep}, {la}, {ad} --- {date}'))
        self.register_instruction(instrNodes.LineComment(institution))

