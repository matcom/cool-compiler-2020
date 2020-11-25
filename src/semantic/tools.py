import itertools as itt
from utils.errors import SemanticError, AttributesError, TypesError, NamesError
from semantic.types import Type

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str, pos) -> Type:
        if name in self.types:
            error_text = SemanticError.TYPE_ALREADY_DEFINED
            raise SemanticError(error_text, *pos)
        typex = self.types[name] = Type(name, pos)
        return typex

    def get_type(self, name:str, pos) -> Type:
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
    def __init__(self, name, vtype, index=None):
        self.name = name
        self.type = vtype
        self.index = index  # saves the index in the scope of the variable

    def __str__(self):
        return f'{self.name} : {self.type.name}'

    def __repr__(self):
        return str(self)

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.attributes = []
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

    def tab_level(self, tabs, name, num) -> str:
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

    def define_variable(self, vname, vtype) -> VariableInfo:
        info = VariableInfo(vname, vtype)
        if info not in self.locals:
            self.locals.append(info)
        return info

    def find_variable(self, vname, index=None) -> VariableInfo:
        locals = self.attributes + self.locals
        locals = locals if index is None else itt.islice(locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent else None

    def find_local(self, vname, index=None) -> VariableInfo:
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_local(vname, self.index) if self.parent else None

    def find_attribute(self, vname, index=None):
        locals = self.attributes if index is None else itt.islice(self.attributes, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_attribute(vname, index) if self.parent else None


    def get_class_scope(self):
        if self.parent == None or self.parent.parent == None:
            return self
        return self.parent.get_class_scope()

    def is_defined(self, vname) -> VariableInfo:
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def define_attribute(self, attr):
        self.attributes.append(attr)