from visitor import *
from cil import *
from mips import *

class CILtoMIPSVisitor:
    def __init__(self):
        self.data = []
        self.text = []
        self.function = None
        self.types = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.types = node.dottypes

        for typePN in node.dottypes:
            self.visit(typePN)    

        for dataNode in node.dotdata:
            self.visit(dataNode)

        for instructionNode in node.dotcode:
            self.visit(instructionNode)

        return MipsProgramNode(self.data, self.text)


    @visitor.when(TypeNode)
    def visit(self, node):
        self.data.append(MipsStringNode(f'{node.name}_name', node.name))
        self.data.append(MipsWordNode(f'{node.name}_size', 4*(len(node.attributes) + 2)))


    @visitor.when(DataNode)
    def visit(self, node):
        self.data.append(MipsStringNode(node.name, node.value))


    @visitor.when(FunctionNode)
    def visit(self, node:FunctionNode):
        self.function = node
        self.register_instruction(MipsLabelNode(node.name))

        self.register_instruction(MipsCommentNode('muevo el fp al sp, pongo en sp ra y avanzo la pila'))
        self.register_instruction(MipsMoveNode('$fp', '$sp'))
        self.register_instruction(MipsSWNode('$ra', '0($sp)'))
        self.register_instruction(MipsAddiuNode('$sp', '$sp', '-4'))

        self.register_instruction(MipsCommentNode('muevo la pila x las variables locales'))
        self.register_instruction(MipsAddiuNode('$sp', '$sp', f'-{len(node.localvars) * 4}'))

        for ins in node.instructions:
            self.visit(ins)
        
        self.register_instruction(MipsCommentNode('return sp, fp, ra'))
        self.register_instruction(MipsLWNode('$ra', '0($fp)'))
        self.register_instruction(MipsAddiuNode('$sp', '$sp', f'{len(node.localvars) * 4 + 8 + len(node.params) * 4}'))
        self.register_instruction(MipsLWNode('$fp', '0($sp)'))
        self.register_instruction(MipsJRNode('$ra'))
        

    @visitor.when(ArgsNode)
    def visit(self, node):
        self.register_instruction(MipsCommentNode('guardando los parametros'))
        self.register_instruction(MipsSWNode('$fp', '0($sp)'))
        self.register_instruction(MipsAddiuNode('$sp', '$sp' ,'-4'))
        
        for name in node.names:
            pos = self.request_pos(name)
            if not pos is None:
                self.register_instruction(MipsLWNode('$a0', pos))
            else:
                self.register_instruction(MipsLINode('$a0', name))
            
            self.register_instruction(MipsSWNode('$a0', '0($sp)'))
            self.register_instruction(MipsAddiuNode('$sp', '$sp', '-4'))



    @visitor.when(ReturnNode)
    def visit(self, node:ReturnNode):
        self.register_instruction(MipsCommentNode('retornando el valor'))
        pos = self.request_pos(node.value)

        if not pos is None:
            self.register_instruction(MipsLWNode('$a0', pos))
        else:
            self.register_instruction(MipsLINode('$a0', node.value))

    @visitor.when(AllocateNode)
    def visit(self, node:AllocateNode):
        self.register_instruction(MipsCommentNode('init allocate'))
        self.register_instruction(MipsLINode('$v0', '9'))
        self.register_instruction(MipsLWNode('$a0', f'{node.type}_size'))
        self.register_instruction(MipsSyscallNode())

        num = int(node.dest.split('_')[-1])
        self.register_instruction(MipsSWNode('$v0', f'-{(num+1) * 4}($fp)'))
        self.register_instruction(MipsCommentNode('end allocate'))



    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode):
        self.register_instruction(MipsJumpAtAddressNode(node.function))

        num = int(node.dest.split('_')[-1])
        self.register_instruction(MipsSWNode('$a0', f'-{(num+1) * 4}($fp)'))
        self.register_instruction(MipsCommentNode('fin llamada dinamica'))

    @visitor.when(DynamicCallNode)
    def visit(self, node:DynamicCallNode):
        self.register_instruction(MipsCommentNode('comienzo llamada dinamica'))
        self.register_instruction(MipsJumpAtAddressNode(node.method))
        
        num = int(node.dest.split('_')[-1])
        self.register_instruction(MipsSWNode('$a0', f'-{(num+1) * 4}($fp)'))
        self.register_instruction(MipsCommentNode('fin llamada dinamica'))



    @visitor.when(SetAttribNode)
    def visit(self, node:SetAttribNode):
        self.register_instruction(MipsCommentNode('init set attribute'))

        pos = self.request_pos(node.ins)
        self.register_instruction(MipsLWNode('$a0', pos))
        
        nameType = node.att.split('_')[1]
        num = -1

        for typeAct in self.types:
            if typeAct.name == nameType:
                num = typeAct.attributes.index(node.att)
                break
        
        pos = self.request_pos(node.value)
        if not pos is None: 
            self.register_instruction(MipsLWNode('$t1', pos))
        else:
            self.register_instruction(MipsLINode('$t1', node.value))

        self.register_instruction(MipsSWNode('$t1', f'{num * 4 + 8}($a0)'))
        self.register_instruction(MipsCommentNode('end set attribute'))
    
    @visitor.when(GetAttribNode)
    def visit(self, node:GetAttribNode):
        self.register_instruction(MipsCommentNode('init get attribute'))
        
        pos_result = self.request_pos(node.dest)
        pos = self.request_pos(node.ins)
        self.register_instruction(MipsLWNode('$a0', pos))

        nameType = node.att.split('_')[1]
        num = -1

        for typeAct in self.types:
            if typeAct.name == nameType:
                num = typeAct.attributes.index(node.att)
                break

        self.register_instruction(MipsLWNode('$a0', f'{num * 4 + 8}($a0)'))
        self.register_instruction(MipsSWNode('$a0', pos_result))
        


    @visitor.when(LoadNode)
    def visit(self, node):
        self.register_instruction(MipsCommentNode('LOAD inicia'))
        self.register_instruction(MipsLANode('$t1', node.msg))
        dest = self.request_pos(node.dest)
        self.register_instruction(MipsLWNode("$t2",dest))
        self.register_instruction(MipsSWNode('$t1', f"{node.desp}($t2)"))

    @visitor.when(LoadAddressNode)
    def visit(self, node):
        pos = self.request_pos(node.dest)
        self.register_instruction(MipsLANode('$t1', node.msg))
        self.register_instruction(MipsSWNode('$t1', pos))

    @visitor.when(LoadIntNode)
    def visit(self, node):
        self.register_instruction(MipsCommentNode('LOAD inicia'))
        self.register_instruction(MipsLWNode('$t1', node.msg))
        dest = self.request_pos(node.dest)
        self.register_instruction(MipsLWNode("$t2",dest))
        self.register_instruction(MipsSWNode('$t1', f"{node.desp}($t2)"))



    @visitor.when(AssignNode)
    def visit(self, node:AssignNode):
        pos_dest = self.request_pos(node.dest)
        pos_src = self.request_pos(node.source)

        if not pos_src is None:
            self.register_instruction(MipsLWNode('$t1', pos_src))
        else:
            self.register_instruction(MipsLINode('$t1', node.source))

        self.register_instruction(MipsSWNode('$t1', pos_dest))

    @visitor.when(GotoNode)
    def visit(self, node):
        self.register_instruction(MipsJumpNode(node.name))

    @visitor.when(GotoIfNode)
    def visit(self, node):
        pos = self.request_pos(node.condition)

        if not pos is None:
            self.register_instruction(MipsLWNode('$a0', pos))
        else:
            self.register_instruction(MipsLINode('$a0', node.condition))

        self.register_instruction(MipsBNENode('$a0', '$zero', node.name))

    @visitor.when(LabelNode)
    def visit(self, node):
        self.register_instruction(MipsLabelNode(node.name))



    @visitor.when(PlusNode)
    def visit(self, node:PlusNode):        
        pos_dest = self.request_pos(node.dest)
        pos_left = self.request_pos(node.left)
        pos_right = self.request_pos(node.right)

        if not pos_left is None:
            self.register_instruction(MipsLWNode('$t1', pos_left))
        else:
            self.register_instruction(MipsLINode('$t1', node.left))

        if not pos_right is None:
            self.register_instruction(MipsLWNode('$a0', pos_right))
        else:
            self.register_instruction(MipsLINode('$a0', node.right))
        
        self.register_instruction(MipsAddNode('$a0', '$a0', '$t1'))
        self.register_instruction(MipsSWNode('$a0', pos_dest))

    @visitor.when(MinusNode)
    def visit(self, node):
        pos_dest = self.request_pos(node.dest)
        pos_left = self.request_pos(node.left)
        pos_right = self.request_pos(node.right)

        if not pos_left is None:
            self.register_instruction(MipsLWNode('$t1', pos_left))
        else:
            self.register_instruction(MipsLINode('$t1', node.left))

        if not pos_right is None:
            self.register_instruction(MipsLWNode('$a0', pos_right))
        else:
            self.register_instruction(MipsLINode('$a0', node.right))
        
        self.register_instruction(MipsMinusNode('$a0', '$t1', '$a0'))
        self.register_instruction(MipsSWNode('$a0', pos_dest))


    @visitor.when(StarNode)
    def visit(self, node):
        pos_dest = self.request_pos(node.dest)
        pos_left = self.request_pos(node.left)
        pos_right = self.request_pos(node.right)

        if not pos_left is None:
            self.register_instruction(MipsLWNode('$t1', pos_left))
        else:
            self.register_instruction(MipsLINode('$t1', node.left))

        if not pos_right is None:
            self.register_instruction(MipsLWNode('$a0', pos_right))
        else:
            self.register_instruction(MipsLINode('$a0', node.right))
        
        self.register_instruction(MipsStarNode('$a0', '$t1', '$a0'))
        self.register_instruction(MipsSWNode('$a0', pos_dest))
    
    @visitor.when(DivNode)
    def visit(self, node):
        pos_dest = self.request_pos(node.dest)
        pos_left = self.request_pos(node.left)
        pos_right = self.request_pos(node.right)

        if not pos_left is None:
            self.register_instruction(MipsLWNode('$t1', pos_left))
        else:
            self.register_instruction(MipsLINode('$t1', node.left))

        if not pos_right is None:
            self.register_instruction(MipsLWNode('$a0', pos_right))
        else:
            self.register_instruction(MipsLINode('$a0', node.right))
        
        self.register_instruction(MipsDivNode('$a0', '$t1', '$a0'))
        self.register_instruction(MipsSWNode('$a0', pos_dest))

    @visitor.when(ComplementNode)
    def visit(self, node):
        pos_dest = self.request_pos(node.dest)
        pos_expression = self.request_pos(node.expression)

        if not pos_expression is None:
            self.register_instruction(MipsLWNode('$t1', pos_expression))
        else:
            self.register_instruction(MipsLINode('$t1', node.expression))

        self.register_instruction(MipsAddiuNode('$t1', '$t1', 1))
        self.register_instruction(MipsNEGNode('$t1', '$t1'))
        self.register_instruction(MipsSWNode('$t1', pos_dest))


    @visitor.when(LessNode)
    def visit(self, node):
        pos_dest = self.request_pos(node.result)
        pos_left = self.request_pos(node.left)
        pos_right = self.request_pos(node.right)

        if not pos_left is None:
            self.register_instruction(MipsLWNode('$t1', pos_left))
        else:
            self.register_instruction(MipsLINode('$t1', node.left))

        if not pos_right is None:
            self.register_instruction(MipsLWNode('$a0', pos_right))
        else:
            self.register_instruction(MipsLINode('$a0', node.right))

        self.register_instruction(MipsBLTNode('$t1', '$a0', node.labelTrue))
        self.register_instruction(MipsLINode('$a0', 0))
        self.register_instruction(MipsJumpNode(node.labelEnd))
        self.register_instruction(MipsLabelNode(node.labelTrue))
        self.register_instruction(MipsLINode('$a0', 1))
        self.register_instruction(MipsLabelNode(node.labelEnd))
        self.register_instruction(MipsSWNode('$a0', pos_dest))

    @visitor.when(LessEqualNode)
    def visit(self, node):
        pos_dest = self.request_pos(node.result)
        pos_left = self.request_pos(node.left)
        pos_right = self.request_pos(node.right)

        if not pos_left is None:
            self.register_instruction(MipsLWNode('$t1', pos_left))
        else:
            self.register_instruction(MipsLINode('$t1', node.left))

        if not pos_right is None:
            self.register_instruction(MipsLWNode('$a0', pos_right))
        else:
            self.register_instruction(MipsLINode('$a0', node.right))

        self.register_instruction(MipsBLENode('$t1', '$a0', node.labelTrue))
        self.register_instruction(MipsLINode('$a0', 0))
        self.register_instruction(MipsJumpNode(node.labelEnd))
        self.register_instruction(MipsLabelNode(node.labelTrue))
        self.register_instruction(MipsLINode('$a0', 1))
        self.register_instruction(MipsLabelNode(node.labelEnd))
        self.register_instruction(MipsSWNode('$a0', pos_dest))

    @visitor.when(StringComparer)
    def visit(self, node):
        pos_dest = self.request_pos(node.result)
        pos_left = self.request_pos(node.left)
        pos_right = self.request_pos(node.right)

        self.register_instruction(MipsSWNode('$fp', '0($sp)'))
        self.register_instruction(MipsAddiuNode('$sp', '$sp' ,'-4'))

        self.register_instruction(MipsLWNode('$a0', pos_left))            
        self.register_instruction(MipsSWNode('$a0', '0($sp)'))
        self.register_instruction(MipsAddiuNode('$sp', '$sp', '-4'))

        self.register_instruction(MipsLWNode('$a0', pos_right))            
        self.register_instruction(MipsSWNode('$a0', '0($sp)'))
        self.register_instruction(MipsAddiuNode('$sp', '$sp', '-4'))

        self.register_instruction(MipsJumpAtAddressNode('function_comparer_string'))
        self.register_instruction(MipsSWNode('$a0', pos_dest))




    # registers
    def register_data(self, instruction):
        self.data.append(instruction)

    def register_instruction(self, instruction):
        self.text.append(instruction)




    # utils
    def request_pos(self, name):
        if name in [x.name for x in self.function.localvars]:
            numb = int( name.split('_')[-1])
            return f'-{(numb+1) * 4}($fp)'
        elif name in [x.name for x in self.function.params]:
            numb = [param.name for param in self.function.params].index(name)
            return f'{(numb + 1) * 4}($fp)'
        else:
            return None