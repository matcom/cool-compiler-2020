from AstNodes import *
import visitor as visitor
import queue
from collections import OrderedDict
import itertools as itt



class SemanticError(Exception):
    @property
    def text(self):
        return f'({self.args[1]},-1) - {self.__class__.__name__}: {self.args[0]}'
class TypeError(SemanticError):
    pass
class NameError(SemanticError):
    pass 

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

class Type:
    def __init__(self, name:str,line=-1):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        self.sons = []
        self.line = line

    def set_parent(self, parent, pos=0):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}', pos)
        self.parent = parent
        parent.sons.append(self)

    def get_attribute(self, name:str,pos=0):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}',pos)
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}',pos)

    def define_attribute(self, name:str, typex, pos):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}',pos)

    def get_method(self, name:str,pos=0):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}',pos)
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}',pos)

    def define_method(self, name:str, param_names:list, param_types:list,  return_type, pos):
        try:
            method = self.get_method(name, pos)
        except SemanticError:
            pass
        else:
            if method.return_type != return_type or method.param_types != param_types:
                raise SemanticError(f'Method "{name}" already defined in {self.name} with a different signature.', pos)

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

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
        output += '\n\t'.join(str(x) for x in self.methods)
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

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class SELF_TYPE(Type):
    def __init__(self):
        Type.__init__(self, "SELF_TYPE")

    def __eq__(self, other):
        return isinstance(other, SELF_TYPE)

class Context:
    def __init__(self):
        self.types = {}
        self.bassic_classes()

    def bassic_classes(self):
        Bool = Type("Bool")
        self.types["Bool"] = Bool

        Int = Type("Int")
        self.types["Int"] = Int

        Object = Type("Object")
        String = Type("String")
        IO = Type("IO")

        Object.define_method("abort",[],[],Object,0)
        Object.define_method("type_name",[],[],String,0)
        Object.define_method("copy",[],[],SELF_TYPE(),0)
        self.types["Object"] =Object

        String.define_method("length",[],[],Int,0)    
        String.define_method("concat",['s'],[String],String,0) 
        String.define_method("substr",['i','l'],[Int,Int],SELF_TYPE(),0)   
        self.types["String"] = String

        IO.define_method("out_string",["x"],[String],SELF_TYPE(),0)
        IO.define_method("out_int",['x'],[Int],SELF_TYPE(),0)
        IO.define_method("in_int",[],[],Int,0)
        IO.define_method("in_string",[], [], String, 0)
        self.types['IO']= IO


    def check_type(self,x:Type,y:Type,pos):
        if not x.conforms_to(y) :
            raise(TypeError(f"Expr type {x.name} is no subclass of {y.name} ",pos))

    def create_type(self, name:str,pos=0):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.' , pos)
        typex = self.types[name] = Type(name,pos)
        return typex

    def get_type(self, name:str,pos=0):
        try:
            return self.types[name]
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.' , pos)

    def closest_common_antecesor(self, typexa:Type, typexb:Type):
        antecesor = []
        while not typexa is None or not typexb is None :
            if not typexb is None :
                if typexb in antecesor:
                    return typexb
                antecesor.append(typexb)

            if not typexa is None:
                if typexa in antecesor:
                    return typexa
                antecesor.append(typexa)
            
            if not typexa is None:
                typexa = typexa.parent
            if not typexb is None:
                typexb = typexb.parent

        return self.get_type("Object") 

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype, cilName=''):
        self.name = name
        self.type = vtype
        self.cilName = cilName

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.id = 0
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        child.id = self.id*10 +len(self.children)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype,pos=0):
        if  self.is_local(vname):
            raise SemanticError(f"Variable {vname} already define in scope " , pos)
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            if not self.parent is None:
                return self.parent.find_variable(vname, self.index)  
            else:
                return None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
