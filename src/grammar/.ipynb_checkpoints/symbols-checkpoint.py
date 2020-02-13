
class Symbol(object):
	"""
	Modelaremos los símbolos del lenguaje con la clase Symbol.
	Esta clase funcionará como base para la definición de terminales y no terminales.
	Entre las funcionalidades básicas de los símbolos tenemos que:

    -Pueden ser agrupados con el operador + para formar oraciones.
    -Podemos conocer si representa la cadena especial epsilon a través de la propiedad IsEpsilon
     que poseen todas las instancias.
    -Podemos acceder a la gramática en la que se definió a través del campo Grammar de cada
     instancia.
    -Podemos consultar la notación del símbolo a través del campo Name de cada instancia.

	Los símbolos no deben ser instanciados directamente (ni sus descendiente) con la aplicación
	de su constructor.
	"""

	def __init__(self, name, grammar):
		self.Name = name
		self.Grammar = grammar

	def __str__(self):
		return self.Name

	def __repr__(self):
		return repr(self.Name)

	def __add__(self, other):
	    if isinstance(other, Symbol):
	        return Sentence(self, other)

	    raise TypeError(other)

	def __or__(self, other):

	    if isinstance(other, (Sentence)):
	        return SentenceList(Sentence(self), other)

	    raise TypeError(other)

	@property
	def IsEpsilon(self):
	    return False

	def __len__(self):
	    return 1


class Terminal(Symbol):
	"""
	Los símbolos terminales los modelaremos con la clase Terminal.
	Dicha clase extiende la clase Symbol para:

    -Incluir propiedades IsNonTerminal - IsTerminal que devolveran True - False respectivamente.

	Los terminales no deben ser instanciados directamente con la aplicación de su constructor.
	"""

	def __init__(self, name, grammar):
	    super().__init__(name, grammar)

	@property
	def IsTerminal(self):
	    return True

	@property
	def IsNonTerminal(self):
	    return False

	@property
	def IsEpsilon(self):
	    return False


class NonTerminal(Symbol):
	"""
	Los símbolos no terminales los modelaremos con la clase NonTerminal.
	Dicha clase extiende la clase Symbol para:

    -Añadir noción de las producción que tiene al no terminal como cabecera.
     Estas pueden ser conocidas a través del campo productions de cada instancia.
    -Permitir añadir producciones para ese no terminal a través del operador %=.
    -Incluir propiedades IsNonTerminal - IsTerminal que devolveran True - False respectivamente.

	Los no terminales no deben ser instanciados directamente con la aplicación de su constructor.
	"""

	def __init__(self, name, grammar):
	    super().__init__(name, grammar)
	    self.productions = []

	def __imod__(self, other):

	    if isinstance(other, (Sentence)):
	        p = Production(self, other)
	        self.Grammar.Add_Production(p)
	        return self

	    # if isinstance(other, tuple):
	    #     assert len(
	    #         other) == 2, "Tiene que ser una Tupla de 2 elementos (sentence, attribute)"
		#
	    #     if isinstance(other[0], Symbol):
	    #         p = AttributeProduction(self, Sentence(other[0]), other[1])
	    #     elif isinstance(other[0], Sentence):
	    #         p = AttributeProduction(self, other[0], other[1])
	    #     else:
	    #         raise Exception("")
		#
	    #     self.Grammar.Add_Production(p)
	    #     return self

		if isinstance(other, tuple):
			assert len(other) > 1

	        if len(other) == 2:
	            other += (None,) * len(other[0])

	        assert len(other) == len(other[0]) + 2, "Debe definirse una, y solo una, regla por cada símbolo de la producción"

			if isinstance(other[0], Symbol) or isinstance(other[0], Sentence):
	            p = AttributeProduction(self, other[0], other[1:])
	        else:
	            raise Exception("")

	        self.Grammar.Add_Production(p)
	        return self

	    if isinstance(other, Symbol):
	        p = Production(self, Sentence(other))
	        self.Grammar.Add_Production(p)
	        return self

	    if isinstance(other, SentenceList):

	        for s in other:
	            p = Production(self, s)
	            self.Grammar.Add_Production(p)

	        return self

	    raise TypeError(other)

	@property
	def IsTerminal(self):
	    return False

	@property
	def IsNonTerminal(self):
	    return True

	@property
	def IsEpsilon(self):
	    return False


class EOF(Terminal):
	"""
	Modelaremos el símbolo de fin de cadena con la clase EOF.
	Dicha clase extiende la clases Terminal para heradar su comportamiento.

	La clase EOF no deberá ser instanciada directamente con la aplicación de su constructor.
	En su lugar, una instancia concreta para determinada gramática G de Grammar se construirá
	automáticamente y será accesible a través de G.EOF.
	"""

	def __init__(self, Grammar):
	    super().__init__('$', Grammar)


