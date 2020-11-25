class Node:
    pass


class ProgramNode(Node):
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code


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


class DataNode(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def GetCode(self):
        new_value = self.value.replace("\n", "\\n")
        return "\t" + self.id + " \"" + new_value + "\""


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


class InstructionNode(Node):
    pass


class LocalNode(Node):
    def __init__(self, id):
        self.id = id

    def GetCode(self):
        return "LOCAL " + self.id

    def __str__(self):
        return str(self.id)


class ParamNode(Node):
    def __init__(self, id):
        self.id = id

    def GetCode(self):
        return "PARAM " + self.id

    def __str__(self):
        return str(self.id)


class MovNode(InstructionNode):
    def __init__(self, result, value):
        self.result = result
        self.value = value

    def GetCode(self):
        return "MOV " + str(self.result) + " " + str(self.value)
    

class UnaryOpNode(InstructionNode):
    def __init__(self, value, result):
        self.value = value
        self.result = result


class NtNode(UnaryOpNode):
    def GetCode(self):
        return "NOT " + str(self.result) + " " + str(self.value)


class CmpNode(UnaryOpNode):
    def GetCode(self):
        return "CMP " + str(self.result) + " " + str(self.value)


class VDNode(UnaryOpNode):
    def GetCode(self):
        return "VD " + str(self.result) + " " + str(self.value)


class BinaryOpNode(InstructionNode):
    def __init__(self, left, right, result):
        self.left = left
        self.right = right
        self.result = result


class AddNode(BinaryOpNode):
    def GetCode(self):
        return "ADD " + str(self.result) + " " + str(self.left) + " " + str(self.right)


class SubNode(BinaryOpNode):
    def GetCode(self):
        return "SUB " + str(self.result) + " " + str(self.left) + " " + str(self.right)


class MulNode(BinaryOpNode):
    def GetCode(self):
        return "Mul " + str(self.result) + " " + str(self.left) + " " + str(self.right)

class DivNode(BinaryOpNode):
    def GetCode(self):
        return "Div " + str(self.result) + " " + str(self.left) + " " + str(self.right)


class LENode(BinaryOpNode):
    def GetCode(self):
        return "LE " + str(self.result) + " " + str(self.left) + " " + str(self.right)

class LNode(BinaryOpNode):
    def GetCode(self):
        return "L " + str(self.result) + " " + str(self.left) + " " + str(self.right)

class ENode(BinaryOpNode):
    def GetCode(self):
        return "E " + str(self.result) + " " + str(self.left) + " " + str(self.right)


class GetAttributeNode(InstructionNode):
    def __init__(self, _type, value, attr, result):
        self.type_name = _type
        self.value = value
        self.attr = attr
        self.result = result

    def GetCode(self):
        return "GATTR " + str(self.result) + " " + str(self.value) + " " + str(self.attr)


class SetAttributeNode(InstructionNode):
    def __init__(self, _type, instance, attr, value):
        self.type_name = _type
        self.value = value
        self.instance = instance
        self.attr = attr

    def GetCode(self):
        return "SATTR " + str(self.instance) + " " + str(self.attr) + " " + str(self.value)


class AllocateNode(InstructionNode):
    def __init__(self, _type, result):
        self.type = _type
        self.result = result

    def GetCode(self):
        return "ALLOC " + str(self.result) + " " + str(self.type)


class AbortNode(InstructionNode):
    def GetCode(self):
        return "EXIT"


class ReadIntNode(InstructionNode):
    def __init__(self, result):
        self.result = result
    
    def GetCode(self):
        return "RINT " + str(self.result)


class CopyNode(InstructionNode):
    def __init__(self, value, result):
        self.result = result
        self.value = value

    def GetCode(self):
        return "COPY " + str(self.result) + " " + str(self.value)


class TypeOfNode(InstructionNode):
    def __init__(self, result, variable):
        self.result = result
        self.variable = variable

    def GetCode(self):
        return "TYPE " + str(self.result) + " " + str(self.variable)


class DispatchCallNode(InstructionNode):
    def __init__(self, type_name, method, result):
        self.type_name = type_name
        self.method = method
        self.result = result

    def GetCode(self):
        return "CALL " + str(self.result) + " " + str(self.type_name) + " " + str(self.method)


class ArgNode(InstructionNode):
    def __init__(self, value):
        self.value = value

    def GetCode(self):
        return "ARG " + str(self.value)


class IfGotoNode(InstructionNode):
    def __init__(self, predicate, label):
        self.predicate = predicate
        self.label = label
    
    def GetCode(self):
        return "IF " + str(self.predicate) + " GOTO " + self.label


class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label

    def GetCode(self):
        return "GOTO " + self.label


class LabelNode(InstructionNode):
    def __init__(self, label_name):
        self.label_name = label_name.id

    def GetCode(self):
        return "LABEL " + self.label_name


class ReturnNode(InstructionNode):
    def __init__(self, return_value = ""):
        self.return_value = return_value

    def GetCode(self):
        return "RETURN " + str(self.return_value)


class StrlenNode(InstructionNode):
    def __init__(self, str, result):
        self.result = result
        self.str = str

    def GetCode(self):
        return "STRLEN " + str(self.result) + " " + self.str


class StrcatNode(InstructionNode):
    def __init__(self, str_a, str_b, result):
        self.result = result
        self.str_a = str_a
        self.str_b = str_b

    def GetCode(self):
        return "STRCAT " + str(self.result) + " " + str(self.str_a) + " " + str(self.str_b)

class LoadDataNode(InstructionNode):
    def __init__(self, result, data):
        self.data = data
        self.result = result

    def GetCode(self):
        return "LDATA " + str(self.result) + " " + str(self.data)


class SetStringNode(InstructionNode):
    def __init__(self, result, str):
        self.str = str
        self.result = result

    def GetCode(self):
        return "SETSTR " + str(self.result) + " " + str(self.str)


class StrsubNode(InstructionNode):
    def __init__(self, str, i, len, result):
        self.str = str
        self.i = i
        self.len = len
        self.result = result

    def GetCode(self):
        return "STRSUB " + str(self.result) + " " + str(self.str) + " " + str(self.i) + " " + str(self.len)

class ToStrNode(InstructionNode):
    def __init__(self, value, result):
        self.result = result
        self.value = value

    def GetCode(self):
        return "TOSTR " + str(self.result) + " " + str(self.value)


class ReadNode(InstructionNode):
    def __init__(self, result):
        self.result = result

    def GetCode(self):
        return "READ " + str(self.result)


class PrintNode(InstructionNode):
    def __init__(self, str):
        self.str = str

    def GetCode(self):
        return "PRINT " + str(self.str)
