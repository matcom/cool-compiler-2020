import ply.lex as lex
import ply.yacc as yacc
import os
import sys
from AST import *
from Semantic_Checking import *
from ASTtoCIL import *
from CILtoMIPS import *

LexerError=False
DispatchList = []
#Welcome='Tiger and Buti Compiler 2020 0.2.0\nCopyright (c) 2019: Jose Gabriel Navarro Comabella, Alberto Helguera Fleitas'

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
def find_column2(input, token):
    line_start=input.rfind('\n',0,token.lexpos(1))
    return (token.lexpos(1)-line_start)

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

def t_true(t):
    r'true'
    t.lexer.ty="Bool"
    return t

def t_false(t):
    r'false'
    t.lexer.ty="Bool"
    return t

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
    t.lexer.ty = "Int"
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
    t.lexer.ty = "String"
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

def posicion(p):
    linea=1
    for i in range(p.lexpos(1)):
        if p.lexer.lexdata[i]=='\n':
            linea+=1
    columna=find_column2(p.lexer.lexdata, p)
    return (linea,columna)


def p_program(p):
    '''program : classdec program
               | classdec'''
    if len(p) == 3:
        p[2].classes.insert(0,p[1])
        p[0] = ProgramNode(classes = p[2].classes)
    else:
        p[0] = ProgramNode(classes = [p[1]])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
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
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_featurelist(p):
    '''featurelist : feature featurelist
                   | empty'''
    if len(p) == 3:
        p[2].insert(0,p[1])
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
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_expressionlist(p):
    '''expressionlist : expression pcoma expressionlist
                      | empty'''
    if len(p)==4:
        p[3].insert(0,p[1])
        p[0] = p[3]
    else:
        p[0] = []
    pass

def p_param(p):
    '''param : id dpoint type'''
    p[0] = ParameterNode(name = p[1], param_type = p[3])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_attribute(p):
    '''attribute : id dpoint type
                 | id dpoint type assign expression'''
    if len(p)==4:
        p[0] = AttributeNode(name = p[1], attr_type = p[3], value = None)
    else:
        p[0] = AttributeNode(name = p[1], attr_type = p[3], value = p[5])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
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
        DispatchList.append(p[1])
    elif p[2] == '(':
        p[4].insert(0,p[3])
        p[0] = DispatchNode(func_id = p[1], parameters = p[4], left_expr = None)
        DispatchList.append(p[1])
    elif p[5] == ')':
        p[0] = DispatchNode(func_id = p[3], parameters = [], left_expr = p[1])
        DispatchList.append(p[3])
    elif p[2] == '.':
        p[6].insert(0,p[5])
        p[0] = DispatchNode(func_id = p[3], parameters = p[6], left_expr = p[1])
        DispatchList.append(p[3])
    elif p[7] == ")":
        p[0] = StaticDispatchNode(func_id = p[5], parent_id = p[3] ,parameters = [], left_expr = p[1])
        DispatchList.append(p[5])
    else:
        p[8].insert(0,p[7])
        p[0] = StaticDispatchNode(func_id = p[5], parent_id = p[3] ,parameters = p[8], left_expr = p[1])
        DispatchList.append(p[5])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

