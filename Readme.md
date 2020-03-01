# COOL: Proyecto de Compilación

La evaluación de la asignatura Complementos de Compilación, inscrita en el programa del 4to año de la Licenciatura en Ciencia de la Computación de la Facultad de Matemática y Computación de la
Universidad de La Habana, consiste este curso en la implementación de un compilador completamente
funcional para el lenguaje _COOL_.

_COOL (Classroom Object-Oriented Language)_ es un pequeño lenguaje que puede ser implementado con un esfuerzo razonable en un semestre del curso. Aun así, _COOL_ mantiene muchas de las características de los lenguajes de programación modernos, incluyendo orientación a objetos, tipado estático y manejo automático de memoria.

### Sobre el Lenguaje COOL

Ud. podrá encontrar la especificación formal del lenguaje COOL en el documento _"COOL Language Reference Manual"_, que se distribuye junto con el presente texto.

## Código Fuente

### Compilando su proyecto

Si es necesario compilar su proyecto, incluya todas las instrucciones necesarias en un archivo [`/src/makefile`](/src/makefile).
Durante la evaluación su proyecto se compilará ejecutando la siguiente secuencia:

```bash
$ cd source
$ make clean
$ make
```

### Ejecutando su proyecto

Incluya en un archivo [`/src/coolc.sh`](/src/coolc.sh) todas las instrucciones que hacen falta para lanzar su compilador. Recibirá como entrada un archivo con extensión `.cl` y debe generar como salida un archivo `.mips` cuyo nombre será el mismo que la entrada.

Para lanzar el compilador, se ejecutará la siguiente instrucción:

```bash
$ cd source
$ ./coolc.sh <input_file.cl>
```

### Sobre el Compilador de COOL

El compilador de COOL se ejecutará como se ha definido anteriormente.
En caso de que no ocurran errores durante la operación del compilador, **coolc.sh** deberá terminar con código de salida 0, generar (o sobrescribir si ya existe) en la misma carpeta del archivo **.cl** procesado, y con el mismo nombre que éste, un archivo con extension **.mips** que pueda ser ejecutado con **spim**. Además, reportar a la salida estándar solamente lo siguiente:

    <línea_con_nombre_y_versión_del_compilador>
    <línea_con_copyright_para_el_compilador>

En caso de que ocurran errores durante la operación del compilador, **coolc.sh** deberá terminar con código
de salida (exit code) 1 y reportar a la salida estándar (standard output stream) lo que sigue...

    <línea_con_nombre_y_versión_del_compilador>
    <línea_con_copyright_para_el_compilador>
    <línea_de_error>_1
    ...
    <línea_de_error>_n

... donde `<línea_de_error>_i` tiene el siguiente formato:

    (<línea>,<columna>) - <tipo_de_error>: <texto_del_error>

Los campos `<línea>` y `<columna>` indican la ubicación del error en el fichero **.cl** procesado. En caso
de que la naturaleza del error sea tal que no pueda asociárselo a una línea y columna en el archivo de
código fuente, el valor de dichos campos debe ser 0.

El campo `<tipo_de_error>` será alguno entre:

- `CompilerError`: se reporta al detectar alguna anomalía con la entrada del compilador. Por ejemplo, si el fichero a compilar no existe.
- `LexicographicError`: errores detectados por el lexer.
- `SyntacticError`: errores detectados por el parser.
- `NameError`: se reporta al referenciar un `identificador` en un ámbito en el que no es visible.
- `TypeError`: se reporta al detectar un problema de tipos. Incluye:
    - incompatibilidad de tipos entre `rvalue` y `lvalue`,
    - operación no definida entre objetos de ciertos tipos, y
    - tipo referenciado pero no definido.
- `AttributeError`: se reporta cuando un atributo o método se referencia pero no está definido.
- `SemanticError`: cualquier otro error semántico.

### Sobre la Implementación del Compilador de COOL

El compilador debe estar implementado en `python`. Usted debe utilizar una herramienta generadora de analizadores
lexicográficos y sintácticos. Puede utilizar la que sea de su preferencia.
