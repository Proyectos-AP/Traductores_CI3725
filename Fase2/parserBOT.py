'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: PARSERBOT.py
*
* Nombres:
*       Alejandra Cordero / Carnet: 12-10645
*       Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion: Definicion del modulo parserBot.
*
*
* Ultima modificacion: 02/10/2015
*
'''

#------------------------------------------------------------------------------#
#                            IMPORTE DE MODULOS                                #
#------------------------------------------------------------------------------#

from Arbol import *
from Tokens import *
from Lexer import * 
import ply.lex as lex 
import ply.yacc as yacc

#------------------------------------------------------------------------------#
#                        DEFINICION DEL MODULO PARSERBOT                       #
#------------------------------------------------------------------------------#

# Reglas de precedencia a utilizar en las gramaticas:
precedence = (
    ('left','TkConjuncion','TkDisyuncion'),
    ('left','TkSuma','TkResta'),
    ('left','TkMult','TkDiv'),
    ('right','UMINUS'),
    ('right','UMNEGACION'),
    )

#------------------------------------------------------------------------------#


def p_inicioPrograma(t):
    ''' inicio : TkCreate LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd
                | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd '''

    if (t[1] == "execute"):
        t[0] = RaizAST(None,Execute(t[2]))

    elif (t[1] == "create"):
        t[0] = RaizAST(Create(t[2]),Execute(t[4]))

    Raiz = t[0]

    return Raiz

#------------------------------------------------------------------------------#

def p_listaDeclaraciones(t):
    ''' LISTA_DECLARACIONES : LISTA_DECLARACIONES LISTA_DECLARACIONES
                            | TkInt TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd 
                            | TkBool TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd 
                            | TkChar TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd '''

    if(t[1] in {"int","bool","char"}):
        t[0] = Declaraciones(t[1],t[3],t[4])

    else:
        t[0] = agregarHijos(t[1],t[2])

#------------------------------------------------------------------------------#

def  p_listaIdent(t):
    ''' LISTA_IDENT : LISTA_IDENT TkComa LISTA_IDENT'''
    t[0] = agregarHijos(t[1],t[3])
 
#------------------------------------------------------------------------------#

def p_listaIdentUnico(t):
    '''  LISTA_IDENT : TkIdent'''
    t[0] = Identificadores(t[1])
    
#------------------------------------------------------------------------------#

def p_listaComportamientos(t):
    ''' LISTA_COMPORTAMIENTOS : LISTA_COMPORTAMIENTOS LISTA_COMPORTAMIENTOS
                              | TkOn CONDICION TkDosPuntos INSTRUCCIONES_ROBOT TkEnd 
                              |'''

    if (len(t) != 1):                     
        if (t[1] == "on"):
            t[0] = ListaComportamiento(t[2],t[4])

        else:
            t[0] = agregarHijos(t[1],t[2])

    else:
        t[0] = None

#------------------------------------------------------------------------------#

def p_condicion(t):
    ''' CONDICION : TkDeActivation
                  | TkActivation
                  | EXPRESION_BIN
                  | TkDefault''' 

    if (t[1] in {"deactivation","activation","default"}):
        t[0] = Condicion(t[1])
    else:
        t[0] = t[1]

#------------------------------------------------------------------------------#

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

    elif (t[1] == "recieve"):
        t[0] = Recieve()

    elif (t[1] == "collect"):
        t[0] = Collect(t[2])

    elif (t[1] == "drop"):
        t[0] = Drop(t[2])

    elif (t[1] in {"up","down","left","right"}):
        t[0] = Movimiento(t[1],t[2])

    elif (t[1] == "read"):
        t[0] = Read(t[2])

    elif (t[1] == "send"):
        t[0] = Send()

    else:
        t[0] = agregarHijos(t[1],t[2])

#------------------------------------------------------------------------------#
 
def p_expresionOpcional(t):
    ''' EXPRESION_OPCIONAL : EXPRESION_BIN
                           |'''
    if (len(t) != 1):                    
        t[0] = t[1]
    else:
        t[0] = None

#------------------------------------------------------------------------------#

def p_guardarVariable(t):
    ''' GUARDAR_VARIABLE : TkAs TkIdent
                        |'''
    if (len(t) != 1):
        if (t[1] == "as"):                    
            t[0] = Identificadores(t[2])
    else:
        t[0] = None

#------------------------------------------------------------------------------#

def p_SecuenciaInstruccionesControlador(t):
    '''  INSTRUCCIONES_CONTROLADOR : INSTRUCCIONES_CONTROLADOR INSTRUCCIONES_CONTROLADOR
                                  | TkActivate LISTA_IDENT TkPunto 
                                  | TkAdvance LISTA_IDENT TkPunto 
                                  | TkDeactivate LISTA_IDENT TkPunto 
                                  | TkIf EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR  TkEnd
                                  | TkIf EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR TkElse TkDosPuntos INSTRUCCIONES_CONTROLADOR  TkEnd
                                  | TkWhile EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR TkEnd
                                  | TkCreate LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd
                                  | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd  '''
   
    if (t[1]=="activate"):
        t[0] = Activate(t[2])

    elif(t[1]=="advance"):
        t[0] = Advance(t[2])

    elif(t[1]=="deactivate"):
        t[0] = Deactivate(t[2])

    elif (t[1]=="if" and t[5] == "end"):
        t[0] = Condicional(t[2],t[4],None)

    elif (t[1]=="if" and t[5] == "else"):
        t[0] = Condicional(t[2],t[4],t[7])

    elif(t[1]=="while"):
        t[0]= While(t[2],t[4])

    elif(t[1]=="execute"):
        t[0] = RaizAST(None,Execute(t[2]))

    elif (t[1] == "create"):
        t[0] = RaizAST(Create(t[2]),Execute(t[4]))

    else:
        t[0] = agregarHijos(t[1],t[2])

#------------------------------------------------------------------------------#

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

#------------------------------------------------------------------------------#

def p_negacion_bool(t):
    '''EXPRESION_BIN : TkNegacion EXPRESION_BIN %prec UMNEGACION'''
    t[0] = OperadorUnario(t[1],t[2])

#------------------------------------------------------------------------------#

def p_expression_uminus(t):
    'EXPRESION_BIN : TkResta EXPRESION_BIN %prec UMINUS'
    t[0] = OperadorUnario(t[1],t[2])

#------------------------------------------------------------------------------#

def p_expression_group(t):
    'EXPRESION_BIN : TkParAbre EXPRESION_BIN TkParCierra'
    t[0] = t[2]

#------------------------------------------------------------------------------#

def p_expression_number(t):
    'EXPRESION_BIN : TkNum'
    t[0] = Number(t[1])

#------------------------------------------------------------------------------#

def p_expression_TrueFalse(t):
    '''EXPRESION_BIN : TkTrue
                     | TkFalse '''
    t[0] = Booleano(t[1])

#------------------------------------------------------------------------------#

def p_expression_name(t):
    'EXPRESION_BIN : TkIdent'
    t[0] = Identificadores(t[1])

#------------------------------------------------------------------------------#

def p_expression_me(t):
    'EXPRESION_BIN : TkMe'
    t[0] = VariableMe(t[1])

#------------------------------------------------------------------------------#

def p_expression_caracter(t):
    'EXPRESION_BIN : TkCaracter'
    t[0] = Caracter(t[1])

#------------------------------------------------------------------------------#

def p_error(t):
    if(t != None):
        print("Error sintactico " + str(t.value) + " en linea " + str(t.lineno))
    else:
        print("Error sintactico")
    sys.exit()

#------------------------------------------------------------------------------#