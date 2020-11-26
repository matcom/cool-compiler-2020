class Node:
    @property
    def clsname(self):
        return str(self.__class__.__name__)

    def to_tuple(self):
        return tuple([
            ("node_class_name", self.clsname)
        ])

    def to_readable(self):
        return "{}".format(self.clsname)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.to_readable())


class NodeProgram(Node):
    def __init__(self, class_list):
        self.class_list = class_list

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname), 
            ("classes", self.class_list)
        ])

    def to_readable(self):
        return "{}(classes={})".format(self.clsname, self.class_list)

class NodeClassTuple(Node, tuple):
    def __init__(self, classes):
        self.classes = classes

class NodeClass(Node):
    def __init__(self, idName: str, methods, attributes, parent):
        self.idName = idName
        self.methods = methods
        self.attributes = attributes
        self.parent = parent

    def to_readable(self):
        return "{}(name='{}', parent={}, methods={}, attributes={})".format(
            self.clsname, self.idName, self.parent, self.methods, self.attributes)

class NodeFeature(Node):
    def __init__(self):
        super(NodeFeature, self).__init__()

#No se si poner aqui una clase para heredar , que sea feature_class.
#Tengo que ver si a futuro necesito iterar por los elementos de una clase
#de manera abstracta.
class NodeClassMethod(NodeFeature):
    def __init__(self,
                idName: str,
                argNames,
                argTypesNames,
                return_type: str,
                body):
        self.idName = idName
        self.argNames = argNames
        self.returnType = return_type
        self.argTypesNames = argTypesNames
        self.body = body

    def to_readable(self):
        return "{}(name='{}', argNames={}, returnType={}, argTypesNames={}, body={})".format(
            self.clsname, self.idName, self.argNames, self.returnType, self.argTypesNames, self.body
            )

class NodeAttr(NodeFeature):
    def __init__(self, idName, attr_type, expr):
        self.idName = idName
        self.attrType = attr_type
        self.expr = expr

class NodeFormalParam(NodeFeature):
    def __init__(self, idName, param_type):
        super().__init__()
        self.idName = idName
        self.paramType = param_type

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("name", self.idNme),
            ("param_type", self.param_type)
        ])

    def to_readable(self):
        return "{}(name='{}', param_type={})".format(self.clsname, self.idName, self.param_type)

class NodeObject(Node):
    def __init__(self, idName):
        super().__init__()
        self.idName = idName

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("name", self.idName)
        ])

    def to_readable(self):
        return "{}(name='{}')".format(self.clsname, self.idName)

class NodeSelf(NodeObject):
    def __init__(self):
        super(Self, self).__init__("SELF")

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname)
        ])

    def to_readable(self):
        return "{}".format(self.clsname)


class NodeConstant(Node):
    def __init__(self):
        super().__init__()


class NodeInteger(NodeConstant):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("content", self.content)
        ])

    def to_readable(self):
        return "{}(content={})".format(self.clsname, self.content)
    

class NodeBoolean(NodeConstant):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("content", self.content)
        ])

    def to_readable(self):
        return "{}(content={})".format(self.clsname, self.content)

class NodeString(NodeConstant):
    def __init__(self, content):
        super(String, self).__init__()
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("content", self.content)
        ])

    def to_readable(self):
        return "{}(content={})".format(self.clsname, repr(self.content))


class NodeExpr(Node):
    def __init__(self):
        super().__init__()

class NodeNewObject(NodeExpr):
    def __init__(self, new_type):
        super().__init__()
        self.type = new_type

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("type", self.type)
        ])

    def to_readable(self):
        return "{}(type={})".format(self.clsname, self.type)


class NodeIsVoid(NodeExpr):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr", self.expr)
        ])

    def to_readable(self):
        return "{}(expr={})".format(self.clsname, self.expr)


class NodeAssignment(NodeExpr):
    def __init__(self, instance, expr):
        super().__init__()
        self.instance = instance
        self.expr = expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("instance", self.instance),
            ("expr", self.expr)
        ])

    def to_readable(self):
        return "{}(instance={}, expr={})".format(self.clsname, self.instance, self.expr)


class NodeBlock(NodeExpr):
    def __init__(self, expr_list):
        super(Block, self).__init__()
        self.expr_list = expr_list

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr_list", self.expr_list)
        ])

    def to_readable(self):
        return "{}(expr_list={})".format(self.clsname, self.expr_list)


class NodeDynamicDispatch(NodeExpr):
    def __init__(self, instance, method, arguments):
        super().__init__()
        self.instance = instance
        self.method = method
        self.arguments = arguments if arguments is not None else tuple()

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("instance", self.instance),
            ("method", self.method),
            ("arguments", self.arguments)
        ])

    def to_readable(self):
        return "{}(instance={}, method={}, arguments={})".format(
            self.clsname, self.instance, self.method, self.arguments)


class NodeStaticDispatch(NodeExpr):
    def __init__(self, instance, dispatch_type, method, arguments):
        super().__init__()
        self.instance = instance
        self.dispatch_type = dispatch_type
        self.method = method
        self.arguments = arguments if arguments is not None else tuple()

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("instance", self.instance),
            ("dispatch_type", self.dispatch_type),
            ("method", self.method),
            ("arguments", self.arguments)
        ])

    def to_readable(self):
        return "{}(instance={}, dispatch_type={}, method={}, arguments={})".format(
            self.clsname, self.instance, self.dispatch_type, self.method, self.arguments)


