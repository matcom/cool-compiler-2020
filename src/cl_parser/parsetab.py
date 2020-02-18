
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programrightBITNOTrightISVOIDleftSTARDIVIDEleftPLUSMINUSnonassocLESSLESSQEQUALSrightNOTARROBA ASSIGN BITNOT BOOL CASE CLASS COLON COMMA DIVIDE DOT ELSE EQUALS ESAC FI ID IF IN INHERITS INTEGER ISVOID LBRACE LESS LESSQ LET LOOP LPAREN MINUS NEW NOT OF PLUS POOL RBRACE RPAREN SEMI STAR STRING THEN TYPEID WHILE WITHprogram : class_listempty :class_list : def_class\n                  | def_class class_listdef_class : CLASS TYPEID LBRACE feature_list RBRACE SEMI\n                 | CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE SEMIfeature_list : empty\n                    | def_attr SEMI feature_list\n                    | def_func SEMI feature_listdef_attr : ID COLON TYPEID\n                | ID COLON TYPEID ASSIGN exprdef_func : ID LPAREN param_list RPAREN COLON TYPEID LBRACE expr RBRACEparam_list : emptyparam_list : param_buildparam_build : param empty\n                   | param COMMA param_buildparam : ID COLON TYPEIDexpr : LET let_list IN expr\n            | CASE expr OF cases_list ESAC\n            | IF expr THEN expr ELSE expr FI\n            | WHILE expr LOOP expr POOLexpr : ID ASSIGN exprexpr : arithlet_list : let_assign\n                | let_assign COMMA let_listlet_assign : param ASSIGN expr\n                  | paramcases_list : case SEMI\n                  | case SEMI cases_listcase : ID COLON TYPEID WITH exprexpr : expr PLUS expr\n            | expr MINUS expr\n            | expr STAR expr\n            | expr DIVIDE expr\n            | expr LESS expr\n            | expr LESSQ expr\n            | expr EQUALS exprexpr : BITNOT expr\n            | ISVOID expr\n            | NOT exprarith : base_callbase_call : fact ARROBA TYPEID DOT func_call\n                 | factfact : fact DOT func_call\n            | func_callfunc_call : ID LPAREN arg_list RPARENarg_list : emptyarg_list : arg_buildarg_build : expr empty\n                 | expr COMMA arg_buildfact : atomfact : LPAREN expr RPARENatom : INTEGERatom : IDatom : NEW TYPEIDatom : LBRACE block RBRACEblock : expr SEMI\n             | expr SEMI blockatom : BOOLatom : STRING'
    
