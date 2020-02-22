'''
Contenedor para la funcion que construye la gramatica de cool.
'''
from grammar.grammar import Grammar
from abstract.tree import ProgramNode, ClassDef, MethodDef, AttributeDef, Param, VariableDeclaration
from abstract.tree import PlusNode, DivNode, MulNode, DifNode, IntegerConstant, FunCall
from abstract.tree import VariableCall, FalseConstant, StringConstant, GreaterThanNode, TrueConstant
from abstract.tree import GreaterEqualNode, LowerThanNode, LowerEqual, AssignNode, IfThenElseNode
from abstract.tree import NotNode, WhileBlockNode, EqualToNode, InstantiateClassNode
from abstract.tree import ActionNode, CaseNode, ParentFuncCall, BlockNode, IsVoidNode
from lexer.tokenizer import Lexer


def build_cool_grammar():
    G = Grammar()
    program = G.NonTerminal('<program>', True)

    class_list, class_def, empty_feature_list, feature_list, meod_def = \
        G.NonTerminals(
            '<class_list> <class_def> <empty_feature_list> <feature_list> <meod_def>')

    attr_def, param_list, param, statement_list = G.NonTerminals(
        '<attr_def> <param_list> <param> <statement_list>')

    var_dec, args_list, instantiation = G.NonTerminals(
        '<var_dec> <args_list> <instantiation>')

    exp, typex, term, factor, nested_lets = G.NonTerminals(
        '<exp> <type> <term> <factor> <nested_lets>')

    arith, atom, actions, action, block = G.NonTerminals(
        '<arith> <atom> <actions> <action> <block>')

    args_list_empty, param_list_empty, case_statement, string_const = G.NonTerminals(
        '<args_list_empty> <param_list_empty> <case> <string_const>')

    class_keyword, def_keyword, in_keyword = G.Terminals('class def in')

    coma, period, dot_comma, opar, cpar, obrack, cbrack, plus, minus, star, div, dd = G.Terminals(
        ', . ; ( ) { } + - * / :')

    idx, let, intx, string, num, equal, true, false, boolean, objectx, classid =\
        G.Terminals('id let int string num = true false bool object classid')

    tilde_string_const, quoted_string_const, void, auto = G.Terminals(
        'tilde_string_const quoted_string_const void AUTO_TYPE')

    if_, then, else_, assign, new, case, of, esac = G.Terminals(
        'if then else assign new case of esac')

    gt, lt, ge, le, eq, not_, implies, isvoid = G.Terminals(
        '> < >= <= == ~ => isvoid')

    while_, do, inherits, arroba, fi, pool, loop = G.Terminals(
        'while do inherits @ fi pool loop')

    # Definir un programa como un conjunto de clases.
    program %= class_list, lambda s: ProgramNode(s[1])

    # Definir un conjunto de clases como una clase o una clase mas una lista de clases.
    class_list %= class_def + dot_comma, lambda s: [s[1]]
    class_list %= class_def + dot_comma + class_list, lambda s: [s[1]] + s[2]

    # Definir la estructura de la declaracion de una clase.
    # Una clase no es mas que un conjunto de features.
    class_def %= class_keyword + classid + obrack + feature_list + cbrack, lambda s: ClassDef(
        s[2], s[4])

    # Definir la estructura de la declaracion de una clase con herencia.
    class_def %= class_keyword + classid + inherits + typex + obrack + feature_list + \
        cbrack + dot_comma, lambda s: ClassDef(s[2], s[6], s[4])

    # Definir un conjunto de features como un metodo unico.
    feature_list %= meod_def + dot_comma, lambda s: [s[1]]

    # Definir un conjunto de features como un unico atributo.
    feature_list %= attr_def + dot_comma, lambda s: [s[1]]

    # Definir una lista de features como la declaracion de un metodo
    # mas una lista de features.
    feature_list %= meod_def + dot_comma + \
        feature_list, lambda s: [s[1]] + s[3]

    # Definir una lista de features como la declaracion de un atributo
    # mas una lista de features.
    feature_list %= attr_def + dot_comma + \
        feature_list, lambda s: [s[1]] + s[3]

    # Definir la estructura de la declaracion de un metodo.
    meod_def %= idx + opar + param_list_empty + cpar + dd + typex + obrack +\
        statement_list + cbrack , lambda s: MethodDef(s[1], s[3], s[6], s[8])

    # Definir la estructura de la declaracion de un atributo.
    attr_def %= idx + dd + typex, lambda s: AttributeDef(s[1], s[3])

    # Definir la estructura de la declaracion de un atributo con valor por defecto.
    attr_def %= idx + dd + typex + assign + \
        exp, lambda s: AttributeDef(s[1], s[3], s[5])

    # Definir la lista de parametros como una lista de parametros o una lista vacia
    param_list_empty %= param_list, lambda s: s[1]
    param_list_empty %= G.Epsilon, lambda s: []

    # Definir una lista de parametros como un parametro separado por coma con una lista
    # de parametros o simplemente un parametro
    param_list %= param, lambda s: [s[1]]
    param_list %= param + coma + param_list, lambda s: [s[1]] + s[3]

    # Definir un la estructura de un parametro como un identificador : Tipo
    param %= idx + dd + typex, lambda s: Param(s[1], s[3])

    # Definir una lista de sentencias como una expresion terminada en punto y coma o
    # una expresion y una lista de sentencias separadas por punto y coma.
    statement_list %= exp, lambda s: [s[1]]

    statement_list %= exp + dot_comma + statement_list, lambda s: [s[1]] + s[3]

    var_dec %= let + nested_lets + in_keyword + \
        exp, lambda s: VariableDeclaration(s[2], s[4])

    nested_lets %= idx + dd + typex, lambda s: [(s[1], s[3], None)]

    nested_lets %= idx + dd + typex + coma + \
        nested_lets, lambda s: [(s[1], s[3], None)] + s[5]

    nested_lets %= idx + dd + typex + assign + \
        exp, lambda s: [(s[1], s[3], s[5])]

    nested_lets %= idx + dd + typex + assign + exp + coma + \
        nested_lets, lambda s: [(s[1], s[3], s[5])] + s[7]

    # Una expresion puede ser una declaracion de una variable
    exp %= var_dec, lambda s: s[1]

    # Una expresion puede ser una constante (True, False, un string, un entero, etc)
    exp %= true, lambda s: TrueConstant()

    exp %= string_const, lambda s: s[1]

    string_const %= quoted_string_const, lambda s: StringConstant(s[1])

    string_const %= tilde_string_const, lambda s: StringConstant(s[1])

    exp %= false, lambda s: FalseConstant()

    # Una expresion puede ser una sentencia de comparacion
    exp %= atom, lambda s: s[1]

    # Una expresion puede ser un bloque IfThenElse
    exp %= if_ + exp + then + exp + else_ + exp + \
        fi, lambda s: IfThenElseNode(s[2], s[4], s[6])

    # Una expresion puede ser una asignacion
    exp %= idx + assign + exp, lambda s: AssignNode(s[1], s[3])

    # Una expresion puede ser una instanciacion de una clase
    #exp %= instantiation, lambda s: s[1]
    factor %= instantiation, lambda s: s[1]

    instantiation %= new + classid + opar + args_list_empty + \
        cpar, lambda s: InstantiateClassNode(s[2], s[4])

    instantiation %= new + classid, lambda s: InstantiateClassNode(s[2], [])

    # Una expresion puede ser un bloque while
    exp %= while_ + exp + loop + statement_list + \
        pool, lambda s: WhileBlockNode(s[3], s[7])

    exp %= arith, lambda s: s[1]

    exp %= block, lambda s: s[1]

    exp %= case_statement, lambda s: s[1]

    exp %= isvoid + exp, lambda s: IsVoidNode(s[2])

    block %= obrack + statement_list + cbrack, lambda s: BlockNode(s[2])

    arith %= arith + plus + term, lambda s: PlusNode(s[1], s[3])

    arith %= arith + minus + term, lambda s: DifNode(s[1], s[3])

    arith %= term, lambda s: s[1]

    term %= term + star + factor, lambda s: MulNode(s[1], s[3])

    term %= term + div + factor, lambda s: DivNode(s[1], s[3])

    term %= factor, lambda s: s[1]

    factor %= opar + arith + cpar, lambda s: s[2]

    factor %= num, lambda s: IntegerConstant(s[1])

    factor %= idx, lambda s: VariableCall(s[1])

    factor %= factor + period + idx + opar + args_list_empty + cpar, lambda s: FunCall(
        s[1], s[3], s[5])

    factor %= idx + opar + args_list_empty + \
        cpar, lambda s: FunCall('self', s[1], s[3])

    factor %= factor + arroba + typex + period + idx + opar + args_list_empty + cpar, lambda s: \
        ParentFuncCall(s[1], s[3], s[5], s[7])

    atom %= factor + gt + factor, lambda s: GreaterThanNode(s[1], s[3])

    atom %= factor + lt + factor, lambda s: LowerThanNode(s[1], s[3])

    atom %= factor + eq + factor, lambda s: EqualToNode(s[1], s[3])

    atom %= factor + ge + factor, lambda s: GreaterEqualNode(s[1], s[3])

    atom %= factor + le + factor, lambda s: LowerEqual(s[1], s[3])

    atom %= not_ + factor, lambda s: NotNode(s[2])

    typex %= intx, lambda s: 'int'

    typex %= boolean, lambda s: 'bool'

    typex %= string, lambda s: 'string'

    typex %= objectx, lambda s: 'object'

    typex %= classid, lambda s: s[1]

    typex %= auto, lambda s: 'AUTO_TYPE'

    typex %= void, lambda s: 'void'

    args_list_empty %= args_list, lambda s: s[1]

    args_list_empty %= G.Epsilon, lambda s: []

    args_list %= exp, lambda s: [s[1]]

    args_list %= exp + coma + args_list, lambda s: [s[1]] + s[3]

    actions %= action, lambda s: [s[1]]

    actions %= action + actions, lambda s: [s[1]] + s[2]

    action %= idx + dd + typex + implies + exp + \
        dot_comma, lambda s: ActionNode(s[1], s[3], s[5])

    case_statement %= case + exp + of + actions + \
        esac, lambda s: CaseNode(s[2], s[4])

    scaped_chars = r"(\a)|(\b)|(\c)|(\d)|(\e)|(\f)|(\g)|(\h)|(\i)|(\j)" +\
        r"|(\k)|(\l)|(\m)|(\n)|(\o)|(\p)|(\q)|(\r)|(\s)|(\t)|(\u)|(\v)|(\x)|(\y)|(\z)" +\
        r'|(!\")' + r"|(!\')"

    operators = r"!+|!*|!-|!/|!(|!)|!=|!:|!>|!<|!||!?|!#|!,"
    quoted_string = r'"(1|2|3|4|5|6|7|8|9|0|A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N' + r'|n|O|o|P|p|Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|! |' + scaped_chars + "|" + operators + ')*"'

    tilde_string = r"'(1|2|3|4|5|6|7|8|9|0|A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N' + r'|n|O|o|P|p|Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|! |" + scaped_chars + ")*'"

    table = [
        (class_keyword, 'class'),
        (def_keyword, 'def'),
        (in_keyword, 'in'),
        (intx, 'int'),
        (boolean, 'bool'),
        (objectx, 'object'),
        (string, 'string'),
        (true, ' true'),
        (false, 'false'),
        (auto, 'AUTO_TYPE'),
        (if_, 'if'),
        (then, 'then'),
        (else_, 'else'),
        (new, 'new'),
        (while_, 'while'),
        (do, 'do'),
        (esac, 'esac'),
        (case, 'case'),
        (of, 'of'),
        (inherits, 'inherits'),
        (coma, ','),
        (period, '.'),
        (dd, ':'),
        (dot_comma, ';'),
        (arroba, '@'),
        (assign, r'<!-'),
        (lt, r'!<'),
        (gt, r'!>'),
        (ge, '>='),
        (le, '<='),
        (eq, '=='),
        (not_, r'!~'),
        (equal, '='),
        (opar, r'!('),
        (cpar, r'!)'),
        (obrack, r'!{'),
        (cbrack, r'!}'),
        (plus, r'!+'),
        (minus, r'!-'),
        (implies, r'=>'),
        (div, '/'),
        (star, r'!*'),
        (let, 'let'),
        (fi, 'fi'),
        (pool, 'pool'),
        (loop, 'loop'),
        (isvoid, 'isvoid'),
        (idx, '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|' +
         'q|r|s|t|u|v|w|x|y|z)(A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N|n|O|o|P|p|'
         + 'Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|_|1|2|3|4|5|6|7|8|9|0)*'),
        (num, '(1|2|3|4|5|6|7|8|9|0)+'),
        (tilde_string_const, tilde_string),
        (quoted_string_const, quoted_string),
        (classid, '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|' +
         'Q|R|S|T|U|V|W|X|Y|Z)(A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N|n|O|o|P|p|'
         + 'Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|_|1|2|3|4|5|6|7|8|9|0)*'),
    ]

    lexer = Lexer(table, G.EOF, ignore_white_space=False)
    return G, lexer
