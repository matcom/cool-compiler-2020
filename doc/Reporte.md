# Reporte sobre el desarrollo del compilador
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

### Codegen
Usando el AST que ya pasó por el semántico y con cierta información de tipos estáticos agregada procedemos a la generación de código intermedio que más tarde se utilizará para producir código MIPS; todo mediante el uso del patrón visitor.

#### CIL
Los componentes del lenguaje CIL son bastante simples. Se encuentra integrado por:
* Instrucciones de a lo sumo dos operadores y un destino.
* Definición de Strings como Data:
* Definición de métodos como globales, que contienen las instrucciones, una lista de parámetros y de variables locales.
* Definición de clases con un mapeo de sus nombres de métodos a los globales, así como definición de sus atributos. En esta definición se incluyen elementos que le pertenecen a su padre antes de los propios, conservando el orden en que se encuentran en el padre.
* Programa CIL, que contiene todo lo anterior.

Con el patrón visitor se transforma del AST de entrada a un programa CIL de salida.  

#### MIPS
Dado el programa CIL se lleva a una transformación a MIPS.  
Una parte importante para entender la estructura es la representación de las clases. Toda clase se guarda como una referencia a un conjunto de palabras, de las cuales la primera siempre es una referencia a su definición de clase y el resto son los atributos.

##### Qué es la definición de clase?
Se puede observar al inicio del programa con la forma *Nombreclase: .word Padreclase, f1, f2...*, que no es más que una ubicación en el heap donde se encuentra guardada la direccion de la definicion de su clase padre, seguida por las direcciones de sus métodos

##### Llamada a un método
La llamada a los métodos tiene un indicador de la posición relativa a su definición de clase. Cuando se llama un método se accede a dicha definición a través de la clase o no, dependiendo del tipo de Dispatch y se llama el método en la posición indicada. En el caso de tipos base, como Int, String y Bool siempre se realiza StaticDispatch al final.

##### Estructura del programa
* Datos y cadenas predefinidas
* Strings
* Definiciones de clase
* Llamada al Main.Special desde el main
* Métodos predefinidos
* Métodos globales del programa

#### Uso de registros
* Registros $a#: Se usan para pasarle parámetros a los métodos en el interior de los métodos se evita su uso y en caso de necesitar usarlos, primero se guardan en la pila para luego restaurarlos. El único caso en que se modifican es si es especificado por el código CIL recibido.
* Registros $s#: Se deben salvar antes de utilizarlos, para luego restaurarlos. No tienen reservada una función específica
* Registros $t#: No necesitan ser salvados antes de utilizarlos. Internamente se utilizan en casi cada conversión a MIPS como lugar donde se cargan los parámetros CIL de la instrucción origen
* Registro $v0: No necesita ser salvado en sus operaciones.Se utiliza para el valor de retorno de las funciones, así como de destino intermedio en la conversión a MIPS. $v1 no se usa
El resto de los registros tiene una función asignada por el estándar de MIPS que no se violó. nos referimos a $ra, $sp, etc.  
Alguna regla se violó en el código estático, debido a que solo se usa en circunstancias específicas y basado en el modelo de programación seguido
  
#### Tipos en tiempo de ejecución
Esto proviene de un tipo CIL que pide inferencia de tipos. Lo que se utiliza es la definición de clase. Se pregunta si tu definición de clase es la buscada, en caso de no serlo se compara con la del padre, y sucesivamente con la de su padre; si en estos casos se encuentra una respuesta afirmativa se retorna verdadero. En caso de ver que llegaste a una clase sin padre(Object), es decir padre igual a 0, se retorna falso.