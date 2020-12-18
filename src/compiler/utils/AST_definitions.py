from json import dumps
class Node:
    def __init__(self, line = 0, column = 0):
        self.line = line
        self.column = column
        
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
        return self.toJSON()

    def __str__(self):
        return str(self.to_readable())

    def __getitem__(self, x):
        return self.__dict__[x]
    
    def __setitem__(self, x, y):
        self.__dict__[x]= y

    def __iter__(self):
        return self.__dict__.__iter__()
    
    def __eq__(self, other):
        return type(self) == type(other) and self.idName == other.idName
        
    def toJSON(self):
        return dumps(self, default=lambda  o: o.__dict__,
        sort_keys=True, indent=4, separators=(',', ': '))


class NodeProgram(Node):
    def __init__(self, class_list):
        super().__init__()
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
    def __init__(self, idName: str, methods, attributes, parent, 
                 line, column):
        super().__init__(line= line, column= column)
        self.idName = idName
        self.methods = methods
        self.attributes = attributes
        self.parent = parent
        
        
        
    def to_readable(self):
        return "{}(name='{}', parent={}, methods={}, attributes={})".format(
            self.clsname, self.idName, self.parent, 
            self.methods, self.attributes)

class NodeFeature(Node):
    def __init__(self, line, column):
        super(NodeFeature, self).__init__(line= line, column= column)

#No se si poner aqui una clase para heredar , que sea feature_class.
#Tengo que ver si a futuro necesito iterar por los elementos de una clase
#de manera abstracta.
class NodeClassMethod(NodeFeature):
    def __init__(self,
                idName: str,
                formal_param_list,
                returnType: str,
                body,
                line,
                column):
        super().__init__(line= line, column= column)
        self.idName = idName
        self.formal_param_list= formal_param_list
        self.returnType = returnType
        self.body = body

    def to_readable(self):
        return "{}(name='{}', formal_param_list={}, returnType={}, body={})".format(
            self.clsname, self.idName, self.formal_param_list, 
            self.returnType, self.body
            )

class NodeAttr(NodeFeature):
    def __init__(self, idName, _type,
                line, column, expr= None):
        super().__init__(line= line, column= column)
        self.idName = idName
        self._type = _type
        self.expr = expr

class NodeFormalParam(NodeFeature):
    def __init__(self, idName, param_type, line, column):
        super().__init__(line= line, column= column)
        self.idName = idName
        self._type = param_type

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("name", self.idNme),
            ("param_type", self._type)
        ])

    def to_readable(self):
        return "{}(name='{}', param_type={})".format(self.clsname, 
        self.idName, self._type)

class NodeObject(Node):
    def __init__(self, idName, line, column):
        super().__init__(line= line, column= column)
        self.idName = idName

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("name", self.idName)
        ])

    def to_readable(self):
        return "{}(name='{}')".format(self.clsname, self.idName)

class NodeSelf(NodeObject):
    def __init__(self, line, column):
        super().__init__(idName= "SELF", line= line, column= column)

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname)
        ])

    def to_readable(self):
        return "{}".format(self.clsname)


class NodeConstant(Node):
    def __init__(self, line, column):
        super().__init__(line= line, column= column)


class NodeInteger(NodeConstant):
    def __init__(self, content, line, column):
        super().__init__(line= line, column= column)
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("content", self.content)
        ])

    def to_readable(self):
        return "{}(content={})".format(self.clsname, self.content)
    

class NodeBoolean(NodeConstant):
    def __init__(self, content, line, column):
        super().__init__(line= line, column= column)
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("content", self.content)
        ])

    def to_readable(self):
        return "{}(content={})".format(self.clsname, self.content)

class NodeString(NodeConstant):
    def __init__(self, content, line, column):
        super().__init__(line= line, column= column)
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("content", self.content)
        ])

    def to_readable(self):
        return "{}(content={})".format(self.clsname, repr(self.content))

# Cada expresión debe tener una función de evaluación asociada.
# Con un valor de retorno x.
class NodeExpr(Node):
    def __init__(self, line, column):
        super().__init__(line= line, column= column)


class NodeNewObject(NodeExpr):
    def __init__(self, new_type, line, column):
        super().__init__(line= line, column= column)
        self.type = new_type

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("type", self.type)
        ])

    def to_readable(self):
        return "{}(type={})".format(self.clsname, self.type)


class NodeIsVoid(NodeExpr):
    def __init__(self, expr, line, column):
        super().__init__(line= line, column= column)


    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr", self.expr)
        ])

    def to_readable(self):
        return "{}(expr={})".format(self.clsname, self.expr)


class NodeAssignment(NodeExpr):
    def __init__(self, idName, expr, line, column):
        super().__init__(line= line, column= column)
        self.idName = idName
        self.expr = expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("idName", self.idName),
            ("expr", self.expr)
        ])

    def to_readable(self):
        return "{}(idName={}, expr={})".format(self.clsname, 
        self.idName, self.expr)


class NodeBlock(NodeExpr):
    def __init__(self, expr_list, line, column):
        super().__init__(line = line, column = column)
        self.expr_list = expr_list

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr_list", self.expr_list)
        ])

    def to_readable(self):
        return "{}(expr_list={})".format(self.clsname, self.expr_list)


