import ply.yacc as yacc
from ply.yacc import YaccProduction, YaccSymbol
from ..utils.errors import error
from ..components.lexer_analyzer import lexer

class pyCoolParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors_parser = []
        self.parser = yacc.yacc(module=self)
        self.row_tracker = 0
        self.column_corrector = 0

    # precedence rules
    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LTEQ', 'LT', 'EQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('right', 'ISVOID'),
        ('right', 'INT_COMP'),
        ('left', 'AT'),
        ('left', 'DOT')
    )


    def positionTrack(self,
    p : YaccProduction,
    functionName,
    indexLinespan = 0,
    indexLexspan = 0):
        """ print('%%%%%%%%%%%%%%%%%')
        if type(p.stack[-1]) != YaccSymbol:
            if self.row_tracker != p.stack[-1].lineno:
                print('--------------')
                print('Inside the if')
                print('before lineno %d' %(self.row_tracker))
                self.column_corrector = p.stack[-1].lexpos
                self.row_tracker = p.stack[-1].lineno
                print (p.stack[-1])
                print('new lineno %d' %self.row_tracker)
                print('and col corrector %d' %self.column_corrector)
                print('--------------')
            else:
                print('--------------')
                print('Outside before lineno %s' %self.row_tracker)
                print('Outside current lineno %s' %p.lineno(indexLinespan))
                print('--------------')
        print('the real col %d' %(p.lexpos(indexLinespan)- self.column_corrector))
        print('the fucked col %d' %(p.lexpos(indexLinespan)))
        print(p.stack)
        print('In the function %s' %functionName)
        print('%%%%%%%%%%%%%%%%%')"""    
        pass
    def p_program(self, p):
        """
        program : class_list
        """
        self.positionTrack(p, functionName='p_program')
        

    def p_class_list(self, p):
        """
        class_list : class_list class SEMICOLON
                   | class SEMICOLON
        """
        self.positionTrack(p, functionName='p_class_list')
        
    def p_class(self, p):
        """
        class : CLASS TYPE LBRACE features_list_opt RBRACE
        """
        self.positionTrack(p, functionName='p_class')
        
    def p_class_inherits(self, p):
        """
        class : CLASS TYPE INHERITS TYPE LBRACE features_list_opt RBRACE
        """
        self.positionTrack(p, functionName='p_class_inherits')
        
    def p_feature_list_opt(self, p):
        """
        features_list_opt : features_list
                          | empty
        """
        self.positionTrack(p, functionName='p_feature_list_opt')
    
    def p_feature_list(self, p):
        """
        features_list : features_list feature SEMICOLON
                      | feature SEMICOLON
        """
        self.positionTrack(p, functionName='p_feature_list')
        
    def p_feature_method(self, p):
        """
        feature : ID LPAREN formal_params_list RPAREN COLON TYPE LBRACE expression RBRACE
        """
        self.positionTrack(p, functionName='p_feature_method')
    
    def p_feature_method_no_formals(self, p):
        """
        feature : ID LPAREN RPAREN COLON TYPE LBRACE expression RBRACE
        """
        self.positionTrack(p, functionName='p_feature_method_no_formals')
        
    def p_feature_attr_initialized(self, p):
        """
        feature : ID COLON TYPE ASSIGN expression
        """
        self.positionTrack(p, functionName='p_feature_attr_initialized')
        
    def p_feature_attr(self, p):
        """
        feature : ID COLON TYPE
        """
        self.positionTrack(p, functionName='p_feature_attr')
        
    def p_formal_list_many(self, p):
        """
        formal_params_list  : formal_params_list COMMA formal_param
                            | formal_param
        """
        self.positionTrack(p, functionName='p_formal_list_many')
        
    def p_formal(self, p):
        """
        formal_param : ID COLON TYPE
        """
        self.positionTrack(p, functionName='p_formal')
        
    def p_expression_object_identifier(self, p):
        """
        expression : ID
        """
        self.positionTrack(p, functionName='p_expression_object_identifier')
        
    def p_expression_integer_constant(self, p):
        """
        expression : INTEGER
        """
        self.positionTrack(p, functionName='p_expression_integer_constant')
        
    def p_expression_boolean_constant(self, p):
        """
        expression : BOOLEAN
        """
        self.positionTrack(p, functionName='p_expression_boolean_constant')
        
    def p_expression_string_constant(self, p):
        """
        expression : STRING
        """
        self.positionTrack(p, functionName='p_expression_string_constant')
    
    def p_expr_self(self, p):
        """
        expression  : SELF
        """
        self.positionTrack(p, functionName='p_expr_self')
            
    def p_expression_block(self, p):
        """
        expression : LBRACE block_list RBRACE
        """
        self.positionTrack(p, functionName='p_expression_block')
            
    def p_block_list(self, p):
        """
        block_list : block_list expression SEMICOLON
                   | expression SEMICOLON
        """
        self.positionTrack(p, functionName='p_block_list')
    
    def p_expression_assignment(self, p):
        """
        expression : ID ASSIGN expression
        """
        self.positionTrack(p, functionName='p_expression_assignment')

