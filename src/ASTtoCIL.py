from src.AST import *
from src.CIL import *
from src.Scope import *
import src.visitor as visitor
from src.DefaultClasses import *


class CILTranspiler:
    def __init__(self):
        self.data={}
        self.datacount=0
        self.variablecount=0
        self.labelcount=0
        self.classidcount=10
        self.caseResultStack=[]
        self.caseEndStack=[]
        self.caseExpresionStack=[]
    def GenerarGrafoDeHerencia(self,classes:list):
        grafo={}
        for c in classes:
            if c.parent in grafo.keys():
                grafo[c.parent].append(c)
            else:
                grafo[c.parent]=[c]
        self.grafo=grafo
        return grafo

    def OrdenarClasesPorHerenciaHelper(self, actual):
        grafo=self.grafo
        if actual not in self.grafo.keys():
            return []
        ordenados=grafo[actual].copy()
        nuevos=[]
        for elemento in ordenados:
            # nuevos.append(elemento)
            nuevos.extend(self.OrdenarClasesPorHerenciaHelper(elemento.name))
        
        ordenados.extend(nuevos)
        return ordenados

    def OrdenarClasesPorHerencia(self, classes:list):
        grafo=self.GenerarGrafoDeHerencia(classes)
        ordenados=[]
        ordenados.extend(self.OrdenarClasesPorHerenciaHelper(None))
        # if "Object" in self.grafo.keys():
        #     ordenados.extend(self.OrdenarClasesPorHerenciaHelper("Object"))
        # if "IO" in self.grafo.keys():
        #     ordenados.extend(self.OrdenarClasesPorHerenciaHelper("IO"))
        
        return ordenados
            
    
    def GenerarDiccionarioAtributos(self, classes:list):
        self.attrib={}
        for c in classes:
            misatributos={}
            atributosordenadosname=[]

            if c.parent != None:
                for elemento in self.attrib[c.parent]:
                    misatributos[elemento.name]=elemento
                    atributosordenadosname.append(elemento.name)


            for at in c.attributes:
                if not (at.name in misatributos.keys()):
                    atributosordenadosname.append(at.name)
                misatributos[at.name]=at
            
            listaAtributos=[]
            for name in atributosordenadosname:
                listaAtributos.append(misatributos[name])

            self.attrib[c.name]=listaAtributos

        return self.attrib

    def GenerarDiccionarioMetodos(self, classes:list):
        self.methods={}
        self.globalnames={}
        counter=0
        for c in classes:
            mismetodos={}

            if c.parent != None:
                for elemento in self.methods[c.parent]:
                    mismetodos[elemento.name]=elemento
                    if elemento.name == '$init' or elemento.name == 'type_name':
                        self.globalnames[c.name+"#"+elemento.name]="f"+str(counter)
                        counter+=1
                    else:
                        self.globalnames[c.name+"#"+elemento.name]=self.globalnames[c.parent+"#"+elemento.name]

            else:
                mismetodos["$init"]=MethodNode("$init",[],None,[])
                mismetodos["type_name"]=MethodNode("$init",[],None,[])
                self.globalnames[c.name+"#"+"$init"]="f"+str(counter)
                counter+=1
                self.globalnames[c.name+"#"+"type_name"]="f"+str(counter)
                counter+=1
            
            for met in c.methods:
                # if c.name+"#"+met.name in self.globalnames.keys():
                self.globalnames[c.name+"#"+met.name]="f"+str(counter)
                counter+=1
                    
                mismetodos[met.name]=met

            self.methods[c.name]=mismetodos.values()

        return (self.methods, self.globalnames)

    def GenerarNombreVariableBase(self):
        self.variablecount+=1
        return "var.var"+str(self.variablecount)

    def GenerarNombreVariable(self, scope:Scope):
        variable=self.GenerarNombreVariableBase()
        scope.locals.append(variable)
        return variable

    def GenerarInit(self, clase:ClassNode, scope:Scope):
        instructions=[]
        if clase.parent!=None:
            dumb=self.GenerarNombreVariable(scope)
            instructions.append(CILArgument(params=["self"]))
            instructions.append(CILVirtualCall(dumb,[clase.parent,"$init"]))
        
        for a in clase.attributes:
            inits=self.visit(a,scope)
            instructions.extend(inits)

        final=self.GenerarNombreVariable(scope)

        result=CILAssign(final,['self'])

        instructions.append(result)
        
        return instructions

    def CILMainInstructions(self):
        nuevo=NewNode("Main")
        instruction=DispatchNode("main",[],nuevo,"Main")
        scope=Scope("Main.special","Object")
        result=self.visit(MethodNode("main",[],"SELF_TYPE",instruction),scope)
        return result



    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, _):        
        claseObject=Defaults.ObjectClass()
        claseIO=Defaults.IOClass()
        claseString=Defaults.StringClass()
        claseBool=Defaults.BoolClass()

        clasescompletas=node.classes.copy()
        clasescompletas.extend([claseObject,claseIO,claseString,claseBool])

        classes=self.OrdenarClasesPorHerencia(clasescompletas)
        atributosdic=self.GenerarDiccionarioAtributos(classes)
        metodosdic,metodosglobalesdic=self.GenerarDiccionarioMetodos(classes)

        classesCIL=[]
        metodosGlobalesCIL={}

        for c in classes:
            #Generando los Types e información de clase
            atributosAST=atributosdic[c.name]
            metodosAST=metodosdic[c.name]
            self.classidcount+=1

            scope=Scope(c.name, c.parent)
            scope.attributes=atributosAST
            scope.class_name=c.name

            main=self.CILMainInstructions()
            main.nombre="Main.Special"
            metodosGlobalesCIL[main.nombre]=main

            #Inicialización de atributos
            initInstructions=self.GenerarInit(c,scope)
            initName=metodosglobalesdic[c.name+"#"+"$init"]
            globalInit=CILGlobalMethod(initName,["self"],scope.locals,initInstructions, c.name)
            metodosGlobalesCIL[globalInit.nombre]=globalInit

            #Metodo type_name
            metodotypename=MethodNode("type_name",[],"String",StringNode('"'+c.name+'"'))
            nombreTypeName=metodosglobalesdic[c.name+"#"+"type_name"]
            metodoglobal=self.visit(metodotypename, scope)
            metodoglobal.nombre=nombreTypeName
            metodosGlobalesCIL[nombreTypeName]=metodoglobal
            

            atributosCIL=[]
            for element in atributosAST:
                nuevoCIL=CILAttribute(element.name, element.type)
                atributosCIL.append(nuevoCIL)

            metodosClaseCIL=[]
            for element in metodosAST:
                nuevoCIL=CILClassMethod(element.name,metodosglobalesdic[c.name+"#"+element.name])
                metodosClaseCIL.append(nuevoCIL)
            
            if not (c.name in ["Object", "IO", "String"]):
                for m in c.methods:
                    globalMethod=self.visit(m, scope)
                    globalMethod.nombre=metodosglobalesdic[c.name+"#"+m.name]
                    metodosGlobalesCIL[globalMethod.nombre]=globalMethod

            elif c.name == "Object":
                #copy
                globalMethod=Defaults.copy_CIL(len(c.attributes))
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

                #abort
                globalMethod=Defaults.abort_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

            elif c.name == "IO":
                #out_string
                globalMethod=Defaults.out_string_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

                #out_int
                globalMethod=Defaults.out_int_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

                #in_string
                globalMethod=Defaults.in_string_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

                #in_int
                globalMethod=Defaults.in_int_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

            elif c.name == "String":
                #length
                globalMethod=Defaults.len_string_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

                #concat
                globalMethod=Defaults.concat_string_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

                #substring
                globalMethod=Defaults.substring_string_CIL()
                globalMethod.nombre=metodosglobalesdic[c.name+"#"+globalMethod.nombre]
                metodosGlobalesCIL[globalMethod.nombre]=globalMethod

            claseCIL=CILClass(c.name,atributosCIL, metodosClaseCIL, c.parent)
            classesCIL.append(claseCIL)

        return CILProgram(classesCIL,self.data.values(), metodosGlobalesCIL.values())

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope:Scope):
        nombrestring="st"+str(self.datacount)
        datadeclaration=CILDataDeclaration(nombrestring, node.value)
        self.datacount+=1
        self.data[datadeclaration.nombre]=datadeclaration
        destino=self.GenerarNombreVariable(scope)
        scope.locals.append(destino)
        return [CILStringLoad(destino, [nombrestring])]


    @visitor.when(IntegerNode)
    def visit(self, node: IntegerNode, scope:Scope):
        destino=self.GenerarNombreVariable(scope)
        instruccion=CILAssign(destino,[node.value])
        return [instruccion]

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode, scope:Scope):
        destino=self.GenerarNombreVariable(scope)
        instruccion=CILAssign(destino,[node.value])
        return [instruccion]

    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope:Scope):
        destino=self.GenerarNombreVariable(scope)
        instruccion=CILAllocate(destino,[node.type])
        if not node.type in ['Int','Bool']:
            argument=CILArgument(params=[destino])
            init=CILCall(destino,[node.type,"$init"])
            return [instruccion, argument,init]
        else:
            return [instruccion]

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope:Scope):
        instrucciones=[]
        for e in node.expressions:
            instrucciones.extend(self.visit(e,scope))
        
        return instrucciones

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope:Scope):
        predicateCode=self.visit(node.predicate,scope)
        thencode=self.visit(node.then_body,scope)
        elsecode=self.visit(node.else_body,scope)

        thenLabel=CILLabel(params=["Lbl"+str(self.labelcount)])
        self.labelcount+=1
        finalLabel=CILLabel(params=["Lbl"+str(self.labelcount)])
        self.labelcount+=1
        
        resultadoPredicado=predicateCode[len(predicateCode)-1].destination
        conditinalJump=CILConditionalJump(params=[resultadoPredicado,thenLabel.params[0]])
        saltoalfinal=CILJump(params=[finalLabel.params[0]])

        destinoinicial=self.GenerarNombreVariable(scope)
        asignacionThen=CILAssign(destinoinicial,[thencode[len(thencode)-1].destination])
        thencode.append(asignacionThen)
        asignacionElse=CILAssign(destinoinicial,[elsecode[len(elsecode)-1].destination])
        elsecode.append(asignacionElse)

        instrucciones=predicateCode
        instrucciones.append(conditinalJump)
        instrucciones.extend(elsecode)
        instrucciones.append(saltoalfinal)
        instrucciones.append(thenLabel)
        instrucciones.extend(thencode)
        instrucciones.append(finalLabel)

        destinofinal=self.GenerarNombreVariable(scope)
        asignacionFinal=CILAssign(destinofinal,[destinoinicial])
        instrucciones.append(asignacionFinal)
        
        return instrucciones

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope:Scope):
        parameters=["self"]
        locales=[]
        scope.locals=locales
        for param in node.parameters:
            parameters.append(param.name)

        scope.params=parameters
    
        instructions=[]
        # for element in node.body:
        instructions.extend(self.visit(node.body,scope))
        locales=scope.locals
        
        # retorno=CILReturn([])
        # if len(instructions)>0:
        #     ultimoDestino=instructions[len(instructions)-1].destination
        #     retorno=CILReturn([ultimoDestino])
        
        return CILGlobalMethod(None,parameters,locales,instructions, scope.class_name)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope:Scope):
        if node.variable not in self.attrib[scope.class_name] and node.variable not in scope.params and node.variable not in scope.locals:
            scope.locals.append(node.variable)

        instrucciones=self.visit(node.expression,scope)
        
        nombrevariable=node.variable#self.GenerarNombreVariable(scope)
        asignacion=CILAssign(nombrevariable,[instrucciones[len(instrucciones)-1].destination])
        instrucciones.append(asignacion)

        return instrucciones

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope:Scope):
        instrucciones=[]
        nombrevariable=self.GenerarNombreVariable(scope)
        asignacion=CILAssign(nombrevariable,[node.id])
        instrucciones.append(asignacion)

        return instrucciones

    @visitor.when(BinaryOperatorNode)
    def visit(self, node: BinaryOperatorNode, scope:Scope):
        instrucciones=self.visit(node.left,scope)
        izquierda=instrucciones[len(instrucciones)-1].destination
        instrucciones.extend(self.visit(node.right,scope))
        derecha=instrucciones[len(instrucciones)-1].destination

        nombrevariable=self.GenerarNombreVariable(scope)
        if isinstance(node, PlusNode):
            nuevoCIL=CILPlus(nombrevariable,[izquierda,derecha])
        elif isinstance(node, MinusNode):
            nuevoCIL=CILMinus(nombrevariable,[izquierda,derecha])
        elif isinstance(node, MultNode):
            nuevoCIL=CILMult(nombrevariable,[izquierda,derecha])
        elif isinstance(node, DivNode):
            nuevoCIL=CILDiv(nombrevariable,[izquierda,derecha])
        elif isinstance(node, LesserNode):
            nuevoCIL=CILLesser(nombrevariable,[izquierda,derecha])
        elif isinstance(node, LesserEqualNode):
            nuevoCIL=CILLesserEqual(nombrevariable,[izquierda,derecha])
        elif isinstance(node, EqualNode):
            if node.isString:
                nuevoCIL=CILStringEqual(nombrevariable,[izquierda,derecha])
            else:
                nuevoCIL=CILEqual(nombrevariable,[izquierda,derecha])
        
        instrucciones.append(nuevoCIL)
        self.variablecount+=1

        scope.locals.append(nuevoCIL.destination)
        return instrucciones

    @visitor.when(UnaryOperatorNode)
    def visit(self, node: UnaryOperatorNode, scope:Scope):
        instrucciones=[]
        if isinstance(node, IsVoidNode):
            instrucciones.extend(self.visit(node.expression, scope))
        else:
            instrucciones.extend(self.visit(node.right, scope))
        
        destinoExpresion=instrucciones[len(instrucciones)-1].destination

        nombrevariable=self.GenerarNombreVariable(scope)
        scope.locals.append(nombrevariable)
        nuevoCIL=CILInstructionNode()
        if isinstance(node, IsVoidNode):
            if node.tipo in ["Bool","Int","String"]:
                nuevoCIL=CILAssign(nombrevariable, 0)
            else:
                nuevoCIL=CILIsVoid(nombrevariable, [destinoExpresion])
        elif isinstance(node, IntComplementNode):
            nuevoCIL=CILIntComplement(nombrevariable, [destinoExpresion])
        elif isinstance(node, BoolComplementNode):
            nuevoCIL=CILComplement(nombrevariable, [destinoExpresion])
        else:
            assert False

        instrucciones.append(nuevoCIL)
        return instrucciones
        


    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope:Scope):
        label=CILLabel(params=["Lbl"+str(self.labelcount)])
        self.labelcount+=1
        finalciclo=CILLabel(params=["Lbl"+str(self.labelcount)])
        self.labelcount+=1

        instructions=[label]
        instructions.extend(self.visit(node.predicate,scope))
        
        negado=self.GenerarNombreVariable(scope)
        scope.locals.append(negado)
        instructions.append(CILComplement(negado,[instructions[len(instructions)-1].destination]))

        instructions.append(CILConditionalJump(params=[negado,finalciclo.params[0]]))

        instructions.extend(self.visit(node.body,scope))

        instructions.append(CILJump(params=[label.params[0]]))
        
        instructions.append(finalciclo)

        resultado=self.GenerarNombreVariable(scope)
        scope.locals.append(resultado)
        instructions.append(CILAssign(resultado,[0]))

        return instructions


    ##TODO Agregarle a Dispatch unos modos que faltaron
    @visitor.when(DispatchNode)
    def visit(self, node:DispatchNode, scope:Scope):
        instructions=[]
        if node.left_expression==None:
            node.left_expression=VariableNode("self")
            node.left_type=scope.class_name

        leftInstructions=self.visit(node.left_expression, scope)
        instructions.extend(leftInstructions)

        virtual=node.left_type in ["Int", "Bool", "String"] 

        if virtual: #Caso de los tipos básicos
            if node.func_id=="type_name":
                elstring=StringNode('"'+node.left_type+'"')
                instructions.extend(self.visit(elstring, scope))
                return instructions
                

        # instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))

        destinos=[]
        for p in node.parameters:
            paramInstruction=self.visit(p, scope)
            destinos.append(paramInstruction[len(paramInstruction)-1].destination)
            # paramInstruction.append(CILArgument(params=[paramInstruction[len(paramInstruction)-1].destination]))
            instructions.extend(paramInstruction)

        instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))
        
        for dest in destinos:
            instructions.append(CILArgument(params=[dest]))

        # instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))#Removido de los params: node.left_type,
        resultVariable=self.GenerarNombreVariable(scope)
        if(node.left_type==None):
            print()
        if virtual:
            llamada=CILVirtualCall(resultVariable,[node.left_type,node.func_id])
        else:
            llamada=CILCall(resultVariable,[node.left_type,node.func_id])
        instructions.append(llamada)

        return instructions

    @visitor.when(StaticDispatchNode)
    def visit(self, node:StaticDispatchNode, scope:Scope):
        instructions=[]

        leftInstructions=self.visit(node.left_expression, scope)
        instructions.extend(leftInstructions)

        # instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))

        destinos=[]
        for p in node.parameters:
            paramInstruction=self.visit(p, scope)
            destinos.append(paramInstruction[len(paramInstruction)-1].destination)
            # paramInstruction.append(CILArgument(params=[paramInstruction[len(paramInstruction)-1].destination]))
            instructions.extend(paramInstruction)   

        instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))

        for dest in destinos:
            instructions.append(CILArgument(params=[dest]))     

        # instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))
        resultVariable=self.GenerarNombreVariable(scope)
        llamada=CILVirtualCall(resultVariable,[node.parent_id,node.func_id])
        instructions.append(llamada)

        return instructions

    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        instructions=[]
        for at in node.declarations:
            if at.name not in scope.locals:
                scope.locals.append(at.name)
            delcaracionExp=self.visit(at.value,scope)
            instructions.extend(delcaracionExp)
            if len(delcaracionExp)>0:
                instructions.append(CILAssign(at.name,[delcaracionExp[len(delcaracionExp)-1].destination]))
            else:
                instructions.append(CILAssign(at.name,[0]))
        
        bodyExp=self.visit(node.body,scope)

        instructions.extend(bodyExp)

        return instructions

    @visitor.when(CaseNode)
    def visit(self, node:CaseNode, scope:Scope):
        instructions=[]
        expresion0=self.visit(node.expression, scope)
        instructions.extend(expresion0)

        destinoExpresion0=expresion0[len(expresion0)-1].destination

        resultado1=self.GenerarNombreVariable(scope)
        saltofinal=self.GenerarNombreVariable(scope)
        self.caseResultStack.append(resultado1)
        self.caseExpresionStack.append(destinoExpresion0)
        self.caseEndStack.append(saltofinal)

        for sub in node.subcases:
            nueva=self.GenerarNombreVariable(scope)
            subInstructions=self.visit(sub, scope)
            instructions.extend(subInstructions)

        self.caseResultStack.pop(-1)
        self.caseExpresionStack.pop(-1)
        self.caseEndStack.append(saltofinal)

        instructions.append(CILLabel(params=[saltofinal]))
        
        resultadofinal=self.GenerarNombreVariable(scope)
        instructions.append(CILAssign(resultadofinal,[resultado1]))

        return instructions


    @visitor.when(SubCaseNode)
    def visit(self, node:SubCaseNode, scope:Scope):
        instructions=[]
        # prevName=scope.class_name
        # scope.class_name=node.type

        expresion0=self.caseExpresionStack.pop(-1)
        self.caseExpresionStack.append(expresion0)

        if not node.name in scope.locals:
            scope.locals.append(node.name)

        tipoResult=self.GenerarNombreVariable(scope)
        chequeo=CILTypeCheck(tipoResult,[expresion0, node.type])
        instructions.append(chequeo)

        labelfinal=self.GenerarNombreVariable(scope)
        salto=CILConditionalJump(params=[tipoResult,labelfinal])
        instructions.append(salto)

        asignacion=CILAssign(node.name, [expresion0])
        instructions.append(asignacion)

        instructions.extend(self.visit(node.expression,scope))

        resultVariable=self.GenerarNombreVariable(scope)
        asignacion=CILAssign(resultVariable,[instructions[len(instructions)-1].destination])

        resultHolder=self.caseResultStack.pop(-1)
        self.caseResultStack.append(resultHolder)
        final=CILAssign(resultHolder,[resultVariable])

        instructions.extend([asignacion,final])

        saltofinal=self.caseEndStack.pop(-1)
        self.caseEndStack.append(saltofinal)
        CILJump([saltofinal])

        # scope.class_name=prevName

        instructions.append(CILLabel(params=[labelfinal]))
        
        return instructions
    
    @visitor.when(AttributeNode)
    def visit(self, node:AttributeNode, scope:Scope):
        instructions=[]
        instructions.extend(self.visit(node.value, scope))
        if len(instructions)>0:
            final=CILAssign(node.name,[instructions[len(instructions)-1].destination])
        else:
            final=CILAssign(node.name,[0])
        instructions.append(final)

        return instructions