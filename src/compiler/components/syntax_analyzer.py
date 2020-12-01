import ply.yacc as yacc
from ply.yacc import YaccProduction, YaccSymbol
from ..utils.errors import error
from ..utils.AST_definitions import *
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
        p[0] = NodeProgram(p[1])

    def p_class_list(self, p):
        """
        class_list : class_list class SEMICOLON
                   | class SEMICOLON
        """
        p[0] = NodeClassTuple((p[1],) if len(p) == 3 else p[1] + (p[2], ))

    def p_class(self, p):
        """
        class : CLASS TYPE LBRACE features_list_opt RBRACE
        """
        p[0] = NodeClass(idName = p[2], methods= p[4]['methods'], attributes= p[4]['attributes'], parent = "Object")

    def p_class_inherits(self, p):
        """
        class : CLASS TYPE INHERITS TYPE LBRACE features_list_opt RBRACE
        """
        p[0] = NodeClass(idName = p[2],
                        methods= p[6]['methods'],
                        attributes= p[6]['attributes'],
                        parent = p[4])

    def p_feature_list_opt(self, p):
        """
        features_list_opt : features_list
                          | empty
        """
        p[0] = p[1] if p[1] else { 'methods': (), 'attributes': () }

    def p_feature_list(self, p):
        """
        features_list : features_list feature SEMICOLON
                      | feature SEMICOLON
        """
        if len(p) == 3:
            p[0] = { 'methods': (), 'attributes': () }
            key = 'methods' if type(p[1]) is NodeClassMethod else 'attributes'
            p[0][key] += (p[1], )
        else:
            key = 'methods' if type(p[2]) is NodeClassMethod else 'attributes'
            p[1][key] += (p[2], )
            p[0] = p[1]

    def p_feature_method(self, p):
        """
        feature : ID LPAREN formal_params_list RPAREN COLON TYPE LBRACE expression RBRACE
        """
        p[0] = NodeClassMethod(idName=p[1],
        argNames = [ x.idName for x in p[3] ],
        argTypesNames = [ x.paramType for x in p[3] ],
        return_type=p[6],
        body=p[8])

    def p_feature_method_no_formals(self, p):
        """
        feature : ID LPAREN RPAREN COLON TYPE LBRACE expression RBRACE
        """
        p[0] = NodeClassMethod(idName=p[1], argNames = [], argTypesNames = [], return_type=p[5], body=p[7])

    def p_feature_attr_initialized(self, p):
        """
        feature : ID COLON TYPE ASSIGN expression
        """
        p[0] = NodeAttr(idName= p[1], attr_type= p[3], expr= p[5])

    def p_feature_attr(self, p):
        """
        feature : ID COLON TYPE
        """
        p[0] = NodeAttr(idName= p[1], attr_type= p[3], expr= None)

    def p_formal_list_many(self, p):
        """
        formal_params_list  : formal_params_list COMMA formal_param
                            | formal_param
        """
        p[0] = (p[1], ) if len(p) == 2 else p[1] + (p[3], ) 

    def p_formal(self, p):
        """
        formal_param : ID COLON TYPE
        """
        p[0] = NodeFormalParam(idName=p[1], param_type=p[3])

    def p_expression_object_identifier(self, p):
        """
        expression : ID
        """
        p[0]= NodeObject(idName= p[1]) 
        
    def p_expression_integer_constant(self, p):
        """
        expression : INTEGER
        """
        p[0]= NodeInteger(content= p[1])

    def p_expression_boolean_constant(self, p):
        """
        expression : BOOLEAN
        """
        p[0]= NodeBoolean(content= p[1])

    def p_expression_string_constant(self, p):
        """
        expression : STRING
        """
        p[0]= NodeString(content= p[1])

    def p_expr_self(self, p):
        """
        expression  : SELF
        """
        p[0]= NodeSelf()

    def p_expression_block(self, p):
        """
        expression : LBRACE block_list RBRACE
        """        
        p[0]= NodeBlock(expr_list= p[2])        

    def p_block_list(self, p):
        """
        block_list : block_list expression SEMICOLON
                   | expression SEMICOLON
        """        
        p[0]= (p[1], ) if len(p) == 3 else p[1] + (p[2], )

    def p_expression_assignment(self, p):
        """
        expression : ID ASSIGN expression
        """        
        p[0] = NodeAssignment(idName= NodeObject(idName= p[1]), expr= p[3])

