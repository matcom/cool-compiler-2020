"""Contains Context Structures"""

import itertools as itt
import pprint
from .types import *
from .error import *
from .features import *
from tools.cmp_errors import * 

class Context:
    def __init__(self):
        self.types = {
            'String': StringType(),
            'Int' : IntType(),
            'Object' : ObjectType(),
            'Bool' : BoolType(),
            'IO' : IOType(),
            'SELF_TYPE' : SELF_TYPE()
        }
        self.graph = {}

        # build-in methods
        self.types['Object'].methods['abort'] = Method('abort', [], [], self.types['Object'])
        self.types['Object'].methods['type_name'] = Method('type_name', [], [], self.types['String'])
        self.types['Object'].methods['copy'] = Method('copy', [], [], self.types['Object']) # Must be ret type SELF_TYPE

        self.types['IO'].methods['out_string'] = Method('out_string', ['x'], [self.types['String']], self.types['IO']) # Must be ret type SELF_TYPE
        self.types['IO'].methods['out_int'] = Method('out_int', ['x'], [self.types['Int']], self.types['IO']) # Must be ret type SELF_TYPE
        self.types['IO'].methods['in_string'] = Method('in_string', [], [], self.types['String'])
        self.types['IO'].methods['in_int'] = Method('in_int', [], [], self.types['Int'])

        self.types['String'].methods['length'] = Method('length', [], [], self.types['Int'])
        self.types['String'].methods['concat'] = Method('concat', ['s'], [self.types['String']], self.types['String'])
        self.types['String'].methods['substr'] = Method('substr', ['i', 'l'], [self.types['Int'], self.types['Int']], self.types['String'])

        self.graph['Object'] = ['IO', 'String', 'Bool', 'Int']
        self.graph['IO'] = []
        self.graph['String'] = []
        self.graph['Int'] = []
        self.graph['Bool'] = []

    def create_type(self, name:str):
        if name in self.types:
            raise ContextError(f'Type with the same name ({name}) already in context.')
        typex = Type(name)
        print('---CreateType---')
        print('type: ', typex.name)
        print('parent: ', typex.parent.name)
        self.types[name] = typex
        if not self.graph.__contains__(name):
            self.graph[name] = []
        if self.graph.__contains__(typex.parent.name):
            self.graph[typex.parent.name].append(name)
        else:
            self.graph[typex.parent.name] = [name]
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise ContextError(f'Type "{name}" is not defined.')

    def set_type_tags(self, node='Object', tag=0):
        # print('------Set-----')
        # print('type: ', node)
        # print('tag: ', tag)
        # self.types[node].tag = tag
        # for i,t in enumerate(self.graph[node]):
        #     self.set_type_tags(t, tag + i + 1)
        # print('Done type tags')
        self.types['Object'].tag = 0
        self.types['IO'].tag = 1
        self.types['Main'].tag = 2
        self.types['String'].tag = 2
        self.types['Bool'].tag = 3
        self.types['Int'].tag = 4
            
    def set_type_max_tags(self, node='Object'):
        if not self.graph[node]:
            self.types[node].max_tag = self.types[node].tag
        else:
            for t in self.graph[node]:
                self.set_type_max_tags(t)
            maximum = 0
            for t in self.graph[node]:
                maximum = max(maximum, self.types[t].max_tag)
            self.types[node].max_tag = maximum
        print('Done type max tags')
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
    """ Defines the global scope using a given context """

    def __init__(self, context=None):
        self.context = context
        self.cls_scopes = { }

        if context:
            for cls_name, clsx in context.types.items():
                self.cls_scopes[cls_name] = ClassScope(cls_type=clsx)

    def __str__(self):
        res = '  Program Scope   \n' + '-'*18 + '\nClasses in Program\n' + '-'*18 + '\n\n'
        for name, cls in self.cls_scopes.items():
            res += f'{name}, {str(cls)}\n'
        return res

    def __repr__(self):
        return str(self)

class ClassScope:
    """ Defines the class scope using a given cool class """

    def __init__(self, cls_type=None):
        self.self_type = cls_type
        self.self_var = VariableInfo('self', self.self_type)
        self.parent = None # using in backtrack search
        self.func_scopes = { fname: InnerScope(parent=self) for fname in cls_type.methods.keys() } 
        attr_names = [a.name for a in cls_type.attributes]
        self.attr_scopes = { aname: InnerScope(parent=self) for aname in attr_names}

    def get_attribute(self, name):
        return self.self_var if name == 'self' else self.self_type.get_attribute(name) 

    def is_innerScope(self):
        return False

    def is_class_scope(self):
        return True

    def __str__(self):
        res = 'Class Methods\n' + '-'*25 + '\n'
        for mname, s in self.func_scopes.items():
            res += f'{mname}: {str(s)}\n'
        for aname, s in self.attr_scopes.items():
            res += f'{aname}: {str(s)}\n'
        return res

    def __repr__(self):
        return str(self)

class InnerScope:
    def __init__(self, parent=None):
        self.parent = parent # the scope parent
        self.locals = [ ] # local variables for the current scope
        self.children = [ ]
        self.expr_dict = { }

    def create_child(self):
        child = InnerScope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        if vname == 'self':
            raise ScopeError(SELF_IS_READONLY)

        info = VariableInfo(vname, vtype)
        if info.name in [v.name for v in self.locals]:
            raise ScopeError(f"Identifier {info.name} already defined in this scope")
        else:
            self.locals.append(info)
        return info

    def redefine_variable(self, vname, vtype):
        if vname == 'self':
            raise ScopeError(SELF_IS_READONLY)

        try:
            cvar = next(x for x in self.locals if x.name == vname)
            cvar.type = vtype
            return cvar
        except:
            return self.define_variable(vname, vtype)

    def find_variable(self, vname):
        try:
            return next(x for x in self.locals if x.name == vname)
        except StopIteration:
            if self.parent.is_innerScope():
                return self.parent.find_variable(vname)
            else:
                try:
                    return self.parent.get_attribute(vname)
                except SemanticError:
                    return None

    def get_class_scope(self):
        if self.parent.parent == None:
            return self.parent
        return self.parent.get_class_scope()

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_attribute(self, aname):
        cl_scope = self.get_class_scope()
        return cl_scope.get_attribute(aname) is not None 

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def is_innerScope(self):
        return True

    def is_class_scope(self):
        return False

    def __str__(self, tabs=0):
        res = ('\t' * tabs) + '[ ' + (', '.join( str(local) for local in self.locals )) + ' ]\n'
        if self.children:
            res += '\n'.join(c.__str__(tabs + 1) for c in self.children)
        return res

    def __repr__(self):
        return str(self)