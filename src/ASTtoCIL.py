from AST import *
from CIL import *
from Scope import *
import visitor as visitor
from DefaultClasses import *


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
            nuevos.append(elemento)
            nuevos.extend(self.OrdenarClasesPorHerenciaHelper(elemento.nombre))
        
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

            if c.parent != None:
                for elemento in self.attrib[c.parent]:
                    misatributos[elemento.name]=elemento


            for at in c.attributes:
                misatributos[at.name]=at

            self.attrib[c.name]=misatributos.values()

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
                        self.globalnames[c.name+"#"+met.name]="$f"+str(counter)
                        counter+=1
                    else:
                        self.globalnames[c.name+"#"+elemento.name]=self.globalnames[c.parent+"#"+elemento.name]
                    
            
            for met in c.methods:
                if c.name+"#"+met.name in self.globalnames.keys:
                    self.globalnames[c.name+"#"+met.name]="$f"+str(counter)
                    counter+=1
                    
                mismetodos[met.name]=met

            self.methods[c.name]=mismetodos.values()

        return (self.methods, self.globalnames)

    def GenerarNombreVariable(self):
        self.variablecount+=1
        return "var#"+str(self.variablecount)




    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, _):        
        claseObject=Defaults.ObjectClass()
        claseIO=Defaults.IOClass()
        claseString=Defaults.StringClass()

        clasescompletas=node.classes.copy()
        clasescompletas.extend([claseObject,claseIO,claseString])

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

            #TODO Inicialización de atributos

            atributosCIL=[]
            for element in atributosAST:
                nuevoCIL=CILAttribute(element.name)
                atributosCIL.append(nuevoCIL)

            metodosClaseCIL=[]
            for element in metodosAST:
                nuevoCIL=CILClassMethod(element.name,metodosglobalesdic[c.name+"#"+element.name])
                metodosClaseCIL.append(nuevoCIL)
            
            for m in c.methods:
                globalMethod=self.visit(m, scope)
                globalMethod.name=metodosglobalesdic[c.name+"#"+m.name]
                metodosGlobalesCIL[globalMethod.name]=globalMethod

            claseCIL=CILClass(c.name,atributosCIL, metodosClaseCIL)
            classesCIL.append(claseCIL)

            return CILProgram(classesCIL,self.data.values(), metodosGlobalesCIL.values())

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope:Scope):
        nombrestring="st"+str(self.datacount)
        datadeclaration=CILDataDeclaration(nombrestring, node.value)
        self.datacount+=1
        self.data[datadeclaration.nombre]=datadeclaration
        destino=self.GenerarNombreVariable()
        return [CILStringLoad(destino, [nombrestring])]


    @visitor.when(IntegerNode)
    def visit(self, node: IntegerNode, scope:Scope):
        destino=self.GenerarNombreVariable()
        instruccion=CILAssign(destino,[node.value])
        return [instruccion]

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode, scope:Scope):
        destino=self.GenerarNombreVariable()
        instruccion=CILAssign(destino,[node.value])
        return [instruccion]

    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope:Scope):
        destino=self.GenerarNombreVariable()
        instruccion=CILAllocate(destino,[node.type])
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
        
        resultadoPredicado=predicateCode[len(predicateCode)-1]
        conditinalJump=CILConditionalJump(params=[resultadoPredicado,thenLabel.params[0]])
        saltoalfinal=CILJump(params=[finalLabel.params[0]])

        destinoinicial=self.GenerarNombreVariable()
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

        destinofinal=self.GenerarNombreVariable()
        asignacionFinal=CILAssign(destinofinal,[destinoinicial])
        instrucciones.append(asignacionFinal)
        
        return instrucciones

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope:Scope):
        parameters=["self"]
        locales=[]
        for param in node.parameters:
            parameters.append(param.name)
    
        instructions=[]
        # for element in node.body:
        instructions.extend(self.visit(node.body,scope))
        
        ultimoDestino=instructions[len(instructions)-1].destination
        
        retorno=CILReturn([ultimoDestino])
        
        return CILGlobalMethod(None,parameters,locales,instructions)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope:Scope):
        if node.variable.id not in self.attrib[scope.class_name] and node.variable.id not in scope.params and node.variable.id not in scope.locals:
            scope.locals.append(node.variable.id)

        instrucciones=self.visit(node.expression,scope)
        
        nombrevariable=self.GenerarNombreVariable()
        asignacion=CILAssign(nombrevariable,instrucciones[len(instrucciones)-1].destination)
        instrucciones.append(asignacion)

        return instrucciones

    @visitor.when(BinaryOperatorNode)
    def visit(self, node: BinaryOperatorNode, scope:Scope):
        instrucciones=self.visit(node.left,scope)
        izquierda=instrucciones[len(instrucciones)-1].destination
        instrucciones.extend(self.visit(node.right,scope))
        derecha=instrucciones[len(instrucciones)-1].destination

        nombrevariable=self.GenerarNombreVariable()
        if node is PlusNode:
            nuevoCIL=CILPlus(nombrevariable,[izquierda,derecha])
        elif node is MinusNode:
            nuevoCIL=CILMinus(nombrevariable,[izquierda,derecha])
        elif node is MultNode:
            nuevoCIL=CILMult(nombrevariable,[izquierda,derecha])
        elif node is DivNode:
            nuevoCIL=CILDiv(nombrevariable,[izquierda,derecha])
        elif node is LesserNode:
            nuevoCIL=CILLesser(nombrevariable,[izquierda,derecha])
        elif node is LesserEqualNode:
            nuevoCIL=CILLesserEqual(nombrevariable,[izquierda,derecha])
        elif node is EqualNode:
            nuevoCIL=CILEqual(nombrevariable,[izquierda,derecha])
        
        instrucciones.append(nuevoCIL)
        self.variablecount+=1

        scope.locals.append(nuevoCIL.destination)
        return instrucciones

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope:Scope):
        label=CILLabel(params=["Lbl"+str(self.labelcount)])
        self.labelcount+=1
        finalciclo=CILLabel(params=["Lbl"+str(self.labelcount)])
        self.labelcount+=1

        instructions=[label]
        instructions.extend(self.visit(node.predicate,scope))
        
        negado=self.GenerarNombreVariable()
        instructions.append(CILNot(negado,[instructions[len(instructions)-1]]))

        instructions.append(CILConditionalJump(params=[negado,finalciclo.params[0]]))

        instructions.extend(self.visit(node.body,scope))

        instructions.append(CILJump(params=[label.params[0]]))
        
        instructions.append(finalciclo)

        return instructions

    @visitor.when(DispatchNode)
    def visit(self, node:DispatchNode, scope:Scope):
        instructions=[]
        leftInstructions=self.visit(node.left_expression, scope)
        instructions.extend(leftInstructions)

        instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))

        for p in node.parameters:
            paramInstruction=self.visit(p, scope)
            paramInstruction.append(CILArgument(params=[paramInstruction[len(paramInstruction)-1].destination]))
            instructions.extend(paramInstruction)

        instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))
        resultVariable=self.GenerarNombreVariable()
        llamada=CILVirtualCall(resultVariable,[node.func_id])
        instructions.append(llamada)

        return instructions

    @visitor.when(StaticDispatchNode)
    def visit(self, node:StaticDispatchNode, scope:Scope):
        instructions=[]

        leftInstructions=self.visit(node.left_expression, scope)
        instructions.extend(leftInstructions)

        instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))

        for p in node.parameters:
            paramInstruction=self.visit(p, scope)
            paramInstruction.append(CILArgument(params=[paramInstruction[len(paramInstruction)-1].destination]))
            instructions.extend(paramInstruction)        

        instructions.append(CILArgument(params=[leftInstructions[len(leftInstructions)-1].destination]))
        resultVariable=self.GenerarNombreVariable()
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
        
        bodyExp=self.visit(node.body,scope)

        instructions.extend(bodyExp)

        return instructions

    @visitor.when(CaseNode)
    def visit(self, node:CaseNode, scope:Scope):
        instructions=[]
        expresion0=self.visit(node.expression, scope)
        instructions.extend(expresion0)

        destinoExpresion0=expresion0[len(expresion0)-1].destination

        resultado1=self.GenerarNombreVariable()
        saltofinal=self.GenerarNombreVariable()
        self.caseResultStack.append(resultado1)
        self.caseExpresionStack.append(destinoExpresion0)
        self.caseEndStack.append(saltofinal)

        for sub in node.subcases:
            nueva=self.GenerarNombreVariable()
            subInstructions=self.visit(sub, case)
            instructions.extend(subInstructions)

        self.caseResultStack.pop(-1)
        self.caseExpresionStack.pop(-1)
        self.caseEndStack.append(saltofinal)

        instructions.append(CILLabel([saltofinal]))
        
        resultadofinal=self.GenerarNombreVariable()
        instructions.append(CILAssign(resultadofinal,[resultado1]))

        return instructions


    @visitor.when(SubCaseNode)
    def visit(self, node:SubCaseNode, scope:Scope):
        instructions=[]
        # prevName=scope.class_name
        # scope.class_name=node.type

        expresion0=self.caseExpresionStack.pop(-1)
        self.caseExpresionStack.append(expresion0)

        tipoResult=self.GenerarNombreVariable()
        chequeo=CILTypeCheck(tipoResult,[expresion0, node.type])
        instructions.append(chequeo)

        labelfinal=self.GenerarNombreVariable()
        salto=CILConditionalJump([tipoResult,labelfinal])
        instructions.append(salto)

        asignacion=CILAssign(node.name, [expresion0])
        instructions.append(asignacion)

        instructions.extend(self.visit(node.expression,scope))

        resultVariable=self.GenerarNombreVariable()
        asignacion=CILAssign(resultVariable,[instructions[len(instructions)-1].destination])

        resultHolder=self.caseResultStack.pop(-1)
        self.caseResultStack.append(resultHolder)
        final=CILAssign(resultHolder,[resultVariable])

        instructions.extend([asignacion,final])

        saltofinal=self.caseEndStack.pop(-1)
        self.caseEndStack.append(saltofinal)
        CILJump([saltofinal])

        # scope.class_name=prevName

        instructions.append(CILLabel([labelfinal]))
        
        return instructions
    
    @visitor.when(AttributeNode)
    def visit(self, node:AttributeNode, scope:Scope):
        instructions=[]
        instructions.extend(self.visit(node.value, scope))
        
        final=CILAssign(node.name,[instructions[len(instructions)-1].destination])
        instructions.append(final)

        return instructions