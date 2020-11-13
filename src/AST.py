class Node:
    index=0
    line=0

class ProgramNode(Node):
    def __init__(self, classes):
        self.classes = classes

class ClassNode(Node):
    def __init__(self, name, parent, features):
        self.name = name
        self.parent = parent
        self.methods = []
        self.attributes = []
        if features is not []:
            for foo in features:
                if isinstance(foo,AttributeNode):
                    self.attributes.append(foo)
                else:
                    self.methods.append(foo)

class ClassFeatureNode(Node):
    pass

class MethodNode(ClassFeatureNode):
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

class AttributeNode(ClassFeatureNode):
    def __init__(self, name, attr_type, value):
        self.name = name
        self.type = attr_type
        self.value = value

class ParameterNode(ClassFeatureNode):
    def __init__(self, name, param_type):
        self.name = name
        self.type = param_type

class ExpressionNode(Node):
    pass


class AssignNode(ExpressionNode):
    def __init__(self, variable, expr):
        self.variable = variable
        self.expression = expr

class ConditionalNode(ExpressionNode):
    def __init__(self, predicate, then_body, else_body):
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body

class LoopNode(ExpressionNode):
    def __init__(self, predicate, body):
        self.predicate = predicate
        self.body = body

class LetNode(ExpressionNode):
    def __init__(self, declarations, in_body):
        self.declarations = declarations
        self.body = in_body 

class AtomicNode(ExpressionNode):
    pass

class ConstantNode(AtomicNode):
    pass
    
class StringNode(ConstantNode):
    def __init__(self, value):
        self.value = value

class IntegerNode(ConstantNode):
    def __init__(self, value):
        self.value = value

class BoolNode(ConstantNode):
    def __init__(self, value):
        self.value = value

class NewNode(AtomicNode):
    def __init__(self, new_type):
        self.type = new_type

class BlockNode(AtomicNode):
    def __init__(self, expressions):
        self.expressions = expressions

class CaseNode(AtomicNode):
    def __init__(self, expression, subcases):
        self.expression = expression
        self.subcases = subcases

class SubCaseNode:
    def __init__(self, name, sub_type, expression):
        self.name = name
        self.type = sub_type
        self.expression = expression 

class DispatchNode(AtomicNode):
    def __init__(self, func_id, parameters, left_expr, left_type=None):
        self.func_id = func_id
        self.parameters = parameters
        self.left_expression = left_expr
        self.left_type=left_type

class StaticDispatchNode(AtomicNode):
    def __init__(self, func_id, parent_id ,parameters, left_expr):
        self.func_id = func_id
        self.parent_id = parent_id
        self.parameters = parameters
        self.left_expression = left_expr

class VariableNode(AtomicNode):
    def __init__(self, var_id):
        self.id = var_id

class UnaryOperatorNode(ExpressionNode):
    operator = ""
    pass

class IsVoidNode(UnaryOperatorNode):
    def __init__(self, expr):
        self.expression = expr

class IntComplementNode(UnaryOperatorNode):
    def __init__(self, right):
        self.right = right

class BoolComplementNode(UnaryOperatorNode):
    def __init__(self, right):
        self.right = right

class BinaryOperatorNode(ExpressionNode):
    operator=""
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ComparisonNode(BinaryOperatorNode):
    pass

class LesserNode(ComparisonNode):
    pass

class LesserEqualNode(ComparisonNode):
    pass

class EqualNode(ComparisonNode):
    def __init__(self,left,right, isString=False):
        self.left = left
        self.right = right
        self.isString = isString

class ArithmeticNode(BinaryOperatorNode):
    pass

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class MultNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass



