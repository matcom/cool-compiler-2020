
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftDOTleftATleftNOTleftISVOIDleftSTARDIVleftPLUSMINUSleftGREATEREQLOWEREQLOWERGREATEREQUALleftLNOTrightASSIGNARROW ASSIGN AT BOOL CASE CBRACKET CLASS COLON COMMA CPAREN DIV DOT ELSE EQUAL ESAC FI GREATER GREATEREQ ID IF IN INHERITS INT ISVOID LET LNOT LOOP LOWER LOWEREQ MINUS NEW NOT OBRACKET OF OPAREN PLUS POOL SEMICOLON STAR STRING THEN TYPE WHILEprogram : class_listempty :class_list : def_class class_list\n                  | def_classdef_class : CLASS TYPE OBRACKET feature_list CBRACKET SEMICOLON\n                  | CLASS TYPE INHERITS TYPE OBRACKET feature_list CBRACKET SEMICOLONfeature_list : def_attr SEMICOLON feature_list\n                    | def_func SEMICOLON feature_list\n                    | emptydef_attr : assign_elemdef_func : ID OPAREN param_list CPAREN COLON TYPE OBRACKET expr_list CBRACKETparam_list : param COMMA param_list\n                  | param\n                  | emptyparam : ID COLON TYPEexpr_list : expr expr_list\n                 | exprassign : ID ASSIGN exprfunc_call : expr AT TYPE DOT ID OPAREN arg_list CPAREN\n                 | expr DOT ID OPAREN arg_list CPAREN\n                 | ID OPAREN arg_list CPARENarg_list : expr COMMA arg_list\n                | expr\n                | emptyif_expr : IF expr THEN expr ELSE expr FIloop_expr : WHILE expr LOOP expr POOLblock : OBRACKET block_list CBRACKETblock_list : expr SEMICOLON block_list\n                  | expr SEMICOLONlet_expr : LET assign_list IN exprassign_list : assign_elem COMMA assign_list\n                   | assign_elemassign_elem : ID COLON TYPE assign_operassign_oper : ASSIGN expr\n                    | emptycase_expr : CASE expr  OF case_list ESACcase_list : case_elem SEMICOLON case_list\n                 | case_elem SEMICOLONcase_elem : ID COLON TYPE ARROW exprinit_expr : NEW TYPEexpr : NOT expr\n            | cmp\n            | ecmp : e LOWER e\n           | e GREATER e\n           | e EQUAL e\n           | e GREATEREQ e\n           | e LOWEREQ ee : e PLUS t\n         | e MINUS t\n         | tt : t STAR f\n         | t DIV f\n         | ff : NOT f\n         | OPAREN expr CPAREN\n         | atom\n         | ISVOID fatom : ID\n            | INT\n            | BOOL\n            | STRING\n            | assign\n            | func_call\n            | if_expr\n            | loop_expr\n            | block\n            | let_expr\n            | case_expr\n            | init_expr'
    
