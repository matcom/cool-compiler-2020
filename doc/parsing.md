# Parsing 

## Cool Tokens
  
    'CLASS',
    'INHERITS',
    'IF',
    'THEN',
    'ELSE',
    'FI',
    'WHILE',
    'LOOP',
    'POOL',
    'LET',
    'IN',
    'CASE',
    'OF',
    'ESAC',
    'NEW',
    'ISVOID',
    'NOT',
  
    'INTEGER',             # int
    'STRING',              # string
    'BOOL',                # bool
    'PLUS',                # +
    'MINUS',               # -
    'STAR',                # *
    'DIVIDE',              # /
    'BITNOT',              # ~
    'LESS',                # <
    'LESSQ',               # <=
    'EQUALS',              # =
    'WITH',                # =>
    'ASSIGN',              # <-
    'LPAREN',              # (
    'RPAREN',              # )
    'LBRACE',              # {
    'RBRACE',              # }
    'SEMI',                # ;
    'COLON',               # :
    'COMMA',               # ,
    'DOT',                 # .
    'ARROBA',              # @
    'TYPEID',
    'ID',
    'ERROR'

## Cool Grammar

    program      : class_list

    class_list   : def_class
                 | def_class class_list

    def_class    : CLASS TYPEID LBRACE feature_list RBRACE SEMI
                 | CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE SEMI

    feature_list : def_attr SEMI feature_list
                 | def_func SEMI feature_list
                 | empty

    def_attr     : ID COLON TYPEID
                 | ID COLON TYPEID ASSIGN expr
    
    def_func     : ID LPAREN param_list RPAREN COLON TYPEID LBRACE expr RBRACE

    param_list   : param_build
                 | empty

    param_build  : param empty
                 | param COMMA param_build

    param        : ID COLON TYPEID

    expr         : LET let_list IN expr
                 | CASE expr OF cases_list ESAC
                 | IF expr THEN expr ELSE expr FI
                 | WHILE expr LOOP expr POOL
                 | ID ASSIGN expr
                 | arith
                 | expr PLUS expr
                 | expr MINUS expr
                 | expr STAR expr
                 | expr DIVIDE expr
                 | expr LESS expr
                 | expr LESSQ expr
                 | expr EQUALS expr
                 | BITNOT expr
                 | ISVOID expr
                 | NOT expr

    let_list     : let_assign
                 | let_assign COMMA let_list

    let_assign   : ID COLON TYPEID ASSIGN expr
                 | ID COLON TYPEID

    cases_list   : case SEMI
                 | case SEMI cases_list

    case         : ID COLON TYPEID WITH expr

    arith        : base_call

    base_call    : fact ARROBA TYPEID DOT ID LPAREN arg_list RPAREN
                 | fact

    fact         : fact DOT ID LPAREN arg_list RPAREN
                 | ID LPAREN arg_list RPAREN
                 | atom
                 | LPAREN expr RPAREN

    arg_list     : arg_build
                 | empty

    arg_build    : expr empty
                 | expr COMMA arg_build  

    atom         : INTEGER  
                 | ID
                 | NEW TYPEID
                 | LBRACE block RBRACE
                 | BOOL
                 | STRING

    block        : expr SEMI
                 | expr SEMI block

## Cool AST

    ASTNode
    |
    ├── ProgramNode
    │   
    ├── ClassDeclarationNode
    ├── AttrDeclarationNode
    ├── FuncDeclarationNode
    ├── FormalParamNode
    ├── VarDeclarationNode
    |
    ├── ExprNode
    │   ├── OperationNode
    |   |   ├── BinaryOperationNode
    |   |   |   ├── SumNode
    |   |   |   ├── DifNode
    |   |   |   ├── StarNode
    |   |   |   ├── DivNode
    |   |   |   ├── LessNode
    |   |   |   ├── LessEqualNode
    |   |   |   └── EqualNode
    |   |   |
    |   |   └── UnaryOperationNode
    |   |       ├── BitNotNode
    |   |       └── NotNode    
    |   |
    │   ├── VariableNode
    │   ├── NewNode
    │   ├── ConditionalNode
    │   ├── LetNode
    │   ├── LetDeclarationNode
    │   ├── BlockNode
    │   ├── CaseNode
    │   ├── AssignNode
    │   ├── IsVoid
    │   ├── ConditionalNode
    │   ├── WhileNode
    │   |
    │   ├── SelfCallNode
    │   ├── ParentCallNode
    │   ├── ExprCallNode
    |   |
    │   └── ConstantNode
    |       ├── IntegerNode
    |       ├── StringNode
    |       └── BoolNode 
    |
    └── ErrorNode