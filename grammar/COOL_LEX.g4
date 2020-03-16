lexer grammar COOL_LEX;

CLASS
   : C L A S S
   ;

ELSE
   : E L S E
   ;

FALSE
   : 'f' A L S E
   ;

FI
   : F I
   ;

IF
   : I F
   ;

IN
   : I N
   ;

INHERITS
   : I N H E R I T S
   ;

ISVOID
   : I S V O I D
   ;

LET
   : L E T
   ;

LOOP
   : L O O P
   ;

POOL
   : P O O L
   ;

THEN
   : T H E N
   ;

WHILE
   : W H I L E
   ;

CASE
   : C A S E
   ;

ESAC
   : E S A C
   ;

NEW
   : N E W
   ;

OF
   : O F
   ;

NOT
   : N O T
   ;

TRUE
   : 't' R U E
   ;
   // primitives

STRING
    : STRING_SIMPLE
    | STRING_MULTILINE
    ;

STRING_SIMPLE_START :
  '"' -> pushMode(SIMPLE_STR)
  ;

STRING_SIMPLE
   : STRING_SIMPLE_START STRING_SIMPLE_CONTENT STRING_SIMPLE_STOP
   | STRING_SIMPLE_START STRING_SIMPLE_STOP
   ;

fragment
STRING_CONTENT
    : ESC | ~["\r\n\u0000]
    ;

STRING_FIRSTLINE
   : '"' STRING_CONTENT* '\\\r\n' -> pushMode(MULTILINE_STR)
   ;

INT
   : [0-9]+
   ;

TYPEID
   : [A-Z] [_0-9A-Za-z]*
   ;

OBJECTID
   : [a-z] [_0-9A-Za-z]*
   ;

ASSIGNMENT
   : '<-'
   ;

CASE_ARROW
   : '=>'
   ;

ADD
   : '+'
   ;

MINUS
   : '-'
   ;

MULTIPLY
   : '*'
   ;

DIVISION
   : '/'
   ;

LESS_THAN
   : '<'
   ;

LESS_EQUAL
   : '<='
   ;

EQUAL
   : '='
   ;

INTEGER_NEGATIVE
   : '~'
   ;

OPEN_ROUND
    : '('
    ;

CLOSE_ROUND
    : ')'
    ;

OPEN_CURLY
    : '{'
    ;

CLOSE_CURLY
    : '}'
    ;

AT
    : '@'
    ;

DOT
    : '.'
    ;

COMMA
    : ','
    ;

COLON
    : ':'
    ;

SEMICOLON
    : ';'
    ;

fragment A
   : [aA]
   ;

fragment C
   : [cC]
   ;

fragment D
   : [dD]
   ;

fragment E
   : [eE]
   ;

fragment F
   : [fF]
   ;

fragment H
   : [hH]
   ;

fragment I
   : [iI]
   ;

fragment L
   : [lL]
   ;

fragment N
   : [nN]
   ;

fragment O
   : [oO]
   ;

fragment P
   : [pP]
   ;

fragment R
   : [rR]
   ;

fragment S
   : [sS]
   ;

fragment T
   : [tT]
   ;

fragment U
   : [uU]
   ;

fragment V
   : [vV]
   ;

fragment W
   : [wW]
   ;

fragment ESC
   : '\\' (["\\/bfnrt] | UNICODE)
   ;

fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;

fragment HEX
   : [0-9a-fA-F]
   ;

   // skip spaces, tabs, newlines, note that \v is not suppoted in antlr

WHITESPACE
   : [ \t\r\n\f]+ -> skip
   ;

   // comments

ONE_LINE_COMMENT
   : '--' (~ '\n')* '\n'? -> skip
   ;

OPEN_COMMENT
   : '(*' -> pushMode(MULTILINE_COMMENT)
   ;

mode MULTILINE_COMMENT;

COMMENT
   : ((OPEN_COMMENT COMMENT  CLOSE_COMMENT) | (.)+? ) -> skip
   ;

CLOSE_COMMENT
   : '*)' -> popMode
   ;

mode MULTILINE_STR;

STRING_INNERLINE
   : STRING_CONTENT* '\\\r\n'
   ;

STRING_LASTLINE
   : STRING_CONTENT* '"' -> popMode
   ;

STRING_MULTILINE
    : STRING_FIRSTLINE STRING_INNERLINE* STRING_LASTLINE
    ;

mode SIMPLE_STR;

STRING_SIMPLE_CONTENT
    : STRING_CONTENT+
    ;

STRING_SIMPLE_STOP :
  '"' -> popMode
  ;