precedence=(
    #('left','expression'),
    ('nonassoc','assign'),
    ('right','not'),
    ('nonassoc','less','lesse','equal'),
    ('left','plus','minus'),
    ('left','mult','div'),
    ('right','isvoid'),
    ('right','intnot'),
    ('left','arroba'),
    ('left','point'),
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
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_loopexp(p):
    '''loopexp : while expression loop expression pool'''
    p[0] = LoopNode(predicate = p[2], body = p[4])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_blockexp(p):
    '''blockexp : lbracket expressionlist rbracket'''#'''blockexp : lbracket expression pcoma expressionlist rbracket'''
    p[0] = BlockNode(expressions = p[2])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_letexp(p):
    '''letexp : let attribute letattributelist in expression'''
    p[3].insert(0,p[2])
    p[0] = LetNode(declarations = p[3], in_body = p[5])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_caseexp(p):
    '''caseexp : case expression of subcase listcase esac'''
    p[5].insert(0,p[4]) 
    p[0] = CaseNode(expression = p[2], subcases = p[5])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
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
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_newexp(p):
    '''newexp : new type'''
    p[0] = NewNode(new_type = p[2])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_isvoidexp(p):
    '''isvoidexp : isvoid expression'''
    p[0] = IsVoidNode(expr = p[2])
    pass

def p_aritmetica(p):
    '''aritmetica : expression plus expression
                  | expression minus expression
                  | expression mult expression
                  | expression div expression
                  | intnot expression'''
    if p[2] == '+':
        if isinstance(p[1],IntegerNode) and isinstance(p[3],IntegerNode):
            v1 = int(p[1].value)
            v2 = int(p[3].value)
            res = v1 + v2
            p[0] = IntegerNode(value = str(res))
        else:
            p[0] = PlusNode(left = p[1], right = p[3])
            p[0].operator = p[2]
    elif p[2] == '-':
        if isinstance(p[1],IntegerNode) and isinstance(p[3],IntegerNode):
            v1 = int(p[1].value)
            v2 = int(p[3].value)
            res = v1 - v2
            p[0] = IntegerNode(value = str(res))
        else:
            p[0] = MinusNode(left = p[1], right = p[3])
            p[0].operator = p[2]
    elif p[2] == '*':
        if isinstance(p[1],IntegerNode) and isinstance(p[3],IntegerNode):
            v1 = int(p[1].value)
            v2 = int(p[3].value)
            res = v1 * v2
            p[0] = IntegerNode(value = str(res))
        else:
            p[0] = MultNode(left = p[1], right = p[3])
            p[0].operator = p[2]
    elif p[2] == '/':
        if isinstance(p[1],IntegerNode) and isinstance(p[3],IntegerNode):
            v1 = int(p[1].value)
            v2 = int(p[3].value)
            res = v1 // v2
            p[0] = IntegerNode(value = str(res))
        else:
            p[0] = DivNode(left = p[1], right = p[3])
            p[0].operator = p[2]
    else:
        if isinstance(p[1],IntegerNode):
            v1 = int(p[1].value)
            res = -1*v1
            p[0] = IntegerNode(value = str(res))
        else:
            p[0] = IntComplementNode(right = p[2])
            p[0].operator = p[1]
    
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_comparison(p):
    '''comparison : expression less expression
                  | expression lesse expression
                  | expression equal expression
                  | not expression'''
    if p[2] == '<':
        if isinstance(p[1],IntegerNode) and isinstance(p[3],IntegerNode):
            v1 = int(p[1].value)
            v2 = int(p[3].value)
            res = v1 < v2
            p[0] = BoolNode(value = lower(str(res)))
        else:
            p[0] = LesserNode(left = p[1], right = p[3])
            p[0].operator = p[2]
    elif p[2] == '<=':
        if isinstance(p[1],IntegerNode) and isinstance(p[3],IntegerNode):
            v1 = int(p[1].value)
            v2 = int(p[3].value)
            res = v1 <= v2
            p[0] = BoolNode(value = lower(str(res)))
        else:
            p[0] = LesserEqualNode(left = p[1], right = p[3])
            p[0].operator = p[2]
    elif p[2] == '=':
        if isinstance(p[1],IntegerNode) and isinstance(p[3],IntegerNode):
            v1 = int(p[1].value)
            v2 = int(p[3].value)
            res = v1 == v2
            p[0] = BoolNode(value = lower(str(res)))
        else:
            p[0] = EqualNode(left = p[1], right = p[3])
            p[0].operator = p[2]
    else:
        p[0] = BoolComplementNode(right = p[2])
        p[0].operator = p[1]

    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

    pass

def p_parenexpression(p):
    '''parenexpression : lparen expression rparen'''
    p[0] = p[2]
    # p[0].type=p[2].type Esto lo comente, tiro error
    pass

def p_constantexp(p):
    '''constantexp : number
                | string
                | true
                | false'''
    if p.lexer.ty == "Int":
        p[0] = IntegerNode(value = p[1])
    elif p.lexer.ty == "String":
        p[0] = StringNode(value = p[1])
    elif p.lexer.ty == "Bool":
        p[0] = BoolNode(value = p[1])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_identifier(p):
    '''identifier : id'''
    p[0] = VariableNode(var_id = p[1])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
    pass

def p_assignment(p):
    '''assignment : id assign expression'''
    p[0] = AssignNode(variable = p[1], expr = p[3])
    (linea,columna) = posicion(p)
    p[0].index = columna
    p[0].line = linea
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

if __name__=='__main__':
    nombrearchivo=sys.argv[1]
    # nombrearchivo="c/hola/f.txt"
    # archivoescritura=nombrearchivo[:-3]
    # archivoescritura=archivoescritura[archivoescritura.rfind('/'):]
    archivo=open(nombrearchivo,encoding='utf-8')
    texto=archivo.read()
    respuesta=elimina_comentarios2(texto)
# respuesta=elimina_comentarios_fin_de_linea(respuesta)
    LexerError=False
    mylex.input(respuesta)
    for t in mylex:
        pass
    
    parser=yacc.yacc()
    if not LexerError:
        ast=parser.parse(respuesta,lexer=mylex, tracking=True,debug=False)
    else:
        exit(1)
    if parser.errorok:
        semantic=Semantics_Checker()
        semanticvalid=semantic.visit(ast,None)
        if semanticvalid:
            tocil=CILTranspiler()
            codigoCIL=tocil.visit(ast, None)
                
            toMIPS=MIPSCompiler()
            instrucciones=toMIPS.visit(codigoCIL, None)
            with open(f'{sys.argv[1][:-3]}.mips', 'w') as f:
                f.write(instrucciones)
        else:
            exit(1)
    else:
        exit(1)
    # else:
    #     exit(1)
    
        # else:
        #     exit(1)
# else:
#     exit(1)

    
if False:
    tests = [(file) for file in os.listdir('tests\\codegen') if file.endswith('.cl')]
    errors=[(file) for file in os.listdir('tests\\codegen') if file.endswith('_error.txt')]
    for i in range(len(tests)):
        LexerError=False
        mylex.lineno=0
        te=tests[i]
        print(te)
        # if(te=="atoi.cl"):
        #     print("here")
        # else:
        #     continue
        archivo=open("tests\\codegen\\"+te,encoding='utf-8')
        texto=archivo.read()
        respuesta=elimina_comentarios2(texto)
        # respuesta=elimina_comentarios_fin_de_linea(respuesta)
        mylex.input(respuesta)
        for t in mylex:
            pass
        if not LexerError:
            parser=yacc.yacc()
            ast = parser.parse(respuesta,lexer=mylex, tracking=True, debug = False)
            # for classc in ast.classes:
            #     for foo in classc.methods:
            #         print(classc.name+'--'+foo.name)
            semantic = Semantics_Checker()
            semantic.visit(ast,None)
            tocil=CILTranspiler()
            programaCIL=tocil.visit(ast,None)
            tipos=[]
            for tipo in programaCIL.Types:
                tipos.append(tipo)
                # print("este")
            metodos=[]
            for met in programaCIL.Methods:
                metodos.append(met)
                # print("este")
            #for metodo in programaCIL.Methods:
            #    for instruccion in metodo.intrucciones:
            #        instruccion.instructionPrint()
            toMIPS=MIPSCompiler()
            resultado=toMIPS.visit(programaCIL, None)
            file=open("tests\\codegen\\"+te+".asm",mode="w")
            file.write(resultado)
            file.flush()
            file.close()


        else:
            LexerError=False
        # er=errors[i]
        # print(er)
        # archivoerror=open("tests\\semantic\\"+er,encoding='utf-8')
        # print(archivoerror.read())

#archivo=open("tests\\parser\\program1.cl",encoding='utf-8')
#texto=archivo.read()
#respuesta=elimina_comentarios(texto)
#respuesta=elimina_comentarios_fin_de_linea(respuesta)
#parser.parse(respuesta,lexer=mylex, debug=True)
#print(parser.parse(r'clas%s P { f(): Int { variab <- 2 ;}; };', debug=True))

#return 1