class CoolSemantic:

    def __init__(self , ast):
        self.ast = ast
        self.mask = set()

    def check_semantics(self):
        errors = []
        collector = TypeCollector(errors)
        collector.visit(self.ast)
        context = collector.context
        #builder = TypeBuilder(context, errors)
        #builder.visit(self.ast)
        cycles = self.check_for_cycles(context)
        for cycle in cycles :
            errors.append(SemanticError(f"Class {cycle[0][0]},  is involved in an inheritance cycle.",cycle[0][1]))
            return errors
        builder = TypeBuilder(context,errors)
        builder.visit(self.ast)
        typechecking = TypeChecking (context,errors)
        scope = Scope()
        typechecking.visit(self.ast, scope)
        #print('Context:')
        #print(context)
        return errors, context , scope

    def check_for_cycles(self , context):
        visited = set()
        on_cycle = {}
        count = 0
        for tp in context.types:
            temp = context.types[tp]
            ancestor = set()
            while 1:
                if temp.name in visited:
                    break
                ancestor.add(temp.name)
                visited.add(temp.name)
                if temp.parent is None:
                    break
                if temp.parent.name in ancestor:
                    on_cycle[count] = []
                    on_cycle[count].append((temp.name,temp.line))
                    temp2 = temp.parent
                    while temp != temp2:
                        on_cycle[count].append((temp2.name,temp2.line))
                        temp2 = temp2.parent
                    on_cycle[count].sort(key= lambda x:x[1],reverse=True)
                    count = count + 1
                    break
                temp = temp.parent
        return on_cycle.values()
  
            

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        # Your code here!!!
        for decl in node.declarations:
            self.visit(decl)
        for dec_node in node.declarations:
            try:
                if dec_node.parent is not None:
                    self.context.get_type(dec_node.id, dec_node.line).set_parent(self.context.get_type(dec_node.parent,dec_node.line),node.line)
            except SemanticError as e:
                self.errors.append(e)
    # Your code here!!!
    # ????
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id,node.line)
        except SemanticError as e:
            self.errors.append(e)

def sort_types(types):
        q = queue.deque()
        lst = []
        for tp in types:
            if types[tp].parent is None:
                if tp != "Object":
                    types[tp].set_parent( types["Object"])

        q.append("Object")
        while len(q) != 0:
            tp = q.popleft()
            lst.append(tp)
            for son in types[tp].sons:
                q.append(son.name)
        return lst        
            
class TypeBuilder:
    def __init__(self, context:Context, errors=[]):
        self.context = context
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    # Your code here!!!
    # ????
    @visitor.when(ProgramNode)
    def visit(self, node):
        nodec={ def_class.id:def_class for def_class in node.declarations}
        sorted_types = sort_types(self.context.types)
        for stypes in sorted_types:
            if stypes in nodec:
                self.visit(nodec[stypes])
        
            
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):

        self.current_type = self.context.get_type(node.id,node.line)
        for feature in node.features:
            self.visit(feature)
            
        # dont forget the parent class
        # and check errors
        
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):        
        try:
            attr_type = SELF_TYPE() if node.type == "SELF_TYPE" else self.context.get_type(node.type,node.line)
            if node.id == "self":
                    raise SemanticError('Trying to assign value to self' ,node.line)  
            self.current_type.define_attribute(node.id, attr_type, node.line)
        except SemanticError as e:
            self.errors.append(e)
        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        arg_names = [param[0] for param in node.params]
        arg_types = []
        for param in node.params:
            try:
                arg_types.append(self.context.get_type(param[1],node.line) )
            except SemanticError as e:
                self.errors.append(e)
                arg_types.append(ErrorType())
        try:
            ret_type = SELF_TYPE() if node.type =="SELF_TYPE" else self.context.get_type(node.type,node.line)
        except SemanticError as e:
            self.errors.append(e)
            ret_type = ErrorType()
        try:
            self.current_type.define_method(node.id, arg_names, arg_types, ret_type, node.line)
        except SemanticError as e:
            self.errors.append(e)