class NodeLet(NodeExpr):
    def __init__(self, instance, return_type, init_expr, body):
        super().__init__()
        self.instance = instance
        self.return_type = return_type
        self.init_expr = init_expr
        self.body = body

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("instance", self.instance),
            ("return_type", self.return_type),
            ("init_expr", self.init_expr),
            ("body", self.body)
        ])

    def to_readable(self):
        return "{}(instance={}, return_type={}, init_expr={}, body={})".format(
            self.clsname, self.instance, self.return_type, self.init_expr, self.body)


class NodeIf(NodeExpr):
    def __init__(self, predicate, then_body, else_body):
        super().__init__()
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("predicate", self.predicate),
            ("then_body", self.then_body),
            ("else_body", self.else_body)
        ])

    def to_readable(self):
        return "{}(predicate={}, then_body={}, else_body={})".format(
            self.clsname, self.predicate, self.then_body, self.else_body)


class NodeWhileLoop(NodeExpr):
    def __init__(self, predicate, body):
        super().__init__()
        self.predicate = predicate
        self.body = body

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("predicate", self.predicate),
            ("body", self.body)
        ])

    def to_readable(self):
        return "{}(predicate={}, body={})".format(self.clsname, self.predicate, self.body)


class NodeCase(NodeExpr):
    def __init__(self, expr, actions):
        super().__init__()
        self.expr = expr
        self.actions = actions

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr", self.expr),
            ("actions", self.actions)
        ])

    def to_readable(self):
        return "{}(expr={}, actions={})".format(self.clsname, self.expr, self.actions)


# ############################## UNARY OPERATIONS ##################################


class NodeNodeUnaryOperation(NodeExpr):
    def __init__(self):
        super().__init__()

class NodeIntegerComplement(NodeUnaryOperation):
    def __init__(self, integer_expr):
        super().__init__()
        self.symbol = "~"
        self.integer_expr = integer_expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("integer_expr", self.integer_expr)
        ])

    def to_readable(self):
        return "{}(expr={})".format(self.clsname, self.integer_expr)


class NodeBooleanComplement(NodeUnaryOperation):
    def __init__(self, boolean_expr):
        super(BooleanComplement, self).__init__()
        self.symbol = "!"
        self.boolean_expr = boolean_expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("boolean_expr", self.boolean_expr)
        ])

    def to_readable(self):
        return "{}(expr={})".format(self.clsname, self.boolean_expr)

# ############################## BINARY OPERATIONS ##################################

class NodeBinaryOperation(NodeExpr):
    def __init__(self):
        super().__init__()

class NodeAddition(NodeBinaryOperation):
    def __init__(self, first, second):
        super().__init__()
        self.symbol = "+"
        self.first = first
        self.second = second

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("first", self.first),
            ("second", self.second)
        ])

    def to_readable(self):
        return "{}(first={}, second={})".format(self.clsname, self.first, self.second)


class NodeSubtraction(NodeBinaryOperation):
    def __init__(self, first, second):
        super().__init__()
        self.symbol = "-"
        self.first = first
        self.second = second

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("first", self.first),
            ("second", self.second)
        ])

    def to_readable(self):
        return "{}(first={}, second={})".format(self.clsname, self.first, self.second)


class NodeMultiplication(NodeBinaryOperation):
    def __init__(self, first, second):
        super().__init__()
        self.symbol = "*"
        self.first = first
        self.second = second

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("first", self.first),
            ("second", self.second)
        ])

    def to_readable(self):
        return "{}(first={}, second={})".format(self.clsname, self.first, self.second)


class NodeDivision(NodeBinaryOperation):
    def __init__(self, first, second):
        super().__init__()
        self.symbol = "/"
        self.first = first
        self.second = second

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("first", self.first),
            ("second", self.second)
        ])

    def to_readable(self):
        return "{}(first={}, second={})".format(self.clsname, self.first, self.second)


class NodeEqual(NodeBinaryOperation):
    def __init__(self, first, second):
        super().__init__()
        self.symbol = "="
        self.first = first
        self.second = second

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("first", self.first),
            ("second", self.second)
        ])

    def to_readable(self):
        return "{}(first={}, second={})".format(self.clsname, self.first, self.second)


class NodeLessThan(NodeBinaryOperation):
    def __init__(self, first, second):
        super().__init__()
        self.symbol = "<"
        self.first = first
        self.second = second

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("first", self.first),
            ("second", self.second)
        ])

    def to_readable(self):
        return "{}(first={}, second={})".format(self.clsname, self.first, self.second)


class NodeLessThanOrEqual(NodeBinaryOperation):
    def __init__(self, first, second):
        super().__init__()
        self.symbol = "<="
        self.first = first
        self.second = second

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("first", self.first),
            ("second", self.second)
        ])

    def to_readable(self):
        return "{}(first={}, second={})".format(self.clsname, self.first, self.second)

