class Node:
    pass


class ProgramNode(Node):
    def __init__(self, types, data, code, built_in_code):
        self.types = types
        self.data = data
        self.code = code
        self.built_in_code = built_in_code


class TypeNode(Node):
    def __init__(self, type):
        self.attributes = []
        self.methods = {}
        self.type = type


class DataNode(Node):
    def __init__(self, id, val):
        self.id = id
        self.val = val


class FuncNode(Node):
    def __init__(self, name, params, locals, body):
        self.name = name
        self.params = params
        self.locals = locals
        self.body = body


class InstructionNode(Node):
    def __init__(self):
        self.locals = []

    def check_local(self, var):
        if type(var) is LocalNode:
            self.locals.append(var)


class LocalNode(Node):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class ParamNode(Node):
    def __init__(self, id):
        self.id = id


class AssignNode(InstructionNode):
    def __init__(self, id, val):
        super().__init__()
        self.id = id
        self.val = val
        self.check_local(id)
        self.check_local(val)


class ArithNode(InstructionNode):
    def __init__(self, left, right, result):
        super().__init__()
        self.left = left
        self.right = right
        self.result = result
        self.check_local(left)
        self.check_local(right)
        self.check_local(result)


class PlusNode(ArithNode):
    pass


class MinusNode(ArithNode):
    pass


class StarNode(ArithNode):
    pass


class DivNode(ArithNode):
    pass


class LessEqNode(ArithNode):
    pass


class LessNode(ArithNode):
    pass


class NotNode(InstructionNode):
    def __init__(self, value, result):
        super().__init__()
        self.value = value
        self.result = result
        self.check_local(value)
        self.check_local(result)


class GetAttrNode(InstructionNode):
    def __init__(self, obj, attr, result):
        super().__init__()
        self.attr = attr
        self.obj = obj
        self.result = result
        self.check_local(obj)
        self.check_local(result)


class SetAttrNode(InstructionNode):
    def __init__(self, obj, attr, val):
        super().__init__()
        self.val = val
        self.obj = obj
        self.attr = attr
        self.check_local(obj)
        self.check_local(val)


class SetIndexNode(InstructionNode):
    def __init__(self, array, index, val):
        self.val = val
        self.array = array
        self.index = index


class GetIndexNode(InstructionNode):
    def __init__(self, array, index, result):
        self.result = result
        self.array = array
        self.index = index


class AllocateNode(InstructionNode):
    def __init__(self, _type, addr):
        super().__init__()
        self.type = _type
        self.addr = addr
        self.check_local(addr)


class AbortNode(InstructionNode):
    pass


class ReadIntNode(InstructionNode):
    def __init__(self, result):
        self.result = result


class CopyNode(InstructionNode):
    def __init__(self, val, result):
        self.result = result
        self.val = val


class TypeOfNode(InstructionNode):
    def __init__(self, result, var):
        super().__init__()
        self.result = result
        self.var = var
        self.check_local(result)
        self.check_local(var)


class ArrayNode(InstructionNode):
    def __init__(self, len, result):
        self.len = len
        self.result = result


class CallNode(InstructionNode):
    def __init__(self, method, result):
        self.method = method
        self.result = result


class VCAllNode(InstructionNode):
    def __init__(self, type, method, result):
        super().__init__()
        self.method = method
        self.type = type
        self.result = result
        self.check_local(result)
        self.check_local(type)


class ArgNode(InstructionNode):
    def __init__(self, val):
        super().__init__()
        self.val = val
        self.check_local(val)


class ConditionalGotoNode(InstructionNode):
    def __init__(self, predicate, label):
        super().__init__()
        self.predicate = predicate
        self.label = label
        self.check_local(predicate)


class GotoNode(InstructionNode):
    def __init__(self, label):
        super().__init__()
        self.label = label


class LabelNode(InstructionNode):
    def __init__(self, label_name):
        super().__init__()
        self.label_name = label_name


class ReturnNode(InstructionNode):
    def __init__(self, ret_value):
        super().__init__()
        self.ret_value = ret_value
        self.check_local(ret_value)


class LoadNode(InstructionNode):
    def __init__(self, addr, result):
        super().__init__()
        self.result = result
        self.addr = addr
        self.check_local(result)


class LengthNode(InstructionNode):
    def __init__(self, str, result):
        self.result = result
        self.str = str


class ConcatNode(InstructionNode):
    def __init__(self, str_a, str_b, result):
        self.result = result
        self.str_a = str_a
        self.str_b = str_b


class SubStringNode(InstructionNode):
    def __init__(self, str, i, len, result):
        self.result = result
        self.i = i
        self.len = len
        self.str = str


class StrNode(InstructionNode):
    def __init__(self, val, str):
        super().__init__()
        self.str = str
        self.val = val
        self.check_local(val)
        self.check_local(str)


class ReadNode(InstructionNode):
    def __init__(self, val):
        super().__init__()
        self.val = val
        self.check_local(val)


class PrintNode(InstructionNode):
    def __init__(self, str):
        super().__init__()
        self.str = str
        self.check_local(str)
