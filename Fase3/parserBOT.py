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


global scopeActual
global Top
global Pila
global Ultimo
global esListaComportamiento 
esListaComportamiento = 0
Ultimo = None
scopeActual = None
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
    scope = scopeActual

    # Se verifica si la variable fue declarada en algun alcance anterior
    VerificarVariableNoDeclarada(ListaIdentificadores,scopeActual)

    # Se verifica si la variable fue declarada en el alcance local
    while (aux!=None) :
        redeclaracion = Tabla.buscar(aux.value)
        if (redeclaracion != None):
            print("Error de contexto: Redeclaracion de la variable","\'"+\
                str(aux.value)+"\'","en la linea",aux.numeroLinea,".")
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

    while (aux != None):
        Existe = TablaSimbolos.buscarLocal(aux.value)

        if Existe == None:
            print("Error de contexto: la variable \'"+str(aux.value)+"\'" + 
                " no ha sido declarada en la linea",aux.numeroLinea,".")
            sys.exit()

        aux = aux.sig

    return Existe

#------------------------------------------------------------------------------#
def VerificarVariableNoDeclarada(NodoVariable,TablaSimbolos):


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

    # aux = NodoVariable
    # Existe = None
    # Tabla = TablaSimbolos
    # print("TABLA: ",Tabla)

    # while (aux!= None):

    #     while (Tabla!= None):
            
    #         Existe = Tabla.padre.buscar(aux.value)

    #         if (Existe != None):
    #             print("Error de contexto en la linea",aux.numeroLinea,":la variable \'"+str(aux.value)+"\'" +
    #                 " ya ha sido declarada.")
    #             sys.exit()

    #     aux = aux.sig

    # return Existe

    aux = NodoVariable
    Existe = None
    Tabla = TablaSimbolos
    while (Tabla!= None):

        # print("ULTIMO SCOPE ANTERIOR",Tabla.padre.tabla)
        while (aux!= None):

            Existe = Tabla.padre.buscar(aux.value)

            if (Existe != None):
                print("Error de contexto en la linea",aux.numeroLinea,
                    ":la variable \'"+str(aux.value)+"\'" + 
                    " ya ha sido declarada.")
                sys.exit()

            aux = aux.sig
        aux = NodoVariable
        Tabla = Tabla.scopeAnterior

    return Existe

#------------------------------------------------------------------------------#

def VerificarVariableDeclaradaE(NodoVariable,TablaSimbolos):

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
    Existe = None
    Tabla = TablaSimbolos

    while (aux!= None):

        while (Tabla!= None):
            
            Existe = Tabla.padre.buscar(aux.value)

            if (Existe == None and Tabla.scopeAnterior==None):
                print("Error de contexto en la linea",aux.numeroLinea,":la variable \'"+str(aux.value)+"\'"+" no ha sido declarada.")
                sys.exit()

            elif(Existe==None and Tabla.scopeAnterior!=None):
                Tabla = Tabla.scopeAnterior

            else:
                if (Existe[1]!="robot"):
                    print("Error de contexto en la linea",aux.numeroLinea,":la variable \'"+str(aux.value)+"\'"+" no ha sido declarada.")
                    sys.exit()

                else:
                    break

        Tabla = TablaSimbolos
        aux = aux.sig

    return Existe

#------------------------------------------------------------------------------#

def VerificarTipoVariable(tipo,tipoVariableAevaluar,numeroLinea):

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

    if (tipoVariableAevaluar!=tipo):
        print("Error de contexto: Hay un error de tipos en la linea",numeroLinea,".")
        sys.exit()
    
#------------------------------------------------------------------------------#

def VerificarCondicionListaDeclaraciones(ArbolCondicion,TablaSimbolos):

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


    aux = ArbolCondicion


    while (aux!=None):
        #print("Condicion",aux.condicion.type)

        if (aux.condicion.type not in {"activation","deactivation","default"} ):

            Tipo = VerificarExpresionBinaria(aux.condicion,TablaSimbolos)
            #print("TIPO",Tipo)

            if (Tipo != "bool"):
                print("Error de contexto: Hay un error de tipos en la linea",aux.numeroLinea,".")
                sys.exit()

        aux = aux.sig

