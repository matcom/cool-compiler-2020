from ply import yacc
from ..lexer import CoolLexer, find_column
from .ast_parser import *
from ..commons import terminals, keywords, tokens
from ..errors import SyntacticError
# Parser


class CoolParser:
    """
    CoolParser class.
    """

    def __init__(self, lexer):
        self.tokens = tokens + tuple(terminals.values())
        self.parser = yacc.yacc(module=self, start='program')
        self.error_list = []
        self.lexer = lexer

    def parse(self, code):
        result = self.parser.parse(
            code, self.lexer.lexer, tokenfunc=self.lexer.token)
        return result, self.error_list

    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LESS', 'LESSEQUAL', 'EQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'STAR', 'DIV'),
        ('right', 'ISVOID'),
        ('right', 'INT_COMPLEMENT'),
        ('left', 'AT'),
        ('left', 'DOT'),
    )

    def p_epsilon(self, p):
        'epsilon :'
        pass

    def p_program(self, p):
        '''program : class_list'''
        p[0] = ProgramNode(p[1])

    def p_class_list(self, p):
        '''class_list : def_class class_list
                      | def_class'''
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

    def p_class_list_error(self, p):
        '''class_list : error class_list  '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_def_class(self, p):
        '''def_class : CLASS TYPE OCURL feature_list CCURL SEMI
                    | CLASS TYPE INHERITS TYPE OCURL feature_list CCURL SEMI '''
        if len(p) == 7:
            p[0] = ClassDeclarationNode(p.slice[2], p[4])
        else:
            p[0] = ClassDeclarationNode(
                p.slice[2], p[6], parent=p.slice[4])

    def p_def_class_error(self, p):
        '''def_class : CLASS error OCURL feature_list CCURL SEMI
                    | CLASS TYPE OCURL error CCURL SEMI
                    | CLASS error OCURL error CCURL SEMI
                    | CLASS TYPE INHERITS TYPE OCURL error CCURL SEMI
                    | CLASS TYPE INHERITS error OCURL error CCURL SEMI
                    | CLASS error INHERITS TYPE OCURL error CCURL SEMI
                    | CLASS error INHERITS error OCURL feature_list CCURL SEMI
                    | CLASS error INHERITS error OCURL error CCURL SEMI '''
        p[0] = ErrorNode()

    def p_feature_list(self, p):
        '''feature_list : feature feature_list
                        | epsilon'''
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = []

    def p_feature_list_error(self, p):
        'feature_list : error feature_list'
        p[0] = [p[1]] + p[2]

    def p_feature_attribute(self, p):
        '''feature : ID COLON TYPE SEMI
                   | ID COLON TYPE ASSIGN expr SEMI '''
        if len(p) == 5:
            p[0] = AttrDeclarationNode(p.slice[1], p.slice[3])
        else:
            p[0] = AttrDeclarationNode(
                p.slice[1], p.slice[3], p[5])

    def p_def_attribute_error(self, p):
        '''feature : error COLON TYPE
                    | ID COLON error
                    | error COLON error
                    | error COLON TYPE ASSIGN expr
                    | ID COLON error ASSIGN expr
                    | ID COLON TYPE ASSIGN error
                    | ID COLON error ASSIGN error
                    | error COLON TYPE ASSIGN error
                    | error COLON error ASSIGN expr
                    | error COLON error ASSIGN error'''
        p[0] = ErrorNode()

    def p_feature_function(self, p):
        '''feature : ID OPAR param_list CPAR COLON TYPE OCURL expr CCURL SEMI
                   | ID OPAR CPAR COLON TYPE OCURL expr CCURL SEMI '''
        if len(p) == 11:
            p[0] = FuncDeclarationNode(
                p.slice[1], p[3], p.slice[6], p[8])
        else:
            p[0] = FuncDeclarationNode(
                p.slice[1], [], p.slice[5], p[7])

    def p_feature_function_error(self, p):
        '''feature : error OPAR param_list CPAR COLON TYPE OCURL expr CCURL SEMI
                    | ID OPAR error CPAR COLON TYPE OCURL expr CCURL SEMI
                    | ID OPAR param_list CPAR COLON error OCURL expr CCURL SEMI
                    | ID OPAR param_list CPAR COLON TYPE OCURL error CCURL SEMI
                    | error OPAR error CPAR COLON TYPE OCURL expr CCURL SEMI
                    | error OPAR param_list CPAR COLON error OCURL expr CCURL SEMI
                    | error OPAR param_list CPAR COLON TYPE OCURL error CCURL SEMI
                    | ID OPAR error CPAR COLON error OCURL error CCURL SEMI
                    | error OPAR error CPAR COLON TYPE OCURL error CCURL SEMI
                    | error OPAR error CPAR COLON error OCURL error CCURL SEMI
                    | error OPAR param_list CPAR COLON error OCURL error CCURL SEMI
                    | error OPAR CPAR COLON TYPE OCURL expr CCURL SEMI
                    | ID OPAR CPAR COLON error OCURL expr CCURL SEMI
                    | ID OPAR CPAR COLON TYPE OCURL error CCURL SEMI
                    | ID OPAR CPAR COLON error OCURL error CCURL SEMI
                    | ID error CPAR COLON TYPE OCURL error CCURL SEMI
                    | ID error CPAR COLON TYPE OCURL expr CCURL SEMI
                    | ID error CPAR COLON error OCURL error CCURL SEMI '''
        p[0] = ErrorNode()

    def p_param_list(self, p):
        '''param_list : param
                        | param COMMA param_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_param(self, p):
        '''param : ID COLON TYPE'''
        p[0] = (p.slice[1], p.slice[3])

    def p_expr_block(self, p):
        '''expr_block : expr SEMI
                    | expr SEMI expr_block'''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_let_list(self, p):
        '''let_list : ID COLON TYPE
                    | ID COLON TYPE ASSIGN expr
                    | ID COLON TYPE COMMA let_list
                    | ID COLON TYPE ASSIGN expr COMMA let_list'''
        if len(p) == 4:
            p[0] = [LetVariableDeclaration(p.slice[1], p.slice[3], None)]
        elif len(p) == 6 and p.slice[4].lex == '<-':
            p[0] = [LetVariableDeclaration(
                p.slice[1], p.slice[3], p[5])]
        elif len(p) == 6:
            p[0] = [LetVariableDeclaration(
                p.slice[1], p.slice[3], None)] + p[5]
        else:
            p[0] = [LetVariableDeclaration(
                p.slice[1], p.slice[3], p[5])] + p[7]

    def p_let_list_error(self, p):
        '''let_list : error COLON TYPE
                    | ID COLON error
                    | error COLON error 
                    | error COLON TYPE ASSIGN expr
                    | ID COLON error ASSIGN expr
                    | ID COLON TYPE ASSIGN error
                    | ID COLON error ASSIGN error
                    | error COLON error ASSIGN expr
                    | error COLON TYPE ASSIGN error
                    | error COLON error ASSIGN error
                    | error COLON TYPE COMMA let_list
                    | ID COLON error COMMA let_list
                    | ID COLON TYPE COMMA error
                    | ID COLON error COMMA error
                    | error COLON error COMMA let_list
                    | error COLON TYPE COMMA error
                    | error COLON error COMMA error
                    | error COLON error ASSIGN error COMMA error
                    | ID COLON error ASSIGN error COMMA error
                    | error COLON TYPE ASSIGN error COMMA error
                    | ID COLON TYPE ASSIGN error COMMA error
                    | error COLON error ASSIGN expr COMMA error
                    | ID COLON error ASSIGN expr COMMA error
                    | error COLON TYPE ASSIGN expr COMMA error
                    | ID COLON TYPE ASSIGN expr COMMA error
                    | error COLON error ASSIGN error COMMA let_list
                    | ID COLON error ASSIGN error COMMA let_list
                    | error COLON TYPE ASSIGN error COMMA let_list
                    | ID COLON TYPE ASSIGN error COMMA let_list
                    | error COLON error ASSIGN expr COMMA let_list
                    | ID COLON error ASSIGN expr COMMA let_list
                    | error COLON TYPE ASSIGN expr COMMA let_list '''
        p[0] = [ErrorNode()]

    def p_case_list(self, p):
        '''case_list : ID COLON TYPE ACTION expr SEMI
                    | ID COLON TYPE ACTION expr SEMI case_list '''
        if len(p) == 7:
            p[0] = [CaseVariableDeclaration(
                p.slice[1], p.slice[3], p[5])]
        else:
            p[0] = [CaseVariableDeclaration(
               p.slice[1], p.slice[3], p[5])] + p[7]

    def p_case_list_error(self, p):
        '''case_list : error COLON TYPE ACTION expr SEMI
                    | ID COLON error ACTION expr SEMI
                    | ID COLON TYPE ACTION error SEMI
                    | ID COLON TYPE error error SEMI
                    | error COLON error ACTION expr SEMI
                    | error COLON TYPE ACTION error SEMI
                    | error COLON error ACTION error SEMI
                    | error COLON TYPE ACTION expr SEMI case_list
                    | ID COLON error ACTION expr SEMI case_list
                    | ID COLON TYPE ACTION error SEMI case_list
                    | ID COLON TYPE error error SEMI case_list
                    | error COLON error ACTION expr SEMI case_list
                    | error COLON TYPE ACTION error SEMI case_list
                    | error COLON error ACTION error SEMI case_list
                    | error COLON TYPE ACTION expr SEMI error
                    | ID COLON TYPE ACTION expr SEMI error
                    | ID COLON error ACTION expr SEMI error
                    | ID COLON TYPE error error SEMI error
                    | error COLON error ACTION expr SEMI error
                    | error COLON TYPE ACTION error SEMI error
                    | error COLON error ACTION error SEMI error'''
        p[0] = [ErrorNode()]

    def p_func_call(self, p):
        '''funccall : ID OPAR CPAR
                    | ID OPAR arg_list CPAR'''
        if len(p) == 4:
            p[0] = (p.slice[1], [])
        else:
            p[0] = (p.slice[1], p[3])

    def p_func_call_error(self, p):
        '''funccall : error OPAR CPAR
                    | ID OPAR error CPAR
                    | error OPAR arg_list CPAR
                    | error OPAR error CPAR'''
        p[0] = (ErrorNode(), ErrorNode())

    def p_arg_list(self, p):
        ''' arg_list : expr
                     | expr COMMA arg_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_arg_list_error(self, p):
        ''' arg_list : error
                    | error COMMA arg_list'''
        p[0] = [ErrorNode()]

    def p_expr(self, p):
        '''expr : ID ASSIGN expr
                | operat '''
        if len(p) == 4:
            p[0] = AssignNode(p.slice[1], p[3])
        else:
            p[0] = p[1]

    def p_expr_error(self, p):
        '''expr : ID ASSIGN error 
                | error ASSIGN expr '''
        p[0] = ErrorNode()

    def p_comp(self, p):
        '''operat : operat LESSEQUAL operat
                    | operat LESS operat
                    | operat EQUAL operat'''
        if p.slice[2].lex == '<=':
            p[0] = LessEqualNode(p[1], p[3])
        elif p.slice[2].lex == '<':
            p[0] = LessNode(p[1], p[3])
        else:
            p[0] = EqualNode(p[1], p[3])

    def p_comp_error(self, p):
        '''operat : error LESSEQUAL operat
                    | error LESSEQUAL error
                    | operat LESSEQUAL error
                    | error LESS operat
                    | error LESS error
                    | operat LESS error
                    | error EQUAL operat
                    | error EQUAL error
                    | operat EQUAL error'''
        p[0] = ErrorNode()

    def p_arith(self, p):
        '''operat : operat PLUS operat
                | operat MINUS operat
                | operat STAR operat
                | operat DIV operat '''
        if p.slice[2].lex == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p.slice[2].lex == '-':
            p[0] = MinusNode(p[1], p[3])
        elif p.slice[2].lex == '*':
            p[0] = StarNode(p[1], p[3])
        else:
            p[0] = DivNode(p[1], p[3])

    def p_operat_error(self, p):
        '''operat : operat PLUS error
                    | error PLUS error
                    | error PLUS operat
                    | error MINUS operat
                    | error MINUS error
                    | operat MINUS error
                    | operat STAR error
                    | error STAR error
                    | error STAR operat
                    | operat DIV error 
                    | error DIV error 
                    | error DIV operat '''
        p[0] = ErrorNode()

    def p_base_operat(self, p):
        '''operat : baseop'''
        p[0] = p[1]

    def p_static_call(self, p):
        '''baseop : subatom AT TYPE DOT funccall '''
        p[0] = FunctionCallNode(p[1], *p[5], p.slice[3])

    def p_static_call_error(self, p):
        '''baseop : error AT TYPE DOT funccall
                | subatom AT error DOT funccall
                | subatom AT TYPE DOT error
                | error AT error DOT funccall
                | error AT TYPE DOT error
                | subatom AT error DOT error
                | error AT error DOT error '''
        p[0] = ErrorNode()

    def p_sub_atom(self, p):
        '''baseop : subatom'''
        p[0] = p[1]

    def p_parent_expr(self, p):
        '''subatom : OPAR expr CPAR'''
        p[0] = p[2]

    def p_parent_expr_error(self, p):
        '''subatom : error expr CPAR
                    | OPAR expr error'''
        p[0] = ErrorNode()

    def p_dynamic_call(self, p):
        '''subatom : subatom DOT funccall '''
        p[0] = FunctionCallNode(p[1], *p[3])

    def p_dynamic_call_error(self, p):
        '''subatom : subatom DOT error 
                   | error DOT funccall
                   | error DOT error '''
        p[0] = ErrorNode()

    def p_member_call(self, p):
        '''subatom : funccall '''
        p[0] = MemberCallNode(*p[1])

    def p_unary_operations(self, p):
        '''subatom : INT_COMPLEMENT baseop
                    | NOT baseop
                    | ISVOID baseop '''
        if p.slice[1].lex == '~':
            p[0] = ComplementNode(p[2])
        elif p.slice[1].lex == 'not':
            p[0] = NotNode(p[2])
        else:
            p[0] = IsVoidNode(p[2])

    # def p_unary_operations_error(self, p):
    #     '''subatom : INT_COMPLEMENT error
    #                 | NOT error
    #                 | ISVOID error '''
    #     p[0] = ErrorNode()

    def p_complex_sub_atom(self, p):
        '''subatom : IF expr THEN expr ELSE expr FI
                    | WHILE expr LOOP expr POOL
                    | LET let_list IN expr 
                    | CASE expr OF case_list ESAC '''
        # | LET let_list
        if p.slice[1].lex == 'if':
            p[0] = IfThenElseNode(p[2], p[4], p[6])
        elif p.slice[1].lex == 'while':
            p[0] = WhileLoopNode(p[2], p[4])
        elif p.slice[1].lex == 'let':
            p[0] = LetInNode(p[2], p[4])
        # elif p.slice[1].lex == 'let':
        #     p[0] = LetInNode(p[2], None)
        else:
            p[0] = CaseOfNode(p[2], p[4])

    def p_atom(self, p):
        '''subatom : atom'''
        p[0] = p[1]

    def p_new(self, p):
        '''atom : NEW TYPE'''
        p[0] = NewNode(p.slice[2])

    def p_new_error(self, p):
        '''atom : NEW error'''
        p[0] = ErrorNode()

    def p_atom_expr_block(self, p):
        '''atom : OCURL expr_block CCURL '''
        p[0] = BlockNode(p[2])

    def p_atom_expr_block_error(self, p):
        '''atom : OCURL error CCURL '''
        p[0] = ErrorNode()

    def p_atom_id(self, p):
        '''atom : ID'''
        p[0] = IdNode(p.slice[1])

    def p_atom_integer(self, p):
        '''atom : INTEGER'''
        p[0] = IntegerNode(p.slice[1])

    def p_atom_string(self, p):
        '''atom : STRING'''
        p[0] = StringNode(p.slice[1])

    def p_atom_bool(self, p):
        '''atom : BOOL'''
        p[0] = BoolNode(p.slice[1])

    def p_error(self, p):
        if p is None:
            colm = find_column(self.lexer.lexer, self.lexer.lexer)
            line = self.lexer.lexer.lineno
            error = SyntacticError(
                line, colm, 'ERROR at or near "%s"' % 'EOF')
            self.error_list.append(error)
        else:
            error = SyntacticError(
                p.lineno, p.lexpos, 'ERROR at or near "%s"' % p.lex)
            self.error_list.append(error)
