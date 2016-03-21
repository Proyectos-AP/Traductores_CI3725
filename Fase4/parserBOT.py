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
* Ultima modificacion: 7/03/2016
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

#------------------------------------------------------------------------------#
#                            VARIABLES GLOBALES                                #
#------------------------------------------------------------------------------#

global scopeActual
global Ultimo
global esListaComportamiento 
esListaComportamiento = 0
Ultimo = None
scopeActual = None

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

def CrearTablaSimbolos(ListaIdentificadores,tipoRobot,instrucciones):

    '''
      * Descripción de la función: Esta funcion dada una lista de identificadores.
                                    y un tipo crea una tabla de simbolos y a su
                                    vez va chequeando si existe una redeclaracion

      * Variables de entrada: 
            - ListaIdentificadores: Lista enlazada de identificadores
            - tipoRobot: Tipo de los valores que almacenaran los identificadores

      * Variables de salida: 
            - Ninguno
    '''

    global Ultimo
    aux = ListaIdentificadores
    Tabla = TablaSimbolos(Ultimo)
    Tabla.instrucciones = instrucciones
    Ultimo = Tabla

    while (aux!=None) :

        redeclaracion, tablaEncontrada = Tabla.buscar(aux.value)

        if (redeclaracion != None):
            print("Error en la linea",aux.numeroLinea,
                ": Redeclaracion de la variable","\'"+str(aux.value))
            sys.exit()
        else:
            Tabla.insertar(aux.value,tipoRobot,"robot")

        aux = aux.sig

    # Inserto 'me' en la tabla
    Tabla.insertar("me",tipoRobot)


#------------------------------------------------------------------------------#

def VerificarVariableDeclarada(NodoVariable,TablaSimbolos):

    '''
      * Descripción de la función: Esta funcion dado un nodo identificadores y 
                                    una tabla de simbolos verifica si el 
                                    identificadores
                                    existe en esa tabla.

      * Variables de entrada: 
            - NodoVariable: Apuntador a la cabecera de la primera lista enlazada
            - TablaSimbolos: Apuntador a la cabecera de la primera lista enlazada.

      * Variables de salida: 
            - Resultado: Si no existe la variable en la tabla de simbolos 
                        entonces "Resultado" sera retornado con el valor None. 
                        Si la variable existe entonces "Resultado" almacenara el
                        tipo de la variable a buscar.
    '''

    aux = NodoVariable
    Resultado = None
    while (aux != None):
        Resultado = TablaSimbolos.buscarLocal(aux.value)

        if Resultado == None:
            print("Error en la linea",aux.numeroLinea,
                ": la variable \'"+str(aux.value)+"\'" + " no ha sido declarada.")
            sys.exit()

        aux = aux.sig

    return Resultado

#------------------------------------------------------------------------------#

def VerificarVariableDeclaradaExecute(NodoVariable,TablaSimbolos):

    '''

      * Descripción de la función: Esta funcion dado un nodo identificadores y 
                                    una tabla de simbolos verifica si el 
                                    identificadores existe en esa tabla 
                                    (Esta funcion se utiliza en las instrucciones 
                                    que se encuentran dentro del Execute).

      * Variables de entrada: 

            - NodoVariable: Estructura que almacena la variable a buscar.
            - TablaSimbolos: Tabla de simbolos en donde se buscara la variable.

      * Variables de salida: 
            - Resultado: Si no existe la variable en la tabla de simbolos 
                        entonces "Resultado" sera retornado con el valor None. 
                        Si la variable existe entonces "Resultado" almacenara el
                        tipo de la variable a buscar.
    '''

    aux = NodoVariable
    Resultado = None
    Tabla = TablaSimbolos

    while (aux!= None):

        while (Tabla!= None):
            
            Resultado,tablaEncontrada = Tabla.padre.buscar(aux.value)

            # if (tablaEncontrada!= None):
            #     print("El valor es:",aux.value)
            #     print("La tabla es:",tablaEncontrada.tabla)
            #     print("El tipo de las instrucciones:",tablaEncontrada.instrucciones.type)
            #     print("La condicion es:",tablaEncontrada.instrucciones.condicion.type)

            if (Resultado == None and Tabla.scopeAnterior==None):
                print("Error en la linea",aux.numeroLinea,
                    ":la variable \'"+str(aux.value)+"\'"+" no ha sido declarada.")
                sys.exit()

            elif(Resultado==None and Tabla.scopeAnterior!=None):
                Tabla = Tabla.scopeAnterior

            elif (Resultado!=None):

                break

        aux = aux.sig
        Tabla = TablaSimbolos

    return Resultado

