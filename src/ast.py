class AST:
    def __init__(self):
        pass

    @property
    def class_name(self):
        return str(self.__class__.__name__)

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name)
        ])

    def to_readable(self):
        return f"{self.class_name}"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.to_readable())


class Program(AST):
    def __init__(self, classes):
        super(Program, self).__init__()
        self.classes = classes

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("classes", self.classes)
        ])

    def to_readable(self):
        return f"{self.class_name}(classes={self.classes})"


class Class(AST):
    def __init__(self, name, parent, features):
        super(Class, self).__init__()
        self.name = name
        self.parent = parent
        self.features = features

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("name", self.name),
            ("parent", self.parent),
            ("features", self.features)
        ])

    def to_readable(self):
        return f"{self.class_name}(name='{self.name}', parent={self.parent}, features={self.features})"


class ClassFeature(AST):
    def __init__(self):
        super(ClassFeature, self).__init__()


class ClassMethod(ClassFeature):
    def __init__(self, name, formal_params, return_type, body):
        super(ClassMethod, self).__init__()
        self.name = name
        self.formal_params = formal_params
        self.return_type = return_type
        self.body = body

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("name", self.name),
            ("formal_params", self.formal_params),
            ("return_type", self.return_type),
            ("body", self.body)
        ])

    def to_readable(self):
        return f"{self.class_name}(name='{self.name}', formal_params={self.formal_params}, return_type={self.return_type}, body={self.body})"


class ClassAttribute(ClassFeature):
    def __init__(self, name, attr_type, init_expr):
        super(ClassAttribute, self).__init__()
        self.name = name
        self.attr_type = attr_type
        self.init_expr = init_expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("name", self.name),
            ("attr_type", self.attr_type),
            ("init_expr", self.init_expr)
        ])

    def to_readable(self):
        return f"{self.class_name}(name='{self.name}', attr_type={self.attr_type}, init_expr={self.init_expr})"


class FormalParam(ClassFeature):
    def __init__(self, name, param_type):
        super(FormalParam, self).__init__()
        self.name = name
        self.param_type = param_type

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("name", self.name),
            ("param_type", self.param_type)
        ])

    def to_readable(self):
        return f"{self.class_name}(name='{self.name}', param_type={self.param_type})"


class Object(AST):
    def __init__(self, name):
        super(Object, self).__init__()
        self.name = name

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("name", self.name)
        ])

    def to_readable(self):
        return f"{self.class_name}(name='{self.name}')"


class Self(Object):
    def __init__(self):
        super(Self, self).__init__("SELF")

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name)
        ])

    def to_readable(self):
        return f"{self.class_name}"


class Constant(AST):
    def __init__(self):
        super(Constant, self).__init__()


class Integer(Constant):
    def __init__(self, content):
        super(Integer, self).__init__()
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("content", self.content)
        ])

    def to_readable(self):
        return f"{self.class_name}(content={self.content})"


class String(Constant):
    def __init__(self, content):
        super(String, self).__init__()
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("content", self.content)
        ])

    def to_readable(self):
        return f"{self.class_name}(content={self.content})"


class Boolean(Constant):
    def __init__(self, content):
        super(Boolean, self).__init__()
        self.content = content

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("content", self.content)
        ])

    def to_readable(self):
        return f"{self.class_name}(content={self.content})"


class Expr(AST):
    def __init__(self):
        super(Expr, self).__init__()


class NewObject(Expr):
    def __init__(self, new_type):
        super(NewObject, self).__init__()
        self.type = new_type

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("type", self.type)
        ])

    def to_readable(self):
        return f"{self.class_name}(type={self.type})"


class IsVoid(Expr):
    def __init__(self, expr):
        super(IsVoid, self).__init__()
        self.expr = expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("expr", self.expr)
        ])

    def to_readable(self):
        return f"{self.class_name}(expr={self.expr})"


class Assignment(Expr):
    def __init__(self, instance, expr):
        super(Assignment, self).__init__()
        self.instance = instance
        self.expr = expr

    def to_tuple(self):
        return tuple([
            ("class_name", self.class_name),
            ("instance", self.instance),
            ("expr", self.expr)
        ])

    def to_readable(self):
        return f"{self.class_name}(instance={self.instance}, expr={self.expr})"

