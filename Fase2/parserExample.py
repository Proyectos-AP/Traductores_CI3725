import sys
import os
from Arbol import *

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

def LeerArchivoEntrada(): 
  '''
    Descripción de la función: Lee el archivo de entrada.

    * Variables de entrada: Ninguna
    * Variables de salida: data// Almacena toda la informacion que se 
                                  encuentra en el archivo de entrada.

  '''

  # Verificación de la correctitud de los argumentos dados.
  try:
  # Se verifica que se introduzcan los argumentos necesarios.
    assert(len(sys.argv) == 2)
    NombreArchivoEntrada = sys.argv[1]
    # Se verifica que el archivo de entrada esté en el directorio
    # correspondiente.
    assert(os.path.isfile(NombreArchivoEntrada))
  except:
    print("Error: Los argumentos dados no son validos")
    print("El programa se cerrará.")
    sys.exit()
  # Lectura del archivo de entrada.
  with open(NombreArchivoEntrada,'r') as Archivo:
    data = Archivo.read()
    Archivo.close

  return data

#------------------------------------------------------------------------------#

# def imprimirAST(Raiz):

#     if (Raiz.arbolInstruccion!=None):
#         aux =Raiz.arbolInstruccion.Instrucciones
#         print("SECUENCIACION")
#         while (aux != None ):
#             if (aux.type in {"ACTIVATE","DEACTIVATE","ADVANCE"}):
#                 aux.imprimirInstruccionesSimples()
#             else:
#                 if(aux.type == "ITERACION INDETERMINADA"):
#                     aux.imprimirWhile()
#                 elif(aux.type == "CONDICIONAL"):
#                     aux.imprimirCondiional()
#             aux=aux.sig

#------------------------------------------------------------------------------#

reserved = {
    'create'           : 'TkCreate',
    'bot'              : 'TkBot' ,
    'on'               : 'TkOn',
    'activation'       : 'TkActivation' ,
    'deactivation'     : 'TkDeActivation',
    'store'            : 'TkStore' ,
    'end'              : 'TkEnd'  ,
    'execute'          : 'TkExecute' ,
    'activate'         : 'TkActivate',
    'deactivate'       : 'TkDeactivate' ,
    'send'             : 'TkSend' ,   
    'advance'          : 'TkAdvance' ,
    'recieve'          : 'TkRecieve',
    'default'          : 'TkDefault' ,
    'me'               : 'TkMe' ,
    'drop'             : 'TkDrop',
    'collect'          : 'TkCollect',
    'as'               : 'TkAs',
    'int'              : 'TkInt',
    'left'             : 'TkLeft',
    'right'            : 'TkRight',
    'up'               : 'TkUp' ,
    'down'             : 'TkDown' ,
    'read'             : 'TkRead',
    'while'            : 'TkWhile' ,
    'bool'             : 'TkBool',
    'if'               : 'TkIf',
    'else'             : 'TkElse'  ,
    'true'             : 'TkTrue'  ,
    'false'            : 'TkFalse',
    'char'             : 'TkChar'
}

tokens = [
    'TkComa',
    'TkPunto',
    'TkDosPuntos',
    'TkParAbre',
    'TkParCierra',
    'TkSuma',
    'TkResta',
    'TkMult',
    'TkDiv',
    'TkMod',
    'TkConjuncion',
    'TkDisyuncion',
    'TkNegacion',
    'TkMenor',
    'TkMayor',
    'TkMenorIgual',
    'TkMayorIgual',
    'TkIgual',
    'TkDesigual',
    'TkIdent',
    'TkNum',
    'TkCaracter',
    'TkErrorNum'
] + list(reserved.values())

