from typing import List, Optional, Any, Dict, Tuple
import cil.nodes as nodes
from abstract.semantics import VariableInfo, Context, Type, Method

LCA_TABLE = Dict[Tuple[str, str], str]


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
        self._lcatable: LCA_TABLE = {}

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

    def __do_euler_trip(self, root: str, visited: Dict[str, bool], tour: List[str]):
        # Este metodo realiza el tour de euler en el grafo representado esta instancia.

        # Marcar el nodo desde el que partimos como visitado.
        visited[root] = True

        # Agregar el nodo al tour cuando lo vemos por primera vez.
        tour.append(root)

        for v in self._adytable[root]:
            # Realizar el tour por todos los subarboles que no hayamos visitado.
            if not visited[v]:
                self.__do_euler_trip(v, visited, tour)
                # Volver a agregar el nodo del que partimos cuando regresamos a el.
                tour.append(root)

    def __compute_nodes_levels(self, root: str, visited: Dict[str, bool], levels: List[int], lvl: int = 0):
        # Es la misma idea que el tour de euler, visitar los nodos en DFS y agregar para cada nodo
        # su distancia desde la raiz

        # marcar el nodo raiz de este subarbol como visitado
        visited[root] = True

        # agregar el nivel de este nodo a la lista de niveles
        levels.append(lvl)

        # Visitar los nodos adyacentes en DFS
        for v in self._adytable[root]:
            # Realizar el recorrido por los subarboles que no hayamos visitado
            if not visited[v]:
                self.__compute_nodes_levels(v, visited, levels, lvl + 1)
                # Volver a agregar el nivel del nodo cuando regresamos a el.
                levels.append(lvl)

    def __compute_representative_array(self, tour: List[str]) -> Dict[str, int]:
        # El representativo de cada nodo es la primera ocurrencia j del nodo tour[j]
        visited: Dict[str, bool] = {node: False for node in self._adytable.keys()}
        representative: Dict[str, int] = {}
        for i, node in enumerate(tour):
            if not visited[node]:
                representative[node] = i
                visited[node] = True
        return representative

    def build_lca_table(self):
        # Realizar el preprocesamiento necesario para crear la Tabla LCA.
        # Este preprocesamiento coincide con una DP para preprocesar un array para RMQ.
        # La implementacion del preprocesamiento es O(n^2). Existen algoritmos para preprocesar en
        # O(n) y responder las querys en O(1), pero dado que vamos a preguntar las n(n-1)/2 querys
        # para almacenarlas en la tabla, hacer el preprocesamiento en O(n^2) no afecta el orden del
        # tiempo total de construccion. No obstante la DP es necesaria para no realizar el preprocesamiento
        # en O(n^3).

        # Verificar que se halla construido el grafo
        assert self._adytable
        visited: Dict[str, bool] = {node: False for node in self._adytable.keys()}

        # Crear el tour de euler
        tour: List[str] = []
        # La raiz de la jerarquia es Object
        root = 'Object'
        self.__do_euler_trip(root, visited, tour)

        # crear el array de niveles
        levels: List[int] = []
        for node in visited.keys():
            visited[node] = False
        self.__compute_nodes_levels(root, visited, levels)

        # crear el array de nodos representativos
        representative = self.__compute_representative_array(tour)
        nodes = len(levels)

        # Preprocesar la tabla para responder las rmq-querys.
        # rmq_table[i][j] contiene el indice del menor elemento en el intervalo[i, j]
        rmq_table: List[List[int]] = [[0 for _ in range(nodes)] for _ in range(nodes)]

        # Sabemos que rmq[i,i] = i. Entonces podemos inicializar la tabla
        for i in range(nodes):
            rmq_table[i][i] = i

        # Para calcular la tabla solo tenemos que aplicar la DP:
        # rmq[i, j] = min(A[rmq[i, j-1]], A[j]) donde A es nuestro array
        for i in range(nodes):  # Iterar de menor a mayor longitud del intervalo
            for j in range(i + 1, nodes):
                m1 = rmq_table[i][j-1]
                if levels[m1] < levels[j]:
                    rmq_table[i][j] = m1
                else:
                    rmq_table[i][j] = j

        # TODO: Sera mejor representar en CIL la tabla rmq, el tour y los representativos e implementar una rutina
        #       para procesar una query, de modo que no halla que construir la tabla LCA en O(n^2), se puedan hacer
        #       las querys en O(1) y poder hacer el preprocesamiento en O(n)??
        #       Tener en cuenta que esto implica mas estructura en el codigo del programa, o sea, mas espacio en memoria
        #       y es un poco mas complejo.

        # Con la tabla construida, pasemos a hacer todas las preguntas
        for node1 in self._adytable.keys():
            for node2 in self._adytable.keys():
                # El LCA lo podemos calcular como LCA(x,y) = E[RMQ(r[x], r[y])] donde E es el tour de euler
                # y r es el array representativo.
                m1 = min(representative[node1], representative[node2])
                m2 = max(representative[node1], representative[node2])
                self._lcatable[node1, node2] = tour[rmq_table[m1][m2]]
                self._lcatable[node2, node1] = tour[rmq_table[m1][m2]]


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

    def register_params(self, vinfo: VariableInfo) -> str:
        # Registra un parametro en la funcion en construccion y devuelve el nombre procesado del parametro
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

    def do_label(self, label: str) -> str:
        self.__labels_count += 1
        return f"label_{label}_{self.__labels_count}"

    def __build_CART(self) -> None:
        """
        CART: Context Aware Runtime Table.\
        Esta estructura almacena datos relacionados con la jerarquia de clases definida en el programa. CART se debe almacenar \
        en la seccion .DATA y sera usada por metodos relacionados con chequeo de tipos en tiempo de ejecucion. La estructura es una \
        tabla LCA, o sea, una tabla donde dadas dos clases A y B, CART[A, B] = C donde C es otra clase y se cumple que \
        A < C, B < C, y C es la primera clase en la jerarquia que partiendo de A o de B, cumple esa condicion; el operador \
        '<' significa "se conforma en" o "es subclase de".
        """

        # Crear el grafo de herencia basado en el contexto que tenemos hasta el momento.
        graph = InheritanceGraph()
        for itype in self.context.types:
            if self.context.types[itype].parent is not None:
                graph.add_edge(self.context.types[itype].parent.name, itype)  # type: ignore

        # Crear la tabla LCA
        graph.build_lca_table()
        self.lca_table = graph._lcatable

        # Procesar la tabla LCA para hacerla accesible en runtime
        # Para crear la tabla solo tenemos que definir varias etiquetas que describan
        # los tipos, y cada celda de la tabla contiene la direccion de estas etiquetas
        data_nodes_dict: Dict[str, nodes.DataNode] = {}
        for itype in self.context.types:
            data_node = self.register_data(itype)
            data_nodes_dict[itype] = data_node


    def __build_builtins(self):
        pass
