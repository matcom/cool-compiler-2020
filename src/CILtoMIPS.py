from src.AST import *
from src.CIL import *
from src.ScopeMIPS import *
import src.visitor as visitor

# class MIPSClass:
#     def __init__(self, cantidadatributos, etiquetasfunciones):
#         self.cantidadatributos=cantidadatributos
#         self.etiquetasfunciones=etiquetasfunciones

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
        atributos=self.atributos[scope.methodclass]
        DicNombreAtributos={}
        nombresAtributos=[]
        for at in atributos:
            nombresAtributos.append(at.name)
            DicNombreAtributos[at.name]=at.attributeType

        if parametro0 is int:
            instrucciones+="li $t0,"+str(parametro0)+"\n"
        elif parametro0 in scope.locals.keys():
            instrucciones+="lw $t0,"+scope.locals[parametro0]+"\n"
        elif parametro0 in scope.parameters.keys():
            instrucciones+="lw $t0,"+scope.parameters[parametro0]+"\n"
        elif parametro0 in scope.registerparameters.keys():
            instrucciones+="move $t0,"+scope.registerparameters[parametro0]+"\n"
        elif parametro0 in nombresAtributos:
            instrucciones+="lw $t0,"+str(nombresAtributos.index(parametro0)*4+4)+"($a0)\n"
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
        elif parametro1 in nombresAtributos:           
            instrucciones+="lw $t1,"+str(nombresAtributos.index(parametro1)*4+4)+"($a0)\n"
        else:
            assert False

        return instrucciones

    def save(self, destino:str,scope:ScopeMIPS):
        instrucciones=""
        nombresAtributos=[]
        for at in atributos:
            nombresAtributos.append(at.name)

        if destino in scope.locals.keys():
            instrucciones+="sw $v0,"+scope.locals[parametro]+"\n"
        elif destino in scope.parameters.keys():
            instrucciones+="sw $v0,"+scope.parameters[parametro]+"\n"
        elif destino in scope.registerparameters.keys():
            instrucciones+="move "+scope.registerparameters[parametro]+",$t0\n"
        elif destino in nombresAtributos:
            instrucciones+="sw $v0,"+str(nombresAtributos.index(destino)*4+4)+"($a0)\n"
        else:
            assert False
        return instrucciones

    def loadAndSaveAndInstructions(self,node:CILInstructionNode, instructions:str, scope:ScopeMIPS):
        return self.load(node,scope)+instructions+self.save(node.destination,scope)
    
    @visitor.on('node')
    def visit(self, node, scope:ScopeMIPS):
        pass

    @visitor.when(CILProgram)
    def visit(self, node:CILProgram, _):
        datainstructions=".data\n"
        for element in node.Data:
            datainstructions+=element.nombre+': asciiz "'+element.valorString+'"\n'
            self.data[element.nombre]=element.valorString

        scope=ScopeMIPS()
        
        for element in node.Types:
            self.clases.append(element.name)
            self.atributos[element.name]=element.listaAtributos
            self.metodos[element.name]=element.listaMetodos
            metodosnombre=[]
            for met in element.listaMetodos:
                metodosnombre.append(met.localname)
            
            scope.classmethods[element.name]=metodosnombre
            
            datainstructions+=element.name+"$clase: word "

            for i in range(len(element.listaMetodos)):
                if i>0:
                    datainstructions+=","
                datainstructions+=element.listaMetodos[i].globalname
                self.metodosglobales[element.name+"#"+element.listaMetodos[i].localname]=element.listaMetodos[i].globalname

            datainstructions+="\n"

        instrucciones=""
        for element in node.Methods:
            instrucciones.append(self.visit(element, scope))

    @visitor.when(CILGlobalMethod)
    def visit(self, node:CILGlobalMethod, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+=node.nombre+":\n"

        scope.methodname=node.nombre
        scope.methodclass=node.originclass

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

    @visitor.when(CILAbort)
    def visit(self, node:CILAbort, scope:ScopeMIPS):
        instrucciones="jal .Object.abort\n"
        return instrucciones

    @visitor.when(CILAssign)
    def visit(self, node:CILAssign, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+=self.load(node,scope)

        instrucciones+="move $v0, $t0\n"

        instrucciones+=self.save(node.destination,scope)

        return instrucciones

    @visitor.when(CILPlus)
    def visit(self, node:CILPlus, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+=self.load(CILPlus)

        instrucciones+="add $v0, $t0, $t1\n"

        instrucciones+=self.save(node.destination,scope)
        
        return instrucciones

    @visitor.when(CILMinus)
    def visit(self, node:CILMinus, scope:ScopeMIPS):
        instrucciones="sub $v0, $t0, $t1\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILMult)
    def visit(self, node:CILMult, scope:ScopeMIPS):
        instrucciones="mult $t0, $t1\n"
        instrucciones+="mflo $v0\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILDiv)
    def visit(self, node:CILDiv, scope:ScopeMIPS):
        instrucciones="div $t0, $t1\n"
        instrucciones+="mflo $v0\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILEqual)
    def visit(self, node:CILEqual, scope:ScopeMIPS):
        instrucciones="move s0, $a0\n"
        instrucciones+="move s1, $a1\n"
        instrucciones+="move $a0, $t0\n"
        instrucciones+="move $a1, $t1\n"
        instrucciones+="jal .Int.igual\n"
        instrucciones+="move $a0, $s0\n"
        instrucciones+="move $a1, $s1\n"
        return self.loadAndSaveAndInstructions(node, instrucciones, scope)

    @visitor.when(CILLabel)
    def visit(self, node:CILLabel, scope:ScopeMIPS):
        instrucciones=node.params[0]+"\n"
        return instrucciones

    @visitor.when(CILArgument)
    def visit(self, node:CILArgument, scope:ScopeMIPS):
        instrucciones=self.load(node,scope)
        if scope.paramcount<4:
            instrucciones+="move $a"+str(scope.paramcount)+", $t0\n"
        else:
            instrucciones+="addi $sp, $sp, -4\n"
            instrucciones+="sw $t0, 0($sp)\n"
        
        return instrucciones

    @visitor.when(CILAllocate)
    def visit(self, node:CILAllocate, scope:ScopeMIPS):
        instrucciones=""
        tipo=node.params[0]
        tamanno=(len(self.atributos[tipo])+1)*4
        instrucciones+="addi $sp, $sp, -4\n"
        instrucciones+="sw $a0, 0($sp)\n"

        instrucciones+="li $a0,"+str(tamanno)+"\n"
        instrucciones+="syscall\n"
        
        instrucciones+="la $t0, "+tipo+"$clase\n"
        instrucciones+="sw $t0, 0($v0)\n"

        #Poniendo en 0 todos los elementos
        for i in range(len(self.atributos[tipo])):
            instrucciones+="sw zero, "+str(i*4+4)+"($v0)\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="addi $sp, $sp, 4\n"

        #TODO Llamar al metodo init suyo

        return instrucciones+self.save(node.destination,scope)

    @visitor.when(CILVirtualCall)
    def visit(self, node:CILVirtualCall, scope:ScopeMIPS):
        tipo=node.params[0]
        func_id=node.params[1]
        instrucciones=""
        instrucciones+="la $t0,"+tipo+"$clase\n"
        instrucciones+="lw $t0,"+str(scope.classmethods[tipo].index(func_id)*4)+"($t0)\n"
        instrucciones+="addi $sp, $sp, -4\n"
        instrucciones+="sw $ra, 0($sp)\n"
        instrucciones+="jal $t0\n"
        instrucciones+="lw $ra, 0($sp)\n"
        
        for i in range(scope.paramcount):
            if scope.paramcount-1-i<4:
                instrucciones+="lw $a"+str(scope.paramcount-1-i)+", "+str(i*4+4)+"($sp)\n"

        instrucciones+="addi $sp, $sp, "+str(scope.paramcount*4+4)+"\n"
        instrucciones+=self.save(node.destination,scope)

        scope.paramcount=0
        
        return instrucciones

    @visitor.when(CILCall)
    def visit(self, node:CILCall, scope:ScopeMIPS):
        tipo=node.params[0]
        func_id=node.params[1]
        instrucciones="lw $t0, $a0"
        instrucciones+="lw $t0,"+str(scope.classmethods[tipo].index(func_id)*4)+"($t0)\n"
        instrucciones+="addi $sp, $sp, -4\n"
        instrucciones+="sw $ra, 0($sp)\n"
        instrucciones+="jal $t0\n"
        instrucciones+="lw $ra, 0($sp)\n"

        for i in range(scope.paramcount):
            if scope.paramcount-1-i<4:
                instrucciones+="lw $a"+str(scope.paramcount-1-i)+", "+str(i*4+4)+"($sp)\n"

        instrucciones+="addi $sp, $sp, "+str(scope.paramcount*4+4)+"\n"
        instrucciones+=self.save(node.destination,scope)

        scope.paramcount=0
        
        return instrucciones

    @visitor.when(CILArgument)
    def visit(self, node:CILArgument, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+=self.load(CILArgument,scope)
        instrucciones+="addi $sp, $sp, -4\n"
        if scope.paramcount<4:
            instrucciones+="sw $a"+str(scope.paramcount)+", 0($sp)\n"
            instrucciones+="move $a"+str(scope.paramcount)+",$t0"
        else:
            instrucciones+="sw $t0, 0($sp)\n"
        
        return instrucciones

    @visitor.when(CILStringLoad)
    def visit(self, node:CILStringLoad, scope:ScopeMIPS):
        nombrestring=node.params[0]
        instrucciones+="la $v0, "+nombrestring
        instrucciones+=self.save(node.destino,scope)
        return instrucciones

    @visitor.when(CILStringEqual)
    def visit(self, node:CILStringEqual, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -12\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $a1, 4($sp)\n"
        instrucciones+="sw $ra, 8($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="move $a1, $t1\n"
        instrucciones+="jal .Str.stringcomparison"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $a1, 4($sp)\n"
        instrucciones+="lw $ra, 8($sp)\n"
        instrucciones+="addi $sp, $sp, 12\n"
        
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILStringConcat)
    def visit(self, node:CILStringEqual, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -12\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $a1, 4($sp)\n"
        instrucciones+="sw $ra, 8($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="move $a1, $t1\n"
        instrucciones+="jal .Str.stringconcat"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $a1, 4($sp)\n"
        instrucciones+="lw $ra, 8($sp)\n"
        instrucciones+="addi $sp, $sp, 12\n"
        
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)
    
    @visitor.when(CILStringLenght)
    def visit(self, node:CILStringLenght, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -8\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $ra, 8($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="jal .Str.stringlength"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $ra, 8($sp)\n"
        instrucciones+="addi $sp, $sp, 8\n"
        
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILOutString)
    def visit(self, node:CILOutString, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -8\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $ra, 8($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="jal .IO.out_string"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $ra, 8($sp)\n"
        instrucciones+="addi $sp, $sp, 8\n"
        
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)
