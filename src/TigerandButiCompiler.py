import ply.lex as lex
import ply.yacc as yacc
import os
import sys
from AST import *

LexerError=False

typesDic={}

typeToTree={}

visited=[]
nodosReferidos=[]
nodosDefinidos={}

class ElementoAtributo():
    def __init__(self,nombre,tipo, columna, linea):
        self.nombre=nombre
        self.tipo=tipo
        self.columna=columna
        self.linea=linea

class ElementoClase():
    def __init__(self,valor,padre,columna, linea,token,atributos={},hijos={}):
        self.valor=valor
        self.hijos=hijos
        self.atributos=atributos
        self.columna=columna
        self.linea=linea
        self.padre=padre
        self.token=token

    def RellenaHijos():
        for nodo in nodosDefinidos.values:
            if not nodo.padre in nodosDefinidos.keys:
                print('('+str(self.linea)+', '+str(self.columna)+') - SemanticError: ERROR at or near "'+ str(self.token)+'"')#Padre no definido
            else:
                nodosDefinidos[nodo.padre].hijos[nodo.valor]=nodo

    def HayCiclos(self):
        if self.valor in visited:
            return True
        else:
            visited.append(self.valor)

        for hijo in self.hijos.values:
            if hijo.HayCiclos():
                return True
        return False

    def HayCiclosBase(self):
        visited=[]
        respuesta=self.HayCiclos()

        for nodo in nodosDefinidos.values:
            if not nodo.valor in visited:
                print('('+str(nodo.linea)+', '+str(nodo.columna)+') - SemanticError: ERROR at or near "'+ str(nodo.token)+'"')


nodosDefinidos["Object"]=ElementoClase("Object",None,0,0,"Object")


#Welcome='Tiger and Buti Compiler 2020 0.2.0\nCopyright (c) 2019: José Gabriel Navarro Comabella, Alberto Helguera Fleitas'

#print(Welcome)

tokens=(
    'class', 'else', 'false', 'if','fi', 'in', 'inherits', 'isvoid', 'let', 'loop', 'pool', 'then', 'while', 'case', 'esac', 'new', 'of', 'true',
    'type', 'constant', 'id','string','number',
    'lparen','rparen','assign','point','plus','minus','mult','div','arroba',
    'implica','less','lesse','equal',
    'intnot','not',
    'lbracket','rbracket','pcoma','coma','dpoint',
    'unfinished_string',
    'comment','eofcomment','eofstring'
    )
reserverd=('not','class', 'else', 'false', 'if','fi', 'in', 'inherits', 'isvoid', 'let', 'loop', 'pool', 'then', 'while', 'case', 'esac', 'new', 'of', 'true')

def find_column(input, token):
    line_start=input.rfind('\n',0,token.lexpos)
    return (token.lexpos-line_start)

def elimina_comentarios2(text):
    acumulado=0
    respuesta=""
    bypass=False
    finlinea=False

    for indice in range(len(text)-1):
        if finlinea:
            if text[indice]=='\n':
                finlinea=False
                respuesta+='\n'
            continue

        if(text[indice]=='-' and text[indice+1]=='-' and acumulado == 0 and not (indice>0 and text[indice-1]=='<')):
            finlinea=True
            respuesta+=' '
            continue

        if bypass:
            bypass=False
            respuesta+=' '
            continue

        if text[indice]=='(' and text[indice+1]=='*':
            acumulado+=1
            bypass=True
            respuesta+=' '
            continue
        
        if  acumulado>0 and text[indice]=='*' and text[indice+1]==')':
            acumulado-=1
            bypass=True
            respuesta+=' '
            continue

        if acumulado==0 or text[indice]=='\n':
            respuesta+=text[indice]
        else:
            respuesta+=' '

    if acumulado>0:
        respuesta+=' ###EOFCOMMENT###'
    elif not bypass:
        respuesta+=text[len(text)-1]
    
    return respuesta


def elimina_comentarios(text):
    count=0
    faltan=0
    respuesta=''
    for i in range(len(text)):
        found=text.find('(*', i, i+2)
        if(-1!=found):
            count+=1
        found=text.find('*)',i, i+2)
        if(-1!=found and count>0):
            count-=1
            if(count==0):
                faltan=2
        if count==0 and faltan==0:
            respuesta+=text[i]
        else:
            faltan-=1
            if text.find('\n',i,i+1)>=0:
                respuesta+='\n'
            else:
                respuesta+=' '
    if count>0:
        
       # for i in range(max(len(text)-text.rfind('\n')-1,0)):
       #     respuesta+=' '
        respuesta+='###EOFCOMMENT###'
    return respuesta


#def t_comment(t):
#    r'\(\*(.|\n)*\*\)'
#    for a in t.value:
#        if a=='\n':
#            t.lexer.lineno+=1
#    pass

def t_eofcomment(t):
    r'\#\#\#EOFCOMMENT\#\#\#'
    line_start=t.lexer.lexdata.rfind('\n',0,t.lexpos)+1
    columna=t.lexpos-line_start+1
    global LexerError
    linea=1
    for i in range(t.lexpos):
        if t.lexer.lexdata[i]=='\n':
            linea+=1
    outstr="({0}, {1}) - LexicographicError: EOF in comment".format(linea, columna)
    print(outstr)#'('+str(t.lexer.lineno)+','+str(columna)+') - LexicographicError: EOF in comment')
    LexerError=True

t_class=r'class'
t_else=r'else'
t_false=r'false'
t_fi=r'fi'
t_if=r'if'
t_in=r'in'
t_inherits=r'inherits'
t_isvoid=r'isvoid'
t_let=r'let'
t_loop=r'loop'
t_pool=r'pool'
t_then=r'then'
t_while=r'while'
t_case=r'case'
t_esac=r'esac'
t_new=r'new'
t_of=r'of'
t_true=r'true'

t_lparen=r'\('
t_rparen=r'\)'
t_assign=r'<-'
t_point=r'\.'
t_plus=r'\+'
t_minus=r'-'
t_mult=r'\*'
t_div=r'/'
t_arroba=r'\@'

t_lbracket=r'{'
t_rbracket=r'}'
t_coma=r','
t_pcoma=r';'
t_dpoint=r'\:'

t_implica=r'\=\>'
t_less=r'\<'
t_lesse=r'\<\='
t_equal=r'\='

t_intnot=r'~'
t_not=r'not'


def t_type(t):
    r'[A-Z][a-zA-Z_0-9]*'
    if t.value.lower() not in reserverd:
        t.type='type'
    else:
        t.type=t.value
        t.value=t.value
    return t

def t_id(t):
    r'[a-z][a-zA-Z_0-9]*'
    if t.value.lower() not in reserverd:
        t.type='id'
    else:
        t.type=t.value
        t.value=t.value
    return t

def t_number(t):
    r'[0-9]+'
    #t.type='constant'
    t.value=int(t.value)
    t.type="Int"
    return t

def t_newline(t):
    r'(\n)+'
    t.lexer.lineno+=len(t.value)

def t_string(t):
    r'"([^"\\\n]|\\\n|\\.)*"'
    #r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
    for a in t.value:
        if a=='\n':
            t.lexer.lineno+=1
    encontrado=t.value.find('\0')
    if encontrado>-1:
        columna=find_column(t.lexer.lexdata,t)
        columna+=encontrado
        linea=1
        for i in range(t.lexpos):
            if t.lexer.lexdata[i]=='\n':
                linea+=1
        outstr="({0}, {1}) - LexicographicError: String contains null character".format(linea, columna)
        global LexerError
        LexerError=True
        print(outstr)#'('+str(t.lexer.lineno)+','+str(columna)+') - LexicographicError: String contains null character')
    t.type='String'
    return t



def t_eofstring(t):
    r'"(\\\s|\\(.)|[^"\n])*$'
    pos=find_column(t.lexer.lexdata,t)
    columna=pos
    todavia=True
    linea=1
    for i in range(t.lexpos):
        if t.lexer.lexdata[i]=='\n':
            linea+=1
    for a in t.value:
        pos+=1
        if a=='\n':
            t.lexer.lineno+=1
            linea+=1
            pos=1
        columna=pos
    
    outstr="({0}, {1}) - LexicographicError: EOF in string constant".format(linea, columna)
    print(outstr)#'('+str(t.lexer.lineno)+','+str(columna)+') - LexicographicError: EOF string constant')
    global LexerError
    LexerError=True
    return t

def t_unfinished_string(t):
    r'\"(\\\s|\\.|[^"\n])*\n'
    pos=find_column(t.lexer.lexdata,t)
    columna=pos
    todavia=True
    linea=t.lexer.lineno
    for a in t.value:
        pos+=1
        if a=='\n':
            t.lexer.lineno+=1
            if todavia:
                columna=pos-1
                todavia=False
    outstr="({0}, {1}) - LexicographicError: Unterminated string constant".format(linea, columna)
    print(outstr)#'('+str(linea)+','+str(columna)+') - LexicographicError: Unterminated string constant')
    global LexerError
    LexerError=True
    return t

def t_ignored(t):
    r'(\s|\f|\t|\v)'
    pass

