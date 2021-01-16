import visitor as visitor
from AST import *
import AST_CIL


class Build_CIL:
    def __init__(self, ast):
        self.idCount = 0
        self.astCIL = AST_CIL.Program()
        self.local_variables = [Var('self', 'SELF_TYPE')]
        self.local_variables_map = [(0,0)]
        self.local_variables_original = {}
        self.local_variables_name = {}
        self.constructor = {}
        self.classmethods = {}
        self.visit(ast, self.astCIL)

    @visitor.on('node')
    def visit(self, node, nodeCIL):
        pass

    @visitor.when(Program)
    def visit(self, program, programCIL):
        for c in program.classes:
            self.visit(c, programCIL)

    @visitor.when(Class)
    def visit(self, _class, programCIL):
        #clase que estoy visitando
        self.current_class = _class.name

        #crear el tipo correspondiente
        _type = AST_CIL.Type(_class.name)
        #annadir el codigo de la clase

        for m in _class.methods:
            self.visit(m, _type)

        programCIL.type_section.append(_type)
        self.current_class = None

    @visitor.when(Method)
    def visit(self, method, typeCIL):
        
        self.current_method = method.id

        func = 'function' + '_' + self.current_class + '_' + method.id
        self.idCount += 1

        typeCIL.methods[method.id] = func

        self.classmethods[(self.current_class, method.id)] = func

        f = AST_CIL.Function(func)

        p = AST_CIL.Param('_self')

        f.params.append(p)

        for arg in method.parameters:
            p = AST_CIL.Param(arg.id)
            f.params.append(p)

        result = self.visit(method.expression, f)
        f.instructions.append(AST_CIL.Return(result))
        
        self.astCIL.code_section.append(f)

        self.local_variables.clear()
        self.local_variables_map.clear()
        self.local_variables.append(Var('self','SELF_TYPE'))
        self.local_variables_map.append((0,0))
        self.current_method = None

    @visitor.when(Block)
    def visit(self, block , functionCIL):
        pass

    @visitor.when(Star)
    def visit(self, star , functionCIL):
        pass

    @visitor.when(Plus)
    def visit(self, plus , functionCIL):
        pass

    @visitor.when(Minus)
    def visit(self, minus, functionCIL):
        pass

    @visitor.when(Div)
    def visit(self, div, functionCIL):
        pass

    @visitor.when(Star)
    def visit(self, star , functionCIL):
        pass

    @visitor.when(Plus)
    def visit(self, plus , functionCIL):
        pass

    @visitor.when(Minus)
    def visit(self, minus, functionCIL):
        pass

    @visitor.when(Div)
    def visit(self, div, functionCIL):
        pass

    @visitor.when(LowerEqualThan)
    def visit(self, lowerEqualThan, functionCIL):
        pass

    @visitor.when(EqualThan)
    def visit(self, equalThan, functionCIL):
        pass

    @visitor.when(LowerThan)
    def visit(self, lowerThan, functionCIL):
        pass

    @visitor.when(Not)
    def visit(self, negation, functionCIL):
        pass

    @visitor.when(IntegerComplement)
    def visit(self, I_complement, functionCIL):
        pass

    @visitor.when(IsVoid)
    def visit(self, is_void, functionCIL):
        pass

    @visitor.when(Type)
    def visit(self, _type, functionCIL):
        pass

    @visitor.when(NewType)
    def visit(self, new_type, functionCIL):
        pass

    @visitor.when(Boolean)
    def visit(self, boolean, functionCIL):
        pass

    @visitor.when(Interger)
    def visit(self, interger, functionCIL):
        pass

    @visitor.when(String)
    def visit(self, string, functionCIL):
        #crear tag
        #annadir a data
        tag = 's' + str(len(self.astCIL.data_section))
        self.astCIL.data_section[string.value] = tag
        return tag

    @visitor.when(Conditional)
    def visit(self, cond, functionCIL):
        pass

    @visitor.when(Loop)
    def visit(self, loop, functionCIL):
        pass

    @visitor.when(LetVar)
    def visit(self, let, functionCIL):
        pass

    @visitor.when(Assign)
    def visit(self, assign, functionCIL):
        pass

    @visitor.when(Attribute)
    def visit(self, attr, functionCIL):
        pass

    @visitor.when(Var)
    def visit(self, var, functionCIL):
        pass

    @visitor.when(Dispatch)
    def visit(self, dispatch, functionCIL):
        
        dest = 'local' + str((dispatch.line, dispatch.index)) + str(self.idCount)
        self.idCount += 1

        for item in dispatch.parameters:
            result = self.visit(item, functionCIL)
            functionCIL.instructions.append(AST_CIL.Arg(result))

        intr = AST_CIL.Call(dest, dispatch.func_id)

        functionCIL.localvars.append(AST_CIL.Local(dest))
        functionCIL.instructions.append(intr)

        return dest

    @visitor.when(StaticDispatch)
    def visit(self, static_dispatch, functionCIL):
        pass

    @visitor.when(Branch)
    def visit(self, branch, functionCIL):
        pass

    @visitor.when(Case)
    def visit(self, case, functionCIL):
        pass
