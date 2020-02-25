import ply.yacc as yacc
from tokens import tokens

# AST Classes
class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
        self.line = declarations[0].line
        self.column = declarations[0].column

class DeclarationNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features
        self.line = 0
        self.column = 0

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expression=None):
        self.id = idx
        self.type = typex
        self.expression = expression
        self.line = 0
        self.column = 0

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.line = 0
        self.column = 0

class ExpressionNode(Node):
    pass

class IfThenElseNode(ExpressionNode):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
        self.line = condition.line
        self.column = condition.column

class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.line = condition.line
        self.column = condition.column
        

class BlockNode(ExpressionNode):
    def __init__(self, expressions):
        self.expressions = expressions
        self.line = expressions[-1].line
        self.column = expressions[-1].column

class LetInNode(ExpressionNode):
    def __init__(self, let_body, in_body):
        self.let_body = let_body
        self.in_body = in_body
        self.line = in_body.line
        self.column = in_body.column

class CaseOfNode(ExpressionNode):
    def __init__(self, expression, branches):
        self.expression = expression
        self.branches = branches
        self.line = expression.line
        self.column = expression.column

class AssignNode(ExpressionNode):
    def __init__(self, idx, expression):
        self.id = idx
        self.expression = expression
        self.line = 0
        self.column = 0

class UnaryNode(ExpressionNode):
    def __init__(self, expression):
        self.expression = expression
        self.line = expression.line
        self.column = expression.column

class NotNode(UnaryNode):
    pass

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.line = left.line
        self.column = left.column

class LessEqualNode(BinaryNode):
    pass

class LessNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
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
    def __init__(self, obj, idx, args, typex=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex
        self.line = 0
        self.column = 0

class MemberCallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
        self.line = 0
        self.column = 0

class NewNode(ExpressionNode):
    def __init__(self, typex):
        self.type = typex
        self.line = 0
        self.column = 0

class AtomicNode(ExpressionNode):
    def __init__(self, token):
        self.token = token
        self.line = 0
        self.column = 0

class IntegerNode(AtomicNode):
    pass

class IdNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class BoolNode(AtomicNode):
    pass


    # Get the token map from the lexer.  This is required.
class CoolParser():

    def __init__(self):
        self.tokens = tokens
        self.errors = []

    def p_program(self, p):
        'program : class_list'
        p[0]=ProgramNode(p[1])

    def p_class_list(self, p):
        'class_list : def_class class_list'
        p[0]=[p[1]] + p[2]

    def p_class_list_s(self, p):
        'class_list : def_class'
        p[0]=[p[1]]

    def p_def_class(self, p):
        'def_class : CLASS TYPE OCUR feature_list CCUR SEMI'
        p[0]=ClassDeclarationNode(p[2],p[4])

    def p_def_class_h(self, p):
        'def_class : CLASS TYPE INHERITS TYPE OCUR feature_list CCUR SEMI'
        p[0]=ClassDeclarationNode(p[2],p[6],p[4])


    def p_feature_list(self, p):
        'feature_list : feature feature_list'
        p[0]=[p[1]]+p[2]

    def p_feature_list_e(self, p):
        'feature_list : empty'
        p[0]=[]
    def p_feature_1(self, p):
        'feature : OBJECT COLON TYPE SEMI'
        p[0]=AttrDeclarationNode(p[1],p[3])

    def p_feature_2(self, p):
        'feature : OBJECT COLON TYPE LARROW expr SEMI'
        p[0]=AttrDeclarationNode(p[1],p[3],p[5])

    def p_feature_3(self, p):
        'feature : OBJECT OPAR param_list CPAR COLON TYPE OCUR expr CCUR SEMI'
        p[0]=FuncDeclarationNode(p[1], p[3], p[6], p[8]) 

    def p_feature_4(self, p):
        'feature : OBJECT OPAR CPAR COLON TYPE OCUR expr CCUR SEMI'
        p[0]=FuncDeclarationNode(p[1], [], p[5], p[7])


    def p_param_list_1(self, p):
        'param_list : param'
        p[0]=[p[1]]

    def p_param_list_2(self, p):
        'param_list : param COMMA param_list'
        p[0]=[p[1]] + p[3]

    # <param>        ???
    def p_param(self, p):
        r'param : OBJECT COLON TYPE'
        p[0]=(p[1],p[3])

    # <expr-list>    ???
    def p_expr_list_1(self, p):
        'expr_list : expr SEMI'
        p[0]=[p[1]]

    def p_expr_list_2(self, p):
        'expr_list : expr SEMI expr_list'
        p[0]=[p[1]]+p[3]

    # <let-list>     ???
    def p_let_list1(self, p):
        'let_list : OBJECT COLON TYPE'
        p[0]=[(p[1], p[3], None)]

    def p_let_list2(self, p):
        'let_list : OBJECT COLON TYPE LARROW expr'
        p[0]=[(p[1], p[3], p[5])]

    def p_let_list3(self, p):
        'let_list : OBJECT COLON TYPE COMMA let_list'
        p[0]=[(p[1], p[3], None)] + p[5]

    def p_let_list4(self, p):
        'let_list : OBJECT COLON TYPE LARROW expr COMMA let_list'
        p[0]=[(p[1], p[3], p[5])] + p[7]

    # <case-list>    ???
    def p_case_list_1(self, p):
        'case_list : OBJECT COLON TYPE RARROW expr SEMI'
        p[0] = [(p[1], p[3], p[5])]

    def p_case_list_2(self, p):
        'case_list : OBJECT COLON TYPE RARROW expr SEMI case_list'
        p[0] = [(p[1], p[3], p[5])] + p[7]

    # <truth-expr>   ???

    def p_expr_2(self, p):
        'expr : comp_expr'
        p[0]=p[1]

    # <comp-expr>    ???

    def p_comp_expr_1(self, p):
        'comp_expr : comp_expr LESSEQUAL arith'
        p[0]= LessEqualNode(p[1], p[3])

    def p_comp_expr_2(self, p):
        'comp_expr : comp_expr LESS arith'
        p[0]= LessNode(p[1], p[3])

    def p_comp_expr_3(self, p):
        'comp_expr : comp_expr EQUAL arith'
        p[0]= EqualNode(p[1], p[3])

    def p_comp_expr_4(self, p):
        'comp_expr : arith'
        p[0]= p[1]

    # <arith>       ???

    def p_arith_1(self, p):
        'arith2 : arith2 PLUS term'
        p[0]= PlusNode(p[1], p[3])

    def p_arith_2(self, p):
        'arith2 : arith2 MINUS term'
        p[0]= MinusNode(p[1], p[3])

    def p_arith_3(self, p):
        'arith2 : term'
        p[0]=p[1]

    def p_arith_2_1(self, p):
        r'arith : NOT arith2'
        p[0]=NotNode(p[2])

    def p_arith_2_2(self, p):
        r'arith : arith2'
        p[0]=p[1]


    # <term>        ???
    def p_term_1(self, p):
        'term : term MULT factor'
        p[0]=StarNode(p[1], p[3])

    def p_term_2(self, p):
        'term : term DIV factor'
        p[0]=DivNode(p[1], p[3])

    def p_term_3(self, p):
        'term : factor'
        p[0]=p[1]
    # <factor>      ???
    def p_factor_1(self, p):
        'factor : ISVOID factor2'
        p[0]= IsVoidNode(p[2])
    def p_factor_2(self, p):
        'factor : factor2'
        p[0]=p[1]
    # <factor-2>    ???
    def p_factor_2_1(self, p):
        'factor2 : INT_COMPLEMENT atom'
        p[0]=ComplementNode(p[2])
    def p_factor_2_2(self, p):
        'factor2 : atom'
        p[0]=p[1]
    # <atom>        ???

    def p_atom_1(self, p):
        'atom : IF expr THEN expr ELSE expr FI'
        p[0]=IfThenElseNode(p[2], p[4], p[6])

    def p_atom_2(self, p):
        'atom : WHILE expr LOOP expr POOL'
        p[0]=WhileLoopNode(p[2], p[4])

    def p_atom_3(self, p):
        'atom : LET let_list IN expr'
        p[0]= LetInNode(p[2],p[4])

    def p_atom_4(self, p):
        'atom : CASE expr OF case_list ESAC '
        p[0]=CaseOfNode(p[2], p[4])

    def p_atom_5 (self, p):
        'atom : OBJECT LARROW expr'
        p[0]= AssignNode(p[1],p[3])

    def p_atom_6(self, p):
        'atom : atom func_call'
        p[0]= FunctionCallNode(p[1], *p[2])

    def p_atom_7(self, p):
        'atom : member_call'
        p[0]=p[1]

    def p_atom_8(self, p):
        'atom : NEW TYPE'
        p[0]= NewNode(p[2])

    def p_atom_9(self, p):
        'atom : OPAR expr CPAR'
        p[0]=p[2]

    def p_atom_10(self, p):
        'atom : OBJECT'
        p[0]=IdNode(p[1])

    def p_atom_11(self, p):
        'atom : INTEGER'
        p[0]= IntegerNode(p[1])

    def p_atom_12(self, p):
        'atom : STRING'
        p[0]=StringNode(p[1])

    def p_atom_13(self, p):
        'atom : BOOL'
        p[0]=BoolNode(p[1])

    def p_atom_14(self, p):
        r'atom : OCUR expr_list CCUR'
        p[0]=BlockNode(p[2])
    #<func-call> ???
    def p_func_call_1(self, p):
        'func_call : DOT OBJECT OPAR arg_list CPAR'
        p[0]=(p[2],p[4])

    def p_func_call_2(self, p):
        'func_call : DOT OBJECT OPAR CPAR'
        p[0]=(p[2],[])
        
    def p_func_call_3(self, p):
        'func_call : AT TYPE DOT OBJECT OPAR arg_list CPAR'
        p[0]=(p[4],p[6],p[2])

    def p_func_call_4(self, p):
        'func_call : AT TYPE DOT OBJECT OPAR  CPAR'
        p[0]=(p[4],[],p[2])

    def p_arg_list_1(self, p):
        'arg_list : expr'
        p[0]=[p[1]]

    def p_arg_list_2(self, p):
        'arg_list : expr COMMA arg_list'
        p[0]=[p[1]]+p[3]

    def p_member_call_1(self, p):
        'member_call : OBJECT OPAR arg_list CPAR'
        p[0]= MemberCallNode(p[1],p[3])

    def p_member_call_2(self, p):
        'member_call : OBJECT OPAR CPAR'
        p[0]= MemberCallNode(p[1],[])

    def p_empty(self, p):
        'empty :'
        p[0]=[]
        pass
    
    # Error rule for syntax errors
    def p_error(self, p):
        self.errors.append(f"({p.lineno},{self.lexer.find_column(self.data, p)}) - SyntacticError: Error near {p.value}")
    
    def build(self):
        self.parser = yacc.yacc(module=self, write_tables=False)

    def parse(self, lexer):
        self.data = lexer.data
        self.lexer = lexer
        self.build()
        
        result = self.parser.parse(lexer=lexer)
        return self.errors