'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: parserBOT.py
*
* Nombres:
*     Alejandra Cordero / Carnet: 12-10645
*     Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion: Definicion del modulo parserBot.
*
*
* Ultima modificacion: 12/02/2016
*
'''

#------------------------------------------------------------------------------#
#                            IMPORTE DE MODULOS                                #
#------------------------------------------------------------------------------#

from Arbol import *
from Tokens import *
from Lexer import * 
from TablaSimbolos import *
import ply.lex as lex 
import ply.yacc as yacc



global Top
global Pila
global Ultimo
global esListaComportamiento 
esListaComportamiento = 0
Ultimo = None
Pila = []

#------------------------------------------------------------------------------#
#                           DEFINICION DE FUNCIONES                            #
#------------------------------------------------------------------------------#

def unirListaEnlazada(lista1,lista2):
    '''
      * Descripción de la función: Esta funcion une dos listas enlazadas
                                 dado dos apuntadores a la cabecera de las 
                                 mismas.
      * Variables de entrada: 
            - lista1: Apuntador a la cabecera de la primera lista enlazada
            - lista2: Apuntador a la cabecera de la primera lista enlazada.
      * Variables de salida: 
            - lista1: apuntador a la cabecera de la lista enlazada unida.
    '''
    aux = lista1
    while aux.sig != None:
        aux = aux.sig
    aux.sig = lista2

    return lista1

#------------------------------------------------------------------------------#

def CrearTablaSimbolos(ListaIdentificadores,tipoRobot):

    '''
      * Descripción de la función: Esta funcion une dos listas enlazadas
                                 dado dos apuntadores a la cabecera de las 
                                 mismas.
      * Variables de entrada: 
            - lista1: Apuntador a la cabecera de la primera lista enlazada
            - lista2: Apuntador a la cabecera de la primera lista enlazada.
      * Variables de salida: 
            - lista1: apuntador a la cabecera de la lista enlazada unida.
    '''

    global Ultimo
    aux = ListaIdentificadores
    Tabla = TablaSimbolos(Ultimo)
    Ultimo = Tabla

    while (aux!=None) :

        redeclaracion = Tabla.buscar(aux.value)

        if (redeclaracion != None):
            print("Error de contexto: Redeclaracion de la variable","\'"+\
                str(aux.value)+"\'","en la linea",aux.numeroLinea)
            sys.exit()
        else:
            Tabla.insertar(aux.value,tipoRobot,"robot")

        aux = aux.sig

    # Inserto 'me' en la tabla
    Tabla.insertar("me",tipoRobot) 

#------------------------------------------------------------------------------#

def VerificarVariableDeclarada(NodoVariable,TablaSimbolos):

    '''
      * Descripción de la función: Esta funcion une dos listas enlazadas
                                 dado dos apuntadores a la cabecera de las 
                                 mismas.
      * Variables de entrada: 
            - lista1: Apuntador a la cabecera de la primera lista enlazada
            - lista2: Apuntador a la cabecera de la primera lista enlazada.
      * Variables de salida: 
            - lista1: apuntador a la cabecera de la lista enlazada unida.
    '''

    aux = NodoVariable

    while (aux!= None):
        Existe = TablaSimbolos.buscar(aux.value)
        if Existe == None:
            print("Error de contexto: la variable \'"+str(aux.value)+"\' \
                no ha sido declarada en la linea",aux.numeroLinea)
            sys.exit()
        aux = aux.sig

    return Existe

#------------------------------------------------------------------------------#

def VerificarTipoVariable(tipo,identificador,tipoVariableAevaluar):

    '''
      * Descripción de la función: Esta funcion une dos listas enlazadas
                                 dado dos apuntadores a la cabecera de las 
                                 mismas.
      * Variables de entrada: 
            - lista1: Apuntador a la cabecera de la primera lista enlazada
            - lista2: Apuntador a la cabecera de la primera lista enlazada.
      * Variables de salida: 
            - lista1: apuntador a la cabecera de la lista enlazada unida.
    '''

    if (tipoVariableAevaluar[0]!=tipo):
        print("Error de contexto: Hay un error de tipos en la linea",\
            identificador.numeroLinea)
        sys.exit()
    
#------------------------------------------------------------------------------#

def VerificarCondicionListaDeclaraciones(ArbolCondicion):

    '''
      * Descripción de la función: Esta funcion une dos listas enlazadas
                                 dado dos apuntadores a la cabecera de las 
                                 mismas.
      * Variables de entrada: 
            - lista1: Apuntador a la cabecera de la primera lista enlazada
            - lista2: Apuntador a la cabecera de la primera lista enlazada.
      * Variables de salida: 
            - lista1: apuntador a la cabecera de la lista enlazada unida.
    '''

    if (ArbolCondicion.condicion.type == "EXPRESION_BINARIA"):

        VerificarExpresionBinaria(ArbolCondicion.condicion)
    else:
        pass
   
#------------------------------------------------------------------------------#

def VerificarInstruccionesListaDeclaraciones(ArbolInstrucciones,tipoRobot):

    '''
      * Descripción de la función: Esta funcion une dos listas enlazadas
                                 dado dos apuntadores a la cabecera de las 
                                 mismas.
      * Variables de entrada: 
            - lista1: Apuntador a la cabecera de la primera lista enlazada
            - lista2: Apuntador a la cabecera de la primera lista enlazada.
      * Variables de salida: 
            - lista1: apuntador a la cabecera de la lista enlazada unida.
    '''

    instrucciones = ArbolInstrucciones.instrucciones
    #print("INTRUCCION",instrucciones.type)
    while (instrucciones!=None):

        if (instrucciones.type in {"STORE","DROP","RIGHT","LEFT","UP","DOWN"}):
            print("Debo construir una funcion que chequee los tipos de expresion binarias")
            VerificarExpresionBinaria(instrucciones.expresiones)

        elif (instrucciones.type in {"COLLECT","READ"}):
            # print("Se Verifica identificador")
            identificador = instrucciones.identificador
            if (identificador!=None):
                resultado = Ultimo.buscar(identificador.value)
                # print("RESULTADO",resultado)
                # print("INTRUCCION",instrucciones.type)

                if(resultado!=None):

                    if(resultado[1]=="robot"):
                        print("Error de contexto en linea",
                            identificador.numeroLinea ,": No se deben usar \
                            variables bot")
                    
                    # En duda
                    elif(resultado[1]!="robot"):
                        print("Error de contexto en linea",
                            identificador.numeroLinea ,": redeclaracion de\
                             variables")
                    sys.exit()

                else:
                    # print("Insertando")
                    Ultimo.insertar(identificador.value,tipoRobot)

        # print("TABLA",Ultimo.tabla)
        instrucciones = instrucciones.sig

#------------------------------------------------------------------------------#

def VerificarExpresionBinaria(exprBin):

    '''
      * Descripción de la función: Esta funcion une dos listas enlazadas
                                 dado dos apuntadores a la cabecera de las 
                                 mismas.
      * Variables de entrada: 
            - lista1: Apuntador a la cabecera de la primera lista enlazada
            - lista2: Apuntador a la cabecera de la primera lista enlazada.
      * Variables de salida: 
            - lista1: apuntador a la cabecera de la lista enlazada unida.
    '''

    Raiz = exprBin

    if (Raiz != None):

        if (Raiz.type != "EXPRESION_BINARIA"):

            if (Raiz.type in {"ident","me"}):

                Resultado = VerificarVariableDeclarada(Raiz,Ultimo)

                if (esListaComportamiento == 1):

                    if (Resultado[1]=="robot"):

                        print("Error de contexto en linea",Raiz.numeroLinea ,
                            ": No se deben usar variables bot")
                        sys.exit()

                
                return Resultado[0]

            else:

                print("RESULTADO 2:",Raiz.type)
                return Raiz.type

        elif(Raiz.type == "EXPRESION_BINARIA"):

            if (Raiz.op in {"-","*","/","%","<",">","/=","=","<=",">=","+"}) :
                if (VerificarExpresionBinaria(Raiz.left) != "int" \
                    or VerificarExpresionBinaria(Raiz.right) != "int"):
                    print("Error de tipos en la linea",Raiz.linea)
                    sys.exit()

                else:

                    if (Raiz.op in {"-","*","/","%","+"}):
                        return "int"

                    else:
                        return "bool"

            elif (Raiz.op in {"/\\","\\/"}):

                if (VerificarExpresionBinaria(Raiz.left) != "bool" \
                    or VerificarExpresionBinaria(Raiz.right) != "bool"):
                    print("Error de tipos en la linea",Raiz.linea)
                    sys.exit()
                else:
                    return "bool"

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

# Descripcion de la funcion: Regla para los posibles inicios de un programa 
# en BOT
def p_inicioPrograma(t):
    ''' inicio : OPEN_SCOPE TkCreate LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd CLOSE_SCOPE
                | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd '''

    
    if (t[1] == "execute"):
        t[0] = RaizAST(None,Execute(t[2]),Ultimo)
        #print("execute")

    elif (t[2] == "create"):
        #print("1create")
        t[0] = RaizAST(Create(t[3]),Execute(t[5]),Ultimo)
        #t[0] = TablaSimbolos


#------------------------------------------------------------------------------#

def p_openScope(t):
    '''OPEN_SCOPE : '''

    global Top
    global Ultimo
    global Pila
    global esListaComportamiento 
    #print("prendo")
    esListaComportamiento  = 1
    Top = TopeDeTablaSimbolos(Ultimo)
    Ultimo = Top
    # Empilo Top
    Pila.append(Top)


#------------------------------------------------------------------------------#

def p_closeScope(t):
    '''CLOSE_SCOPE : '''
    global Ultimo
    global Top
    global Pila
    aux = Ultimo
    while (aux!= None):

        if(aux.type!="top"):
            print(aux.tabla)
        else:
            print("Estoy en el top")
        aux = aux.padre
    Ultimo =  Top.padre
    # Desempilo top
    Pila.pop()

    # Asigno top al tope de la pila
    if (len(Pila)==0):
        Top = None
    else:
        Top = Pila[-1]


#------------------------------------------------------------------------------#

# def p_empty(t):
#     '''empty : '''
#     pass
#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir las declaraciones de robots.
def p_listaDeclaraciones(t):
    ''' LISTA_DECLARACIONES : LISTA_DECLARACIONES LISTA_DECLARACIONES
                            | TkInt TkBot LISTA_IDENT CHECK_LISTA_DECLARACION LISTA_COMPORTAMIENTOS TkEnd 
                            | TkInt TkBot LISTA_IDENT TkEnd 
                            | TkBool TkBot LISTA_IDENT CHECK_LISTA_DECLARACION LISTA_COMPORTAMIENTOS TkEnd
                            | TkBool TkBot LISTA_IDENT TkEnd  
                            | TkChar TkBot LISTA_IDENT CHECK_LISTA_DECLARACION LISTA_COMPORTAMIENTOS TkEnd
                            | TkChar TkBot LISTA_IDENT TkEnd '''

    #print("Lista declaraciones")
    if(t[1] in {"int","bool","char"}):

        if (t[4] == "end"):
            t[0] = Declaraciones(t[1],t[3],t[5])
        else:
            t[0] = Declaraciones(t[1],t[3],None)


        # Se crea la tabla de simbolos
        CrearTablaSimbolos(t[3],t[1])

        global esListaComportamiento 
        esListaComportamiento  = 0

        Arbol = t[5]

        # Se verifica la condicion de la lista de declaraciones  
        VerificarCondicionListaDeclaraciones(Arbol)

        #Se verifican las instrucciones de la lista de declaraciones
        VerificarInstruccionesListaDeclaraciones(Arbol,t[1])
  
    else:

        t[0] = unirListaEnlazada(t[1],t[2])

# #------------------------------------------------------------------------------#

def p_checkListaComportamiento(t):
    '''CHECK_LISTA_DECLARACION : '''
    global esListaComportamiento 
    esListaComportamiento  = 1

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para la secuenciacion de identificadores 
# en una declaracion de robot.
def  p_listaIdent(t):
    ''' LISTA_IDENT : LISTA_IDENT TkComa LISTA_IDENT'''
    #print("ListaComportamiento")
    t[0] = unirListaEnlazada(t[1],t[3])

 
#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir un identificador por declaracion.
def p_listaIdentUnico(t):
    '''  LISTA_IDENT : TkIdent'''
    t[0] = Identificadores(t[1],t.lineno(1))
    
#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para iniciar / secuenciar la lista de 
# comportamientos de un robot.
def p_listaComportamientos(t):
    ''' LISTA_COMPORTAMIENTOS : LISTA_COMPORTAMIENTOS LISTA_COMPORTAMIENTOS
                              | TkOn CONDICION TkDosPuntos INSTRUCCIONES_ROBOT TkEnd'''

    #print("Lista comportamientos")
    #print(t[2],t[4])
                   
    if (t[1] == "on"):

        t[0] = ListaComportamiento(t[2],t[4])

    else:
        t[0] = unirListaEnlazada(t[1],t[2])


#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla que define las posibles condiciones que 
# pueden utilizarse para una lista de comportamientos de un robot.
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

# Descripcion de la funcion: Regla para definir / secuencias las instrucciones
# de robot a utilizar en las listas de comportamiento.
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
    
    #print("IR")
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
        t[0] = unirListaEnlazada(t[1],t[2])
 

#------------------------------------------------------------------------------#
 
# Descripcion de la funcion: Regla que se utiliza cuando en una instruccion 
# de robot de movimiento la expresion a evaluar es opcional.
def p_expresionOpcional(t):
    ''' EXPRESION_OPCIONAL : EXPRESION_BIN
                           |'''
    if (len(t) != 1):                    
        t[0] = t[1]
    else:
        t[0] = None

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla a utilizar en las instrucciones Collect 
# y Read para almacenar el valor del identificador utilizado.
def p_guardarVariable(t):
    ''' GUARDAR_VARIABLE : TkAs TkIdent
                        |'''
    if (len(t) != 1):
        if (t[1] == "as"):                    
            t[0] = Identificadores(t[2],t.lineno(2))
    else:
        t[0] = None

def p_S(t):
    ''' S : OPEN_SCOPE TkCreate LISTA_DECLARACIONES
          | '''
#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir / secuenciar las instrucciones
# de controlador de un programa en BOT.
def p_SecuenciaInstruccionesControlador(t):
    '''  INSTRUCCIONES_CONTROLADOR : INSTRUCCIONES_CONTROLADOR INSTRUCCIONES_CONTROLADOR
                                  | TkActivate LISTA_IDENT TkPunto 
                                  | TkAdvance LISTA_IDENT TkPunto 
                                  | TkDeactivate LISTA_IDENT TkPunto 
                                  | TkIf EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR  TkEnd
                                  | TkIf EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR TkElse TkDosPuntos INSTRUCCIONES_CONTROLADOR  TkEnd
                                  | TkWhile EXPRESION_BIN TkDosPuntos INSTRUCCIONES_CONTROLADOR TkEnd
                                  | OPEN_SCOPE TkCreate LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd CLOSE_SCOPE
                                  | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd  '''
   
    
    #print("IC")

    # TablaDeAlcance = UltimaTablaSimbolos
    # tablaSimb = TablaSimbolos(UltimaTablaSimbolos)
    # global UltimaTablaSimbolos
    # UltimaTablaSimbolos = tablaSimb

    if (t[1]=="activate"):
        #UltimaTablaSimbolos = TablaDeAlcance 
        #print("activate")
        t[0] = Activate(t[2])
        VerificarVariableDeclarada(t[2],Ultimo) 

    elif(t[1]=="advance"):
        #print("advance")
        t[0] = Advance(t[2])
        VerificarVariableDeclarada(t[2],Ultimo)

    elif(t[1]=="deactivate"):
        #print("deactivate")
        t[0] = Deactivate(t[2])
        VerificarVariableDeclarada(t[2],Ultimo)

    elif (t[1]=="if" and t[5] == "end"):
        t[0] = Condicional(t[2],t[4],None)

    elif (t[1]=="if" and t[5] == "else"):
        t[0] = Condicional(t[2],t[4],t[7])

    elif(t[1]=="while"):

        t[0]= While(t[2],t[4])

    elif(t[1]=="execute"):

        t[0] = RaizAST(None,Execute(t[2]))

    elif (t[2] == "create"):
        #print("create")
        t[0] = RaizAST(Create(t[3]),Execute(t[5]),Ultimo)

    else:
        #print("hola")
        # UltimaTablaSimbolos = TablaDeAlcance
        t[0] = unirListaEnlazada(t[1],t[2])
    

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir las expresiones binarias 
# (aritmeticas, booleanas y relacionales)
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

    t[0] = ExpresionBinaria(t[1],t[2],t[3],t.lineno(2))

    if (esListaComportamiento  != 1):
        print("Chequeo tipos")
        VerificarExpresionBinaria(t[0])
    else:
        pass

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir la negacion booleana.
def p_negacion_bool(t):
    '''EXPRESION_BIN : TkNegacion EXPRESION_BIN %prec UMNEGACION'''
    t[0] = OperadorUnario(t[1],t[2])
    if( t[2]!= "booleano"):
        print("Error de tipos")
        sys.exit()

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para el operador menos unario.
def p_expression_uminus(t):
    'EXPRESION_BIN : TkResta EXPRESION_BIN %prec UMINUS'
    t[0] = OperadorUnario(t[1],t[2])
    if( t[2]!= "number"):
        print("Error de tipos")
        sys.exit()

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir la parentizacion.
def p_expression_group(t):
    'EXPRESION_BIN : TkParAbre EXPRESION_BIN TkParCierra'
    t[0] = t[2]

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar el valor de un numero.
def p_expression_number(t):
    'EXPRESION_BIN : TkNum'
    t[0] = Number(t[1])

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar un valor booleano 
# (True o False)
def p_expression_TrueFalse(t):
    '''EXPRESION_BIN : TkTrue
                     | TkFalse '''
    t[0] = Booleano(t[1])

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar un identificador.
def p_expression_name(t):
    'EXPRESION_BIN : TkIdent'
    t[0] = Identificadores(t[1],t.lineno(1))
    
#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar la variable especial
# me
def p_expression_me(t):
    'EXPRESION_BIN : TkMe'
    t[0] = VariableMe(t[1])

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar un caracter.
def p_expression_caracter(t):
    'EXPRESION_BIN : TkCaracter'
    t[0] = Caracter(t[1])

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para detectar e imprimir errores sintacticos.
def p_error(t):
    if(t != None):
        print("Error sintactico " + str(t.value) + " en linea " + str(t.lineno))
    else:
        print("Error sintactico")

    sys.exit()

#------------------------------------------------------------------------------#