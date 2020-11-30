class Node:
    pass


class ProgramNode(Node):
    def __init__(self, types, data, code, built_in_code):
        self.types = types
        self.data = data
        self.code = code
        self.built_in_code = built_in_code

    def __str__(self):
        type_code = ''
        data_code = ''
        func_code = ''
        for t in self.types:
            if t.type == 'SELF_TYPE':
                continue
            type_code += f'{str(t)}\n'
        for d in self.data:
            data_code += f'{str(d)}\n'
        for f in self.built_in_code:
            func_code += f'{str(f)}\n'
        for f in self.code:
            func_code += f'{str(f)}\n'

        return f'.TYPES \n\n{type_code}\n.DATA\n\n{data_code}\n.CODE\n\n{func_code}\n'


class TypeNode(Node):
    def __init__(self, type):
        self.attributes = []
        self.methods = {}
        self.type = type

    def __str__(self):
        attr_code = ''
        method_code = ''
        for attr in self.attributes:
            attr_code += f'\tattribute {attr};\n'

        for name in self.methods:
            method_code += f'\tmethod {name}:{self.methods[name]}_{name};\n'

        return f'type {self.type} {{\n{attr_code}{method_code}}}\n'


class DataNode(Node):
    def __init__(self, id, val):
        self.id = id
        self.val = val

    def __str__(self):
        return f'{self.id} = \"{self.val}\" ;'


class FuncNode(Node):
    def __init__(self, name, params, locals, body):
        self.name = name
        self.params = params
        self.locals = locals
        self.body = body

    def __str__(self):
        params_code = ''
        locals_code = ''
        body_code = ''
        for param in self.params:
            params_code += f'\t{str(param)}\n'

        for local in self.locals:
            locals_code += f'\tLOCAL {local} ;\n'

        for instruction in self.body:
            body_code += f'\t{str(instruction)}\n'

        return f'function {self.name} {{\n{params_code}{locals_code}{body_code}}}\n'


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

    def __str__(self):
        return f'PARAM {self.id} ;'


class AssignNode(InstructionNode):
    def __init__(self, result, val):
        super().__init__()
        self.result = result
        self.val = val
        self.check_local(result)
        self.check_local(val)

    def __str__(self):
        return f'{self.result} = {self.val} ;'


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
    def __str__(self):
        return f'{self.result} = {self.left} + {self.right} ;'


class MinusNode(ArithNode):
    def __str__(self):
        return f'{self.result} = {self.left} - {self.right} ;'


class StarNode(ArithNode):
    def __str__(self):
        return f'{self.result} = {self.left} * {self.right} ;'


class DivNode(ArithNode):
    def __str__(self):
        return f'{self.result} = {self.left} / {self.right} ;'


class LessEqNode(ArithNode):
    def __str__(self):
        return f'{self.result} = {self.left} <= {self.right} ;'


class LessNode(ArithNode):
    def __str__(self):
        return f'{self.result} = {self.left} < {self.right} ;'


class NotNode(InstructionNode):
    def __init__(self, value, result):
        super().__init__()
        self.value = value
        self.result = result
        self.check_local(value)
        self.check_local(result)

    def __str__(self):
        return f'{self.result} = ~ {self.value}'


class GetAttrNode(InstructionNode):
    def __init__(self, obj, attr, result, attr_index=0):
        super().__init__()
        self.attr = attr
        self.obj = obj
        self.result = result
        self.attr_index = attr_index
        self.check_local(obj)
        self.check_local(result)

    def __str__(self):
        return f'{self.result} = GETATTR {self.obj} {self.attr} ;'


class SetAttrNode(InstructionNode):
    def __init__(self, obj, attr, val, attr_index=0):
        super().__init__()
        self.val = val
        self.obj = obj
        self.attr = attr
        self.attr_index = attr_index
        self.check_local(obj)
        self.check_local(val)

    def __str__(self):
        return f'SETATTR {self.obj} {self.attr} {self.val} ;'


class SetIndexNode(InstructionNode):
    def __init__(self, array, index, val):
        self.val = val
        self.array = array
        self.index = index

    def __str__(self):
        return f'SETINDEX {self.array} {self.index} {self.val} ;'


class GetIndexNode(InstructionNode):
    def __init__(self, array, index, result):
        self.result = result
        self.array = array
        self.index = index

    def __str__(self):
        return f'{self.result} = GETINDEX {self.array} {self.index} ;'