class Sentence(object):
	"""
	Modelaremos los oraciones y formas oracionales del lenguaje con la clase Sentence.
	Esta clase funcionará como una colección de terminales y no terminales.
	Entre las funcionalidades básicas que provee tenemos que nos :

    -Permite acceder a los símbolos que componen la oración a través del campo _symbols de
     cada instancia.
    -Permite conocer si la oración es completamente vacía a través de la propiedad IsEpsilon.
    -Permite obtener la concatenación con un símbolo u otra oración aplicando el operador +.
    -Permite conocer la longitud de la oración (cantidad de símbolos que la componen)
     utilizando la función build-in de python len(...).

	Las oraciones pueden ser agrupadas usando el operador |.
	Esto nos será conveniente para definir las producciones tengan la misma cabecera
	(no terminal en la parte izquierda) en una única sentencia.
	El grupo de oraciones se maneja con la clase SentenceList.

	No se deben crear instancias de Sentence y SentenceList directamente
	con la aplicación de los respectivos constructores.
	En su lugar, usaremos el operador + entre símbolos para formar las oraciones,
	y el operador | entre oraciones para agruparlas.
	"""

	def __init__(self, *args):
	    self._symbols = tuple(x for x in args if not x.IsEpsilon)
	    self.hash = hash(self._symbols)

	def __len__(self):
	    return len(self._symbols)

	def __add__(self, other):
	    if isinstance(other, Symbol):
	        return Sentence(*(self._symbols + (other,)))

	    if isinstance(other, Sentence):
	        return Sentence(*(self._symbols + other._symbols))

	    raise TypeError(other)

	def __or__(self, other):
	    if isinstance(other, Sentence):
	        return SentenceList(self, other)

	    if isinstance(other, Symbol):
	        return SentenceList(self, Sentence(other))

	    raise TypeError(other)

	def __repr__(self):
	    return str(self)

	def __str__(self):
	    return ("%s " * len(self._symbols) % tuple(self._symbols)).strip()

	def __iter__(self):
	    return iter(self._symbols)

	def __getitem__(self, index):
	    return self._symbols[index]

	def __eq__(self, other):
	    return self._symbols == other._symbols

	def __hash__(self):
	    return self.hash

	@property
	def IsEpsilon(self):
	    return False

class SentenceList(object):

    def __init__(self, *args):
        self._sentences = list(args)

    def Add(self, symbol):
        if not symbol and (symbol is None or not symbol.IsEpsilon):
            raise ValueError(symbol)

        self._sentences.append(symbol)

    def __iter__(self):
        return iter(self._sentences)

    def __or__(self, other):
        if isinstance(other, Sentence):
            self.Add(other)
            return self

        if isinstance(other, Symbol):
            return self | Sentence(other)

class Epsilon(Terminal, Sentence):
	"""
	Modelaremos tanto la cadena vacía como el símbolo que la representa: epsilon (ϵ),
	en la misma clase: Epsilon.
	Dicha clase extiende las clases Terminal y Sentence por lo que ser comporta como ambas.
	Sobreescribe la implementación del método IsEpsilon para indicar que en efecto toda instancia
	de la clase reprensenta epsilon.

	La clase Epsilon no deberá ser instanciada directamente con la aplicación de su constructor.
	En su lugar, una instancia concreta para determinada gramática G de Grammar se construirá
	automáticamente y será accesible a través de G.Epsilon.
	"""

	def __init__(self, grammar):
	    super().__init__('epsilon', grammar)


	def __str__(self):
	    return "e"

	def __repr__(self):
	    return 'epsilon'

	def __iter__(self):
	    yield self

	def __len__(self):
	    return 0

	def __add__(self, other):
	    return other

	def __eq__(self, other):
	    return isinstance(other, (Epsilon,))

	def __hash__(self):
	    return hash("")

	@property
	def IsEpsilon(self):
	    return True


