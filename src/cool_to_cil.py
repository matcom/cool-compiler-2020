import visitor as visitor
from AST import *
import AST_CIL

class Build_CIL:
    def __init__(self, ast, sem):
        self.end_line = {}
        self.idCount = 0
        self.astCIL = AST_CIL.Program()
        self.local_variables = [Var('self', 'SELF_TYPE')]
        self.local_variables_map = [(0,0)]
        self.local_variables_original = {}
        self.local_variables_name = {}
        self.constructor = {}
        self.classmethods = {}
        self.BFS(sem.graph, sem.classmethods_original)
        self.visit(ast, self.astCIL)

    def BFS(self, graph, class_methods):
        self.classmethods[('Object', 'abort')]        = 'function_Object_abort'
        self.classmethods[('Object', 'type_name')]    = 'function_Object_type_name'
        self.classmethods[('Object', 'copy')]         = 'function_Object_copy'
        self.classmethods[('IO', 'out_string')]       = 'function_IO_out_string'
        self.classmethods[('IO', 'out_int')]          = 'function_IO_out_int'
        self.classmethods[('IO', 'in_string')]        = 'function_IO_in_string'
        self.classmethods[('IO', 'in_int')]           = 'function_IO_in_int'
        self.classmethods[('String', 'length')]       = 'function_String_length'
        self.classmethods[('String', 'concat')]       = 'function_String_concat'
        self.classmethods[('String', 'substr')]       = 'function_String_substr'

        l = ['Object']
        while len(l) > 0:
            temp = l.pop(0)
            if not graph.__contains__(temp): continue
            for _class in graph[temp]:
                l.append(_class)
                for function in class_methods[temp]:
                    self.classmethods[(_class, function)] = self.classmethods[(temp, function)]                


    def get_local(self):
        dest = 'local_' + str(self.idCount)
        self.idCount += 1
        return dest

    @visitor.on('node')
    def visit(self, node, nodeCIL):
        pass

    @visitor.when(Program)
    def visit(self, program, programCIL):

        #añadir IO, Object, Int, String, Bool
        _type_IO = AST_CIL.Type('IO')
        func = 'function' + '_' + 'IO' + '_' + 'out_string'
        _type_IO.methods['out_string'] = func
        self.classmethods[('IO', 'out_string')] = func
        f = AST_CIL.Function(func)
        f.params.append('x')
        f.instructions.append(AST_CIL.Print('x'))        
        self.astCIL.code_section.append(f)
        programCIL.type_section.append(_type_IO)

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
        typeCIL.methods[method.id] = func

        self.classmethods[(self.current_class, method.id)] = func

        f = AST_CIL.Function(func)

        for arg in method.parameters:
            f.params.append(arg.id)

        result = self.visit(method.expression, f)
        f.instructions.append(AST_CIL.Return(result))
        
        self.astCIL.code_section.append(f)

        self.local_variables.clear()
        self.local_variables_map.clear()
        self.local_variables.append(Var('self','SELF_TYPE'))
        self.local_variables_map.append((0,0))
        self.current_method = None 
    
    @visitor.when(String)
    def visit(self, string, functionCIL):
        #crear tag
        #annadir a data
        tag = 's' + str(len(self.astCIL.data_section))

        n = len(string.value)

        if string.value[n-1] == '\n':
            s = string.value.replace("\n",'\\n\"')
            s = '\"' + s
        else: s = '"' + s + '"'

        self.astCIL.data_section[s] = tag
        d = self.get_local()
        intr = AST_CIL.Load(d, tag)
        functionCIL.localvars.append(d)
        functionCIL.instructions.append(intr)
        return d

    @visitor.when(Dispatch)
    def visit(self, dispatch, functionCIL):
        dest = 'local_' + str(self.idCount)
        self.idCount += 1

        for item in dispatch.parameters:    #e(e1,e2,...,en)
            result = self.visit(item, functionCIL)
            functionCIL.instructions.append(AST_CIL.Arg(result))

        intr = AST_CIL.Call(dest, self.classmethods[(self.current_class, dispatch.func_id)])
        functionCIL.localvars.append(dest)
        functionCIL.instructions.append(intr)

        return dest