class TypeChecking:
    def __init__(self, context:Context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope=None):
        for dec in node.declarations:
            try:
                self.visit(dec,scope.create_child())
            except SemanticError as e:
                self.errors.append(e)


    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):      
        try :
            typex = self.context.get_type(node.id, node.line)
        except SemanticError as e:
            self.errors.append(e)

        self.current_type = typex
        #for at in typex.all_attributes():
        #    scope.define_variable(at[0].name, at[0].type,node.line)
        scope.define_variable("self",typex,node.line)
        mscope = scope.create_child()
        ascope = scope.create_child()
        for feat in node.features:
            if isinstance(feat, FuncDeclarationNode):
                self.visit(feat,mscope.create_child())
            else:
                self.visit(feat, ascope.create_child())

    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode,scope:Scope):
        self.visit(node.expression, scope.create_child())
        if not node.expression is None:
            try:
                typex =self.current_type if node.type == "SELF_TYPE" else self.context.get_type(node.type,node.line)
                self.context.check_type(node.expression.type,typex,node.line)
            except SemanticError as e:
                self.errors.append(e)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode,scope:Scope):
        method = self.current_type.get_method(node.id)
        for i in range(len(method.param_names)):
            try:
                if method.param_names[i] == "self":
                    raise SemanticError('Trying to assign value to self' ,node.line)   
                scope.define_variable(method.param_names[i],method.param_types[i],node.line)
            except SemanticError as e:
                self.errors.append(e)

        self.visit(node.body,scope.create_child())
        try:
            typex = method.return_type if not isinstance(method.return_type,SELF_TYPE) else self.current_type
            self.context.check_type(node.body.type,typex,node.line)
        except SemanticError as e:
            self.errors.append(e)
        

    @visitor.when(CaseOfNode)
    def visit(self, node:CaseOfNode, scope:Scope):
        node.type = ErrorType()
        sce = scope.create_child()
        self.visit(node.expression, sce)
        scb = scope.create_child()
        common_type = None
        for branches in node.branches:
            tmpscope = scb.create_child()
            try :
                typex = self.context.get_type(branches[1],node.line)
                if common_type is None:
                    common_type = typex
                else:
                    common_type = self.context.closest_common_antecesor(common_type,typex)
            except SemanticError as e:
                self.errors.append(e)
            tmpscope.define_variable(branches[0],typex,node.line)
            self.visit(branches[2],tmpscope)
        
        node.type = common_type
        
        



    @visitor.when(FunctionCallNode)
    def visit(self, node:FunctionCallNode, scope:Scope):    
        self.visit(node.obj,scope.create_child())
        node.type = ErrorType()

        for i in range(len(node.args)):
            self.visit(node.args[i],scope.create_child())

        if not node.typex is None:            
            try:
                temp = self.context.get_type(node.typex,node.line)
                self.context.check_type(node.obj.type,temp,node.line)
            except SemanticError as e:
                self.errors.append(e)
                return
        else:
            if  isinstance( node.obj.type , ErrorType):
                return
            node.typex = node.obj.type.name
        try:
            typex = self.context.get_type(node.typex,node.line)
        except SemanticError as e:
            self.errors.append(e)
            return
        try :
            if  isinstance( typex , ErrorType):
                return
            method = typex.get_method(node.id,node.line)
            ret_type = method.return_type  if not isinstance(method.return_type,SELF_TYPE) else typex    
            node.type = ret_type
            if len(method.param_types) != len(node.args):
                raise SemanticError (f'Method takes {len(method.param_types)} params but {len(node.args)} were given', node.line)
            for i in range(len(node.args)):
                try:
                    self.context.check_type(node.args[i].type,method.param_types[i],node.line)
                except SemanticError as e:
                    self.errors.append(e)
        except SemanticError as e:
            self.errors.append(e)  

    @visitor.when(MemberCallNode)
    def visit(self, node:MemberCallNode, scope:Scope):    
        node.type = ErrorType()

        for i in range(len(node.args)):
            self.visit(node.args[i],scope.create_child())

        typex = self.current_type
        try :
            if  isinstance( typex , ErrorType):
                return
            method = typex.get_method(node.id, node.line)
            ret_type = method.return_type  if not isinstance(method.return_type,SELF_TYPE) else typex    
            node.type = ret_type
            if len(method.param_types) != len(node.args):
                raise SemanticError (f'Method takes {len(method.param_types)} params but {len(node.args)} were given')
            for i in range(len(node.args)):
                try:
                    self.context.check_type(node.args[i].type,method.param_types[i],node.line)
                except SemanticError as e:
                    self.errors.append(e)
        except SemanticError as e:
            self.errors.append(e)


        

    @visitor.when(IfThenElseNode)
    def visit(self,node:IfThenElseNode,scope:Scope):
        self.visit(node.condition,scope.create_child())
        try:
            self.context.check_type(node.condition.type,self.context.get_type("Bool"),node.line)
        except SemanticError as e:
            self.errors.append(e)
        
        self.visit(node.if_body,scope.create_child())
        
        self.visit(node.else_body, scope.create_child())

        try:    
            node.type = self.context.closest_common_antecesor(node.if_body.type, node.else_body.type)
        except SemanticError as e:
            self.errors.append(e)
            node.type =  ErrorType()


    @visitor.when(AssignNode)
    def visit(self, node:AssignNode,scope:Scope):
        self.visit(node.expression, scope.create_child())
        try:
            if node.id == "self":
                raise SemanticError('Trying to assign value to self' ,node.line)
                
            var = scope.find_variable(node.id)
            
            if var is None:
                try:
                    at =  [ at[0] for at in self.current_type.all_attributes() if at[0].name == node.id]
                    var = at[0]
                except:
                    raise NameError(f"Variable {node.id} not defined",node.line)

            typex = self.current_type if isinstance(var.type , SELF_TYPE) else var.type
            self.context.check_type(node.expression.type, typex, node.line)
            node.type = node.expression.type
        except SemanticError as e:
            self.errors.append(e)
            node.type = node.expression.type
     

    @visitor.when(WhileLoopNode)
    def visit(self , node:WhileLoopNode, scope:Scope):
        self.visit(node.condition, scope.create_child())
        if self.context.get_type("Bool",node.line) != node.condition.type:
            self.errors.append(SemanticError("Expr should be boolean", node.line))
        self.visit(node.body, scope.create_child())
        node.type = self.context.get_type("Object",node.line)
          

    @visitor.when(BlockNode)
    def visit (self, node:BlockNode, scope:Scope):
        for expr in node.expressions:
            self.visit(expr,scope.create_child())
        node.type = node.expressions[-1].type
        

    @visitor.when(LetInNode)
    def visit(self, node:LetInNode,scope:Scope):
        sc = scope.create_child()
        for init in node.let_body:
            if not init[2] is None:
                self.visit(init[2],sc)
                try:
                    typex = self.context.get_type(init[1],node.line) if  init[1] != "SELF_TYPE" else self.current_type
                    self.context.check_type(init[2].type,typex,node.line)
                except SemanticError as e:
                    self.errors.append(e)

            sc = sc.create_child()
            typex= None
            try:
                typex = self.context.get_type(init[1],node.line) if  init[1] != "SELF_TYPE" else self.current_type
            except SemanticError as e:
                self.errors.append(e)
                typex = ErrorType()
            try:    
                if init[0] == "self":
                    raise SemanticError('Trying to assign value to self' ,node.line)    
                sc.define_variable(init[0],typex,node.line)
            except SemanticError as e:
                self.errors.append(e)
        
        sc = sc.create_child()
        node.body_scope=sc
        self.visit(node.in_body,sc)
        node.type = node.in_body.type
        

    @visitor.when(NewNode)
    def visit(self, node:NewNode,scope:Scope):
        try:
            if node.type == "SELF_TYPE":
                node.type= self.current_type
            else:
                node.type = self.context.get_type(node.type,node.line)
        except SemanticError as e:
            self.errors.append(e)
            node.type = ErrorType()

        

    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope:Scope):
       
        self.visit(node.expression,scope.create_child())
        node.type = self.context.get_type("Bool", node.line)
        

    @visitor.when(ArithmeticNode)
    def visit(self, node:ArithmeticNode,scope:Scope):
        self.visit(node.left,scope.create_child())
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        self.visit(node.right,scope.create_child())
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        node.type = self.context.get_type("Int", node.line)
        

    @visitor.when(LessNode)
    def visit(self, node:LessNode,scope:Scope):
        self.visit(node.left,scope.create_child())
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        self.visit(node.right,scope.create_child())
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        node.type = self.context.get_type("Bool", node.line)

    @visitor.when(LessEqualNode)
    def visit(self, node:LessEqualNode, scope:Scope):
        self.visit(node.left,scope.create_child())
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        self.visit(node.right,scope.create_child())
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        node.type = self.context.get_type("Bool", node.line)

    @visitor.when(EqualNode)
    def visit(self, node:EqualNode, scope:Scope):
        self.visit(node.left,scope.create_child())
        self.visit(node.right,scope.create_child())
        if node.left.type != node.right.type:
            basic = ['Int', 'String', 'Bool']
            if node.left.type.name in basic or node.right.type.name in basic:
                self.errors.append(TypeError("Exprs must have same type", node.line))
        node.type = self.context.get_type("Bool", node.line)

    @visitor.when(ComplementNode)
    def visit(self, node:ComplementNode, scope:Scope):
        self.visit(node.expression, scope.create_child())
        if node.expression.type != self.context.get_type("Int", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        node.type = self.context.get_type("Int", node.line)

    @visitor.when(NotNode)
    def visit(self, node:NotNode, scope:Scope):
        self.visit(node.expression, scope.create_child())
        if node.expression.type != self.context.get_type("Bool", node.line):
            self.errors.append(TypeError ("Expr must be an integer" ,node.line))
        node.type = self.context.get_type("Bool", node.line)


    @visitor.when(IntegerNode)
    def visit (self, node:IntegerNode,scope:Scope):
        node.type = self.context.get_type("Int", node.line)        

    @visitor.when(StringNode)
    def visit (self, node:StringNode, scope:Scope):
        node.type = self.context.get_type("String", node.line)

    @visitor.when(BoolNode)
    def visit (self, node:BoolNode, scope:Scope):
        node.type = self.context.get_type("Bool",node.line)

    @visitor.when(IdNode)
    def visit (self, node:IntegerNode,scope:Scope):
    
        x = scope.find_variable(node.token)
        if x is None:
            try:
                at =  [ at[0] for at in self.current_type.all_attributes() if at[0].name == node.token]
                x = at[0]
            except:    
                node.type = ErrorType()
                self.errors.append(NameError(f"Variable {node.token} not defined",node.line))
                return
        node.type = x.type if not isinstance(x.type , SELF_TYPE) else self.current_type
       
