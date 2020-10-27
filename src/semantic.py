import itertools as itt


class SemanticException(Exception):
    @property
    def text(self):
        return self.args[0]

class ErrorSemantic():
    def __init__(self, message, line, column):
        self.type = 'SemanticError'
        self.value = message
        self.line = line
        self.column = column
        self.text = f'({self.line}, {self.column}) - {self.type}: {self.value}'

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.type}: {self.value}'

    def __repr__(self):
        return str(self)


class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)


class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n, t in zip(
            self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types


class Type:
    def __init__(self, name: str):
        self.name = name
        self.sealed = False  # indicates if this type is restricted for inheritance
        self.attributes = []
        self.methods = {}
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticException(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def has_attr(self, name: str):
        try: 
            attr_name = get_attribute(name)
        except:
            return False
        return True

    def get_attribute(self, name: str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticException(
                    f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticException:
                raise SemanticException(
                    f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name: str, typex):
        try:
            self.get_attribute(name)
        except SemanticException:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticException(
                f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name: str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticException(
                    f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticException:
                raise SemanticException(
                    f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name: str, param_names: list, param_types: list, return_type):
        try:
            method = self.get_method(name)
        except SemanticException:
            method = self.methods[name] = Method(
                name, param_names, param_types, return_type)
            return method
        else:
            try:
                self.methods[name]
            except KeyError:
                if method.return_type != return_type or method.param_types != param_types:
                    raise SemanticException(
                        f'Method "{name}" is already defined in {self.name} with a different signature')
            else:
                raise SemanticException(
                    f'Method "{name}" is already defined in {self.name}')

        return method

    def get_all_attributes(self):
        all_attributes = self.parent and self.parent.get_all_attributes() or []
        all_attributes += self.attributes
        return all_attributes
    
    def get_all_methods(self):
        all_methods = self.parent and self.parent.get_all_methods() or []
        all_methods += [(self.name, method) for method in self.methods]
        
        return all_methods

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def ancestors_path(self):
        """
        Return a list with all ancestors of the self type, starting by self
        """
        l = []
        l.append(self)
        current_parent = self.parent
        while (current_parent is not None):
            l.append(current_parent)
            current_parent = current_parent.parent
        return l

    def join(self, other):
        """
        Return the least type C such as self <= C and other <= C
        """

        if self.name == other.name:  # A |_| A = A
            return self

        other_path = other.ancestors_path()
        for p in self.ancestors_path():
            for o in other_path:
                if o.name == p.name:
                    return p
        return other

    def multiple_join(self, args):
        """
        Return the least type C such as all type in args conforms with C
        """
        least_type = self
    
        for t in args:
            if isinstance(least_type, ErrorType) or isinstance(t, ErrorType):
                least_type = ErrorType()
                return least_type
            least_type = least_type.join(t)

        return least_type

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods.values())
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)


class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')

    def bypass(self):
        return True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)


class IOType(Type):
    def __init__(self):
        Type.__init__(self, 'IO')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IOType)


class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String')
        self.sealed = True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)


class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'Int')
        self.sealed = True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)


class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')
        self.sealed = True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)


class Context:
    def __init__(self):
        self.types = {}
        self.graph = {}
        self.classes = {}
        self.types['ErrorType'] = ErrorType()

    def create_builtin_types(self):
        self.types['SELF_TYPE'] = Type('SELF_TYPE')

        self.types['Object'] = ObjectType()
        self.types['IO'] = IOType()
        self.types['String'] = StringType()
        self.types['Int'] = IntType()
        self.types['Bool'] = BoolType()
        self.graph['Object'] = ['IO', 'String', 'Bool', 'Int']
        self.graph['IO'] = []
        self.graph['String'] = []
        self.graph['Int'] = []
        self.graph['Bool'] = []

        self.types['IO'].set_parent(self.types['Object'])
        self.types['String'].set_parent(self.types['Object'])
        self.types['Int'].set_parent(self.types['Object'])
        self.types['Bool'].set_parent(self.types['Object'])

        self.types['Object'].define_method('abort', [], [], self.types['Object'])
        self.types['Object'].define_method('type_name', [], [], self.types['String'])
        self.types['Object'].define_method('copy', [], [], self.types['SELF_TYPE'])

        self.types['IO'].define_method('out_string', ['x'], [self.types['String']], self.types['SELF_TYPE'])
        self.types['IO'].define_method('out_int', ['x'], [self.types['Int']], self.types['SELF_TYPE'])
        self.types['IO'].define_method('in_string', [], [], self.types['String'])
        self.types['IO'].define_method('in_int', [], [], self.types['Int'])

        self.types['String'].define_method('length', [], [], self.types['Int'])
        self.types['String'].define_method('concat', ['s'], [self.types['String']], self.types['String'])
        self.types['String'].define_method('substr', ['i', 'l'], [self.types['Int'], self.types['Int']], self.types['String'])



    def create_type(self, node):
        if node.name in self.types:
            raise SemanticException(
                f'Type with the same name ({node.name}) already in context.')
        typex = self.types[node.name] = Type(node.name)
        self.classes[node.name] = node
        if not self.graph.__contains__(node.name):
            self.graph[node.name] = []
        if self.graph.__contains__(node.parent):
            self.graph[node.parent].append(node.name)
        else:
            self.graph[node.parent] = [node.name]
        return typex

    def get_type(self, name: str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticException(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)


class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(
            self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if (self.parent is not None) else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def remove_local(self, vname):
        self.locals = [local for local in self.locals if local.name != vname]
