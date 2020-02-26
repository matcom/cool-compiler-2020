import itertools as itt

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name}: {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.param_infos = [VariableInfo(f'_{name}_{pname}', ptype) for pname, ptype in zip(param_names, params_types)] 
        self.return_type = return_type
        self.return_info = VariableInfo(f'_{name}', return_type)

    def __str__(self):
        params = ', '.join(f'{n}: {t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str, sealed=False, built_in = False):
        self.name = name
        self.attributes = []
        self.methods = {}
        self.parent = None
        self.sealed = sealed
        self.built_in = built_in

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        if parent.sealed:
            raise SemanticError(f'Parent type "{parent.name}" is sealed. Can\'t inherit from it.')
        self.parent = parent

    def type_union(self, other):
        if self == other:
            return other

        t1 = [self]
        while t1[-1] != None:
            t1.append(t1[-1].parent)

        t2 = [other]
        while t2[-1] != None:
            t2.append(t2[-1].parent)

        while t1[-2] == t2[-2]:
            t1.pop()
            t2.pop()

        return t1[-1]

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in self.methods:
            raise SemanticError(f'Method "{name}" already defined in {self.name}')
            # raise SemanticError(f'Method "{name}" already defined in {self.name} with a different signature.')

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

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

class SelfType(Type):
    def __init__(self):
        Type.__init__(self, 'SELF_TYPE')
        self.sealed = True

    def conforms_to(self, other):
        return False

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, SelfType)

class AutoType(Type):
    def __init__(self):
        Type.__init__(self, 'AUTO_TYPE')
        self.sealed = True

    def union_type(self, other):
        return self

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class ErrorType(Type):
    def __init__(self, message = ""):
        Type.__init__(self, '<error>')
        self.sealed = True
        self.message = message

    def union_type(self, other):
        return self

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str, builtin = False):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name,built_in=builtin)
        return typex

    def add_type(self, typex):
        if typex.name in self.types:
            raise SemanticError(f'Type with the same name ({typex.name}) already in context.')
        self.types[typex.name] = typex
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype
        self.infered = not isinstance(vtype, AutoType)
        self.calls = []
        self.assigns = []

    def set_calls(self, typex):
        if not self.infered and not isinstance(typex, AutoType):
            self.calls.append(typex)

    def set_assigns(self, typex):
        if not self.infered:
            self.assigns.append(typex)

    def infer_type(self):
        if not self.infered:
            message = ""
            t = all(not x.built_in for x in self.calls + self.assigns)
            #print(t)
            if t:
                call = None
                for typex in self.calls:
                    if not call or typex.conforms_to(call):
                        call = typex
                    elif call.conforms_to(typex):
                        pass
                    else:
                        call = ErrorType()
                        break

                assign = None
                for typex in self.assigns:
                    assign = typex if not assign else assign.type_union(typex)

                if assign:
                    self.type = assign if not call or assign.conforms_to(call) else ErrorType()
                else:
                    self.type = call

                if not self.type or isinstance(self.type, ErrorType):
                    self.type = AutoType()

                self.infered = not isinstance(self.type, AutoType)
                self.calls = []
                self.assigns = []

                return self.infered, message
            
            else:
                self.type = None
                for x in self.assigns + self.calls:
                    if x.built_in:
                        self.type = x
                        break
                error = []

                #print(self.type.name)

                for x in self.assigns + self.calls:
                    if not x.conforms_to(self.type):
                        error.append(x)
                
                message = f"Incompatible Types {self.type.name} and " + " ".join(e.name for e in error) if error else ""

                self.infered = True

                self.calls = []
                self.assigns = []

                return True, message


        return False, ""

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Variable Name: {self.name}, Variable Type: {self.type} \n'
            

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
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "".join(str(i) for i in self.locals) + "".join(str(s) for s in self.children)
        #return f'Scope: {self.index}\n' + "\n".join(str(x) for x in self.locals) + "\n".join(str(s) for s in self.children) 