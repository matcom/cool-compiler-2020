from core.cmp.pycompiler import Grammar
from core.cmp.functions import LR1Parser
from core.cmp.utils import Token, tokenizer

empty_token = Token("", "")
empty_token.row, empty_token.column = (0, 0)

# AST Classes
class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class DeclarationNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx.lex
        self.tid = idx
        self.features = features
        if not parent:
            parent = Token("Object", "type")
            parent.row = idx.row
            parent.column = idx.column
        self.parent = parent.lex
        self.tparent = parent

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None, arrow=empty_token):
        self.id = idx.lex
        self.tid = idx
        self.type = typex.lex
        self.ttype = typex
        self.arrow = arrow
        self.expr = expr

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx.lex
        self.tid = idx
        self.params = params
        self.type = return_type.lex
        self.ttype = return_type
        self.body = body

class ExpressionNode(Node):
    pass

class IfThenElseNode(ExpressionNode):
    def __init__(self, condition, if_body, if_token, else_body):
        self.token = if_token
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body, token):
        self.token = token
        self.condition = condition
        self.body = body

class BlockNode(ExpressionNode):
    def __init__(self, exprs):
        self.exprs = exprs

class LetInNode(ExpressionNode):
    def __init__(self, let_body, in_body):
        self.let_body = let_body
        self.in_body = in_body

class CaseOfNode(ExpressionNode):
    def __init__(self, expr, branches):
        self.expr = expr
        self.branches = branches

class CaseExpressionNode(AttrDeclarationNode):
    	pass

class LetAttributeNode(AttrDeclarationNode):
	pass

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx.lex
        self.tid = idx
        self.expr= expr

class UnaryNode(ExpressionNode):
    def __init__(self, expr, symbol):
        self.symbol = symbol
        self.expr = expr

class NotNode(UnaryNode):
    pass

class BinaryNode(ExpressionNode):
    def __init__(self, left, right, symbol):
        self.symbol = symbol
        self.left = left
        self.right = right

class ComparisonNode(BinaryNode):
    pass

class LessEqualNode(ComparisonNode):
    pass

class LessNode(ComparisonNode):
    pass

class EqualNode(ComparisonNode):
    pass

class ArithmeticNode(BinaryNode):
    pass

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class IsVoidNode(UnaryNode):
    pass

class ComplementNode(UnaryNode):
    pass

class FunctionCallNode(ExpressionNode):
    def __init__(self, obj, idx, args, typex=empty_token):
        self.obj = obj
        self.id = idx.lex
        self.tid = idx
        self.args = args
        self.type = typex.lex
        self.ttype = typex

class MemberCallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx.lex
        self.tid = idx
        self.args = args

class NewNode(ExpressionNode):
    def __init__(self, typex):
        self.type = typex.lex
        self.ttype = typex

class AtomicNode(ExpressionNode):
    def __init__(self, token):
        self.lex = token.lex
        self.token = token

class IntegerNode(AtomicNode):
    pass

class IdNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class BoolNode(AtomicNode):
    pass

def FunctionCallNodeBuilder(obj, calls):
    while len(calls):
        obj = FunctionCallNode(obj, *calls[0])
        calls.pop(0)
    return obj

class Param(Node):
    def __init__(self, tid, ttype):
        self.tid = tid
        self.ttype = ttype
        self.type = ttype.lex
        
    def __iter__(self):
        yield self.tid.lex
        yield self.type

        
# Grammar

CoolGrammar = Grammar()

# non-terminals
program = CoolGrammar.NonTerminal('<program>', startSymbol=True)
class_list, def_class = CoolGrammar.NonTerminals('<class-list> <def-class>')
feature_list, feature = CoolGrammar.NonTerminals('<feature-list> <feature>')
param_list, param = CoolGrammar.NonTerminals('<param-list> <param>')
expr, member_call, expr_list, block, let_list, case_list = CoolGrammar.NonTerminals('<expr> <member-call> <expr-list> <block> <let-list> <case-list>')
arith, term, func_expr, void, compl_expr, cmp_expr, statement = CoolGrammar.NonTerminals('<arith> <term> <func-expr> <void> <compl-expr> <cmp-expr> <statement>')
atom, func_call, arg_list = CoolGrammar.NonTerminals('<atom> <func-call> <arg-list>')
final_expr, unary_expr = CoolGrammar.NonTerminals('<final> <unary>')

# terminals
classx, inherits = CoolGrammar.Terminals('class inherits')
ifx, then, elsex, fi = CoolGrammar.Terminals('if then else fi')
whilex, loop, pool = CoolGrammar.Terminals('while loop pool')
let, inx = CoolGrammar.Terminals('let in')
case, of, esac = CoolGrammar.Terminals('case of esac')
semi, colon, comma, dot, at, opar, cpar, ocur, ccur, larrow, rarrow = CoolGrammar.Terminals('; : , . @ ( ) { } <- =>')
plus, minus, star, div, isvoid, compl = CoolGrammar.Terminals('+ - * / isvoid ~')
notx, less, leq, equal = CoolGrammar.Terminals('not < <= =')
new, idx, typex, integer, string, boolx = CoolGrammar.Terminals('new id type integer string bool')
eof = CoolGrammar.EOF

