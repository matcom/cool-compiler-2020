
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programrightBITNOTrightISVOIDleftSTARDIVIDEleftPLUSMINUSnonassocLESSLESSQEQUALSrightNOTARROBA ASSIGN BITNOT BOOL CASE CLASS COLON COMMA DIVIDE DOT ELSE EQUALS ESAC FI ID IF IN INHERITS INTEGER ISVOID LBRACE LESS LESSQ LET LOOP LPAREN MINUS NEW NOT OF PLUS POOL RBRACE RPAREN SEMI STAR STRING THEN TYPEID WHILE WITHprogram : class_listempty :class_list : def_class\n                  | def_class class_listdef_class : CLASS TYPEID LBRACE feature_list RBRACE SEMI\n                 | CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE SEMIfeature_list : empty\n                    | def_attr SEMI feature_list\n                    | def_func SEMI feature_listdef_attr : ID COLON TYPEID\n                | ID COLON TYPEID ASSIGN exprdef_func : ID LPAREN param_list RPAREN COLON TYPEID LBRACE expr RBRACEparam_list : empty\n                  | param\n                  | param COMMA param_listparam : ID COLON TYPEIDexpr : LET let_list IN expr\n            | CASE expr OF cases_list ESAC\n            | IF expr THEN expr ELSE expr FI\n            | WHILE expr LOOP expr POOLexpr : ID ASSIGN exprexpr : arithlet_list : let_assign\n                | let_assign COMMA let_listlet_assign : param ASSIGN expr\n                  | paramcases_list : case SEMI\n                  | case SEMI cases_listcase : ID COLON TYPEID WITH exprarith : arith PLUS arith\n             | arith MINUS arith\n             | arith STAR arith\n             | arith DIVIDE arith\n             | arith LESS arith\n             | arith LESSQ arith\n             | arith EQUALS aritharith : BITNOT arith\n             | ISVOID arith\n             | NOT aritharith : base_callbase_call : fact ARROBA TYPEID DOT func_call\n                 | factfact : fact DOT func_call\n            | func_callfunc_call : ID LPAREN arg_list RPARENarg_list : empty\n                | expr\n                | expr COMMA arg_listfact : atomfact : LPAREN expr RPARENatom : INTEGERatom : IDatom : NEW TYPEIDatom : LBRACE block RBRACEblock : expr SEMI\n             | expr SEMI blockatom : BOOLatom : STRING'
    