# Expresiones regulares para tokens simples.
t_TkComa         = r','
t_TkPunto        = r'\.'
t_TkDosPuntos    = r'\:'
t_TkParAbre      = r'\('
t_TkParCierra    = r'\)'
t_TkSuma         = r'\+'
t_TkResta        = r'-'
t_TkMult         = r'\*'
t_TkDiv          = r'/'
t_TkMod          = r'\%'
t_TkConjuncion   = r'/\\'
t_TkDisyuncion   = r'\\/'
t_TkNegacion     = r'\~'
t_TkMenor        = r'<'
t_TkMayor        = r'>'
t_TkMenorIgual   = r'<='
t_TkMayorIgual   = r'>='
t_TkIgual        = r'='
t_TkDesigual     = r'/='


# Ignora los tabs y espacios
t_ignore  = ' \t'

#------------------------------------------------------------------------------#

def t_TkErrorNum(t):

    r'[\d_]+[a-zA-Z_]+'
    t.value = t.value[0]
    return t
    
#------------------------------------------------------------------------------#

    # Descripción de la función: Regla para tokens correspondientes
    # a numeros.
def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

#------------------------------------------------------------------------------#

    # Descripción de la función:    Regla para conjuntos de caracteres. 
    # Si el caracter es igual a algun caracter reservado entonces t.type 
    # sera igual al del caracter reservado,de no ser igual a ningun 
    # caracter reservado entonces t.type sera igual a TkIdent.
def t_TkIdent(t):

    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'TkIdent')
    return t

#------------------------------------------------------------------------------#

# Descripción de la función:Regla para contar los numeros de linea.
def t_newline(t):

    r'\n+'
    t.lexer.lineno += len(t.value)

#------------------------------------------------------------------------------#

    # Descripción de la función: Reglas para los comentarios.
    # Los tokens obtenidos por esta expresion regular seran omitidos.
def t_TkComment(t):
    r'(\$-(.|\n)*?-\$)|(\$\$.*)'
    t.lexer.lineno += t.value.count('\n')
    pass

#------------------------------------------------------------------------------#

    # Descripción de la función: Reglas para caracteres. Este token solo 
    # toma caracteres encerrados entre comillas simples.
def t_TkCaracter(t):

    r'\'.\''
    return t

#------------------------------------------------------------------------------#
    # Descripción de la función: Funcion para localizar el numero de 
    # columna de una palabra.
# def NumeroColumna(input,token):

#     last_cr = input.rfind('\n',0,token.lexpos)
#     columna = (token.lexpos - last_cr) 
#     return columna

#------------------------------------------------------------------------------#

    # Descripción de la función: Funcion para el manejo de errores .
def t_error(t):

    ErrorEncontrado = token(None,t.value[0],\
        t.lineno,self.NumeroColumna(self.data,t))
    t.lexer.skip(1)

#-------------------------------------------------------------------------------#  
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

global Raiz
# Parsing rules

precedence = (
    ('left','TkConjuncion','TkDisyuncion'),
    ('left','TkSuma','TkResta'),
    ('left','TkMult','TkDiv'),
    ('right','UMINUS'),
    ('right','UMNEGACION'),
    )

# dictionary of names
names = { }

def p_inicioPrograma(t):
    ''' inicio : TkCreate LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd
                | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd '''

    if(t[1]=="execute"):
        t[0] = RaizAST(None,Execute(t[2]))
    elif (t[1] == "create"):
        t[0] = RaizAST(Create(t[2]),Execute(t[4]))

    global Raiz
    Raiz = t[0]


# def p_IniciolistaDeclaraciones(t):
#     ''' INICIO_LISTA_DECLARACIONES :  LISTA_DECLARACIONES LISTA_COMPORTAMIENTOS'''

def p_listaDeclaraciones(t):
    ''' LISTA_DECLARACIONES : LISTA_DECLARACIONES LISTA_DECLARACIONES
                            | TkInt TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd 
                            | TkBool TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd 
                            | TkChar TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd '''

    if(t[1] in {"int","bool","char"}):
        t[0] = Declaraciones(t[1],t[3],t[4])
    else:
        t[0] = agregarHijos(t[1],t[2])

def  p_listaIdent(t):
    ''' LISTA_IDENT : LISTA_IDENT TkComa LISTA_IDENT'''
    # t[0]= ListaHijos([t[1]]+[t[2]]
    t[0] = agregarHijos(t[1],t[3])
    # print(t[1].value)
    # global Raiz
    # Raiz = t[0]
 
def p_listaIdentUnico(t):
    '''  LISTA_IDENT : TkIdent'''
    t[0]=Identificadores(t[1])
    
# def p_IniciolistaComportamientos(t):
#     ''' INICIO_LISTA_COMPORTAMIENTOS : TkOn CONDICION TkDosPuntos INICIO_INSTRUCCIONES_ROBOT 
#                               |'''

def p_listaComportamientos(t):
    ''' LISTA_COMPORTAMIENTOS : LISTA_COMPORTAMIENTOS LISTA_COMPORTAMIENTOS
                              | TkOn CONDICION TkDosPuntos INSTRUCCIONES_ROBOT TkEnd 
                              |'''

    if (t[1] == "on"):
        t[0] = ListaComportamiento(t[2],t[4])
    else:
        t[0] = agregarHijos(t[1],t[2])
        global Raiz
        Raiz = t[0]

def p_condicion(t):
    ''' CONDICION : TkDeActivation
                  | TkActivation
                  | EXPRESION_BIN
                  | TkDefault''' 

    if (t[1] == "deactivation"):
        t[0]=Deactivation()
    elif(t[1] == "activation"):
        t[0]=Activation()
    elif(t[1] == "default"):
        t[0]=Default()
    else:
        t[0]=t[1]


def p_instruccionRobot(t):
    ''' INSTRUCCIONES_ROBOT : INSTRUCCIONES_ROBOT INSTRUCCIONES_ROBOT
                            | TkStore EXPRESION_BIN TkPunto 
                            | TkRecieve TkPunto
                            | TkCollect GUARDAR_VARIABLE TkPunto 
                            | TkDrop EXPRESION_BIN TkPunto
                            | TkRight EXPRESION_OPCIONAL TkPunto 
                            | TkLeft EXPRESION_OPCIONAL TkPunto 
                            | TkUp EXPRESION_OPCIONAL TkPunto 
                            | TkDown EXPRESION_OPCIONAL TkPunto 
                            | TkRead GUARDAR_VARIABLE TkPunto 
                            | TkSend TkPunto  '''
    if (t[1] == "store"):
        t[0] = Store(t[2])
        # global Raiz
        # Raiz = t[0]
    elif (t[1] == "recieve"):
        t[0] = Recieve()
        # global Raiz
        # Raiz = t[0]
    elif (t[1] == "collect"):
        t[0] = Collect(t[2])
        # global Raiz
        # Raiz = t[0]
    elif (t[1] == "drop"):
        t[0] = Drop(t[2])
        # global Raiz
        # Raiz = t[0]
    elif (t[1] in {"up","down","left","right"}):
        t[0] = Movimiento(t[1],t[2])
        # global Raiz
        # Raiz = t[0]
    elif (t[1] == "read"):
        t[0] = Read(t[2])
        # global Raiz
        # Raiz = t[0]
    elif (t[1] == "send"):
        t[0] = Send()
        # global Raiz
        # Raiz = t[0]
    else:
        t[0] = agregarHijos(t[1],t[2])
        # global Raiz
        # Raiz = t[0]

 
def p_expresionOpcional(t):
    ''' EXPRESION_OPCIONAL : EXPRESION_BIN
                           |'''
    if (len(t) != 1):                    
        t[0] = t[1]
    else:
        t[0] = None

def p_guardarVariable(t):
    ''' GUARDAR_VARIABLE : TkAs TkIdent
                        |'''
    if (len(t) != 1):
        if (t[1] == "as"):                    
            t[0] = Identificadores(t[2])
    else:
        t[0] = None

def p_SecuenciaInstruccionesControlador(t):
    '''  INSTRUCCIONES_CONTROLADOR : INSTRUCCIONES_CONTROLADOR INSTRUCCIONES_CONTROLADOR
                                  | TkActivate LISTA_IDENT TkPunto 
                                  | TkAdvance LISTA_IDENT TkPunto 
                                  | TkDeactivate LISTA_IDENT TkPunto 
                                  | TkIf EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR  TkEnd
                                  | TkIf EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR TkElse TkDosPuntos INSTRUCCIONES_CONTROLADOR  TkEnd
                                  | TkWhile EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR TkEnd

    '''
    if (t[1]=="activate"):
        t[0] = Activate(t[2])
        # global Raiz
        # Raiz = t[0]
    elif(t[1]=="advance"):
        t[0] = Advance(t[2])
        # global Raiz
        # Raiz = t[0]
    elif(t[1]=="deactivate"):
        t[0] = Deactivate(t[2])
        # global Raiz
        # Raiz = t[0]
    elif (t[1]=="if" and t[5] == "end"):
        t[0] = Condicional(t[2],t[4],None)

    elif (t[1]=="if" and t[5] == "else"):
        t[0] = Condicional(t[2],t[4],t[7])

    elif(t[1]=="while"):

        t[0]= While(t[2],t[4])
    else:
        t[0] = agregarHijos(t[1],t[2])
    
# def InstruccionesControlador(t):

#     ''' INSTRUCCIONES_CONTROLADOR : '''


# def p_expresionCondicional(t):
#     ''' EXPRESION_CONDICIONAL : INSTRUCCIONES_CONTROLADOR EXPRESION_ELSE'''


# def p_expresionElse(t):
#     ''' EXPRESION_ELSE : TkElse TkDosPuntos INSTRUCCIONES_CONTROLADOR 
#                         |'''

# def p_expresionBool(t):
#     ''' EXPRESION_BOOL : EXPRESION_BOOL TkConjuncion EXPRESION_BOOL
#                         | EXPRESION_BOOL TkDisyuncion EXPRESION_BOOL
#                         | EXPRESION_BOOL TkIgual EXPRESION_BOOL
#                         | EXPRESION_BOOL TkDesigual EXPRESION_BOOL
#                         | TkNegacion EXPRESION_BOOL
#                         | EXPRESION_ARITMETICA TkMayor EXPRESION_ARITMETICA
#                         | EXPRESION_ARITMETICA TkMenor EXPRESION_ARITMETICA
#                         | EXPRESION_ARITMETICA TkMayorIgual EXPRESION_ARITMETICA
#                         | EXPRESION_ARITMETICA TkMenorIgual EXPRESION_ARITMETICA
#                         | TkTrue
#                         | TkFalse'''


# def p_expresionExecute(t):
#     ''' expressionE : TkExecute expression '''

# def p_statement_assign(t):
#     'statement : TkIdent TkIgual EXPRESION_BIN'
#     names[t[1]] = t[3]

# def p_statement_expr(t):
#     '''statement : EXPRESION_BIN'''

#     #print(t[1])