# ######################### UNARY OPERATIONS #######################################
    
    def p_expression_new(self, p):
        """
        expression : NEW TYPE
        """
        self.positionTrack(p, functionName='p_expression_new')
        
    def p_expression_isvoid(self, p):
        """
        expression : ISVOID expression
        """
        self.positionTrack(p, functionName='p_expression_isvoid')
        
    def p_expression_integer_complement(self, p):
        """
        expression : INT_COMP expression
        """
        self.positionTrack(p, functionName='p_expression_integer_complement')
        
    def p_expression_boolean_complement(self, p):
        """
        expression : NOT expression
        """
        self.positionTrack(p, functionName='p_expression_boolean_complement')
    
    # ######################### PARENTHESIZED, MATH & COMPARISONS #####################
    
    def p_expression_math_operations(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULTIPLY expression
                   | expression DIVIDE expression
        """
        self.positionTrack(p, functionName='p_expression_math_operations')
        
    def p_expression_math_comparisons(self, p):
        """
        expression : expression LT expression
                   | expression LTEQ expression
                   | expression EQ expression
        """
        self.positionTrack(p, functionName='p_expression_math_comparisons')
        
    def p_expression_with_parenthesis(self, p):
        """
        expression : LPAREN expression RPAREN
        """
        self.positionTrack(p, functionName='p_expression_with_parenthesis')
    
    # ######################### CONTROL FLOW EXPRESSIONS ##############################
    
    def p_expression_if_conditional(self, p):
        """
        expression : IF expression THEN expression ELSE expression FI
        """
        self.positionTrack(p, functionName='p_expression_if_conditional')
        
    def p_expression_while_loop(self, p):
        """
        expression : WHILE expression LOOP expression POOL
        """
        self.positionTrack(p, functionName='p_expression_while_loop')
    
    ## ######################### LET EXPRESSIONS ########################################
    
    def p_expression_let(self, p):
        """
         expression : let_expression
        """
        self.positionTrack(p, functionName='p_expression_let')
        
    def p_expression_let_simple(self, p):
        """
        let_expression : LET ID COLON TYPE IN expression
                       | nested_lets COMMA LET ID COLON TYPE
        """
        self.positionTrack(p, functionName='p_expression_let_simple')
        
    def p_expression_let_initialized(self, p):
        """
        let_expression : LET ID COLON TYPE ASSIGN expression IN expression
                       | nested_lets COMMA LET ID COLON TYPE ASSIGN expression
        """
        self.positionTrack(p, functionName='p_expression_let_initialized')
        
    def p_inner_lets_simple(self, p):
        """
        nested_lets : ID COLON TYPE IN expression
                    | nested_lets COMMA ID COLON TYPE
        """
        self.positionTrack(p, functionName='p_inner_lets_simple')
        
    def p_inner_lets_initialized(self, p):
        """
        nested_lets : ID COLON TYPE ASSIGN expression IN expression
                    | nested_lets COMMA ID COLON TYPE ASSIGN expression
        """
        self.positionTrack(p, functionName='p_inner_lets_initialized')
    
    # ######################### CASE EXPRESSION ########################################
    
    def p_expression_case(self, p):
        """
        expression : CASE expression OF actions_list ESAC
        """
        self.positionTrack(p, functionName='p_expression_case')
        
    def p_actions_list(self, p):
        """
        actions_list : actions_list action
                     | action
        """
        self.positionTrack(p, functionName='p_actions_list')
        
    def p_action_expr(self, p):
        """
        action : ID COLON TYPE ARROW expression SEMICOLON
        """
        self.positionTrack(p, functionName='p_action_expr')
    

    # ######################### METHODS DISPATCH ######################################
    
    def p_expression_dispatch(self, p):
        """
        expression : expression DOT ID LPAREN arguments_list_opt RPAREN
        """
        self.positionTrack(p, functionName='p_expression_dispatch')
    
    def p_arguments_list_opt(self, p):
        """
        arguments_list_opt : arguments_list
                           | empty
        """
        self.positionTrack(p, functionName='p_arguments_list_opt')

    
    def p_arguments_list(self, p):
        """
        arguments_list : arguments_list COMMA expression
                       | expression
        """
        self.positionTrack(p, functionName='p_arguments_list')
            
    def p_expression_static_dispatch(self, p):
        """
        expression : expression AT TYPE DOT ID LPAREN arguments_list_opt RPAREN
        """
        self.positionTrack(p, functionName='p_expression_static_dispatch')
        
    
    def p_expression_self_dispatch(self, p):
        """
        expression : ID LPAREN arguments_list_opt RPAREN
        """
        self.positionTrack(p, functionName='p_expression_self_dispatch')



    # ######################### ################## ###################################
    
    def p_empty(self, p):
        """
        empty :
        """
        self.positionTrack(p, functionName='p_empty')

    def findColumn(self, trackedRow):
        for i in range(len(self.parser.symstack) -1, 1, -1):
            if self.parser.symstack[i].lineno != trackedRow:
                return self.parser.symstack[i].lexpos
        return 0

    def p_error(self, p):
        """
        Error rule for Syntax Errors handling and reporting.
        """
        error_message = "EOF in string" if p is None else "Error at or near %s" %p.value
        column_corrector = 0 if p is None else self.findColumn(p.lineno)
        self.errors_parser.append(
        error(message= error_message,
        error_type="SyntacticError",
        row_and_col= (0,0) if p is None else (p.lineno, p.lexpos - column_corrector - 1)))
        print("Aquí ando")
        self.parser.errok()
        self.parser.token()


def run_parser(tokens, source_program):
    parserCool = pyCoolParser(tokens)
    lexer.lineno = 1
    parserCool.parser.parse(source_program, tracking=True, lexer=lexer)
    return parserCool.errors_parser

