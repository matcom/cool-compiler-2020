import sys
sys.path.append('/..')
from code_generation import *
import visitors.visitor as visitor
from cl_ast import *

class codeVisitor:

    def __init__(self, context):
        #code IL
        self.code = []
        self.data = []

        self.count = 0
        self.current_class = 'Main'

        self.virtual_table = VirtualTable()

        self.depth = {}

        self.collectTypes(context)
        self.setBuiltInTypes()
        # self.setClassConstructor()
        self.setInitialCode()

    def getInt(self):
        self.count = self.count + 1
        return self.count 

    def collectTypes(self, context):
        # print('collecting types')
        types = {}
        methods = {}
        attr = {}

        for t in context.types:
            t_str = str(t)
            # print('----------------Typessssss-------------------------')
            # print(t_str)
            if context.types[t].parent is not None:
                types[t_str] = context.types[t].parent
            methods[t_str] = []
            attr[t_str] = context.types[t].attributes
            if len(context.types[t].attributes):
                for atr in context.types[t].attributes:
                    self.virtual_table.add_attr(t_str, atr)
            # else:
            #     self.virtual_table.add_method(t_str, '-', [])
            for m in context.types[t].methods.keys():
                methods[t_str] = (context.types[t].methods[m])
                # print("class {} method_name {} params {}".format(t_str,(context.types[t].methods[m]).name, (context.types[t].methods[m]).param_names))
                self.virtual_table.add_method(t_str, (context.types[t].methods[m]).name, (context.types[t].methods[m]).param_names)
        # print(str(self.virtual_table))
        # print('-------------------------------')
        for t in types:
            self.data.append(HierarchyIL(t, types[t].name))

        for m in self.virtual_table.methods.keys():
            self.data.append(VirtualTableIL(m, self.virtual_table.methods[m]))
        depth = dict([(types[x].name, len(types) + 2) for x in types])
        depth['Object'] = 0
        # TODO set some depth features for simplicity
        # for _ in types:
        #     for c in types:
        #         if c is None:
        #             continue
        #         p = types[c]
        #         depth[c.name] = min(depth[c.name], depth[p] + 1)
        # self.depth = depth

    def setInitialCode(self):
        self.code.append(CommentIL('--------------Initial Code---------------'))
        self.code.append(LabelIL("main", ""))
        
        # self.code.append(CustomLineIL("sub $a0, $a0, $a0\n"))
        # self.code.append(CustomLineIL("sub $a1, $a1, $a1\n"))
        # self.code.append(CustomLineIL("sub $a2, $a2, $a2\n"))
        # self.code.append(CustomLineIL("sub $a3, $a3, $a3\n"))

        self.code.append(PushIL())
        self.code.append(PushIL())
        self.code.append(PushIL())

        self.code.append(AllocateIL(1, self.virtual_table.get_index('Main'), 'Main'))
        self.code.append(DispatchParentIL(2, 1, 'Main.Constructor'))

        self.code.append(DispatchIL(3,1,self.virtual_table.get_method_id('Main', 'main')))

        self.code.append(GotoIL("Object.abort"))
        self.code.append(CommentIL('--------------End Initial Code---------------'))

    def setBuiltInTypes(self):
        built_in = ['Object','Int', 'IO', 'Bool', 'String']
        for t in built_in:
            self.code.append(LabelIL(t, 'Constructor', True))
            self.code.append(PushIL())
            self.code.append(ReturnIL())

    def setClassConstructor(self, attributes):
        self.code.append(LabelIL(self.current_class, 'Constructor', True))

        vars = Variables()
        vars.add_var('self')
        vars.add_temp()

        for node in attributes:
            if node.expr == None:
                continue
            self.visit(node.expr, vars)
            p = vars.peek_last()
            index = self.virtual_table.get_attributes_id(self.current_class, node.id)
            self.code.append(VarToMemoIL(vars.id('self'), vars.id(p), index))

        self.code.append(PushIL())
        self.code.append(ReturnIL())


    def handleBinaryOps(self, node, variables, symbol):
        self.code.append(CommentIL('Binary'))
        self.code.append(PushIL())
        res = variables.add_temp()

        self.visit(node.left, variables)
        left = variables.peek_last()
        self.visit(node.right, variables)
        right = variables.peek_last()

        self.code.append(BinaryOperationIL(variables.id(res), variables.id(left), variables.id(right), symbol))

        variables.pop_var()
        variables.pop_var()
        self.code.append(PopIL(2))

    def handleUnaryOps(self, node, variables, symbol):
        self.code.append(CommentIL('Unary'))
        res = variables.add_temp()
        self.code.append(PushIL())

        self.visit(node.expr, variables)
        v = variables.peek_last()

        self.code.append(UnaryOperationIL(variables.id(res), variables.id(v), symbol))
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    #program
    @visitor.when(ProgramNode)
    def visit(self, node):
        # print('ProgramNode')
        for n in node.declarations:
            self.visit(n)
    
    #declarations
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        # print('ClassDeclarationNode')
        self.current_class = node.id
        # print('--current_class {}\n'.format(node.id))
        attributes = []
        for f in node.features:
            if type(f) == AttrDeclarationNode:
                attributes.append(f)
        
        self.setClassConstructor(attributes)

        for f in node.features:
            self.visit(f)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        pass

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        self.code.append(LabelIL(self.current_class, node.id, True))

        variables = Variables()
        variables.add_var('self')

        for p in node.params:
            variables.add_var(p.id)

        variables.add_temp()

        self.visit(node.body, variables)
        self.code.append(ReturnIL())

    @visitor.when(VarDeclarationNode)
    def visit(self, node, variables):
        self.code.append(PushIL())
        p = variables.add_var(node.idx)

        if node.expr != None:
            self.visit(node.expr, variables)
            res = variables.peek_last()
            self.code.append(VarToVarIL(variables.id(p), variables.id(res)))
            variables.pop_var()
            self.code.append(PopIL())

    #operations: binary
    @visitor.when(SumNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '+')

    @visitor.when(DiffNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '-')

    @visitor.when(StarNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '*')

    @visitor.when(DivNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '/')

    @visitor.when(LessNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '<')

    @visitor.when(LessEqualNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '<=')

    @visitor.when(EqualNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '=')

    #operations: unary

    @visitor.when(BitNotNode)
    def visit(self, node, variables):
        self.handleUnaryOps(node, variables, '~')

    @visitor.when(NotNode)
    def visit(self, node, variables):
        self.handleUnaryOps(node, variables, '!')

    #expressions: atomics
    @visitor.when(VariableNode)
    def visit(self, node, variables):
        self.code.append(PushIL())
        result = variables.add_temp()
        # print(node.id)
        if node.id in variables.stack:
            self.code.append(VarToVarIL(variables.id(result), variables.id(node.id)))
        else:
            self.code.append(MemoToVarIL(variables.id(result), variables.id('self'), self.virtual_table.get_attributes_id(self.current_class, node.id)))

    @visitor.when(NewNode)
    def visit(self, node, variables):
        result = variables.add_temp()
        self.code.append(PushIL())

        dispatch = variables.add_temp()
        self.code.append(PushIL())

        self.code.append(PushIL())
        p = variables.add_temp()

        size = self.virtual_table.get_index(node.type)
        self.code.append(AllocateIL(variables.id(p), size, node.type))

        self.code.append(VarToVarIL(variables.id(result), variables.id(p)))
        self.code.append(DispatchParentIL(variables.id(dispatch), variables.id(p), node.type + '.Constructor'))

        self.code.append(PopIL(2))
        variables.pop_var()
        variables.pop_var()

    #expressions: complex
    @visitor.when(ConditionalNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Condition'))
        result = variables.add_temp()
        self.code.append(PushIL())

        self.visit(node.cond, variables)
        p = variables.peek_last()

        IF = LabelIL('_if', self.getInt())
        FI = LabelIL('_fi', IF.second)

        self.code.append(IfJumpIL(variables.id(p), IF.label))

        self.visit(node.else_stm, variables)
        ELSE = variables.peek_last()
        self.code.append(VarToVarIL(variables.id(result), variables.id(ELSE)))

        self.code.append(GotoIL(FI.label))

        self.code.append(IF)
        self.visit(node.stm, variables)
        _if = variables.peek_last()
        self.code.append(VarToVarIL(variables.id(result), variables.id(_if)))
        variables.pop_var()

        self.code.append(LabelIL('_fi', IF.second))

        variables.pop_var()
        self.code.append(PopIL(2))
        

    @visitor.when(WhileNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('loop'))
        self.code.append(PushIL())
        
        result = variables.add_temp()

        LOOP = LabelIL('_loop', self.getInt())
        POOL = LabelIL('_pool', LOOP.second)
        BODY = LabelIL('_body', LOOP.second)

        self.code.append(LOOP)

        self.visit(node.cond, variables)
        p = variables.peek_last()

        self.code.append(IfJumpIL(variables.id(p), BODY.label))

        self.code.append(GotoIL(POOL.label))

        self.code.append(BODY)
        self.visit(node.expr, variables)
        variables.pop_var()
        variables.pop_var()
        self.code.append(PopIL(2))
        self.code.append(GotoIL(LOOP.label))
        
        self.code.append(POOL)


    @visitor.when(LetNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Let'))
        self.code.append(PushIL())
        result = variables.add_temp()
        result1 = variables.add_temp()
        vars = variables.get_copy()

        for expr in node.init_list:
            self.visit(expr, vars)
            vars = vars.get_copy()

        self.visit(node.expr, vars)
        p = vars.peek_last()

        self.code.append(VarToVarIL(result, p))
        pop_times = 2
        try:
            pop_times = len(node.expr) + 1
        except:
            pass

        self.code.append(PopIL(pop_times))



    @visitor.when(LetDeclarationNode)
    def visit(self, node, variables):
        pass

    @visitor.when(BlockNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Block'))
        result = variables.add_temp()
        self.code.append(PushIL(0))
        for expr in node.expr_list:
            self.visit(expr, variables)
        
        p = variables.peek_last()
        self.code.append(VarToVarIL(variables.id(result), variables.id(p)))

        self.code.append(PopIL(len(node.expr_list)))
        for i in range(len(node.expr_list)):
            variables.pop_var()

    @visitor.when(CaseNode)
    def visit(self, node, variables):
        # print(node.case_list)
        # node.case_list.sort(key = lambda x : self.depth[x.typex], reverse = True)

        result = variables.add_temp()
        self.code.append(PushIL())

        self.visit(node.expr, variables)
        p = variables.peek_last()

        labels = []
        for b in node.case_list:
            labels.append(LabelIL('branch', self.getInt()))

        index = 0
        for b in node.case_list:
            tmp = variables.add_temp()
            self.code.append(PushIL())

            self.code.append(InheritIL(variables.id(p), b.typex, variables.id(tmp)))
            
            self.code.append(IfJumpIL(variables.id(tmp), labels[index].label))
            self.code.append(PopIL(1))
            variables.pop_var()
            index += 1

        end_label = LabelIL('esac', self.getInt())
        i = 0
        for b in node.case_list:
            self.code.append(labels[i])
            i += 1
            variables.pop_var()
            self.code.append(PopIL(1))

            self.code.append(PushIL())
            result = variables.add_var(b.id)
            self.code.append(VarToVarIL(variables.id(result), variables.id(p)))

            self.visit(b.expr, variables)
            m = variables.peek_last()

            self.code.append(VarToVarIL(variables.id(result), variables.id(m)))
            
            variables.pop_var()
            variables.pop_var()
            variables.pop_var()

            self.code.append(PopIL(3))

    @visitor.when(OptionNode)
    def visit(self, node, variables):
        pass

    @visitor.when(AssignNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Assignment'))
        self.visit(node.expr, variables)
        p = variables.peek_last()
        
        if node.id in variables.stack:
            self.code.append(VarToVarIL(variables.id(node.id), variables.id(p)))
        else:
            self.code.append(VarToMemoIL(variables.id('self'), variables.id(p), self.virtual_table.get_attributes_id(self.current_class, node.id)))

    @visitor.when(IsVoidNode)
    def visit(self, node, vars):
        pass

    #expression: complex->dispatch
    @visitor.when(ExprCallNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Point-Dispatch'))

        result = variables.add_temp()
        self.code.append(PushIL())
        # print('----------node {}---------'.format(node))
        index = self.virtual_table.get_method_id(node.obj, node.id)

        self.code.append(CommentIL('push object'))
        # print('-------obj-------- ',node.obj)
        self.visit(node.obj, variables)

        name = variables.peek_last()

        i = 0
        for p in node.args:
            self.code.append(CommentIL('Args: ' + str(i)))
            i += 1
            self.visit(p, variables)
        
        self.code.append(DispatchIL(variables.id(result), variables.id(name), index))

        for i in range(0, len(node.args) + 1):
            variables.pop_var()

        self.code.append(PopIL(len(node.args) + 1))

    @visitor.when(SelfCallNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Self-Dispatch'))

        result = variables.add_temp()
        self.code.append(PushIL())
        # print('----------node {}---------'.format(node))
        index = self.virtual_table.get_method_id(self.current_class, node.id)

        if self.current_class != 'Main':
            self.code.append(CommentIL('push self'))
            s = variables.add_temp()
            self.code.append(PushIL())
            self.code.append(VarToVarIL(variables.id(s), variables.id('self')))
        
        i = 0
        for p in node.args:
            self.code.append(CommentIL('Args: ' + str(i)))
            i += 1
            self.visit(p, variables)
        self.code.append(DispatchIL(variables.id(result), variables.id('self'), index))

        n = 0
        if self.current_class == 'Main':
            n = 1

        for i in range(len(node.args) + n):
            variables.pop_var()
        
        self.code.append(PopIL(len(node.args) + n))

    @visitor.when(ParentCallNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Parent-Dispatch'))

        result = variables.add_temp()
        self.code.append(PushIL())

        self.code.append('push object')
        self.visit(node.obj, variables)
        name = variables.peek_last()

        i = 0
        for p in node.args:
            self.code.append(CommentIL('Args: ' + str(i)))
            i += 1
            self.visit(p, variables)
        
        method = node.id + '.' + node.obj.id
        
        self.code.append(DispatchParentIL(variables.id(result), variables.id(name), method))

        for i in range((len(node.args) + 1)):
            variables.pop_var()
        self.code.append(PopIL(len(node.args) + 1))


    #constants
    @visitor.when(IntegerNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Integer'))
        variables.add_temp()
        self.code.append(PushIL(int(node.lex)))

    @visitor.when(StringNode)
    def visit(self, node, variables):
        label = 'string_' + str(self.getInt())
        self.data.append(StringIL(label, node.lex))
        self.code.append(CommentIL('loading label'))
        self.code.append(PushIL())
        p = variables.add_temp()

        self.code.append(LoadLabelIL(variables.id(p), label))

    @visitor.when(BoolNode)
    def visit(self, node, variables):
        variables.add_temp()
        if node.lex:
            self.code.append(PushIL(1))
        else:
            self.code.append(PushIL(0))


    




