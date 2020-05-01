class Node:
    pass

class ProgramNode(Node):
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code
        
class TypesNode(Node):
    def __init__(self, type):
        self.attributes=[]
        self.methods=[]
        self.type=type
        
class DataNode(Node):
    def __init__(self, id, val):
        self.id=id
        self.val=val
        
class FuncNode(Node):
    def __init__(self, name, params, locals, body):
        self.name=name
        self.params=params
        self.locals=locals
        self.body=body
        
class InstructionNode(Node):
    pass
        
class LocalNode(Node):
    def __init__(self, id):
        self.id=id
        
class ParamNode(Node):
    def __init__(self, id):
        self.id=id
        
class AssignNode(InstructionNode):
    def __init__(self, id, val):
        self.id=id
        self.val=val
        
class ArithNode(InstructionNode):
    def __init__(self, left, right, result):
        self.left=left
        self.right=right
        self.result=result

class GetAttrNode(InstructionNode):
    def __init__(self, obj, attr, result):
        self.attr=attr
        self.obj=obj
        self.result=result
        
class SetAttrNode(InstructionNode):
    def __init__(self,  obj, attr, val):
        self.val=val
        self.obj=obj
        self.attr=attr
        
class SetIndexNode(InstructionNode):
    def __init__(self, array, index, val):
        self.val=val
        self.array=array
        self.index=index
        
class GetIndexNode(InstructionNode):
    def __init__(self, array, index, result):
        self.result=result
        self.array=array
        self.index=index
        
class AllocateNode(InstructionNode):
    def __init__(self, type, addr):
        self.type=type
        self.addr=addr
        
class TypeOfNode(InstructionNode):
    def __init__(self, result, var):
        self.result=result
        self.var=var
        
class ArrayNode(InstructionNode):
    def __init__(self, len, result):
        self.len=len
        self.result=result
        
class CallNode(InstructionNode):
    def __init__(self, method):
        self.method=method
        
class VCAllNode(InstructionNode):
    def __init__(self, type, method):
        self.method=method
        
class ArgNode(InstructionNode):
    def __init__(self, val):
        self.val=val
        
class ConditionalGotoNode(InstructionNode):
    def __init__(self, predicate, label):
        self.predicate=predicate
        self.label=label
        
class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label=label
        
class LabelNode(InstructionNode):
    def __init__(self, label_name):
        self.label_name=label_name
        
class ReturnNode(InstructionNode):
    def __init__(self, ret_value):
        self.ret_value=ret_value

class StrOpNode(InstructionNode):
     def __init__(self, str, result):
        self.result=result
        self.str=str
        
class LoadNode(StrOpNode):
    pass
               
class LengthNode(StrOpNode):
    pass

class ConcatNode(StrOpNode):
    pass

class SubStringNode(StrOpNode):
    pass
        
class StrNode(StrOpNode):
    pass
    
class ReadNode(InstructionNode):
    pass

class PrintNode(InstructionNode):
    def __init__(self, str):
        self.str=str
        
        

        
            