#------------------------------------------------------------------------------#

def VerificarTipoVariable(tipo,tipoVariableAevaluar,numeroLinea):

    '''

    * Descripción de la función: Esta funcion dado dos tipos verifica si los mismos
                                 son iguales o no.

    * Variables de entrada: 

        - tipo: Tipo de variable a comparar.
        - tipoVariableAevaluar: Tipo de variable a comparar.
        - numeroLinea : Numero de linea de la variable cuyo tipo se va a comparar.

    * Variables de salida: 

        - Ninguno 
    '''

    if (tipoVariableAevaluar!=tipo):
        print("Error : Hay un error de tipos en la linea",numeroLinea,".")
        sys.exit()
    
#------------------------------------------------------------------------------#

def VerificarCondicionListaDeclaraciones(ArbolCondicion,TablaSimbolos):

    '''
      * Descripción de la función: Esta funcion dado un arbol de condicion
                                    verifica la correctitud de las condiciones
                                    que poseen expresiones.

      * Variables de entrada: 
            - ArbolCondicion: Lista enlazada de condiciones.
            - TablaSimbolos: Tabla de simbolos en la que se verificaran las 
                             variable de las expresiones de la condicion.

      * Variables de salida: 
            - Ninguno.
    '''


    aux = ArbolCondicion
    while (aux!=None):

        if (aux.condicion.type not in {"activation","deactivation","default"} ):

            Tipo = VerificarExpresionBinaria(aux.condicion,TablaSimbolos)

            if (Tipo != "bool"):
                print("Error : Hay un error de tipos en la linea",
                    aux.numeroLinea,".")
                sys.exit()

        aux = aux.sig

#------------------------------------------------------------------------------#

def VerificarGuardaEstructuraControl(ArbolExpr,TablaSimbolos):

    '''
      * Descripción de la función: Esta funcion dado un arbol de expresiones
                                    verifica si la misma es de tipo booleana.


      * Variables de entrada: 
            - ArbolExpr: Arbol de expresiones.
            - TablaSimbolos: Tabla de simbolos en la que se verificaran las 
                             variable de las expresiones del arbol de expresiones.

      * Variables de salida: 
            - Ninguno.
    '''

    Tipo = VerificarExpresionBinaria(ArbolExpr,TablaSimbolos)

    if (Tipo != "bool"):
        print("Error : Hay un error de tipos en la linea",
            ArbolExpr.numeroLinea,".")
        sys.exit()

#------------------------------------------------------------------------------#

def VerificarInstruccionesListaDeclaraciones(ArbolInstrucciones,tipoRobot):

    '''
      * Descripción de la función: Esta funcion dado un arbol de instrucciones,un 
                                    tipo y una tabla de simbolos verifica la 
                                    correctitud semantica de las instrucciones
                                    de la lista de declaraciones del lenguaje 
                                    BOT.

      * Variables de entrada: 
            - ArbolInstrucciones: Lista enlazada de instrucciones.
            - tipoRobot: Tipo de variables (tipo del robot).

      * Variables de salida: 
            - ListaTablas: Arreglo de tabla de simbolos.
    '''

    ListaTablas = []
    aux = ArbolInstrucciones

    while (aux!=None):

        instrucciones = aux.instrucciones
        TablaLocal = TablaSimbolos(Ultimo)
        TablaLocal.insertar("me",tipoRobot)
        while (instrucciones!=None):    

            # Se verifican las expresiones de las instrucciones STORE,DROP,
            #  RIGHT, LEFT, UP y DOWN
            if (instrucciones.type in {"STORE","DROP","right","left","up","down"}):

                Tipo = VerificarExpresionBinaria(instrucciones.expresiones,
                                                TablaLocal)

                if (instrucciones.type in {"right","left","up","down"}):

                    if (Tipo!=None):
                        VerificarTipoVariable(Tipo,"int",
                            instrucciones.numeroLinea)

                # El tipo de expresion de la instruccion STORE debe ser
                # igual al tipo del robot.
                elif (instrucciones.type == "STORE"):
                    VerificarTipoVariable(Tipo,tipoRobot,
                        instrucciones.numeroLinea)

            # Se verifican los identificadores de las instrucciones COLLECT 
            # y READ.
            elif (instrucciones.type in {"COLLECT","READ"}):

                identificador = instrucciones.identificador
                if (identificador!=None):
                    resultado = TablaLocal.buscarLocal(identificador.value)
 
                    if(resultado!=None):
                        
                        print("Error en linea",
                            identificador.numeroLinea ,": La variable \'"+
                            str(identificador.value)+"\' ha sido redeclarada.")
                        sys.exit()

                    else:
                        # Se almacenan las nuevas variables a la tabla.
                        TablaLocal.insertar(identificador.value,
                            tipoRobot,aux.condicion.type)

      
            instrucciones = instrucciones.sig

        TablaLocal.tipo = aux.condicion.type

        ListaTablas += [TablaLocal]    

        aux = aux.sig

    return ListaTablas


