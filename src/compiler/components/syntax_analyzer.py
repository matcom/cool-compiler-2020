import ply.yacc as yacc
from ply.yacc import YaccProduction, YaccSymbol
from ..utils.errors import error
from ..components.lexer_analyzer import lexer

class pyCoolParser:
    def __init__(self, tokens, real_col):
        self.tokens = tokens
        self.errors_parser = []
        self.parser = yacc.yacc(module=self)
        self.row_tracker = 0
        self.column_corrector = 0
        self.real_col = real_col

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
    
    def p_program(self, p):
        """
        program : class_list
        """        
        

    def p_class_list(self, p):
        """
        class_list : class_list class SEMICOLON
                   | class SEMICOLON
        """        
        
    def p_class(self, p):
        """
        class : CLASS TYPE LBRACE features_list_opt RBRACE
        """        
        
    def p_class_inherits(self, p):
        """
        class : CLASS TYPE INHERITS TYPE LBRACE features_list_opt RBRACE
        """        
        
    def p_feature_list_opt(self, p):
        """
        features_list_opt : features_list
                          | empty
        """        
    
    def p_feature_list(self, p):
        """
        features_list : features_list feature SEMICOLON
                      | feature SEMICOLON
        """        
        
    def p_feature_method(self, p):
        """
        feature : ID LPAREN formal_params_list RPAREN COLON TYPE LBRACE expression RBRACE
        """        
    
    def p_feature_method_no_formals(self, p):
        """
        feature : ID LPAREN RPAREN COLON TYPE LBRACE expression RBRACE
        """        
        
    def p_feature_attr_initialized(self, p):
        """
        feature : ID COLON TYPE ASSIGN expression
        """        
        
    def p_feature_attr(self, p):
        """
        feature : ID COLON TYPE
        """        
        
    def p_formal_list_many(self, p):
        """
        formal_params_list  : formal_params_list COMMA formal_param
                            | formal_param
        """        
        
    def p_formal(self, p):
        """
        formal_param : ID COLON TYPE
        """        
        
    def p_expression_object_identifier(self, p):
        """
        expression : ID
        """        
        
    def p_expression_integer_constant(self, p):
        """
        expression : INTEGER
        """        
        
    def p_expression_boolean_constant(self, p):
        """
        expression : BOOLEAN
        """        
        
    def p_expression_string_constant(self, p):
        """
        expression : STRING
        """        
    
    def p_expr_self(self, p):
        """
        expression  : SELF
        """        
            
    def p_expression_block(self, p):
        """
        expression : LBRACE block_list RBRACE
        """        
            
    def p_block_list(self, p):
        """
        block_list : block_list expression SEMICOLON
                   | expression SEMICOLON
        """        
    
    def p_expression_assignment(self, p):
        """
        expression : ID ASSIGN expression
        """        

# ######################### UNARY OPERATIONS #######################################
    
    def p_expression_new(self, p):
        """
        expression : NEW TYPE
        """        
        
    def p_expression_isvoid(self, p):
        """
        expression : ISVOID expression
        """        
        
    def p_expression_integer_complement(self, p):
        """
        expression : INT_COMP expression
        """        
        
    def p_expression_boolean_complement(self, p):
        """
        expression : NOT expression
        """        
    
    # ######################### PARENTHESIZED, MATH & COMPARISONS #####################
    
    def p_expression_math_operations(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULTIPLY expression
                   | expression DIVIDE expression
        """        
        
    def p_expression_math_comparisons(self, p):
        """
        expression : expression LT expression
                   | expression LTEQ expression
                   | expression EQ expression
        """        
        
    def p_expression_with_parenthesis(self, p):
        """
        expression : LPAREN expression RPAREN
        """        
    
    # ######################### CONTROL FLOW EXPRESSIONS ##############################
    
    def p_expression_if_conditional(self, p):
        """
        expression : IF expression THEN expression ELSE expression FI
        """        
        
    def p_expression_while_loop(self, p):
        """
        expression : WHILE expression LOOP expression POOL
        """        
    
    ## ######################### LET EXPRESSIONS ########################################
    
    def p_expression_let(self, p):
        """
         expression : let_expression
        """        
        
    def p_expression_let_simple(self, p):
        """
        let_expression : LET ID COLON TYPE IN expression
                       | nested_lets COMMA LET ID COLON TYPE
        """        
        
    def p_expression_let_initialized(self, p):
        """
        let_expression : LET ID COLON TYPE ASSIGN expression IN expression
                       | nested_lets COMMA LET ID COLON TYPE ASSIGN expression
        """        
        
    def p_inner_lets_simple(self, p):
        """
        nested_lets : ID COLON TYPE IN expression
                    | nested_lets COMMA ID COLON TYPE
        """        
        
    def p_inner_lets_initialized(self, p):
        """
        nested_lets : ID COLON TYPE ASSIGN expression IN expression
                    | nested_lets COMMA ID COLON TYPE ASSIGN expression
        """        
    
    # ######################### CASE EXPRESSION ########################################
    
    def p_expression_case(self, p):
        """
        expression : CASE expression OF actions_list ESAC
        """        
        
    def p_actions_list(self, p):
        """
        actions_list : actions_list action
                     | action
        """        
        
    def p_action_expr(self, p):
        """
        action : ID COLON TYPE ARROW expression SEMICOLON
        """        
    

    # ######################### METHODS DISPATCH ######################################
    
    def p_expression_dispatch(self, p):
        """
        expression : expression DOT ID LPAREN arguments_list_opt RPAREN
        """        
    
    def p_arguments_list_opt(self, p):
        """
        arguments_list_opt : arguments_list
                           | empty
        """        

    
    def p_arguments_list(self, p):
        """
        arguments_list : arguments_list COMMA expression
                       | expression
        """        
            
    def p_expression_static_dispatch(self, p):
        """
        expression : expression AT TYPE DOT ID LPAREN arguments_list_opt RPAREN
        """        
        
    
    def p_expression_self_dispatch(self, p):
        """
        expression : ID LPAREN arguments_list_opt RPAREN
        """        



    # ######################### ################## ###################################
    
    def p_empty(self, p):
        """
        empty :
        """        

    def findColumn(self, trackedRow):
        for i in range(len(self.parser.symstack) -1, 1, -1):
            if self.parser.symstack[i].lineno != trackedRow:
                return self.parser.symstack[i].lexpos
        return 0

    def p_error(self, p):
        """
        Error rule for Syntax Errors handling and reporting.
        """
        if p:
            self.errors_parser.append(
            error(message= "Error at or near %s" %p.value,
            error_type="SyntacticError",
            row_and_col= (p.lineno, self.real_col[str(p)] )))
            
        else:
            self.errors_parser.append(
            error(message= "EOF in string",
            error_type="SyntacticError",
            row_and_col= (0, 0 )))
            
        


def run_parser(tokens, source_program, real_col):
    #print(source_program)
    parserCool = pyCoolParser(tokens, real_col)
    lexer.lineno = 1
    parserCool.parser.parse(source_program, lexer=lexer)
    return parserCool.errors_parser