#------------------------------------------------------------------------------#

def VerificarGuardaEstructuraControl(ArbolExpr,TablaSimbolos):

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

    Tipo = VerificarExpresionBinaria(ArbolExpr,TablaSimbolos)
    #print("TIPO",Tipo)

    if (Tipo != "bool"):
        print("Error de contexto: Hay un error de tipos en la linea",ArbolExpr.numeroLinea,".")
        sys.exit()

#------------------------------------------------------------------------------#

def VerificarInstruccionesListaDeclaraciones(ArbolInstrucciones,tipoRobot,TablaSim):

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
    ListaTablas = []
    aux = ArbolInstrucciones
    #print("INTRUCCION",instrucciones.type)

    while (aux!=None):
        #print("CONDICION",aux.condicion.type)
        instrucciones = aux.instrucciones
        TablaLocal = TablaSimbolos()
        TablaLocal.insertar("me",tipoRobot)
        while (instrucciones!=None):    

            #print("INSTRUCCIONES", instrucciones.type) 
            if (instrucciones.type in {"STORE","DROP","right","left","up","down"}):
                # print("Debo construir una funcion que chequee los tipos de expresion binarias")
                #print("Arbol expresiones",instrucciones.expresiones,instrucciones.type)
                Tipo = VerificarExpresionBinaria(instrucciones.expresiones,TablaLocal)

                if (instrucciones.type in {"right","left","up","down"}):
                    VerificarTipoVariable(Tipo,"int",instrucciones.numeroLinea)

                elif (instrucciones.type == "STORE"):
                    VerificarTipoVariable(Tipo,tipoRobot,instrucciones.numeroLinea)

            elif (instrucciones.type in {"COLLECT","READ"}):

                identificador = instrucciones.identificador
                if (identificador!=None):
                    resultado = TablaLocal.buscarLocal(identificador.value)
 
                    if(resultado!=None):
                        
                        print("Error de contexto en linea",
                            identificador.numeroLinea ,": redeclaracion de\
                             variables.")
                        sys.exit()

                    else:
                        #print("INSERTANDO : ",identificador.value)
                        TablaLocal.insertar(identificador.value,tipoRobot,aux.condicion.type)

      
            instrucciones = instrucciones.sig

        #print("TABLA LOCAL",TablaLocal.tabla)
        ListaTablas += [TablaLocal]    

        aux = aux.sig


#------------------------------------------------------------------------------#

def VerificarInstrucciones(ArbolInstrucciones):

    aux = ArbolInstrucciones
    numActivations = 0
    numDeactivations = 0
    numDeafault = 0

    while (aux!=None):

        if (aux.condicion.type=="activation"):
            numActivations+=1

        elif (aux.condicion.type=="deactivation"):
            numDeactivations+=1

        elif (aux.condicion.type == "default"):
            numDeafault+=1

        
        if(numActivations>1 or numDeactivations>1 or numDeafault>1):
            print("No se puede activar,desactivar o hacer default de un robot mas de una vez.")
            sys.exit()

        # Verificar!!!
        if(aux.condicion.type=="default" and aux.sig!= None):
            print("La instruccion default debe ir al final de las instrucciones.")
            sys.exit()
            
        aux = aux.sig


#------------------------------------------------------------------------------#