#------------------------------------------------------------------------------#

def VerificarInstrucciones(ArbolInstrucciones):

    '''
      * Descripción de la función: Funcion que verifia si el numero de 
                                  declaraciones de activation,deactivation y
                                  default son correctas. Ademas chequea si
                                  la declaracion default es la ultima en la
                                  lista enlazada de declaraciones. 

      * Variables de entrada: 
            - ArbolInstrucciones: Lista enlazada de comportamientos.

      * Variables de salida: 
            - ListaTablas: Arreglo de tabla de simbolos.
    '''

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

        # Se verifica si hay mas de una condicion: activation, deactivation o
        # default.
        if(numActivations>1 or numDeactivations>1 or numDeafault>1):
            print("Error en linea",aux.numeroLinea,
                ": No se puede utilizar el comportamiento activation,",
                "deactivation o default mas de una vez.")
            sys.exit()

        # Se verifica si default es la ultima condicion
        if(aux.condicion.type=="default" and aux.sig!= None):
            print("Error en linea",aux.numeroLinea,
                ": El comportamiento default debe ir al final de los", 
                "comportamientos.")
            sys.exit()
            
        aux = aux.sig


#------------------------------------------------------------------------------#

def VerificarExpresionBinaria(exprBin,TablaSimbolos):

    '''
      * Descripción de la función: Esta funcion verifica la correctitud
                                    semantica de un arbol de expresiones.

      * Variables de entrada: 
            - exprBin: Arbol de expresiones.
            - TablaSimbolos: Tabla de simbolos que sera utilizada para chequear 
                              la declaracion de variables del arbol de expresiones.

      * Variables de salida: 

            - Se retorna el tipo de expresion que se esta verificando(int o bool).
    '''

    Raiz = exprBin


    if (Raiz != None):

        if (Raiz.type != "EXPRESION_BINARIA"):

            # Se chequean las expresiones unarias
            if (Raiz.type == "OPERADOR_UNARIO"):

                operador = Raiz.op

                # Expresion unaria de tipo int
                if(operador == "-"):
                    if(VerificarExpresionBinaria(Raiz.value,TablaSimbolos)!= "int"):

                        print("Error : Hay un error de tipos en la linea",
                            Raiz.numeroLinea,".")
                        sys.exit()

                    else:
                        return "int"

                # Expresion unaria de tipo bool
                elif(operador == "~"):
                    if (VerificarExpresionBinaria(Raiz.value,TablaSimbolos)!= "bool"):
                        print("Error : Hay un error de tipos en la linea",
                            Raiz.numeroLinea,".")
                        sys.exit()
                        
                    else:
                        return "bool"

            else:

                if (Raiz.type in {"ident","me"}):

                    if(esListaComportamiento==1):
                        # Se verifica si la variable fue declarada
                        Resultado = VerificarVariableDeclarada(Raiz,TablaSimbolos)

                        if (Resultado[1]=="robot"):

                            print("Error en linea",Raiz.numeroLinea ,
                                ": No se deben usar variables bot en este alcance.")
                            sys.exit()

                    else:
                        # Se verifica si la variable fue declarada 
                        Resultado = VerificarVariableDeclaradaExecute(Raiz,TablaSimbolos)
                        if (Resultado[1]!="robot"):

                            print("Error en linea",Raiz.numeroLinea ,
                                ": La variable no ha sido declarada.")

                            sys.exit()
                        

                    return Resultado[0]

                else:

                    return Raiz.type

        elif(Raiz.type == "EXPRESION_BINARIA"):

            if (Raiz.op in {"-","*","/","%","<",">","/=","=","<=",">=","+"}) :

                if (Raiz.op in {"-","*","/","%","+"}):
                    # Chequeo de expresiones aritmeticas
                    if (VerificarExpresionBinaria(Raiz.left,TablaSimbolos) != "int" \
                        or VerificarExpresionBinaria(Raiz.right,TablaSimbolos) != "int"):
                        print("Error : Hay un error de tipos en la linea",
                            Raiz.numeroLinea,".")
                        sys.exit()

                    else: 
                        return "int"
                # Chequeo de comparaciones
                elif (Raiz.op in {"=","/="}):

                    Izq = VerificarExpresionBinaria(Raiz.left,TablaSimbolos)
                    Der = VerificarExpresionBinaria(Raiz.right,TablaSimbolos)

                    if ( Izq != Der ):

                        print("Error : Hay un error de tipos en la linea",
                            Raiz.numeroLinea,".")
                        sys.exit()

                    else:

                        return "bool"

                else:

                    if (VerificarExpresionBinaria(Raiz.left,TablaSimbolos) != "int" \
                        or VerificarExpresionBinaria(Raiz.right,TablaSimbolos) != "int"):
                        print("Error : Hay un error de tipos en la linea",
                            Raiz.numeroLinea,".")
                        sys.exit()

                    else: 
                        return "bool"

            # Chequeo de expresiones booleanas
            elif (Raiz.op in {"/\\","\\/"}):

                if (VerificarExpresionBinaria(Raiz.left,TablaSimbolos) != "bool" \
                    or VerificarExpresionBinaria(Raiz.right,TablaSimbolos) != "bool"):
                    print("Error : Hay un error de tipos en la linea",
                        Raiz.numeroLinea,".")
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
        t[0] = RaizAST(None,Execute(t[2]))

    elif (t[1] == "create"):
        scopeActual = scopeActual.scopeAnterior
        t[0] = RaizAST(Create(t[2]),Execute(t[4]))


