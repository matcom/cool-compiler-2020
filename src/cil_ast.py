# clase base del AST del lenguaje CIL
class Node:
    pass

# nodo del programa
class ProgramNode(Node):
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code

# nodo de los tipos
class TypeNode(Node):
    def __init__(self, type_name, attributes_owner, attributes, methods):
        self.attributes_owner = attributes_owner
        self.attributes = attributes
        self.methods = methods
        self.type_name = type_name

    def GetCode(self):
        result = ""
        result += "\ttype " + self.type_name + " {"

        for key in self.attributes_owner.keys():
            result += "\n\t\tattribute " + key + ":" + self.attributes_owner[key]

        for key in self.methods.keys():
            result += "\n\t\tmethod " + key + ":" + self.methods[key] + "_" + key

        result += "\n\t}"

        return result

# nodo de los datos que se definen en la region .data del MIPS
class DataNode(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def GetCode(self):
        if type(self.value) == type("asd"):
            new_value = self.value.replace("\n", "\\n")
        else:
            new_value = str(self.value)
        return "\t" + self.id + " \"" + new_value + "\""

# nodo de funciones
class FunctionNode(Node):
    def __init__(self, name, params, locals, body):
        self.name = name
        self.params = params
        self.locals = locals
        self.body = body

    def GetCode(self):
        result = "\tfunction " + self.name + " {\n"
        for p in self.params:
            result += "\t\t" + p.GetCode() + "\n"
        for l in self.locals:
            result += "\t\t" + l.GetCode() + "\n"
        for s in self.body:
            result += "\t\t" + s.GetCode() + "\n"

        result += "\t}"

        return result


# nodo base de instrucciones en CIL
class InstructionNode(Node):
    pass

# nodo para variables locales
class LocalNode(Node):
    def __init__(self, id):
        self.id = id

    def GetCode(self):
        return "LOCAL " + self.id

    def __str__(self):
        return str(self.id)

# nodo para la operacion de salvado de variables locales
class LocalSaveNode(Node):
    def GetCode(self):
        return "LOCALSAVE"

# nodo para parametros de funciones
class ParamNode(Node):
    def __init__(self, id):
        self.id = id

    def GetCode(self):
        return "PARAM " + self.id

    def __str__(self):
        return str(self.id)

# nodo para la operacion mov
class MovNode(InstructionNode):
    def __init__(self, result, value):
        self.result = result
        self.value = value

    def GetCode(self):
        return "MOV " + str(self.result) + " " + str(self.value)
    
# nodo base de operaciones unarias
class UnaryOpNode(InstructionNode):
    def __init__(self, value, result):
        self.value = value
        self.result = result

# nodo de la operacion not
class NtNode(UnaryOpNode):
    def GetCode(self):
        return "NOT " + str(self.result) + " " + str(self.value)

# nodo de la operacion de complemento de entero
class CmpNode(UnaryOpNode):
    def GetCode(self):
        return "CMP " + str(self.result) + " " + str(self.value)

# nodo de la operacion isvoid
class VDNode(UnaryOpNode):
    def GetCode(self):
        return "VD " + str(self.result) + " " + str(self.value)

# nodo base de las operaciones binarias
class BinaryOpNode(InstructionNode):
    def __init__(self, left, right, result):
        self.left = left
        self.right = right
        self.result = result

# nodo de la operacion suma
class AddNode(BinaryOpNode):
    def GetCode(self):
        return "ADD " + str(self.result) + " " + str(self.left) + " " + str(self.right)

# nodo de la operacion resta
class SubNode(BinaryOpNode):
    def GetCode(self):
        return "SUB " + str(self.result) + " " + str(self.left) + " " + str(self.right)

# nodo de la operacion multiplicacion
class MulNode(BinaryOpNode):
    def GetCode(self):
        return "Mul " + str(self.result) + " " + str(self.left) + " " + str(self.right)

# nodo de la operacion division
class DivNode(BinaryOpNode):
    def GetCode(self):
        return "Div " + str(self.result) + " " + str(self.left) + " " + str(self.right)

# nodo de la operacion <=
class LENode(BinaryOpNode):
    def GetCode(self):
        return "LE " + str(self.result) + " " + str(self.left) + " " + str(self.right)

# nodo de la operacion <
class LNode(BinaryOpNode):
    def GetCode(self):
        return "L " + str(self.result) + " " + str(self.left) + " " + str(self.right)

# nodo de la operacion =
class ENode(BinaryOpNode):
    def GetCode(self):
        return "E " + str(self.result) + " " + str(self.left) + " " + str(self.right)

# nodo de la operacion que pide un atributo de un objeto
class GetAttributeNode(InstructionNode):
    def __init__(self, _type, value, attr, result):
        self.type_name = _type
        self.value = value
        self.attr = attr
        self.result = result

    def GetCode(self):
        return "GATTR " + str(self.result) + " " + str(self.value) + " " + str(self.attr)

# nodo de la operacion que modifica un atributo de un objeto
class SetAttributeNode(InstructionNode):
    def __init__(self, _type, instance, attr, value):
        self.type_name = _type
        self.value = value
        self.instance = instance
        self.attr = attr

    def GetCode(self):
        return "SATTR " + str(self.instance) + " " + str(self.attr) + " " + str(self.value)

# nodo de la operacion de crear inicializar una variable local
class AllocateNode(InstructionNode):
    def __init__(self, _type, result):
        self.type = _type
        self.result = result

    def GetCode(self):
        return "ALLOC " + str(self.result) + " " + str(self.type)

# nodo de la operacion de salida del programa
class AbortNode(InstructionNode):
    def __init__(self, caller_type):
        self.caller_type = caller_type
    def GetCode(self):
        return "EXIT"

# nodo de la operacion de copiar una valor de una variable local en otra 
class CopyNode(InstructionNode):
    def __init__(self, value, result):
        self.result = result
        self.value = value

    def GetCode(self):
        return "COPY " + str(self.result) + " " + str(self.value)

# nodo de la operacion que devuelve el entero que representa el tipo
class TypeOfNode(InstructionNode):
    def __init__(self, result, variable):
        self.result = result
        self.variable = variable

    def GetCode(self):
        return "TYPE " + str(self.result) + " " + str(self.variable)

# nodo de la operacion de llamado de una funcion
class DispatchCallNode(InstructionNode):
    def __init__(self, type_addr, method, result):
        self.type_addr = type_addr
        self.method = method
        self.result = result

    def GetCode(self):
        return "CALL " + str(self.result) + " " + str(self.type_addr) + " " + str(self.method)

# nodo de la operacion de agragar un argumento para la proxima funcion que se llame
class ArgNode(InstructionNode):
    def __init__(self, value):
        self.value = value

    def GetCode(self):
        return "ARG " + str(self.value)

# nodo de la operacion condicional
class IfGotoNode(InstructionNode):
    def __init__(self, predicate, label):
        self.predicate = predicate
        self.label = label
    
    def GetCode(self):
        return "IF " + str(self.predicate) + " GOTO " + self.label

# nodo de la operacion de salto incondicional
class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label

    def GetCode(self):
        return "GOTO " + self.label

# nodo para las etiquetas de salto
class LabelNode(InstructionNode):
    def __init__(self, label_name):
        self.label_name = label_name

    def GetCode(self):
        return "LABEL " + self.label_name

# nodo de la operacion de retorno de funciones
class ReturnNode(InstructionNode):
    def __init__(self, return_value = ""):
        self.return_value = return_value

    def GetCode(self):
        return "RETURN " + str(self.return_value)

# nodo de la operacion de strlen
class StrlenNode(InstructionNode):
    def __init__(self, str, result):
        self.result = result
        self.str = str

    def GetCode(self):
        return "STRLEN " + str(self.result) + " " + self.str

# nodo de la operacion concat
class StrcatNode(InstructionNode):
    def __init__(self, str_a, str_b, result):
        self.result = result
        self.str_a = str_a
        self.str_b = str_b

    def GetCode(self):
        return "STRCAT " + str(self.result) + " " + str(self.str_a) + " " + str(self.str_b)

# nodo de la operacion strsub
class StrsubNode(InstructionNode):
    def __init__(self, str, i, len, result):
        self.str = str
        self.i = i
        self.len = len
        self.result = result

    def GetCode(self):
        return "STRSUB " + str(self.result) + " " + str(self.str) + " " + str(self.i) + " " + str(self.len)

# nodo de la expresion de cargar un dato en una variable local
class LoadDataNode(InstructionNode):
    def __init__(self, result, data):
        self.data = data
        self.result = result

    def GetCode(self):
        return "LDATA " + str(self.result) + " " + str(self.data)

# nodo de la expresion que calcula si el tipo de una variable local hereda de otro
class IsSonNode(InstructionNode):
    def __init__(self, class_son, class_father, result):
        self.son = class_son
        self.father = class_father
        self.result = result

    def GetCode(self):
        return "ISSON " + self.son + " " + self.father + " " + self.result


# nodo de la expresion que lee una cadena de entrada
class ReadNode(InstructionNode):
    def __init__(self, result):
        self.result = result

    def GetCode(self):
        return "READ " + str(self.result)

# nodo de la operacion de leer un entero
class ReadIntNode(InstructionNode):
    def __init__(self, result):
        self.result = result
    
    def GetCode(self):
        return "RINT " + str(self.result)

# nodo de la operacion de imprimir una cadena 
class PrintNode(InstructionNode):
    def __init__(self, str):
        self.str = str

    def GetCode(self):
        return "PRINT " + str(self.str)

# nodo de la operacion de imprimir un entero
class PrintIntNode(InstructionNode):
    def __init__(self, val):
        self.val = val

    def GetCode(self):
        return "PINT " + str(self.val)

# nodo de la operacion que a partir de una variable entera ponga en otra que 
# es una cadena de caracteres el nombre del tipo que representa dicho entero
class TypeNameNode(InstructionNode):
    def __init__(self, result, type_addr):
        self.result = result
        self.type_addr = type_addr

    def GetCode(self):
        return "TYPENAME " + str(self.result) + " " + str(self.type_addr)

# nodo de la operacion que a partir de una cadena de caracteres pone en una variable local
# el entero que representa ese tipo
class TypeAddressNode(InstructionNode):
    def __init__(self, result, type_name):
        self.result = result
        self.type_name = type_name

    def GetCode(self):
        return "TYPEADDR " + str(self.result) + " " + str(self.type_name)