class NodeDynamicDispatch(NodeExpr):
    def __init__(self, expr, method, arguments, line, column):
        super().__init__(line= line, column= column)
        self.expr = expr
        self.method = method
        self.arguments = arguments if arguments is not None else tuple()

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr", self.expr),
            ("method", self.method),
            ("arguments", self.arguments)
        ])

    def to_readable(self):
        return "{}(expr={}, method={}, arguments={})".format(
            self.clsname, self.expr, self.method, self.arguments)


class NodeStaticDispatch(NodeExpr):
    def __init__(self,
                 expr,
                 dispatch_type, method, arguments, line, column):
        super().__init__(line= line, column= column)
        self.expr = expr
        self.dispatch_type = dispatch_type
        self.method = method
        self.arguments = arguments if arguments is not None else tuple()

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr", self.expr),
            ("dispatch_type", self.dispatch_type),
            ("method", self.method),
            ("arguments", self.arguments)
        ])

    def to_readable(self):
        return "{}(expr={}, dispatch_type={}, method={}, arguments={})".format(
            self.clsname, self.expr, self.dispatch_type, 
            self.method, self.arguments)


class NodeLetComplex(NodeExpr):
    def __init__(self, nested_lets, body, line, column):
        super().__init__(line= line, column= column)
        self.nestedLets= nested_lets if type(nested_lets) is list else [nested_lets]
        self.body= body

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("nested_lets", self.nestedLets),
            ("body", self.body)
        ])

    def to_readable(self):
        return "{}(nested_lets={}, body={})".format(
            self.clsname, self.nestedLets, self.body)


class NodeLet(NodeExpr):
    def __init__(self, idName, returnType, body, line, column):
        super().__init__(line= line, column= column)
        self.idName= idName
        self.type= returnType
        self.body= body
        

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("idName", self.idName),
            ("returnType", self.type),
            ("body", self.body)
        ])

    def to_readable(self):
        return "{}(idName={}, returnType={}, body={})".format(
            self.clsname, self.idName, self.type,
            self.body)


class NodeIf(NodeExpr):
    def __init__(self, predicate, then_body, else_body, line, column):
        super().__init__(line= line, column= column)
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
    def __init__(self, predicate, body, line, column):
        super().__init__(line= line, column= column)
        self.predicate = predicate
        self.body = body

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("predicate", self.predicate),
            ("body", self.body)
        ])

    def to_readable(self):
        return "{}(predicate={}, body={})".format(self.clsname, 
        self.predicate, self.body)


class NodeCase(NodeExpr):
    def __init__(self, expr, actions, line, column):
        super().__init__(line= line, column= column)
        self.expr = expr
        self.actions = actions

    def to_tuple(self):
        return tuple([
            ("class_name", self.clsname),
            ("expr", self.expr),
            ("actions", self.actions)
        ])

    def to_readable(self):
        return "{}(expr={}, actions={})".format(self.clsname, 
        self.expr, self.actions)


# ############################## UNARY OPERATIONS ##################################


class NodeUnaryOperation(NodeExpr):
    def __init__(self, line, column):
        super().__init__(line= line, column= column)

class NodeIntegerComplement(NodeUnaryOperation):
    def __init__(self, integer_expr, line, column):
        super().__init__(line= line, column= column)
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
    def __init__(self, boolean_expr, line, column):
        super().__init__(line= line, column= column)
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
    def __init__(self, line, column):
        super().__init__(line= line, column= column)
        self.type= ''

class NodeAddition(NodeBinaryOperation):
    def __init__(self, first, second, line, column):
        super().__init__(line= line, column= column)
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
        return "{}(first={}, second={})".format(self.clsname, 
        self.first, self.second)


class NodeSubtraction(NodeBinaryOperation):
    def __init__(self, first, second, line, column):
        super().__init__(line= line, column= column)
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
        return "{}(first={}, second={})".format(self.clsname, 
        self.first, self.second)


class NodeMultiplication(NodeBinaryOperation):
    def __init__(self, first, second, line, column):
        super().__init__(line= line, column= column)
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
        return "{}(first={}, second={})".format(self.clsname, 
        self.first, self.second)


class NodeDivision(NodeBinaryOperation):
    def __init__(self, first, second, line, column):
        super().__init__(line= line, column= column)
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
        return "{}(first={}, second={})".format(self.clsname, 
        self.first, self.second)


class NodeEqual(NodeBinaryOperation):
    def __init__(self, first, second, line, column):
        super().__init__(line= line, column= column)
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
        return "{}(first={}, second={})".format(self.clsname, 
        self.first, self.second)


class NodeLessThan(NodeBinaryOperation):
    def __init__(self, first, second, line, column):
        super().__init__(line= line, column= column)
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
        return "{}(first={}, second={})".format(self.clsname, 
        self.first, self.second)


class NodeLessThanOrEqual(NodeBinaryOperation):
    def __init__(self, first, second, line, column):
        super().__init__(line= line, column= column)
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
        return "{}(first={}, second={})".format(self.clsname, 
        self.first, self.second)