def t_error(t):
    columna=find_column(t.lexer.lexdata, t)
    token=t.value[0]
  #  if token=='\"':f
  #      print('('+str(t.lexer.lineno)+','+str(columna)+') - LexicographicError: EOF in string constant')
  #  else:
    linea=1
    for i in range(t.lexpos):
        if t.lexer.lexdata[i]=='\n':
            linea+=1
    outstr="({0}, {1}) - LexicographicError: ERROR \"{2}\"".format(linea, columna,str(token))
    print(outstr)#'('+str(t.lexer.lineno)+','+str(columna)+') - LexicographicError: ERROR "'+ token+'"')
    global LexerError
    LexerError=True
    t.lexer.skip(1)

#Me falta agregar conteo de lineas

mylex=lex.lex(debug=False)
#mylex.input(r'class P { f(): Int { 1 + 2 }; };')
#for t in mylex:
#    print('el token =>'+str(t))

def p_program(p):
    '''program : classdec program
               | classdec'''
    if len(p) == 3:
        p[2].insert(0,p[1])
        p[0] = ProgramNode(classes = p[2])
    else:
        p[0] = ProgramNode(classes = [p[2]])
    pass

def p_empty(p):
    'empty :'
    pass

def p_classdec(p):
    '''classdec : class type lbracket featurelist rbracket pcoma
                | class type inherits type lbracket featurelist rbracket pcoma'''
    if len(p)== 7:
        p[0] = ClassNode(name = p[2], parent = "Object", features = p[4])
    else:
        p[0] = ClassNode(name = p[2], parent = p[4], features = p[6])
    
    if len(p)== 7:
        padre="Object"
    else:
        padre=p[4].value

    linea=0
    columna=0
    for i in range(p.lexpos):
            if p.lexer.lexdata[i]=='\n':
                linea+=1
                columna=find_column(p.lexer.lexdata, p)

    Nodo=ElementoClase(p[2].value,padre,columna)
    if not Nodo.valor in nodosDefinidos.keys:
        nodosDefinidos[Nodo.valor]=Nodo
    else:
        print('('+str(linea)+', '+str(columna)+') - SemanticError: ERROR at or near "'+ str(token)+'"')
    pass

def p_featurelist(p):
    '''featurelist : feature featurelist
                   | empty'''
    if len(p) == 3:
        p[2].insert(0,p[2])
        p[0] = p[2]
    else:
        p[0] = []
    pass

def p_feature(p):
    '''feature : attribute pcoma
               | methoddef pcoma'''
    p[0] = p[1]
    pass

def p_expression(p):
    '''expression : constantexp
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
                  | parenexpression'''
    p[0] = p[1]
    pass

def p_methoddef(p):
    '''methoddef : id lparen rparen dpoint type lbracket expression rbracket
                 | id lparen param paramslistdef rparen dpoint type lbracket expression rbracket'''
    if len(p) == 9:
        p[0] = MethodNode(name = p[1], parameters = [], return_type = p[5], body = p[7])
    else:
        p[4].insert( 0, p[3])
        p[0] = MethodNode(name = p[1], parameters = p[4], return_type = p[7], body = p[9])
    pass

def p_expressionlist(p):
    '''expressionlist : expression pcoma expressionlist
                      | empty'''
    if len(p)==4:
        if p[3]=='':
            p[0].type=p[1].type
        else:
            p[0].type=p[3].type
    if len(p)==4:
        p[3].insert(0,p[1])
        p[0] = p[3]
    else:
        p[0] = []
    pass

def p_param(p):
    '''param : id dpoint type'''
    p[0] = ParameterNode(name = p[1], param_type = p[3])
    pass

def p_attribute(p):
    '''attribute : id dpoint type
                 | id dpoint type assign expression'''
    if len(p)==4:
        p[0] = AttributeNode(name = p[1], attr_type = p[3], value = None)
    else:
        p[0] = AttributeNode(name = p[1], attr_type = p[3], value = p[5])
    pass

def p_letattributelist(p):
    '''letattributelist : coma attribute letattributelist
                        | empty'''
    if len(p)==4:
        p[3].insert(0,p[2])
        p[0] = p[3]
    else:
        p[0] = []
    pass

def p_paramslistdef(p):
    '''paramslistdef : coma param paramslistdef
                     | empty'''
    if len(p)==4:
        p[3].insert(0,p[2])
        p[0] = p[3]
    else:
        p[0] = []
    pass

