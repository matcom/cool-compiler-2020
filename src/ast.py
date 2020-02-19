class ProgramNode:
    def __init__(self, def_class_nodes):
        self.def_class_nodes=def_class_nodes
    
class DefClassNode:
    def __init__(self, type, feature_nodes, parent_type): #poner null#
        self.type=type
        self.parent_type=parent_type
        self.feature_nodes=feature_nodes

class FeatureNode:
    pass

class DefAttrNode(FeatureNode):
    def __init__(self,id, type, expr):
        self.id=id
        self.type=type
        self.expr=expr
        
class DefFuncNode(FeatureNode):
    def __init__(self, id, params, return_type, expressions):
        self.id=id
        self.params=params
        self.return_type=return_type
        self.expressions=expressions
        
class AssignNode:
    def __init__(self, id, expr, type): #poner null#
        self.id=id
        self.expr=expr
        self.type=type
        
    
class FuncCallNode:
    def __init__(self, object, type, id, expressions):
        self.object=object
        self.type=type
        self.id=id
        self.expressions=expressions

class IfNode:
    def __init__(self, if_expr, then_expr, else_expr):
        self.if_expr=if_expr
        self.then_expr=then_expr
        self.else_expr=else_expr
        
        
class LoopNode:
    def __init__(self, cond, body):
        self.cond=cond
        self.body=body
        
        
class BlockNode:
    def __init__(self, expressions):
        self.expressions=expressions
        
class LetNode:
    def __init__(self, assign_nodes, expr):
        self.assign_nodes =assign_nodes
        self.expr=expr
        
class CaseNode:
    def __init__(self, expr, ids):
        self.expr=expr
        self.ids=ids
        
class InitNode:
    def __init__(self, type):
        self.type=type
        
class ExpressionNode:
    pass

class ArithNode(ExpressionNode):
    def __init__(self, lvalue, rvalue):
        self.lvalue=lvalue
        self.rvalue=rvalue
    
        
class PlusNode(ArithNode):
    pass

class MinusNode(ArithNode):
    pass

class StarNode(ArithNode):
    pass

class DivNode(ArithNode):
    pass

class UnaryNode(ExpressionNode):
    def __init__(self, val):
        self.val=val
        
class NegationNode(UnaryNode):
    pass

class AtomNode(UnaryNode):
    pass