def VerificarExpresionBinaria(exprBin,TablaSimbolos):

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

    # print("TIPO",Raiz.type,Raiz.op)
    if (Raiz != None):

        if (Raiz.type != "EXPRESION_BINARIA"):

            if (Raiz.type == "OPERADOR_UNARIO"):

                operador = Raiz.op

                if(operador == "-"):
                    if(VerificarExpresionBinaria(Raiz.value,TablaSimbolos)!= "int"):

                        print("Error de contexto: Hay un error de tipos en la linea",Raiz.numeroLinea,".")
                        sys.exit()

                    else:
                        return "int"

                elif(operador == "~"):
                    if (VerificarExpresionBinaria(Raiz.value,TablaSimbolos)!= "bool"):
                        print("Error de contexto: Hay un error de tipos en la linea",Raiz.numeroLinea,".")
                        sys.exit()
                        
                    else:
                        return "bool"

            else:

                if (Raiz.type in {"ident","me"}):

                    #print("Error",Raiz.value)

                    if(esListaComportamiento==1):

                        Resultado = VerificarVariableDeclarada(Raiz,TablaSimbolos)
                        #print("RESULTADO",Resultado,Raiz.value)
                        if (Resultado[1]=="robot"):

                            print("Error de contexto en linea",Raiz.numeroLinea ,
                                ": No se deben usar variables bot.")
                            sys.exit()

                        # else:
                        #     return Resultado[0]

                    else:
                            
                        Resultado = VerificarVariableDeclaradaE(Raiz,TablaSimbolos)
                        if (Resultado[1]!="robot"):

                            print("Error de contexto en linea",Raiz.numeroLinea ,
                                ": La variable no ha sido declarada.")

                            sys.exit()
                        

                    return Resultado[0]

                else:

                    #print("RESULTADO 2:",Raiz.type)
                    return Raiz.type

        elif(Raiz.type == "EXPRESION_BINARIA"):

            if (Raiz.op in {"-","*","/","%","<",">","/=","=","<=",">=","+"}) :

                if (Raiz.op in {"-","*","/","%","+"}):

                    if (VerificarExpresionBinaria(Raiz.left,TablaSimbolos) != "int" \
                        or VerificarExpresionBinaria(Raiz.right,TablaSimbolos) != "int"):
                        print("Error de contexto: Hay un error de tipos en la linea",Raiz.numeroLinea,".")
                        sys.exit()

                    else: 
                        return "int"

                elif (Raiz.op in {"=","/="}):

                    # if (VerificarExpresionBinaria(Raiz.left,TablaSimbolos) not in {"int","char"} \
                    #     or VerificarExpresionBinaria(Raiz.right,TablaSimbolos) not in {"int","char"}):

                    #     print("Error de tipos en la linea",Raiz.linea)
                    #     sys.exit()

                    # else:

                    #     return "bool"
                    Izq = VerificarExpresionBinaria(Raiz.left,TablaSimbolos)
                    Der = VerificarExpresionBinaria(Raiz.right,TablaSimbolos)

                    if ( Izq != Der ):

                        print("Error de contexto: Hay un error de tipos en la linea",Raiz.numeroLinea,".")
                        sys.exit()

                    else:

                        return "bool"

                else:

                    if (VerificarExpresionBinaria(Raiz.left,TablaSimbolos) != "int" \
                        or VerificarExpresionBinaria(Raiz.right,TablaSimbolos) != "int"):
                        print("Error de contexto: Hay un error de tipos en la linea",Raiz.numeroLinea,".")
                        sys.exit()

                    else: 
                        return "bool"


            elif (Raiz.op in {"/\\","\\/"}):

                if (VerificarExpresionBinaria(Raiz.left,TablaSimbolos) != "bool" \
                    or VerificarExpresionBinaria(Raiz.right,TablaSimbolos) != "bool"):
                    print("Error de contexto: Hay un error de tipos en la linea",Raiz.numeroLinea,".")
                    # print(VerificarExpresionBinaria(Raiz.left))
                    # print(VerificarExpresionBinaria(Raiz.right))
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
    ''' inicio :  TkCreate INICIO_LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd
                | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd '''


    global scopeActual
    if (t[1] == "execute"):
        t[0] = RaizAST(None,Execute(t[2]),Ultimo)

    elif (t[1] == "create"):
        #print("1create")
        #t[0] = TablaSimbolos
        scopeActual = scopeActual.scopeAnterior
        t[0] = RaizAST(Create(t[2]),Execute(t[4]),Ultimo)



