from .operation_node_il import *

class NotNodeIL(UnaryNodeIL):
    
    def __str__(self):
        return ("{} = ~{}".format(self.dest, self.expr))

class LogicalNotNodeIL(UnaryNodeIL):
    def __str__(self):
        return ("{} = NOT {}".format(self.dest, self.expr))
class PlusNodeIL(BinaryNodeIL):
    def __str__(self):
        return ("{} = {} + {}".format(self.dest,self.left, self.right))

class MinusNodeIL(BinaryNodeIL):
    def __str__(self):
        return ("{} = {} - {}".format(self.dest,self.left, self.right))
class StarNodeIL(BinaryNodeIL):
    def __str__(self):
        return ("{} = {} * {}".format(self.dest,self.left, self.right))

class DivNodeIL(BinaryNodeIL):
    def __str__(self):
        return ("{} = {} / {}".format(self.dest,self.left, self.right))

class LessNodeIL(BinaryNodeIL):
    def __str__(self):
        return ("{} = {} < {}".format(self.dest,self.left, self.right))

class LessEqNodeIL(BinaryNodeIL):
    def __str__(self):
        return ("{} = {} <= {}".format(self.dest,self.left, self.right))

class EqualNodeIL(BinaryNodeIL):
    def __str__(self):
        return ("{} = {} == {}".format(self.dest,self.left, self.right))

class ArrayNodeIL(InstructionNodeIL):
    pass

class GetIndexNodeIL(InstructionNodeIL):
    pass

class SetIndexNodeIL(InstructionNodeIL):
    pass

