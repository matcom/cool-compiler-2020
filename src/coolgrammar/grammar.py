"""
Contenedor para la funcion que construye la gramatica de cool.
"""
from grammar.grammar import Grammar
from abstract.tree import (
    ProgramNode,
    ClassDef,
    MethodDef,
    AttributeDef,
    Param,
    SelfNode,
    VariableDeclaration,
)
from abstract.tree import PlusNode, DivNode, MulNode, DifNode, IntegerConstant, FunCall
from abstract.tree import VariableCall, FalseConstant, StringConstant, TrueConstant
from abstract.tree import (
    GreaterEqualNode,
    LowerThanNode,
    LowerEqual,
    AssignNode,
    IfThenElseNode,
)
from abstract.tree import NotNode, WhileBlockNode, EqualToNode, InstantiateClassNode
from abstract.tree import ActionNode, CaseNode, ParentFuncCall, BlockNode, IsVoidNode
from abstract.tree import NegNode

# from lexer.tokenizer import Lexer
from tknizer import Tokenizer


def build_cool_grammar():
    G = Grammar()
    program = G.NonTerminal("<program>", True)

    (
        class_list,
        class_def,
        empty_feature_list,
        feature_list,
        method_def,
    ) = G.NonTerminals(
        "<class_list> <class_def> <empty_feature_list> <feature_list> <meod_def>"
    )

    attr_def, param_list, param, statement_list = G.NonTerminals(
        "<attr_def> <param_list> <param> <statement_list>"
    )

    var_dec, args_list, instantiation = G.NonTerminals(
        "<var_dec> <args_list> <instantiation>"
    )

    exp, typex, term, factor, nested_lets, loop_statements = G.NonTerminals(
        "<exp> <type> <term> <factor> <nested_lets> <loop_statements>"
    )

    arith, atom, actions, action, block, postfix = G.NonTerminals(
        "<arith> <atom> <actions> <action> <block> <postfix>"
    )

    args_list_empty, param_list_empty, case_statement, string_const = G.NonTerminals(
        "<args_list_empty> <param_list_empty> <case> <string_const>"
    )

    class_keyword, def_keyword, in_keyword, self_ = G.Terminals("class def in self")

    (
        coma,
        period,
        dot_comma,
        opar,
        cpar,
        obrack,
        cbrack,
        plus,
        minus,
        star,
        div,
        dd,
    ) = G.Terminals(", . ; ( ) { } + - * / :")

    idx, let, intx, string, num, true, false, boolean, objectx, classid = G.Terminals(
        "id let int string num true false bool object classid"
    )

    tilde_string_const, quoted_string_const, void, auto = G.Terminals(
        "tilde_string_const quoted_string_const void AUTO_TYPE"
    )

    if_, then, else_, assign, new, case, of, esac = G.Terminals(
        "if then else assign new case of esac"
    )

    gt, lt, ge, le, eq, not_, implies, isvoid, not_operator = G.Terminals(
        "> < >= <= = ~ => isvoid not"
    )

    while_, do, inherits, arroba, fi, pool, loop = G.Terminals(
        "while do inherits @ fi pool loop"
    )

    program %= class_list, lambda s: ProgramNode(s[1])

    class_list %= class_def + dot_comma, lambda s: [s[1]]
    class_list %= class_def + dot_comma + class_list, lambda s: [s[1]] + s[3]

    class_def %= (
        class_keyword + typex + obrack + empty_feature_list + cbrack,
        lambda s: ClassDef(s[2].lex, s[4], s[2].token_line, s[2].token_column),
    )

    class_def %= (
        class_keyword + typex + inherits + typex + obrack + empty_feature_list + cbrack,
        lambda s: ClassDef(
            s[2].lex, s[6], s[2].token_line, s[2].token_column, s[4].lex
        ),
    )

    feature_list %= method_def + dot_comma, lambda s: [s[1]]

    feature_list %= attr_def + dot_comma, lambda s: [s[1]]

    feature_list %= method_def + dot_comma + feature_list, lambda s: [s[1]] + s[3]

    feature_list %= attr_def + dot_comma + feature_list, lambda s: [s[1]] + s[3]

    empty_feature_list %= G.Epsilon, lambda s: []
    empty_feature_list %= feature_list, lambda s: s[1]

    method_def %= (
        idx
        + opar
        + param_list_empty
        + cpar
        + dd
        + typex
        + obrack
        + statement_list
        + cbrack,
        lambda s: MethodDef(
            s[1].lex,
            s[3],
            s[6].lex,
            s[1].token_line,
            s[1].token_column,
            s[8],
            s[7].token_column - (len(s[6].lex) + 2),
        ),
    )

    attr_def %= idx + dd + typex, lambda s: AttributeDef(
        s[1].lex, s[3].lex, s[1].token_line, s[1].token_column
    )

    attr_def %= idx + dd + typex + assign + exp, lambda s: AttributeDef(
        s[1].lex, s[3].lex, s[1].token_line, s[1].token_column, s[5]
    )

    param_list_empty %= param_list, lambda s: s[1]
    param_list_empty %= G.Epsilon, lambda s: []

    param_list %= param, lambda s: [s[1]]
    param_list %= param + coma + param_list, lambda s: [s[1]] + s[3]

    param %= idx + dd + typex, lambda s: Param(
        s[1].lex, s[3].lex, s[1].token_line, s[1].token_column
    )

    statement_list %= exp, lambda s: s[1]

    # statement_list %= exp + dot_comma + statement_list, lambda s: [s[1]] + s[3]

    var_dec %= let + nested_lets + in_keyword + exp, lambda s: VariableDeclaration(
        s[2], s[1].token_line, s[1].token_column - 3, s[4]
    )

    nested_lets %= idx + dd + typex, lambda s: [
        (s[1].lex, s[3].lex, None, s[3].token_line, s[3].token_column - len(s[3].lex))
    ]

    nested_lets %= (
        idx + dd + typex + coma + nested_lets,
        lambda s: [
            (s[1].lex, s[3].lex, None, s[3].token_line, s[3].token_column - len(s[3].lex))
        ]
        + s[5],
    )

    nested_lets %= idx + dd + typex + assign + exp, lambda s: [
        (s[1].lex, s[3].lex, s[5], s[3].token_line, s[3].token_column - len(s[3].lex))
    ]

    nested_lets %= (
        idx + dd + typex + assign + exp + coma + nested_lets,
        lambda s: [
            (s[1].lex, s[3].lex, s[5], s[3].token_line, s[3].token_column - len(s[3].lex))
        ]
        + s[7],
    )

    exp %= var_dec, lambda s: s[1]

    string_const %= quoted_string_const, lambda s: StringConstant(
        s[1].lex, s[1].token_line, s[1].token_column - len(s[1].lex)
    )

    string_const %= tilde_string_const, lambda s: StringConstant(
        s[1].lex, s[1].token_line, s[1].token_column - len(s[1].lex)
    )

    instantiation %= new + typex, lambda s: InstantiateClassNode(
        s[2].lex, s[1].token_line, s[1].token_column - 3, []
    )

    loop_statements %= exp + dot_comma, lambda s: [s[1]]
    loop_statements %= exp + dot_comma + loop_statements, lambda s: [s[1]] + s[3]

    exp %= idx + assign + exp, lambda s: AssignNode(
        s[1].lex, s[3], s[1].token_line, s[1].token_column
    )

    exp %= while_ + exp + loop + statement_list + pool, lambda s: WhileBlockNode(
        s[2], s[4], s[1].token_line, s[1].token_column - 5
    )

    exp %= atom, lambda s: s[1]

    # exp %= opar + atom + cpar, lambda s: s[2]

    # exp %= arith, lambda s: s[1]

    exp %= block, lambda s: s[1]

    exp %= case_statement, lambda s: s[1]

    exp %= isvoid + exp, lambda s: IsVoidNode(
        s[2], s[1].token_line, s[1].token_column - 6
    )

    block %= obrack + loop_statements + cbrack, lambda s: BlockNode(
        s[2], s[1].token_line, s[1].token_column - 1
    )

    arith %= arith + plus + term, lambda s: PlusNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    arith %= arith + minus + term, lambda s: DifNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    arith %= term, lambda s: s[1]

    term %= term + star + factor, lambda s: MulNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    term %= term + div + factor, lambda s: DivNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    term %= term + star + not_ + factor, lambda s: MulNode(
        s[1], s[4], s[2].token_line, s[2].token_column - 1
    )

    term %= term + div + not_  + factor, lambda s: DivNode(
        s[1], s[4], s[2].token_line, s[2].token_column - 1
    )

    term %= factor, lambda s: s[1]

    term %= not_ + factor, lambda s: NotNode(s[2], s[1].token_line, s[1].token_column)

    # term %= not_operator + factor, lambda s: NegNode(s[2], s[1].token_line, s[1].token_column + 1)

    factor %= if_ + exp + then + exp + else_ + exp + fi, lambda s: IfThenElseNode(
        s[2], s[4], s[6], s[1].token_line, s[1].token_column - 2
    )

    exp %= not_operator + exp, lambda s: NegNode(
        s[2], s[1].token_line, s[1].token_column + 1
    )

    postfix %= not_operator + atom, lambda s: NegNode(
        s[2], s[1].token_line, s[1].token_column + 1
    )

    factor %= opar + exp + cpar, lambda s: s[2]

    factor %= num, lambda s: IntegerConstant(s[1].lex)

    factor %= idx, lambda s: VariableCall(
        s[1].lex, s[1].token_line, s[1].token_column - len(s[1].lex)
    )

    factor %= true, lambda s: TrueConstant()

    factor %= factor + period + idx + opar + args_list_empty + cpar, lambda s: FunCall(
        s[1], s[3].lex, s[5], s[1].line, s[1].column
    )

    factor %= string_const, lambda s: s[1]

    factor %= idx + opar + args_list_empty + cpar, lambda s: FunCall(
        SelfNode(s[1].token_line, s[1].token_column - len(s[1].lex)),
        s[1].lex,
        s[3],
        s[1].token_line,
        s[1].token_column,
    )

    factor %= (
        factor + arroba + typex + period + idx + opar + args_list_empty + cpar,
        lambda s: ParentFuncCall(
            s[1], s[3].lex, s[5].lex, s[7], s[1].line, s[1].column
        ),
    )

    factor %= false, lambda s: FalseConstant()

    factor %= instantiation, lambda s: s[1]

    exp %= atom + lt + atom, lambda s: LowerThanNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    exp %= atom + eq + atom, lambda s: EqualToNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    exp %= atom + ge + atom, lambda s: GreaterEqualNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 2
    )

    exp %= atom + le + atom, lambda s: LowerEqual(
        s[1], s[3], s[2].token_line, s[2].token_column - 2
    )

    exp %= atom + lt + postfix, lambda s: LowerThanNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    exp %= atom + eq + postfix, lambda s: EqualToNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 1
    )

    exp %= atom + ge + postfix, lambda s: GreaterEqualNode(
        s[1], s[3], s[2].token_line, s[2].token_column - 2
    )

    exp %= atom + le + postfix, lambda s: LowerEqual(
        s[1], s[3], s[2].token_line, s[2].token_column - 2
    )

    factor %= self_, lambda s: SelfNode(
        s[1].token_line, s[1].token_column - len(s[1].lex)
    )

    atom %= arith, lambda s: s[1]

    typex %= intx, lambda s: s[1]

    typex %= boolean, lambda s: s[1]

    typex %= string, lambda s: s[1]

    typex %= objectx, lambda s: s[1]

    typex %= classid, lambda s: s[1]

    typex %= auto, lambda s: s[1]

    typex %= void, lambda s: s[1]

    args_list_empty %= args_list, lambda s: s[1]

    args_list_empty %= G.Epsilon, lambda s: []

    args_list %= exp, lambda s: [s[1]]

    args_list %= exp + coma + args_list, lambda s: [s[1]] + s[3]

    actions %= action, lambda s: [s[1]]

    actions %= action + actions, lambda s: [s[1]] + s[2]

    action %= idx + dd + typex + implies + exp + dot_comma, lambda s: ActionNode(
        s[1].lex, s[3].lex, s[5], s[3].token_line, s[3].token_column - len(s[3].lex)
    )

    case_statement %= case + exp + of + actions + esac, lambda s: CaseNode(
        s[2], s[4], s[1].token_line, s[1].token_column - 4
    )

    table = [
        (class_keyword, r"(?i)class"),
        (self_, r"(?i)self"),
        (def_keyword, r"(?i)def"),
        (in_keyword, r"(?i)in"),
        (intx, r"Int"),
        (boolean, r"Bool"),
        (objectx, r"Object"),
        (string, r"String"),
        (true, r"true"),
        (false, r"false"),
        (auto, r"AUTO_TYPE"),
        (if_, r"(?i)if"),
        (then, r"(?i)then"),
        (else_, r"(?i)else"),
        (new, r"(?i)new"),
        (while_, r"(?i)while"),
        (do, r"(?i)do"),
        (esac, r"(?i)esac"),
        (case, r"(?i)case"),
        (of, r"(?i)of"),
        (inherits, r"(?i)inherits"),
        (coma, r","),
        (period, r"\."),
        (dd, r"\:"),
        (dot_comma, r";"),
        (arroba, r"@"),
        (assign, r"<-"),
        (not_operator, r"(?i)not"),
        (lt, r"<"),
        (gt, r">"),
        (ge, r">="),
        (le, r"<="),
        (eq, r"="),
        (not_, r"\~"),
        (opar, r"\("),
        (cpar, r"\)"),
        (obrack, r"\{"),
        (cbrack, r"\}"),
        (plus, r"\+"),
        (minus, r"\-"),
        (implies, r"=>"),
        (div, "/"),
        (star, r"\*"),
        (let, r"(?i)let"),
        (fi, r"(?i)fi"),
        (pool, r"(?i)pool"),
        (loop, r"(?i)loop"),
        (isvoid, r"(?i)isvoid"),
        (idx, r"[a-z]\w*"),
        (num, r"\d+"),
        (tilde_string_const, r"('(?:[^'\\]|\\'|\\|\\\n)*')"),
        (quoted_string_const, r'("(?:[^\n"\\]|\\"|\\|\\\n)*")'),
        (classid, r"[A-Z]\w*"),
        ("StringError", r'("(?:[^"\\]|\\|\\"|\\\n)*\n)'),
        ("StringEOF", r'("(?:[^\n"\\]|\\\n|\\"|\\)*)'),
    ]
    lexer = Tokenizer(table, G.EOF)
    return G, lexer