def p_expression_binaria(t):
    '''EXPRESION_BIN : EXPRESION_BIN TkSuma EXPRESION_BIN
                  | EXPRESION_BIN TkResta EXPRESION_BIN
                  | EXPRESION_BIN TkMult EXPRESION_BIN
                  | EXPRESION_BIN TkDiv EXPRESION_BIN
                  | EXPRESION_BIN TkMod EXPRESION_BIN
                  | EXPRESION_BIN TkConjuncion EXPRESION_BIN
                  | EXPRESION_BIN TkDisyuncion EXPRESION_BIN
                  | EXPRESION_BIN TkIgual EXPRESION_BIN
                  | EXPRESION_BIN TkDesigual EXPRESION_BIN
                  | EXPRESION_BIN TkMayor EXPRESION_BIN
                  | EXPRESION_BIN TkMenor EXPRESION_BIN
                  | EXPRESION_BIN TkMayorIgual EXPRESION_BIN
                  | EXPRESION_BIN TkMenorIgual EXPRESION_BIN'''

    t[0] = BinOp(t[1],t[2],t[3])
    # global Raiz
    # Raiz=t[0]
    # print(t[0].op)
    # print(t[0].left)
    # print(t[0].right)
    # if t[2] == '+'  : 
    #     #t[0] = t[1] + t[3]
    #     t[0]=str(t[1])+" + "+str(t[3])
    # elif t[2] == '-': 
    #     #t[0] = t[1] - t[3]
    #     t[0] = str(t[1])+" - "+str(t[3])
    # elif t[2] == '*': 
    #     #t[0] = t[1] * t[3]
    #     t[0] = str(t[1])+" * "+str(t[3])
    # elif t[2] == '/': 
    #     #t[0] = t[1] / t[3]
    #     t[0] = str(t[1])+" / "+str(t[3])
    # elif t[2] == '/\\' : 
    #     print(str(t[1])+"/\\"+str(t[3]) )
    # elif t[2] == '\\/': 
    #     print(str(t[1])+"\\/"+str(t[3]) )
    #return(Raiz)

# def p_expression_bool(t):
#     '''expressionBool : expressionBool TkConjuncion expressionBool
#                       | expressionBool TkDisyuncion expressionBool'''
#     if t[2] == '/\\'  : print(str(t[1])+"/\\"+str(t[3]) )
#     elif t[2] == '\\/': print(str(t[1])+"\\/"+str(t[3]) )

# def p_expression_True(t):
#     '''expressionBool : TkTrue 
#                         | TkFalse'''
#     t[0] = t[2]

def p_negacion_bool(t):
    '''EXPRESION_BIN : TkNegacion EXPRESION_BIN %prec UMNEGACION'''
    t[0] = OperadorUnario(t[1],t[2])
    # global Raiz
    # Raiz=t[0]


def p_expression_uminus(t):
    'EXPRESION_BIN : TkResta EXPRESION_BIN %prec UMINUS'
    t[0] = OperadorUnario(t[1],t[2])
    # global Raiz
    # Raiz=t[0]

def p_expression_group(t):
    'EXPRESION_BIN : TkParAbre EXPRESION_BIN TkParCierra'
    t[0] = t[2]

def p_expression_number(t):
    'EXPRESION_BIN : TkNum'
    # t[0] = t[1]
    t[0] = Number(t[1])
def p_expression_TrueFalse(t):
    '''EXPRESION_BIN : TkTrue
                     | TkFalse '''
    t[0] = Booleano(t[1])

def p_expression_name(t):
    'EXPRESION_BIN : TkIdent'
    t[0] = Identificadores(t[1])

def p_expression_me(t):
    'EXPRESION_BIN : TkMe'
    t[0] = VariableMe(t[1])
    # try:
    #     t[0] = names[t[1]]
    # except LookupError:
    #     print("Undefined name '%s'" % t[1])
    #     t[0] = 0

def p_expression_caracter(t):
    'EXPRESION_BIN : TkCaracter'
    t[0] = Caracter(t[1])


def p_error(t):
    print("Syntax error at '%s' in line " % t.value,t.lineno)
    #print("Syntax error at ")


import ply.yacc as yacc
parser = yacc.yacc()

datos = LeerArchivoEntrada()
parser.parse(datos)

# print(Raiz.op)
# print(Raiz.left.op)
# print(Raiz.left.left.value)
# print(Raiz.left.right.value)
# print(Raiz.right.value)
# print(Raiz.right.left.value)

#print(Raiz.type)
#print(Raiz.identificador)
#Raiz.expresiones.imprimirExpresionesBinarias()
Raiz.imprimirAST()

