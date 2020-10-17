class InstructionNode:
    def __init__(destination=None, params=[]):
        self.destination=destination
        self.params=params

class ClassMethod:
    def __init__(localname,globalname):
        self.localname=localname
        self.globalname=globalname

class Attribute:
    def __init__(name):
        self.name=name

class CILClass:
    def __init__(listaAtributos=[], listaMetodos=[]):
        self.listaAtributos=listaAtributos
        self.listaMetodos=listaMetodos

class CILTypes:
    def __init__(listaClases):
        self.listaClases=listaClases

class DataDeclaration:
    def __init__(nombre, valorString):
        self.nombre=nombre
        self.valorString=valorString

class GlobalMethod:
    def __init__(nombre, intrucciones=[]):
        self.nombre=nombre
        self.intrucciones=intrucciones