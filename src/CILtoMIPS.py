from AST import *
from CIL import *
from ScopeMIPS import *
import visitor as visitor
import os

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
        self.parents={}

    def load(self, node:CILInstructionNode,scope:ScopeMIPS, soloelprimero=False, desplazamiento=0):
        instrucciones=""
        parametro0=node.params[0]
        # if isinstance(node, CILTypeCheck):
        #     print("here")
        if scope.methodclass != "Main.special":
            atributos=self.atributos[scope.methodclass]
        else:
            atributos=[]
        DicNombreAtributos={}
        nombresAtributos=[]
        for at in atributos:
            nombresAtributos.append(at.name)
            DicNombreAtributos[at.name]=at.attributeType

        if isinstance(parametro0, int):
            instrucciones+="li $t0,"+str(parametro0)+"\n"
        elif parametro0 == 'true':
            instrucciones+="li $t0,1\n"
        elif parametro0 == 'false':
            instrucciones+="move $t0, $zero\n"
        elif parametro0 in nombresAtributos:
            instrucciones+="lw $t0,"+str(nombresAtributos.index(parametro0)*4+4)+"($a0)\n"
        elif parametro0 in scope.locals.keys():
            instrucciones+="lw $t0,"+str(scope.locals[parametro0]+desplazamiento)+"($sp)\n"
        elif parametro0 in scope.parameters.keys():
            instrucciones+="lw $t0,"+str(scope.parameters[parametro0]+desplazamiento)+"($sp)\n"
        elif parametro0 in scope.registerparameters.keys():
            instrucciones+="move $t0,"+scope.registerparameters[parametro0]+"\n"
        elif parametro0 in self.data.keys():
            instrucciones+="la $t0,"+parametro0+"\n"
        elif parametro0 in self.clases:
            instrucciones+="la $t0,"+parametro0+"clase\n"
        else:
            node.instructionPrint()
            assert False

        if len(node.params)<2 or soloelprimero:
            return instrucciones

        parametro1=node.params[1]

        if isinstance(parametro1, int):
            instrucciones+="li $t1,"+str(parametro1)+"\n"
        elif parametro1 == 'true':
            instrucciones+="li $t1,1\n"
        elif parametro1 == 'false':
            instrucciones+="move $t1, $zero\n"
        elif parametro1 in nombresAtributos:           
            instrucciones+="lw $t1,"+str(nombresAtributos.index(parametro1)*4+4)+"($a0)\n"
        elif parametro1 in scope.locals.keys():
            instrucciones+="lw $t1,"+str(scope.locals[parametro1]+desplazamiento)+"($sp)\n"
        elif parametro1 in scope.parameters.keys():
            instrucciones+="lw $t1,"+str(scope.parameters[parametro1]+desplazamiento)+"($sp)\n"
        elif parametro1 in scope.registerparameters.keys():
            instrucciones+="move $t1,"+scope.registerparameters[parametro1]+"\n"
        elif parametro1 in nombresAtributos:           
            instrucciones+="lw $t1,"+str(nombresAtributos.index(parametro1)*4+4)+"($a0)\n"
        elif parametro1 in self.clases:
            instrucciones+="la $t1,"+parametro1+"clase\n"
        else:
            assert False

        if len(node.params)<3 or soloelprimero:
            return instrucciones

        parametro2=node.params[2]

        if isinstance(parametro2, int):
            instrucciones+="li $t2,"+str(parametro2)+"\n"
        elif parametro2 == 'true':
            instrucciones+="li $t2,1\n"
        elif parametro2 == 'false':
            instrucciones+="move $t2, $zero\n"
        elif parametro2 in nombresAtributos:           
            instrucciones+="lw $t2,"+str(nombresAtributos.index(parametro2)*4+4)+"($a0)\n"
        elif parametro2 in scope.locals.keys():
            instrucciones+="lw $t2,"+str(scope.locals[parametro2]+desplazamiento)+"($sp)\n"
        elif parametro2 in scope.parameters.keys():
            instrucciones+="lw $t2,"+str(scope.parameters[parametro2]+desplazamiento)+"($sp)\n"
        elif parametro2 in scope.registerparameters.keys():
            instrucciones+="move $t2,"+scope.registerparameters[parametro2]+"\n"
        elif parametro2 in self.clases:
            instrucciones+="la $t2,"+parametro2+"clase\n"
        else:
            assert False

        return instrucciones

    def save(self, destino:str,scope:ScopeMIPS, desplazamiento=0):
        if scope.methodclass!="Main.special":
            atributos=self.atributos[scope.methodclass]
        else:
            atributos=[]
        instrucciones=""
        nombresAtributos=[]
        for at in atributos:
            nombresAtributos.append(at.name)

        if destino in nombresAtributos:
            instrucciones+="sw $v0,"+str(nombresAtributos.index(destino)*4+4)+"($a0)\n"
        elif destino in scope.locals.keys():
            instrucciones+="sw $v0,"+str(scope.locals[destino]+desplazamiento)+"($sp)\n"
        elif destino in scope.parameters.keys():
            instrucciones+="sw $v0,"+str(scope.parameters[destino]+desplazamiento)+"($sp)\n"
        elif destino in scope.registerparameters.keys():
            instrucciones+="move "+scope.registerparameters[destino]+",$t0\n"
        else:
            # print(destino)
            # print(scope.locals.keys())
            # print(scope.parameters.keys())
            # print(scope.registerparameters.keys())
            # print(nombresAtributos)
            # print(self.data.keys())
            assert False
        return instrucciones

    def loadAndSaveAndInstructions(self,node:CILInstructionNode, instructions:str, scope:ScopeMIPS):
        return self.load(node,scope)+instructions+self.save(node.destination,scope)

    def MainInstruction(self):
        instrucciones=""
        instrucciones+="addi $sp ,$sp, -4\n"
        instrucciones+="sw $ra, 0($sp)\n"
        instrucciones+="jal Main.Special\n"
        instrucciones+="lw $ra, 0($sp)\n"
        instrucciones+="addi $sp ,$sp, 4\n"
        instrucciones+="jr $ra\n"
        instrucciones+="li $v0, 10\n"
        instrucciones+="syscall\n"
        return instrucciones
    
    @visitor.on('node')
    def visit(self, node, sope:ScopeMIPS):
        pass

    @visitor.when(CILProgram)
    def visit(self, node:CILProgram, _):
        datainstructions=".data\n"
        datainstructions+='StringAbort: .asciiz "Abort called from class String'+'\\'+'n'+'"\n'
        datainstructions+='index_error: .asciiz "Wrong Index Detected'+'\\'+'n'+'"\n'
        for element in node.Data:
            datainstructions+=element.nombre+': .asciiz '+element.valorString+'\n'
            self.data[element.nombre]=element.valorString

        scope=ScopeMIPS()
        
        for element in node.Types:
            self.clases.append(element.name)
            self.atributos[element.name]=element.listaAtributos
            self.metodos[element.name]=element.listaMetodos
            self.parents[element.name]=element.parent
            metodosnombre=[]
            for met in element.listaMetodos:
                metodosnombre.append(met.localname)
            
            scope.classmethods[element.name]=metodosnombre
            
            datainstructions+=element.name+"clase: .word "

            if element.parent==None:
                datainstructions+= "0"
            else:
                datainstructions+=element.parent+"clase"


            for i in range(len(element.listaMetodos)):
                datainstructions+=","
                datainstructions+=element.listaMetodos[i].globalname
                self.metodosglobales[element.name+"#"+element.listaMetodos[i].localname]=element.listaMetodos[i].globalname

            datainstructions+="\n"

        instrucciones=".text\n"
        instrucciones+=".globl main\n"
        instrucciones+="main:\n"
        instrucciones+=self.MainInstruction()
        file_dir = 'StaticCode'
        files = [os.path.abspath(file) for file in os.listdir() if file.endswith('Code')]
        archivo=open(os.path.join(files[0],"AssemblyMethods.asm"),encoding='utf-8')
        metodosdefault=archivo.read()
        instrucciones+=metodosdefault
        archivo.close()
        for element in node.Methods:
            # if element.nombre=="f56":
            #     print()
            instrucciones+=(self.visit(element, scope))

        return datainstructions+instrucciones

    @visitor.when(CILGlobalMethod)
    def visit(self, node:CILGlobalMethod, scope:ScopeMIPS):
        # if node.nombre in ["f9","a2i"]:
        #     print("here")
        # if scope.methodclass in ["CellularAutomaton", '"CellularAutomaton"']:
        #     print("here")
        instrucciones=""
        instrucciones+=node.nombre+": #"+node.comments+"\n"

        scope.methodname=node.nombre
        scope.methodclass=node.originclass

        localespropias={}
        for i in range(len(node.locals)):
            localespropias[node.locals[i]]=(i*(4)+4)#+"($sp)"

        scope.locals=localespropias
        
        self.locals[node.nombre]=localespropias

        misregisterparams={}
        misotrosparams={}
        for i in range(len(node.params)):
            if i<4:
                if isinstance(node.params[i], str):
                    misregisterparams[node.params[i]]="$a"+str(i)#$a
                else:
                    misregisterparams[node.params[i].name]="$a"+str(i)
            else:
                if isinstance(node.params[i], str):
                    misotrosparams[node.params[i]]=((i-4+len(node.locals)+1)*4)#+"($sp)"   Puse el mas 1 porque siempre antes de llamar un metodo se guarda $ra en la pila, por lo que los parametros estarian desplazados
                else:
                    misotrosparams[node.params[i].name]=((i-4+len(node.locals)+1)*4)#+"($sp)"

        scope.registerparameters=misregisterparams
        scope.parameters=misotrosparams
        
        self.registerparams[node.nombre]=misregisterparams
        self.params[node.nombre]=misotrosparams
            
        #Inicalizando variables locales
        instrucciones+="addi $sp, $sp, -"+str(4*len(node.locals)+4)+"\n"
        # instrucciones+="sw $ra, 0($sp)\n" Al parecer sobra

        for i in range(len(node.intrucciones)):
            # if not isinstance(node.intrucciones[i],str):
            #     print(node.intrucciones[i])
            instrucciones+=self.visit(node.intrucciones[i], scope)
            
        retorno=None
        if len(node.intrucciones)>0:
            ultimainstruccion=node.intrucciones[len(node.intrucciones)-1]
            retorno=ultimainstruccion.destination
        
        # if retorno != None:
        #     instrucciones+="lw $v0, 0($sp)\n"


        # instrucciones+="lw $ra, 0($sp)\n" Al parecer sobra
        instrucciones+="addi $sp, $sp, "+str(4*len(node.locals)+4)+"\n"
        instrucciones+="jr $ra\n"

        return instrucciones

    @visitor.when(CILConditionalJump)
    def visit(self, node:CILConditionalJump, scope:ScopeMIPS):
        instrucciones=self.load(node,scope,True)
        instrucciones+="bgtz $t0, "+node.params[1]+"\n"
        return instrucciones

    @visitor.when(CILJump)
    def visit(self, node:CILJump, scope:ScopeMIPS):
        instrucciones="b "+node.params[0]+"\n"
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
        instrucciones+=self.load(node, scope)

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
        # instrucciones="move $s0, $a0\n"
        # instrucciones+="move $s1, $a1\n"
        # instrucciones+="move $a0, $t0\n"
        # instrucciones+="move $a1, $t1\n"
        instrucciones="seq $v0 ,$t0, $t1\n"
        # instrucciones+="move $a0, $s0\n"
        # instrucciones+="move $a1, $s1\n"
        return self.loadAndSaveAndInstructions(node, instrucciones, scope)
    @visitor.when(CILLesser)
    def visit(self, node:CILLesser, scope:ScopeMIPS):
        instrucciones="slt $v0, $t0, $t1\n"
        return self.loadAndSaveAndInstructions(node, instrucciones, scope)

    @visitor.when(CILLesserEqual)
    def visit(self, node:CILLesserEqual, scope:ScopeMIPS):
        instrucciones="sle $v0, $t0, $t1\n"
        return self.loadAndSaveAndInstructions(node, instrucciones, scope)

    @visitor.when(CILLabel)
    def visit(self, node:CILLabel, scope:ScopeMIPS):
        instrucciones=node.params[0]+":\n"
        return instrucciones

    # @visitor.when(CILArgument)
    # def visit(self, node:CILArgument, scope:ScopeMIPS):
    #     instrucciones=self.load(node,scope)
    #     if scope.paramcount<4:
    #         instrucciones+="move $a"+str(scope.paramcount)+", $t0\n"
    #     else:
    #         instrucciones+="addi $sp, $sp, -4\n"
    #         instrucciones+="sw $t0, 0($sp)\n"
        
        return instrucciones

    @visitor.when(CILAllocate)
    def visit(self, node:CILAllocate, scope:ScopeMIPS):
        instrucciones=""
        tipo=node.params[0]
        tamanno=4
        if not tipo in ['Int','Bool']:
            tamanno=(len(self.atributos[tipo])+1)*4
        instrucciones+="addi $sp, $sp, -4\n"
        instrucciones+="sw $a0, 0($sp)\n"

        instrucciones+="li $a0,"+str(tamanno)+"\n"
        instrucciones+="li $v0, 9\n"
        instrucciones+="syscall\n"
        
        instrucciones+="la $t0, "+tipo+"clase\n"
        instrucciones+="sw $t0, 0($v0)\n"

        #Poniendo en 0 todos los elementos
        if not tipo in ['Int','Bool',"String"]:
            for i in range(len(self.atributos[tipo])):
                instrucciones+="sw $zero, "+str(i*4+4)+"($v0)\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="addi $sp, $sp, 4\n"

        #TODO Llamar al metodo init suyo

        return instrucciones+self.save(node.destination,scope)

    @visitor.when(CILVirtualCall)
    def visit(self, node:CILVirtualCall, scope:ScopeMIPS):
        tipo=node.params[0]
        func_id=node.params[1]
        instrucciones=""
        instrucciones+="la $t0,"+tipo+"clase\n"
        instrucciones+="lw $t0,"+str(scope.classmethods[tipo].index(func_id)*4+4)+"($t0)\n"
        instrucciones+="addi $sp, $sp, -4\n"
        instrucciones+="sw $ra, 0($sp)\n"
        instrucciones+="jal $t0 #"+str(node.destination)+"<-"+str(node.params)+"\n"
        instrucciones+="lw $ra, 0($sp)\n"
        instrucciones+="addi $sp, $sp, 4\n"

        if scope.paramcount>4:
            instrucciones+="addi $sp, $sp, "+str((scope.paramcount-4)*4)+"\n"
            scope.paramcount=4
        
        for i in range(scope.paramcount):
            instrucciones+="lw $a"+str(scope.paramcount-1-i)+", "+str(i*4)+"($sp)\n"

        instrucciones+="addi $sp, $sp, "+str(scope.paramcount*4)+"\n"
        instrucciones+=self.save(node.destination,scope)

        scope.paramcount=0
        
        return instrucciones

    @visitor.when(CILCall)
    def visit(self, node:CILCall, scope:ScopeMIPS):
        tipo=node.params[0]
        func_id=node.params[1]
        instrucciones="lw $t0, 0($a0)\n"
        instrucciones+="lw $t0,"+str(scope.classmethods[tipo].index(func_id)*4+4)+"($t0)\n"
        instrucciones+="addi $sp, $sp, -4\n"
        instrucciones+="sw $ra, 0($sp)\n"
        instrucciones+="jalr $ra,$t0 #"+str(node.destination)+"<-"+str(node.params)+"\n"
        instrucciones+="lw $ra, 0($sp)\n"
        instrucciones+="addi $sp, $sp, 4\n"

        if scope.paramcount>4:
            instrucciones+="addi $sp, $sp, "+str((scope.paramcount-4)*4)+"\n"
            scope.paramcount=4
        
        for i in range(scope.paramcount):
            instrucciones+="lw $a"+str(scope.paramcount-1-i)+", "+str(i*4)+"($sp)\n"

        instrucciones+="addi $sp, $sp, "+str(scope.paramcount*4)+"\n"
        instrucciones+=self.save(node.destination,scope)

        scope.paramcount=0
        
        return instrucciones

    @visitor.when(CILArgument)
    def visit(self, node:CILArgument, scope:ScopeMIPS):
        instrucciones=""
        # if scope.methodname in ["main","f7"]:
        #     print("este")
        instrucciones+=self.load(node,scope,desplazamiento=scope.paramcount*4)
        instrucciones+="#Argument "+str(node.params[0])+"\n"
        instrucciones+="addi $sp, $sp, -4\n"
        if scope.paramcount<4:
            instrucciones+="sw $a"+str(scope.paramcount)+", 0($sp)\n"
            instrucciones+="move $a"+str(scope.paramcount)+",$t0\n"
        else:
            instrucciones+="sw $t0, 0($sp)\n"

        scope.paramcount+=1
        
        return instrucciones

    @visitor.when(CILStringLoad)
    def visit(self, node:CILStringLoad, scope:ScopeMIPS):
        nombrestring=node.params[0]
        instrucciones="la $v0, "+nombrestring+"\n"
        instrucciones+=self.save(node.destination,scope)
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
        instrucciones+="jal .Str.stringcomparison\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $a1, 4($sp)\n"
        instrucciones+="lw $ra, 8($sp)\n"
        instrucciones+="addi $sp, $sp, 12\n"
        
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILStringSubstring)
    def visit(self, node:CILStringSubstring, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -16\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $a1, 4($sp)\n"
        instrucciones+="sw $a2, 8($sp)\n"
        instrucciones+="sw $ra, 12($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="move $a1, $t1\n"
        instrucciones+="move $a2, $t2\n"
        instrucciones+="jal .Str.substring\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $a1, 4($sp)\n"
        instrucciones+="lw $a2, 8($sp)\n"
        instrucciones+="lw $ra, 12($sp)\n"
        instrucciones+="addi $sp, $sp, 16\n"
        
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
        instrucciones+="jal .Str.stringconcat\n"

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
        instrucciones+="sw $ra, 4($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="jal .Str.stringlength\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $ra, 4($sp)\n"
        instrucciones+="addi $sp, $sp, 8\n"
        
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)


        #TODO A rectificar estos

    @visitor.when(CILOutString)
    def visit(self, node:CILOutString, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -8\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $ra, 4($sp)\n"

        instrucciones+="move $a0, $a1\n"
        instrucciones+="jal .IO.out_string\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $ra, 4($sp)\n"
        instrucciones+="addi $sp, $sp, 8\n"
        instrucciones+="move $v0, $a0\n"
        
        return instrucciones+self.save(node.destination,scope)

    @visitor.when(CILInString)
    def visit(self, node:CILInString, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -8\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $ra, 4($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="jal .IO.in_string\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $ra, 4($sp)\n"
        instrucciones+="addi $sp, $sp, 8\n"
        
        return instrucciones+self.save(node.destination,scope)

    @visitor.when(CILOutInt)
    def visit(self, node:CILOutInt, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -8\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $ra, 4($sp)\n"

        instrucciones+="move $a0, $a1\n"
        instrucciones+="jal .IO.out_int\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $ra, 4($sp)\n"
        instrucciones+="addi $sp, $sp, 8\n"
        instrucciones+="move $v0, $a0\n"
        
        return instrucciones+self.save(node.destination,scope)

    @visitor.when(CILInInt)
    def visit(self, node:CILInInt, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp, $sp, -8\n"
        instrucciones+="sw $a0, 0($sp)\n"
        instrucciones+="sw $ra, 4($sp)\n"

        instrucciones+="move $a0, $t0\n"
        instrucciones+="jal .IO.in_int\n"

        instrucciones+="lw $a0, 0($sp)\n"
        instrucciones+="lw $ra, 4($sp)\n"
        instrucciones+="addi $sp, $sp, 8\n"
        
        return instrucciones+self.save(node.destination,scope)

    # @visitor.when(CILTypeCheck)
    # def visit(self, node:CILTypeCheck, scope:ScopeMIPS):
    #     instrucciones=""
    #     instrucciones+="li $v0, 1\n"
        
    #     return instrucciones + self.save(node.destination, scope)


    @visitor.when(CILCopy)
    def visit(self, node:CILCopy, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="addi $sp ,$sp, -4\n"
        instrucciones+="sw $ra, 0($sp)\n"
        instrucciones+="jal .Object.Copy\n"
        instrucciones+="lw $ra, 0($sp)\n"
        instrucciones+="addi $sp ,$sp, 4\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILIntComplement)
    def visit(self, node:CILIntComplement, scope:ScopeMIPS):
        instrucciones="neg $v0, $t0\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)
    
    @visitor.when(CILComplement)
    def visit(self, node:CILComplement, scope:ScopeMIPS):
        instrucciones=""
        instrucciones+="seq $v0, $t0, $zero\n"
        # instrucciones+="addi $v0 ,$t0, 1\n"
        # instrucciones+="li $t1, 2\n"
        # instrucciones+="rem $v0, $v0, $t1\n"
        return self.loadAndSaveAndInstructions(node,instrucciones,scope)

    @visitor.when(CILTypeCheck)
    def visit(self, node:CILTypeCheck, scope:ScopeMIPS):
        # intermedio=CILTypeCheckIntermediate(node.destination,[node.params[0]])
        instrucciones=""
        instrucciones+="addi $sp ,$sp, -4\n"
        instrucciones+="sw $ra, 0($sp)\n"
        instrucciones+="jal .TypeCheck\n"
        instrucciones+="lw $ra, 0($sp)\n"
        instrucciones+="addi $sp ,$sp, 4\n"
        return self.loadAndSaveAndInstructions(node, instrucciones, scope)

    @visitor.when(CILIsVoid)
    def visit(self, node:CILIsVoid, scope:ScopeMIPS):
        instrucciones="seq $v0, $t0, $zero\n"
        return self.loadAndSaveAndInstructions(node, instrucciones, scope)