from typing import List, Optional, Any
import cil.nodes as nodes
from abstract.semantics import VariableInfo, Context, Type, Method


class BaseCoolToCilVisitor:
    def __init__(self, context: Context):
        self.dot_types: List[nodes.TypeNode] = []
        self.dot_data: List[Any] = []
        self.dot_code: List[nodes.FunctionNode] = []
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.current_function: Optional[nodes.FunctionNode] = None

    @property
    def params(self) -> List[nodes.ParamNode]:
        assert self.current_function is not None
        return self.current_function.params

    @property
    def localvars(self) -> List[nodes.LocalNode]:
        assert self.current_function is not None
        return self.current_function.localvars

    @property
    def instructions(self) -> List[nodes.InstructionNode]:
        assert self.current_function is not None
        return self.current_function.instructions

    def register_params(self, vinfo: VariableInfo) -> str:
        assert self.current_function is not None
        vinfo.name = f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node: nodes.ParamNode = nodes.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def register_local(self, vinfo: VariableInfo) -> str:
        assert self.current_function is not None
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = nodes.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self) -> str:
        vinfo = VariableInfo('internal')
        return self.register_local(vinfo)

    def to_function_name(self, method_name: str, type_name: str) -> str:
        return f"function_{method_name}_at_{type_name}"

    def register_instruction(self, instruction: nodes.InstructionNode) -> nodes.InstructionNode:
        self.instructions.append(instruction)
        return instruction

    def register_function(self, function_name: str) -> nodes.FunctionNode:
        function_node = nodes.FunctionNode(function_name, [], [], [])
        self.dot_code.append(function_node)
        return function_node

    def register_type(self, name: str) -> nodes.TypeNode:
        type_node = nodes.TypeNode(name)
        self.dot_types.append(type_node)
        return type_node

    def register_data(self, value: Any) -> nodes.DataNode:
        vname = f'data_{len(self.dot_data)}'
        data_node = nodes.DataNode(vname, value)
        self.dot_data.append(data_node)
        return data_node