def p_dispatch(p):
    '''dispatch : id lparen rparen
                | id lparen expression expressionparams rparen
                | expression point id lparen rparen
                | expression point id lparen expression expressionparams rparen
                | expression arroba type point id lparen rparen
                | expression arroba type point id lparen expression expressionparams rparen'''
    if p[3] == ')':
        p[0] = DispatchNode(func_id = p[1], parameters = [], left_expr = None)
    elif p[2] == '(':
        p[4].insert(0,p[3])
        p[0] = DispatchNode(func_id = p[1], parameters = p[4], left_expr = p[4], left_type=p[4].type)
    elif p[5] == ')':
        p[0] = DispatchNode(func_id = p[4], parameters = [], left_expr = p[1], p[1].type)
    elif p[2] == '.':
        p[6].insert(0,p[5])
        p[0] = DispatchNode(func_id = p[3], parameters = p[6], left_expr = p[1], p[1].type)
    elif len(p) == 7:
        p[0] = StaticDispatchNode(func_id = p[5], parent_id = p[3] ,parameters = [], left_expr = p[1])
    else:
        p[8].insert(0,p[7])
        p[0] = StaticDispatchNode(func_id = p[5], parent_id = p[3] ,parameters = p[8], left_expr = p[1])

    pass

precedence=(
    #('left','expression'),
    ('nonassoc','assign'),
    ('nonassoc','less','lesse','equal'),
    ('left','plus','minus'),
    ('left','mult','div'),
    ('right','intnot','not'),
    )

def p_expressionparams(p):
    '''expressionparams : coma expression expressionparams
                        | empty'''
    if len(p)==4:
        p[3].insert(0,p[2])
        p[0] = p[3]
    else:
        p[0] = []
    pass

def p_conditional(p):
    '''conditional : if expression then expression else expression fi'''
    p[0] = ConditionalNode(predicate = p[2], then_body = p[4], else_body = p[6])
    if p[2].type!="Bool":
        linea=1
        
        for i in range(p.lexpos):
            if p.lexer.lexdata[i]=='\n':
                linea+=1
                columna=find_column(p.lexer.lexdata, p)
        
        token=p.value
        print('('+str(linea)+', '+str(columna)+') - SemanticError: ERROR at or near "'+ str(token)+'"')

    p[0].type="Object"
    pass

def p_loopexp(p):
    '''loopexp : while expression loop expression pool'''
    p[0] = LoopNode(predicate = p[2], body = p[4])
    if p[2].type!="Bool":
        linea=1
        
        for i in range(p.lexpos):
            if p.lexer.lexdata[i]=='\n':
                linea+=1
                columna=find_column(p.lexer.lexdata, p)
        
        token=p.value
        print('('+str(linea)+', '+str(columna)+') - SemanticError: ERROR at or near "'+ str(token)+'"')

    p[0].type="Object"
    pass

def p_blockexp(p):
    '''blockexp : lbracket expressionlist rbracket'''#'''blockexp : lbracket expression pcoma expressionlist rbracket'''
    p[0] = BlockNode(expressions = p[2])
    p[0].type=p[2].type
    pass

def p_letexp(p):
    '''letexp : let attribute letattributelist in expression'''
    p[3].insert(0,p[2])
    p[0] = LetNode(declarations = p[3], in_body = p[5])
    pass

def p_caseexp(p):
    '''caseexp : case expression of subcase listcase esac'''
    p[5].insert(0,p[4]) 
    p[0] = CaseNode(expression = p[2], subcases = p[5])
    pass

def p_listcase(p):
    '''listcase : subcase listcase
                | empty'''
    if len(p)==3:
        p[2].insert(0,p[1])
        p[0] = p[2]
    else:
        p[0] = []
    pass
    pass

def p_subcase(p):
    '''subcase : id dpoint type implica expression pcoma'''
    p[0] = SubCaseNode(name = p[1], sub_type = p[3], expression = p[5])
    pass

def p_newexp(p):
    '''newexp : new type'''
    p[0] = NewNode(new_type = p[2])
    pass

def p_isvoidexp(p):
    '''isvoidexp : isvoid expression'''
    p[0].type="Bool"
    pass

def p_aritmetica(p):
    '''aritmetica : expression plus expression
                  | expression minus expression
                  | expression mult expression
                  | expression div expression
                  | intnot expression'''
    if p[2] == '+':
        p[0] = PlusNode(left = p[1], right = p[3])
    elif p[2] == '-':
        p[0] = MinusNode(left = p[1], right = p[3])
    elif p[2] == '*':
        p[0] = MultNode(left = p[1], right = p[3])
    elif p[2] == '/':
        p[0] = DivNode(left = p[1], right = p[3])
    else:
        p[0] = IntComplementNode(value = p[2])
    
    if((p[1]=="~" and p[2].type!="Int") or (p[1].type!="Int" or p[3].type!="Int")):
        linea=1
        
        for i in range(p.lexpos):
            if p.lexer.lexdata[i]=='\n':
                linea+=1
                columna=find_column(p.lexer.lexdata, p)
        
        token=p.value
        print('('+str(linea)+', '+str(columna)+') - SemanticError: ERROR at or near "'+ str(token)+'"')

    p[0].type="Int"
    pass

