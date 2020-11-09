# Documentación

**Nombre** | **Grupo** | **Github**
--|--|--
Antonio Otaño Barrera | C411 | [@AntonioJesus0398](https://github.com/AntonioJesus0398)
Denis Gómez Cruz      | C412 | [@dgc9715](https://github.com/dgc9715)
Daniel Enrique Cordovés Borroto | C411 | [@dcordb](https://github.com/dcordb)

## Readme

Para usar el compilador, nos movemos a `/src` y allí ejecutamos `python -m coolcmp -h` para mostrar la ayuda, esto da la siguiente salida:

```
usage: python -m coolcmp [-h] [--ast] [--cil_ast] [--tab_size TAB_SIZE] [--no_mips] file_path

Cool compiler programmed in Python.

positional arguments:
  file_path            Path to cool file to compile

optional arguments:
  -h, --help           show this help message and exit
  --ast                Print AST
  --cil_ast            Print CIL AST
  --tab_size TAB_SIZE  Tab size to convert tabs to spaces, default is 4
  --no_mips            Dont generate mips file
```

Por tanto, para compilar un fichero `code.cl` solo debemos hacer `python -m coolcmp code.cl`. Esto genera un fichero `code.mips`, el cual podemos ejecutar utilizando el simulador SPIM haciendo `spim -f code.mips`.

### Requisitos adicionales

- pytest
- pytest-ordering
- ply
- print-tree2

También estos se  encuentran en el fichero `/requirements.txt`.

### Sobre los Equipos de Desarrollo

Para desarrollar el compilador del lenguaje COOL se trabajará en equipos de 2 o 3 integrantes. El proyecto de Compilación será recogido y evaluado únicamente a través de Github. Es imprescindible tener una cuenta de Github para cada participante, y que su proyecto esté correctamente hosteado en esta plataforma. Próximamente les daremos las instrucciones mínimas necesarias para ello.

### Sobre los Materiales a Entregar

Para la evaluación del proyecto Ud. debe entregar un informe en formato PDF (`report.pdf`) que resuma de manera organizada y comprensible la arquitectura e implementación de su compilador.
El documento **NO** debe exceder las 5 cuartillas.
En él explicará en más detalle su solución a los problemas que, durante la implementación de cada una de las fases del proceso de compilación, hayan requerido de Ud. especial atención.

### Estructura del reporte

Usted es libre de estructurar su reporte escrito como más conveniente le parezca. A continuación le sugerimos algunas secciones que no deberían faltar, aunque puede mezclar, renombrar y organizarlas de la manera que mejor le parezca:

- **Uso del compilador**: detalles sobre las opciones de líneas de comando, si tiene opciones adicionales (e.j., `--ast` genera un AST en JSON, etc.). Básicamente lo mismo que pondrá en este Readme.
- **Arquitectura del compilador**: una explicación general de la arquitectura, en cuántos módulos se divide el proyecto, cuantas fases tiene, qué tipo de gramática se utiliza, y en general, como se organiza el proyecto. Una buena imagen siempre ayuda.
- **Problemas técnicos**: detalles sobre cualquier problema teórico o técnico interesante que haya necesitado resolver de forma particular.

## Sobre la Fecha de Entrega

Se realizarán recogidas parciales del proyecto a lo largo del curso. En el Canal de Telegram [@matcom_cmp](https://t.me/matcom_cmp) se anunciará la fecha y requisitos de cada primera entrega.
