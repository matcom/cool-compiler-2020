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


class AssignNode(InstructionNode):
    def __init__(self, result, value):
        super().__init__()
        self.result = result
        self.value = value
        self.check_local(result)
        self.check_local(val)

    def GetCode(self):
        return "MOV " + self.result + " " + self.value
        

class UnaryOpNode(InstructionNode):
    def __init__(self, value, result):
        super().__init__()
        self.value = value
        self.result = result
        self.check_local(value)
        self.check_local(result)

class NotNode(UnaryOpNode):
    def GetCode(self):
        return "NOT " + self.result + " " + self.value

class BinaryOpNode(InstructionNode):
    def __init__(self, left, right, result):
        super().__init__()
        self.left = left
        self.right = right
        self.result = result
        self.check_local(left)
        self.check_local(right)
        self.check_local(result)


class PlusNode(BinaryOpNode):
    def GetCode(self):
        return "ADD " + self.result + " " + self.left + self.right


class MinusNode(BinaryOpNode):
    def GetCode(self):
        return "SUS " + self.result + " " + self.left + self.right


class StarNode(BinaryOpNode):
    def GetCode(self):
        return "MUL " + self.result + " " + self.left + self.right


class DivNode(BinaryOpNode):
    def GetCode(self):
        return "DIV " + self.result + " " + self.left + self.right


class LessEqNode(BinaryOpNode):
    def GetCode(self):
        return "LE " + self.result + " " + self.left + self.right


class LessNode(BinaryOpNode):
    def GetCode(self):
        return "L " + self.result + " " + self.left + self.right


class GetAttributeNode(InstructionNode):
    def __init__(self, value, attr, result):
        super().__init__()
        self.attr = attr
        self.value = value
        self.result = result
        self.check_local(value)
        self.check_local(result)

    def GetCode(self):
        return "GATTR " + self.result + " " + self.value + self.attr


class SetAttributeNode(InstructionNode):
    def __init__(self, instance, attr, value):
        super().__init__()
        self.value = value
        self.instance = instance
        self.attr = attr
        self.check_local(value)
        self.check_local(val)

    def GetCode(self):
        return "SATTR " + self.instance + " " + self.attr + self.value
        

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
        return "ALLOC " + self.result + " " + self.type


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
        return "TYPE " + self.result + " " + self.variable


class ArrayNode(InstructionNode):
    def __init__(self, lenght, result):
        self.lenght = lenght
        self.result = result

    def GetCode(self):
        return "ARRAY " + self.result + " " + self.lenght


class CallNode(InstructionNode):
    def __init__(self, method, result):
        self.method = method
        self.result = result

    def GetCode(self):
        return "CALL " + self.result + " " + self.method


class VCAllNode(InstructionNode):
    def __init__(self, type_name, method, result):
        super().__init__()
        self.method = method
        self.type_name = type_name
        self.result = result
        self.check_local(result)
        self.check_local(type_name)

    def GetCode(self):
        return "VCALL " + self.result + " " + self.type_name + " " + self.method


class ArgNode(InstructionNode):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.check_local(value)

    def GetCode(self):
        return "ARG " + self.value


class ConditionalGotoNode(InstructionNode):
    def __init__(self, predicate, label):
        super().__init__()
        self.predicate = predicate
        self.label = label
        self.check_local(predicate)
    
    def GetCode(self):
        return "IF " + self.predicate + " GOTO " + self.label


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
        return "RETURN " + self.ret_value


class LoadNode(InstructionNode):
    def __init__(self, addr, result):
        super().__init__()
        self.result = result
        self.addr = addr
        self.check_local(result)

    def GetCode(self):
        return "LOAD " + self.result + " " + self.addr


class LengthNode(InstructionNode):
    def __init__(self, str, result):
        self.result = result
        self.str = str

    def GetCode(self):
        return "STRLEN " + self.result + " " + self.str


class ConcatNode(InstructionNode):
    def __init__(self, str_a, str_b, result):
        self.result = result
        self.str_a = str_a
        self.str_b = str_b

    def GetCode(self):
        return "STRCAT " + self.result + " " + self.str_a + " " + self.str_b


class SubStringNode(InstructionNode):
    def __init__(self, str, i, len, result):
        self.result = result
        self.i = i
        self.len = len
        self.str = str

    def GetCode(self):
        return "STRSUB " + self.result + " " + self.str + " " + self.i + " " + self.len

class StrNode(InstructionNode):
    def __init__(self, value, result):
        super().__init__()
        self.result = result
        self.value = value
        self.check_local(value)
        self.check_local(result)

    def GetCode(self):
        return "TOSTR " + self.result + " " + self.value

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

