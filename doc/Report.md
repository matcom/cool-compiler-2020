# `coolcmp`

Nuestro compilador `coolcmp` está finalmente terminado. En este reporte exponemos el proceso de construcción del compilador, las decisiones de diseño y el uso del mismo.

## Usando `coolcmp`

TODO: opciones....

# Estructura del proyecto

El proyecto se divide en varios módulos:

En la carpeta `/src/coolcmp` tenemos:

- `main.py` es el punto de entrada del proyecto.

- `cmp/ast_cls.py` contiene la definición de los nodos de cada [Abstract Syntax Tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) (_AST_) creado (_Parser_ y _CIL_).

- `cmp/constants.py` contiene constantes usadas por la fase de generación de código principalmente.

- `cmp/environment.py` representa un [entorno](https://craftinginterpreters.com/statements-and-state.html#environments), esto es básicamente un mapa que hace corresponder cada nombre de variable con información sobre su definición.

- `cmp/errors.py` contiene los posibles errores que puede dar el compilador (a excepción de los runtime errors).

- `cmp/gen_cil.py` se encarga de generar código _CIL_.
  
- `cmp/gen_mips.py` se encarga de generar código _MIPS_.

- `cmp/lexer.py` contiene la definición y métodos del lexer.
  
- `cmp/parser.py` contiene la definición y métodos del parser.
  
- `cmp/parse_tab.py` archivo generado automáticamente por `ply`.

- `cmp/print_ast.py` se encarga de imprimir un _AST_ por consola.
  
- `cmp/semantics.py` se encarga del análisis semántico.

- `cmp/source_code.py` representa un código fuente de _Cool_.

- `cmp/type_checker.py` se encarga del chequeo de tipos.

- `cmp/utils.py` define un logger para debuggear.

En la carpeta `/src/unit_tests` tenemos varias pruebas unitarias con las que probamos nuestro compilador (leer el fichero `/src/unit_tests/README.md` para más información).

# Fases de construcción de `coolcmp`

El desarrollo del compilador se realizó en varias fases, cada una planteando una serie de problemas interesantes a resolver:

## Análisis Léxico

En esta fase realizamos el análisis léxico usando el lexer de la herramienta `ply`.

## Análisis Sintáctico

En primer lugar convertimos la gramática de _Cool_, que se encuentra en la forma extendida de la notación de [Backus-Naur](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) (tiene expresiones regulares, por ejemplo), a la forma estándar.

A continuación creamos un pequeño script que genera un "esqueleto" del fichero `parser.py`, el cual contiene cada una de las reglas de la gramática como un método de la clase `Parser`, lo cual es requerido por el parser la herramienta `ply`.

Procedemos a completar cada uno de los métodos con la parte derecha de cada regla. Para esto creamos todas las clases necesarias para modelar cada símbolo de la gramática, estas clases serían los nodos del _AST_. A estas clases añadimos la información de línea y columna en la que se encuentra su símbolo correspondiente.

## Análisis Semántico

Verificamos las reglas semánticas de _Cool_ especificadas en el manual.

### Árbol de Herencia

Procedemos a la creación del árbol de herencia, esto es, un árbol donde cada nodo representa una clase, en el que el nodo $u$ tiene como hijo a $v$ si la clase $v$ hereda de $u$. Notemos además, que este árbol tiene como raíz a la clase _Object_.

Al tener el grafo creado, chequeamos que sea un árbol. Esto lo hacemos con el clásico algoritmo de detección de ciclos en grafos dirigidos, esto es, hacemos un [Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search) (_DFS_) que va visitando los nodos, si estamos en el nodo $u$, vamos al nodo $v$ y detectamos que $v$ es ancestro de $u$ en el [_DFS-tree_](https://en.wikipedia.org/wiki/Depth-first_search#Output_of_a_depth-first_search)[^1] podemos afirmar que existe un ciclo. El siguiente código realiza este _DFS_:

```python
def check_cycles(self):
    seen = {}
    up = {}

    for cls in self.ast_root.cls_list:
        if cls.type.value not in seen:
            self._dfs(cls, seen, up)

def _dfs(self, u, seen, up):
    seen[u.type.value] = up[u.type.value] = True

    for v in u.children:
        if v.type.value not in seen:
            self._dfs(v, seen, up)

        elif up[v.type.value]:
            raise SemanticError(v.type.line, v.type.col, f'Inheritance cycle detected')

    up[u.type.value] = False
```

Podemos notar que este árbol de herencia representa perfectamente la relación de _Conformance_ definida en el manual de _Cool_. Más aún, desde el punto de vista de nuestro árbol podemos afirmar que $A \le B \iff B \text{ es ancestro de } A$.

### Sobre _SELF_TYPE_

_SELF_TYPE_ cumple lo siguiente con respecto a _Conformance_:

1. $\text{SELF\_TYPE}_{X} \le \text{SELF\_TYPE}_{X}$
2. $\text{SELF\_TYPE}_{C} \le P$ si $C \le P$

Nuestro árbol de herencia actual no maneja _SELF_TYPE_, pero podemos manejarlo fácilmente si decimos que cada nodo $C$ tiene un hijo $\text{SELF\_TYPE}_{C}$. De esta forma, el punto $1$ obviamente se cumple, y el punto $2$ también dado que si $P$ es ancestro de $C$, también lo es de $\text{SELF\_TYPE}_{C}$, porque $\text{SELF\_TYPE}_{C}$ es hijo de $C$.

## Chequeo de Tipos

Realizamos el chequeo de tipos usando [visitor pattern](https://en.wikipedia.org/wiki/Visitor_pattern); cumpliendo con las especificaciones en el manual de _Cool_. En esta fase surgen algunos problemas interesantes:

### Conformance Test

Nos hace falta poder responder rápido si un nodo $u$ conforma con $v$ o no. Esto es posible hacerlo en $O(1)$ por cada pregunta. Para esto hacemos un _DFS_ por nuestro árbol de herencia calculando dos valores para cada nodo $x$:

- $\text{td}(x) =$ tiempo de descubrimiento del nodo $x$, esto es, el primer momento en el que el _DFS_ llega a $x$.
- $\text{tf}(x) =$ tiempo de finalización del nodo $x$, esto es, el último momento en el que el _DFS_ está en $x$ (cuando la recursión va a "salir" de $x$).

Sería algo como:

```python
def _dfs(self, u):
    self._t += 1
    u.td = self._t

    for v in u.children:
        self._dfs(v)
    
    u.tf = self._t
```

Luego $u$ conforma con $v$ si $\text{td}(v) \le \text{td}(u) \le \text{tf}(v)$. Esta es una de las tantas propiedades del _DFS-tree_[^2].

### Lowest Common Ancestor

Necesitamos poder contestar preguntas de [Lowest Common Ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) (_LCA_) para realizar la operación "join" descrita en el manual. Para esto hay muchos algoritmos que van desde $O(n)$ por pregunta hasta $O(1)$ con $O(n \log n)$ de pre-procesamiento[^3]. Decidimos no complicarnos e implementamos uno de complejidad lineal por pregunta, este algoritmo es simple:

- supongamos que $u$ está mas lejos de la raíz que $v$ (sino, intercambiamos $u$ con $v$), entonces $lca(u, v) = lca(p(u), v)$, donde $p(u)$ es el padre de $u$. Seguimos haciendo esto mientras que $u \neq v$.
- cuando $u = v$ el _LCA_ es $u$.

## Generación de código CIL

## Generación de código MIPS

[^1]: El [_DFS-tree_](https://en.wikipedia.org/wiki/Depth-first_search#Output_of_a_depth-first_search) de un grafo es un [Spanning Tree](https://en.wikipedia.org/wiki/Spanning_tree) obtenido por una pasada de _DFS_.

[^2]: Para más información, incluida demostración, revisar el [CLRS](https://en.wikipedia.org/wiki/Introduction_to_Algorithms), epígrafe $22.3$ sobre _Depth First Trees_.

[^3]: Incluso existe un algoritmo offline (todas las preguntas se saben de antemano) que funciona en $O(1)$ por pregunta con $O(n)$ de pre-procesamiento.