def p_inicioDeclaraciones(t):

    '''INICIO_LISTA_DECLARACIONES : LISTA_DECLARACIONES '''

    global esListaComportamiento
    global scopeActual
    global Ultimo

    Arbol = t[1]
    # Se crea la tabla de simbolos
    aux = Arbol

    # print("Lista COMPORTAMIENTO",aux.condicion.type)
    # if (aux.sig!=None):
    #     print("Lista COMPORTAMIENTO SIGUIENTE",aux.sig.condicion.type)


    while (aux!= None):
        
        CrearTablaSimbolos(aux.identificadores,aux.tipoRobot)
        #print("Soy la tabla",Ultimo.tabla)
        # if (Ultimo.padre!= None):
        #     print("Soy el padre de la tabla",Ultimo.padre.tabla)


        esListaComportamiento  = 1

        if (aux.listaComportamiento != None):
            #print("LISTA COMPORTAMIENTO",aux.listaComportamiento)
            # Se verifica la condicion de la lista de declaraciones 
            #print(Ultimo.tabla) 
            VerificarCondicionListaDeclaraciones(aux.listaComportamiento,Ultimo)
            #Se verifican si los tipos de las instrucciones de la lista de 
            # son correctos declaraciones
            Ultimo.hijos = VerificarInstruccionesListaDeclaraciones(aux.listaComportamiento,aux.tipoRobot,Ultimo)
            VerificarInstrucciones(aux.listaComportamiento)

        aux = aux.sig

    esListaComportamiento  = 0

    t[0] = Inicio_Declaracion(Ultimo,scopeActual,t[1])
    scopeActual = t[0]
    Ultimo = None

#------------------------------------------------------------------------------#

# def p_openScope(t):
#     '''OPEN_SCOPE : '''

#     global Top
#     global Ultimo
#     global Pila
#     global esListaComportamiento 
#     #print("prendo")
#     esListaComportamiento  = 1
#     Top = TopeDeTablaSimbolos(Ultimo)
#     Ultimo = Top
#     # Empilo Top
#     Pila.append(Top)


#------------------------------------------------------------------------------#

# def p_closeScope(t):
#     '''CLOSE_SCOPE : '''
#     global Ultimo
#     global Top
#     global Pila
#     aux = Ultimo
#     while (aux!= None):

#         if(aux.type!="top"):
#             print(aux.tabla)
#         else:
#             print("Estoy en el top")
#         aux = aux.padre
#     Ultimo =  Top.padre
#     # Desempilo top
#     Pila.pop()

#     # Asigno top al tope de la pila
#     if (len(Pila)==0):
#         Top = None
#     else:
#         Top = Pila[-1]


#------------------------------------------------------------------------------#

# def p_empty(t):
#     '''empty : '''
#     pass
#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir las declaraciones de robots.
def p_listaDeclaraciones(t):
    ''' LISTA_DECLARACIONES : LISTA_DECLARACIONES LISTA_DECLARACIONES
                            | TkInt TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd 
                            | TkInt TkBot LISTA_IDENT TkEnd 
                            | TkBool TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd
                            | TkBool TkBot LISTA_IDENT TkEnd  
                            | TkChar TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd
                            | TkChar TkBot LISTA_IDENT TkEnd '''

    #print("Lista declaraciones")
    if(t[1] in {"int","bool","char"}):

        if (t[4] == "end"):
            t[0] = Declaraciones(t[1],t[3],None)
        else:
            t[0] = Declaraciones(t[1],t[3],t[4])

            # aux=t[4]
            # print("Lista COMPORTAMIENTO",aux.condicion.type)
            # if (aux.sig!=None):
            #     print("Lista COMPORTAMIENTO SIGUIENTE",aux.sig.condicion.type)

        # # Se crea la tabla de simbolos
        # CrearTablaSimbolos(t[3],t[1])


        # Si se tiene una lista de comportamientos entonces se verifica
        # if (t[4] != "end"):
        #     Arbol = t[5]

        #     # Se verifica la condicion de la lista de declaraciones  
        #     VerificarCondicionListaDeclaraciones(Arbol)

        #     #Se verifican si los tipos de las instrucciones de la lista de 
        #     # son correctos declaraciones
        #     VerificarInstruccionesListaDeclaraciones(Arbol,t[1])

        #     VerificarInstrucciones(Arbol)
  
        # global esListaComportamiento 
        # esListaComportamiento  = 0
    else:

        t[0] = unirListaEnlazada(t[1],t[2])

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

        t[0] = ListaComportamiento(t[2],t[4],t.lineno(1))

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
    
    #print("IR",t[1])
    if (t[1] == "store"):
        t[0] = Store(t[2],t.lineno(1))

    elif (t[1] == "recieve"):
        t[0] = Recieve()

    elif (t[1] == "collect"):
        t[0] = Collect(t[2])

    elif (t[1] == "drop"):
        t[0] = Drop(t[2])

    elif (t[1] in {"up","down","left","right"}):
        t[0] = Movimiento(t[1],t[2],t.lineno(1))

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

