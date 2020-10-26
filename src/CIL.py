class CILInstructionNode:
    def __init__(destination=None, params=[]):
        self.destination=destination
        self.params=params

class CILBinaryOperator(CILInstructionNode):
    pass

class CILAritmetic(CILBinaryOperator):
    pass

class CILComparison(CILBinaryOperator):
    pass

class CILPlus(CILAritmetic):
    pass
class CILMinus(CILAritmetic):
    pass
class CILMult(CILAritmetic):
    pass
class CILDiv(CILAritmetic):
    pass

class CILLesser(CILComparison):
    pass
class CILLesserEqual(CILComparison):
    pass
class CILEqual(CILComparison):
    pass
class CILDifferent(CILComparison):
    pass

class CILLabel(CILInstructionNode):
    pass
class CILConditionalJump(CILInstructionNode):
    pass
class CILJump(CILInstructionNode):
    pass

class CILUnaryOperator(CILInstructionNode):
    pass
class CILNot(CILUnaryOperator):
    pass
class CILComplement(CILUnaryOperator):
    pass
class CILIsVoid(CILUnaryOperator):
    pass
class CILAssign(CILUnaryOperator):
    pass

class CILMemory(CILInstructionNode):
    pass
class CILAllocate(CILMemory):
    pass

class CILMethodInstruction(CILInstructionNode):
    pass
class CILCall(CILMethodInstruction):
    pass
class CILVirtualCall(CILMethodInstruction):
    pass
class CILArgument(CILMethodInstruction):
    pass
class CILReturn(CILMethodInstruction):
    pass


class CILClassMethod:
    def __init__(localname,globalname):
        self.localname=localname
        self.globalname=globalname

class CILAttribute:
    def __init__(name):
        self.name=name

class CILClass:
    def __init__(name,listaAtributos=[], listaMetodos=[]):
        self.name=name
        self.listaAtributos=listaAtributos
        self.listaMetodos=listaMetodos

class CILDataDeclaration:
    def __init__(nombre, valorString):
        self.nombre=nombre
        self.valorString=valorString

class CILGlobalMethod:
    def __init__(nombre, params=[], locals=[], intrucciones=[]):
        self.nombre=nombre
        self.params=params
        self.intrucciones=intrucciones

class CILProgram:
    def __init__(Types=[],Data=[],Methods=[]):
        self.Types=Types
        self.Data=Data
        self.Methods=Methods