#------------------------------------------------------------------------------#

def p_inicioDeclaraciones(t):

    '''INICIO_LISTA_DECLARACIONES : LISTA_DECLARACIONES '''

    global esListaComportamiento
    global scopeActual
    global Ultimo

    Arbol = t[1]
    # Se crea la tabla de simbolos
    aux = Arbol
    # Se itera por todas las listas de declaraciones
    while (aux!= None):
        
        CrearTablaSimbolos(aux.identificadores,aux.tipoRobot,aux.listaComportamiento)
        esListaComportamiento  = 1

        if (aux.listaComportamiento != None):
            VerificarCondicionListaDeclaraciones(aux.listaComportamiento,Ultimo)
            Ultimo.hijos = \
            VerificarInstruccionesListaDeclaraciones(aux.listaComportamiento,aux.tipoRobot)
            VerificarInstrucciones(aux.listaComportamiento)

        aux = aux.sig

    esListaComportamiento  = 0

    t[0] = Inicio_Declaracion(Ultimo,scopeActual,t[1])
    scopeActual = t[0]
    Ultimo = None
    
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


    if(t[1] in {"int","bool","char"}):

        if (t[4] == "end"):
            t[0] = Declaraciones(t[1],t[3],None)
        else:
            t[0] = Declaraciones(t[1],t[3],t[4])

    else:

        t[0] = unirListaEnlazada(t[1],t[2])

#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para la secuenciacion de identificadores 
# en una declaracion de robot.
def  p_listaIdent(t):
    ''' LISTA_IDENT : LISTA_IDENT TkComa LISTA_IDENT'''

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
        t[0] = Condicion(t[1],t.lineno(1))
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

    if (t[1]=="activate"):

        t[0] = Activate(t[2])
        VerificarVariableDeclaradaExecute(t[2],scopeActual) 

    elif(t[1]=="advance"):
 
        t[0] = Advance(t[2])
        VerificarVariableDeclaradaExecute(t[2],scopeActual)

    elif(t[1]=="deactivate"):

        t[0] = Deactivate(t[2])
        VerificarVariableDeclaradaExecute(t[2],scopeActual)

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

        t[0] = RaizAST(Create(t[2]),Execute(t[4]))
        scopeActual = scopeActual.scopeAnterior


    else:

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


#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para definir la negacion booleana.
def p_negacion_bool(t):
    '''EXPRESION_BIN : TkNegacion EXPRESION_BIN %prec UMNEGACION'''
    t[0] = OperadorUnario(t[1],t[2],t.lineno(1))


#------------------------------------------------------------------------------#

# Descripcion de la funcion: Regla para el operador menos unario.
def p_expression_uminus(t):
    'EXPRESION_BIN : TkResta EXPRESION_BIN %prec UMINUS'
    t[0] = OperadorUnario(t[1],t[2],t.lineno(1))
 

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