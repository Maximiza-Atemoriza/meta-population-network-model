
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CCUR CPAR DIF EQUAL FRAC LBREAK MACRO MINUS NUMBER OCUR OPAR PLUS STAR SYMBOL UNDERsystem : equation_listequation_list : equationequation_list : equation LBREAK equation_listequation : differential EQUAL expressiondifferential : FRAC OCUR DIF identifier CCUR OCUR DIF identifier CCURfraction : FRAC OCUR expression CCUR OCUR expression CCURexpression : arithexpression : MINUS expressionarith : termarith : arith PLUS termarith : arith MINUS termterm : term STAR factorterm : idlistidlist : factor idlistidlist : factorfactor : fractionfactor : NUMBERfactor : OPAR expression CPARfactor : identifieridentifier : atomatom : SYMBOLatom : MACROidentifier : atom UNDER atomidentifier : atom UNDER NUMBERidentifier : atom UNDER OCUR identifier CCUR'
    
_lr_action_items = {'FRAC':([0,6,7,12,14,16,17,18,19,21,22,23,25,26,28,31,37,39,40,46,47,51,],[5,5,20,20,20,-16,-17,20,-19,-20,-21,-22,20,20,20,20,-18,-23,-24,20,-25,-6,]),'$end':([1,2,3,9,10,11,13,14,15,16,17,19,21,22,23,27,29,34,35,36,37,39,40,47,51,],[0,-1,-2,-3,-4,-7,-9,-15,-13,-16,-17,-19,-20,-21,-22,-8,-14,-10,-11,-12,-18,-23,-24,-25,-6,]),'LBREAK':([3,10,11,13,14,15,16,17,19,21,22,23,27,29,34,35,36,37,39,40,47,51,],[6,-4,-7,-9,-15,-13,-16,-17,-19,-20,-21,-22,-8,-14,-10,-11,-12,-18,-23,-24,-25,-6,]),'EQUAL':([4,52,],[7,-5,]),'OCUR':([5,20,32,42,43,],[8,31,41,45,46,]),'MINUS':([7,11,12,13,14,15,16,17,18,19,21,22,23,29,31,34,35,36,37,39,40,46,47,51,],[12,26,12,-9,-15,-13,-16,-17,12,-19,-20,-21,-22,-14,12,-10,-11,-12,-18,-23,-24,12,-25,-6,]),'NUMBER':([7,12,14,16,17,18,19,21,22,23,25,26,28,31,32,37,39,40,46,47,51,],[17,17,17,-16,-17,17,-19,-20,-21,-22,17,17,17,17,40,-18,-23,-24,17,-25,-6,]),'OPAR':([7,12,14,16,17,18,19,21,22,23,25,26,28,31,37,39,40,46,47,51,],[18,18,18,-16,-17,18,-19,-20,-21,-22,18,18,18,18,-18,-23,-24,18,-25,-6,]),'SYMBOL':([7,12,14,16,17,18,19,21,22,23,24,25,26,28,31,32,37,39,40,41,46,47,48,51,],[22,22,22,-16,-17,22,-19,-20,-21,-22,22,22,22,22,22,22,-18,-23,-24,22,22,-25,22,-6,]),'MACRO':([7,12,14,16,17,18,19,21,22,23,24,25,26,28,31,32,37,39,40,41,46,47,48,51,],[23,23,23,-16,-17,23,-19,-20,-21,-22,23,23,23,23,23,23,-18,-23,-24,23,23,-25,23,-6,]),'DIF':([8,45,],[24,48,]),'CPAR':([11,13,14,15,16,17,19,21,22,23,27,29,30,34,35,36,37,39,40,47,51,],[-7,-9,-15,-13,-16,-17,-19,-20,-21,-22,-8,-14,37,-10,-11,-12,-18,-23,-24,-25,-6,]),'CCUR':([11,13,14,15,16,17,19,21,22,23,27,29,33,34,35,36,37,38,39,40,44,47,49,50,51,],[-7,-9,-15,-13,-16,-17,-19,-20,-21,-22,-8,-14,42,-10,-11,-12,-18,43,-23,-24,47,-25,51,52,-6,]),'PLUS':([11,13,14,15,16,17,19,21,22,23,29,34,35,36,37,39,40,47,51,],[25,-9,-15,-13,-16,-17,-19,-20,-21,-22,-14,-10,-11,-12,-18,-23,-24,-25,-6,]),'STAR':([13,14,15,16,17,19,21,22,23,29,34,35,36,37,39,40,47,51,],[28,-15,-13,-16,-17,-19,-20,-21,-22,-14,28,28,-12,-18,-23,-24,-25,-6,]),'UNDER':([21,22,23,],[32,-21,-22,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'system':([0,],[1,]),'equation_list':([0,6,],[2,9,]),'equation':([0,6,],[3,3,]),'differential':([0,6,],[4,4,]),'expression':([7,12,18,31,46,],[10,27,30,38,49,]),'arith':([7,12,18,31,46,],[11,11,11,11,11,]),'term':([7,12,18,25,26,31,46,],[13,13,13,34,35,13,13,]),'factor':([7,12,14,18,25,26,28,31,46,],[14,14,14,14,14,14,36,14,14,]),'idlist':([7,12,14,18,25,26,31,46,],[15,15,29,15,15,15,15,15,]),'fraction':([7,12,14,18,25,26,28,31,46,],[16,16,16,16,16,16,16,16,16,]),'identifier':([7,12,14,18,24,25,26,28,31,41,46,48,],[19,19,19,19,33,19,19,19,19,44,19,50,]),'atom':([7,12,14,18,24,25,26,28,31,32,41,46,48,],[21,21,21,21,21,21,21,21,21,39,21,21,21,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> system","S'",1,None,None,None),
  ('system -> equation_list','system',1,'p_system','parser.py',18),
  ('equation_list -> equation','equation_list',1,'p_equation_list_single','parser.py',23),
  ('equation_list -> equation LBREAK equation_list','equation_list',3,'p_equation_list_multi','parser.py',28),
  ('equation -> differential EQUAL expression','equation',3,'p_equation','parser.py',33),
  ('differential -> FRAC OCUR DIF identifier CCUR OCUR DIF identifier CCUR','differential',9,'p_differential','parser.py',38),
  ('fraction -> FRAC OCUR expression CCUR OCUR expression CCUR','fraction',7,'p_fraction','parser.py',43),
  ('expression -> arith','expression',1,'p_expression','parser.py',48),
  ('expression -> MINUS expression','expression',2,'p_neg_expression','parser.py',53),
  ('arith -> term','arith',1,'p_arith_term','parser.py',58),
  ('arith -> arith PLUS term','arith',3,'p_arith_plus','parser.py',63),
  ('arith -> arith MINUS term','arith',3,'p_arith_minus','parser.py',68),
  ('term -> term STAR factor','term',3,'p_term_star','parser.py',78),
  ('term -> idlist','term',1,'p_term_idlist','parser.py',83),
  ('idlist -> factor idlist','idlist',2,'p_idlist_multi','parser.py',88),
  ('idlist -> factor','idlist',1,'p_idlist_single','parser.py',93),
  ('factor -> fraction','factor',1,'p_factor_fraction','parser.py',98),
  ('factor -> NUMBER','factor',1,'p_factor_num','parser.py',103),
  ('factor -> OPAR expression CPAR','factor',3,'p_factor_pexpression','parser.py',108),
  ('factor -> identifier','factor',1,'p_factor_symbol','parser.py',113),
  ('identifier -> atom','identifier',1,'p_symbol_atom','parser.py',118),
  ('atom -> SYMBOL','atom',1,'p_atom_symbol','parser.py',123),
  ('atom -> MACRO','atom',1,'p_atom_macro','parser.py',128),
  ('identifier -> atom UNDER atom','identifier',3,'p_symbol_comp','parser.py',134),
  ('identifier -> atom UNDER NUMBER','identifier',3,'p_symbol_comp1','parser.py',139),
  ('identifier -> atom UNDER OCUR identifier CCUR','identifier',5,'p_symbol_comp2','parser.py',144),
]
