import itertools as itt
from utils.errors import SemanticError, AttributesError, TypesError, NamesError

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
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types


class MethodError(Method):
    def __init__(self, name, param_names, param_types, return_types):
        super().__init__(name, param_names, param_types, return_types)

    def __str__(self):
        return f'[method] {self.name} ERROR'


class Type:
    def __init__(self, name:str, pos):
        if name == 'ObjectType':
            return ObjectType(pos)
        self.name = name
        self.attributes = []
        self.methods = {}
        self.parent = ObjectType(pos)
        self.pos = pos

    def set_parent(self, parent):
        if type(self.parent) != ObjectType and self.parent is not None:
            error_text = TypesError.PARENT_ALREADY_DEFINED % self.name
            raise TypesError(error_text, *self.pos)
        self.parent = parent

    def get_attribute(self, name:str, pos):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                error_text = AttributesError.ATTRIBUTE_NOT_DEFINED % (name, self.name)
                raise AttributesError(error_text, *pos)
            try:
                return self.parent.get_attribute(name, pos)
            except AttributesError:
                error_text = AttributesError.ATTRIBUTE_NOT_DEFINED % (name, self.name)
                raise AttributesError(error_text, *pos)

    def define_attribute(self, name:str, typex, pos):
        try:
            self.get_attribute(name, pos)
        except AttributesError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            error_text = AttributesError.ATTRIBUTE_ALREADY_DEFINED %(name, self.name)
            raise AttributesError(error_text, *pos)

    def get_method(self, name:str, pos):
        try:
            return self.methods[name]
        except KeyError:
            error_text = AttributesError.METHOD_NOT_DEFINED %(name, self.name)
            if self.parent is None:
                raise AttributesError(error_text, *pos)
            try:
                return self.parent.get_method(name, pos)
            except AttributesError:
                raise AttributesError(error_text, *pos)

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in self.methods:
            error_text = AttributesError.METHOD_ALREADY_DEFINED % (name, self.name)
            raise AttributesError(error_text, *pos)

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def change_type(self, method, nparm, newtype):
        idx = method.param_names.index(nparm)
        method.param_types[idx] = newtype
                

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

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
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, '<error>', pos)

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, ErrorType)

    def __ne__(self, other):
        return not isinstance(other, ErrorType)

class VoidType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, '<void>', pos)

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class BoolType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, 'Bool', pos)

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)
    
    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, BoolType)


class IntType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, 'Int', pos)

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IntType)

class StringType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, 'String', pos)

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, StringType)

class AutoType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, 'AUTO_TYPE', pos)

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, AutoType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, AutoType)

class ObjectType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Object'
        self.attributes = []
        self.methods = {}
        self.parent = None
        self.pos = pos


    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, ObjectType)

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str, pos):
        if name in self.types:
            error_text = TypesError.TYPE_ALREADY_DEFINED % name
            raise TypesError(error_text, *pos)
        typex = self.types[name] = Type(name, pos)
        return typex

    def get_type(self, name:str, pos):
        try:
            return self.types[name]
        except KeyError:
            error_text = TypesError.TYPE_NOT_DEFINED % name
            raise TypesError(error_text, *pos)

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

    def __str__(self):
        return f'{self.name} : {self.type.name}'

    def __repr__(self):
        return str(self)

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.expr_dict = { }
        self.functions = { }
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def __str__(self):
        res = ''
        for scope in self.children:
            try:
                classx = scope.locals[0]
                name = classx.type.name
            except:
                name = '1'
            res += name + scope.tab_level(1, '', 1) #'\n\t' +  ('\n' + '\t').join(str(local) for local in scope.locals) + '\n'
        return res

    def tab_level(self, tabs, name, num):
        res = ('\t' * tabs) +  ('\n' + ('\t' * tabs)).join(str(local) for local in self.locals)
        if self.functions:
            children = '\n'.join(v.tab_level(tabs + 1, '[method] ' + k, num) for k, v in self.functions.items())
        else:
            children = '\n'.join(child.tab_level(tabs + 1, num, num + 1) for child in self.children)
        return "\t" * (tabs-1) + f'{name}' + "\t" * tabs + f'\n{res}\n{children}'

    def __repr__(self):
        return str(self)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent else None

    def get_class_scope(self):
        if self.parent == None or self.parent.parent == None:
            return self
        return self.parent.get_class_scope()

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def define_attribute(self, attr):
        self.locals.append(attr)