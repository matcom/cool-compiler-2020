class Node:
    pass


class ProgramNode(Node):
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code


class TypeNode(Node):
    def __init__(self, type_name, attributes, methods):
        self.attributes = attributes
        self.methods = methods
        self.type_name = type_name

    def GetCode(self):
        result = ""
        result += "\ttype " + self.type_name + " {"

        for key in self.attributes.keys():
            result += "\n\t\tattribute " + key + ":" + self.attributes[key]

        for key in self.methods.keys():
            result += "\n\t\tmethod " + key + ":" + self.methods[key] + "_" + key

        result += "\n\t}"

        return result


class DataNode(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def GetCode(self):
        return "\t" + self.id + " \"" + self.value + "\""


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
    def __init__(self):
        self.locals = []

    def check_local(self, var):
        if type(var) is LocalNode:
            self.locals.append(var)


class LocalNode(Node):
    def __init__(self, id):
        self.id = id

    def GetCode(self):
        return "LOCAL " + self.id


class ParamNode(Node):
    def __init__(self, id):
        self.id = id

    def GetCode(self):
        return "PARAM " + self.id


class MovNode(InstructionNode):
    def __init__(self, result, value):
        super().__init__()
        self.result = result
        self.value = value
        self.check_local(result)
        self.check_local(value)

    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.value
        if type(b) == LocalNode:
            b = b.id
        return "MOV " + str(a) + " " + str(b)
    

class UnaryOpNode(InstructionNode):
    def __init__(self, value, result):
        super().__init__()
        self.value = value
        self.result = result
        self.check_local(value)
        self.check_local(result)

class NtNode(UnaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.value
        if type(b) == LocalNode:
            b = b.id
        return "NOT " + str(a) + " " + str(b)

class CmpNode(UnaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.value
        if type(b) == LocalNode:
            b = b.id
        return "CMP " + str(a) + " " + str(b)

class VDNode(UnaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.value
        if type(b) == LocalNode:
            b = b.id
        return "VD " + str(a) + " " + str(b)

class BinaryOpNode(InstructionNode):
    def __init__(self, left, right, result):
        super().__init__()
        self.left = left
        self.right = right
        self.result = result
        self.check_local(left)
        self.check_local(right)
        self.check_local(result)


class AddNode(BinaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.left
        if type(b) == LocalNode:
            b = b.id
        c = self.right
        if type(c) == LocalNode:
            c = c.id
        return "ADD " + str(a) + " " + str(b) + " " + str(c)


class SusNode(BinaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.left
        if type(b) == LocalNode:
            b = b.id
        c = self.right
        if type(c) == LocalNode:
            c = c.id
        return "SUS " + str(a) + " " + str(b) + " " + str(c)


class MulNode(BinaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.left
        if type(b) == LocalNode:
            b = b.id
        c = self.right
        if type(c) == LocalNode:
            c = c.id
        return "MUL " + str(a) + " " + str(b) + " " + str(c)

class DivNode(BinaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.left
        if type(b) == LocalNode:
            b = b.id
        c = self.right
        if type(c) == LocalNode:
            c = c.id
        return "DIV " + str(a) + " " + str(b) + " " + str(c)


class LENode(BinaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.left
        if type(b) == LocalNode:
            b = b.id
        c = self.right
        if type(c) == LocalNode:
            c = c.id
        return "LE " + str(a) + " " + str(b) + " " + str(c)

class LNode(BinaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.left
        if type(b) == LocalNode:
            b = b.id
        c = self.right
        if type(c) == LocalNode:
            c = c.id
        return "L " + str(a) + " " + str(b) + " " + str(c)

class ENode(BinaryOpNode):
    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.left
        if type(b) == LocalNode:
            b = b.id
        c = self.right
        if type(c) == LocalNode:
            c = c.id
        return "E " + str(a) + " " + str(b) + " " + str(c)


class GetAttributeNode(InstructionNode):
    def __init__(self, value, attr, result):
        super().__init__()
        self.attr = attr
        self.value = value
        self.result = result
        self.check_local(value)
        self.check_local(result)

    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.value
        if type(b) == LocalNode:
            b = b.id
        c = self.attr
        if type(c) == LocalNode:
            c = c.id
        return "GATTR " + str(a) + " " + str(b) + " " + str(c)


class SetAttributeNode(InstructionNode):
    def __init__(self, instance, attr, value):
        super().__init__()
        self.value = value
        self.instance = instance
        self.attr = attr
        self.check_local(instance)
        self.check_local(value)

    def GetCode(self):
        a = self.instance
        if type(a) == LocalNode:
            a = a.id
        b = self.attr
        if type(b) == LocalNode:
            b = b.id
        c = self.value
        if type(c) == LocalNode:
            c = c.id
        
        return "SATTR " + str(a) + " " + str(b) + " " + str(c)
        

class SetIndexNode(InstructionNode):
    def __init__(self, array, index, value):
        self.value = value
        self.array = array
        self.index = index

    def GetCode(self):
        return "SINDEX " + self.array + " " + self.index + " " + self.value


class GetIndexNode(InstructionNode):
    def __init__(self, array, index, result):
        self.result = result
        self.array = array
        self.index = index

    def GetCode(self):
        return "GINDEX " + self.result + " " + self.array + " " + self.index   


class AllocateNode(InstructionNode):
    def __init__(self, _type, result):
        super().__init__()
        self.type = _type
        self.result = result
        self.check_local(result)

    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.type
        if type(b) == LocalNode:
            b = b.id
        return "ALLOC " + str(a) + " " + str(b)


class AbortNode(InstructionNode):
    def GetCode(self):
        return "EXIT"


class ReadIntNode(InstructionNode):
    def __init__(self, result):
        self.result = result
    
    def GetCode(self):
        return "RINT " + self.result


class CopyNode(InstructionNode):
    def __init__(self, value, result):
        self.result = result
        self.value = value

    def GetCode(self):
        return "COPY " + self.result + " " + self.value


class TypeOfNode(InstructionNode):
    def __init__(self, result, variable):
        super().__init__()
        self.result = result
        self.variable = variable
        self.check_local(result)
        self.check_local(variable)

    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = self.result.id
        b = self.variable
        if type(b) == LocalNode:
            b = self.result.id
        return "TYPE " + str(a) + " " + str(b)


class ArrayNode(InstructionNode):
    def __init__(self, lenght, result):
        self.lenght = lenght
        self.result = result

    def GetCode(self):
        return "ARRAY " + self.result + " " + self.lenght


class DispatchCallNode(InstructionNode):
    def __init__(self, type_name, method, result):
        super().__init__()
        self.method = method
        self.type_name = type_name
        self.result = result
        self.check_local(result)
        self.check_local(type_name)

    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = self.result.id
        b = self.type_name
        if type(b) == LocalNode:
            b = self.type_name.id
        return "VCALL " + a + " " + b + " " + self.method


class ArgNode(InstructionNode):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.check_local(value)

    def GetCode(self):
        a = self.value
        if type(a) == LocalNode:
            a = a.id
        return "ARG " + str(a)


class IfGotoNode(InstructionNode):
    def __init__(self, predicate, label):
        super().__init__()
        self.predicate = predicate
        self.label = label
        self.check_local(predicate)
    
    def GetCode(self):
        a = self.predicate
        if type(a) == LocalNode:
            a = a.id
        return "IF " + str(a) + " GOTO " + self.label


class GotoNode(InstructionNode):
    def __init__(self, label):
        super().__init__()
        self.label = label

    def GetCode(self):
        return "GOTO " + self.label


class LabelNode(InstructionNode):
    def __init__(self, label_name):
        super().__init__()
        self.label_name = label_name

    def GetCode(self):
        return "LABEL " + self.label_name


class ReturnNode(InstructionNode):
    def __init__(self, ret_value = ""):
        super().__init__()
        self.ret_value = ret_value
        self.check_local(ret_value)

    def GetCode(self):
        a = self.ret_value
        if type(a) == LocalNode:
            a = a.id
        return "RETURN " + str(a)


class LoadNode(InstructionNode):
    def __init__(self, addr, result):
        super().__init__()
        self.result = result
        self.addr = addr
        self.check_local(result)

    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.id
        b = self.addr
        if type(b) == LocalNode:
            b = b.id
        return "LOAD " + str(a) + " " + str(b)


class StrlenNode(InstructionNode):
    def __init__(self, str, result):
        self.result = result
        self.str = str

    def GetCode(self):
        return "STRLEN " + self.result + " " + self.str


class StrcatNode(InstructionNode):
    def __init__(self, str_a, str_b, result):
        self.result = result
        self.str_a = str_a
        self.str_b = str_b

    def GetCode(self):
        return "STRCAT " + self.result + " " + self.str_a + " " + self.str_b


class StrsubNode(InstructionNode):
    def __init__(self, str, i, len, result):
        self.result = result
        self.i = i
        self.len = len
        self.str = str

    def GetCode(self):
        return "STRSUB " + self.result + " " + self.str + " " + self.i + " " + self.len

class ToStrNode(InstructionNode):
    def __init__(self, value, result):
        super().__init__()
        self.result = result
        self.value = value
        self.check_local(value)
        self.check_local(result)

    def GetCode(self):
        a = self.result
        if type(a) == LocalNode:
            a = a.GetCode()
        b = self.value
        if type(b) == LocalNode:
            b = b.GetCode()
        return "TOSTR " + str(a) + " " + str(b)

class ReadNode(InstructionNode):
    def __init__(self, result):
        super().__init__()
        self.result = result
        self.check_local(result)

    def GetCode(self):
        return "READ " + self.result


class PrintNode(InstructionNode):
    def __init__(self, str):
        super().__init__()
        self.str = str
        self.check_local(str)

    def GetCode(self):
        return "PRINT " + self.str

