# Get the token map from the lexer
from cl_ast import *
from cl_lexer.coollexer import CoolLexer
from pipeline import State
from tools.utils import find_column
from tools.cmp_errors import SyntacticError
import ply.yacc as yacc

class CoolParser(State):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.lexer = CoolLexer('Lex')
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def run(self, raw):
        ast = self.parser.parse(raw, lexer=self.lexer.lexer)
        self.errors = self.lexer.errors + self.errors
        return ast

    # Set the grammar start symbol
    start = 'program'

    # Program Rule
    def p_program(self, p):
        '''program : class_list'''
        p[0] = ProgramNode(0, 0, p[1])

    # Empty Production
    def p_empty(self, p):
        '''empty :'''
        pass

    # Classes Rules
    def p_class_list(self, p):
        '''class_list : def_class
                      | def_class class_list'''
        try:
            p[0] = [ p[1] ] + p[2]
        except:
            p[0] = [ p[1] ]

    # Class Definition Rules
    def p_def_class(self, p):
        '''def_class : CLASS TYPEID LBRACE feature_list RBRACE SEMI
                     | CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE SEMI'''
        if p[3].lower() == 'inherits':
            p[0] = ClassDeclarationNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[2], p[6], p[4])
            p[0].parent_pos = (p.lineno(4), find_column(p.lexer.lexdata, p.lexpos(4)))
        else:
            p[0] = ClassDeclarationNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[2], p[4])

    # Class Feature List Rules
    def p_feature_list(self, p):
        '''feature_list : empty
                        | def_attr SEMI feature_list
                        | def_func SEMI feature_list'''
        try:
            p[0] = [ p[1] ] + p[3]
        except:
            p[0] = []

    # Attr Definition Rules
    def p_def_attr(self, p):
        '''def_attr : ID COLON TYPEID
                    | ID COLON TYPEID ASSIGN expr'''
        try:
            p[0] = AttrDeclarationNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[5])
        except:
            p[0] = AttrDeclarationNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3])
            p[0].type_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))

    # Func Definition Rules
    def p_def_func(self, p):
        '''def_func : ID LPAREN param_list RPAREN COLON TYPEID LBRACE expr RBRACE'''
        p[0] = FuncDeclarationNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[6], p[8])
        p[0].type_pos = (p.lineno(6), find_column(p.lexer.lexdata, p.lexpos(6)))

    # Func Parameters List Rules
    def p_param_list_ept(self, p):
        '''param_list : empty'''
        p[0] = []

    def p_param_list_prm(self, p):
        '''param_list : param_build'''
        p[0] = p[1]

    def p_param_build(self, p):
        '''param_build : param empty
                       | param COMMA param_build'''
        try:
            p[0] = [ p[1] ] + p[3]
        except:
            p[0] = [ p[1] ]

    # Parameter Rule
    def p_param(self, p):
        '''param : ID COLON TYPEID'''
        p[0] = FormalParamNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3]) # (ID, TYPE)

    #    Expression Rules
    #   ------------------

    def p_expr(self, p):
        '''expr : LET let_list IN expr
                | CASE expr OF cases_list ESAC
                | IF expr THEN expr ELSE expr FI
                | WHILE expr LOOP expr POOL'''
        if p[1].lower() == 'let':
            p[0] = LetNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2], p[4])
        elif p[1].lower() == 'case':
            p[0] = CaseNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2], p[4])
        elif p[1].lower() == 'if':
            p[0] = ConditionalNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2], p[4], p[6])
        elif p[1].lower() == 'while':
            p[0] = WhileNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2], p[4])

    # Assign Production
    def p_expr_assign(self, p):
        '''expr : ID ASSIGN expr'''
        p[0] = AssignNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3])

    # Precedence Production
    def p_expr_arith(self, p):
        '''expr : arith'''
        p[0] = p[1]

    # Let Rules

    def p_let_list(self, p):
        '''let_list : let_assign
                    | let_assign COMMA let_list'''
        try:
            p[0] = [ p[1] ] + p[3]
        except:
            p[0] = [ p[1] ]

    def p_let_assign(self, p):
        '''let_assign : ID COLON TYPEID ASSIGN expr
                      | ID COLON TYPEID'''
        try:
            p[0] = LetDeclarationNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[5])
        except:
            p[0] = LetDeclarationNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3])
        p[0].type_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))

    # Case Rules

    def p_cases_list(self, p):
        '''cases_list : case SEMI
                      | case SEMI cases_list'''
        try:
            p[0] = [ p[1] ] + p[3]
        except:
            p[0] = [ p[1] ]

    def p_case(self, p):
        '''case : ID COLON TYPEID WITH expr'''
        p[0] = OptionNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[5])

    #   Arith Operations
    # -------------------

    # Operators Precedence
    precedence = (
        ('right', 'NOT'),
        ('nonassoc', 'LESS', 'LESSQ', 'EQUALS'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'STAR', 'DIVIDE'),
        ('right', 'ISVOID'),
        ('right', 'BITNOT'),
    )

    # Binary Operations Rules

    def p_expr_binary(self, p):
        '''expr : expr PLUS expr
                | expr MINUS expr
                | expr STAR expr
                | expr DIVIDE expr
                | expr LESS expr
                | expr LESSQ expr
                | expr EQUALS expr'''
        if p[2] == '+':
            p[0] = SumNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
        elif p[2] == '-':
            p[0] = DiffNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
        elif p[2] == '*':
            p[0] = StarNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
        elif p[2] == '<':
            p[0] = LessNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
        elif p[2] == '<=':
            p[0] = LessEqualNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
        elif p[2] == '=':
            p[0] = EqualNode(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)), p[1], p[3])

    # Unary Operations Rules

    def p_expr_unary(self, p):
        '''expr : BITNOT expr
                | ISVOID expr
                | NOT expr'''
        if p[1] == '~':
            p[0] = BitNotNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2])
        elif p[1].lower() == 'isvoid':
            p[0] = IsVoidNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2])
        elif p[1].lower() == 'not':
            p[0] = NotNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2])

    def p_arith_basecall(self, p): 
        '''arith : base_call'''
        p[0] = p[1]

    # Function Call Rules

    def p_basecall(self, p): # Parent Call (Review)
        '''base_call : fact ARROBA TYPEID DOT ID LPAREN arg_list RPAREN
                     | fact'''
        try:
            p[0] = ParentCallNode(p.lineno(5), find_column(p.lexer.lexdata, p.lexpos(5)), p[1], p[3], p[5], p[7])
        except:
            p[0] = p[1]

    def p_factcall(self, p):
        '''fact : fact DOT ID LPAREN arg_list RPAREN
                | ID LPAREN arg_list RPAREN'''
        try:
            p[0] = ExprCallNode(p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)), p[1], p[3], p[5])
        except:
            p[0] = SelfCallNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1], p[3])

    def p_arglist_ept(self, p):
        '''arg_list : empty'''
        p[0] = []

    def p_arglist_prm(self, p):
        '''arg_list : arg_build'''
        p[0] = p[1]

    def p_arg_build(self, p):
        '''arg_build : expr empty
                     | expr COMMA arg_build'''
        try:
            p[0] = [ p[1] ] + p[3]
        except:
            p[0] = [ p[1] ]

    # Atomic Operations

    def p_factatom(self, p):
        '''fact : atom'''
        p[0] = p[1]

    def p_fact_group(self, p):
        '''fact : LPAREN expr RPAREN'''
        p[0] = p[2]

    def p_atom_int(self, p):
        '''atom : INTEGER'''
        p[0] = IntegerNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1])

    def p_atom_id(self, p):
        '''atom : ID'''
        p[0] = VariableNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1])

    def p_atom_new(self, p):
        '''atom : NEW TYPEID'''
        p[0] = NewNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2])

    def p_atom_block(self, p):
        '''atom : LBRACE block RBRACE'''
        p[0] = BlockNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[2])

    def p_block(self, p):
        '''block : expr SEMI
                 | expr SEMI block'''
        try:
            p[0] = [ p[1] ] + p[3]
        except:
            p[0] = [ p[1] ]

    def p_atom_bool(self, p):
        '''atom : BOOL'''
        p[0] = BoolNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1])

    def p_atom_string(self, p):
        '''atom : STRING'''
        p[0] = StringNode(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)), p[1])

    def p_error(self, p):
        if p:
           line = self.lexer.lexer.lineno
           col = find_column(self.lexer.lexer.lexdata, p.lexpos)
           self.errors.append(SyntacticError(line, col, f"ERROR at or near {p.value}"))
        else:
           self.errors.append(SyntacticError(0, 0, "ERROR at or near EOF"))