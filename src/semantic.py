from AstNodes import *
import visitor as visitor
import queue

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

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

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = {}
        self.parent = None
        self.sons = []
        self.height = -1

    def set_parent(self, parent,pos=0):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name} {pos}.')
        if parent.name in ["Int","String", "Bool"]:
            raise SemanticError(f'Types can\'t have basic type "{parent.name}" as parent {pos}')
        self.parent = parent
        parent.sons.append(self)

    def get_attribute(self, name:str, pos=0):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name} {pos}.')
            try:
                return self.parent.get_attribute(name, pos)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name} {pos}.')

    def define_attribute(self, name:str, typex, pos):
        try:
            self.get_attribute(name, pos=0)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name} {pos}.')

    def get_method(self, name:str, pos=0):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name} {pos}.')
            try:
                return self.parent.get_method(name, pos)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name} {pos}.')

    def define_method(self, name:str, param_names:list, param_types:list,  return_type, pos):
        try:
            method = self.get_method(name, pos)
        except SemanticError:
            pass
        else:
            if method.return_type != return_type or method.param_types != param_types:
                raise SemanticError(f'Method "{name}" already defined in {self.name} with a different signature {pos}.')

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def inherits_from(self, a):
        if a.name == 'Object':
            return True
        temp = self
        while True:
            if temp == a:
                return True
            if temp.parent is None:
                return False
            temp = temp.parent

    def __str__(self):
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output = f'type {self.name}'
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

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def __eq__(self, other):
        return isinstance(other, VoidType)

class SELF_TYPE(Type):
    def __init__(self):
        Type.__init__(self, 'SELF_TYPE')

    def __eq__(self, other):
        return isinstance(other, SELF_TYPE)

class Context:
    def __init__(self):
        self.types = {}
        self.locals = {}
        self.parent = None
        self.current_type = None
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

        IO.define_method("out_string",["x"],[String],SELF_TYPE(),0)
        IO.define_method("out_int",['x'],[Int],SELF_TYPE,0)
        IO.define_method("in_int",[],[],Int,0)
        
        String.define_method("lenght",[],[],Int,0)    
        String.define_method("concat",['s'],[String],String,0) 
        String.define_method("substr",['i','l'],[Int,Int],SELF_TYPE(),0)   
        self.types["String"] = String
        

    def child_context(self):
        child = Context()
        child.types = self.types
        child.parent = self
        child.current_type = self.current_type
        return child

    def create_type(self, name:str, pos=0):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context {pos}.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str, pos=0):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined {pos}.')

    def define_local(self, name:str, typex, pos):
        if name in self.locals:
            raise SemanticError(f'Variable with the same name "{name}" already in context {pos}')            
        attr= Attribute(name, typex)
        self.locals[name] = attr
        return attr 

    def get_local(self, name:str, pos=0):
        try:
            return self.locals[name]
        except KeyError:
            if self.parent is None:
                try:
                    return self.current_type.get_attribute(name)
                except :
                    raise SemanticError(f'Variable "{name}" is not defined {pos}')
            try:
                return self.parent.get_local(name, pos)
            except :                
                try:
                    return self.current_type.get_attribute(name)
                except SemanticError as e:
                    raise SemanticError(f'Variable "{name}" is not defined {pos}')
                    

    def sort_types(self):
        q = queue.deque()
        lst = []
        for tp in self.types:
            if self.types[tp].parent is None:
                if tp != "Object":
                    self.types[tp].set_parent( self.types["Object"])

        q.append("Object")
        while len(q) != 0:
            tp = q.popleft()
            lst.append(tp)
            for son in self.types[tp].sons:
                q.append(son.name)
        return lst

    def inherits_from(self,a:Type, b:Type, pos=0):
        return a.inherits_from(b)
        
    def check_type(self,x,y,pos):
        if not self.inherits_from(x, y, pos) :
            raise(SemanticError(f"Expr type {x.name} is no subclass of {y.name} {pos}"))

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
        self.check_for_cycles(context)
        builder = TypeBuilder(context,errors)
        builder.visit(self.ast)
        typechecking = TypeChecking (context,errors)
        typechecking.visit(self.ast)
        print('Context:')
        print(context)
        return errors

    def check_for_cycles(self , context):
        visited = set()
        on_cycle = set()
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
                    on_cycle.add(temp)
                    break
                temp = temp.parent

  
            

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
        sorted_types = self.context.sort_types()
        for stypes in sorted_types:
            if stypes in nodec:
                self.visit(nodec[stypes])
        
            
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):

        self.context.current_type = self.context.get_type(node.id,node.line)
        for feature in node.features:
            self.visit(feature)
            
        # dont forget the parent class
        # and check errors
        
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):        
        try:
            attr_type = self.context.get_type(node.type,node.line)
            self.context.current_type.define_attribute(node.id, attr_type, node.line)
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
            self.context.current_type.define_method(node.id, arg_names, arg_types, ret_type, node.line)
        except SemanticError as e:
            self.errors.append(e)