class Production(object):
	"""
	Modelaremos las producciones con la clase Production. Las funcionalidades básicas
	con que contamos son:

    -Poder acceder la cabecera (parte izquierda) y cuerpo (parte derecha) de cada
     producción a través de los campos Left y Right respectivamente.
    -Consultar si la producción es de la forma X→ϵ a través de la propiedad IsEpsilon.
    -Desempaquetar la producción en cabecera y cuerpo usando asignaciones: left, right = production.

	Las producciones no deben ser instanciadas directamente con la aplicación de su constructor.
	En su lugar, se presentan las siguientes facilidades para formar producciones a partir
	de una instancia G de Grammar y un grupo de terminales y no terminales:

    Para definir una producción de la forma E→E+T:

  	E %= E + plus + T

	Para definir múltiples producciones de la misma cabecera en una única sentencia (E→E+T | E−T | T):

  	E %= E + plus + T | E + minus + T | T

	Para usar epsilon en una producción (ejemplo S→aS | ϵ) haríamos:

  	S %= S + a | G.Epsilon
	"""

	def __init__(self, nonTerminal, sentence):

		self.Left = nonTerminal
		self.Right = sentence

	def __str__(self):

         return '%s := %s' % (self.Left, self.Right)

	def __repr__(self):

		return '%s -> %s' % (self.Left, self.Right)

	def __iter__(self):
		yield self.Left
		yield self.Right

	def __eq__(self, other):
	    return isinstance(other, Production) and self.Left == other.Left and self.Right == other.Right


	@property
	def IsEpsilon(self):
	    return self.Right.IsEpsilon

class AttributeProduction(Production):
	"""
	Con esta clase modelaremos las producciones de las gramáticas atributadas.
	Cada una de estas producciones se compone por:

    Un no terminal como cabecera. Accesible a través del campo Left.
    Una oración como cuerpo. Accesible a través del campo Right.
    Un conjunto de reglas para evaluar los atributos. Accesible a través del campo atributes.

	Las producciones no deben ser instanciadas directamente con la aplicación de su constructor.
	En su lugar, se presentan las siguientes facilidades para formar producciones a partir de una
	instancia G de Grammar y un grupo de terminales y no terminales:

    Para definir una producción de la forma B0→B1B2...Bn que:

    -Asocia a B0 una regla λ0 para sintetizar sus atributos, y Asocia a B1…Bn las reglas λ1…λn
	que hereden sus atributos respectivamentes.

    B0 %= B1 + B2 + ... + Bn, lambda0, lambda1, lambda2, ..., lambdaN

    Donde lambda0, lambda1, ..., lambdaN son funciones que reciben 2 parámetros.

    Como primer parámetro los atributos heredados que se han computado para cada instancia
    de símbolo en la producción, durante la aplicación de esa instancia de producción específicamente.
    Los valores se acceden desde una lista de n + 1 elementos. Los valores se ordenan según aparecen
    los símbolos en la producción, comenzando por la cabecera. Nos referiremos a esta colección como inherited.
    Como segundo parámetro los atributos sintetizados que se han computado para cada instancia de símbolo
    en la producción, durante la aplicación de esa instancia de producción específicamente.
    Sigue la misma estructura que el primer parámetro. Nos referiremos a esta colección como synteticed.

    La función lambda0 sintetiza los atributos de la cabecera.
    La evaluación de dicha función produce el valor de synteticed[0].
    El resto de los atributos sintetizados de los símbolos de la producción se calcula de la siguiente forma:

    -En caso de que el símbolo sea un terminal, evalúa como su lexema.
    -En caso de que el símbolo sea un no terminal, se obtiene de evaluar la función lambda0 en la
     instancia de producción correspondiente.

    La función lambda_i, con i entre 1 y n, computa los atributos heredados de la i-ésima ocurrencia
     de símbolo en la producción. La evaluación de dicha función produce el valor de inherited[i].
     El valor de inherited[0] se obtiene como el atributo que heredó la instancia concreta del símbolo
     en la cabecera antes de comenzar a aplicar la producción.

    En caso de que no se vaya a sociar una regla a un símbolo se incluirá un None.

         E %= T X    ,  lambda h,s: s[2]  ,    None    ,   lambda h,s: s[1]
      # ___________     ________________     ________      ________________
      # producción  |    regla para E    |  sin regla  |     regla para X

        [0]: lambda h,s: s[2] al ser lambda0 sintetiza el valor de E. Lo hace en función del valor que
        	 sintetiza X (accesible desde s[2]).
        [1]: None al ser lambda1 indica que no se incluye regla para heredar valor a T.
        [2]: lambda h,s: s[1] al ser lambda2 hereda un valor a X. Lo hace en función del valor que sintetiza T
        	 accesible desde s[1]).

    No se deben definir múltiples producciones de la misma cabecera en una única sentencia.

	"""

	def __init__(self, nonTerminal, sentence, attributes):
	    if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
	        sentence = Sentence(sentence)
	    super(AttributeProduction, self).__init__(nonTerminal, sentence)

	    self.attributes = attributes

	def __str__(self):
	    return '%s := %s' % (self.Left, self.Right)

	def __repr__(self):
	    return '%s -> %s' % (self.Left, self.Right)

	def __iter__(self):
	    yield self.Left
	    yield self.Right


	@property
	def IsEpsilon(self):
	    return self.Right.IsEpsilon
