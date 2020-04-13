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
from abstract.tree import NegNode
from lexer.tokenizer import Lexer
from tknizer import Tokenizer


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

    exp, typex, term, factor, nested_lets, loop_statements = G.NonTerminals(
        '<exp> <type> <term> <factor> <nested_lets> <loop_statements>')

    arith, atom, actions, action, block = G.NonTerminals(
        '<arith> <atom> <actions> <action> <block>')

    args_list_empty, param_list_empty, case_statement, string_const = G.NonTerminals(
        '<args_list_empty> <param_list_empty> <case> <string_const>')

    class_keyword, def_keyword, in_keyword = G.Terminals('class def in')

    coma, period, dot_comma, opar, cpar, obrack, cbrack, plus, minus, star, div, dd = G.Terminals(
        ', . ; ( ) { } + - * / :')

    idx, let, intx, string, num, true, false, boolean, objectx, classid =\
        G.Terminals('id let int string num true false bool object classid')

    tilde_string_const, quoted_string_const, void, auto = G.Terminals(
        'tilde_string_const quoted_string_const void AUTO_TYPE')

    if_, then, else_, assign, new, case, of, esac = G.Terminals(
        'if then else assign new case of esac')

    gt, lt, ge, le, eq, not_, implies, isvoid, not_operator = G.Terminals(
        '> < >= <= = ~ => isvoid not')

    while_, do, inherits, arroba, fi, pool, loop = G.Terminals(
        'while do inherits @ fi pool loop')

    program %= class_list, lambda s: ProgramNode(s[1])

    class_list %= class_def + dot_comma, lambda s: [s[1]]
    class_list %= class_def + dot_comma + class_list, lambda s: [s[1]] + s[2]

    class_def %= class_keyword + classid + obrack + feature_list + cbrack, lambda s: ClassDef(
        s[2], s[4])

    class_def %= class_keyword + classid + inherits + typex + obrack + feature_list + \
        cbrack, lambda s: ClassDef(s[2], s[6], s[4])

    feature_list %= meod_def + dot_comma, lambda s: [s[1]]

    feature_list %= attr_def + dot_comma, lambda s: [s[1]]

    feature_list %= meod_def + dot_comma + \
        feature_list, lambda s: [s[1]] + s[3]

    feature_list %= attr_def + dot_comma + \
        feature_list, lambda s: [s[1]] + s[3]

    meod_def %= idx + opar + param_list_empty + cpar + dd + typex + obrack +\
        statement_list + cbrack , lambda s: MethodDef(s[1], s[3], s[6], s[8])

    attr_def %= idx + dd + typex, lambda s: AttributeDef(s[1], s[3])

    attr_def %= idx + dd + typex + assign + \
        exp, lambda s: AttributeDef(s[1], s[3], s[5])

    param_list_empty %= param_list, lambda s: s[1]
    param_list_empty %= G.Epsilon, lambda s: []

    param_list %= param, lambda s: [s[1]]
    param_list %= param + coma + param_list, lambda s: [s[1]] + s[3]

    param %= idx + dd + typex, lambda s: Param(s[1], s[3])

    statement_list %= exp, lambda s: s[1]

    # statement_list %= exp + dot_comma + statement_list, lambda s: [s[1]] + s[3]

    var_dec %= let + nested_lets + in_keyword + \
        exp, lambda s: VariableDeclaration(s[2], s[4])

    nested_lets %= idx + dd + typex, lambda s: [(s[1], s[3], None)]

    nested_lets %= idx + dd + typex + coma + \
        nested_lets, lambda s: [(s[1], s[3], None)] + s[5]

    nested_lets %= idx + dd + typex + assign + \
        exp, lambda s: [(s[1], s[3], s[5])]

    nested_lets %= idx + dd + typex + assign + exp + coma + \
        nested_lets, lambda s: [(s[1], s[3], s[5])] + s[7]

    exp %= var_dec, lambda s: s[1]

    string_const %= quoted_string_const, lambda s: StringConstant(s[1])

    string_const %= tilde_string_const, lambda s: StringConstant(s[1])

    instantiation %= new + typex, lambda s: InstantiateClassNode(s[2], [])

    loop_statements %= exp + dot_comma, lambda s: [s[1]]
    loop_statements %= exp + dot_comma + loop_statements, lambda s: [s[1]] + s[
        3]

    exp %= idx + assign + exp, lambda s: AssignNode(s[1], s[3])

    exp %= while_ + exp + loop + statement_list + \
        pool, lambda s: WhileBlockNode(s[2], s[5])

    exp %= atom, lambda s: s[1]

    #exp %= opar + atom + cpar, lambda s: s[2]

    #exp %= arith, lambda s: s[1]

    exp %= block, lambda s: s[1]

    exp %= case_statement, lambda s: s[1]

    exp %= isvoid + exp, lambda s: IsVoidNode(s[2])

    block %= obrack + loop_statements + cbrack, lambda s: BlockNode(s[2])

    arith %= arith + plus + term, lambda s: PlusNode(s[1], s[3])

    arith %= arith + minus + term, lambda s: DifNode(s[1], s[3])

    arith %= term, lambda s: s[1]

    term %= term + star + factor, lambda s: MulNode(s[1], s[3])

    term %= term + div + factor, lambda s: DivNode(s[1], s[3])

    term %= factor, lambda s: s[1]

    term %= not_ + factor, lambda s: NotNode(s[2])

    term %= not_operator + factor, lambda s: NegNode(s[2])

    factor %= if_ + exp + then + exp + else_ + exp + fi, lambda s: IfThenElseNode(
        s[2], s[4], s[6])

    factor %= opar + atom + cpar, lambda s: s[2]

    factor %= num, lambda s: IntegerConstant(s[1])

    factor %= idx, lambda s: VariableCall(s[1])

    factor %= true, lambda s: TrueConstant()

    factor %= factor + period + idx + opar + args_list_empty + cpar, lambda s: FunCall(
        s[1], s[3], s[5])

    factor %= string_const, lambda s: s[1]

    factor %= idx + opar + args_list_empty + \
        cpar, lambda s: FunCall('self', s[1], s[3])

    factor %= factor + arroba + typex + period + idx + opar + args_list_empty + cpar, lambda s: \
        ParentFuncCall(s[1], s[3], s[5], s[7])

    factor %= false, lambda s: FalseConstant()

    factor %= instantiation, lambda s: s[1]

    atom %= arith + lt + arith, lambda s: LowerThanNode(s[1], s[3])

    atom %= arith + eq + arith, lambda s: EqualToNode(s[1], s[3])

    atom %= arith + ge + arith, lambda s: GreaterEqualNode(s[1], s[3])

    atom %= arith + le + arith, lambda s: LowerEqual(s[1], s[3])

    atom %= arith, lambda s: s[1]

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

    operators = r"!+|!*|!-|!/|!(|!)|!=|!.|!>|!<|!:|!?|!#|!,"
    quoted_string = r'"(1|2|3|4|5|6|7|8|9|0|A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N' + r'|n|O|o|P|p|Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|! |' + scaped_chars + "|" + operators + ')*"'

    tilde_string = r"'(1|2|3|4|5|6|7|8|9|0|A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N' + r'|n|O|o|P|p|Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|! |" + scaped_chars + ")*'"

    # table = [
    #     (class_keyword, '(c|C)(l|L)(a|A)(s|S)(s|S)'),
    #     (def_keyword, '(d|D)(e|E)(f|F)'),
    #     (in_keyword, '(i|I)(n|N)'),
    #     (intx, 'Int'),
    #     (boolean, 'Bool'),
    #     (objectx, 'Object'),
    #     (string, 'String'),
    #     (true, ' true'),
    #     (false, 'false'),
    #     (auto, 'AUTO_TYPE'),
    #     (if_, '(i|I)(f|F)'),
    #     (then, '(t|T)(h|H)(e|E)(n|N)'),
    #     (else_, '(e|E)(l|L)(s|S)(e|E)'),
    #     (new, '(n|N)(e|E)(w|W)'),
    #     (while_, '(w|W)(h|H)(i|I)(l|L)(e|E)'),
    #     (do, '(d|D)(o|O)'),
    #     (esac, '(e|E)(s|S)(a|A)(c|C)'),
    #     (case, '(c|C)(a|A)(s|S)(e|E)'),
    #     (of, '(o|O)(f|F)'),
    #     (inherits, '(i|I)(n|N)(h|H)(e|E)(r|R)(i|I)(t|T)(s|S)'),
    #     (coma, ','),
    #     (period, '.'),
    #     (dd, ':'),
    #     (dot_comma, ';'),
    #     (arroba, '@'),
    #     (assign, r'<!-'),
    #     (not_operator, r'(N|n)(o|O)(T|t)'),
    #     (lt, r'!<'),
    #     (gt, r'!>'),
    #     (ge, '>='),
    #     (le, '<='),
    #     (eq, '='),
    #     (not_, r'!~'),
    #     (opar, r'!('),
    #     (cpar, r'!)'),
    #     (obrack, r'!{'),
    #     (cbrack, r'!}'),
    #     (plus, r'!+'),
    #     (minus, r'!-'),
    #     (implies, r'=>'),
    #     (div, '/'),
    #     (star, r'!*'),
    #     (let, '(l|L)(e|E)(t|T)'),
    #     (fi, '(f|F)(i|I)'),
    #     (pool, '(p|P)(o|O)(o|O)(l|L)'),
    #     (loop, '(l|L)(o|O)(o|O)(p|P)'),
    #     (isvoid, '(i|I)(s|S)(v|V)(o|O)(i|I)(d|D)'),
    #     (idx, '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|' +
    #      'q|r|s|t|u|v|w|x|y|z)(A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N|n|O|o|P|p|'
    #      + 'Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|_|1|2|3|4|5|6|7|8|9|0)*'),
    #     (num, '(1|2|3|4|5|6|7|8|9|0)+'),
    #     (tilde_string_const, tilde_string),
    #     (quoted_string_const, quoted_string),
    #     (classid, '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|' +
    #      'Q|R|S|T|U|V|W|X|Y|Z)(A|a|B|b|C|c|D|d|E|e|F|f|G|g|H|h|I|i|J|j|K|k|L|l|M|m|N|n|O|o|P|p|'
    #      + 'Q|q|R|r|S|s|T|t|u|U|V|v|W|w|X|x|Y|y|Z|z|_|1|2|3|4|5|6|7|8|9|0)*'),
    # ]

    # lexer = Lexer(table, G.EOF, ignore_white_space=False)
    table = [
        (class_keyword, r'(?i)class'),
        (def_keyword, r'(?i)def'),
        (in_keyword, r'(?i)in'),
        (intx, r'Int'),
        (boolean, r'Bool'),
        (objectx, r'Object'),
        (string, r'String'),
        (true, r'true'),
        (false, r'false'),
        (auto, r'AUTO_TYPE'),
        (if_, r'(?i)if'),
        (then, r'(?i)then'),
        (else_, r'(?i)else'),
        (new, r'(?i)new'),
        (while_, r'(?i)while'),
        (do, r'(?i)do'),
        (esac, r'(?i)esac'),
        (case, r'(?i)case'),
        (of, r'(?i)of'),
        (inherits, r'(?i)inherits'),
        (coma, r','),
        (period, r'\.'),
        (dd, r'\:'),
        (dot_comma, r';'),
        (arroba, r'@'),
        (assign, r'<-'),
        (not_operator, r'(?i)not'),
        (lt, r'<'),
        (gt, r'>'),
        (ge, r'>='),
        (le, r'<='),
        (eq, r'='),
        (not_, r'\~'),
        (opar, r'\('),
        (cpar, r'\)'),
        (obrack, r'\{'),
        (cbrack, r'\}'),
        (plus, r'\+'),
        (minus, r'\-'),
        (implies, r'=>'),
        (div, '/'),
        (star, r'\*'),
        (let, r'(?i) let'),
        (fi, r'(?i)fi'),
        (pool, r'(?i)pool'),
        (loop, r'(?i)loop'),
        (isvoid, r'(?i)isvoid'),
        (idx, r'[a-z]\w*'),
        (num, r'\d+'),
        (tilde_string_const, r"('(?:[^'\\]|\\'|\\|\\\n)*')"),
        (quoted_string_const, r'("(?:[^\n"\\]|\\"|\\|\\\n)*")'),
        (classid, r'[A-Z]\w*'),
        ("StringError", r'("(?:[^"\\]|\\|\\"|\\\n)*\n)'),
        ("StringEOF", r'("(?:[^\n"\\]|\\\n|\\"|\\)*)')
    ]
    lexer = Tokenizer(table, G.EOF)
    return G, lexer
