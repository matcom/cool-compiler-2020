from code_generation.ast import *

def program_cg_visitor(program:ProgramNode):
    type_code=''
    data_code=''
    func_code=''
    for t in program.types:       
        type_code+=f'{type_cg_visitor(t)}\n'
    for d in program.data:
        data_code+=f'{data_cg_visitor(d)}\n'
    for f in program.code:
        func_code+=f'{func_cg_visitor(f)}\n'
        
    return f'.TYPES \n {type_code} .DATA \n {data_code} .CODE \n {func_code}'
      
def type_cg_visitor(type: TypeNode):
    attr_code=''
    method_code=''
    for attr in type.attributes:
        attr_code+=f'attribute {attr}; \n'
    
    for met in type.methods:
        method_code+=f'method {met}:{type.name}_{met};\n'
        
    return f'type {type.name} {{ \n {attr_code} {method_code} }}'

def data_cg_visitor(data: DataNode):
    return f'{data.id} = {data.value} ;'

def func_cg_visitor(func: FuncNode):
    params_code=''
    locals_code=''
    body_code=''
    for param in func.params:
        params_code+=f'{param_cg_visitor(param)}\n'
        
    for local in func.locals:
        locals_code+=f'{local_cg_visitor(local)}\n'
        
    for instruction in func.body:
        body_code+=f'{instruction_cg_visitor(instruction)}\n'
        
    return f'function {func.name} {{ \n {params_code} {locals_code} {body_code} }}'
        
def param_cg_visitor(param:ParamNode):
    return f'PARAM {param} ;'

def local_cg_visitor(local:LocalNode):
    return f'LOCAL {local} ;'

def instruction_cg_visitor(instruction:InstructionNode):
    try:
        return __visitors__[type(instruction)](instruction)
    except KeyError:
        print(f'Not visitor for {instruction}')

def assign_cg_visitor(assign:AssignNode):
    return f'{assign.id} = {assign.val} ;'

def plus_cg_visitor(plus:PlusNode):
    return f'{plus.result} = {plus.left} + {plus.right} ;'

def minus_cg_visitor(minus:MinusNode):
    return f'{minus.result} = {minus.left} - {minus.right} ;'

def star_cg_visitor(star:StarNode):
    return f'{star.result} = {star.left} * {star.right} ;'

def div_cg_visitor(div:DivNode):
    return f'{div.result} = {div.left} / {div.right} ;'

def get_attr_cg_visitor(getattr:GetAttrNode):
    return f'{getattr.result} = GETATTR {getattr.obj} {getattr.attr} ;'

def set_attr_cg_visitor(setattr:SetAttrNode):
    return f'SETATTR {setattr.obj} {setattr.attr} {setattr.val} ;'

def get_index_cg_visitor(getindex:GetIndexNode):
    return f'{getindex.result} = GETINDEX {getindex.array} {getindex.index} ;'

def set_index_cg_visitor(setindex:SetIndexNode):
    return f'SETINDEX {setindex.array} {setindex.index} {setindex.val} ;'

def allocate_cg_visitor(allocate:AllocateNode):
    return f'{allocate.addr} = ALLOCATE {allocate.type} ;'

def typeof_cg_visitor(typeof: TypeOfNode):
    return f'{typeof.result} = TYPEOF {typeof.var} ;'

def array_cg_visitor(array: ArrayNode):
    return f'{array.result} = ARRAY {array.len} ;'

def call_cg_visitor(call:CallNode):
    return f'{call.result} = CALL {call.method} ;'

def vcall_cg_visitor(vcall:VCAllNode):
    return f'{vcall.result} = VCALL {vcall.type} {vcall.method} ;'

def arg_cg_visitor(arg:ArgNode):
    return f'ARG {arg.val} ;'

def cond_goto_cg_visitor(gcoto:ConditionalGotoNode):
    return f'IF {cgoto.predicate} GOTO {cgoto.label} ;'

def goto_cg_visitor(goto:GotoNode):
    return f'GOTO {goto.label} ;'

def label_cg_visitor(label:LabelNode):
    return f'LABEL {label.label_name} ;'

def return_cg_visitor(ret:ReturnNode):
    return f'RETURN {ret.ret_value} ;' if ret.ret_value else f'RETURN ;'

def load_cg_visitor(load:LoadNode):
    return f'{load.result} = LOAD {load.addr} ;'

def length_cg_visitor(length:LengthNode):
    return f'{length.result} = LENGTH {length.str} ;'

def concat_cg_visitor(concat:ConcatNode):
    return f'{concat.result} = CONCAT {concat.str_a} {concat.str_b} ;'

def substring_cg_visitor(substring:SubStringNode):
    return f'{substring.result} = SUBSTRING {substring.str_a} {substring.str_b} ;'

def str_cg_visitor(str: StrNode):
    return f'{str.str} = STR {str.val} ;'

def read_cg_visitor(read:ReadNode):
    return 'READ ;'

def print_cg_visitor(print:PrintNode):
    return f'PRINT {print.str} ;'


__visitors__ = {
    AssignNode:assign_cg_visitor,
    PlusNode:plus_cg_visitor,
    MinusNode:minus_cg_visitor,
    StarNode:star_cg_visitor,
    DivNode:div_cg_visitor,
    GetAttrNode:get_attr_cg_visitor,
    SetAttrNode:set_attr_cg_visitor,
    GetIndexNode:get_index_cg_visitor,
    SetIndexNode:set_index_cg_visitor,
    AllocateNode:allocate_cg_visitor,
    TypeOfNode:typeof_cg_visitor,
    ArrayNode:array_cg_visitor,
    CallNode:call_cg_visitor,
    VCAllNode:vcall_cg_visitor,
    ArgNode:arg_cg_visitor,
    ConditionalGotoNode:cond_goto_cg_visitor,
    GotoNode:goto_cg_visitor,
    LabelNode: label_cg_visitor,
    ReturnNode:return_cg_visitor,
    LoadNode:load_cg_visitor,
    LengthNode:length_cg_visitor,
    ConcatNode:concat_cg_visitor,
    SubStringNode:substring_cg_visitor,
    StrNode:str_cg_visitor,
    ReadNode:read_cg_visitor,
    PrintNode:print_cg_visitor
}
    


