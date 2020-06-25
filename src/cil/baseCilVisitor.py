from typing import List, Optional, Any, Dict, Tuple
import cil.nodes as nodes
from abstract.semantics import VariableInfo, Context, Type, Method

TDT = Dict[Tuple[str, str], int]


# Esta clase no debe ser utilizada directamente en el desarrollo del compilador.
# Solo esta pensada para dar soporte a un grafo que represente la jerarquia de
# clases de Cool, sobre la cual se construira una tabla LCA para poder consultar
# la jerarquia en runtime. InheritanceGraph representa grafos no dirigidos ya que
# las restricciones de Cool permiten hacer transformaciones al Grafo Dirigido que
# se obtiene de la jerarquia de clases para trabajar sobre arboles.
class InheritanceGraph:
    def __init__(self):
        # Lista de adyacencia del grafo
        self._adytable: Dict[str, List[str]] = {}

        # Tabla LCA
        self.tdt: TDT = {}

        self._discover: Dict[str, int] = {}
        self._finalization: Dict[str, int] = {}
        self.__time = 0
        self.root_distance: Dict[str, int] = {}

    def add_edge(self, parent: str, child: str) -> None:
        # Agregar una arista a la lista de adyacencia.
        try:
            # Caso de que se hallan inicializado las listas de cada nodo.
            self._adytable[parent].append(child)
        except KeyError:
            # Hay k inicializar las listas de cada nodo.
            self._adytable[parent] = [child]
        try:
            self._adytable[child].append(parent)
        except KeyError:
            self._adytable[child] = [parent]

    def __ancestor(self, node_x: str, node_y: str) -> bool:
        # Devuelve true si x es ancestro de y.
        # Para realizar este calculo nos basamos en el arbol
        # construido por el DFS, y tenemos en cuenta los tiempos
        # de descubrimiento y finalizacion
        return self._discover[node_x] < self._discover[node_y] < self._finalization[node_y] < self._finalization[node_x]

    def __distance_from(self, node_x: str, node_y: str) -> int:
        # Si x es ancestro de y, entonces la distancia entre ellos
        # se calcula como d[y] - d[x], si x no es ancenstro de y,
        # entonces podemos definir la distancia entre ellos como infinito
        if self.__ancestor(node_x, node_y):
            return self.root_distance[node_y] - self.root_distance[node_x]
        else:
            return -1

    def __dfs(self, root: str, visited: Dict[str, bool], deep=0):
        visited[root] = True
        self._discover[root] = self.__time
        self.root_distance[root] = deep
        self.__time += 1

        for v in self._adytable[root]:
            if not visited[v]:
                self.__dfs(v, visited, deep + 1)
                self.__time += 1
        self._finalization[root] = self.__time

    def build_tdt(self):
        # Construir una tabla de distancia para cada Nodo del arbol.
        # En dicha tabla, tdt[x, y] = d donde d es la distancia entre
        # el nodo x y el nodo y, si x es ancestro de y, entonces d >= 1,
        # si x == y, d = 0 y d = -1 en otro caso
        visited = {node: False for node in self._adytable}

        # Realizar un recorrido dfs para inicializar los array d y f
        root = 'Object'
        self.__dfs(root, visited)

        # Construir la tabla
        for nodex in self._adytable:
            for nodey in self._adytable:
                if nodey == nodex:
                    self.tdt[(nodex, nodey)] = 0
                else:
                    self.tdt[(nodex, nodey)] = self.__distance_from(nodex, nodey)


class BaseCoolToCilVisitor:
    """
    Clase base para el visitor que transforma un AST de COOL en un AST de CIL.
    """
    def __init__(self, context: Context):
        self.dot_types: List[nodes.TypeNode] = []
        self.dot_data: List[Any] = []
        self.dot_code: List[nodes.FunctionNode] = []
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.current_function: Optional[nodes.FunctionNode] = None
        self.__labels_count: int = 0
        self.__build_CART()
        self.__build_builtins()

    @property
    def params(self) -> List[nodes.ParamNode]:
        # Obtener los parametros de la funcion que esta actualmente en construccion
        assert self.current_function is not None
        return self.current_function.params

    @property
    def localvars(self) -> List[nodes.LocalNode]:
        # Obtener las variables locales definidas en la funcion que esta actualmente en construccion
        assert self.current_function is not None
        return self.current_function.localvars

    @property
    def instructions(self) -> List[nodes.InstructionNode]:
        # Obtiene las instrucciones de la funcion que esta actualmente en construccion
        assert self.current_function is not None
        return self.current_function.instructions

    def register_params(self, vinfo: VariableInfo) -> nodes.ParamNode:
        # Registra un parametro en la funcion en construccion y devuelve el nombre procesado del parametro
        assert self.current_function is not None
        name = f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node: nodes.ParamNode = nodes.ParamNode(name)
        self.params.append(param_node)
        return param_node

    def register_local(self, vinfo: VariableInfo) -> nodes.LocalNode:
        assert self.current_function is not None
        name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = nodes.LocalNode(name)
        self.localvars.append(local_node)
        return local_node

    def define_internal_local(self) -> nodes.LocalNode:
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

    def do_label(self, label: str) -> str:
        self.__labels_count += 1
        return f"label_{label}_{self.__labels_count}"

    def __build_CART(self) -> None:
        """
        CART: Context Aware Runtime Table.\
        Esta estructura almacena datos relacionados con la jerarquia de clases definida en el programa. CART se debe almacenar \
        en la seccion .DATA y sera usada por metodos relacionados con chequeo de tipos en tiempo de ejecucion. La estructura es una \
        TDT (type distance table), donde dadas dos clases A y B, CART[A, B] = d donde d es la distancia entre la clase A y \
        la clase B, si la clase A es ancestro de la clase B en la jerarquia de tipos, 0 si A = B y -1 en otro caso.
        """

        # Crear el grafo de herencia basado en el contexto que tenemos hasta el momento.
        graph = InheritanceGraph()
        for itype in self.context.types:
            if self.context.types[itype].parent is not None:
                graph.add_edge(self.context.types[itype].parent.name, itype)  # type: ignore

        # Crear la TDT
        graph.build_tdt()
        self.tdt_table = graph.tdt

        # Procesar la TDT para hacerla accesible en runtime.
        self.tdt_data_node = self.register_data(self.tdt_table)

    def __build_builtins(self):
        pass