_lr_action_items = {'CLASS':([0,3,22,68,],[4,4,-5,-6,]),'$end':([1,2,3,5,22,68,],[0,-1,-4,-3,-5,-6,]),'TYPE':([4,8,20,31,39,67,70,145,],[6,15,29,38,69,97,99,150,]),'OBRACKET':([6,15,35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,69,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[7,21,64,64,-42,-43,-51,-54,64,-57,64,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,64,64,64,64,98,-41,-54,64,64,64,64,64,64,64,64,64,-58,64,64,64,-40,64,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,64,64,-27,64,64,64,64,-21,64,-30,64,-26,-36,64,-20,-25,64,-19,]),'INHERITS':([6,],[8,]),'ID':([7,17,18,19,21,33,35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,71,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,120,121,123,124,125,126,127,131,141,142,143,144,146,147,152,153,154,],[14,14,14,25,14,25,50,50,-42,-43,-51,-54,50,-57,50,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,50,50,50,95,50,100,-41,-54,50,50,50,50,50,50,50,50,50,-58,50,50,50,-40,50,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,50,50,-27,50,50,95,135,50,138,50,-21,50,-30,50,-26,-36,135,50,-20,-25,50,-19,]),'CBRACKET':([7,9,12,17,18,21,23,24,30,43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,91,97,101,102,103,104,105,106,107,108,109,110,111,117,118,122,123,126,130,131,137,142,143,147,152,154,],[-2,16,-9,-2,-2,-2,-7,-8,37,-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,117,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-29,136,-17,-21,-28,-30,-16,-26,-36,-20,-25,-19,]),'SEMICOLON':([10,11,13,16,29,34,36,37,41,43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,92,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,134,136,142,143,147,152,154,155,],[17,18,-10,22,-2,-33,-35,68,-34,-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,118,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,144,-11,-26,-36,-20,-25,-19,-39,]),'OPAREN':([14,35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,100,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,138,141,142,143,146,147,152,153,154,],[19,47,47,-42,-43,-51,-54,47,-57,47,88,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,47,47,47,47,-41,-54,47,47,47,47,47,47,47,47,47,-58,47,47,47,-40,47,125,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,47,47,-27,47,47,47,47,-21,47,-30,146,47,-26,-36,47,-20,-25,47,-19,]),'COLON':([14,25,32,95,135,],[20,31,39,20,145,]),'CPAREN':([19,26,27,28,33,38,40,43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,83,84,88,97,101,102,103,104,105,106,107,108,109,110,111,112,113,114,117,125,126,127,131,139,140,142,143,146,147,151,152,154,],[-2,32,-13,-14,-2,-15,-12,-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,110,-58,-2,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,126,-23,-24,-27,-2,-21,-2,-30,147,-22,-26,-36,-2,-20,154,-25,-19,]),'COMMA':([27,29,34,36,38,41,43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,94,97,101,102,103,104,105,106,107,108,109,110,111,113,117,126,131,142,143,147,152,154,],[33,-2,-33,-35,-15,-34,-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,120,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,127,-27,-21,-30,-26,-36,-20,-25,-19,]),'ASSIGN':([29,50,],[35,87,]),'IN':([29,34,36,41,43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,93,94,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,132,142,143,147,152,154,],[-2,-33,-35,-34,-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,119,-32,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-31,-26,-36,-20,-25,-19,]),'NOT':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[42,42,-42,-43,-51,-54,42,-57,85,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,42,42,42,42,-41,-54,85,85,85,85,85,85,85,85,85,-58,85,42,42,-40,42,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,42,42,-27,42,42,42,42,-21,42,-30,42,-26,-36,42,-20,-25,42,-19,]),'ISVOID':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[49,49,-42,-43,-51,-54,49,-57,49,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,49,49,49,49,-41,-54,49,49,49,49,49,49,49,49,49,-58,49,49,49,-40,49,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,49,49,-27,49,49,49,49,-21,49,-30,49,-26,-36,49,-20,-25,49,-19,]),'INT':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[51,51,-42,-43,-51,-54,51,-57,51,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,51,51,51,51,-41,-54,51,51,51,51,51,51,51,51,51,-58,51,51,51,-40,51,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,51,51,-27,51,51,51,51,-21,51,-30,51,-26,-36,51,-20,-25,51,-19,]),'BOOL':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[52,52,-42,-43,-51,-54,52,-57,52,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,52,52,52,52,-41,-54,52,52,52,52,52,52,52,52,52,-58,52,52,52,-40,52,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,52,52,-27,52,52,52,52,-21,52,-30,52,-26,-36,52,-20,-25,52,-19,]),'STRING':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[53,53,-42,-43,-51,-54,53,-57,53,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,53,53,53,53,-41,-54,53,53,53,53,53,53,53,53,53,-58,53,53,53,-40,53,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,53,53,-27,53,53,53,53,-21,53,-30,53,-26,-36,53,-20,-25,53,-19,]),'IF':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[62,62,-42,-43,-51,-54,62,-57,62,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,62,62,62,62,-41,-54,62,62,62,62,62,62,62,62,62,-58,62,62,62,-40,62,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,62,62,-27,62,62,62,62,-21,62,-30,62,-26,-36,62,-20,-25,62,-19,]),'WHILE':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[63,63,-42,-43,-51,-54,63,-57,63,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,63,63,63,63,-41,-54,63,63,63,63,63,63,63,63,63,-58,63,63,63,-40,63,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,63,63,-27,63,63,63,63,-21,63,-30,63,-26,-36,63,-20,-25,63,-19,]),'LET':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[65,65,-42,-43,-51,-54,65,-57,65,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,65,65,65,65,-41,-54,65,65,65,65,65,65,65,65,65,-58,65,65,65,-40,65,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,65,65,-27,65,65,65,65,-21,65,-30,65,-26,-36,65,-20,-25,65,-19,]),'CASE':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[66,66,-42,-43,-51,-54,66,-57,66,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,66,66,66,66,-41,-54,66,66,66,66,66,66,66,66,66,-58,66,66,66,-40,66,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,66,66,-27,66,66,66,66,-21,66,-30,66,-26,-36,66,-20,-25,66,-19,]),'NEW':([35,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,72,73,74,75,76,77,78,79,80,81,82,84,85,87,88,97,98,101,102,103,104,105,106,107,108,109,110,111,115,116,117,118,119,123,125,126,127,131,141,142,143,146,147,152,153,154,],[67,67,-42,-43,-51,-54,67,-57,67,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,67,67,67,67,-41,-54,67,67,67,67,67,67,67,67,67,-58,67,67,67,-40,67,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,67,67,-27,67,67,67,67,-21,67,-30,67,-26,-36,67,-20,-25,67,-19,]),'AT':([41,43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,83,84,86,89,90,92,96,97,101,102,103,104,105,106,107,108,109,110,111,113,117,123,126,128,129,131,142,143,147,148,152,154,155,],[70,-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,70,-54,70,70,70,70,70,-40,-43,-43,-43,-43,-43,-49,-50,-52,-53,-56,-18,70,-27,70,-21,70,70,70,-26,-36,-20,70,-25,-19,70,]),'DOT':([41,43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,83,84,86,89,90,92,96,97,99,101,102,103,104,105,106,107,108,109,110,111,113,117,123,126,128,129,131,142,143,147,148,152,154,155,],[71,-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,71,-54,71,71,71,71,71,-40,124,-43,-43,-43,-43,-43,-49,-50,-52,-53,-56,-18,71,-27,71,-21,71,71,71,-26,-36,-20,71,-25,-19,71,]),'THEN':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,89,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,115,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'LOOP':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,90,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,116,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'OF':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,96,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,121,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'STAR':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,-43,81,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'DIV':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,-43,82,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'LOWER':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,74,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'GREATER':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,75,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'EQUAL':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,76,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'GREATEREQ':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,77,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'LOWEREQ':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,78,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'PLUS':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,79,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'MINUS':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,152,154,],[-42,80,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-54,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,-25,-19,]),'ELSE':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,128,131,142,143,147,152,154,],[-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,141,-30,-26,-36,-20,-25,-19,]),'POOL':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,129,131,142,143,147,152,154,],[-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,142,-30,-26,-36,-20,-25,-19,]),'FI':([43,44,45,46,48,50,51,52,53,54,55,56,57,58,59,60,61,72,73,84,97,101,102,103,104,105,106,107,108,109,110,111,117,126,131,142,143,147,148,152,154,],[-42,-43,-51,-54,-57,-59,-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-41,-54,-58,-40,-44,-45,-46,-47,-48,-49,-50,-52,-53,-56,-18,-27,-21,-30,-26,-36,-20,152,-25,-19,]),'ESAC':([133,144,149,],[143,-38,-37,]),'ARROW':([150,],[153,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_list':([0,3,],[2,5,]),'def_class':([0,3,],[3,3,]),'feature_list':([7,17,18,21,],[9,23,24,30,]),'def_attr':([7,17,18,21,],[10,10,10,10,]),'def_func':([7,17,18,21,],[11,11,11,11,]),'empty':([7,17,18,19,21,29,33,88,125,127,146,],[12,12,12,28,12,36,28,114,114,114,114,]),'assign_elem':([7,17,18,21,65,120,],[13,13,13,13,94,94,]),'param_list':([19,33,],[26,40,]),'param':([19,33,],[27,27,]),'assign_oper':([29,],[34,]),'expr':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[41,72,83,86,89,90,92,96,86,86,86,86,86,86,86,86,86,72,111,113,123,128,129,92,131,123,113,113,148,113,155,]),'cmp':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'e':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[44,44,44,44,44,44,44,44,101,102,103,104,105,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'t':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[45,45,45,45,45,45,45,45,45,45,45,45,45,106,107,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'f':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[46,73,46,84,46,46,46,46,46,46,46,46,46,46,46,108,109,73,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'atom':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'assign':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,]),'func_call':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'if_expr':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'loop_expr':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'block':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,]),'let_expr':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,]),'case_expr':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'init_expr':([35,42,47,49,62,63,64,66,74,75,76,77,78,79,80,81,82,85,87,88,98,115,116,118,119,123,125,127,141,146,153,],[61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,]),'block_list':([64,118,],[91,130,]),'assign_list':([65,120,],[93,132,]),'arg_list':([88,125,127,146,],[112,139,140,151,]),'expr_list':([98,123,],[122,137,]),'case_list':([121,144,],[133,149,]),'case_elem':([121,144,],[134,134,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_list','program',1,'p_program','parser.py',20),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',25),
  ('class_list -> def_class class_list','class_list',2,'p_class_list','parser.py',30),
  ('class_list -> def_class','class_list',1,'p_class_list','parser.py',31),
  ('def_class -> CLASS TYPE OBRACKET feature_list CBRACKET SEMICOLON','def_class',6,'p_def_class','parser.py',40),
  ('def_class -> CLASS TYPE INHERITS TYPE OBRACKET feature_list CBRACKET SEMICOLON','def_class',8,'p_def_class','parser.py',41),
  ('feature_list -> def_attr SEMICOLON feature_list','feature_list',3,'p_feature_list','parser.py',49),
  ('feature_list -> def_func SEMICOLON feature_list','feature_list',3,'p_feature_list','parser.py',50),
  ('feature_list -> empty','feature_list',1,'p_feature_list','parser.py',51),
  ('def_attr -> assign_elem','def_attr',1,'p_def_attr','parser.py',59),
  ('def_func -> ID OPAREN param_list CPAREN COLON TYPE OBRACKET expr_list CBRACKET','def_func',9,'p_def_func','parser.py',64),
  ('param_list -> param COMMA param_list','param_list',3,'p_param_list','parser.py',69),
  ('param_list -> param','param_list',1,'p_param_list','parser.py',70),
  ('param_list -> empty','param_list',1,'p_param_list','parser.py',71),
  ('param -> ID COLON TYPE','param',3,'p_param','parser.py',79),
  ('expr_list -> expr expr_list','expr_list',2,'p_expr_list','parser.py',84),
  ('expr_list -> expr','expr_list',1,'p_expr_list','parser.py',85),
  ('assign -> ID ASSIGN expr','assign',3,'p_assign','parser.py',93),
  ('func_call -> expr AT TYPE DOT ID OPAREN arg_list CPAREN','func_call',8,'p_func_call','parser.py',98),
  ('func_call -> expr DOT ID OPAREN arg_list CPAREN','func_call',6,'p_func_call','parser.py',99),
  ('func_call -> ID OPAREN arg_list CPAREN','func_call',4,'p_func_call','parser.py',100),
  ('arg_list -> expr COMMA arg_list','arg_list',3,'p_arg_list','parser.py',110),
  ('arg_list -> expr','arg_list',1,'p_arg_list','parser.py',111),
  ('arg_list -> empty','arg_list',1,'p_arg_list','parser.py',112),
  ('if_expr -> IF expr THEN expr ELSE expr FI','if_expr',7,'p_if_expr','parser.py',120),
  ('loop_expr -> WHILE expr LOOP expr POOL','loop_expr',5,'p_loop_expr','parser.py',125),
  ('block -> OBRACKET block_list CBRACKET','block',3,'p_block','parser.py',130),
  ('block_list -> expr SEMICOLON block_list','block_list',3,'p_block_list','parser.py',135),
  ('block_list -> expr SEMICOLON','block_list',2,'p_block_list','parser.py',136),
  ('let_expr -> LET assign_list IN expr','let_expr',4,'p_let_expr','parser.py',144),
  ('assign_list -> assign_elem COMMA assign_list','assign_list',3,'p_assign_list','parser.py',149),
  ('assign_list -> assign_elem','assign_list',1,'p_assign_list','parser.py',150),
  ('assign_elem -> ID COLON TYPE assign_oper','assign_elem',4,'p_assign_elem','parser.py',158),
  ('assign_oper -> ASSIGN expr','assign_oper',2,'p_assign_oper','parser.py',163),
  ('assign_oper -> empty','assign_oper',1,'p_assign_oper','parser.py',164),
  ('case_expr -> CASE expr OF case_list ESAC','case_expr',5,'p_case_expr','parser.py',172),
  ('case_list -> case_elem SEMICOLON case_list','case_list',3,'p_case_list','parser.py',177),
  ('case_list -> case_elem SEMICOLON','case_list',2,'p_case_list','parser.py',178),
  ('case_elem -> ID COLON TYPE ARROW expr','case_elem',5,'p_case_elem','parser.py',186),
  ('init_expr -> NEW TYPE','init_expr',2,'p_init_expr','parser.py',191),
  ('expr -> NOT expr','expr',2,'p_expr','parser.py',196),
  ('expr -> cmp','expr',1,'p_expr','parser.py',197),
  ('expr -> e','expr',1,'p_expr','parser.py',198),
  ('cmp -> e LOWER e','cmp',3,'p_cmp','parser.py',206),
  ('cmp -> e GREATER e','cmp',3,'p_cmp','parser.py',207),
  ('cmp -> e EQUAL e','cmp',3,'p_cmp','parser.py',208),
  ('cmp -> e GREATEREQ e','cmp',3,'p_cmp','parser.py',209),
  ('cmp -> e LOWEREQ e','cmp',3,'p_cmp','parser.py',210),
  ('e -> e PLUS t','e',3,'p_e','parser.py',224),
  ('e -> e MINUS t','e',3,'p_e','parser.py',225),
  ('e -> t','e',1,'p_e','parser.py',226),
  ('t -> t STAR f','t',3,'p_t','parser.py',237),
  ('t -> t DIV f','t',3,'p_t','parser.py',238),
  ('t -> f','t',1,'p_t','parser.py',239),
  ('f -> NOT f','f',2,'p_f','parser.py',251),
  ('f -> OPAREN expr CPAREN','f',3,'p_f','parser.py',252),
  ('f -> atom','f',1,'p_f','parser.py',253),
  ('f -> ISVOID f','f',2,'p_f','parser.py',254),
  ('atom -> ID','atom',1,'p_atom','parser.py',268),
  ('atom -> INT','atom',1,'p_atom','parser.py',269),
  ('atom -> BOOL','atom',1,'p_atom','parser.py',270),
  ('atom -> STRING','atom',1,'p_atom','parser.py',271),
  ('atom -> assign','atom',1,'p_atom','parser.py',272),
  ('atom -> func_call','atom',1,'p_atom','parser.py',273),
  ('atom -> if_expr','atom',1,'p_atom','parser.py',274),
  ('atom -> loop_expr','atom',1,'p_atom','parser.py',275),
  ('atom -> block','atom',1,'p_atom','parser.py',276),
  ('atom -> let_expr','atom',1,'p_atom','parser.py',277),
  ('atom -> case_expr','atom',1,'p_atom','parser.py',278),
  ('atom -> init_expr','atom',1,'p_atom','parser.py',279),
]