_lr_action_items = {'CLASS':([0,3,21,58,],[4,4,-5,-6,]),'$end':([1,2,3,5,21,58,],[0,-1,-3,-4,-5,-6,]),'TYPEID':([4,8,18,31,51,56,78,125,],[6,14,24,55,81,84,102,131,]),'LBRACE':([6,14,30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,84,89,91,93,94,107,108,110,126,133,],[7,20,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,108,52,52,52,52,52,52,52,52,52,]),'INHERITS':([6,],[8,]),'RBRACE':([7,9,10,16,17,20,22,23,29,35,41,45,46,47,48,50,53,54,74,75,76,77,81,82,85,95,96,97,98,99,100,101,103,105,106,107,109,111,120,121,123,127,128,134,],[-2,15,-7,-2,-2,-2,-8,-9,34,-52,-22,-40,-42,-44,-49,-51,-57,-58,-37,-52,-38,-39,-53,106,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-55,-45,-17,-56,129,-18,-20,-41,-19,]),'ID':([7,16,17,19,20,30,33,37,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,79,89,90,91,92,93,94,107,108,110,119,124,126,133,],[13,13,13,25,13,35,25,25,35,35,35,75,75,75,35,35,35,35,75,75,75,75,75,75,75,104,35,25,35,116,35,35,35,35,35,104,116,35,35,]),'SEMI':([11,12,15,24,34,35,36,41,45,46,47,48,50,53,54,74,75,76,77,81,83,85,95,96,97,98,99,100,101,103,105,106,109,111,115,123,127,128,129,134,135,],[16,17,21,-10,58,-52,-11,-22,-40,-42,-44,-49,-51,-57,-58,-37,-52,-38,-39,-53,107,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,124,-18,-20,-41,-12,-19,-29,]),'COLON':([13,25,32,116,],[18,31,56,125,]),'LPAREN':([13,30,35,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,75,89,91,93,94,104,107,108,110,126,133,],[19,49,60,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,60,49,49,49,49,60,49,49,49,49,49,]),'RPAREN':([19,26,27,28,33,35,41,45,46,47,48,50,53,54,55,57,60,74,75,76,77,80,81,85,86,87,88,95,96,97,98,99,100,101,103,105,106,109,110,111,122,123,127,128,134,],[-2,32,-13,-14,-2,-52,-22,-40,-42,-44,-49,-51,-57,-58,-16,-15,-2,-37,-52,-38,-39,105,-53,-21,109,-46,-47,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-2,-17,-48,-18,-20,-41,-19,]),'ASSIGN':([24,35,55,63,],[30,59,-16,91,]),'COMMA':([28,35,41,45,46,47,48,50,53,54,55,62,63,74,75,76,77,81,85,88,95,96,97,98,99,100,101,103,105,106,109,111,113,123,127,128,134,],[33,-52,-22,-40,-42,-44,-49,-51,-57,-58,-16,90,-26,-37,-52,-38,-39,-53,-21,110,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,-25,-18,-20,-41,-19,]),'LET':([30,38,39,40,49,52,59,60,89,91,93,94,107,108,110,126,133,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'CASE':([30,38,39,40,49,52,59,60,89,91,93,94,107,108,110,126,133,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'IF':([30,38,39,40,49,52,59,60,89,91,93,94,107,108,110,126,133,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'WHILE':([30,38,39,40,49,52,59,60,89,91,93,94,107,108,110,126,133,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'BITNOT':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'ISVOID':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'NOT':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'INTEGER':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'NEW':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'BOOL':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'STRING':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,]),'ARROBA':([35,46,47,48,50,53,54,75,81,103,105,106,109,],[-52,78,-44,-49,-51,-57,-58,-52,-53,-43,-50,-54,-45,]),'DOT':([35,46,47,48,50,53,54,75,81,102,103,105,106,109,],[-52,79,-44,-49,-51,-57,-58,-52,-53,119,-43,-50,-54,-45,]),'PLUS':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,95,96,97,98,99,100,101,103,105,106,109,128,],[-52,67,-40,-42,-44,-49,-51,-57,-58,67,-52,67,-39,-53,-30,-31,67,67,-34,-35,-36,-43,-50,-54,-45,-41,]),'MINUS':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,95,96,97,98,99,100,101,103,105,106,109,128,],[-52,68,-40,-42,-44,-49,-51,-57,-58,68,-52,68,-39,-53,-30,-31,68,68,-34,-35,-36,-43,-50,-54,-45,-41,]),'STAR':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,95,96,97,98,99,100,101,103,105,106,109,128,],[-52,69,-40,-42,-44,-49,-51,-57,-58,69,-52,69,-39,-53,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-41,]),'DIVIDE':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,95,96,97,98,99,100,101,103,105,106,109,128,],[-52,70,-40,-42,-44,-49,-51,-57,-58,70,-52,70,-39,-53,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-41,]),'LESS':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,95,96,97,98,99,100,101,103,105,106,109,128,],[-52,71,-40,-42,-44,-49,-51,-57,-58,71,-52,71,-39,-53,71,71,71,71,None,None,None,-43,-50,-54,-45,-41,]),'LESSQ':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,95,96,97,98,99,100,101,103,105,106,109,128,],[-52,72,-40,-42,-44,-49,-51,-57,-58,72,-52,72,-39,-53,72,72,72,72,None,None,None,-43,-50,-54,-45,-41,]),'EQUALS':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,95,96,97,98,99,100,101,103,105,106,109,128,],[-52,73,-40,-42,-44,-49,-51,-57,-58,73,-52,73,-39,-53,73,73,73,73,None,None,None,-43,-50,-54,-45,-41,]),'OF':([35,41,45,46,47,48,50,53,54,64,74,75,76,77,81,85,95,96,97,98,99,100,101,103,105,106,109,111,123,127,128,134,],[-52,-22,-40,-42,-44,-49,-51,-57,-58,92,-37,-52,-38,-39,-53,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,-18,-20,-41,-19,]),'THEN':([35,41,45,46,47,48,50,53,54,65,74,75,76,77,81,85,95,96,97,98,99,100,101,103,105,106,109,111,123,127,128,134,],[-52,-22,-40,-42,-44,-49,-51,-57,-58,93,-37,-52,-38,-39,-53,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,-18,-20,-41,-19,]),'LOOP':([35,41,45,46,47,48,50,53,54,66,74,75,76,77,81,85,95,96,97,98,99,100,101,103,105,106,109,111,123,127,128,134,],[-52,-22,-40,-42,-44,-49,-51,-57,-58,94,-37,-52,-38,-39,-53,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,-18,-20,-41,-19,]),'IN':([35,41,45,46,47,48,50,53,54,55,61,62,63,74,75,76,77,81,85,95,96,97,98,99,100,101,103,105,106,109,111,112,113,123,127,128,134,],[-52,-22,-40,-42,-44,-49,-51,-57,-58,-16,89,-23,-26,-37,-52,-38,-39,-53,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,-24,-25,-18,-20,-41,-19,]),'ELSE':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,85,95,96,97,98,99,100,101,103,105,106,109,111,117,123,127,128,134,],[-52,-22,-40,-42,-44,-49,-51,-57,-58,-37,-52,-38,-39,-53,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,126,-18,-20,-41,-19,]),'POOL':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,85,95,96,97,98,99,100,101,103,105,106,109,111,118,123,127,128,134,],[-52,-22,-40,-42,-44,-49,-51,-57,-58,-37,-52,-38,-39,-53,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,127,-18,-20,-41,-19,]),'FI':([35,41,45,46,47,48,50,53,54,74,75,76,77,81,85,95,96,97,98,99,100,101,103,105,106,109,111,123,127,128,132,134,],[-52,-22,-40,-42,-44,-49,-51,-57,-58,-37,-52,-38,-39,-53,-21,-30,-31,-32,-33,-34,-35,-36,-43,-50,-54,-45,-17,-18,-20,-41,134,-19,]),'ESAC':([114,124,130,],[123,-27,-28,]),'WITH':([131,],[133,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_list':([0,3,],[2,5,]),'def_class':([0,3,],[3,3,]),'feature_list':([7,16,17,20,],[9,22,23,29,]),'empty':([7,16,17,19,20,33,60,110,],[10,10,10,27,10,27,87,87,]),'def_attr':([7,16,17,20,],[11,11,11,11,]),'def_func':([7,16,17,20,],[12,12,12,12,]),'param_list':([19,33,],[26,57,]),'param':([19,33,37,90,],[28,28,63,63,]),'expr':([30,38,39,40,49,52,59,60,89,91,93,94,107,108,110,126,133,],[36,64,65,66,80,83,85,88,111,113,117,118,83,121,88,132,135,]),'arith':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[41,41,41,41,74,76,77,41,41,41,41,95,96,97,98,99,100,101,41,41,41,41,41,41,41,41,41,]),'base_call':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,]),'fact':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'func_call':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,79,89,91,93,94,107,108,110,119,126,133,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,103,47,47,47,47,47,47,47,128,47,47,]),'atom':([30,38,39,40,42,43,44,49,52,59,60,67,68,69,70,71,72,73,89,91,93,94,107,108,110,126,133,],[48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'let_list':([37,90,],[61,112,]),'let_assign':([37,90,],[62,62,]),'block':([52,107,],[82,120,]),'arg_list':([60,110,],[86,122,]),'cases_list':([92,124,],[114,130,]),'case':([92,124,],[115,115,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_list','program',1,'p_program','config.py',10),
  ('empty -> <empty>','empty',0,'p_empty','config.py',15),
  ('class_list -> def_class','class_list',1,'p_class_list','config.py',20),
  ('class_list -> def_class class_list','class_list',2,'p_class_list','config.py',21),
  ('def_class -> CLASS TYPEID LBRACE feature_list RBRACE SEMI','def_class',6,'p_def_class','config.py',29),
  ('def_class -> CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE SEMI','def_class',8,'p_def_class','config.py',30),
  ('feature_list -> empty','feature_list',1,'p_feature_list','config.py',38),
  ('feature_list -> def_attr SEMI feature_list','feature_list',3,'p_feature_list','config.py',39),
  ('feature_list -> def_func SEMI feature_list','feature_list',3,'p_feature_list','config.py',40),
  ('def_attr -> ID COLON TYPEID','def_attr',3,'p_def_attr','config.py',48),
  ('def_attr -> ID COLON TYPEID ASSIGN expr','def_attr',5,'p_def_attr','config.py',49),
  ('def_func -> ID LPAREN param_list RPAREN COLON TYPEID LBRACE expr RBRACE','def_func',9,'p_def_func','config.py',57),
  ('param_list -> empty','param_list',1,'p_param_list','config.py',62),
  ('param_list -> param','param_list',1,'p_param_list','config.py',63),
  ('param_list -> param COMMA param_list','param_list',3,'p_param_list','config.py',64),
  ('param -> ID COLON TYPEID','param',3,'p_param','config.py',75),
  ('expr -> LET let_list IN expr','expr',4,'p_expr','config.py',82),
  ('expr -> CASE expr OF cases_list ESAC','expr',5,'p_expr','config.py',83),
  ('expr -> IF expr THEN expr ELSE expr FI','expr',7,'p_expr','config.py',84),
  ('expr -> WHILE expr LOOP expr POOL','expr',5,'p_expr','config.py',85),
  ('expr -> ID ASSIGN expr','expr',3,'p_expr_assign','config.py',98),
  ('expr -> arith','expr',1,'p_expr_arith','config.py',103),
  ('let_list -> let_assign','let_list',1,'p_let_list','config.py',109),
  ('let_list -> let_assign COMMA let_list','let_list',3,'p_let_list','config.py',110),
  ('let_assign -> param ASSIGN expr','let_assign',3,'p_let_assign','config.py',117),
  ('let_assign -> param','let_assign',1,'p_let_assign','config.py',118),
  ('cases_list -> case SEMI','cases_list',2,'p_cases_list','config.py',127),
  ('cases_list -> case SEMI cases_list','cases_list',3,'p_cases_list','config.py',128),
  ('case -> ID COLON TYPEID WITH expr','case',5,'p_case','config.py',135),
  ('arith -> arith PLUS arith','arith',3,'p_arith_binary','config.py',154),
  ('arith -> arith MINUS arith','arith',3,'p_arith_binary','config.py',155),
  ('arith -> arith STAR arith','arith',3,'p_arith_binary','config.py',156),
  ('arith -> arith DIVIDE arith','arith',3,'p_arith_binary','config.py',157),
  ('arith -> arith LESS arith','arith',3,'p_arith_binary','config.py',158),
  ('arith -> arith LESSQ arith','arith',3,'p_arith_binary','config.py',159),
  ('arith -> arith EQUALS arith','arith',3,'p_arith_binary','config.py',160),
  ('arith -> BITNOT arith','arith',2,'p_arith_unary','config.py',179),
  ('arith -> ISVOID arith','arith',2,'p_arith_unary','config.py',180),
  ('arith -> NOT arith','arith',2,'p_arith_unary','config.py',181),
  ('arith -> base_call','arith',1,'p_arith_basecall','config.py',190),
  ('base_call -> fact ARROBA TYPEID DOT func_call','base_call',5,'p_basecall','config.py',196),
  ('base_call -> fact','base_call',1,'p_basecall','config.py',197),
  ('fact -> fact DOT func_call','fact',3,'p_factcall','config.py',204),
  ('fact -> func_call','fact',1,'p_factcall','config.py',205),
  ('func_call -> ID LPAREN arg_list RPAREN','func_call',4,'p_func_call','config.py',212),
  ('arg_list -> empty','arg_list',1,'p_arglist','config.py',216),
  ('arg_list -> expr','arg_list',1,'p_arglist','config.py',217),
  ('arg_list -> expr COMMA arg_list','arg_list',3,'p_arglist','config.py',218),
  ('fact -> atom','fact',1,'p_factatom','config.py',230),
  ('fact -> LPAREN expr RPAREN','fact',3,'p_fact_group','config.py',234),
  ('atom -> INTEGER','atom',1,'p_atom_int','config.py',238),
  ('atom -> ID','atom',1,'p_atom_id','config.py',242),
  ('atom -> NEW TYPEID','atom',2,'p_atom_new','config.py',246),
  ('atom -> LBRACE block RBRACE','atom',3,'p_atom_block','config.py',250),
  ('block -> expr SEMI','block',2,'p_block','config.py',254),
  ('block -> expr SEMI block','block',3,'p_block','config.py',255),
  ('atom -> BOOL','atom',1,'p_atom_bool','config.py',262),
  ('atom -> STRING','atom',1,'p_atom_string','config.py',266),
]
