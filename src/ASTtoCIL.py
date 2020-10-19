from AST import *
from CIL import *
import visitor as visitor

class CILTranspiler:
    def __init__(self):
        self.data={}
        self.datacount=0
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
                    



    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when('ProgramNode')
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
            
            claseCIL=CILClass(atributosCIL, metodosClaseCIL)

    @visitor.when('StringNode')
    def visit(self, node: StringNode, _):
        datadeclaration=CILDataDeclaration("st"+str(self.datacount), node.value)
        self.datacount+=1
        self.data[datadeclaration.nombre]=datadeclaration