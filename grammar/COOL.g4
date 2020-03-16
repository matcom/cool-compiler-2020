parser grammar COOL;

options {
    tokenVocab=COOL_LEX;
}

program
   : programBlocks EOF
   ;

programBlocks
   : classDefine SEMICOLON programBlocks? # classes
   ;

classDefine
   : CLASS TYPEID (INHERITS TYPEID)? OPEN_CURLY (feature SEMICOLON)* CLOSE_CURLY
   ;

feature
   : OBJECTID OPEN_ROUND (formal (COMMA formal)*)* CLOSE_ROUND COLON TYPEID OPEN_CURLY expression CLOSE_CURLY # method
   | OBJECTID COLON TYPEID (ASSIGNMENT expression)? # property
   ;

formal
   : OBJECTID COLON TYPEID
   ;
/* method argument */
   
   
expression
   : expression (AT TYPEID)? DOT OBJECTID OPEN_ROUND (expression (COMMA expression)*)? CLOSE_ROUND # methodCall
   | OBJECTID OPEN_ROUND (expression (COMMA expression)*)? CLOSE_ROUND # ownMethodCall
   | IF expression THEN expression ELSE expression FI # if
   | WHILE expression LOOP expression POOL # while
   | OPEN_CURLY (expression SEMICOLON)+ CLOSE_CURLY # block
   | LET OBJECTID COLON TYPEID (ASSIGNMENT expression)? (COMMA OBJECTID COLON TYPEID (ASSIGNMENT expression)?)* IN expression # letIn
   | CASE expression OF (OBJECTID COLON TYPEID CASE_ARROW expression SEMICOLON)+ ESAC # case
   | NEW TYPEID # new
   | INTEGER_NEGATIVE expression # negative
   | ISVOID expression # isvoid
   | expression MULTIPLY expression # multiply
   | expression DIVISION expression # division
   | expression ADD expression # add
   | expression MINUS expression # minus
   | expression LESS_THAN expression # lessThan
   | expression LESS_EQUAL expression # lessEqual
   | expression EQUAL expression # equal
   | NOT expression # boolNot
   | OPEN_ROUND expression CLOSE_ROUND # parentheses
   | OBJECTID # id
   | INT # int
   | STRING # string
   | TRUE # true
   | FALSE # false
   | OBJECTID ASSIGNMENT expression # assignment
   ;
   // key words