class AllocateNode(InstructionNode):
    def __init__(self, _type, result):
        super().__init__()
        self.type = _type
        self.result = result
        self.check_local(result)

    def __str__(self):
        return f'{self.result} = ALLOCATE {self.type} ;'


class AbortNode(InstructionNode):
    def __init__(self, type_name: str = None):
        self.type_name = type_name

    def __str__(self):
        return f'ABORT {self.type_name} ;'


class ReadIntNode(InstructionNode):
    def __init__(self, result):
        self.result = result

    def __str__(self):
        return f'{self.result} = READINT ;'


class CopyNode(InstructionNode):
    def __init__(self, val, result):
        self.result = result
        self.val = val

    def __str__(self):
        return f'{self.result} = COPY {self.val} ;'


class TypeOfNode(InstructionNode):
    def __init__(self, result, var):
        super().__init__()
        self.result = result
        self.var = var
        self.check_local(result)
        self.check_local(var)

    def __str__(self):
        return f'{self.result} = TYPEOF {self.var} ;'


class ArrayNode(InstructionNode):
    def __init__(self, len, result):
        self.len = len
        self.result = result

    def __str__(self):
        return f'{self.result} = ARRAY {self.len} ;'


class CallNode(InstructionNode):
    def __init__(self, method, result):
        self.method = method
        self.result = result

    def __str__(self):
        return f'{self.result} = CALL {self.method} ;'


class VCAllNode(InstructionNode):
    def __init__(self, type, method, result):
        super().__init__()
        self.method = method
        self.type = type
        self.result = result
        self.check_local(result)
        self.check_local(type)

    def __str__(self):
        return f'{self.result} = VCALL {self.type} {self.method} ;'


class ArgNode(InstructionNode):
    def __init__(self, val):
        super().__init__()
        self.val = val
        self.check_local(val)

    def __str__(self):
        return f'ARG {self.val} ;'


class ConditionalGotoNode(InstructionNode):
    def __init__(self, predicate, label):
        super().__init__()
        self.predicate = predicate
        self.label = label
        self.check_local(predicate)

    def __str__(self):
        return f'IF {self.predicate} GOTO {self.label} ;'


class GotoNode(InstructionNode):
    def __init__(self, label):
        super().__init__()
        self.label = label

    def __str__(self):
        return f'GOTO {self.label} ;'


class LabelNode(InstructionNode):
    def __init__(self, label_name):
        super().__init__()
        self.label_name = label_name

    def __str__(self):
        return f'LABEL {self.label_name} ;'


class ReturnNode(InstructionNode):
    def __init__(self, ret_value):
        super().__init__()
        self.ret_value = ret_value
        self.check_local(ret_value)

    def __str__(self):
        return f'RETURN {self.ret_value} ;' if self.ret_value else f'RETURN ;'


class LoadNode(InstructionNode):
    def __init__(self, addr, result):
        super().__init__()
        self.result = result
        self.addr = addr
        self.check_local(result)

    def __str__(self):
        return f'{self.result} = LOAD {self.addr} ;'


class LengthNode(InstructionNode):
    def __init__(self, str, result):
        self.result = result
        self.str = str

    def __str__(self):
        return f'{self.result} = LENGTH {self.str} ;'


class ConcatNode(InstructionNode):
    def __init__(self, str_a, str_b, result):
        self.result = result
        self.str_a = str_a
        self.str_b = str_b

    def __str__(self):
        return f'{self.result} = CONCAT {self.str_a} {self.str_b} ;'


class SubStringNode(InstructionNode):
    def __init__(self, str, i, len, result):
        self.result = result
        self.i = i
        self.len = len
        self.str = str

    def __str__(self):
        return f'{self.result} = SUBSTRING {self.str} {self.i} {self.len};'


class StrNode(InstructionNode):
    def __init__(self, val, result):
        super().__init__()
        self.result = result
        self.val = val
        self.check_local(val)
        self.check_local(result)

    def __str__(self):
        return f'{self.result} = STR {self.val} ;'


class ReadNode(InstructionNode):
    def __init__(self, result):
        super().__init__()
        self.result = result
        self.check_local(result)

    def __str__(self):
        return f'{self.result} = READ ;'


class PrintNode(InstructionNode):
    def __init__(self, str):
        super().__init__()
        self.str = str
        self.check_local(str)

    def __str__(self):
        return f'PRINT {self.str} ;'
