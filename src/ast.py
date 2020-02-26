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