# productions
program %= class_list, lambda h, s: ProgramNode(s[1])

# <class-list> 
class_list %= def_class + class_list, lambda h, s: [s[1]] + s[2]
class_list %= def_class, lambda h, s: [s[1]]

# <def-class> 
def_class %= classx + typex + ocur + feature_list + ccur + semi, lambda h, s: ClassDeclarationNode(s[2], s[4])
def_class %= classx + typex + inherits + typex + ocur + feature_list + ccur + semi, lambda h, s: ClassDeclarationNode(s[2], s[6], s[4])

# <feature-list>
feature_list %= feature + feature_list, lambda h, s: [s[1]] + s[2]
feature_list %= CoolGrammar.Epsilon, lambda h, s: []

# <def-attr>
feature %= idx + colon + typex + semi, lambda h, s: AttrDeclarationNode(s[1], s[3])
feature %= idx + colon + typex + larrow + expr + semi, lambda h, s: AttrDeclarationNode(s[1], s[3], s[5], s[4])

# <def-func>
feature %= idx + opar + param_list + cpar + colon + typex + ocur + expr + ccur + semi, lambda h, s: FuncDeclarationNode(s[1], s[3], s[6], s[8]) 
feature %= idx + opar + cpar + colon + typex + ocur + expr + ccur + semi, lambda h, s: FuncDeclarationNode(s[1], [], s[5], s[7]) 

# <param-list>
param_list %= param, lambda h, s: [s[1]]
param_list %= param + comma + param_list, lambda h, s: [s[1]] + s[3]

# <param>
param %= idx + colon + typex, lambda h, s: Param(s[1], s[3])

# <block>
block %= expr + semi, lambda h, s: [s[1]]
block %= expr + semi + block, lambda h, s: [s[1]] + s[3]

# <let-list>
let_list %= idx + colon + typex, lambda h, s: [LetAttributeNode(s[1], s[3])]
let_list %= idx + colon + typex + larrow + expr, lambda h, s: [LetAttributeNode(s[1], s[3], s[5], s[4])]
let_list %= idx + colon + typex + comma + let_list, lambda h, s: [LetAttributeNode(s[1], s[3])] + s[5]
let_list %= idx + colon + typex + larrow + expr + comma + let_list, lambda h, s: [LetAttributeNode(s[1], s[3], s[5], s[4])] + s[7]

# <case-list>
case_list %= idx + colon + typex + rarrow + expr + semi, lambda h, s: [CaseExpressionNode(s[1], s[3], s[5])]
case_list %= idx + colon + typex + rarrow + expr + semi + case_list, lambda h, s: [CaseExpressionNode(s[1], s[3], s[5])] + s[7]

# <func-call>
func_call %= dot + idx + opar + arg_list + cpar, lambda h, s: (s[2], s[4])
func_call %= dot + idx + opar + cpar, lambda h, s: (s[2], [])
func_call %= at + typex + dot + idx + opar + arg_list + cpar, lambda h, s: (s[4], s[6], s[2])
func_call %= at + typex + dot + idx + opar + cpar, lambda h, s: (s[4], [], s[2])

# <arg-list>
arg_list %= expr, lambda h, s: [s[1]]
arg_list %= expr + comma + arg_list, lambda h, s: [s[1]] + s[3]

# <member-call>
member_call %= idx + opar + arg_list + cpar, lambda h, s: MemberCallNode(s[1], s[3])
member_call %= idx + opar + cpar, lambda h, s: MemberCallNode(s[1], [])

# <expr>
expr %= arith + plus  + unary_expr, lambda h, s: PlusNode(s[1], s[3], s[2])
expr %= arith + minus + unary_expr, lambda h, s: MinusNode(s[1], s[3], s[2])
expr %= term  + star  + unary_expr, lambda h, s: StarNode(s[1], s[3], s[2])
expr %= term  + div   + unary_expr, lambda h, s: DivNode(s[1], s[3], s[2])
expr %= arith + plus  + term + star + unary_expr, lambda h, s: PlusNode(s[1], StarNode(s[3], s[5], s[4]), s[2])
expr %= arith + minus + term + star + unary_expr, lambda h, s: MinusNode(s[1], StarNode(s[3], s[5], s[4]), s[2])
expr %= arith + plus  + term + div  + unary_expr, lambda h, s: PlusNode(s[1], DivNode(s[3], s[5], s[4]), s[2])
expr %= arith + minus + term + div  + unary_expr, lambda h, s: MinusNode(s[1], DivNode(s[3], s[5], s[4]), s[2])
expr %= arith + leq   + unary_expr, lambda h, s: LessEqualNode(s[1], s[3], s[2])
expr %= arith + less  + unary_expr, lambda h, s: LessNode(s[1], s[3], s[2])
expr %= arith + equal + unary_expr, lambda h, s: EqualNode(s[1], s[3], s[2])
expr %= unary_expr, lambda h, s: s[1]
expr %= cmp_expr, lambda h, s: s[1]

