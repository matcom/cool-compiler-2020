
class Type:
    def __init__(self,className,parent="Object"):
        self.Name = className
        self.AttrList = [Attribute("self",className)]
        self.MethList = {}
        self.Default = "void"
        self.Parent = parent
        self.Children = []

    def DefineAttr(self, attr_name, attr_type):
        if ( not self.__IsDefineAttr(attr_name) == None):
            return False
        else:
            attr = Attribute(attr_name, attr_type)
            self.AttrList.append(attr)
            return True
    
    def DefineMeth(self, meth_name, params_name, params_type, return_type, rename):
        if (self.__IsDefineMeth(meth_name, params_type, return_type)):
            return False
        else:
            self.MethList[meth_name] = Method(meth_name, return_type, params_name, params_type, rename)

    def __IsDefineAttr(self, attr_name):
        attr = [ attr.Type for attr in self.AttrList if attr.Name == attrName]
        if len(attr):
            return attr[0]
        if self.Parent == None:
            return None
        return self.Parent._IsDefineAttribute(attrName)
    
    def __IsDefineAttrParent(self, attr_name):
        type = self.Parent
        if (self.Parent == None):
            return False
        return type.__IsDefineAttr(attr_name)

    def __IsDefineMeth(self, meth_name, params_type, return_type):
        for meth in self.MethList:
            if (meth.Name == meth_name and params_type == meth.ParamsType and meth.ReturnType == return_type):
                return True
        if(self.Parent == None):
            return None
        else:
            return self.Parent.__IsDefineMeth(meth_name, params_type, return_type)

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

    def GetMeth(self, meth_name, params_type, return_type):
        for meth in self.MethList.values:
            if (meth.Name == meth_name and meth.ReturnType == return_type and len(params_type) == len(meth.ParamsType)):
                for x in range(len(meth.ParamsType)):
                    if (not meth.ParamsType[x] == params_type[x]):
                        return None
                return meth
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
    def __init__(self,meth_name,  params_name, params_type,return_type, rename):
        self.Name = meth_name
        self.ReturnType = return_type
        self.ParamsName = params_name
        self.ParamsType = params_type
        self.rename = rename

class Variable:
    def __init__(self, var_name, var_type, value = None):
        self.Name = var_name
        self.Type = var_type
        self.Value = value

class Context:
    def __init__(self, parent):
        if parent is None:
            self.buildin = self.__GetBuildIn()
        # self.Hierarchy = {"Object":Type("Object",None)}
        # self.HierarchyNode = Type("Object",None)

        self.Variables = {} #nombre de la variable, su tipo
        self.Parent = parent
        self.Children = []
        self.CurrentClass = None
        self.OrderClasses = []

    '''def DefineVar(var_name, var_type, value = None):
        if (__IsDefineVar(var_name)):
            return None
        else:
            self.Variables[var_name] = Variable(var_name, var_type, value)
    
    def __IsDefineVar(var_name):
        for var in self.Variables.keys:
            if (var == var_name):
                return self.Variables[var_name]
        parent = self.Parent
        if (parent is None):
            return None
        else:
            return parent.__IsDefineVar(var_name)'''

    def __GetBuildIn(self):
        self.Hierarchy = {}
        typeObject =  Type("Object",parent = None)
        self.Hierarchy["Object"] = typeObject

        typeString =  Type("String","Object")
        # typeObject =  Type("Object",self.Hierarchy["Object"])
        typeBool =  Type("Bool","Object")
        typeInt =  Type("Int","Object")
        typeIO =  Type("IO","Object")

        typeObject.MethList["abort"] = (Method("abort",[],[],"Object",None))
        typeObject.MethList["type_name"] =(Method("type_name",[],[],"String",None))
        
        typeIO.MethList["in_string"] =(Method("in_string",[],[],"String",None))
        typeIO.MethList["in_int"] =(Method("in_int",[],[],"Int",None))
        typeIO.MethList["out_string"] = (Method("out_string", ["x"], ["String"], "IO", None))
        typeIO.MethList["out_int"] = (Method("out_int", ["x"], ["Int"], "IO", None))

        typeString.MethList["length"] =(Method("length",[],[],"Int",None))
        typeString.MethList["concat"] =(Method("concat",["s"],["String"],"String",None))
        typeString.MethList["substr"] =(Method("substr",["i","l"],["Int","Int"],"String",None))
        
        typeInt.default = 0
        typeBool.default = "false"
        typeString.default = ""

        
        self.Hierarchy["String"] = typeString
        self.Hierarchy["Bool"] = typeBool
        self.Hierarchy["Int"] = typeInt
        self.Hierarchy["IO"] = typeIO
        
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
        return self.Hierarchy.get(typeName)

    def __IsDefineType(self,typeName):
        return self.Hierarchy.__contains__(typeName)

    def DefineType(self, type_name, type_parent):
        if(self.__IsDefineType(type_name)):
            return None
        else:
            t = Type(type_name, type_parent)
            self.Hierarchy[type_name] = t
            return t
    
    def DefineVar(self, var_name, var_type, value = None):
        if (self.__IsDefineVar(var_name) is None):
            v = Variable(var_name, var_type, value)
            self.Variables[var_name] = v
        else:
            return self.Variables[var_name]
            
    def __IsDefineVar(self, var_name, var_type):
        if (var_name in self.Variables.keys):
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
        derivedparent = derived.parent
        if derivedparent == None:
            return False
        if derivedparent.name == ancestor:
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
            vtype = self.Hierarchy[self.currentClass]._IsDefineAttributeInParent(vname)
            if vtype == None:
                return None
            return vtype
        return vinfo.ctype        

    # def GetVariableType(self,variable):
    #     return self.variables[variable]

    # def IsLocalVariable(self,vname):
    #     if self.variables.__contains__(vname):
    #         return True, self.variables[vname]
    #     return False,None

    def CreateChildContext(self):
        childContext = Context(self)
        childContext.Hierarchy = self.Hierarchy
        childContext.currentClass = self.currentClass
        return childContext

    def BuildTypesHierarchy(self):
        '''
        directed graph
        '''
        graph = [[] for i in range(len(self.Hierarchy))]

        for _type in self.Hierarchy:
            u = self.Hierarchy[_type.Parent]
            v = self.Hierarchy[_type.Name]
            graph[u].append(v)
        self.inheritance_graph = graph

    def CheckMain(self):
        _type = self.GetType("Main")
        if _type is not None: # checking if there is the program has a class Main 
            method = _type.GetMeth("main") # the method main is not inherited because enviroment is None
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

   
    def IsTree(self):
        #self.build_types_graph()
        self.visited = [False]*len(self.Hierarchy.keys)
        for u in range(len(self.Hierarchy.keys)):
            if not self.visited[u]:
                if self.dfs_cycles(u):
                    #error
                    return 0
        return 1

    def dfs_cycles(self, u):
        self.visited[u] = True
        for v in self.graph[u]:
            if self.visited[v]:
                return True
            if self.dfs_cycles(v):
                return True
        return False
        