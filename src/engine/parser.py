from .cp import Grammar, LR1Parser
from ply import yacc
from ast_parser import *
from lexer import tokens,literals

# Parser

class CoolParser:
    """
    CoolParser class.
    """
    def __init__(self, tokens, literals):
        self.tokens = None
        self.literals = None
        self.parser = yacc.yacc(module=self,start='program')
        self.error_list = []


    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LESS', 'LESSEQUAL', 'EQUAL'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'ISVOID')
        ('right', 'INT_COMPLEMENT')
        ('left', '@'),
        ('left', '.'),
    )

    def p_epsilon(p):
        'epsilon :'
        pass

    def p_program(p):
        '''program : class_list'''
        p[0] = ProgramNode(p[1])

    def p_class_list(p):
        '''class_list : def_class class_list
                      | def_class'''
        if len(p) == 3:
            p[0] = [s[1]] + s[2]
        else:
            p[0] = [p[1]]

    def p_def_class(p):
        '''def_class : CLASS TYPE '(' feature_list ')' ';'
                    | CLASS TYPE INHERITS TYPE '(' feature_list ')' ';' '''
        if len(p) == 7:
            p[0] = ClassDeclarationNode(p[2], p[4])
        else:
            p[0] = ClassDeclarationNode(p[2], p[6], parent=p[4])

    def p_feature_list(p):
        '''feature_list : feature feature_list
                        | epsilon'''
        if len(p) == 3:
            p[0] = [p[1]] + p[2]

    def p_feature_attribute(p):
        '''feature : ID ':' TYPE ';'
                | ID ':' TYPE ASSIGN expr ';' '''
        if len(p) == 5:
            p[0] = AttrDeclarationNode(p[1], p[3])
        else:
            p[0] = AttrDeclarationNode(p[1], p[3], p[5])

    def p_feature_function(p):
        '''feature : ID '(' param_list ')' ':' TYPE '(' expr ')' ';'
                   | ID '(' ')' ':' TYPE '(' expr ')' ';''''
        if len(p) == 11:
            p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8])
        else:
            p[0] = FuncDeclarationNode(p[1], [], p[5], p[7])

    def p_param_list(p):
        '''param_list : param
                    | param comma param_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_param(p):
        '''param : ID ':' TYPE'''
        p[0] = (p[1], p[3])

    def p_expr_list(p):
        '''expr_block : expr semi
                     | expr semi expr_block'''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_let_list(p):
        '''let_list : ID ':' TYPE
                    | ID ':' TYPE ACTION expr
                    | ID ':' TYPE comma let_list
                    | ID ':' TYPE ACTION expr comma let_list'''
        if len(p) == 4:
            p[0] = [LetVariableDeclaration(p[1], p[3], None)]
        elif len(p) == 6 and p[4].lex == '=>':
            p[0] = [LetVariableDeclaration(p[1], p[3], p[5])]
        elif len(p) == 6:
            p[0] = [LetVariableDeclaration(p[1], p[3], None)] + p[5]
        else:
            p[0] = [LetVariableDeclaration(p[1], p[3], p[5])] + p[7]

    def p_case_list(p):
        '''case_list : ID ':' TYPE ACTION expr ';'
                    | ID ':' TYPE ACTION expr ';' case_list '''
        if len(p) == 7:
            p[0] = [CaseVariableDeclaration(s[1], s[3], s[5])]
        else:
            p[0] = [CaseVariableDeclaration(s[1], s[3], s[5])] + p[7]
    
    def p_compar(p):
        '''expr : expr LESSEQUAL expr
                | expr LESS expr
                | expr EQUAL expr'''
        if p[2].lex == '<=':
            p[0] = LessEqualNode(p[1], p[3])
        elif p[2] == '<':
            p[0] = LessNode(p[1], p[3])
        else:
            p[0] = EqualNode(p[1], p[3])

    def p_unary(p):
        ''' expr : '~' expr
                 | NOT expr
                 | ISVOID expr'''
        if p[1].lex == '~':
            p[0] = ComplementNode(p[2])
        elif p[1].lex == 'not':
            p[0] = NotNode(p[2])
        else:
            p[0] = IsVoidNode(p[2])

    def p_arith(p):
        '''expr : expr '+' expr
                | expr '-' expr'''
        if p[2].lex == '+':
            p[0] = PlusNode(p[0], p[3])
        elif p[2].lex == '-':
            p[0] = MinusNode(p[0], p[3])

    def p_term(p):
        '''expr : expr '*' expr
                | expr '/' expr'''
       elif p[2].lex == '*':
            p[0] = StarNode(p[1], p[3])
        else:
            p[0] = DivNode(p[1], p[3])

    def p_sub_atomic(p):
        '''expr : IF expr THEN expr ELSE expr FI
                | WHILE expr LOOP expr POOL
                | '(' expr_list ')'
                | LET let_list IN expr 
                | LET let_list 
                | CASE expr of case_list ESAC
                | ID ASSIGN expr'''
        if p[1].lex == 'if':
            p[0] = IfThenElseNode(p[2], p[4], p[6])
        elif p[1].lex == 'while':
            p[0] = WhileLoopNode(p[2], p[4])
        elif p[1].lex == '(':
            p[0] = BlockNode(p[2])
        elif len(p) == 5 and p[1].lex == 'let':
            p[0] = LetInNode(p[2], p[4])
        elif p[1].lex == 'let':
            p[0] = LetInNode(p[2], None)
        elif p[1].lex == 'case':
            p[0] = CaseOfNode(p[2], p[4])
        else:
            p[0] = AssignNode(p[1], p[3])

    def p_atomic(p):
        '''expr : new0 TYPE
                | '(' expr ')''''
        if p[0].lex == 'new':
            p[0] = NewNode(p[2])
        elif p[0].lex == '(':
            p[0] = p[2]

    def p_atomic_func_call(p):
        '''expr : expr func_call'''
        p[0] = FunctionCallNode(p[1], *p[2])

    def p_static_call(p):
        '''func_call : '.' ID '(' arg_list ')'
                     | '.' ID '(' ')''''
        if len(p) == 6:
            p[0] = (p[2], p[4])
        else:
            p[0] = (p[2], [])

    def p_dynamic_call(p):
        '''func_call : '@' TYPE '.' ID '(' arg_list ')'
                     | '@' TYPE '.' ID '(' ')''''
        if len(p) == 6:
            p[0] = (p[4], p[6], p[2])
        else:
            p[0] = (p[4], [], p[2])
    def p_atomic_member_call(p):
        '''expr : ID '(' arg_list ')'
                | ID '(' ')''''

    def p_arg_list(p):
        ''' arg_list : expr
                     | expr ',' arg_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:``
            p[0] = [p[1]] + p[3]
    
    def p_atomic_id(p):
        '''expr : ID'''
        p[0] = IdNode(p[1])

    def p_atomic_integer(p):
        '''expr : INTEGER'''
        p[0] = IntegerNode(p[1])

    def p_atomic_string(p):
        '''expr : STRING'''
        p[0] = StringNode(p[1])

    def p_atomic_bool(p):
        '''expr : BOOL'''
        p[0] = BoolNode(p[1])

parser = CoolParser(tokens, literals)

if __name__ == '__main__':