# ######################### UNARY OPERATIONS #######################################
    
    def p_expression_new(self, p):
        """
        expression : NEW TYPE
        """
        p[0] = NodeNewObject(new_type= p[2])


    def p_expression_isvoid(self, p):
        """
        expression : ISVOID expression
        """
        p[0] = NodeIsVoid(expr= p[2])
        
    def p_expression_integer_complement(self, p):
        """
        expression : INT_COMP expression
        """
        p[0] = NodeIntegerComplement(p[2])        
        

    def p_expression_boolean_complement(self, p):
        """
        expression : NOT expression
        """
        p[0] = NodeBooleanComplement(p[2])        
    
    # ######################### PARENTHESIZED, MATH & COMPARISONS #####################
    
    def p_expression_math_operations(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULTIPLY expression
                   | expression DIVIDE expression
        """        
        if p[2] == '+':
            p[0] = NodeAddition(first=p[1], second=p[3])
        elif p[2] == '-':
            p[0] = NodeSubtraction(first=p[1], second=p[3])
        elif p[2] == '*':
            p[0] = NodeMultiplication(first=p[1], second=p[3])
        elif p[2] == '/':
            p[0] = NodeDivision(first=p[1], second=p[3])

    def p_expression_math_comparisons(self, p):
        """
        expression : expression LT expression
                   | expression LTEQ expression
                   | expression EQ expression
        """    
        if p[2] == '<':
            p[0] = NodeLessThan(first=p[1], second=p[3])
        elif p[2] == '<=':
            p[0] = NodeLessThanOrEqual(first=p[1], second=p[3])
        elif p[2] == '=':
            p[0] = NodeEqual(first=p[1], second=p[3])    
        
    def p_expression_with_parenthesis(self, p):
        """
        expression : LPAREN expression RPAREN
        """        
        p[0] = p[2]

    # ######################### CONTROL FLOW EXPRESSIONS ##############################
    
    def p_expression_if_conditional(self, p):
        """
        expression : IF expression THEN expression ELSE expression FI
        """        
        p[0]= NodeIf(predicate=p[2], then_body=p[4], else_body=p[6])

    def p_expression_while_loop(self, p):
        """
        expression : WHILE expression LOOP expression POOL
        """        
        p[0] = NodeWhileLoop(predicate=p[2], body=p[4])

    ## ######################### LET EXPRESSIONS ########################################
    def p_expression_let(self, p):
        """
         expression : let_expression
        """        
        p[0]= p[1]

    def p_expression_let_simple(self, p):
        """
        let_expression : LET nested_lets IN expression
        """
        p[0]= NodeLetComplex(nested_lets= p[2], body= p[4])

    def p_nested_lets_simple(self, p):
        """
        nested_lets : ID COLON TYPE
                    | nested_lets COMMA ID COLON TYPE
        """
        p[0]= NodeLet(idName= p[1], return_type= p[3],
        body = None)

    def p_nested_lets_initialize(self, p):
        """
        nested_lets : ID COLON TYPE ASSIGN expression
                    | nested_lets COMMA ID COLON TYPE ASSIGN expression
        """
        p[0]= NodeLet(idName= p[1],
        return_type= p[3],
        body= p[5])

    # ######################### CASE EXPRESSION ########################################
    
    def p_expression_case(self, p):
        """
        expression : CASE expression OF actions_list ESAC
        """        
        p[0]= NodeCase(expr=p[2], actions=p[4])

    def p_actions_list(self, p):
        """
        actions_list : actions_list action
                     | action
        """        
        p[0]= (p[1],) if len(p) == 2 else p[1] + (p[2],)

    def p_action_expr(self, p):
        """
        action : ID COLON TYPE ARROW expression SEMICOLON
        """
        p[0] = (p[1], p[3], p[5])

    # ######################### METHODS DISPATCH ######################################
    
    def p_expression_dispatch(self, p):
        """
        expression : expression DOT ID LPAREN arguments_list_opt RPAREN
        """        
        p[0] = NodeDynamicDispatch(idName=p[1], 
        method=p[3], arguments=p[5])

    def p_arguments_list_opt(self, p):
        """
        arguments_list_opt : arguments_list
                           | empty
        """        
        p[0] = tuple() if p.slice[1].type == "empty" else p[1]
    
    def p_arguments_list(self, p):
        """
        arguments_list : arguments_list COMMA expression
                       | expression
        """        
        p[0]= (p[1], ) if len(p) == 2 else p[1] + (p[2], )

    def p_expression_static_dispatch(self, p):
        """
        expression : expression AT TYPE DOT ID LPAREN arguments_list_opt RPAREN
        """        
        p[0] = NodeStaticDispatch(idName=p[1],
        dispatch_type=p[3], method=p[5], arguments=p[7])
    
    def p_expression_self_dispatch(self, p):
        """
        expression : ID LPAREN arguments_list_opt RPAREN
        """        
        p[0] = NodeDynamicDispatch(idName=NodeSelf(),
        method=p[1], arguments=p[3])


    # ######################### ################## ###################################
    
    def p_empty(self, p):
        """
        empty :
        """
        p[0]= None

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
    #print("The source_program ", source_program)
    parserCool = pyCoolParser(tokens, real_col)
    lexer.lineno = 1
    ast_result = parserCool.parser.parse(source_program, lexer=lexer)
    #print("The ast_result ", ast_result)
    return ast_result, parserCool.errors_parser