class TypeChecking:
    def __init__(self, context:Context, errors=[]):
        self.context = context
        self.context.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        for dec in node.declarations:
            try:
                self.visit(dec)
            except SemanticError as e:
                self.errors.append(e)

#Declarations
    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode):
        parent_contex = self.context
        self.context = self.context.child_context()
        try :
            typex = self.context.get_type(node.id, node.line)
        except SemanticError as e:
            self.errors.append(e)

        self.context.current_type = typex
        self.context.define_local("self" , typex, node.line)
        for feat in node.features:
            self.visit(feat)
        self.context = parent_contex
        self.context.current_type = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode):
        self.visit(node.expression)
        if not node.expression is None:
            try:
                typex =self.context.current_type if node.type == "SELF_TYPE" else self.context.get_type(node.type,node.line)
                self.context.check_type(node.expression.type,typex,node.line)
            except SemanticError as e:
                self.errors.append(e)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode):
        parent_contex = self.context
        self.context = self.context.child_context()
        method = self.context.current_type.get_method(node.id)
        for i in range(len(method.param_names)):
            try:
                self.context.define_local(method.param_names[i],method.param_types[i],node.line)
            except SemanticError as e:
                self.errors.append(e)

        self.visit(node.body)
        try:
            typex = method.return_type if not isinstance(method.return_type,SELF_TYPE) else self.context.current_type
            self.context.check_type(node.body.type,typex,node.line)
        except SemanticError as e:
            self.errors.append(e)
        self.context = parent_contex

    @visitor.when(MemberCallNode)
    def visit(self, node:FunctionCallNode):
        parent_contex = self.context
        self.context = self.context.child_context()
        node.type = ErrorType()
        self.context = parent_contex
    
    @visitor.when(FunctionCallNode)
    def visit(self, node:FunctionCallNode):
        parent_contex = self.context
        self.context = self.context.child_context()
        self.visit(node.obj)
        node.type = ErrorType()
        for i in range(len(node.args)):
            self.visit(node.args[i])

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
            method = typex.get_method(node.id)
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
        self.context = parent_contex

    @visitor.when(IfThenElseNode)
    def visit(self,node:IfThenElseNode):
        parent_contex = self.context
        self.context = self.context.child_context()
        self.visit(node.condition)
        try:
            self.context.check_type(node.condition.type,self.context.get_type("Bool"),node.line)
        except SemanticError as e:
            self.errors.append(e)
        
        self.visit(node.if_body)
        
        self.visit(node.else_body)

        try:    
            node.type = self.context.closest_common_antecesor(node.if_body.type, node.else_body.type)
        except SemanticError as e:
            self.errors.append(e)
            node.type =  ErrorType()
        self.context = parent_contex

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode):
        parent_contex = self.context 
        self.context = self.context.child_context()
        
        self.visit(node.expression)
        try:
            if node.id == self:
                raise SemanticError(f'Trying to assign value to self {node.line}')    
            var = self.context.get_local(node.id,node.line)
            self.context.check_type(node.expression.type, var.type, node.line)
            node.type = node.expression.type
        except SemanticError as e:
            self.errors.append(e)
            self.type = node.expression.type
        self.context = parent_contex

    @visitor.when(WhileLoopNode)
    def visit(self , node:WhileLoopNode):
        parent_contex = self.context 
        self.context = self.context.child_context()
            
        self.visit(node.condition)
        if self.context.get_type("Bool",node.line) != node.condition.type:
            self.errors.append(SemanticError("Expr should be boolean"))
        self.visit(node.body)
        self.type = self.context.get_type("Object",node.line)
        self.context = parent_contex    

    @visitor.when(BlockNode)
    def visit (self, node:BlockNode):
        parent_contex = self.context 
        self.context = self.context.child_context()
        for expr in node.expressions:
            self.visit(expr)
        node.type = node.expressions[-1].type
        self.context = parent_contex

    @visitor.when(LetInNode)
    def visit(self, node:LetInNode):
        parent_contex = self.context 
        self.context = self.context.child_context()
        for init in node.let_body:
            if not init[2] is None:
                self.visit(init[2])
                try:
                    self.context.check_type(init[2].type,self.context.get_type(init[1],node.line),node.line)
                except SemanticError as e:
                    self.errors.append(e)

            self.context = self.context.child_context()
            typex= None
            try:
                typex = self.context.get_type(init[1],node.line)
            except SemanticError as e:
                self.errors.append(e)
                typex = ErrorType()
            try:    
                self.context.define_local(init[0],typex,node.line)
            except SemanticError as e:
                self.errors.append(e)
        
        self.visit(node.in_body)
        node.type = node.in_body.type
        self.context = parent_contex

    @visitor.when(NewNode)
    def visit(self, node:NewNode):
        parent_contex = self.context 
        self.context = self.context.child_context()
        try:
            if node.type == "SELF_TYPE":
                node.type= self.context.current_type
            else:
                node.type = self.context.get_type(node.type,node.line)
        except SemanticError as e:
            self.errors.append(e)
            node.type = ErrorType()

        self.context = parent_contex

    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode):
        parent_contex = self.context 
        self.context = self.context.child_context()
        self.visit(node.expression)
        node.type = self.context.get_type("Bool", node.line)
        self.context = parent_contex
