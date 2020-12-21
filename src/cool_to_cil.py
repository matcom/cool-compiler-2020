import ast_hierarchy as ast
import cil_hierarchy as cil
import visitor
from context import VariableInfo, MethodInfo
from copy import copy


class COOLToCILVisitor:
    def __init__(self, programnode:cil.CILProgramNode):
        self.programnode = programnode

        # La sección .TYPES del CIL
        self.dottypes = {}
        # La sección .DATA del CIL
        self.dotdata = {}
        # La sección .CODE del CIL
        self.dotcode = []

        self.current_class = None

        self.current_function = None

        # Variables locales del método actual
        self.localvars = []

        # Instrucciones del método actual
        self.instructions = []

        # Parametros del metodo actual
        self.arguments = []

        self.internal_count = 0

        self.void = 0

    # Util Methods
    def change_current_function(self, current_func):
        self.current_function = current_func
        self.localvars = current_func.localvars
        self.instructions = current_func.instructions
        self.arguments = current_func.arguments

    def define_internal_local(self):
        vinfo = VariableInfo('internal')
        vinfo.name = self.build_internal_vname(vinfo.name)
        return self.register_local(vinfo)

    def build_internal_vname(self, vname):
        vname = '{}_{}'.format(vname, self.internal_count)
        self.internal_count += 1
        return vname

    def build_label(self):
        fname = 'label_{}'.format(self.internal_count)
        self.internal_count += 1
        return cil.CILLabelNode(fname)

    def register_local(self, vinfo):
        vinfo.vmholder = len(self.localvars) + len(self.arguments)+1
        local_node = cil.CILLocalNode(vinfo)
        self.localvars.append(local_node)
        return local_node.vinfo

    def register_instruction(self, instruction):
        self.instructions.append(instruction)

    def register_argument(self, vinfo):
        vinfo.vmholder = len(self.arguments)+1
        argum = cil.CILArgNode(vinfo)
        self.arguments.append(argum)
        return argum.vinfo
    
    def register_data(self, value):
        vname = 'data_{}'.format(len(self.dotdata))
        data_node = cil.CILDataNode(vname, value)
        self.dotdata[vname] = data_node
        return data_node

    def _boxing(self, vinfo, ctype):
        vlocal = self.define_internal_local()
        self.register_instruction(cil.CILAllocateNode(vlocal, self.dottypes[ctype].cinfo))
        # t_local = self.define_internal_local()
        # self.register_instruction(cil.CILTypeOfNode(t_local, vlocal))
        self.register_instruction(cil.CILSaveState())
        self.register_instruction(cil.CILParamNode(vlocal))
        useless = self.define_internal_local()
        fname = self.dottypes[ctype].methods['ctor'].finfo.name
        self.register_instruction(cil.CILStaticCallNode(useless, fname))
        num2 = self.dottypes[ctype].attrs['value'].vmholder
        self.register_instruction(cil.CILSetAttribNode(vlocal, num2, vinfo))
        return vlocal

    def _ifboxing(self, vvar, cond):
        vret = vvar
        if cond == 'String' or cond == 'Int' or cond == 'Bool':
            vret = self._boxing(vvar, cond)
        return vret

    def _ifobjectboxing(self, vvar, cond1, cond2):
        vret = vvar
        if (cond1 == 'String' or cond1 == 'Int' or cond1 == 'Bool') and cond2 == 'Object':
            vret = self._boxing(vvar, cond1)
        return vret

    # Visit
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode): 
        # print("------------visit node: ProgramNode")       
        self.dottypes = self.programnode.dottypes
        self.dotcode = self.programnode.dotcode
        self.dotdata = self.programnode.dotdata

        for child in node.classes:
            self.visit(child)

        return self.programnode

    @visitor.when(ast.ClassNode)
    def visit(self, node: ast.ClassNode):
        # print("------------visit node: CoolClass")
        self.current_class = self.dottypes[node.typeName]
        parent_class = self.current_class.cinfo.parent

        self.change_current_function(self.current_class.methods['ctor'])
        self.register_argument(VariableInfo('self'))

        useless = self.define_internal_local()
        self.register_instruction(cil.CILSaveState())
        self.register_instruction(cil.CILParamNode(self.arguments[0].vinfo))
        name = parent_class.methods['ctor'].finfo.name
        self.register_instruction(cil.CILStaticCallNode(useless, name))


        for feature in node.features:
            if isinstance(feature, ast.AttributeFeatureNode):
                self.visit(feature)
        
        self.register_instruction(cil.CILReturnNode())

        for feature in node.features:
            if isinstance(feature, ast.FunctionFeatureNode):
                self.visit(feature)

    @visitor.when(ast.AttributeFeatureNode)
    def visit(self, node: ast.AttributeFeatureNode, dest = None):
        # si es un attributo de la clase 
        if self.current_class.attrs.__contains__(node.id):
            var_self = self._find('self')
            vlocal = self.define_internal_local()
            self.visit(node.expression, vlocal)
            num = self.current_class.attrs[node.id].vmholder
            self.register_instruction(cil.CILSetAttribNode(var_self, num, vlocal))
        #si es un atributo interno de un statement
        else:
            node.vinfo = VariableInfo(node.id, node.typeName)
            vlocal = self.register_local(node.vinfo)
            if node.id == 'self':
                v_self = self._find('self')
                self.register_instruction(cil.CILAssignNode(dest, v_self))
            elif not node.vinfo in [a.vinfo for a in self.localvars] and not node.vinfo in [a.vinfo for a in self.arguments]:
                v_self = self._find('self')
                num = self.dottypes[self.current_class.cinfo.name].attrs[node.id].vmholder
                self.register_instruction(cil.CILGetAttribNode(dest, v_self, num))
            else:
                self.register_instruction(cil.CILAssignNode(dest, node.vinfo))
            



    @visitor.when(ast.FunctionFeatureNode)
    def visit(self, node: ast.FunctionFeatureNode):
        # print("------------visit node: Method")
        self.change_current_function(self.dottypes[self.current_class.cinfo.name].methods[node.id])
        
        self.register_argument(VariableInfo('self'))
        for param in node.parameters:            
            self.register_argument(param.vinfo)

        ret_var = self.define_internal_local()
        self.visit(node.statements, ret_var)
        # print("///////////tipo retorno", self.current_function.finfo.returnType)
        # print("////////////tipo", node.exprbody.typeName)
        var_box = self._ifobjectboxing(ret_var, node.statements.typeName, self.current_function.finfo.returnType)
        self.register_instruction(cil.CILReturnNode(var_box))

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode, dest):
        # print("------------visit node: PlusNode")  
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)
        self.register_instruction(cil.CILPlusNode(dest, left, right))

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode, dest):
        # print("------------visit node: MinusNode")  
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)
        self.register_instruction(cil.CILMinusNode(dest, left, right))

    @visitor.when(ast.TimesNode)
    def visit(self, node: ast.TimesNode, dest):
        # print("------------visit node: StarNode")  
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)
        self.register_instruction(cil.CILStarNode(dest, left, right))

    @visitor.when(ast.DivideNode)
    def visit(self, node: ast.DivideNode, dest):
        # print("------------visit node: DivNode")  
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)

        label1 = self.build_label()
        labelerror = self.build_label()
        labelend = self.build_label()

        vhalt = self.define_internal_local()
        self.register_instruction(cil.CILMinusNode(vhalt, right, 0))
        self.register_instruction(cil.CILGotoIfNode(vhalt, label1))
        self.register_instruction(cil.CILGotoNode(labelerror))
        
        self.register_instruction(label1)

        self.register_instruction(cil.CILDivNode(dest, left, right))
        self.register_instruction(cil.CILGotoNode(labelend))

        self.register_instruction(labelerror)
        var1 = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_4']))
        self.register_instruction(cil.CILPrintStrNode(var1))
        self.register_instruction(cil.CILErrorNode())

        self.register_instruction(labelend)

    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode, dest):
        # print("------------visit node: Neg")  
        right = self.define_internal_local()
        self.visit(node.expr, right)
        self.register_instruction(cil.CILMinusNode(dest, 0, right))

    @visitor.when(ast.NotNode)
    def visit(self, node: ast.NotNode, dest):
        # print("------------visit node: Not")  
        right = self.define_internal_local()
        self.visit(node.expr, right)
        self.register_instruction(cil.CILMinusNode(dest, 1, right))

    @visitor.when(ast.LetStatementNode)
    def visit(self, node: ast.LetStatementNode, dest):
        # print("------------visit node: Let")  
        #hacr el visit
        for item in node.variables:
            self.visit(item, dest)

        self.visit(node.expression, dest)

    # @visitor.when(ast.Declaration)
    # def visit(self, node: ast.Declaration):
    #     # print("------------visit node: Declaration")  
    #     vlocal = self.register_local(node.vinfo)
    #     ret_var = self.define_internal_local()
    #     self.visit(node.expr, ret_var)
    #     vbox = self._ifobjectboxing(ret_var, node.expr.typeName, node.vinfo.ctype)
    #     self.register_instruction(cil.CILAssignNode(vlocal, vbox))
    #     return vlocal

    @visitor.when(ast.BlockStatementNode)
    def visit(self, node: ast.BlockStatementNode, dest):
        # print("------------visit node: Block")  
        last = None
        for expr in node.expressions:
            vlocal = self.define_internal_local()
            last = vlocal
            self.visit(expr, vlocal)
        self.register_instruction(cil.CILAssignNode(dest, last))

    @visitor.when(ast.AssignStatementNode)
    def visit(self, node: ast.AssignStatementNode, dest):
        # print("------------visit node: Assignment")  
        v_temp = self.define_internal_local()
        self.visit(node.id, v_temp)
        self.visit(node.expression, v_temp)
        # print("................. node.id.vinfo",node.id.typeName)
        v_box = self._ifobjectboxing(v_temp, node.expression.typeName, node.id.typeName)

        if not node.id.vinfo in [a.vinfo for a in self.localvars] and not node.id.vinfo in [a.vinfo for a in self.arguments]:
            v_self = self._find('self')
            num = self.dottypes[self.current_class.cinfo.name].attrs[node.id.name].vmholder
            self.register_instruction(cil.CILSetAttribNode(v_self, num, v_box))
            self.register_instruction(cil.CILGetAttribNode(dest, v_self, num))
        else:
            self.register_instruction(cil.CILAssignNode(node.id.vinfo, v_box))
            self.register_instruction(cil.CILAssignNode(dest, node.id.vinfo))

    @visitor.when(ast.ConstantStringNode)
    def visit(self, node: ast.ConstantStringNode, dest):
        msg = self.register_data(node.lex)
        var = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var, msg))
        self.register_instruction(cil.CILAssignNode(dest, var))

    @visitor.when(ast.ConstantBoolNode)
    def visit(self, node: ast.ConstantBoolNode, dest):
        var = 1 if node.value else 0
        self.register_instruction(cil.CILAssignNode(dest, var))

    @visitor.when(ast.ConstantNumericNode)
    def visit(self, node: ast.ConstantNumericNode, dest):
        self.register_instruction(cil.CILAssignNode(dest, node.lex))

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, dest):
        #crear su vinfo y definirlo en los locals
        for local in self.localvars:
            if local.vinfo.name == node.lex:
                node.vinfo = local.vinfo
        

    @visitor.when(ast.ConditionalStatementNode)
    def visit(self, node: ast.ConditionalStatementNode, dest):
        # print("------------visit node: Conditional")  
        if_eval = self.define_internal_local()
        self.visit(node.ifexpr, if_eval)

        label_then = self.build_label()
        label_end = self.build_label()

        self.register_instruction(cil.CILGotoIfNode(if_eval, label_then))
        self.visit(node.elseexpr, dest)
        self.register_instruction(cil.CILGotoNode(label_end))
        self.register_instruction(label_then)
        self.visit(node.thenexpr, dest)
        self.register_instruction(label_end)

    @visitor.when(ast.LoopStatementNode)
    def visit(self, node: ast.LoopStatementNode, dest):
        # print("------------visit node: Loop")  

        cond_eval = self.define_internal_local()

        label_entry = self.build_label()
        self.register_instruction(label_entry)

        self.visit(node.whileexpr, cond_eval)

        label_end = self.build_label()
        label_loop = self.build_label()
        self.register_instruction(cil.CILGotoIfNode(cond_eval, label_loop))
        self.register_instruction(cil.CILGotoNode(label_end))

        self.register_instruction(label_loop)

        vbody = self.define_internal_local()
        self.visit(node.loopexpr, vbody)

        self.register_instruction(cil.CILGotoNode(label_entry))
        self.register_instruction(label_end)

        self.register_instruction(cil.CILAssignNode(dest, self.void))

    @visitor.when(ast.LessNode)
    def visit(self, node: ast.LessNode, dest):
        # print("------------visit node: LessThan")  
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, vleft)
        self.visit(node.right, vright)
        rest = self.define_internal_local()
        self.register_instruction(cil.CILLessThan(dest, vleft, vright))

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode, dest):
        # print("------------visit node:.LessEqualThan")  
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, vleft)
        self.visit(node.right, vright)
        self.register_instruction(cil.CILPlusNode(vright, 1, vright))
        rest = self.define_internal_local()
        self.register_instruction(cil.CILLessThan(dest, vleft, vright))

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode, dest):
        # print("------------visit node: Equal")  
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, vleft)
        self.visit(node.right, vright)
        
        if node.left.typeName == 'String':

            vlength_r = self.define_internal_local()
            self.register_instruction(cil.CILLengthNode(vlength_r, vright))
            vlength_l = self.define_internal_local()
            self.register_instruction(cil.CILLengthNode(vlength_l, vleft))
            
            self.register_instruction(cil.CILMinusNode(dest, vlength_l, vlength_r))

            label_loop = self.build_label()
            label_loopbody = self.build_label()
            label_equal = self.build_label()
            label_notequal = self.build_label()
            label_end = self.build_label()

            self.register_instruction(cil.CILGotoIfNode(dest, label_notequal))

            pos = self.define_internal_local()
            self.register_instruction(cil.CILAssignNode(pos, 0))

            self.register_instruction(label_loop)
            self.register_instruction(cil.CILGotoIfNode(vlength_r, label_loopbody))

            self.register_instruction(cil.CILGotoNode(label_equal))
            
            self.register_instruction(label_loopbody)
            cleft = self.define_internal_local()
            cright = self.define_internal_local()
            self.register_instruction(cil.CILGetIndexNode(cleft, vleft, pos))           
            self.register_instruction(cil.CILGetIndexNode(cright, vright, pos))
            self.register_instruction(cil.CILMinusNode(vlength_r, vlength_r, 1))
            self.register_instruction(cil.CILPlusNode(pos, pos, 1))
            
            vrest = self.define_internal_local()
            self.register_instruction(cil.CILMinusNode(vrest, cleft, cright))
            self.register_instruction(cil.CILGotoIfNode(vrest, label_notequal))

            self.register_instruction(cil.CILGotoNode(label_loop))          

            self.register_instruction(label_equal)
            self.register_instruction(cil.CILAssignNode(dest, 1))
            self.register_instruction(cil.CILGotoNode(label_end))            
            
            self.register_instruction(label_notequal)
            self.register_instruction(cil.CILAssignNode(dest, 0))
            self.register_instruction(label_end)

        else:
            rest = self.define_internal_local()
            self.register_instruction(cil.CILMinusNode(rest, vleft, vright))
            label_1 = self.build_label()
            label_2 = self.build_label()
            self.register_instruction(cil.CILGotoIfNode(rest, label_1))
            self.register_instruction(cil.CILAssignNode(dest, 1))
            self.register_instruction(cil.CILGotoNode(label_2))
            self.register_instruction(label_1)
            self.register_instruction(cil.CILAssignNode(dest, 0))
            self.register_instruction(label_2)

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode, dest):
        # print("------------visit node: IsVoid")  
        vlocal = self.define_internal_local()
        self.visit(node.expr, vlocal)
        v_box = self._ifboxing(vlocal, node.expr.typeName)
        # self.register_instruction(cil.CILMinusNode(dest, self.void, v_box))

        rest = self.define_internal_local()
        self.register_instruction(cil.CILMinusNode(rest, self.void, v_box))
        label_1 = self.build_label()
        label_2 = self.build_label()
        self.register_instruction(cil.CILGotoIfNode(rest, label_1))
        self.register_instruction(cil.CILAssignNode(dest, 1))
        self.register_instruction(cil.CILGotoNode(label_2))
        self.register_instruction(label_1)
        self.register_instruction(cil.CILAssignNode(dest, 0))
        self.register_instruction(label_2)

    @visitor.when(ast.NewStatementNode)
    def visit(self, node: ast.NewStatementNode, dest):
        # print("------------visit node: New")
        if node.newType == 'Int' or node.newType == 'Bool':
            self.register_instruction(cil.CILAssignNode(dest, 0))

        elif node.newType == 'String':
            msg = self.register_data("")
            var = self.define_internal_local()
            self.register_instruction(cil.CILLoadNode(var, msg))
            self.register_instruction(cil.CILAssignNode(dest, var))

        else:                
            self.register_instruction(cil.CILAllocateNode(dest, self.dottypes[node.newType].cinfo))
            self.register_instruction(cil.CILSaveState())
            self.register_instruction(cil.CILParamNode(dest))
            useless = self.define_internal_local()
            # v_type = self.define_internal_local()
            # self.register_instruction(cil.CILTypeOfNode(v_type, dest))
            fname = self.dottypes[node.newType].methods['ctor'].finfo.name
            self.register_instruction(cil.CILStaticCallNode(useless, fname))

    @visitor.when(ast.CaseStatementNode)
    def visit(self, node: ast.CaseStatementNode, dest):
        # print("------------visit node: Case")  
        vexpr = self.define_internal_local()
        self.visit(node.case0, vexpr)

        vbox = self._ifboxing(vexpr, node.case0.typeName)

        vhalt = self.define_internal_local()
        self.register_instruction(cil.CILMinusNode(vhalt, self.void, vbox))

        label1 = self.build_label()
        labelerror = self.build_label()
        labelend = self.build_label()

        self.register_instruction(cil.CILGotoIfNode(vhalt, label1))
        self.register_instruction(cil.CILGotoNode(labelerror))
        
        self.register_instruction(label1)

        texpr = self.define_internal_local()
        self.register_instruction(cil.CILTypeOfNode(texpr, vbox))

        expr_list = [self.visit(case) for case in node.exprList]

        label_init = self.build_label()
        self.register_instruction(label_init)

        label_error = self.build_label()

        for tlocal, label_expr, _, _ in expr_list:
            vinternal = self.define_internal_local()
            # self.register_instruction(cil.CILMinusNode(vinternal, tlocal, texpr))

            rest = self.define_internal_local()
            self.register_instruction(cil.CILMinusNode(rest, tlocal, texpr))
            label_1 = self.build_label()
            label_2 = self.build_label()
            self.register_instruction(cil.CILGotoIfNode(rest, label_1))
            self.register_instruction(cil.CILAssignNode(vinternal, 1))
            self.register_instruction(cil.CILGotoNode(label_2))
            self.register_instruction(label_1)
            self.register_instruction(cil.CILAssignNode(vinternal, 0))
            self.register_instruction(label_2)

            # self.register_instruction(cil.CILMinusNode(vinternal, 1, vinternal))
            self.register_instruction(cil.CILGotoIfNode(vinternal, label_expr))

        vobject = self.define_internal_local()
        self.register_instruction(cil.CILAllocateNode(vobject, self.dottypes['Object'].cinfo))
        self.register_instruction(cil.CILTypeOfNode(vobject, vobject))
        vo_comp = self.define_internal_local()
        # self.register_instruction(cil.CILMinusNode(vo_comp, vobject, texpr))

        rest = self.define_internal_local()
        self.register_instruction(cil.CILMinusNode(rest, vobject, texpr))
        label_1 = self.build_label()
        label_2 = self.build_label()
        self.register_instruction(cil.CILGotoIfNode(rest, label_1))
        self.register_instruction(cil.CILAssignNode(vo_comp, 1))
        self.register_instruction(cil.CILGotoNode(label_2))
        self.register_instruction(label_1)
        self.register_instruction(cil.CILAssignNode(vo_comp, 0))
        self.register_instruction(label_2)

        # self.register_instruction(cil.CILMinusNode(vo_comp, 1, vo_comp))
        self.register_instruction(cil.CILGotoIfNode(vo_comp, label_error))

        tparent = self.define_internal_local()
        self.register_instruction(cil.CILParentNode(tparent, texpr))
        self.register_instruction(cil.CILAssignNode(texpr, tparent))

        self.register_instruction(cil.CILGotoNode(label_init))

        label_end = self.build_label()
        for _, label_expr, expr, vinternalocal in expr_list:
            self.register_instruction(label_expr)
            self.register_instruction(cil.CILAssignNode(vinternalocal, vexpr))
            resp = self.define_internal_local()
            self.visit(expr, resp)
            self.register_instruction(cil.CILAssignNode(dest, resp))
            self.register_instruction(cil.CILGotoNode(label_end))

        self.register_instruction(label_error)
        # self.register_instruction(cil.CILPrintStrNode(var1))
        var2 = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var2, self.dotdata['exception_3']))
        self.register_instruction(cil.CILPrintStrNode(var2))
        self.register_instruction(cil.CILErrorNode())
        self.register_instruction(label_end)

        self.register_instruction(cil.CILGotoNode(labelend))

        self.register_instruction(labelerror)
        var1 = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_2']))
        self.register_instruction(cil.CILPrintStrNode(var1))
        self.register_instruction(cil.CILErrorNode())

        self.register_instruction(labelend)

    @visitor.when(ast.CaseBranchNode)
    def visit(self, node: ast.CaseBranchNode):
        # print("------------visit node: CaseExpr")  
        vlocal = node.decl.vinfo
        self.register_local(vlocal)

        ctype_ = vlocal.ctype
        self.register_instruction(cil.CILAllocateNode(vlocal, self.dottypes[ctype_].cinfo))
        # vbox = self._ifboxing(vlocal, vlocal.ctype)

        tlocal = self.define_internal_local()
        self.register_instruction(cil.CILTypeOfNode(tlocal, vlocal))

        label = self.build_label()
        return ((tlocal, label, node.expr, vlocal))


    @visitor.when(ast.FunctionCallStatement)
    def visit(self, node: ast.FunctionCallStatement, dest):
        if node.instance.lex == 'self':
            params = []
            method_ = self.dottypes[self.current_class.cinfo.name].methods[node.function].finfo
            vself = self._find('self')      

            vhalt = self.define_internal_local()
            self.register_instruction(cil.CILMinusNode(vhalt, self.void, vself))

            label1 = self.build_label()
            labelerror = self.build_label()
            labelend = self.build_label()

            self.register_instruction(cil.CILGotoIfNode(vhalt, label1))
            self.register_instruction(cil.CILGotoNode(labelerror))
            
            self.register_instruction(label1)

            for i, expr in enumerate(node.args):
                vlocal = self.define_internal_local()
                self.visit(expr, vlocal)
                p = method_.paramsType[i]

                v_box = self._ifobjectboxing(vlocal, expr.typeName, p)
                params.append(v_box)

            self.register_instruction(cil.CILSaveState())  

            self.register_instruction(cil.CILParamNode(vself))
            
            for p in params:
                self.register_instruction(cil.CILParamNode(p))

            self.register_instruction(cil.CILStaticCallNode(dest, method_.name))
            self.register_instruction(cil.CILGotoNode(labelend))

            self.register_instruction(labelerror)
            var1 = self.define_internal_local()
            self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_1']))
            self.register_instruction(cil.CILPrintStrNode(var1))
            self.register_instruction(cil.CILErrorNode())

            self.register_instruction(labelend)
        elif not node.dispatchType is None:
            params = []
            ctype_ = node.instance.typeName
            method_ = self.dottypes[ctype_].methods[node.function].finfo

            for i, expr in enumerate(node.args):
                vlocal = self.define_internal_local()
                self.visit(expr, vlocal)
                p = method_.paramsType[i]

                v_box = self._ifobjectboxing(vlocal, expr.typeName, p)
                params.append(v_box)

            v_eval = self.define_internal_local()
            self.visit(node.function, v_eval)

            v_box_eval = self._ifboxing(v_eval, node.typeName)

            vhalt = self.define_internal_local()
            self.register_instruction(cil.CILMinusNode(vhalt, self.void, v_box_eval))
            
            label1 = self.build_label()
            labelerror = self.build_label()
            labelend = self.build_label()

            self.register_instruction(cil.CILGotoIfNode(vhalt, label1))
            self.register_instruction(cil.CILGotoNode(labelerror))
            
            self.register_instruction(label1)

            v_type = self.define_internal_local()
            self.register_instruction(cil.CILTypeOfNode(v_type, v_box_eval))

            self.register_instruction(cil.CILSaveState())
            self.register_instruction(cil.CILParamNode(v_box_eval))
            for p in params:
                self.register_instruction(cil.CILParamNode(p))

            self.register_instruction(cil.CILDynamicCallNode(dest, v_type, method_.vmholder))
            self.register_instruction(cil.CILGotoNode(labelend))

            self.register_instruction(labelerror)
            var1 = self.define_internal_local()
            self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_1']))
            self.register_instruction(cil.CILPrintStrNode(var1))
            self.register_instruction(cil.CILErrorNode())

            self.register_instruction(labelend)
        else:
            params = []
            method_ = self.dottypes[node.typeName].methods[node.function].finfo

            for i, expr in enumerate(node.args):
                vlocal = self.define_internal_local()
                self.visit(expr, vlocal)
                p = method_.paramsType[i]

                v_box = self._ifobjectboxing(vlocal, expr.typeName, p)
                params.append(v_box)

            v_expr = self.define_internal_local()
            self.visit(node.instance, v_expr)

            v_box_eval = self._ifboxing(v_expr, node.instance.typeName)

            vhalt = self.define_internal_local()
            self.register_instruction(cil.CILMinusNode(vhalt, self.void, v_box_eval))
            
            label1 = self.build_label()
            labelerror = self.build_label()
            labelend = self.build_label()

            self.register_instruction(cil.CILGotoIfNode(vhalt, label1))
            self.register_instruction(cil.CILGotoNode(labelerror))
            
            self.register_instruction(label1)

            self.register_instruction(cil.CILSaveState())
            self.register_instruction(cil.CILParamNode(v_box_eval))
            
            for p in params:
                self.register_instruction(cil.CILParamNode(p))

            self.register_instruction(cil.CILStaticCallNode(dest, method_.name))
            self.register_instruction(cil.CILGotoNode(labelend))

            self.register_instruction(labelerror)
            var1 = self.define_internal_local()
            self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_1']))
            self.register_instruction(cil.CILPrintStrNode(var1))
            self.register_instruction(cil.CILErrorNode())

            self.register_instruction(labelend)

    # @visitor.when(ast.Void)
    # def visit(self, node: ast.Void, dest):
    #     # print("------------visit node: Void")  
    #     self.register_instruction(cil.CILAssignNode(dest, self.void))

    # ======================================================================

    def _find(self, name):
        for argument in self.arguments:
            if argument.vinfo.name == name:
                return argument.vinfo

        for cilLocalNode in self.localvars:
            if cilLocalNode.vinfo.name == name:
                return cilLocalNode.vinfo

        dest = self.define_internal_local()
        vself = self._find('self')
        # vtype = self.define_internal_local()
        # self.register_instruction(cil.CILTypeOfNode(vtype, vself))
        num = self.dottypes[self.current_class.cinfo.name].attrs[name].vmholder
        self.register_instruction(cil.CILGetAttribNode(dest, vself, num))
        return dest