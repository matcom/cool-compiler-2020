# Reporte sobre el de desarrollo del compilador
En este reporte expondremos los requerimientos y forma de uso de nuestro compilador, además daremos un repaso sobre el diseño del mismo y sus distintas fases.
## Formas de uso y requeriminetos
Nuestro compilador fue desarrollado en el lenguaje **Python** y actualmente para ser usado solo necesita del uso de módulo **ply** del mismo.
Para ser ejecutado solo se debe dirigir a `\src` en nuetro proyecto y ejecutar `python TigerandButiCompiler.py {input}` donde _input_ sería la dirección del archivo a compilar, como resultado se obtendrá un arvhivo _.mips_ con el mismo nombre del archivo.
## Estructura del proyecto
La totalidad del mismo se halla en `\src` siendo *TigerandButiCompiler* nuestro archivo principal además de contener las definiciones del lexer y el parser y en _AST_ se define el AST generado por nuestro parser.   
Para la fase de chequeo semántico se creó *Semantics_Checking* donde se realiza el chequeo semántico, apoyándose en *Scope* donde se define el concepto de Scope y en *Cool_Type* donde se define el concepto de tipo de COOL además de definir los tipos básicos.  
En la fase de generación de código se adiconan bastantes nuevos elementos como *CIL* donde se define un AST para la versión de CIL utlizada en nuestro proceso de compilación, en *ASTtoCIL* se realiza el proceso de convertir nuestro, AST generado por el parser, en un nuevo AST de CIL y en *DefaultClasses* se definen las clases básicas de COOL como nodos del AST original para ser aprovechadas, además se definen algunos métodos útiles para convertir los llamados a métodos basicos en código MIPS. Luego en *CILtoMIPS* se realiza la conversión de nuestro AST de CIL en un código en MIPS, para hacerlo se apoyan en un Scope usado para este caso definido en *ScopeMIPS* y en el archivo *AssemblyMethods* dentro de `\StaticCode` donde se definen la mayor parte de de los métodos básicos en código MIPS.
## Fases de desarrollo
El proyecto fue dividido en disitintas fases para su implementación, estas fueron:
  1. Lexing
  2. Parsing
  3. Semantic Checking
  4. Code Generation

A continuación daremos un resumen de como se desarrollaron las mismas así como algunas de las problemáticas principales que hallamos
### Lexing
En esta fase se definieron los distintos tipos de tokens que se usarían posteriormente en nuestro parser. Gracias al uso de **ply** en su submódulo **lex** la definicón de los mismos fue bastante directa y legible.  
Para la creación de los tokens se define cual es su forma en strings mediante el uso de expresiones regulares y luego se crea el mismo mediante la aplicación de los métodos definidos por cada tipo de token.  
Es válido destacar que en el caso de los comentarios fue tomada la decisión de eliminarlos del texto del código en COOL mediante un preprocesamiento para hacer más facil nuestro trabajo.
### Parsing
Luego de obtener todos los tokens de nuestro programa de COOL gracias a **lex** los mismos son pasados a el otro submódulo de **ply** llamado **yacc**. En el mismo mediante una definicion de una gramática BNF, usando los tokens dados por el lexer usado anteriormente, se logra la creacón de un AST para el programa en COOL.  
El proceso de definición de esta dependió sobre todo de los nodos definidos en el AST de COOL, mencionado antes, y de la gramática para programas válidos de COOL dada por nosotros.  
Uno de los procesos mas engorrosos fueron los llamados a los distintos tipos de Dispatch ya que estos poseen varias definiciones según la forma en que se llame. Otra problemática que tuvimos fue debido al orden en que debía quedar el AST lo cual se solucionó mediante la declaración de la precedencia entre distintos operadores. 
### Semantic Checking
Ya teniendo el AST de COOL se puede pasar a chequearlo semánticamente, este proceso se realiza mediante el uso del patrón **visitor** con el cual comenzando desde el primero nodo del AST devuelto por **yacc**, se puede ir recorriendo la totalidad de estos.  
Durante todo este proceso de recorrido se van guardando las clases, variables, atributos y métodos mediante el concepto de Scope.  
Por cada nodo del AST se intenta inferir un tipo estático el cual es guardado en el mismo. Los errores que pueden levantarse en este proceso han sido definidos según el Manual de COOL para lograr su correcta implementación.   
Una problemática a destacar fue el caso de hallar las clases con herencia cíclica, este proceso se realiza al comienzo del chequeo tratando de por cada nodo de clase llegar al antecesor común ya definido, al comienzo este será Object, para luego definirse, si durante esta búsqueda se topa con un nodo que también está en medio del proceso significa que existe un ciclo por lo cual devolvemos el error. 