# print(Raiz.type)
# print(Raiz.Instrucciones.type)
# print(Raiz.Instrucciones.expresionesCondicional.op)
# print(Raiz.Instrucciones.expresionesCondicional.left.value)
# print(Raiz.Instrucciones.expresionesCondicional.right.value)
# print(Raiz.Instrucciones.exito.type)
# print(Raiz.Instrucciones.exito.Identificadores.value)
# print(Raiz.Instrucciones.fracaso.type)
# print(Raiz.Instrucciones.fracaso.Identificadores.value)
# # print(Raiz.Instrucciones.exito.sig.type)
# # print(Raiz.Instrucciones.exito.sig.Identificadores.value)
# print(Raiz.Instrucciones.sig.type)
# print(Raiz.Instrucciones.sig.Identificadores.value)


# print(Raiz.type)
# print(Raiz.tipoRobot)
# print(Raiz.identificadores.value)
# print(Raiz.listaComportamiento.condicion.type)
# print(Raiz.listaComportamiento.instrucciones.type)
# Raiz.listaComportamiento.instrucciones.expresiones.imprimirExpresionesBinarias()
# print(Raiz.listaComportamiento.instrucciones.sig.type)

# print(Raiz.sig.type)
# print(Raiz.sig.tipoRobot)
# print(Raiz.sig.identificadores.value)
# print(Raiz.sig.listaComportamiento.condicion.type)
# print(Raiz.sig.listaComportamiento.instrucciones.type)
# Raiz.sig.listaComportamiento.instrucciones.expresiones.imprimirExpresionesBinarias()
# print(Raiz.sig.listaComportamiento.instrucciones.sig.type)



# print(Raiz.condicion.type)
# print(Raiz.instrucciones.type)
# print(Raiz.instrucciones.sig.type)

# print(Raiz.sig.type)
# print(Raiz.sig.condicion.type)
# print(Raiz.sig.instrucciones.type)
# Raiz.sig.instrucciones.expresiones.imprimirExpresionesBinarias()
# print(Raiz.sig.instrucciones.sig.type)



# print(Raiz.sig.type)
# print(Raiz.Instrucciones.expresiones.op)
# print(Raiz.Instrucciones.expresiones.left.value)
# print(Raiz.Instrucciones.expresiones.right.value)
# print(Raiz.Instrucciones.InstruccionesWhile.type)
# print(Raiz.Instrucciones.InstruccionesWhile.Identificadores.value)
# print(Raiz.Instrucciones.InstruccionesWhile.sig.type)
# print(Raiz.Instrucciones.InstruccionesWhile.sig.Identificadores.value)
# print(Raiz.sig.sig.type)
# print(Raiz.Instrucciones.sig.Identificadores.value)


# print(Raiz.Instrucciones.Identificadores.value)
# print(Raiz.Instrucciones.Identificadores.sig.value)
# print(Raiz.Instrucciones.Identificadores.sig.sig.value)
# print(Raiz.Instrucciones.sig.type)
# print(Raiz.Instrucciones.sig.Identificadores.value)
# print(Raiz.Instrucciones.sig.sig.type)
# print(Raiz.Instrucciones.sig.sig.Identificadores.value)

# print(Raiz.Identificadores.value)
# print(Raiz.Identificadores.sig.value)
# print(Raiz.Identificadores.sig.sig.value)

# print(Raiz.value)
# print(Raiz.sig.value)
# print(Raiz.sig.sig.value)
#print(Raiz.hijos[1].value)

# print(Raiz.hijos[0].value)
# print(Raiz.hijos[1].value)
#print(Raiz.hijos[1].hijos[1].value)

# print(Raiz.op)
# print(Raiz.left.value)
# print(Raiz.right.op)
# print(Raiz.right.left.value)
# print(Raiz.right.right.value)

# print(Raiz.op)
# print(Raiz.value.op)
# print(Raiz.value.left.op)
# print(Raiz.value.left.left.value)
# print(Raiz.value.left.right.value)
# print(Raiz.value.right.value)