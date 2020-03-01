import ply.lex as lex
import ply.yacc as yacc
import os
import sys

LexerError=False

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
    if count>0:
        
        for i in range(max(len(text)-text.rfind('\n')-1,0)):
            respuesta+=' '
        respuesta+='###EOFCOMMENT###'
    return respuesta


def elimina_comentarios_fin_de_linea(text):
    lista=[]
    result=0
    encontrado=False
    respuesta=''
    while result>=0:
        lista.append(result)
        if encontrado:
            result=text.find('\n',result)
            encontrado=False
        else:
            result=text.find('--',result)
            encontrado=True
    for i in range(1,len(lista),2):
        respuesta+=text[lista[i-1]:lista[i]]
    if len(lista)%2!=0:
        respuesta+=text[lista[len(lista)-1]:]
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
        t.type=t.value.lower()
        t.value=t.value.lower()
    return t

def t_id(t):
    r'[a-z][a-zA-Z_0-9]*'
    if t.value.lower() not in reserverd:
        t.type='id'
    else:
        t.type=t.value.lower()
        t.value=t.value.lower()
    return t

def t_number(t):
    r'[0-9]+'
    #t.type='constant'
    t.value=int(t.value)
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
        print(outstr)#'('+str(t.lexer.lineno)+','+str(columna)+') - LexicographicError: String contains null character')
    t.type='string'
    global LexerError
    LexerError=True
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
    outstr="({0}, {1}) - LexicographicError: Unterminated string constant".format(linea+1, columna)
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
    pass

def p_empty(p):
    'empty :'
    pass

def p_classdec(p):
    '''classdec : class type lbracket featurelist rbracket pcoma
                | class type inherits type lbracket featurelist rbracket pcoma'''
    pass

def p_featurelist(p):
    '''featurelist : feature featurelist
                   | empty'''
    pass

def p_feature(p):
    '''feature : attribute pcoma
               | methoddef pcoma'''
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
    pass

def p_methoddef(p):
    '''methoddef : id lparen rparen dpoint type lbracket expression rbracket
                 | id lparen param paramslistdef rparen dpoint type lbracket expression rbracket'''
    pass

def p_expressionlist(p):
    '''expressionlist : expression pcoma expressionlist
                      | empty'''
    pass

def p_param(p):
    '''param : id dpoint type'''
    pass

def p_attribute(p):
    '''attribute : id dpoint type
                 | id dpoint type assign expression'''
    pass

def p_letattributelist(p):
    '''letattributelist : coma attribute letattributelist
                        | empty'''

def p_paramslistdef(p):
    '''paramslistdef : coma param paramslistdef
                     | empty'''
    pass

def p_dispatch(p):
    '''dispatch : id lparen rparen
                | id lparen expression expressionparams rparen
                | expression point id lparen rparen
                | expression point id lparen expression expressionparams rparen
                | expression arroba type point id lparen rparen
                | expression arroba type point id lparen expression expressionparams rparen'''
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
    pass

def p_conditional(p):
    '''conditional : if expression then expression else expression fi'''
    pass

def p_loopexp(p):
    '''loopexp : while expression loop expression pool'''
    pass

def p_blockexp(p):
    '''blockexp : lbracket expressionlist rbracket'''#'''blockexp : lbracket expression pcoma expressionlist rbracket'''
    pass

def p_letexp(p):
    '''letexp : let attribute letattributelist in expression'''
    pass

def p_caseexp(p):
    '''caseexp : case expression of subcase listcase esac'''
    pass

def p_listcase(p):
    '''listcase : subcase listcase
                | empty'''
    pass

def p_subcase(p):
    '''subcase : id dpoint type implica expression pcoma'''
    pass

def p_newexp(p):
    '''newexp : new type'''
    pass

def p_isvoidexp(p):
    '''isvoidexp : isvoid expression'''
    pass

def p_aritmetica(p):
    '''aritmetica : expression plus expression
                  | expression minus expression
                  | expression mult expression
                  | expression div expression
                  | intnot expression'''
    pass

def p_comparison(p):
    '''comparison : expression less expression
                  | expression lesse expression
                  | expression equal expression
                  | not expression'''
    pass

def p_parenexpression(p):
    '''parenexpression : lparen expression rparen'''
    pass

def p_constantexp(p):
    '''constantexp : number
                | string
                | true
                | false'''
    pass

def p_identifier(p):
    '''identifier : id'''
    pass

def p_assignment(p):
    '''assignment : id assign expression'''
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
respuesta=elimina_comentarios(texto)
respuesta=elimina_comentarios_fin_de_linea(respuesta)

mylex.input(respuesta)
for t in mylex:
    pass

parser=yacc.yacc()
if not LexerError:
    parser.parse(respuesta,lexer=mylex, debug=False)
return 1

    
if False:
    tests = [(file) for file in os.listdir('tests\\lexer') if file.endswith('.cl')]
    errors=[(file) for file in os.listdir('tests\\lexer') if file.endswith('_error.txt')]
    for i in range(len(tests)):
        mylex.lineno=0
        te=tests[i]
        print(te)
        archivo=open("tests\\lexer\\"+te,encoding='utf-8')
        texto=archivo.read()
        respuesta=elimina_comentarios(texto)
        respuesta=elimina_comentarios_fin_de_linea(respuesta)
        mylex.input(respuesta)
        for t in mylex:
            pass
        if not LexerError:
            parser.parse(respuesta,lexer=mylex, debug=False)
        else:
            LexerError=False
        er=errors[i]
        print(er)
        archivoerror=open("tests\\lexer\\"+er,encoding='utf-8')
        print(archivoerror.read())

#archivo=open("tests\\parser\\program1.cl",encoding='utf-8')
#texto=archivo.read()
#respuesta=elimina_comentarios(texto)
#respuesta=elimina_comentarios_fin_de_linea(respuesta)
#parser.parse(respuesta,lexer=mylex, debug=True)
#print(parser.parse(r'clas%s P { f(): Int { variab <- 2 ;}; };', debug=True))

#return 1
