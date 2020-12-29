import visitor as visitor
from AST import *
import tools


class Semantic:
    def __init__(self):
        self.error = []
        #classes
        self.classmethods = {}
        self.classmethods['Object'] = {
            'abort':    ([],'Object'),
            'type_name':([],'String'),
            'copy':     ([],'SELF_TYPE')}
        self.classmethods['IO'] = {
            'out_string': ([('x','String')] , 'SELF_TYPE'),
            'out_int':    ([('x','Int')] , 'SELF_TYPE'),
            'in_string':  ([], 'String'),
            'in_int':     ([], 'Int')}
        self.classmethods['Int'] = {}
        self.classmethods['String'] = {
            'length': ([], 'Int'),
            'concat': ([('s','String')], 'String'),
            'substr': ([('i','Int'), ('l','Int')], 'String')}
        self.classmethods['Bool'] = {}
        self.classmethods_original = {}
        self.class_attrs = {'Object':[], 'IO':[], 'Int':[], 'String':[], 'Bool':[]}
        self.graph = {}
        self.local_variables = [('self', 'SELF_TYPE')]
        self.current_class = None
        self.current_method = None
        self.class_parent = {'Int':'Object', 'String':'Object', 'Bool':'Object', 'IO':'Object'}
        self.conforms = {
            'Object':set(['Object']),
            'Int':set(['Object','Int']),
            'String':set(['Object','String']),
            'IO':set(['Object','IO']),
            'Bool':set(['Object','Bool'])}
        #conforms to

    def lca(self, type1, type2):
        temp = type1
        parents = set([temp])
        while temp != 'Object':
            temp =  self.class_parent[temp]
            parents.add(temp)

        temp = type2
        while not parents.__contains__(temp):
            temp = self.class_parent[temp]

        return temp

    def check_eq(self, method1, method2):
        args1 = method1[0]
        return_type1 = method1[1]

        args2 = method2[0]
        return_type2 = method2[1]

        if return_type1 != return_type2 or len(args1) != len(args2):
            return False

        n = len(args1)
        for i in range(n):
            if args1[i][1] != args2[i][1]:
                return False
        return True

    def ComputeInheritsfeature(self, program):
        l = ['Object']
        while len(l) > 0:
            temp = l[0]
            l.pop(0)
            if not self.graph.__contains__(temp):
                continue
            for c in self.graph[temp]:
                last = len(self.class_attrs[temp]) - 1
                for i in range(last, -1, -1):
                    self.class_attrs[c].insert(0, self.class_attrs[temp][i])

                self.conforms[c].update(self.conforms[temp])
                l.append(c)
                for m in self.classmethods[temp].items():
                    if not self.classmethods[c].__contains__(m[0]):
                        # SI NO CONTIENE EL METODO, LO AGREGO A LA CLASE
                        self.classmethods[c][m[0]] = m[1]
                    elif not self.check_eq(m[1], self.classmethods[c][m[0]]):
                        for _class in program.classes:
                            if _class.name == c:
                                for _method in _class.methods:
                                    if _method.id == m[0]:
                                        self.error.append('({}, {}) - SemanticError: the types of the formal parameters, and the return type are not exactly the same in both definitions.'.format(_method.line, _method.index))
                                        return False
        return True


    '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
    # @visitor.on('node')
    # def visit(self, node):
    #     pass

    @visitor.when(Program)
    def visit(self, program):
        '''Classes defined only once'''
        for c in program.classes:
            if not self.classmethods.__contains__(c.name):
                self.classmethods[c.name] = {}
                self.conforms[c.name] = set([c.name])
            else:
                self.error.append('({}, {}) - SemanticError: Classes may not be redefined.'.format(c.line, c.index))
                return False
            self.class_attrs[c.name] = c.attributes
            for m in c.methods:
                if self.classmethods[c.name].__contains__(m.id):
                    self.error.append('({}, {}) - SemanticError: Method {} is multiply defined.'.format(m.line, m.index, m.id))
                    return False
                params = [(v.id, v.type) for v in m.parameters]
                self.classmethods[c.name][m.id] = (params, m.return_type)

        if not self.classmethods.__contains__('Main'):
            #print('Every program must have a class Main')
            return False

        '''Inheritance relationships'''
        classes = self.classmethods.keys()
        self.graph['Object'] = ['Int', 'String', 'Bool', 'IO']
        for c in program.classes:
            if c.inherit is None:
                self.graph['Object'].append(c.name)
                self.conforms[c.name].add('Object')
                self.class_parent[c.name] = 'Object'
            elif not self.classmethods.__contains__(c.inherit.name):
                self.error.append('({}, {}) - TypeError: Class {} inherits from an undefined class {}.'.format(c.line, c.index, c.name, c.inherit.name))
                return False
            elif c.inherit.name == 'Int' or c.inherit.name =='String' or c.inherit.name =='Bool' or c.inherit.name =='Object':
                self.error.append('({}, {}) - SemanticError: Class {} cannot inherit class {}.'.format(c.line, c.index, c.name, c.inherit.name))
                return False
            else:
                if self.graph.__contains__(c.inherit.name):
                    self.graph[c.inherit.name].append(c.name)   #c.name is a child class of c.inherit
                else: self.graph[c.inherit.name] = [c.name]
                self.class_parent[c.name] = c.inherit.name
                self.conforms[c.name].add(c.inherit.name)
            if tools.dfs(self.graph, classes):#si hay ciclo
                self.error.append('({}, {}) - SemanticError: Class {}, or an ancestor of {}, is involved in an inheritance cycle.'.format(c.line, c.index, c.name, c.name))
                return False

        self.classmethods_original.update(self.classmethods)
        if not self.ComputeInheritsfeature(program):
            return False

        for _cl in classes:
            for _item in self.classmethods[_cl].items():
                if _item[1][1] == 'SELF_TYPE':
                    _new = (_item[1][0],_cl)
                    self.classmethods[_cl][_item[0]] = _new

        for c in program.classes:
            if not self.graph.__contains__(c.name):
                atr_id = set([x.id for x in self.class_attrs[c.name]])
                if len(atr_id) < len(self.class_attrs[c.name]):
                    _redefinedID = set([])
                    for item in self.class_attrs[c.name]:
                        if _redefinedID.__contains__(item.id):
                            self.error.append('({}, {}) - SemanticError: Attribute redef.'.format(item.line, item.index))
                            return False
                        else: _redefinedID.add(item.id)

        for _item in self.class_attrs.items():
            n = len(_item[1])
            for i in range(n):
                if _item[1][i].type == 'SELF_TYPE':
                    _item[1][i].type = _item[0]

        '''visito las clases'''
        for c in program.classes:
            if not self.visit(c):
                return False
        return True

    @visitor.when(Class)
    def visit(self, _class):

        if _class.name == 'Main':
            if not self.classmethods[_class.name].__contains__('main'):
                #print('error: Main class must have a method main')
                return False
            elif len(self.classmethods['Main']['main'][0]) > 0:
                #print('error: main takes no formal parameters')
                return False

        self.current_class = _class.name

        for m in _class.methods:
            if not self.visit(m):
                return False

        #importante
        for atr in _class.attributes:
            if not self.visit(atr):
                return False

        self.current_class = None
        return True

    @visitor.when(Method)
    def visit(self, method):

        for formal in method.parameters:
            if not self.visit(formal):
                return False

        args = method.parameters
        if not method.parameters is None:
            args_id = set([arg.id for arg in args])
            if len(args_id) < len(args):
                self.error.append('({}, {}) - SemanticError: The identifiers used in the formal parameter list must be distinct.'.format(method.line, method.index))
                return False

        self.current_method = method.id
        if not self.visit(method.expression):
            return False

        self.local_variables.clear()
        self.local_variables.append(('self','SELF_TYPE'))
        self.current_method = None
        _returnType = method.return_type if method.return_type != 'SELF_TYPE' else self.current_class
        if not self.conforms[method.expression.static_type].__contains__(_returnType): 
            self.error.append('({}, {}) - TypeError: Inferred return type {} of method {} does not conform to declared return type {}.'.format(method.line, method.expression.index, method.expression.static_type, method.id, _returnType))
            return False
        return True



    @visitor.when(Block)
    def visit(self, block):

        for e in block.expressions:
            if not self.visit(e):
                return False

        n = len(block.expressions) - 1
        block.static_type = block.expressions[n].static_type
        return True



    @visitor.when(Star)
    def visit(self, star):
        if not self.visit(star.first):
            return False
        if not self.visit(star.second):
            return False
        if star.first.static_type != "Int" or star.second.static_type != "Int":
            self.error.append('({}, {}) - TypeError: non-Int arguments: {} * {}'.format(star.line, star.index,star.first.static_type,star.second.static_type))
            return False
        star.static_type = 'Int'
        return True

    @visitor.when(Plus)
    def visit(self, plus):
        if not self.visit(plus.first):
            return False
        if not self.visit(plus.second):
            return False
        if plus.first.static_type != "Int" or plus.second.static_type != "Int":
            self.error.append('({}, {}) - TypeError: non-Int arguments: {} + {}'.format(plus.line, plus.index, plus.first.static_type, plus.second.static_type))
            return False
        plus.static_type = 'Int'
        return True

    @visitor.when(Minus)
    def visit(self, minus):
        if not self.visit(minus.first):
            return False
        if not self.visit(minus.second):
            return False
        if minus.first.static_type != "Int" or minus.second.static_type != "Int":
            self.error.append('({}, {}) - TypeError: non-Int arguments: {} - {}'.format(minus.line, minus.index,minus.first.static_type, minus.second.static_type))
            return False
        minus.static_type = 'Int'
        return True

    @visitor.when(Div)
    def visit(self, div):
        if not self.visit(div.first):
            return False
        if not self.visit(div.second):
            return False
        if div.first.static_type != "Int" or div.second.static_type != "Int":
            self.error.append('({}, {}) - TypeError: non-Int arguments: {} / {}'.format(div.line, div.index, div.first.static_type, div.second.static_type))
            return False
        div.static_type = 'Int'
        return True





    @visitor.when(LowerEqualThan)
    def visit(self, lowerEqualThan):
        if not self.visit(lowerEqualThan.first):
            return False

        if not self.visit(lowerEqualThan.second):
            return False

        if lowerEqualThan.first.static_type != "Int" or lowerEqualThan.second.static_type != "Int":
            self.error.append('({}, {}) - TypeError: non-Int arguments: {} <= {}'.format(lowerEqualThan.line, lowerEqualThan.index,lowerEqualThan.first.static_type,lowerEqualThan.second.static_type))
            return False

        lowerEqualThan.static_type = 'Bool'
        return True

    @visitor.when(EqualThan)
    def visit(self, equalThan):
        if not self.visit(equalThan.first):
            return False

        if not self.visit(equalThan.second):
            return False

        if equalThan.first.static_type == 'Int' or equalThan.first.static_type == 'String' or equalThan.first.static_type == 'Bool':
            if equalThan.first.static_type != equalThan.second.static_type:
                self.error.append('({}, {}) - TypeError: Illegal comparison with a basic type.'.format(equalThan.line, equalThan.index))
                return False

        equalThan.static_type = 'Bool'
        return True

    @visitor.when(LowerThan)
    def visit(self, lowerThan):
        if not self.visit(lowerThan.first):
            return False
        if not self.visit(lowerThan.second):
            return False
        if lowerThan.first.static_type != 'Int' or lowerThan.second.static_type != 'Int':
            self.error.append('({}, {}) - TypeError: non-Int arguments: {} < {}'.format(lowerThan.line, lowerThan.index,lowerThan.first.static_type,lowerThan.second.static_type))
            return False

        lowerThan.static_type = 'Bool'
        return True



    @visitor.when(Not)
    def visit(self, negation):
        if not self.visit(negation.expr):
            return False

        if negation.expr.static_type != 'Bool':
            self.error.append("({}, {}) - TypeError: Argument of 'not' has type {} instead of Bool.".format(negation.line, negation.index, negation.expr.static_type))
            return False

        negation.static_type = 'Bool'
        return True

    @visitor.when(IntegerComplement)
    def visit(self, I_complement):

        if not self.visit(I_complement.expression):
            return False

        if I_complement.expression.static_type != "Int":
            self.error.append("({}, {}) - TypeError: Argument of '~' has type {} instead of Int.".format(I_complement.line, I_complement.index, I_complement.expression.static_type))
            return False

        I_complement.static_type = 'Int'
        return True


    @visitor.when(IsVoid)
    def visit(self, is_void):

        if not self.visit(is_void.expression):
            return False

        is_void.static_type = 'Bool'
        return True






    @visitor.when(Type)
    def visit(self, _type):
        #expr --> ID

        #verificar si esta declarado
        if _type.name == 'self':
            _type.static_type = self.current_class
            return True
        else:
            n = len(self.local_variables) - 1
            for i in range(n, -1, -1):
                local_id, local_type =  self.local_variables[i]
                if local_id == _type.name:
                    _type.static_type = local_type
                    return True

            if not self.current_method is None:
                for args_id,args_type in self.classmethods[self.current_class][self.current_method][0]:
                    if args_id == _type.name:
                        _type.static_type = args_type
                        return True

            for _var in self.class_attrs[self.current_class]:
                attr_id = _var.id
                attr_type = _var.type
                if attr_id == _type.name:
                    _type.static_type = attr_type
                    return True

        #print("error: tipo no declarado")
        self.error.append('({}, {}) - NameError: Undeclared identifier {}.'.format(_type.line, _type.index, _type.name))
        return False


    @visitor.when(NewType)
    def visit(self, new_type):
        if new_type.type_name == 'SELF_TYPE':
            new_type.static_type = self.current_class
        else:
            if not self.classmethods.__contains__(new_type.type_name):
                self.error.append("({}, {}) - TypeError: 'new' used with undefined class {}.".format(new_type.line, new_type.index, new_type.type_name))
                return False
            new_type.static_type = new_type.type_name
        return True


    @visitor.when(Boolean)
    def visit(self, boolean):
        boolean.static_type = 'Bool'
        return True

    @visitor.when(Interger)
    def visit(self, interger):
        interger.static_type = 'Int'
        return True

    @visitor.when(String)
    def visit(self, string):
        string.static_type = 'String'
        return True



    @visitor.when(Conditional)
    def visit(self, cond):
        if not self.visit(cond.if_expression):
            return False
        if not self.visit(cond.then_expression):
            return False
        if not self.visit(cond.else_expression):
            return False

        if cond.if_expression.static_type != 'Bool':
            self.error.append("({}, {}) - TypeError: Predicate of 'if' does not have type Bool.".format(cond.line, cond.index))
            return False

        thenType = cond.then_expression.static_type
        elseType = cond.else_expression.static_type

        cond.static_type = self.lca(thenType, elseType)
        return True

    @visitor.when(Loop)
    def visit(self, loop):

        if not self.visit(loop.while_expression):
            return False

        if not self.visit(loop.loop_expression):
            return False

        if loop.while_expression.static_type != 'Bool':
            self.error.append('({}, {}) - TypeError: Loop condition does not have type Bool.'.format(loop.line, loop.index))
            return False

        loop.static_type = 'Object'

        return True



    @visitor.when(LetVar)
    def visit(self, let):

        for item in let.declarations:
            if not self.visit(item):
                return False
            self.local_variables.append((item.id, item.static_type))

            # if item.expr is None:
            #     local_variables.append((item.id,item.type))
            # else:
            #     if not visit(item.expr):
            #         return False
            #local_variables.append((item.id,item.type))

        if not self.visit(let.in_expression):
            return False

        n = len(let.declarations)
        m = len(self.local_variables)

        for i in range(n):
            self.local_variables.pop(m - i - 1)

        let.static_type = let.in_expression.static_type

        return True



    @visitor.when(Assign)
    def visit(self, assign):

        if not self.visit(assign.expression):
            return False

        id_declared = False
        id_type = None

        #verificar si esta declarado
        if assign.id == 'self':
            self.error.append("({}, {}) - SemanticError: Cannot assign to 'self'.".format(assign.line, assign.index))
            return False
        else:
            n = len(self.local_variables) - 1
            for i in range(n, -1, -1):
                local_id, local_type =  self.local_variables[i]
                if local_id == assign.id:
                    id_declared = True
                    id_type = local_type
                    break
            if not id_declared:
                if not self.current_method is None:
                    for args_id, args_type in self.classmethods[self.current_class][self.current_method][0]:
                        if args_id == assign.id:
                            id_declared = True
                            id_type = args_type
                            break
            if not id_declared: 
                for _var in self.class_attrs[self.current_class]:
                    attr_id = _var.id
                    attr_type = _var.type
                    if attr_id == assign.id:
                        id_declared = True
                        id_type = attr_type
                        break

        if not id_declared:
            #print('error: variable no declarada')
            return False

        if not self.conforms[assign.expression.static_type].__contains__(id_type):
            #print('error: el tipo de la variable no se corresponde con el de la expression')
            return False

        assign.static_type = assign.expression.static_type
        return True




    @visitor.when(Attribute)
    def visit(self, attr):

        if attr.id == 'self':
            self.error.append('({}, {}) - SemanticError: is an error to assign to self or to bind self in a let, a case, or as a formal parameter. It is also illegal to have attributes named self.'.format(attr.line, attr.index))
            return False

        if not self.classmethods.__contains__(attr.type):
            self.error.append('({}, {}) - TypeError: Class {} of declaration of {} is undefined.'.format(attr.line, attr.index, attr.type, attr.id))
            return False
        if not self.visit(attr.expr):
            return False
        if not self.conforms[attr.expr.static_type].__contains__(attr.type):
            self.error.append('({}, {}) - TypeError: Inferred type {} of initialization of {} does not conform to declared type {}.'.format(attr.line, attr.index, attr.expr.static_type, attr.id, attr.type))
            return False

        attr.static_type = attr.type
        return True

    @visitor.when(Var)
    def visit(self, var):

        if var.id == 'self':
            self.error.append('({}, {}) - SemanticError: is an error to assign to self or to bind self in a let, a case, or as a formal parameter. It is also illegal to have attributes named self.'.format(var.line, var.index))
            return False

        if not self.classmethods.__contains__(var.type):
            self.error.append('({}, {}) - TypeError: Class {} of declaration of {} is undefined.'.format(var.line, var.index, var.type, var.id))
            return False

        var.static_type = var.type
        return True


    @visitor.when(Dispatch)
    def visit(self, dispatch):
        paramsTypes = []
        if not dispatch.parameters is None:
            for e in dispatch.parameters:
                if not self.visit(e):
                    return False
                paramsTypes.append(e.static_type)
        if dispatch.left_expression is None:
            if not self.classmethods[self.current_class].__contains__(dispatch.func_id):
                self.error.append('({}, {}) - AttributeError: Dispatch to undefined method {}.'.format(dispatch.line, dispatch.index, dispatch.func_id))
                return False
            officialArgsType = [x[1] for x in self.classmethods[self.current_class][dispatch.func_id][0]]
            _static_type = self.classmethods[self.current_class][dispatch.func_id][1]
        else:
            if not self.visit(dispatch.left_expression):
                return False
            if not self.classmethods[dispatch.left_expression.static_type].__contains__(dispatch.func_id):
                self.error.append('({}, {}) - AttributeError: Dispatch to undefined method {}.'.format(dispatch.line, dispatch.index, dispatch.func_id))
                return False
            officialArgsType = [x[1] for x in self.classmethods[dispatch.left_expression.static_type][dispatch.func_id][0]]
            _static_type = self.classmethods[dispatch.left_expression.static_type][dispatch.func_id][1]

        if len(officialArgsType) != len(paramsTypes):
            self.error.append('({}, {}) - SemanticError: Method {} called with wrong number of arguments.'.format(dispatch.line, dispatch.index, dispatch.func_id))
            return False

        _len = len(paramsTypes)
        for i in range(_len):
            if not self.conforms[paramsTypes[i]].__contains__(officialArgsType[i]):
                self.error.append('({}, {}) - TypeError: In call of method {}, of parameters does not conform to declared type.'.format(dispatch.line, dispatch.index, dispatch.func_id))
                return False
        dispatch.static_type = _static_type
        return True


    @visitor.when(StaticDispatch)
    def visit(self, static_dispatch):
        paramsTypes = []
        if not static_dispatch.parameters is None:
            for e in static_dispatch.parameters:
                if not self.visit(e):
                    return False
                paramsTypes.append(e.static_type)

        if not self.visit(static_dispatch.left_expression):
            return False

        if not self.conforms[static_dispatch.left_expression.static_type].__contains__(static_dispatch.parent_type):
            self.error.append('({}, {}) - TypeError: Expression type {} does not conform to declared static dispatch type {}.'.format(static_dispatch.line, static_dispatch.index, static_dispatch.left_expression.static_type, static_dispatch.parent_type))
            return False

        if not self.classmethods_original[static_dispatch.parent_type].__contains__(static_dispatch.func_id):
            self.error.append('({}, {}) - AttributeError: Dispatch to undefined method {}.'.format(static_dispatch.line, static_dispatch.index, static_dispatch.func_id))
            return False

        officialArgsType = [x[1] for x in self.classmethods[static_dispatch.left_expression.static_type][static_dispatch.func_id][0]]
        if len(officialArgsType) != len(paramsTypes):
            self.error.append('({}, {}) - SemanticError: Method {} called with wrong number of arguments.'.format(static_dispatch.line, static_dispatch.index, static_dispatch.func_id))
            return False
        _len = len(paramsTypes)
        for i in range(_len):
            if not self.conforms[paramsTypes[i]].__contains__(officialArgsType[i]):
                self.error.append('({}, {}) - TypeError: In call of method {}, of parameters does not conform to declared type.'.format(static_dispatch.line, static_dispatch.index, static_dispatch.func_id))
                return False

        static_dispatch.static_type = self.classmethods[static_dispatch.left_expression.static_type][static_dispatch.func_id][1]
        return True

    @visitor.when(Branch)
    def visit(self, branch):
        if not self.visit(branch.expr):
            return False
        branch.static_type = branch.expr.static_type
        return True

    @visitor.when(Case)
    def visit(self, case):

        if not self.visit(case.case_expression):
            return False

        branchTypeSet = set([])
        for branch in case.implications:
            if branchTypeSet.__contains__(branch.var.type):
                self.error.append('({}, {}) - SemanticError: Duplicate branch {} in case statement.'.format(branch.line, branch.index, branch.var.type))
                return False
            branchTypeSet.add(branch.var.type)
            if not self.classmethods.__contains__(branch.var.type):
                self.error.append('({}, {}) - TypeError: Class {} of case branch is undefined.'.format(branch.line, branch.index, branch.var.type))
                return False

            self.local_variables.append((branch.var.id, branch.var.type))
            if not self.visit(branch):
                return False
            n = len(self.local_variables) - 1
            self.local_variables.pop(n)
        
        static_type = case.implications[0].static_type
        for branch in case.implications[1:]:
            static_type = self.lca(static_type, branch.static_type)

        case.static_type = static_type
        return True
