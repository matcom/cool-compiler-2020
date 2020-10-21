from AST import *
from CIL import *
from Scope import *
import visitor as visitor

class CILTranspiler:
    def __init__(self):
        self.data={}
        self.datacount=0
        self.variablecount=0
        self.labelcount=0
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
        ordenados=grafo[actual]
        nuevos=[]
        for elemento in ordenados:
            nuevos.append(elemento)
            nuevos.extend(self.OrdenarClasesPorHerenciaHelper(elemento.nombre))
        
        ordenados.extend(nuevos)
        return ordenados

    def OrdenarClasesPorHerencia(self, classes:list):
        grafo=self.GenerarGrafoDeHerencia(classes)
        ordenados=[]
        if "Object" in self.grafo.keys():
            ordenados.extend(self.OrdenarClasesPorHerenciaHelper("Object"))
        if "IO" in self.grafo.keys():
            ordenados.extend(self.OrdenarClasesPorHerenciaHelper("IO"))
        
        return ordenados
            
    
    def GenerarDiccionarioAtributos(self, classes:list):
        self.attrib={}
        for c in classes:
            misatributos={}

            if c.parent not in ["Object","IO"]:
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

            if c.parent not in ["Object","IO"]:
                for elemento in self.methods[c.parent]:
                    mismetodos[elemento.name]=elemento
                    self.globalnames[c.name+"#"+elemento.name]=self.globalnames[c.parent+"#"+elemento.name]
            
            for met in c.methods:
                if c.name+"#"+met.name in self.globalnames.keys:
                    self.globalnames[c.name+"#"+met.name]="f"+str(counter)
                    counter+=1
                    
                mismetodos[met.name]=met

            self.methods[c.name]=mismetodos.values()

        return (self.methods, self.globalnames)

    def GenerarNombreVariable():
        self.variablecount+=1
        return "var#"+str(self.variablecount)
                    



    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, _):
        classes=self.OrdenarClasesPorHerencia(node.classes)
        atributosdic=self.GenerarDiccionarioAtributos(classes)
        metodosdic,metodosglobalesdic=self.GenerarDiccionarioMetodos(classes)

        classesCIL=[]

        for c in classes:
            #Generando los Types e información de clase
            atributosAST=atributosdic[c.name]
            metodosAST=metodosdic[c.name]

            atributosCIL=[]
            for element in atributosAST:
                nuevoCIL=CILAttribute(element.name)
                atributosCIL.append(nuevoCIL)

            metodosClaseCIL=[]
            for element in metodosAST:
                nuevoCIL=CILClassMethod(element.name,metodosglobalesdic[c.name+"#"+element.name])
                metodosClaseCIL.append(nuevoCIL)
            
            claseCIL=CILClass(c.name,atributosCIL, metodosClaseCIL)
            classesCIL.append(claseCIL)

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope:Scope):
        datadeclaration=CILDataDeclaration("st"+str(self.datacount), node.value)
        self.datacount+=1
        self.data[datadeclaration.nombre]=datadeclaration

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
        parameters=[]
        locales=[]
        for param in node.parameters:
            parameters.append(param.name)
    
        instructions=[]
        for element in node.body:
            instructions.extend(self.visit(element,scope))
        
        return CILGlobalMethod(parameters,locales,instructions)

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