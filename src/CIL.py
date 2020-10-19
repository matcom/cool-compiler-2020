class CILInstructionNode:
    def __init__(destination=None, params=[]):
        self.destination=destination
        self.params=params

class CILClassMethod:
    def __init__(localname,globalname):
        self.localname=localname
        self.globalname=globalname

class CILAttribute:
    def __init__(name):
        self.name=name

class CILClass:
    def __init__(listaAtributos=[], listaMetodos=[]):
        self.listaAtributos=listaAtributos
        self.listaMetodos=listaMetodos

class CILDataDeclaration:
    def __init__(nombre, valorString):
        self.nombre=nombre
        self.valorString=valorString

class CILGlobalMethod:
    def __init__(nombre, intrucciones=[]):
        self.nombre=nombre
        self.intrucciones=intrucciones

class CILProgram:
    def __init__(Types=[],Data=[],Methods=[]):
        self.Types=Types
        self.Data=Data
        self.Methods=Methods