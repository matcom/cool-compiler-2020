
class Type:
    def __init__(self,className,parent):
        self.Name = className
        self.AttrList = [Attribute("self",self)]
        self.MethList = {}
        self.Default = "void"
        self.Parent = parent
        self.Children = []

    def DefineAttr(self, attr_name, attr_type):
        if self.__IsDefineAttr(attr_name, self) is None:
            attr = Attribute(attr_name, attr_type)
            self.AttrList.append(attr)
            return attr
        else:
            return None
    
    def __IsDefineAttr(self, attr_name, _type):
        for attr in _type.AttrList:
            if attr.Name == attr_name:
                return attr
        return None 
        #Verificar que no hay attr con el mismo nombre en los ancestros
        # parent = _type.Parent
        # if parent is None or not isinstance(parent, Type):
        #     return None
        # else:
        #     return self.__IsDefineAttr(attr_name, parent)

    def IsDefineAttr2(self,attr_name, _type):
        for attr in _type.AttrList:
            if attr.Name == attr_name:
                return attr
        parent = _type.Parent
        if parent is None or not isinstance(parent, Type):
            return None
        else:
            return self.IsDefineAttr2(attr_name, parent)


    def DefineMeth(self, meth_name, params_name, params_type, return_type, rename, context):
        if (self.__IsDefineMeth(meth_name, params_type, return_type)):
            return None
        else:
            self.MethList[meth_name] = Method(meth_name, params_name, params_type, return_type, rename, context)
            return self.MethList[meth_name]

    
        
    
    def DefineInHierarchy(self, attr_name):
        for attr in self.AttrList:
            if attr.Name == attr_name:
                return True
        _type = self.Parent
        if (self.Parent == None):
            return False
        return _type.DefineInHierarchy(attr_name)



    def __IsDefineMeth(self, meth_name, params_type, return_type):
        for meth in self.MethList:
            if (meth == meth_name and params_type == self.MethList[meth].ParamsType and self.MethList[meth].ReturnType == return_type):
                return True

    def __IsDefineMethParent(self, meth_name, params_type, return_type):
        type = self.Parent
        if (self.Parent == None):
            return False
        else:
            return self.Parent.__IsDefineMeth(meth_name, params_type, return_type)

    def GetMethodReturnType(self, meth_name):
        if (meth_name in self.MethList.keys):
            return self.MethList[meth_name].ReturnType
        if (self.Parent is None):
            return None
        return self.Parent.GetMethodReturnType(meth_name)

    def GetAttr(self, attr_name):
        for attr in self.AttrList:
            if (attr.Name == attr_name):
                return attr
        if (self.Parent is None):
            return None
        return self.Parent.GetAttr(attr_name)

    def GetMeth(self, meth_name, params_type):
        for meth in self.MethList:
            if (self.MethList[meth].Name == meth_name and  len(params_type) == len(self.MethList[meth].ParamsType)):
                for x in range(len(self.MethList[meth].ParamsType)):
                    if (not self.MethList[meth].ParamsType[x] == params_type[x]):
                        return None
                return self.MethList[meth]
        parent = self.Parent
        if (parent is None):
            return None
        else: 
            return parent.GetMeth(meth_name, params_type, return_type)

class Attribute:
    def __init__(self, attr_name, attr_type):
        self.Name = attr_name
        self.Type = attr_type

class Method:
    def __init__(self,meth_name,  params_name, params_type,return_type, rename, context):
        self.Name = meth_name
        self.ReturnType = return_type
        self.ParamsName = params_name
        self.ParamsType = params_type
        self.rename = rename
        self.Context = context

class Variable:
    def __init__(self, var_name, var_type, value = None):
        self.Name = var_name
        self.Type = var_type
        self.Value = value