#Binary
#Arithmetic
    @visitor.when(ArithmeticNode)
    def visit(self, node:ArithmeticNode):
        self.visit(node.left)
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(SemanticError (f"Expr must be an integer {node.line}"))
        self.visit(node.right)
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(SemanticError (f"Expr must be an integer {node.line}"))
        node.type = self.context.get_type("Int", node.line)
        
#Comp
    @visitor.when(LessNode)
    def visit(self, node:LessNode):
        self.visit(node.left)
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(SemanticError (f"Expr must be an integer {node.line}"))
        self.visit(node.right)
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(SemanticError (f"Expr must be an integer {node.line}"))
        node.type = self.context.get_type("Bool", node.line)

    @visitor.when(LessEqualNode)
    def visit(self, node:LessEqualNode):
        self.visit(node.left)
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(SemanticError (f"Expr must be an integer {node.line}"))
        self.visit(node.right)
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(SemanticError (f"Expr must be an integer {node.line}"))
        node.type = self.context.get_type("Bool", node.line)



#Atomic
    @visitor.when(IntegerNode)
    def visit (self, node:IntegerNode):
        node.type = self.context.get_type("Int", node.line)        

    @visitor.when(StringNode)
    def visit (self, node:IntegerNode):
        node.type = self.context.get_type("String", node.line)

    @visitor.when(BoolNode)
    def visit (self, node:IntegerNode):
        node.type = self.context.get_type("Bool",node.line)

    @visitor.when(IdNode)
    def visit (self, node:IntegerNode):
        try:
            x = self.context.get_local(node.token, node.line)
            node.type = x.type
        except SemanticError as e:
            self.errors.append(e)
            node.type =  ErrorType()

