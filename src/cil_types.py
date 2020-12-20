import ast_hierarchy as ast
import cil_hierarchy as cil
import visitor
from context import VariableInfo, MethodInfo, ClassInfo
from copy import copy


class CILTypes:
    def __init__(self, type_hierachy):
        self.type_hierachy = type_hierachy

        # La sección .TYPES del CIL
        self.dottypes = {}

        self.dotdata = {
            "exception_1": cil.CILDataNode("exception_1", "Se esta realizando dispatch sobre valor void"),
            "exception_2": cil.CILDataNode("exception_2", "Se esta realizando case sobre valor void"),
            "exception_3": cil.CILDataNode("exception_3", "El tipo de la expresion case no concuerda con ninguna rama"),
            "exception_4": cil.CILDataNode("exception_4", "Division por cero"),
            "exception_5": cil.CILDataNode("exception_5", "Substring fuera de rango"),
            "exception_6": cil.CILDataNode("exception_6", "Abort"),
        }

        self.dotcode = []

        self.current_class_name = ''

        self.current_function_name = ''

        # Variables locales del método actual
        self.localvars = []

        # Instrucciones del método actual
        self.instructions = []

        # Parametros del metodo actual
        self.arguments = []

        self.internal_count = 0

        self.void = 0

    # Util Methods
    def change_current_function(self, fname=''):
        self.current_function_name = fname
        self.localvars = []
        self.instructions = []
        self.arguments = []

    def define_internal_local(self):
        vinfo = VariableInfo('internal')
        vinfo.name = self.build_internal_vname(vinfo.name)
        return self.register_local(vinfo)

    def build_internal_vname(self, vname):
        vname = '{}_{}'.format(vname, self.internal_count)
        self.internal_count += 1
        return vname
    
    def build_funcname(self, fname):
        fname = '{}_{}'.format(fname, self.internal_count)
        self.internal_count += 1
        return fname

    def register_local(self, vinfo):
        vinfo.vmholder = len(self.localvars) + len(self.arguments) + 1
        local_node = cil.CILLocalNode(vinfo)
        self.localvars.append(local_node)
        return local_node.vinfo

    def register_instruction(self, instruction):
        self.instructions.append(instruction)

    def register_function(self, function):
        self.dotcode.append(function)

    def build_label(self):
        fname = 'label_type_{}'.format(self.internal_count)
        self.internal_count += 1
        return cil.CILLabelNode(fname)

    def register_data(self, value):
        vname = 'data_{}'.format(len(self.dotdata))
        data_node = cil.CILDataNode(vname, value)
        self.dotdata[vname] = data_node
        return data_node

    # Visit
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        object_class = self.object_bi()
        self.dottypes['Object'] = object_class
        self.dottypes['Int'] = self.int_bi(object_class)
        self.dottypes['Bool'] = self.bool_bi(object_class)
        self.dottypes['String'] = self.string_bi(object_class)
        self.dottypes['IO'] = self.io_bi(object_class)

        for child in node.classes:
            self.dottypes[child.typeName] = self.visit(child)

        self.change_current_function('entry')
        vlocal = self.define_internal_local()
        cclass = self.dottypes['Main']
        self.register_instruction(cil.CILAllocateNode(vlocal, cclass.cinfo))
        
        self.register_instruction(cil.CILSaveState())
        self.register_instruction(cil.CILParamNode(vlocal))

        vlocal2 = self.define_internal_local()
        nctor = cclass.methods['ctor'].finfo.name
        self.register_instruction(cil.CILStaticCallNode(vlocal2, nctor))
        
        
        mname = cclass.methods['main'].finfo.name
        self.register_instruction(cil.CILSaveState())
        self.register_instruction(cil.CILParamNode(vlocal))
        self.register_instruction(cil.CILStaticCallNode(vlocal2, mname))
        self.register_instruction(cil.CILReturnFinal())
        
        entry_m = cil.CILFunctionNode(MethodInfo(self.current_function_name), self.arguments, self.localvars, self.instructions)
        self.register_function(entry_m)
        
        return cil.CILProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(ast.ClassNode)
    def visit(self, node: ast.ClassNode):
        self.current_class_name = node.typeName
        parent = self.dottypes[node.fatherTypeName.Name]

        attrs = copy(parent.attrs)
        for feature in node.features:
            if isinstance(feature, ast.AttributeFeatureNode):
                # vinfo = feature.vinfo
                vinfo = VariableInfo(feature.id, feature.typeName)
                vinfo.vmholder = len(attrs.keys())+1
                attrs[feature.id] = vinfo

        ctor = self.build_funcname('ctor')
        constructor = cil.CILFunctionNode(MethodInfo(ctor, vmholder=2), [], [], [])
        self.register_function(constructor)

        methods = copy(parent.methods)
        methods['ctor'] = constructor
        
        for feature in node.features:
            if isinstance(feature, ast.FunctionFeatureNode):
                meth_ = self.type_hierachy[self.current_class_name].MethList[feature.id]
                finfo = MethodInfo(meth_.Name)
                ffunc = cil.CILFunctionNode(finfo, [], [], [])
                self.register_function(ffunc)

                if not methods.__contains__(feature.id):
                    ffunc.finfo.vmholder = len(methods.keys())+2 
                else:
                    ffunc.finfo.vmholder = methods[feature.id].finfo.vmholder             

                methods[feature.id] = ffunc            
                ffunc.finfo.paramsType = meth_.ParamsType
                ffunc.finfo.returnType = meth_.ReturnType           
                
        vinfo = ClassInfo(self.current_class_name, 4*len(attrs.keys()), 4*len(methods.keys()), parent)
        return cil.CILTypeNode(vinfo, attrs, methods)

    # Tipos built-in
    def object_bi(self):
        attrs = {}
        self.change_current_function()
        self.arguments.append(cil.CILArgNode(VariableInfo('self', vmholder=1)))
        # self.register_instruction(cil.CILSetAttribNode(self.arguments[0].vinfo, 'value', self.void))
        # self.register_instruction(cil.CILSetAttribNode(self.arguments[0].vinfo, 'type', self.void))
        self.register_instruction(cil.CILReturnNode())

        ctor_func = cil.CILFunctionNode(MethodInfo(self.build_funcname('ctor'), vmholder= 2), self.arguments, self.localvars, self.instructions)
        self.register_function(ctor_func)


        self.change_current_function()
        self.arguments.append(cil.CILArgNode(VariableInfo('self', vmholder=1)))
        
        var1 = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_6']))
        
        self.register_instruction(cil.CILPrintStrNode(var1))
        self.register_instruction(cil.CILErrorNode())
        self.register_instruction(cil.CILReturnNode())
        abort_func = cil.CILFunctionNode(MethodInfo(self.build_funcname('abort'), vmholder= 3, returnType='Object'), self.arguments, self.localvars, self.instructions)
        self.register_function(abort_func)

        self.change_current_function()
        self.arguments.append(cil.CILArgNode(VariableInfo('self', vmholder=1)))
        vlocal = self.define_internal_local()
        # self.register_instruction(cil.CILGetAttribNode(vlocal, self.arguments[0].vinfo, 'type'))
        self.register_instruction(cil.CILTypeOfNode(vlocal, self.arguments[0].vinfo))
        self.register_instruction(cil.CILTypeName(vlocal, vlocal))
        self.register_instruction(cil.CILReturnNode(vlocal))

        typename_func = cil.CILFunctionNode(MethodInfo(self.build_funcname('type_name'), vmholder= 4, returnType='String'), self.arguments, self.localvars, self.instructions)
        self.register_function(typename_func)

        methods = {'ctor': ctor_func, 'abort':abort_func, 'type_name': typename_func}
        # methods = {'ctor': ctor_func, 'type_name': typename_func}
        cinfo = ClassInfo('Object', 4*len(attrs.keys()), 4*len(methods.keys()))
        return cil.CILTypeNode(cinfo, attrs, methods)

    def int_bi(self, object_type):
        attrs = {'value': VariableInfo('value', vmholder=1)}
        methods = copy(object_type.methods)
        cinfo = ClassInfo('Int', 4*len(attrs.keys()), 4*len(methods.keys()), object_type)
        return cil.CILTypeNode(cinfo, attrs, methods)

    def bool_bi(self, object_type):
        attrs = {'value': VariableInfo('value', vmholder=1)}
        methods = copy(object_type.methods)
        cinfo = ClassInfo('Bool', 4*len(attrs.keys()), 4*len(methods.keys()), object_type)
        return cil.CILTypeNode(cinfo, attrs, methods)

    def string_bi(self, object_type):
        attrs = {'value': VariableInfo('value', vmholder=1)}
        methods = copy(object_type.methods)

        self.change_current_function()
        self.arguments = [cil.CILArgNode(VariableInfo('self', vmholder=1)), cil.CILArgNode(VariableInfo('string2', vmholder=2))]
        
        vlocal1 = self.define_internal_local()
        self.register_instruction(cil.CILGetAttribNode(vlocal1, self.arguments[0].vinfo, attrs['value'].vmholder))

        vlocal2 = self.define_internal_local()
        self.register_instruction(cil.CILConcatNode(vlocal2, vlocal1, self.arguments[1].vinfo))

        # self.register_instruction(cil.CILSetAttribNode(self.arguments[0].vinfo, 'value', vlocal2))
        self.register_instruction(cil.CILReturnNode(vlocal2))

        concat_func = cil.CILFunctionNode(MethodInfo(self.build_funcname('concat'), paramsType = ['String'], returnType='String'), self.arguments, self.localvars, self.instructions)
        self.register_function(concat_func)

        self.change_current_function()
        self.arguments = [cil.CILArgNode(VariableInfo('self', vmholder=1))]

        v_local3 = self.define_internal_local()
        self.register_instruction(cil.CILGetAttribNode(v_local3, self.arguments[0].vinfo, attrs['value'].vmholder))

        v_local4 = self.define_internal_local()
        self.register_instruction(cil.CILLengthNode(v_local4, v_local3))

        self.register_instruction(cil.CILReturnNode(v_local4))

        length_func = cil.CILFunctionNode(MethodInfo(self.build_funcname('length'), returnType='Int'), self.arguments, self.localvars, self.instructions)
        self.register_function(length_func)


        # Substring
        self.change_current_function()
        self.arguments = [cil.CILArgNode(VariableInfo('self', vmholder=1)), cil.CILArgNode(VariableInfo('i', vmholder=2)), cil.CILArgNode(VariableInfo('l', vmholder=3))]
        
        label_val = self.build_label()
        label_nval = self.build_label()
        label_fin = self.build_label()

        label_nval1 = self.build_label()
        label_fin1 = self.build_label()

        label_nval2 = self.build_label()
        label_fin2 = self.build_label()

        vvar2 = self.define_internal_local()
        self.register_instruction(cil.CILAssignNode(vvar2, 0))

        vvar1 = self.define_internal_local()
        self.register_instruction(cil.CILLessThan(vvar1, self.arguments[1].vinfo, vvar2))
        self.register_instruction(cil.CILGotoIfNode(vvar1, label_nval1))

        self.register_instruction(cil.CILLessThan(vvar1, self.arguments[2].vinfo, vvar2))
        self.register_instruction(cil.CILGotoIfNode(vvar1, label_nval2))

        self.register_instruction(cil.CILGotoIfNode(self.arguments[2].vinfo, label_val))

        self.register_instruction(cil.CILGotoNode(label_nval))

        self.register_instruction(label_val)
        v_local5 = self.define_internal_local()
        self.register_instruction(cil.CILGetAttribNode(v_local5, self.arguments[0].vinfo, attrs['value'].vmholder))

        vhalt = self.define_internal_local()
        vlength = self.define_internal_local()
        self.register_instruction(cil.CILLengthNode(vlength, v_local5))

        vsum = self.define_internal_local()
        self.register_instruction(cil.CILPlusNode(vsum, self.arguments[1].vinfo, self.arguments[2].vinfo))
        self.register_instruction(cil.CILMinusNode(vsum, vsum, 1))
        self.register_instruction(cil.CILLessThan(vhalt, vsum, vlength))

        label1 = self.build_label()
        labelerror = self.build_label()
        labelend = self.build_label()

        self.register_instruction(cil.CILGotoIfNode(vhalt, label1))
        self.register_instruction(cil.CILGotoNode(labelerror))
        
        self.register_instruction(label1)

        v_local6 = self.define_internal_local()
        self.register_instruction(cil.CILSubstringNode(v_local6, v_local5, self.arguments[1].vinfo, self.arguments[2].vinfo))
        self.register_instruction(cil.CILReturnNode(v_local6))

        self.register_instruction(cil.CILGotoNode(labelend))

        self.register_instruction(labelerror)
        var1 = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_5']))
        self.register_instruction(cil.CILPrintStrNode(var1))
        self.register_instruction(cil.CILErrorNode())

        self.register_instruction(labelend)
        self.register_instruction(cil.CILGotoNode(label_fin))

        self.register_instruction(label_nval)
        msg = self.register_data("")
        var = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var, msg))
        self.register_instruction(cil.CILReturnNode(var))

        self.register_instruction(label_fin)
        self.register_instruction(cil.CILGotoNode(label_fin2))

        self.register_instruction(label_nval2)
        var1 = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_5']))
        self.register_instruction(cil.CILPrintStrNode(var1))
        self.register_instruction(cil.CILErrorNode())

        self.register_instruction(label_fin2)
        self.register_instruction(cil.CILGotoNode(label_fin1))

        self.register_instruction(label_nval1)
        var1 = self.define_internal_local()
        self.register_instruction(cil.CILLoadNode(var1, self.dotdata['exception_5']))
        self.register_instruction(cil.CILPrintStrNode(var1))
        self.register_instruction(cil.CILErrorNode())

        self.register_instruction(label_fin1)


        substr_func = cil.CILFunctionNode(MethodInfo(self.build_funcname('substr'), paramsType = ['Int', 'Int'], returnType='String'), self.arguments, self.localvars, self.instructions)
        self.register_function(substr_func)

        length_func.finfo.vmholder = len(methods.keys())+2
        methods['length'] = length_func
        concat_func.finfo.vmholder = len(methods.keys())+2
        methods['concat'] = concat_func
        substr_func.finfo.vmholder = len(methods.keys())+2
        methods['substr'] = substr_func

        cinfo = ClassInfo('String', 4*len(attrs.keys()), 4*len(methods.keys()), object_type)
        return cil.CILTypeNode(cinfo, attrs, methods)

    def io_bi(self, object_type):
        attrs = {}
        methods = copy(object_type.methods)

        # Print string
        self.change_current_function()
        self.arguments = [cil.CILArgNode(VariableInfo('self', vmholder=1)), cil.CILArgNode(VariableInfo('x', vmholder=2))]

        self.register_instruction(cil.CILPrintStrNode(self.arguments[1].vinfo))

        # v_local1 = self.define_internal_local()
        self.register_instruction(cil.CILReturnNode(self.arguments[0].vinfo))
        out_string = cil.CILFunctionNode(MethodInfo(self.build_funcname('out_string'), paramsType = ['String'], returnType='IO'), self.arguments, self.localvars, self.instructions)
        self.register_function(out_string)

        # Print int
        self.change_current_function()
        self.arguments = [cil.CILArgNode(VariableInfo('self', vmholder=1)), cil.CILArgNode(VariableInfo('x', vmholder=2))]

        self.register_instruction(cil.CILPrintIntNode(self.arguments[1].vinfo))

        # v_local1 = self.define_internal_local()
        self.register_instruction(cil.CILReturnNode(self.arguments[0].vinfo))
        out_int = cil.CILFunctionNode(MethodInfo(self.build_funcname('out_int'), paramsType = ['Int'], returnType='IO'), self.arguments, self.localvars,
                                         self.instructions)
        self.register_function(out_int)

        # Read string
        self.change_current_function()
        self.arguments = [cil.CILArgNode(VariableInfo('self', vmholder=1))]

        v_local = self.define_internal_local()
        self.register_instruction(cil.CILReadStrNode(v_local))
        self.register_instruction(cil.CILReturnNode(v_local))

        in_string = cil.CILFunctionNode(MethodInfo(self.build_funcname('in_string'), returnType='String'), self.arguments, self.localvars,
                                      self.instructions)
        self.register_function(in_string)

        # Read int
        self.change_current_function()
        self.arguments = [cil.CILArgNode(VariableInfo('self', vmholder=1))]

        v_local = self.define_internal_local()
        self.register_instruction(cil.CILReadIntNode(v_local))
        self.register_instruction(cil.CILReturnNode(v_local))

        in_int = cil.CILFunctionNode(MethodInfo(self.build_funcname('in_int'), returnType='Int'), self.arguments, self.localvars,
                                        self.instructions)
        self.register_function(in_int)

        out_string.finfo.vmholder = len(methods.keys())+2
        methods['out_string'] = out_string
        out_int.finfo.vmholder = len(methods.keys())+2
        methods['out_int'] = out_int
        in_string.finfo.vmholder = len(methods.keys())+2
        methods['in_string'] = in_string
        in_int.finfo.vmholder = len(methods.keys())+2
        methods['in_int'] = in_int

        cinfo = ClassInfo('IO', 4*len(attrs.keys()), 4*len(methods.keys()), object_type)
        return cil.CILTypeNode(cinfo, attrs, methods)