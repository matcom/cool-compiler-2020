import sys
sys.path.append('/..')
from nodesIL import *
from virtual_table import VirtualTable
from variables import Variables
import visitor
from ..cl_ast import *

class codeVisitor:

    def __init__(self):
        #code IL
        self.code = []
        self.data = []

        self.count = 0
        self.current_class = 'Main'

        self.virtual_table = VirtualTable()

        self.depth = {}

    def getInt(self):
        self.count = self.count + 1
        return self.count 

    def collectTypes(self, classes):
        types = {'Object' : None, 'IO' : 'Object', 'Int' : 'Object', 'Bool' : 'Object', 'String' : 'Object'}
        methods = {'Object' : ['abort', 'type_name', 'copy'],'IO' : ['out_string', 'out_int', 'in_string', 'in_int'],'String' : ['length', 'concat', 'substr'],'Int' : [], 'Bool' : [] }
        
        attr = dict([ (x, []) for x in types ])

        for node in classes:
            types[node.idx.value] = node.parent.value

            for f in node.features:
                if type(f) == AttrDeclarationNode:
                    if not node.idx.value in attr:
                        attr[node.idx.value] = []
                    attr[node.idx.value].append(f.name.value)
                else:
                    if not node.idx.value in methods:
                        methods[node.idx.value] = []
                    methods[node.idx.value].append(f.name.value)
        
        for t in types.keys():
            nodes = [t]
            x = t

            while types[x] != None:
                x = types[x]
                nodes.append(x)
            
            nodes.reverse()

            for n in nodes:
                try:
                    self.virtual_table.add_method(t, n, methods[n])
                except:
                    pass

                try:
                    self.virtual_table.add_attr(t, attr[n])

        for t in types:
            slef.data.append(HierarchyIL(t, types[t]))

        for m in self.virtual_table.methods:
            self.data.append(VirtualTableIL(c, self.virtual_table.methods[m]))

        depth = dict([(x, len(types) + 2) for x in types])
        depth['Object'] = 0

        for _ in types:
            for c in types:
                if c == 'Object':
                    continue
                p = types[c]
                depth[c] = min(depth[c], depth[p] + 1)
        self.depth = depth

    def setInitialCode(self):
        self.code.append(CommentIL('--------------Initial Code---------------'))
        self.code.append(LabelIL("main", ""))
        
        self.append(PushIL())
        self.append(PushIL())
        self.append(PushIL())

        self.code.append(AllocateIL(1, self.vt.get_index('Main'), 'Main'))
        self.code.append(DispatchParentIL(2, 1, 'Main.Constructor'))

        self.code.append(DispatchIL(3,1,self.virtual_table.get_method_id('Main', 'main')))

        self.code.append(GotoIL("Object.abort"))

    def setBuiltInTypes(self):
        built_in = ['Object', 'IO', 'Bool', 'String']
        for t in built_in:
            self.code.append(LabelIL(t, 'Constructor', True))
            self.code.append(PushIL())
            self.append(ReturnIL())

    def setClassConstructor(self, attributes):
        self.code.append(LabelIL(self.current_class, 'Constructor', True))

        vars = Variables()
        vars.add_var('self')
        vars.add_temp()

        for node in attributes:
            if node.value == None:
                continue
            self.visit(node.value, vars)
            p = vars.peek_last()
            index = self.virtual_table.get_attributes_id(self.current_class, node.name.value)
            self.code.append(VarToMemoIL(vars.id('self'), vars.id(p), index)))

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
        res = variables.add_tmp()
        self.code.append(PushIL())

        self.visit(node.expr, variables)
        v = variables.peek_last()

        self.code.append(UnaryOperationIL(variables.id(res), variables.id(v), symbol))
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    #program
    @visitor.on(ProgramNode)
    def visit(self, node):
        self.visit(node.declarations)
    
    #declarations
    @visitor.on(ClassDeclarationNode)
    def visit(self, node):
        self.current_class = node.idx.value

        attributes = []
        for f in node.features:
            if type(f) == AttrDeclarationNode:
                attributes.append(f)
        
        self.setClassConstructor(attributes)

        for f in node.features:
            self.visit(f)

    @visitor.on(AttrDeclarationNode)
    def visit(self, node):
        pass

    @visitor.on(FuncDeclarationNode)
    def visit(self, node):
        self.code.append(LabelIL(self.current_class, node.idx, True))

        variables = Variables()
        variables.add_var('self')

        for p in node.params:
            variables.add_var(p.name)

        variables.add_temp()

        self.visit(node.body, variables)
        self.code.append(ReturnIL())

    @visitor.on(VarDeclarationNode)
    def visit(self, node):
        pass

    #operations: binary
    @visitor.on(SumNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '+')

    @visitor.on(DiffNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '-')

    @visitor.on(StarNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '*')

    @visitor.on(DivNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '/')

    @visitor.on(LessNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '<')

    @visitor.on(LessEqualNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '<=')

    @visitor.on(EqualNode)
    def visit(self, node, variables):
        self.handleBinaryOps(node, variables, '=')

    #operations: unary

    @visitor.on(BitNotNode)
    def visit(self, node, variables):
        self.handleUnaryOps(node, variables, '~')

    @visitor.on(NotNode)
    def visit(self, node, variables):
        self.handleUnaryOps(node, variables, '!')

    #expressions: atomics
    @visitor.on(VariableNode)
    def visit(self, node, variables):
        self.code.append(PushIL())
        result = variables.add_temp()

        if node.id.value in variables.variables:
            self.code.append(VarToVarIL(variables.id(result), variables.id(node.id.value)))
        else:
            self.code.append(MemoToVarIL(variables.id(result), variables.id('self'), self.virtual_table.get_attributes_id(self.current_class, node.id.value)))

    @visitor.on(NewNode)
    def visit(self, node, variables):
        result = variables.add_temp()
        self.code.append(PushIL())

        dispatch = variables.add_tmp()
        self.code.append(PushIL())

        self.code.append(PushIL())
        p = variables.add_tmp()

        size = self.virtual_table.get_index(node.type.value)
        self.code.append(AllocateIL(variables.id(p), size, node.type.value))

        self.code.append(VarToVarIL(variables.id(result), variables.id(p)))
        self.code.append(DispatchParentIL(variables.id(dispatch), variables.id(p), node.type.value + '.Constructor'))

        self.code.append(PopIL(2))
        variables.pop_var()
        variables.pop_var()

    #expressions: complex
    @visitor.on(ConditionalNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Condition'))
        result = variables.add_temp()
        self.code.append(PushIL())

        self.visit(node.cond, variables)
        p = variables.peek_last()

        IF = LabelIL('_if', self.getInt())
        FI = labelIL('_fi', IF.second)

        self.append(IfJumpIL(variables.id(p), IF.label))

        self.visit(node.else_stm, variables)
        ELSE = variables.peek_last()
        self.code.append(VarToVarIL(variables.id(result), variables.id(ELSE)))

        self.code.append(GotoIL(FI.label))

        self.code.append(IF)
        self.visit(node.stm, variables)
        _if = variables.peek_last()
        self.code.append(VarToVarIL(variables.id(result), variables.id(_if)))
        variables.pop_var()

        self.code.append(LabelIL('_fi'), IF.second)

        variables.pop_var()
        self.code.append(PopIL(2))
        

    @visitor.on(WhileNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('loop'))
        self.code.append(PushIL())
        
        result = variables.add_tmp()

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


    @visitor.on(LetNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Let'))
        self.code.append(PushIL())
        result = variables.add_temp()

        vars = variables.get_copy()

        for expr in node.init_list:
            self.visit(expr, vars)
            vars = vars.get_copy()

        self.visit(node.expr, vars)
        p = vars.peek_last()

        self.code.append(VarToVarIL(result, p))
        pop_times = len(node.expr) + 1

        self.code.append(PopIL(pop_times))



    @visitor.on(LetDeclarationNode)
    def visit(self, node):
        pass

    @visitor.on(BlockNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Block'))
        result = variables.add_temp()
        self.code.append(PushIL(0))
        for expr in node.expr_list:
            self.visit(expr, variables)
        
        p = variables.peek_last()
        self.code.append(VarToVarIL(variables.id(result), variables.id(p)))

        self.code.append(PopIL())
        for i in range(0, len(node.expr_list)):
            variables.pop_var()

    @visitor.on(CaseNode)
    def visit(self, node, variables):
        node.case_list.sort(key = lambda x : self.depth[x.type], reverse = True)

        result = variables.add_temp()
        self.code.append(PushIL())

        self.visit(node.expr, variables)
        p = variables.peek_last()

        labels = []
        for b in node.branches:
            labels.append(LabelIL('branch', self.getInt()))

        index = 0
        for b in node.branches:
            tmp = variables.add_temp()
            self.code.apppend(PushIL())

            self.code.append(InheritIL(variables.id(p), b.typex, variables.id(tmp)))
            
            self.code.append(IfJumpIL(variables.id(tmp), labels[i].label))
            self.code.append(PopIL(1))
            variables.pop_var()
            i += 1

        end_label = LabelIL('esac', self.getInt())
        i = 0
        for b in node.branches:
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

    @visitor.on(OptionNode)
    def visit(self, node):
        pass

    @visitor.on(AssignNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Assignment'))
        self.visit(node.expr, variables)
        p = variables.peek_last()
        
        if node.idx.value in variables.variables:
            self.code.append(VarToVarIL(variables.id(node.idx.value), variables.id(p)))
        else:
            self.code.append(VarToMemoIL(variables.id('self'), variables.id(p), self.virtual_table.get_attributes_id(self.current_class, node.idx.value)))

    @visitor.on(IsVoidNode)
    def visit(self, node):
        pass

    #expression: complex->dispatch
    @visitor.on(ExprCallNode)
    def visit(self, node):
        pass

    @visitor.on(SelfCallNode)
    def visit(self, node):
        pass

    @visitor.on(ParentCallNode)
    def visit(self, node):
        pass

    #constants
    @visitor.on(IntegerNode)
    def visit(self, node, variables):
        self.code.append(CommentIL('Integer'))
        variables.add_temp()
        self.code.append(PushIL(int(self.lex))

    @visitor.on(StringNode)
    def visit(self, node, variables):
        label = 'string_' + str(self.getInt())
        self.data.append(StringIL(label, node.lex))
        self.code.append(CommentIL('loading label'))
        self.code.append(PushIL())
        p = variables.add_tmp()

        self.code.append(LoadLabelIL(variables.id(p), label))

    @visitor.on(BoolNode)
    def visit(self, node):
        variables.add_tmp()
        if node.lex:
            self.code.append(PushIL(1))
        else:
            self.code.append(PushIL(0))


    