# <unary>
unary_expr %= isvoid + unary_expr, lambda h, s: IsVoidNode(s[1], s[3], s[2])
unary_expr %= compl  + unary_expr, lambda h, s: ComplementNode(s[1], s[3], s[2])
unary_expr %= final_expr, lambda h, s: s[1]

# <final>
final_expr %= let + let_list + inx + expr, lambda h, s: LetInNode(s[2], s[4])
final_expr %= idx + larrow + expr, lambda h, s: AssignNode(s[1], s[3])
final_expr %= notx + expr, lambda h, s: NotNode(s[2], s[1])

# <cmp-exp>
cmp_expr %= arith + leq + arith, lambda h, s: LessEqualNode(s[1], s[3], s[2])
cmp_expr %= arith + less + arith, lambda h, s: LessNode(s[1], s[3], s[2])
cmp_expr %= arith + equal + arith, lambda h, s: EqualNode(s[1], s[3], s[2])
cmp_expr %= arith, lambda h, s: s[1]

# <arith>
arith %= arith + plus + term, lambda h, s: PlusNode(s[1], s[3], s[2])
arith %= arith + minus + term, lambda h, s: MinusNode(s[1], s[3], s[2])
arith %= term, lambda h, s: s[1]

# <term>
term %= term + star + void, lambda h, s: StarNode(s[1], s[3], s[2])
term %= term + div + void, lambda h, s: DivNode(s[1], s[3], s[2])
term %= void, lambda h, s: s[1]

# <void>
void %= isvoid + void, lambda h, s: IsVoidNode(s[2], s[1])
void %= compl_expr, lambda h, s: s[1]

#<compl-expr>
compl_expr %= compl + void, lambda h, s: ComplementNode(s[2], s[1])
compl_expr %= func_expr, lambda h, s: s[1]

# <func-expr>
func_expr %= func_expr + func_call, lambda h, s: FunctionCallNode(s[1], *s[2])
func_expr %= atom, lambda h, s: s[1]

# <atom> 
atom %= member_call, lambda h, s: s[1]
atom %= new + typex, lambda h, s: NewNode(s[2])
atom %= opar + expr + cpar, lambda h, s: s[2]
atom %= idx, lambda h, s: IdNode(s[1])
atom %= integer, lambda h, s: IntegerNode(s[1])
atom %= string, lambda h, s: StringNode(s[1])
atom %= boolx, lambda h, s: BoolNode(s[1])
atom %= ocur + block + ccur, lambda h, s: BlockNode(s[2])
atom %= ifx + expr + then + expr + elsex + expr + fi, lambda h, s: IfThenElseNode(s[2], s[4], s[1], s[6])
atom %= whilex + expr + loop + expr + pool, lambda h, s: WhileLoopNode(s[2], s[4], s[1])
atom %= case + expr + of + case_list + esac, lambda h, s: CaseOfNode(s[2], s[4])

# Parser
CoolParser = LR1Parser(CoolGrammar)

# Tokenizer

fixed_tokens = { t.Name: Token(t.Name, t) for t in CoolGrammar.terminals if t not in { idx, integer, typex, string, boolx}}
booleans = ['false', 'true']
previous = [new, colon, classx, inherits]

@tokenizer(CoolGrammar, fixed_tokens)
def tokenize_text(token):
    lex = token.lex
    try:
        float(lex)
        return token.transform_to(integer)
    except ValueError:
        if lex[0].islower() and lex.lower() in booleans:
            return token.transform_to(boolx)
        if lex.count('"') >= 2 and lex[0] == '"' and lex[-1] == '"':
            return token.transform_to(string)
        return token.transform_to(idx)
    
deprecated_tokenize_text = tokenize_text

def tokenize_text(text):
    tokens = deprecated_tokenize_text(text)
    if tokens:
        for i in range(1, len(tokens)):
            if tokens[i].token_type == idx and tokens[i-1].token_type in previous:
                tokens[i] = Token(tokens[i].lex, typex)
    return tokens

def pprint_tokens(tokens):
    indent = 0
    pending = []
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi }:
            if token.token_type == ccur:
                indent -= 1
            print('    '*indent + ' '.join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    print(' '.join([str(t.token_type) for t in pending]))

def format_tokens(tokens):
    indent = 0
    pending = []
    txt = ''
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi }:
            if token.token_type == ccur:
                indent -= 1
            txt += '    '*indent + ' '.join(str(t.token_type) for t in pending) + '\n'
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    txt += ' '.join([str(t.token_type) for t in pending])
    return txt

# Example text
_text = '''
class Main {
    main ( console : IO ) : AUTO_TYPE {
        let x : AUTO_TYPE <- 3 + 2 in {
            case a of {
                x : Int => 3 ;
                p : string => "OK" ;
            } esac ;
        } ;
    } ;
} ;
'''
_text2 = '''
class Main inherits IO {
     main() : String {
         foo(42)
     };

     foo(i : Int) : String {
        if i = 0 then "" else 
	    (let next : Int <- i / 10 in
		foo(next).concat(foo(i - next * 10))
	    )
        fi
    };
};
'''