def p_comparison(p):
    '''comparison : expression less expression
                  | expression lesse expression
                  | expression equal expression
                  | not expression'''
    if p[2] == '<':
        p[0] = LesserNode(left = p[1], right = p[3])
    elif p[2] == '<=':
        p[0] = LesserEqualThanNode(left = p[1], right = p[3])
    elif p[2] == '=':
        p[0] = EqualNode(left = p[1], right = p[3])
    else:
        p[0] = BoolComplementNode(value = p[2])

    if p[2].value=="equal" and p[1].type=="String":
        p[0].isString=True

    if((p[1].value=="not" and p[2].type!="Bool") or (p[1].type!="Int" or p[3].type!="Int") or (p[2].value=="equal" and p[1].type!=p[3].type)):
        linea=1
        
        for i in range(p.lexpos):
            if p.lexer.lexdata[i]=='\n':
                linea+=1
                columna=find_column(p.lexer.lexdata, p)
        
        token=p.value
        print('('+str(linea)+', '+str(columna)+') - SemanticError: ERROR at or near "'+ str(token)+'"')

    p[0].type="Bool"
    pass

    pass

def p_parenexpression(p):
    '''parenexpression : lparen expression rparen'''
    p[0] = p[2]
    p[0].type=p[2].type
    pass

def p_constantexp(p):
    '''constantexp : number
                | string
                | true
                | false'''
    if p[1].type == "Int":
        p[0] = IntegerNode(value = p[1])
    elif p[1].type == "String":
        p[0] = StringNode(value = p[1])
    else:
        p[1].type = "Bool"
        p[0] = BoolNode(value = p[1])
    p[0].type=p[1].type
    pass

def p_identifier(p):
    '''identifier : id'''
    p[0] = VariableNode(var_id = p[1])
    pass

def p_assignment(p):
    '''assignment : id assign expression'''
    p[0] = AssignNode(variable = p[1], expr = p[3])
    p[0].id=p[1].value
    p[0].type=p[3].type
    pass

def p_error(p):
    if p==None:
        print("(0, 0) - SyntacticError: 'ERROR at or near EOF'")
        return
    linea=1
    for i in range(p.lexpos):
        if p.lexer.lexdata[i]=='\n':
            linea+=1
    columna=find_column(p.lexer.lexdata, p)
    token=p.value
    print('('+str(linea)+', '+str(columna)+') - SyntacticError: ERROR at or near "'+ str(token)+'"')
    return

archivo=open(sys.argv[1],encoding='utf-8')
texto=archivo.read()
respuesta=elimina_comentarios2(texto)
# respuesta=elimina_comentarios_fin_de_linea(respuesta)

LexerError=False
mylex.input(respuesta)
for t in mylex:
    pass

parser=yacc.yacc()
if not LexerError:
    parser.parse(respuesta,lexer=mylex, debug=False)
exit(1)

    
if False:
    tests = [(file) for file in os.listdir('tests\\parser') if file.endswith('.cl')]
    errors=[(file) for file in os.listdir('tests\\parser') if file.endswith('_error.txt')]
    for i in range(len(tests)):
        LexerError=False
        mylex.lineno=0
        te=tests[i]
        print(te)
        archivo=open("tests\\parser\\"+te,encoding='utf-8')
        texto=archivo.read()
        respuesta=elimina_comentarios(texto)
        respuesta=elimina_comentarios_fin_de_linea(respuesta)
        mylex.input(respuesta)
        for t in mylex:
            pass
        if not LexerError:
            print("parseo")
            parser.parse(respuesta,lexer=mylex, debug=False)
        else:
            LexerError=False
        er=errors[i]
        print(er)
        archivoerror=open("tests\\parser\\"+er,encoding='utf-8')
        print(archivoerror.read())

#archivo=open("tests\\parser\\program1.cl",encoding='utf-8')
#texto=archivo.read()
#respuesta=elimina_comentarios(texto)
#respuesta=elimina_comentarios_fin_de_linea(respuesta)
#parser.parse(respuesta,lexer=mylex, debug=True)
#print(parser.parse(r'clas%s P { f(): Int { variab <- 2 ;}; };', debug=True))

#return 1
