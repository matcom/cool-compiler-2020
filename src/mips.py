import visitor
import cil_hierarchy as cil
# from context import Hierarchy
import context
import mips_utility as util
# from hierarchy import TypeHierarchy as Hierarchy

import context as ctx
instruction = ""
enter = "\n"

class VisitorMIPS:
    def __init__(self):
        self.internal_count = 0
        



    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.CILProgramNode)  
    def visit(self, node):
        # print("----------->CILProgramNode")
        data = ".data " + enter 
        textinit = (".globl	main" + enter 
        + ".text " + enter)
        labels = ""
        text = "main:" + enter

        for item in node.dottypes.values():
            data += self.visit(item)
            # data1, labels1, text1 = self.visit(item)
            # data += data1
            # labels += labels1
            # text +=  text1

        for item in node.dotdata.values():
            data += self.visit(item)

        for item in node.dotcode:
            labels += self.visit(item) 

        data += "buffer: .space 1024" + enter
        text +=  "j entry" + enter
      
        
        return data + textinit + text + labels 


    @visitor.when(cil.CILDataNode)   
    def visit(self, node):
        # print("----------->CILDataNode")

        return "" + node.vname + ": .asciiz " + "\""+ node.value + "\""+ enter
        

    @visitor.when(cil.CILTypeNode)  
    def visit(self, node):
        # print("----------->CILTypeNode")

        # data = (node.cinfo.name + ": .space " + str(node.cinfo.meth_length + 4) + enter
        #      + ".asciiz " + "\""+ node.cinfo.name + "\""+ enter)
        labelbody = ""

        data = (node.cinfo.name + ": " 
            + ".word " + str(node.cinfo.meth_length + 8) + enter)

        parent = node.cinfo.parent
        if parent == None:
            data += ".word 0"  + enter
        else:
            data += ".word " + parent.cinfo.name + enter
            

        lista = list(node.methods.values())
        lista.sort(key=lambda x:x.finfo.vmholder)
        # print("/////lista",lista)
        
        for func in lista:
            data += ".word " + func.finfo.name + enter
        data += ".asciiz " + "\""+ node.cinfo.name + "\""+ enter

        
        # i = 8
        # text = (util.ReservaMemoria(4*node.methods.__len__() + i)
        #     + "# apunta tipo a tabla"  + enter
        #     + "la $t1, " + node.cinfo.name +"t" + enter
        #     + "sw $t1, 0($v0) " + enter
        #     + "# referencia a padre") + enter
        
        # text = ("# CILTypeNode" + enter
        #     # + "la $t1, " + node.cinfo.name +"t" + enter
        #     # + "sw $t1, " + node.cinfo.name + enter
        #     + "la $v0, "+ node.cinfo.name + enter)


        # parent = node.cinfo.parent
        # if not parent == None:
        #     print("parent",parent)
        #     text += ( "la $t1, " + parent.cinfo.name + enter
        #         + "sw $t1, 0($v0) " + enter
        #         # + "la $t1, " + node.cinfo.name + enter
        #         # + "sw $v0, 0($t1)" + enter
        #         + "# rellenar tabla" + enter )
        # else:
        #     text += ("li $t1, " + str(0) + enter
        #              + "sw $t1, 0($v0) " + enter
        #             #  + "la $t1, " + node.cinfo.name + enter
        #             #  + "sw $v0, 0($t1)" + enter
        #              + "# rellenar tabla" + enter)


        # i = 8
        # for func in node.methods.values():
        #     labelname = "" + func.finfo.name
        #     # labelbody1 = self.visit(func)
        #     # capturar direccion del label del metodo y asociarlo en la tv
        #     text += ("la $t1, " + labelname + enter 
        #          + "la $t2, " + node.cinfo.name + enter
        #          + "sw $t1, " + str(i) +"($t2)" + enter)
        #     # labelbody += labelbody1
        #     i += 4  
        # return (data, labelbody, text)
        return data


    @visitor.when(cil.CILFunctionNode) 
    def visit(self, node):
        # print("----------->CILFunctionNode")
        label = "" + node.finfo.name

        text = ("# cil function Node" + enter
              + label +":"+ enter)
        pos_sp = len(node.arguments) * 4

        text += "addi $a3, $sp, " + str(pos_sp)+ enter
        
        text += ("# reservar locarvars" + enter
              + util.ReservaPila(len(node.localvars)))

        # for item in node.arguments:
        #     text+= self.visit(item)
        # for item in node.localvars:
        #     print("cosa",self.visit(item))
        #     text+= self.visit(item)
        for item in node.instructions:
            # print("item",item)
            text += self.visit(item)
        
        # text += "# prueba" + enter + util.PrintStr("strName")
        return text

    # @visitor.when(cil.CILArgNode)
    # def visit(self, node):
    #     return "# Arg Node" + enter


  
    # @visitor.when(cil.CILLocalNode)
    # def visit(self, node):
    #     text = "# CILLocalNode" + enter
    #     lenhttype = 1
    #     text = "" + (util.ReservaMemoria(lenhttype)
    #         + "# localNode"+ enter    # falta rellenarlo, o sea, el valor d esas variables...
    #         + "addi $sp, $sp,-4" + enter
    #         + "sw $v0, 0($sp)" + enter)

    #     print("text",text)
    #     return text

    
    @visitor.when(cil.CILAssignNode)   
    def visit(self, node):  
        # print("----------->CILAssignNode")
        text = "# assign" + enter
        if isinstance(node.source,int):
            text += "li $t1, " + str(node.source) + enter
        else:
            text += "lw $t1, " + "-"+ str(4*node.source.vmholder)+"($a3)" + enter

        text += "sw $t1, " + "-"+ str(4*node.dest.vmholder)+"($a3)" + enter
        return text
            

    @visitor.when(cil.CILPlusNode)   
    def visit(self, node):
        # print("----------->CILPlusNode")
        text = "# CILPlusNode" + enter
        # if(isinstance(node.left,int)):
        #     text += "li $t2, " +str(node.left) + enter
        # else:
        #      text += "lw $t2, " + "-" + str(4*(node.left.vmholder))+"($a3)" + enter

        # if(isinstance(node.right,int)):
        #     text += "li $t3, " +str(node.right) + enter
        # else:
        #      text += "lw $t3, " + "-" + str(4*(node.right.vmholder))+"($a3)" + enter

        # text += "add $t1, $t2, $t3" + enter
        #     + "sw $t1, " + "-" + str(4*(node.dest.vmholder))+"($a3)" + enter)
        # text += util.Opera("add",4*(node.dest.vmholder),4*(node.left.vmholder),4*(node.right.vmholder))

        text += util.Opera("add",node)
        return text

    @visitor.when(cil.CILMinusNode)   
    def visit(self, node):
        # print("----------->CILMinusNode")
        text = "# CILMinusNode" + enter
        # text += util.Opera("sub",4*(node.dest.vmholder),4*(node.left.vmholder),4*(node.right.vmholder))
        text += util.Opera("sub",node)
        return text

    @visitor.when(cil.CILStarNode) # necesito en el vinfo q haya un flag q m diga si es int o no
    def visit(self, node):
        # print("----------->CILStarNode")
        text = "# CILStarNode" + enter
        # text += util.OperaSpecial("mult",4*(node.dest.vmholder),4*(node.left.vmholder),4*(node.right.vmholder))
        text += util.Opera("mul",node)
        return text
    
    @visitor.when(cil.CILDivNode) # necesito en el vinfo q haya un flag q m diga si es int o no
    def visit(self, node):
        # print("----------->CILDivNode")
        text = "# CILDivNode" + enter
        # text += util.OperaSpecial("div",4*(node.dest.vmholder),4*(node.left.vmholder),4*(node.right.vmholder))
        text += util.OperaSpecial("div",node)
        return text

    @visitor.when(cil.CILAllocateNode)   
    def visit(self, node):
        # print("----------->CILAllocateNode")
        text = "# CILAllocateNode" + enter
        tam = node.cinfo.attr_length
        text += (util.ReservaMemoria(tam+4)
                + " # guardar en dest" + enter
                + "sw $v0, "+ "-"+ str(4*(node.dest.vmholder))+"($a3)" + enter
                + " # en la instancia poner referencia a su info_table" + enter
                + "la $t1, "+ node.cinfo.name + enter
                + "sw $t1, 0($v0)" + enter)
        return text

    @visitor.when(cil.CILGotoIfNode)   
    def visit(self, node):
        # print("----------->CILGotoIfNode")
        text = "# CILGotoIfNode" + enter 
        text += ( "lw $t1, " + "-"+ str(4*(node.vinfo.vmholder))+"($a3)"+ enter
            +"bne $t1, $zero, "+ node.label.name + enter)
        return text

    

    @visitor.when(cil.CILGotoNode)  
    def visit(self, node):
        # print("----------->CILGotoNode")
        text = "# CILGotoNode" + enter
        text += "j "+ node.label.name + enter
        return text

    @visitor.when(cil.CILLabelNode)  
    def visit(self, node):
        # print("----------->CILLabelNode")
        text = "# CILLabelNode" + enter
        text += node.name +":" + enter
        return text

        
    @visitor.when(cil.CILTypeOfNode)  
    def visit(self, node):
        # print("----------->CILTypeOfNode")
        text = "# CILTypeOfNode" + enter
        text += ("# llegar hasta la inf_table" + enter
                + "lw $t1, " + "-"+ str(4*(node.var.vmholder))+"($a3)"+ enter
                + "lw $t2, 0($t1) " + enter
                # + "lw $v1, 0($t2)"+ enter
                + "# guardarlo en  destino" + enter
                + "sw $t2," + "-"+ str(4*(node.dest.vmholder))+"($a3)"+ enter)
        return text


    @visitor.when(cil.CILLoadNode)   
    def visit(self, node):
        # print("----------->CILLoadNode")
        text = "# CILLoadNode" + enter
        text += ("la $t1, " + node.msg.vname + enter
                + "sw $t1," + "-"+ str(4*node.dest.vmholder)+"($a3)"+ enter )
        return text




    @visitor.when(cil.CILParamNode)   
    def visit(self, node):
        # print("----------->CILParamNode")
        text = "# CILParamNode " + enter
        text += "lw $t1, "+ "-"+ str(4*node.vinfo.vmholder)+"($a3)" + enter
        text += util.Push("$t1")
        return text 


    @visitor.when(cil.CILSetAttribNode)   
    def visit(self, node):
        # print("----------->CILSetAttribNode")
        text = "# CILSetAttribNode" + enter
        text += ("lw $t1, "+ "-"+ str(4*node.dest.vmholder)+"($a3)" + enter
            +"addi $t2, $t1, "+ str(4*node.nattr)+ enter
            +"lw $t3, "+ "-"+ str(4*node.source.vmholder)+"($a3)" + enter
            + "sw $t3, 0($t2)"+ enter)
        return text

    @visitor.when(cil.CILGetAttribNode)   
    def visit(self, node):
        # print("----------->CILGetAttribNode")
        text = "# CILGetAttribNode" + enter
        text += ("lw $t1, "+ "-"+ str(4*node.source.vmholder)+"($a3)" + enter
            +"lw $t2, "+ str(4*node.nattr)+ "($t1)" + enter
            +"addi $t3, $a3, "+ "-"+ str(4*node.dest.vmholder)+ enter
            + "sw $t2, 0($t3)"+ enter)
        return text

    @visitor.when(cil.CILGetIndexNode)   
    def visit(self, node):
        # print("----------->CILGetIndexNode")
        text = "# CILGetIndexNode" + enter
        text += ("lw $t1, "+ "-"+ str(4*node.array.vmholder)+"($a3)" + enter
            + "lw $t2, -"+ str(4*node.index.vmholder)+"($a3)" + enter
            + "add $t3, $t1,$t2" + enter 
            + "lb $t4, 0($t3) " + enter
            + "li $t2, 0" + enter 
            + "sw $t2, " + "-"+ str(4*node.dest.vmholder)+"($a3)" + enter
            + "sb $t4, " + "-"+ str(4*node.dest.vmholder)+"($a3)" + enter)
        return text



    @visitor.when(cil.CILReturnNode)  
    def visit(self, node):
        # print("----------->CILReturnNode")
        text = "# CILReturnNode" + enter
        if node.value == None:
            text += "li $v1, 0" + enter
            # text += "jr $ra"  
            # return text
        elif isinstance(node.value,int):
            text += "li $v1, " + str(node.value) + enter
            # text += "jr $ra"
        else:
            text += ("lw $t1, "+ "-"+ str(4*node.value.vmholder)+"($a3)" + enter
                + "move $v1, $t1" + enter )
        text += "# restaurar pila con respecto al metodo" + enter
        text += "move $sp, $a3" + enter
        text += "jr $ra"+ enter
        return text


    @visitor.when(cil.CILSaveState)    
    def visit(self, node):
        # print("----------->CILSaveState")
        text = (" # SaveState"+ enter 
            + util.SalvaRegistros())
        return text

    @visitor.when(cil.CILStaticCallNode)    
    def visit(self, node):
        # print("----------->CILStaticCallNode")
        text = (" # CILStaticCallNode" + enter
            + "jal " + node.meth_name + enter 
            + util.CargaRegistros()
            + "sw $v1, -" + str(4*node.dest.vmholder) +"($a3)" + enter)


        return text



    @visitor.when(cil.CILDynamicCallNode)   
    def visit(self, node):
        # print("----------->CILDynamicCallNode")
        text = "# CILDynamicCallNode"  + enter
        text+= ("lw $t1, -" + str(4*node.ctype.vmholder)+"($a3)"+ enter
            + "lw $t2, "+ str(4*node.meth_name)+"($t1)"+  enter
            + "jalr $t2" + enter
            + util.CargaRegistros()
            + "sw $v1, -" + str(4*node.dest.vmholder) +"($a3)" + enter)
        return text




    @visitor.when(cil.CILLengthNode)    
    def visit(self, node):
        # print("----------->CILLengthNode")
        text = (util.Length(node.array.vmholder,self)
                + "sw $s0, "+ "-"+ str(4*node.dest.vmholder)+"($a3)" + enter)
        return text


    @visitor.when(cil.CILConcatNode) 
    def visit(self, node):
        # print("----------->CILConcatNode")
        text = "# CILConcatNode" + enter
        text += util.Concat(4*node.array1.vmholder,4*node.array2.vmholder,self)
        text += "sw $t5, -"+ str(4*node.dest.vmholder) +"($a3)" + enter
        return text



    @visitor.when(cil.CILSubstringNode)   
    def visit(self, node):
        # print("----------->CILSubstringNode")
        text = ("# CILSubstringNode" + enter
            + util.Substring(4*node.i.vmholder,4*node.l.vmholder,4*node.array.vmholder,self)
            + "sw $v0, "+ "-"+ str(4*node.dest.vmholder)+"($a3)"+ enter)
        return text



    @visitor.when(cil.CILReadStrNode) 
    def visit(self, node):
        # print("----------->CILReadStrNode")
        text = ("# CILReadStrNode" + enter
            + util.leerString(self)
            + "sw $t5, -" + str(4*node.vinfo.vmholder)+"($a3)" + enter) 
        return text 


        
    @visitor.when(cil.CILReadIntNode)   
    def visit(self, node):
        # print("----------->CILReadIntNode")
        text = ("# CILReadNodeInt" + enter
            + "li $v0, 5" + enter
            + "syscall"+ enter
            + "sw $v0, " + util.DeLaPila(node.vinfo.vmholder))
        return text


    @visitor.when(cil.CILPrintIntNode)   
    def visit(self, node):
        # print("----------->CILPrintIntNode")
        text = (" # CILPrintNodeInt " + enter
            + "lw $t1, " + util.DeLaPila(node.vinfo.vmholder) 
            + "li $v0, 1" + enter
            + "move $a0, $t1" + enter
            + "syscall"+ enter)
        return text

    @visitor.when(cil.CILPrintStrNode)  
    def visit(self, node):
        # print("----------->CILPrintStrNode")
        text = (" # CILPrintNodeStr " + enter
            + "lw $t1, " + util.DeLaPila(node.vinfo.vmholder) 
            + "li $v0, 4" + enter
            + "move $a0, $t1" + enter
            + "syscall"+ enter)
        return text

    @visitor.when(cil.CILParentNode)   
    def visit(self, node):
        # print("----------->CILParentNode")
        text = " # CILParentNode" + enter
        text += "lw $t1, -" + str(4*node.ntype.vmholder) + "($a3)" + enter
        text += "lw $t2, 4($t1) " + enter
        text += "sw $t2, -"+ str(4*node.dest.vmholder) + "($a3)" + enter
        return text

    @visitor.when(cil.CILErrorNode) 
    def visit(self, node):
        # print("----------->CILErrorNode")
        text = "# CILErrorNode" + enter
        text +=  "li $a0, "+ str(node.num) + enter
        text +=  "li $v0, 17" + enter
        text +=  "syscall" + enter
        return text

    @visitor.when(cil.CILLessThan) 
    def visit(self, node):
        # print("----------->CILLessThan")
        text = ("# CILLessThan" + enter
            + "lw $t1, -" + str(4*node.left.vmholder) +"($a3)" + enter
            + "lw $t2, -" + str(4*node.right.vmholder) +"($a3)" + enter
            + "slt $t3, $t1, $t2" + enter
            + "sw $t3, -" + str(4*node.dest.vmholder)+"($a3)" + enter) 
        return text

    @visitor.when(cil.CILTypeName) 
    def visit(self, node):
        # print("----------->CILTypeName")
        text = ("# CILTypeName" + enter
            + "lw $t1, -" + str(4*node.nclass.vmholder) +"($a3)" + enter
            + "lw $t2, 0($t1)" + enter
            + "add $t3, $t2, $t1" + enter
            # + "lw $t4, 0($t3)" + enter
            + "sw $t3, -" + str(4*node.dest.vmholder)+"($a3)" + enter) 
        return text

    @visitor.when(cil.CILReturnFinal) 
    def visit(self, node):
        # print("----------->CILReturnFinal")
        text = "# CILReturnFinal" + enter
        text +=  "li $a0, 0" + enter
        text +=  "li $v0, 17" + enter
        text +=  "syscall" + enter
        return text
    










# como se hace lo d ver la representacion en str de un # 
# necesito q los vmholder de los locals sean seguido de arg 
# arreglar los operadore, pues tengo q saber si hay una direccion o un int
# el typeof resolverlo desde cil, o sea, coger el nmbre q ya va a estar en el .data d mips y es a lo q apunta

# con q mult trabajar 

# revisar las excepciones del length
# el return del entry tiene q salir del programa... si sigue coje la proxima etiqueta...



# self_type
# read str
# static dispatch
# substring 