class Context:
    def __init__(self, parent):
        self.Variables = {} #nombre de la variable, su tipo
        self.Parent = parent
        self.Children = []
        self.CurrentClass = None
        
        if parent is None:
            self.buildin = self.__GetBuildIn()
        self.OrderClasses = []

    def IsDefineMeth2(self, ctype, meth_name):
        if ctype is None:
            return None
        # la clase tiene ese metodo???
        if not ctype.MethList.keys().__contains__(meth_name):
            #preguntar si el padre tiene ese meth
            parent = ctype.Parent
            return self.IsDefineMeth2(parent,meth_name)
        return ctype.MethList[meth_name]
        
    def IsDefineMeth(self,ctype, meth_name, params_type, return_type):
        if ctype is None:
            return None
        myctype = self.Hierarchy[ctype]
        # la clase tiene ese metodo???
        if not myctype.MethList.keys().__contains__(meth_name):
            #preguntar si el padre tiene ese meth
            parent = myctype.Parent
            return self.IsDefineMeth(parent,meth_name, params_type, return_type)
        meth = myctype.MethList[meth_name]
        if not (len(params_type)== len(meth.ParamsType)):
            return None 
        for i,param in enumerate(params_type):
            if not (meth.ParamsType[i] == param) and (not self.IsDerived(param,meth.ParamsType[i])):
                return None

    def __GetBuildIn(self):
        self.Hierarchy = {}
        typeObject =  Type("Object",parent = None)
        self.Hierarchy["Object"] = typeObject

        

        typeString =  Type("String",typeObject)
        # typeObject =  Type("Object",self.Hierarchy["Object"])
        typeBool =  Type("Bool",typeObject)
        typeInt =  Type("Int",typeObject)
        typeIO =  Type("IO",typeObject)

        self.Hierarchy["String"] = typeString
        self.Hierarchy["Bool"] = typeBool
        self.Hierarchy["Int"] = typeInt
        self.Hierarchy["IO"] = typeIO
        self.Hierarchy["error"] = Type("error", typeObject)

        typeObject.MethList["abort"] = (Method("abort",[],[],"Object",None,self))
        typeObject.MethList["type_name"] =(Method("type_name",[],[],"String",None, self))
        
        typeIO.MethList["in_string"] =(Method("in_string",[],[],"String",None, self))
        typeIO.MethList["in_int"] =(Method("in_int",[],[],"Int",None, self))
        child_context = self.CreateChildContext()
        child_context.DefineVar("x","String")
        typeIO.MethList["out_string"] = (Method("out_string", ["x"], ["String"], "IO", None, child_context))
        child_context = self.CreateChildContext()
        child_context.DefineVar("x", "Int")
        typeIO.MethList["out_int"] = (Method("out_int", ["x"], ["Int"], "IO", None, child_context))

        
        typeString.MethList["length"] =(Method("length",[],[],"Int",None, self))
        child_context = self.CreateChildContext()
        child_context.DefineVar("s", "String")
        typeString.MethList["concat"] =(Method("concat",["s"],["String"],"String",None, child_context))
        child_context = self.CreateChildContext()
        child_context.DefineVar("i", "Int")
        child_context.DefineVar("l", "Int")
        typeString.MethList["substr"] =(Method("substr",["i","l"],["Int","Int"],"String",None, child_context))

        
        typeInt.default = 0
        typeBool.default = "false"
        typeString.default = ""

        typeObject.MethList["type_name"].ComputedType = [self.GetType("String")]
        typeObject.MethList["abort"].ComputedType = [self.GetType("Object")]

        typeIO.MethList["out_int"].ComputedType = [self.GetType("IO")]
        typeIO.MethList["in_string"].ComputedType = [self.GetType("String")]
        typeIO.MethList["in_int"].ComputedType = [self.GetType("Int")]
        typeIO.MethList["out_string"].ComputedType = [self.GetType("IO")]

        typeString.MethList["substr"].ComputedType = [self.GetType("String")]
        typeString.MethList["length"].ComputedType = [self.GetType("Int")]
        typeString.MethList["concat"].ComputedType = [self.GetType("String")]
        
        return [typeString,typeBool,typeInt]

    def GetMethodReturnType(self, meth_name, params_type):
        myctype = self.Hierarchy[ctype]
        meth = myctype.GetMethodReturnType(methodName)
        if meth == None:
            return None
        if not (len(paramsType)== len(meth.paramsType)):
            return None 
        for i,param in enumerate(paramsType):
            if not (meth.paramsType[i] == param) and (not self.IsDerived(param,meth.paramsType[i])):
                return None
        return meth.returnType

    def GetType(self,typeName): # devuelve el objeto
        for _type in self.Hierarchy.keys():
            if _type == typeName:
                return self.Hierarchy[typeName]
        return None

    def MostDefineType(self,typeName):
        return (not self.Hierarchy.__contains__(typeName))

    def DefineType(self, type_name, type_parent):
        if self.MostDefineType(type_name):
            t = Type(type_name, type_parent)
            self.Hierarchy[type_name] = t
            return t
        else:
            return None
            
    
    def DefineVar(self, var_name, var_type, value = None):
        if (self.__IsDefineVar(var_name, var_type) is None):
            v = Variable(var_name, var_type, value)
            self.Variables[var_name] = v
            return v
        else:
            return None
            
    def __IsDefineVar(self, var_name, var_type):
        if (var_name in self.Variables.keys()):
            v = self.Variables[var_name]
            return v.Type
        return None
    

    def LinkTypes(self,errors):
        values = list(self.Hierarchy.values())
        # for item in values:
        #     print(item.name)
        # print("values1",values1)
        # a = self.Hierarchy["String"]
        # print("a",a.name)
        # values = values1.remove(a)
        # print("values",values)
        for item in values:
            # print("item.name",item.name)
            # print("item.parent",item.parent)
            if not (item.parent == None):
                # print("item.parent1",item.parent)
                parent = self.GetType(item.parent)
                # print("here",parent)
                if parent == None:
                    errors.append("(0,0) - TypeError: El tipo "+ item.parent + " no esta definido")
                    return False
                item.parent = parent
                parent.children.append(item)

        return self.IsValid(errors)
        # return True

    def IsDerived(self, derived, ancestor):
        # print("derived,ancestor",derived,ancestor)
        derivedType = self.GetType(derived)
        return self._IsDerived(derivedType,ancestor)

    def _IsDerived(self, derived, ancestor):
        # print("derived,ancestor1",derived.name,ancestor)
        derivedparent = derived.Parent
        if derivedparent == None:
            return False
        if derivedparent.Name == ancestor:
            return True
        return self._IsDerived(derivedparent,ancestor)

    def IsValid(self,errors): #revisar q no haya ciclos
        for item in self.buildin:
            if len(item.children):
                errors.append("(0,0) - SemanticError: No se puede heredar del metodo "+ item.name)
                # print("buildin con hijos "  + item.name)
                return False
        return self.NotExistCicle(errors)

    def NotExistCicle(self,errors):
        # self.order_classes = []
        self._NotExistCicle( self.Hierarchy["Object"],self.order_classes)
        # print("No Hay ciclo", len(self.order_classes) == len(self.Hierarchy))
        # print(self.order_classes)
        if len(self.order_classes) == len(self.Hierarchy):
            self.sorted = self.order_classes
            return True
        errors.append("(0,0) - SemanticError: No pueden existir ciclos en la herencia")
        return False
        # return len(self.order_classes) == len(self.Hierarchy)

    def _NotExistCicle(self, a: Type, types: list):
        # print("aciclicos",a.name)
        if a is None:
            return True
        if types.__contains__(a.name):
            return False
        types.append(a.name)

        for child in a.children:
            if not self._NotExistCicle(child, types):
                return False
        return True

    def NotIOReimplemetation(self):
        # print("------------")
        
        # print("HOLA")
        io = self.Hierarchy["IO"]
        succ = io.children 
        # print("----cosita",io.children)
        # print("----cosita2",io.children[0].MethList)
        # print("succ ", succ)
        while len(succ):
            item = succ.pop()
            # print("metodos", item.MethList.values())
            for m in item.MethList.values():
                if m.name == "in_string" or m.name == "in_int" or m.name == "out_string" or m.name == "out_int":
                    return False
            succ = succ + item.children

        # print("------------")
        return True

    def LCA(self,a: Type, b: Type):
        # Si son iguales
        if a.name == b.name:
            return a.name
        
        # Lista de los posibles ancestros
        ancestors = []
    
        # Voy subiendo hasta llegar a la raíz y guardando los nodos.name que son los ancestros de a
        while a is not None:
            ancestors.append(a.name)
            a = a.parent
    
        # Trato de encontrar un ancestro de b que sea ancestro de a, el cual será el LCA
        # b = b.parent
        while b is not None:
            if ancestors.__contains__(b.name):
                return b.name
            b = b.parent
    
        return None

    def _GetType(self, vname):
        var =  self.variables.get(vname) 
        if var == None:
            return None
        return var.ctype

    def GetVinfo(self,vname):
        # print("is def var")
        var =  self.variables.get(vname) 
        if not (var == None):
            # print("contain",vname)
            return var
        if self.parent == None:
            return None
        # print("parent")
        return self.parent.GetVinfo(vname)

    def IsDefineVariable(self,vname):
        vinfo = self.GetVinfo(vname)
        if vinfo == None:
            vtype = self.Hierarchy[self.CurrentClass]._IsDefineAttributeInParent(vname)
            if vtype == None:
                return None
            return vtype
        return vinfo.ctype        

    def CreateChildContext(self):
        childContext = Context(self)
        childContext.Hierarchy = self.Hierarchy
        childContext.CurrentClass = self.CurrentClass
        for var in self.Variables.keys():
            childContext.Variables[var] = self.Variables[var]
        return childContext

    def BuildTypesHierarchy(self):
        '''
        directed graph
        '''
        graph = {}
        for _type in self.Hierarchy:
            graph[_type] = []
        for _type in self.Hierarchy:
            if _type != "Object":
                u = self.Hierarchy[_type].Parent.Name
                v = self.Hierarchy[_type].Name
                graph[u].append(v)
        self.inheritance_graph = graph

    def CheckMain(self):
        _type = self.GetType("Main")
        if _type is not None: # checking if there is the program has a class Main 
            method = _type.GetMeth("main", []) # the method main is not inherited because enviroment is None
            if method is None: # checking if the a class Main has a method named main
                #error
                pass
            if len(method.ParamsName) > 0: # checking if the method main takes no formal parameters
                #error
                pass
            #retorno
            pass
        else:
            #error
            pass            
   
    def IsTree(self, errors):
        #self.build_types_graph()
        self.visited = {}
        for u in self.Hierarchy:
            self.visited[u] = False
        for u in self.Hierarchy:
            if not self.visited[u]:
                if self.dfs_cycles(u):
                    errors.append("SemanticError: Class " + u + ", or an ancestor of " + u + ", is involved in an inheritance cycle.")
                    return 0
        return 1

    def dfs_cycles(self, u):
        self.visited[u] = True
        for v in self.inheritance_graph[u]:
            if self.visited[v]:
                return True
            if self.dfs_cycles(v):
                return True
        return False

    def GetAttr(self, _type, lex):
        for _var in self.Variables.keys():
            if (_var == lex):
                return self.Variables[_var]
        return self.__GetAttr(_type, lex)
    

    def __GetAttr(self,_type, lex):
        for _var in _type.AttrList:
            if (_var.Name == lex):
                return _var
        parent = _type.Parent
        if parent is None:
            return None
        else:
            return self.__GetAttr(parent, lex)
            
class VariableInfo:
    def __init__(self, name, ctype = None, vmholder = 0):
        self.name = name
        self.ctype = ctype
        self.vmholder = vmholder

    def __str__(self):
        return " name: " + str(self.name) + ", tipo: "+ str(self.ctype)  + ", vmholder: " + str(self.vmholder)

class MethodInfo:
    def __init__(self, name, vmholder = 0, paramsType = [], returnType = None):
        self.name = name
        self.vmholder = vmholder
        self.paramsType = paramsType
        self.returnType = returnType

    def __str__(self):
        return " name: " + str(self.name)  + ", vmholder: " + str(self.vmholder)

class ClassInfo:
    def __init__(self, name, attr_length = 0, meth_length = 0, parent = None):
        self.name = name
        self.attr_length = attr_length
        self.meth_length = meth_length
        self.parent = parent

    def __str__(self):
        return " name: " + str(self.name)  + " parent: " + str(self.parent.cinfo.name) + ", attr_length: " + str(self.attr_length) + ", meth_length: " + str(self.meth_length)
            
            