_lr_action_items = {'CLASS':([0,3,21,60,],[4,4,-5,-6,]),'$end':([1,2,3,5,21,60,],[0,-1,-3,-4,-5,-6,]),'TYPEID':([4,8,18,32,53,58,79,128,],[6,14,24,57,82,85,104,134,]),'LBRACE':([6,14,31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,85,98,100,102,103,109,110,113,129,136,],[7,20,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,110,54,54,54,54,54,54,54,54,54,]),'INHERITS':([6,],[8,]),'RBRACE':([7,9,10,16,17,20,22,23,30,37,43,47,48,49,50,52,55,56,76,77,78,82,83,86,91,92,93,94,95,96,97,105,107,108,109,111,114,123,124,126,130,131,137,],[-2,15,-7,-2,-2,-2,-8,-9,36,-54,-23,-41,-43,-45,-51,-53,-59,-60,-38,-39,-40,-55,108,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-57,-46,-18,-58,132,-19,-21,-42,-20,]),'ID':([7,16,17,19,20,31,35,39,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,80,98,99,100,101,102,103,109,110,113,122,127,129,136,],[13,13,13,25,13,37,25,25,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,106,37,25,37,119,37,37,37,37,37,106,119,37,37,]),'SEMI':([11,12,15,24,36,37,38,43,47,48,49,50,52,55,56,76,77,78,82,84,86,91,92,93,94,95,96,97,105,107,108,111,114,118,126,130,131,132,137,138,],[16,17,21,-10,60,-54,-11,-23,-41,-43,-45,-51,-53,-59,-60,-38,-39,-40,-55,109,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,127,-19,-21,-42,-12,-20,-30,]),'COLON':([13,25,33,119,],[18,32,58,128,]),'LPAREN':([13,31,37,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,106,109,110,113,129,136,],[19,51,62,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,62,51,51,51,51,51,]),'RPAREN':([19,26,27,28,29,34,37,43,47,48,49,50,52,55,56,57,59,62,76,77,78,81,82,86,87,88,89,90,91,92,93,94,95,96,97,105,107,108,111,112,114,125,126,130,131,137,],[-2,33,-13,-14,-2,-15,-54,-23,-41,-43,-45,-51,-53,-59,-60,-17,-16,-2,-38,-39,-40,107,-55,-22,111,-47,-48,-2,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-49,-18,-50,-19,-21,-42,-20,]),'ASSIGN':([24,37,57,72,],[31,61,-17,100,]),'COMMA':([29,37,43,47,48,49,50,52,55,56,57,71,72,76,77,78,82,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,126,130,131,137,],[35,-54,-23,-41,-43,-45,-51,-53,-59,-60,-17,99,-27,-38,-39,-40,-55,-22,113,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,-26,-19,-21,-42,-20,]),'LET':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'CASE':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'IF':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'WHILE':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'BITNOT':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'ISVOID':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'NOT':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'INTEGER':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'NEW':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'BOOL':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'STRING':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'ARROBA':([37,48,49,50,52,55,56,82,105,107,108,111,],[-54,79,-45,-51,-53,-59,-60,-55,-44,-52,-56,-46,]),'DOT':([37,48,49,50,52,55,56,82,104,105,107,108,111,],[-54,80,-45,-51,-53,-59,-60,-55,122,-44,-52,-56,-46,]),'PLUS':([37,38,43,47,48,49,50,52,55,56,73,74,75,76,77,78,81,82,84,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,120,121,124,126,130,131,135,137,138,],[-54,63,-23,-41,-43,-45,-51,-53,-59,-60,63,63,63,63,63,-40,63,-55,63,63,63,-31,-32,63,63,-35,-36,-37,-44,-52,-56,-46,63,63,63,63,63,-19,-21,-42,63,-20,63,]),'MINUS':([37,38,43,47,48,49,50,52,55,56,73,74,75,76,77,78,81,82,84,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,120,121,124,126,130,131,135,137,138,],[-54,64,-23,-41,-43,-45,-51,-53,-59,-60,64,64,64,64,64,-40,64,-55,64,64,64,-31,-32,64,64,-35,-36,-37,-44,-52,-56,-46,64,64,64,64,64,-19,-21,-42,64,-20,64,]),'STAR':([37,38,43,47,48,49,50,52,55,56,73,74,75,76,77,78,81,82,84,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,120,121,124,126,130,131,135,137,138,],[-54,65,-23,-41,-43,-45,-51,-53,-59,-60,65,65,65,65,65,-40,65,-55,65,65,65,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,65,65,65,65,65,-19,-21,-42,65,-20,65,]),'DIVIDE':([37,38,43,47,48,49,50,52,55,56,73,74,75,76,77,78,81,82,84,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,120,121,124,126,130,131,135,137,138,],[-54,66,-23,-41,-43,-45,-51,-53,-59,-60,66,66,66,66,66,-40,66,-55,66,66,66,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,66,66,66,66,66,-19,-21,-42,66,-20,66,]),'LESS':([37,38,43,47,48,49,50,52,55,56,73,74,75,76,77,78,81,82,84,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,120,121,124,126,130,131,135,137,138,],[-54,67,-23,-41,-43,-45,-51,-53,-59,-60,67,67,67,67,67,-40,67,-55,67,67,67,67,67,67,67,None,None,None,-44,-52,-56,-46,67,67,67,67,67,-19,-21,-42,67,-20,67,]),'LESSQ':([37,38,43,47,48,49,50,52,55,56,73,74,75,76,77,78,81,82,84,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,120,121,124,126,130,131,135,137,138,],[-54,68,-23,-41,-43,-45,-51,-53,-59,-60,68,68,68,68,68,-40,68,-55,68,68,68,68,68,68,68,None,None,None,-44,-52,-56,-46,68,68,68,68,68,-19,-21,-42,68,-20,68,]),'EQUALS':([37,38,43,47,48,49,50,52,55,56,73,74,75,76,77,78,81,82,84,86,90,91,92,93,94,95,96,97,105,107,108,111,114,116,120,121,124,126,130,131,135,137,138,],[-54,69,-23,-41,-43,-45,-51,-53,-59,-60,69,69,69,69,69,-40,69,-55,69,69,69,69,69,69,69,None,None,None,-44,-52,-56,-46,69,69,69,69,69,-19,-21,-42,69,-20,69,]),'OF':([37,43,47,48,49,50,52,55,56,73,76,77,78,82,86,91,92,93,94,95,96,97,105,107,108,111,114,126,130,131,137,],[-54,-23,-41,-43,-45,-51,-53,-59,-60,101,-38,-39,-40,-55,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,-19,-21,-42,-20,]),'THEN':([37,43,47,48,49,50,52,55,56,74,76,77,78,82,86,91,92,93,94,95,96,97,105,107,108,111,114,126,130,131,137,],[-54,-23,-41,-43,-45,-51,-53,-59,-60,102,-38,-39,-40,-55,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,-19,-21,-42,-20,]),'LOOP':([37,43,47,48,49,50,52,55,56,75,76,77,78,82,86,91,92,93,94,95,96,97,105,107,108,111,114,126,130,131,137,],[-54,-23,-41,-43,-45,-51,-53,-59,-60,103,-38,-39,-40,-55,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,-19,-21,-42,-20,]),'IN':([37,43,47,48,49,50,52,55,56,57,70,71,72,76,77,78,82,86,91,92,93,94,95,96,97,105,107,108,111,114,115,116,126,130,131,137,],[-54,-23,-41,-43,-45,-51,-53,-59,-60,-17,98,-24,-27,-38,-39,-40,-55,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,-25,-26,-19,-21,-42,-20,]),'ELSE':([37,43,47,48,49,50,52,55,56,76,77,78,82,86,91,92,93,94,95,96,97,105,107,108,111,114,120,126,130,131,137,],[-54,-23,-41,-43,-45,-51,-53,-59,-60,-38,-39,-40,-55,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,129,-19,-21,-42,-20,]),'POOL':([37,43,47,48,49,50,52,55,56,76,77,78,82,86,91,92,93,94,95,96,97,105,107,108,111,114,121,126,130,131,137,],[-54,-23,-41,-43,-45,-51,-53,-59,-60,-38,-39,-40,-55,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,130,-19,-21,-42,-20,]),'FI':([37,43,47,48,49,50,52,55,56,76,77,78,82,86,91,92,93,94,95,96,97,105,107,108,111,114,126,130,131,135,137,],[-54,-23,-41,-43,-45,-51,-53,-59,-60,-38,-39,-40,-55,-22,-31,-32,-33,-34,-35,-36,-37,-44,-52,-56,-46,-18,-19,-21,-42,137,-20,]),'ESAC':([117,127,133,],[126,-28,-29,]),'WITH':([134,],[136,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_list':([0,3,],[2,5,]),'def_class':([0,3,],[3,3,]),'feature_list':([7,16,17,20,],[9,22,23,30,]),'empty':([7,16,17,19,20,29,62,90,],[10,10,10,27,10,34,88,112,]),'def_attr':([7,16,17,20,],[11,11,11,11,]),'def_func':([7,16,17,20,],[12,12,12,12,]),'param_list':([19,],[26,]),'param_build':([19,35,],[28,59,]),'param':([19,35,39,99,],[29,29,72,72,]),'expr':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[38,73,74,75,76,77,78,81,84,86,90,91,92,93,94,95,96,97,114,116,120,121,84,124,90,135,138,]),'arith':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'base_call':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),'fact':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'func_call':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,80,98,100,102,103,109,110,113,122,129,136,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,105,49,49,49,49,49,49,49,131,49,49,]),'atom':([31,40,41,42,44,45,46,51,54,61,62,63,64,65,66,67,68,69,98,100,102,103,109,110,113,129,136,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'let_list':([39,99,],[70,115,]),'let_assign':([39,99,],[71,71,]),'block':([54,109,],[83,123,]),'arg_list':([62,],[87,]),'arg_build':([62,113,],[89,125,]),'cases_list':([101,127,],[117,133,]),'case':([101,127,],[118,118,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_list','program',1,'p_program','config.py',12),
  ('empty -> <empty>','empty',0,'p_empty','config.py',17),
  ('class_list -> def_class','class_list',1,'p_class_list','config.py',22),
  ('class_list -> def_class class_list','class_list',2,'p_class_list','config.py',23),
  ('def_class -> CLASS TYPEID LBRACE feature_list RBRACE SEMI','def_class',6,'p_def_class','config.py',31),
  ('def_class -> CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE SEMI','def_class',8,'p_def_class','config.py',32),
  ('feature_list -> empty','feature_list',1,'p_feature_list','config.py',40),
  ('feature_list -> def_attr SEMI feature_list','feature_list',3,'p_feature_list','config.py',41),
  ('feature_list -> def_func SEMI feature_list','feature_list',3,'p_feature_list','config.py',42),
  ('def_attr -> ID COLON TYPEID','def_attr',3,'p_def_attr','config.py',50),
  ('def_attr -> ID COLON TYPEID ASSIGN expr','def_attr',5,'p_def_attr','config.py',51),
  ('def_func -> ID LPAREN param_list RPAREN COLON TYPEID LBRACE expr RBRACE','def_func',9,'p_def_func','config.py',59),
  ('param_list -> empty','param_list',1,'p_param_list_ept','config.py',64),
  ('param_list -> param_build','param_list',1,'p_param_list_prm','config.py',68),
  ('param_build -> param empty','param_build',2,'p_param_build','config.py',72),
  ('param_build -> param COMMA param_build','param_build',3,'p_param_build','config.py',73),
  ('param -> ID COLON TYPEID','param',3,'p_param','config.py',81),
  ('expr -> LET let_list IN expr','expr',4,'p_expr','config.py',88),
  ('expr -> CASE expr OF cases_list ESAC','expr',5,'p_expr','config.py',89),
  ('expr -> IF expr THEN expr ELSE expr FI','expr',7,'p_expr','config.py',90),
  ('expr -> WHILE expr LOOP expr POOL','expr',5,'p_expr','config.py',91),
  ('expr -> ID ASSIGN expr','expr',3,'p_expr_assign','config.py',104),
  ('expr -> arith','expr',1,'p_expr_arith','config.py',109),
  ('let_list -> let_assign','let_list',1,'p_let_list','config.py',115),
  ('let_list -> let_assign COMMA let_list','let_list',3,'p_let_list','config.py',116),
  ('let_assign -> param ASSIGN expr','let_assign',3,'p_let_assign','config.py',123),
  ('let_assign -> param','let_assign',1,'p_let_assign','config.py',124),
  ('cases_list -> case SEMI','cases_list',2,'p_cases_list','config.py',133),
  ('cases_list -> case SEMI cases_list','cases_list',3,'p_cases_list','config.py',134),
  ('case -> ID COLON TYPEID WITH expr','case',5,'p_case','config.py',141),
  ('expr -> expr PLUS expr','expr',3,'p_expr_binary','config.py',160),
  ('expr -> expr MINUS expr','expr',3,'p_expr_binary','config.py',161),
  ('expr -> expr STAR expr','expr',3,'p_expr_binary','config.py',162),
  ('expr -> expr DIVIDE expr','expr',3,'p_expr_binary','config.py',163),
  ('expr -> expr LESS expr','expr',3,'p_expr_binary','config.py',164),
  ('expr -> expr LESSQ expr','expr',3,'p_expr_binary','config.py',165),
  ('expr -> expr EQUALS expr','expr',3,'p_expr_binary','config.py',166),
  ('expr -> BITNOT expr','expr',2,'p_expr_unary','config.py',185),
  ('expr -> ISVOID expr','expr',2,'p_expr_unary','config.py',186),
  ('expr -> NOT expr','expr',2,'p_expr_unary','config.py',187),
  ('arith -> base_call','arith',1,'p_arith_basecall','config.py',196),
  ('base_call -> fact ARROBA TYPEID DOT func_call','base_call',5,'p_basecall','config.py',202),
  ('base_call -> fact','base_call',1,'p_basecall','config.py',203),
  ('fact -> fact DOT func_call','fact',3,'p_factcall','config.py',210),
  ('fact -> func_call','fact',1,'p_factcall','config.py',211),
  ('func_call -> ID LPAREN arg_list RPAREN','func_call',4,'p_func_call','config.py',218),
  ('arg_list -> empty','arg_list',1,'p_arglist_ept','config.py',222),
  ('arg_list -> arg_build','arg_list',1,'p_arglist_prm','config.py',226),
  ('arg_build -> expr empty','arg_build',2,'p_arg_build','config.py',230),
  ('arg_build -> expr COMMA arg_build','arg_build',3,'p_arg_build','config.py',231),
  ('fact -> atom','fact',1,'p_factatom','config.py',240),
  ('fact -> LPAREN expr RPAREN','fact',3,'p_fact_group','config.py',244),
  ('atom -> INTEGER','atom',1,'p_atom_int','config.py',248),
  ('atom -> ID','atom',1,'p_atom_id','config.py',252),
  ('atom -> NEW TYPEID','atom',2,'p_atom_new','config.py',256),
  ('atom -> LBRACE block RBRACE','atom',3,'p_atom_block','config.py',260),
  ('block -> expr SEMI','block',2,'p_block','config.py',264),
  ('block -> expr SEMI block','block',3,'p_block','config.py',265),
  ('atom -> BOOL','atom',1,'p_atom_bool','config.py',272),
  ('atom -> STRING','atom',1,'p_atom_string','config.py',276),
]
