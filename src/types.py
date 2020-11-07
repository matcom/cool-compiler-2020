class CoolType:
    def __init__(self, name, parent_type):
        self.name = name
        self.parent_type = parent_type
        if not self.parent_type:
            self.inherit = True
        else:
            self.inherit = False
        self.methods = {}
        self.attributes = {}

    def defined(self, method_name):
        return method_name in self.methods.keys()

    def add_method(self, method_name, args_names, return_type):
        if not self.defined(method_name):
            args = []
            for arg in args_names:
                type_of_arg = get_type_by_name(arg)
                if type_of_arg is None:
                    return False
                args.append(type_of_arg)
            type_of_return = get_type_by_name(return_type)
            if type_of_return is None:
                return False
            self.methods[method_name] = CoolMethod(method_name, args, type_of_return)
            return True
        else:
            return False

    def get_attributes(self):
        node = self
        attr = []
        while node:
            for attrs in node.attributes.values():
                attr.append(attrs)
            node = node.parent_type
        return attr

    def get_self_methods(self):
        return self.methods

    def get_methods_inherited(self):
        node = self
        methods = []
        while node:
            for method in node.methods.values():
                method.class_name = node.name
                methods.append(method)
            node = node.parent_type
        return methods

    def get_method_without_inherit(self, method_name, args):
        try:
            method = self.methods[method_name]
        except KeyError:
            return False, None, 'error getting method'
        if len(args) != len(method.args):
            # TODO Update error message
            return False, None, "error , mismatch method args length"
        for i, a in enumerate(args):
            if not inherits(a, method.args[i]):
                return False, None, 'error args methods'
        return True, method, None

    def get_method(self, method_name, args):
        exist, method, error_message = self.get_method_without_inherit(method_name, args)
        if not exist and self.parent_type:
            return self.parent_type.get_method(method_name, args)
        elif exist:
            return exist, None
        return None, error_message

    def add_attribute(self, attribute_name, attribute_type, expression):
        attr = self.get_attribute(attribute_name)
        if attr is not None:
            return False
        class_attr_type = get_type_by_name(attribute_type)
        if not class_attr_type:
            return False
        self.attributes[attribute_name] = CoolAttribute(attribute_name, class_attr_type, expression)
        return True

    def get_attribute(self, attribute_name):
        t = self
        while t is not None:
            if attribute_name in t.attributes:
                return t.attributes[attribute_name]
            t = t.parent_type
        return None


class CoolAttribute:
    def __init__(self, attribute_name, attribute_type, expression):
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        self.expression = expression


class CoolMethod:
    def __init__(self, method_name, args, return_type):
        self.name = method_name
        self.args = args
        self.return_type = return_type


def inherits(a, b):
    current = a
    while current != b:
        if current is None:
            return False
        current = current.parent
    return True


def get_type_by_name(type_name):
    if type_name in AllTypes:
        return AllTypes[type_name]
    return None


# Declaring default types
self_type = CoolType('SELF_TYPE', None)
io_type = CoolType('IO', None)
string_type = CoolType('String', None)
int_type = CoolType('Int', None)
bool_type = CoolType('Bool', None)

AllTypes = {
    'SELF_TYPE': self_type,
    'IO': io_type,
    'String': string_type,
    'Int': int_type,
    'Bool': bool_type
}
