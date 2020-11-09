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

## Chequeo de Tipos

## Generación de código CIL

## Generación de código MIPS