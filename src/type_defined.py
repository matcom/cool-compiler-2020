# clase que representa un tipo en COOL
class CoolType:
    # inherit dice si de este tipo se puede heredar
    def __init__(self, name, parent_type, inherit=True):
        self.name = name
        self.parent_type = parent_type
        self.inherit = inherit
        self.methods = {}
        self.attributes = {}

    def defined(self, method_name):
        return method_name in self.methods.keys()
    
    # en el chequeo semantico se van agregando los metodos y atributos y si se encuentra
    # algun tipo de error se devuelve
    def add_method(self, method_name, args_types, args_names, return_type, expression = None):
        if not self.defined(method_name):
            if len(args_types) != len(args_names):
                args_names = ['a' * i for i, _ in enumerate(args_types)]
            final_args_type = []
            names_added = []
            for i, arg in enumerate(args_types):
                type_of_arg = get_type_by_name(arg)
                if type_of_arg is None:
                    return [f'- TypeError: Class {arg} of formal parameter b is undefined.']
                if len(args_names) > i:
                    final_args_type.append(type_of_arg)
                if args_names[i] in names_added:
                    return [f'- SemanticError: Formal parameter {args_names[i]} is multiply defined.', i]
                else:
                    names_added.append(args_names[i])
            type_of_return = get_type_by_name(return_type)
            if type_of_return is None:
                return 'Method should return something'
            self.methods[method_name] = CoolMethod(method_name, final_args_type, args_names, type_of_return, expression)
            return []
        else:
            # TODO Update error
            return [f'- SemanticError: Method {method_name} is multiply defined.']

    def get_attributes_as_dict(self):
        node = self
        attr = {}
        nodes_list = []
        while node:
            nodes_list = [node] + nodes_list
            node = node.parent_type
        
        for n in nodes_list:
            for attrs in n.attributes.keys():
                if attrs in attr:
                    continue
                attr[attrs] = n.attributes[attrs]

        return attr
 
    def get_attributes(self):
        node = self
        attr = []
        while node:
            for attrs in node.attributes.values():
                if attrs in attr:
                    continue
                attr.append(attrs)
            node = node.parent_type
        return attr

    def get_self_methods(self):
        return self.methods

    # para devolver los metodos que se heredan
    def get_methods_inherited(self):
        node = self.parent_type
        methods = {}
        while node:
            for methodName in node.methods.keys():
                methods[methodName] = node.methods[methodName]
            node = node.parent_type
        return methods

    # para devolver que tipo es el que define cada uno de mis metodos
    def get_owner(self, func):
        mine = self.get_self_methods()

        if func in mine:
            return self.name
        
        owner = ""
        node = self.parent_type
        while node:
            for methodName in node.methods.keys():
                if func in node.methods:
                    return node.name
            node = node.parent_type
        
        return owner

    def get_methods(self):
        selfMethods = self.get_self_methods()
        inheritedMethods = self.get_methods_inherited()
        result = {}

        for key in selfMethods:
            if key in result:
                continue
            result[key] = selfMethods[key]

        for key in inheritedMethods:
            if key in result:
                continue
            result[key] = inheritedMethods[key]

        return result

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
        attr = self.get_attribute_inherited(attribute_name)
        if attr is not None:
            return [f'- SemanticError: Attribute {attribute_name} is an attribute of an inherited class.']
        if attribute_name in self.attributes.keys():
            return [f'- SemanticError: Attribute {attribute_name} is multiply defined in class.']
        class_attr_type = get_type_by_name(attribute_type)
        if not class_attr_type:
            return [f'- TypeError: Class {attribute_type} of attribute {attribute_name} is undefined.', 1]
        self.attributes[attribute_name] = CoolAttribute(attribute_name, class_attr_type, expression)
        return []

    # devolver los atributos heredados
    def get_attribute_inherited(self, attribute_name):
        t = self.parent_type
        while t is not None:
            if attribute_name in t.attributes:
                return t.attributes[attribute_name]
            t = t.parent_type
        return None

    # para devolver los tipos que definen mis atributos
    def get_attribute_owner(self):
        node = self
        AO = {}
        nodes_list = []
        while node:
            nodes_list = [node] + nodes_list
            node = node.parent_type

        for n in nodes_list:
            for attrs in n.attributes.values():
                if attrs.attribute_name == "self":
                    continue
                AO[attrs.attribute_name] = n.name

        return AO
        
    # para devolver a que profundidad estoy del arbol que se forma con los tipos
    # y la herencia entre ellos
    def get_tree_depth(self):
        node = self

        result = 0

        while node:
            result += 1
            node = node.parent_type
        
        return result

    # para devolver que tipo es el que define cada uno de mis metodos
    def get_method_owner(self):
        node = self
        MO = {}
        while node:
            for method in node.methods.values():
                if method.name in MO:
                    continue
                MO[method.name] = node.name
            node = node.parent_type
        return MO

# clase base de un atributo en COOL
class CoolAttribute:
    def __init__(self, attribute_name, attribute_type, expression = None):
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        self.expression = expression

# clase base de un metodo en COOL
class CoolMethod:
    def __init__(self, method_name, args_types, args_names, return_type, expression = None):
        self.name = method_name
        self.args_types = args_types
        self.args_names = args_names
        self.return_type = return_type
        self.expression = expression


# para ponerles identificadores a los metodos que existen,
# esto es usado para optimizar la generacion de codigo en mips
METHODS_NAME_TO_ID = {}
def refresh_methods_id():
    global AllTypes, METHODS_NAME_TO_ID
    id = 0
    for t in AllTypes.keys():
        for m in AllTypes[t].methods.keys():
            if m in METHODS_NAME_TO_ID:
                continue
            METHODS_NAME_TO_ID[m] = id
            id += 1


# devuelve True si el tipo a hereda de b
def inherits(a, b):
    current = a
    while current != b:
        if current is None:
            return False
        current = current.parent
    return True

# devuelve un tipo a partir de su nombre
def get_type_by_name(type_name):
    if type_name in AllTypes:
        return AllTypes[type_name]
    return None


# declarando los tipos por defecto
object_type = CoolType('Object', None)
self_type = CoolType('SELF_TYPE', None, False)
io_type = CoolType('IO', object_type)
string_type = CoolType('String', object_type, False)
int_type = CoolType('Int', object_type, False)
bool_type = CoolType('Bool', object_type, False)

# AllTypes contendra toda la informacion de todos los tipos
AllTypes = {
    'Object': object_type,
    'SELF_TYPE': self_type,
    'IO': io_type,
    'String': string_type,
    'Int': int_type,
    'Bool': bool_type
}

# finalmente agregamos los metodos de los tipos basicos
object_type.add_method('abort', [], [], 'Object')
object_type.add_method('type_name', [], [], 'String')
object_type.add_method('copy', [], [], 'SELF_TYPE')

io_type.add_method('out_string', ['String'], ['s'], 'IO')
io_type.add_method('out_int', ['Int'], ['i'], 'IO')
io_type.add_method('in_string', [], [], 'String')
io_type.add_method('in_int', [], [], 'Int')

string_type.add_method('length', [], [], 'Int')
string_type.add_method('concat', ['String'], ['s'], 'String')
string_type.add_method('substr', ['Int', 'Int'], ['a', 'b'], 'String')

# lista de los tipos basicos
BasicTypes = ['Object', 'SELF_TYPE', 'IO', 'String', 'Int', 'Bool']
