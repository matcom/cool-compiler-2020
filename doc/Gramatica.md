# Gramática usada
En lo siguiente mostraremos la gramática BNF usada para la realización de nuestro compilador:
```
program : classdec program
        | classdec
classdec : class type lbracket featurelist rbracket pcoma
         | class type inherits type lbracket featurelist rbracket pcoma
featurelist : feature featurelist
            | empty
feature : attribute pcoma
        | methoddef pcoma
methoddef : id lparen rparen dpoint type lbracket expression rbracket
          | id lparen param paramslistdef rparen dpoint type lbracket expression rbracket
paramslistdef : coma param paramslistdef
              | empty
param : id dpoint type
attribute : id dpoint type
          | id dpoint type assign expression
empty :
expression  : constantexp
            | identifier
            | assignment
            | dispatch
            | conditional
            | loopexp
            | blockexp
            | letexp
            | caseexp
            | newexp
            | isvoidexp
            | aritmetica
            | comparison
            |parenexpression
dispatch : id lparen rparen
         | id lparen expression expressionparams rparen
         | expression point id lparen rparen
         | expression point id lparen expression expressionparams rparen
         | expression arroba type point id lparen rparen
         | expression arroba type point id lparen expression expressionparams rparen
expressionparams : coma expression expressionparams
                 | empty
conditional : if expression then expression else expression fi
loopexp : while expression loop expression pool
blockexp : lbracket expressionlist rbracket
expressionlist : expression pcoma expressionlist
               | empty
letexp : let attribute letattributelist in expression
letattributelist : coma attribute letattributelist
                 | empty
caseexp : case expression of subcase listcase esac
listcase : subcase listcase
         | empty
subcase : id dpoint type implica expression pcoma
newexp : new type
isvoidexp : isvoid expression
aritmetica : expression plus expression
           | expression minus expression
           | expression mult expression
           | expression div expression
           | intnot expression
comparison  : expression less expression
            | expression lesse expression
            | expression equal expression
            | not expression
parenexpression : lparen expression rparen
constantexp : number
            | string
            | true
            | false
identifier : id
assignment : id assign expression
```