class SetAttribNodeIL(InstructionNodeIL):
    def __init__(self, obj, attr, value, typex, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr

        self.value = value
        self.attr_type = typex

        self.out = obj
        self.in1 = value
    
    def __str__(self):
        return ("SETATTR {} {} = {}".format(self.obj,self.attr, self.value))

class GetAttribNodeIL(InstructionNodeIL):
    def __init__(self, dest, obj, attr, attr_type, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        # self.type_name = typex
        self.dest = dest
        self.attr_type = attr_type

        self.out = dest
        self.in1 = obj

    def __str__(self):
        return ("{} = GETATTR {} {}".format(self.dest,self.obj,self.attr))

class TypeOfNodeIL(InstructionNodeIL):
    def __init__(self, obj, dest, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.dest = dest

        self.out = dest
        self.in1 = obj

    def __str__(self):
        return ("{} = TYPEOF {}".format(self.dest,self.obj))

class LabelNodeIL(InstructionNodeIL):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label
    
    def __str__(self):
        return ("LABEL {}".format(self.label))


class GotoNodeIL(InstructionNodeIL):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label
    def __str__(self):
        return ("GOTO {}".format(self.label))

class GotoIfNodeIL(InstructionNodeIL):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.in1 = cond
    
    def __str__(self):
        return ("IF {} GOTO {}".format(self.cond, self.label))

class GotoIfFalseNodeIL(InstructionNodeIL):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.in1 = cond
    
    def __str__(self):
        return ("IF NOT {} GOTO {}".format(self.cond,self.label))

class StaticCallNodeIL(InstructionNodeIL):
    def __init__(self, dest, function, args, xtype, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.function = function
        self.dest = dest
        self.args = args
        # self.return_type = return_type
        
        self.out = dest
    
    def __str__(self):
        args = '\n\t'.join(str(arg) for arg in self.args)
        return ("{}\n\t{} = CALL {}".format(args, self.dest, self.function))

class DynamicCallNodeIL(InstructionNodeIL):
    def __init__(self, dest, method,args, xtype, obj, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.method = method
        self.dest = dest
        self.args = args
        # self.return_type = return_type
        self.obj = obj

        self.out = dest
        self.in1 = obj
    
    def __str__(self):
        args = '\n\t'.join(str(arg) for arg in self.args)
        return ("{}\n\t{} = VCALL {} {}".format(args, self.dest, self.type, self.method))

class ArgNodeIL(InstructionNodeIL):
    def __init__(self, name, idx=None):
        super().__init__(idx)
        self.dest = name
        self.out = name

    def __str__(self):
        return f"ARG {self.dest}"

class ReturnNodeIL(InstructionNodeIL):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.out = value
    
    def __str__(self):
        to_return = ""
        if self.value is not None:
            to_return = " " + str(self.value)
        return "RETURN" + to_return

class LoadNodeIL(InstructionNodeIL):
    def __init__(self, msg, dest, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.msg = msg

        self.out = dest

    def __str__(self):
        return ("{} = LOAD {}".format(self.dest, self.msg))

class LengthNodeIL(InstructionNodeIL):
    def __init__(self, arg, dest, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.arg = arg

        self.out = dest
        self.in1 = arg

    def __str__(self):
        return ("{} = LENGTH {}".format(self.dest, self.arg))

class ConcatNodeIL(InstructionNodeIL):
    def __init__(self, arg1, len1, arg2, len2, dest, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.arg1 = arg1
        self.arg2 = arg2
        self.len1 = len1
        self.len2 = len2
        self.out = dest
        self.in1 = arg1
        self.in2 = arg2
    
    def __str__(self):
        return ("{} = CONCAT {} {}".format(self.dest, self.arg1, self.arg2))

class StringEqualsNodeIL(InstructionNodeIL):
    def __init__(self, s1, s2, result):
        self.s1 = s1
        self.s2 = s2
        self.result = result

class SubstringNodeIL(InstructionNodeIL):
    def __init__(self, begin, end, word, dest, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.begin = begin
        self.word = word
        self.end = end

        self.out = dest
        self.in1 = begin
        self.in2 = end

    def __str__(self):
        return ("{} = SUBSTR {} {} {}".format(self.dest, self.word, self.begin, self.end))

class ToStrNodeIL(InstructionNodeIL):
    def __init__(self, dest, ivalue, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.ivalue = ivalue

        self.out = dest
        self.in1 = ivalue

    def __str__(self):
        return ("{} = STR {}".format(self.dest, self.ivalue))

class OutStringNodeIL(InstructionNodeIL):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.in1 = value

    def __str__(self):
        return ("OUT_STR {}".format(self.value))

class OutIntNodeIL(InstructionNodeIL):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.in1 = value

    def __str__(self):
        return ("OUT_INT {}".format(self.value))

class ReadStringNodeIL(InstructionNodeIL):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest

        self.out = dest

    def __str__(self):
        return ("{} = READ_STR".format(self.dest))

class ReadIntNodeIL(InstructionNodeIL):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest

        self.out = dest

    def __str__(self):
        return ("{} = READ_INT".format(self.dest))

class ExitNodeIL(InstructionNodeIL):
    def __init__(self, classx, value=0, idx=None):
        super().__init__(idx)
        self.classx = classx        # instance of the method that called the class
        self.value = value

        self.in1 = value
        self.in2 = classx

    def __str__(self):
        return ("EXIT {}".format(self.value))

class CopyNodeIL(InstructionNodeIL):
    def __init__(self, source, dest, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source

        self.out = dest
        self.in1 = source

    def __str__(self):
        return ("{} = COPY {}".format(self.dest, self.source))

class ConformsNodeIL(InstructionNodeIL):
    def __init__(self, dest, expr, type2, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.expr = expr
        self.type = type2

        self.out = dest
        self.in1 = expr
    
    def __str__(self):
        return ("{} = CONFORMS {}".format(self.dest, self.expr, self.type))
        
class VoidConstantNodeIL(InstructionNodeIL):
    def __init__(self, obj, idx=None):
        super().__init__(idx)
        self.obj = obj

        self.out = obj
    
    def __str__(self):
        return ("{} = Void".format(self.obj))

class ErrorNodeIL(InstructionNodeIL):
    def __init__(self, typex, idx=None):
        super().__init__(idx)
        self.type = typex

    def __str__(self):
        return ("ERROR {}".format(self.type))

class BoxingNodeIL(InstructionNodeIL):
    def __init__(self, dest, type_name, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.type = type_name

        self.out = dest

class IsVoidNodeIL(InstructionNodeIL):
    def __init__(self, result_local, expre_value):
        self.result_local = result_local
        self.expre_value = expre_value

class CaseNodeIL(InstructionNodeIL):
    def __init__(self, local_expr, first_label):
        self.local_expr = local_expr
        self.first_label = first_label

class OptionNodeIL(InstructionNodeIL):
    def __init__(self, local_expr, tag, max_tag, next_label):
        self.local_expr = local_expr
        self.tag = tag
        self.max_tag = max_tag
        self.next_label = next_label