# def p_S(t):
#     ''' S : OPEN_SCOPE TkCreate LISTA_DECLARACIONES
#           | '''

# def p_T(t):
#     '''T : TkExecute INSTRUCCIONES_CONTROLADOR TkEnd '''

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
                                  | TkCreate INICIO_LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd
                                  | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd  '''
   
    global scopeActual
    #print("IC")

    # TablaDeAlcance = UltimaTablaSimbolos
    # tablaSimb = TablaSimbolos(UltimaTablaSimbolos)
    # global UltimaTablaSimbolos
    # UltimaTablaSimbolos = tablaSimb

    if (t[1]=="activate"):
        #UltimaTablaSimbolos = TablaDeAlcance 
        #print("activate")
        t[0] = Activate(t[2])
        VerificarVariableDeclaradaE(t[2],scopeActual) 

    elif(t[1]=="advance"):
        #print("advance")
        t[0] = Advance(t[2])
        VerificarVariableDeclaradaE(t[2],scopeActual)

    elif(t[1]=="deactivate"):
        #print("deactivate")
        t[0] = Deactivate(t[2])
        VerificarVariableDeclaradaE(t[2],scopeActual)

    elif (t[1]=="if" and t[5] == "end"):
        t[0] = Condicional(t[2],t[4],None)
        VerificarGuardaEstructuraControl(t[2],scopeActual)

    elif (t[1]=="if" and t[5] == "else"):
        t[0] = Condicional(t[2],t[4],t[7])
        VerificarGuardaEstructuraControl(t[2],scopeActual)

    elif(t[1]=="while"):

        t[0]= While(t[2],t[4])
        VerificarGuardaEstructuraControl(t[2],scopeActual)

    elif(t[1]=="execute"):

        t[0] = RaizAST(None,Execute(t[2]))

    elif (t[1] == "create"):
        #print("create")
        t[0] = RaizAST(Create(t[2]),Execute(t[4]),Ultimo)
        scopeActual = scopeActual.scopeAnterior


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

    # if (esListaComportamiento  != 1):
    #     print("Chequeo tipos")
    #     VerificarExpresionBinaria(t[0],scopeActual)
    # else:
    #     pass

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir la negacion booleana.
def p_negacion_bool(t):
    '''EXPRESION_BIN : TkNegacion EXPRESION_BIN %prec UMNEGACION'''
    t[0] = OperadorUnario(t[1],t[2],t.lineno(1))
    # if( VerificarExpresionBinaria(t[2],scopeActual)!= "bool"):
    #     #print("Error de tipos BOOL")
    #     sys.exit()

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para el operador menos unario.
def p_expression_uminus(t):
    'EXPRESION_BIN : TkResta EXPRESION_BIN %prec UMINUS'
    t[0] = OperadorUnario(t[1],t[2],t.lineno(1))
    # if( VerificarExpresionBinaria(t[2],scopeActual)!= "int"):
    #     print("Error de tipos INT")
    #     sys.exit()

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir la parentizacion.
def p_expression_group(t):
    'EXPRESION_BIN : TkParAbre EXPRESION_BIN TkParCierra'
    t[0] = t[2]

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar el valor de un numero.
def p_expression_number(t):
    'EXPRESION_BIN : TkNum'
    t[0] = Number(t[1],t.lineno(1))

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar un valor booleano 
# (True o False)
def p_expression_TrueFalse(t):
    '''EXPRESION_BIN : TkTrue
                     | TkFalse '''
    t[0] = Booleano(t[1],t.lineno(1))

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
    t[0] = VariableMe(t[1],t.lineno(1))

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para almacenar un caracter.
def p_expression_caracter(t):
    'EXPRESION_BIN : TkCaracter'
    t[0] = Caracter(t[1],t.lineno(1))

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para detectar e imprimir errores sintacticos.
def p_error(t):
    if(t != None):
        print("Error sintactico " + str(t.value) + " en linea " + str(t.lineno))
    else:
        print("Error sintactico.")

    sys.exit()

#------------------------------------------------------------------------------#