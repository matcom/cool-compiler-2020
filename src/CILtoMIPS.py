from AST import *
from CIL import *
from ScopeMIPS import *
import visitor as visitor

class MIPSClass:
    def __init__(self, cantidadatributos, etiquetasfunciones):
        self.cantidadatributos=cantidadatributos
        self.etiquetasfunciones=etiquetasfunciones

class MIPSCompiler:
    def __init__(self):
        self.clases=[]
        self.atributos={}
        self.metodos={}
        self.metodosglobales={}
        self.data={}
        self.locals={}
        self.registerparams={}
        self.params={}

    def load(self, node:CILInstructionNode,scope:ScopeMIPS):
        instrucciones=""
        parametro0=node.params[0]
        if parametro0 is int:
            instrucciones+="li $t0,"+str(parametro0)+"\n"
        elif parametro0 in scope.locals.keys():
            instrucciones+="lw $t0,"+scope.locals[parametro0]+"\n"
        elif parametro0 in scope.parameters.keys():
            instrucciones+="lw $t0,"+scope.parameters[parametro0]+"\n"
        elif parametro0 in scope.registerparameters.keys():
            instrucciones+="move $t0,"+scope.registerparameters[parametro0]+"\n"
        else:
            assert False

        if len(node.params<2):
            return instrucciones

        parametro1=node.params[1]

        if parametro1 is int:
            instrucciones+="li $t1,"+str(parametro1)+"\n"
        elif parametro1 in scope.locals.keys():
            instrucciones+="lw $t1,"+scope.locals[parametro1]+"\n"
        elif parametro1 in scope.parameters.keys():
            instrucciones+="lw $t1,"+scope.parameters[parametro1]+"\n"
        elif parametro1 in scope.registerparameters.keys():
            instrucciones+="move $t1,"+scope.registerparameters[parametro1]+"\n"
        else:
            assert False

        return instrucciones

    def save(self, destino:str,scope:ScopeMIPS):
        instrucciones=""
        if destino in scope.locals.keys():
            instrucciones+="sw $v0,"+scope.locals[parametro]+"\n"
        elif destino in scope.parameters.keys():
            instrucciones+="sw $v0,"+scope.parameters[parametro]+"\n"
        elif destino in scope.registerparameters.keys():
            instrucciones+="move "+scope.registerparameters[parametro]+",$t0\n"
        else:
            assert False
        return instrucciones

    def loadAndSaveAndInstructions(self,node:CILInstructionNode, instructions:str, scope:ScopeMIPS):
        return self.load(node,scope)+instructions+self.save(node.destination,scope)
    
    @visitor.on('node')
    def visit(self, node, scope:ScopeMIPS):
        pass

    @visitor.on(CILProgram)
    def visit(self, node:CILProgram, _):
        datainstructions=".data\n"
        for element in node.Data:
            datainstructions+=element.nombre+': asciiz "'+element.valorString+'"\n'
            self.data[element.nombre]=element.valorString
        
        for element in node.Types:
            self.clases.append(element.name)
            self.atributos[element.name]=element.listaAtributos
            self.metodos[element.name]=element.listaMetodos
            
            datainstructions+=element.name+"$clase: word "

            for i in range(len(element.listaMetodos)):
                if i>0:
                    datainstructions+=","
                datainstructions+=element.listaMetodos[i]

            datainstructions+="\n"

        instrucciones=""
        for element in node.Methods:
            instrucciones.append(self.visit(element))

    @visitor.on(CILGlobalMethod)
    def visit(self, node:CILGlobalMethod, _):
        instrucciones=""
        instrucciones+=node.nombre+":\n"

        scope=ScopeMIPS()
        scope.methodname=node.nombre

        localespropias={}
        for i in range(len(node.locals)):
            localespropias[node.locals[i]]=str(i*(4)+4)+"($sp)"

        scope.locals=localespropias
        
        self.locals[node.nombre]=localespropias

        misregisterparams={}
        misotrosparams={}
        for i in range(len(node.params)):
            if i<4:
                misregisterparams[node.params[i]]="$a"+str(i)
            else:
                misotrosparams[node.params[i]]=str((i-4+len(node.locals))*4)+"($sp)"

        scope.registerparameters=misregisterparams
        scope.parameters=misotrosparams
        
        self.registerparams[node.nombre]=misregisterparams
        self.params[node.nombre]=misotrosparams
            
        #Inicalizando variables locales
        instrucciones+="addi $sp, $sp, -"+str(4*len(node.locals)+4)+"\n"
        instrucciones+="sw $ra, 0($sp)\n"

        for i in range(len(node.intrucciones)):
            instrucciones+=self.visit(inst, scope)


        ultimainstruccion=node.intrucciones[len(node.intrucciones)-1]
        retorno=ultimainstruccion.destination
        
        if retorno != None:
            instrucciones+="lw $v0, 0($sp)\n"


        instrucciones+="lw $ra, 0($sp)\n"
        instrucciones+="addi $sp, $sp, "+str(4*len(node.locals)+4)+"\n"
        instrucciones+="jr $ra\n"

        return instrucciones

    @visitor.on(CILAbort)
    def visit(self, node:CILAbort, scope:ScopeMIPS):
        instrucciones="jal .Object.abort\n"
        return instrucciones

    @visitor.on(CILAssign)
    def visit(self, node:CILAssign, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+=self.load(node,scope)

        instrucciones+="move $v0, $t0\n"

        instrucciones+=self.save(node.destination,scope)

        return instrucciones

    @visitor.on(CILPlus)
    def visit(self, node:CILPlus, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+=self.load(CILPlus)

        instrucciones+="add $v0, $t0, $t1\n"

        instrucciones+=self.save(node.destination,scope)
        
        return instrucciones

    @visitor.on(CILMinus)
    def visit(self, node:CILMinus, scope:ScopeMIPS):
        instrucciones="sub $v0, $t0, $t1\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.on(CILMult)
    def visit(self, node:CILMult, scope:ScopeMIPS):
        instrucciones="mult $t0, $t1\n"
        instrucciones+="mflo $v0\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.on(CILDiv)
    def visit(self, node:CILDiv, scope:ScopeMIPS):
        instrucciones="div $t0, $t1\n"
        instrucciones+="mflo $v0\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.on(CILEqual)
    def visit(self, node:CILEqual, scope:ScopeMIPS):
        instrucciones="move s0, $a0\n"
        instrucciones+="move s1, $a1\n"
        instrucciones+="move $a0, $t0\n"
        instrucciones+="move $a1, $t1\n"
        instrucciones+="jal .Int.igual\n"
        instrucciones+="move $a0, $s0\n"
        instrucciones+="move $a1, $s1\n"
        return self.loadAndSaveAndInstructions(node, instrucciones, scope)

    @visitor.on(CILLabel)
    def visit(self, node:CILLabel, scope:ScopeMIPS):
        instrucciones=node.params[0]+"\n"
        return instrucciones

    @visitor.on(CILArgument)
    def visit(self, node:CILArgument, scope:ScopeMIPS):
        instrucciones=self.load(node,scope)
        if scope.paramcount<4:
            instrucciones+="move $a"+str(scope.paramcount)+", $t0\n"
        else:
            instrucciones+="addi $sp, $sp, -4\n"
            instrucciones+="sw $t0, 0($sp)\n"
        
        return instrucciones

    @visitor.on(CILAllocate)
    def visit(self, node:CILAllocate, scope:ScopeMIPS):
        instrucciones=""
        tipo=node.params[0]
        tamanno=(len(self.atributos[tipo])+1)*4
        instrucciones+="addi $sp, $sp, -4\n"
        instrucciones+="sw $a0, 0($sp)\n"

        instrucciones+="li $a0,"+str(tamanno)+"\n"
        instrucciones+="syscall\n"
        
        instrucciones+="la $t0, "+tipo+"$clase\n"
        instrucciones+="sw $to, 0($v0)\n"
        instrucciones+="sw $to, 4($v0)\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="addi $sp, $sp, 4\n"

        #TODO Llamar al metodo init suyo

        return instrucciones+self.save(node.destination,scope)
