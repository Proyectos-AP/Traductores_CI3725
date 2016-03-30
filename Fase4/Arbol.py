'''
*
* Universidad Simón Bolívar
* Departamento de Computación y Tecnología de la Información
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: Arbol.py
*
* Nombres:
*     Alejandra Cordero / Carnet: 12-10645
*     Pablo Maldonado   / Carnet: 12-10561
*
* Descripción: Definición de la clase Árbol.
*
* Última modificación: 30/03/2016
*
'''
#------------------------------------------------------------------------------#
#                            IMPORTE DE MÓDULOS                                #
#------------------------------------------------------------------------------#

from TablaSimbolos import *
import sys

#------------------------------------------------------------------------------#
#                        DEFINICIÓN DE LA CLASE ÁRBOL                          #
#------------------------------------------------------------------------------#

class Expr: 
    '''
      * Descripción:
    '''

    ScopeActual = None  # 
    ultimo = None       #
    Matriz = {}         #

    def imprimirInstrucciones(self,numeroTabs):
        '''
        * Descripción de la función: Imprime las instrucciones del árbol de 
          instrucciones.
        * Variables de entrada:
            - numeroTabs: Número de tabulaciones que tendrán las impresiones.
        * Variables de salida: Ninguna.
        '''
        aux = self

        if(aux.sig != None):
            espacio = "   " * numeroTabs
            print(espacio + "SECUENCIACION")

        while (aux!= None):
            if (aux.type in {"ACTIVATE","DEACTIVATE","ADVANCE"}):
                aux.imprimirInstruccionesSimples(numeroTabs)
            elif (aux.type in {"ITERACION INDETERMINADA","CONDICIONAL"}):
                if (aux.type == "ITERACION INDETERMINADA"):
                    aux.imprimirWhile(numeroTabs)
                elif (aux.type == "CONDICIONAL"):
                    aux.imprimirCondicional(numeroTabs)
            else:
                aux.imprimirAST(numeroTabs)
            aux = aux.sig

    def imprimirInstruccionesSimples(self,numeroTabs):
        '''
        * Descripción de la función: Esta funcion imprime el conjunto de 
        instrucciones que son de la forma INSTRUCCION LISTA_DE_IDENTIFICADORES, 
        es decir, ACTIVATE,DEACTIVATE,ADVANCE.
        * Variables de entrada:
            - numeroTabs: Numero de tabulaciones que tendran las impresiones.
        * Variables de salida: Ninguna
        '''
        espacio = "   "*numeroTabs

        # Se imprime el tipo de la instrucción:
        print(espacio + self.type)
        # Se imprimen las identificadores de las instrucciones:
        numeroTabs += 1
        espacio = "   " * numeroTabs
        aux = self.Identificadores

        while (aux != None):
            print(espacio + "- var:",aux.value)
            aux = aux.sig

    def imprimirExpresionesBinarias(self,numeroTabs):
        '''
        * Descripción de la función: Esta funcion imprime el arbol de 
        expresiones binarias en preorder.
        * Variables de entrada:
            - numeroTabs: Numero de tabulaciones que tendran las impresiones.
        * Variables de salida: Ninguna
        '''
        numeroTabs += 1
        espacio = "   " * numeroTabs
        if (self != None):
            if (self.type == "EXPRESION_BINARIA"):
                print(espacio + "-operacion: ",self.op)

                if (self.left.type in {"EXPRESION_BINARIA","OPERADOR_UNARIO"}):
                    operadorIzquierdo = self.left.op
      
                else:
                    operadorIzquierdo = self.left.value

                print(espacio + "-operador izquierdo:",operadorIzquierdo)

                if (self.right.type in {"EXPRESION_BINARIA","OPERADOR_UNARIO"}):
                    operadorDerecho = self.right.op

                else:
                    operadorDerecho = self.right.value

                print(espacio + "-operador derecho:",operadorDerecho)

                # Se llama recursivamente la funcion para imprimir:
                if (self.left.type == "EXPRESION_BINARIA"):
                    self.left.imprimirExpresionesBinarias(numeroTabs)
                elif(self.left.type == "OPERADOR_UNARIO"):
                    self.left.value.imprimirExpresionesBinarias(numeroTabs)

                if (self.right.type == "EXPRESION_BINARIA"):
                    self.right.imprimirExpresionesBinarias(numeroTabs)
                elif(self.right.type == "OPERADOR_UNARIO"):
                    self.right.value.imprimirExpresionesBinarias(numeroTabs)

            else:
                print(espacio + "-expresion:",self.value)

    def buscar(self,identificador,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        ultimo = tablaSimbolos
        scope = Expr.ScopeActual
        ident = identificador

        while (scope != None):
            resultado,tablaEncontrada = ultimo.buscar(ident)

            if (resultado != None):
                return resultado,tablaEncontrada
                break

            else:
                scope = scope.scopeAnterior
                if (scope != None):
                    ultimo = scope.padre

    def verificarTipos(self,tipo,elemento):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        mismoTipo = False

        if (tipo == "int" and isinstance(elemento,int) and 
            not(isinstance(elemento,bool))):
            mismoTipo = True
        elif (tipo == "bool" and isinstance(elemento,bool)):
            mismoTipo = True
        elif (tipo == "char" and isinstance(elemento,str) and 
            len(elemento) == 1 or elemento in {"\\n","\\t","\\'"}):
            mismoTipo = True

        return mismoTipo

    def CorrerInstruccionesControlador(self,instrucciones,tabla,ident):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        aux = instrucciones
        while (aux!= None):
            aux.ejecutar(tabla,ident)
            aux = aux.sig

#------------------------------------------------------------------------------#
#                               RAÍZ DEL AST                                   #
#------------------------------------------------------------------------------#

class RaizAST(Expr):

    def __init__(self,ArbolDeclaracion,ArbolInstruccion):
        '''
        * Descripción:
        '''
        self.type = "RaizAST"
        self.arbolDeclaracion = ArbolDeclaracion
        self.arbolInstruccion = ArbolInstruccion
        self.sig = None

    def imprimirAST(self,numeroTabs):
        '''
        * Descripción de la función: Esta funcion se encarga de imprimir la 
        rama de instrucciones del AST.
        * Variables de entrada:
            - numeroTabs: Numero de tabulaciones que tendran las impresiones.
        * Variables de salida: Ninguna.
        '''

        espacio = "   "*numeroTabs
        numeroTabs+=1
        if (self.arbolInstruccion!=None):
            print(espacio+"INICIO PROGRAMA")
            aux = self.arbolInstruccion.Instrucciones
            aux.imprimirInstrucciones(numeroTabs)

    def inicializarTablas(self,tabla):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''
        
        aux = tabla

        while (aux!=None):
            
            for i in aux.tabla:
                aux.tabla[i][2] = 0
                aux.tabla[i][3] = None
                aux.tabla[i][4] = [0,0]

            aux = aux.padre

    def ejecutar(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        if (self.arbolDeclaracion!= None):
            auxDeclaracion = self.arbolDeclaracion.listaDeclaraciones
            auxDeclaracion.actualizarScope()
            self.inicializarTablas(Expr.ultimo)
            
        auxInstrucciones = self.arbolInstruccion.Instrucciones
        
        while (auxInstrucciones!=None):
            auxInstrucciones.ejecutar()
            auxInstrucciones = auxInstrucciones.sig

        ultimo = Expr.ultimo
        while (ultimo!=None):
            ultimo = ultimo.padre
            
        if (self.arbolDeclaracion!= None):
            auxDeclaracion.devolverScope()
    
#------------------------------------------------------------------------------#
#                      RAÍZ DEL ÁRBOL DE DECLARACIONES                         #
#------------------------------------------------------------------------------#

class Create(Expr):
    def __init__(self,listaDeclaraciones):
        '''
        * Descripción:
        '''
        self.type = "CREATE"
        self.listaDeclaraciones = listaDeclaraciones
 
#------------------------------------------------------------------------------#
#                      RAÍZ DEL ÁRBOL DE INSTRUCCIONES                         #
#------------------------------------------------------------------------------#

class Execute(Expr):
    def __init__(self,listaInstrucciones):
        '''
        * Descripción:
        '''
        self.type = "EXECUTE"
        self.Instrucciones = listaInstrucciones
        self.sig = None

#------------------------------------------------------------------------------#
#                         RAÍZ LISTA DE DECLARACIONES                          #
#------------------------------------------------------------------------------#

class Inicio_Declaracion(Expr):

    def __init__(self,ultimo,scopeAnterior,listaDeclaraciones):
        '''
        * Descripción:
        '''
        self.padre = ultimo
        self.scopeAnterior = scopeAnterior
        self.listaDeclaraciones = listaDeclaraciones

    def actualizarScope(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''
        Expr.ScopeActual = self
        Expr.ultimo = self.padre

    def devolverScope(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''
        Expr.ScopeActual = self.scopeAnterior

        if(self.scopeAnterior!=None):
            Expr.ultimo = self.scopeAnterior.padre

        else:
            Expr.ultimo = None
  
#------------------------------------------------------------------------------#
#                         LISTA DE DECLARACIONES                               #
#------------------------------------------------------------------------------#

class Store(Expr):
    ''' Nodo que almacena el apuntador del arbol de expresiones de la 
        instruccion STORE'''
    def __init__(self,listaExpresiones,numeroLinea):
        '''
        * Descripción:
        '''
        self.type = "STORE"
        self.expresiones = listaExpresiones
        self.numeroLinea = numeroLinea
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        tablaPadre = tabla.padre

        if (self.expresiones.type == "me"):

            resultado, tablaEncontrada = self.buscar(VariableRobot,tablaPadre)
            variableParaAlmacenar = resultado[3]

            # La variable me no tiene un valor asociado:
            if (variableParaAlmacenar == None):
                print("Error en la linea",self.expresiones.numeroLinea,
                    ": la variable \'"+self.expresiones.value+
                    "\' no tiene valor asociado.")
                sys.exit()

        else:
            variableParaAlmacenar = self.expresiones.evaluar(VariableRobot,tabla)

        tabla.tabla["me"][3] = variableParaAlmacenar
        tablaPadre.tabla["me"][3] = variableParaAlmacenar
        tablaPadre.tabla[VariableRobot][3] = variableParaAlmacenar

#------------------------------------------------------------------------------#

class Drop(Expr):
    ''' Nodo que almacena el apuntador del árbol de expresiones de la 
        instrucción DROP'''
    def __init__(self,listaExpresiones):
        '''
        * Descripción:
        '''
        self.type = "DROP"
        self.expresiones = listaExpresiones
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        tablaPadre = tabla.padre
        tablaRobot = tablaPadre.tabla[VariableRobot]
        posicionRobot = tablaRobot[4]
        tipoRobot = tablaRobot[0]

        if (self.expresiones.type == "me"):
            # Se debe verificar si el robot tenia un valor asociado o no:
            variableParaAlmacenar = tablaRobot[3]
            if (variableParaAlmacenar == None):
                print("Error: El robot '" + VariableRobot + "' no tiene valor",
                    end="")
                print(" asociado para almacenar en la posición " + 
                    str(tuple(posicionRobot)))
                print("de la Matriz.")
                sys.exit()

        else:
            variableParaAlmacenar = self.expresiones.evaluar(VariableRobot,tabla)

        tipoCorrecto = self.verificarTipos(tipoRobot,variableParaAlmacenar)

        # Se verifica soltado inadecuado:
        if(tipoCorrecto):
            Expr.Matriz[tuple(posicionRobot)] = variableParaAlmacenar

        else:
            print("Error en la línea",self.expresiones.numeroLinea,
                ": soltado inadecuado.")
            sys.exit()

#------------------------------------------------------------------------------#

class Collect(Expr):
    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion COLLECT '''
    def __init__(self,identificador):
        '''
        * Descripción:
        '''
        self.type = "COLLECT"
        self.identificador = identificador
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''
        # Se busca la posición actual del robot:
        tablaPadre = tabla.padre
        posicionRobot = tablaPadre.tabla[VariableRobot][4]
        identificadorPresente = False

        # Se verifica si hay un identificador:
        if (self.identificador != None):
            # Si hay presente un identificador, el tipo de este debe
            # coincidir con el tipo del robot:
            identificadorPresente = True
            variableParaActualizar = self.identificador.value
            tipoVariableParaActualizar = tabla.tabla[variableParaActualizar][0]

        else:
            variableParaActualizar = VariableRobot
            tipoVariableParaActualizar = tablaPadre.tabla[variableParaActualizar][0]

        if (not(tuple(posicionRobot) in Expr.Matriz)):
            print("Error: La posición " + str(tuple(posicionRobot)) + 
                " de la Matriz no tiene valor almacenado para hacer collect.")
            sys.exit()
        else:
            # Se verifica que el tipo del elemento de la matriz coincida 
            # con el tipo de elemento a actualizar (valor robot / variable):
            valorMatriz = Expr.Matriz[tuple(posicionRobot)]
            if (not(self.verificarTipos(tipoVariableParaActualizar,valorMatriz))):
                print("Error: El elemento almacenado en la posición " + 
                    str(tuple(posicionRobot)) + 
                " de la Matriz no corresponde con el tipo del robot '" +
                VariableRobot +"'.")
                sys.exit()
            else:

                if (identificadorPresente):
                    tabla.tabla[variableParaActualizar][3] = valorMatriz

                else:
                    # Se actualiza el valor del robot:
                    tabla.tabla["me"][3] = valorMatriz
                    tablaPadre.tabla["me"][3] = valorMatriz
                    tablaPadre.tabla[VariableRobot][3] = valorMatriz

#------------------------------------------------------------------------------#

class Read(Expr):
    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion READ '''
    def __init__(self,identificador):
        '''
        * Descripción:
        '''
        self.type = "READ"
        self.identificador = identificador
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        entrada = input("Introduzca el valor que desea guardar: ")

        if (self.identificador == None):

            VariableAguardar = "me"

        else:
            VariableAguardar= self.identificador.value
            
        # Se verifica el tipo de la entrada:
        resultado = tabla.buscarLocal(VariableAguardar)
        tipoRobot = resultado[0]

        if(tipoRobot == "int"):

            try:
                assert(int(entrada) or entrada == "0")
                entrada = int(entrada)
            except:
                print("Error: Entrada \'",entrada,
                    "\' inválida para robot de tipo",tipoRobot)
                sys.exit()

        elif(tipoRobot == "char"):

            try:
                assert(len(entrada) == 1 or entrada in {"\\n","\\t","\\'"})

            except:
                print("Error: Entrada \'",entrada,
                    "\' inválida para robot de tipo",tipoRobot)
                sys.exit()

        elif (tipoRobot == "bool"):

            try:
                assert(entrada in {'true','false'})
            except:
                print("Error: Entrada \'",entrada,
                    "\' inválida para robot de tipo",tipoRobot)
                sys.exit()

        # Se modifica el valor de la variable:
        tabla.tabla[VariableAguardar][3] = entrada

        # Si el read no tiene identificadores asociados el valor de la entrada
        # se guarda en la variable me:
        if (self.identificador == None):
            tablaPadre = tabla.padre
            tabla.tabla["me"][3] = entrada
            tablaPadre.tabla[VariableRobot][3] = entrada
            tablaPadre.tabla["me"][3] = entrada
 
#------------------------------------------------------------------------------#

class Recieve(Expr):
    def __init__(self):
        '''
        * Descripción:
        '''
        self.type = "RECIEVE"
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''
        print("Recieve")

#------------------------------------------------------------------------------#
    
class Send(Expr):
    def __init__(self):
        '''
        * Descripción:
        '''
        self.type = "SEND"
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        resultado = tabla.buscarLocal("me")
        valor = resultado[3]
        if (valor == None):
            print("Error: El robot '" + VariableRobot + "' no tiene valor"
                 +  " asociado para imprimir en pantalla.")
            sys.exit()

        tipoVariable = resultado[0]

        if (tipoVariable == "char"):

            if (valor in {"\'\\n\'","\\n"}):
                print()
            elif (valor in {"\'\\t\'","\\t"}):
                print("    ",end="")

            elif (valor in {"\'\\\'\'"}):
                print("'",end = "")

            elif (len(valor) > 1):
                print(str(valor[1]),end = "")

            else:
                print(valor,end = "")

        elif (tipoVariable == "bool"):
            if (valor == True):
                print("true",end = "")
            elif (valor == False):
                print("false",end = "")
            else:
                print(valor,end = "")

        else:
            print(valor,end = "")

#------------------------------------------------------------------------------#

class Movimiento(Expr):
    ''' Nodo que almacena la direccion del movimiento del robot.'''
    def __init__(self,tipo,listaExpresiones,numeroLinea):
        '''
        * Descripción:
        '''
        self.type = tipo
        self.expresiones = listaExpresiones
        self.numeroLinea = numeroLinea
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        if (self.expresiones != None):

            numeroPasos = self.expresiones.evaluar(VariableRobot,tabla)

            if (numeroPasos < 0):
                print("Error: La expresión calculada para realizar el" +
                    "movimiento del robot" + VariableRobot + " no es válida.")
                sys.exit()

        else:
            numeroPasos = 1

        tablaPadre = tabla.padre
        posicionAnteriorRobot = tablaPadre.tabla[VariableRobot][4]

        # Se actualiza la posición del robot:

        if (self.type == "up"):

            tablaPadre.tabla[VariableRobot][4][1] += numeroPasos

        elif (self.type == "down"):

            tablaPadre.tabla[VariableRobot][4][1] -= numeroPasos

        elif (self.type == "left"):

            tablaPadre.tabla[VariableRobot][4][0] -= numeroPasos

        elif (self.type == "right"):

            tablaPadre.tabla[VariableRobot][4][0] += numeroPasos

#------------------------------------------------------------------------------#

class Condicion(Expr):
    ''' Nodo que almacena el tipo de condición de la lista de comportamiento.
    del robot '''
    def __init__(self,type,numeroLinea):
        '''
        * Descripción:
        '''
        self.type = type
        self.numeroLinea = numeroLinea
        self.sig = None

#------------------------------------------------------------------------------#

class ListaComportamiento(Expr):
    ''' Lista de comportamiento del robot.'''
    def __init__(self,condicion,instrucciones,numeroLinea):
        '''
        * Descripción:
        '''
        self.type = "Lista de comportamientos"
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.numeroLinea = numeroLinea
        self.sig = None

#------------------------------------------------------------------------------#

class Declaraciones(Expr):
    ''' Raíz del árbol de las variables declaradas en el programa.'''
    def __init__(self,tipoRobot,identificadores,listaComportamiento):
        '''
        * Descripción:
        '''
        self.type = "DECLARACIONES"
        self.tipoRobot = tipoRobot
        self.identificadores = identificadores
        self.listaComportamiento = listaComportamiento
        self.sig = None

#------------------------------------------------------------------------------#
#                      INSTRUCCIONES DEL CONTROLADOR                           #
#------------------------------------------------------------------------------#

class Activate(Expr):

    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion ACTIVATE '''
    def __init__(self,listaIdentificadores):
        '''
        * Descripción:
        '''
        self.type = "ACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

    def verificarActivacion(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        ident = self.Identificadores
        ultimo = Expr.ultimo

        while (ident!= None):

            resultado,tablaEncontrada = self.buscar(ident.value,ultimo)

            if (resultado[2] == 1):
                print("Error en la línea",ident.numeroLinea,
                    ": activación ilegal del robot \'"+ident.value+"\'.")
                sys.exit()

            else:
                tablaEncontrada.tabla[ident.value][2] = 1

            ident = ident.sig

    def ejecutar(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        ultimo = Expr.ultimo
        tablaLocal =  None
        self.verificarActivacion()
        identificador = self.Identificadores

        while (identificador != None):

            # Se busca la tabla de simbolos asociada a la variable:
            resultado,tablaEncontrada = self.buscar(identificador.value,ultimo)

            ListaComportamiento = tablaEncontrada.instrucciones
            tablaEncontrada.tabla["me"] = resultado

            for i in tablaEncontrada.hijos:
                if (i.tipo == "activation"):
                    tablaLocal = i
                    break

            if (tablaLocal != None):
                tablaLocal.tabla["me"] = resultado

            while (ListaComportamiento != None):

                if (ListaComportamiento.condicion.type == "activation"):
                    instrucciones = ListaComportamiento.instrucciones
                    self.CorrerInstruccionesControlador(instrucciones,tablaLocal,
                                                        identificador.value)
                    break

                ListaComportamiento = ListaComportamiento.sig

            identificador = identificador.sig
        
#------------------------------------------------------------------------------#

class Deactivate(Expr):
    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion DEACTIVATE '''
    def __init__(self,listaIdentificadores):
        '''
        * Descripción:
        '''
        self.type = "DEACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

    def verificarDesactivacion(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        ident = self.Identificadores
        ultimo = Expr.ultimo
        tablaEncontrada = None

        while (ident != None):
            resultado,tablaEncontrada = self.buscar(ident.value,ultimo)

            if (resultado[2] == 0):
                print("Error en la línea",ident.numeroLinea,
                    ": desactivación ilegal del robot \'" + ident.value + "\'.")
                sys.exit()

            else:
                tablaEncontrada.tabla[ident.value][2] = 0

            ident = ident.sig

    def ejecutar(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        ultimo = Expr.ultimo
        tablaLocal =  None
        self.verificarDesactivacion()
        identificador = self.Identificadores

        while (identificador != None):

            # Se busca la tabla de símbolos asociada a la variable:
            resultado,tablaEncontrada = self.buscar(identificador.value,ultimo)

            ListaComportamiento = tablaEncontrada.instrucciones
            tablaEncontrada.tabla["me"] = resultado

            for i in tablaEncontrada.hijos:
                if (i.tipo == "deactivation"):
                    tablaLocal = i
                    break

            if (tablaLocal != None):
                tablaLocal.tabla["me"] = resultado

            while (ListaComportamiento != None):

                if (ListaComportamiento.condicion.type == "deactivation"):

                    instrucciones = ListaComportamiento.instrucciones
                    self.CorrerInstruccionesControlador(instrucciones,tablaLocal,
                                                        identificador.value)
                    break

                ListaComportamiento = ListaComportamiento.sig

            identificador = identificador.sig
        
#------------------------------------------------------------------------------#

class Advance(Expr):
    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion ADVANCE '''
    def __init__(self,listaIdentificadores):
        '''
        * Descripción:
        '''
        self.type = "ADVANCE"
        self.Identificadores = listaIdentificadores

        self.sig = None

    def verificarActivacion(self):
        '''
        * Descripción:
        '''

        ident = self.Identificadores
        ultimo = Expr.ultimo

        while (ident != None):

            resultado,tablaEncontrada = self.buscar(ident.value,ultimo)

            if (resultado[2] == 0):
                print("Error en la línea " + str(ident.numeroLinea) +
                    ": el robot \'"+ident.value+"\' no está activado.")
                sys.exit()

            ident = ident.sig

    def ejecutar(self):
        '''
        * Descripción:
        '''

        ultimo = Expr.ultimo
        tablaLocal =  None
        # Los robots que se avanzarán deben estar activados:
        self.verificarActivacion()
        identificador = self.Identificadores

        while (identificador != None):

            comportamientoEncontrado = 0

            # Se busca la tabla de simbolos asociada a la variable:
            resultado,tablaEncontrada = self.buscar(identificador.value,ultimo)

            ListaComportamiento = tablaEncontrada.instrucciones
            tablaEncontrada.tabla["me"] = resultado
            indiceTablaComportamiento = 0 

            # Se busca un comportamiendo cuya condición (es una expresion)
            # retorne True:
            while (ListaComportamiento!= None):

                if (ListaComportamiento.condicion.type == "EXPRESION_BINARIA"):
                    # Se verifica si se cumple alguna de las condiciones:
                    resultadoExpresion = \
                    ListaComportamiento.condicion.evaluar(identificador.value,
                                                            tablaEncontrada )

                    # La expresion retorna True
                    if (resultadoExpresion):
                        comportamientoEncontrado = 1
                        instrucciones = ListaComportamiento.instrucciones

                        # Se busca la tabla de símbolos de la lista de 
                        # comportamientos:
                        for i in tablaEncontrada.hijos:
                            if (i.tipo == "EXPRESION_BINARIA" and 
                                tablaEncontrada.hijos.index(i) == \
                                indiceTablaComportamiento):
                               tablaLocal = i
                               break
                        break

                ListaComportamiento = ListaComportamiento.sig
                indiceTablaComportamiento = indiceTablaComportamiento + 1

            # Si no se encuentra un comportamiendo cuya condición (es una expresión)
            # retorne True se busca la lista de comportamiento cuya condición
            # sea default:

            if (comportamientoEncontrado != 1):
                ListaComportamiento = tablaEncontrada.instrucciones
                while (ListaComportamiento != None):

                    if (ListaComportamiento.condicion.type == "default"):
                        comportamientoEncontrado = 1
                        instrucciones = ListaComportamiento.instrucciones

                        # Se busca la tabla de simbolos de la lista de 
                        # comportamientos
                        for i in tablaEncontrada.hijos:
                            if (i.tipo == "default"):
                                tablaLocal = i
                                break
                        break
                    ListaComportamiento = ListaComportamiento.sig

            if (comportamientoEncontrado == 0):
                print("Error: El robot \'" + identificador.value +
                    "\' no posee comportamientos para realizar un \'advance\'.")
                sys.exit()

            else:
                # Si existe una tabla de simbolos ligada a la lista de 
                # comportamiento se actualiza la variable me de dicha tabla:
                if (tablaLocal != None):
                    tablaLocal.tabla["me"] = resultado

                # Se corren las instrucciones del controlador:
                self.CorrerInstruccionesControlador(instrucciones,tablaLocal,
                                                    identificador.value)

            identificador = identificador.sig
        
#------------------------------------------------------------------------------#

class While(Expr):
    ''' Raiz del árbol de instrucciones y expresiones de la iteración
         indeterminada '''
    def __init__(self,listaExpresiones,listaInstrucciones):
        '''
        * Descripción:
        '''
        self.type = "ITERACION INDETERMINADA"
        self.expresiones = listaExpresiones
        self.InstruccionesWhile = listaInstrucciones
        self.sig = None

    def imprimirWhile(self,numeroTabs):
        '''
        * Descripción de la función: Esta función se encarga de imprimir
        la instruccion WHILE con su guardia y sus instrucciones.
        * Variables de entrada:
            - numeroTabs: Número de tabulaciones que tendrán las impresiones.
        * Variables de salida: Ninguna.
        '''
        # Se calcula el número de tabs para la instruccion WHILE:
        espacio = "   " * numeroTabs
        numeroTabs += 1

        # Se imprime un WHILE:
        print(espacio+self.type)

        espacio = "   " * numeroTabs
        print(espacio + "-guardia :",self.expresiones.type)

        # Numero de tabs para las expresiones:
        numeroTabsExpr = numeroTabs + 1         
        if(self.expresiones.type == "OPERADOR_UNARIO"):
            expr = self.expresiones.value

            # Se calcula una nueva cantidad de tabs para las expresiones:
            numeroTabs2 = numeroTabs + 1
            espacio2 = "   " * numeroTabs2
            numeroTabsExpr = numeroTabs2

            print(espacio2 + "-operador unario:",self.expresiones.op)
            
        else:
            expr = self.expresiones

        expr.imprimirExpresionesBinarias(numeroTabsExpr)

        # Número de tabs para las instrucciones:
        numeroTabs += 1
        print(espacio + "-instrucciones:")
        self.InstruccionesWhile.imprimirInstrucciones(numeroTabs)

    def ejecutar(self):

        tabla = Expr.ultimo
        resultado = self.expresiones.evaluar(None,tabla)
        if (resultado == True):
            while True:
                aux = self.InstruccionesWhile
                while (aux != None):
                    aux.ejecutar()
                    aux = aux.sig

                resultado = self.expresiones.evaluar(None,tabla)

                if (resultado != True):
                    break

#------------------------------------------------------------------------------#

class Condicional(Expr):
    ''' Raiz del arbol de instrucciones y expresiones del condicional '''
    def __init__(self,listaExpresiones,exito,fracaso):
        '''
        * Descripción:
        '''
        self.type = "CONDICIONAL"
        self.expresionesCondicional = listaExpresiones
        self.exito = exito
        self.fracaso = fracaso
        self.sig = None

    def imprimirCondicional(self,numeroTabs):
        '''
        * Descripción de la función: Esta funcion se encarga de imprimir
        la instruccion IF con su guardia y sus instrucciones.
        * Variables de entrada:
            - numeroTabs: Numero de tabulaciones que tendran las impresiones.
        * Variables de salida: Ninguna
        '''

        # Se calcula el número de tabs para la instruccion IF:
        espacio = "   "*numeroTabs
        print(espacio + self.type)

        # Se calcula el número de tabs para la guardia del IF:
        numeroTabs += 1
        espacio = "   "*numeroTabs

        print(espacio + "-guardia :",self.expresionesCondicional.type)

        # Se calcula el número de tabs para las expresiones:
        numeroTabs2 = numeroTabs + 1
        espacio2 = "   " * numeroTabs2
        numeroTabsExpr = numeroTabs

        if(self.expresionesCondicional.type == "OPERADOR_UNARIO"):

            # Se recalcula el numero de tabs para las expresiones:
            expr = self.expresionesCondicional.value
            numeroTabsExpr = numeroTabs2
            print(espacio2 + "-operador unario:",self.expresionesCondicional.op)

        else:
            expr = self.expresionesCondicional


        expr.imprimirExpresionesBinarias(numeroTabsExpr)
        print(espacio + "-exito:")

        numeroTabs += 1 # Número de tabs para las instrucciones del IF:
        self.exito.imprimirInstrucciones(numeroTabs)

        if(self.fracaso != None):
            print(espacio + "-fracaso:")
            self.fracaso.imprimirInstrucciones(numeroTabs)

    def ejecutar(self):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        tabla = Expr.ultimo
        resultado = self.expresionesCondicional.evaluar(None,tabla)
        aux = None
        if (resultado == True):
            aux = self.exito

        else:
            if (self.fracaso != None):
                aux = self.fracaso

        while (aux != None):
            aux.ejecutar()
            aux = aux.sig

#------------------------------------------------------------------------------#
#                               EXPRESIONES                                    #
#------------------------------------------------------------------------------#

class ExpresionBinaria(Expr):
    ''' Raiz del árbol de las expresiones binarias '''
    def __init__(self,left,op,right,linea):
        '''
        * Descripción:
        '''
        self.type = "EXPRESION_BINARIA"
        self.left = left
        self.right = right
        self.op = op
        self.numeroLinea = linea

    def evaluar(self,VariableRobot,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''
      
        resultadoIzq = self.left.evaluar(VariableRobot,tablaSimbolos)
        resultadoDer = self.right.evaluar(VariableRobot,tablaSimbolos)
        
        if (self.op == "+"):
            return resultadoIzq + resultadoDer

        elif (self.op == "-"):
            return resultadoIzq - resultadoDer

        elif (self.op == "/"):
            if (resultadoDer == 0):
                print("Error en la línea",self.numeroLinea,": división entre 0.")
                sys.exit()
            return resultadoIzq / resultadoDer

        elif (self.op == "*"):
            return resultadoIzq * resultadoDer

        elif (self.op == "%"):
            return resultadoIzq % resultadoDer

        elif (self.op == "<"):
            return resultadoIzq < resultadoDer

        elif (self.op == ">"):
            return resultadoIzq > resultadoDer

        elif (self.op == "/="):
            return resultadoIzq != resultadoDer

        elif (self.op == "="):
            return resultadoIzq == resultadoDer

        elif (self.op == "<="):
            return resultadoIzq <= resultadoDer

        elif (self.op == ">="): 
            return resultadoIzq >= resultadoDer

        elif (self.op == "/\\"):
            return resultadoIzq and resultadoDer

        elif (self.op == "\\/"):
            return resultadoIzq or resultadoDer

#------------------------------------------------------------------------------#

class OperadorUnario(Expr):
    ''' Raiz del arbol de las expresiones unarias '''
    def __init__(self,op,value,numeroLinea):
        '''
        * Descripción:
        '''
        self.type = "OPERADOR_UNARIO"
        self.op = op
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        resultado = self.value.evaluar(VariableRobot,tablaSimbolos)

        if (self.op == "-"):
            return (- resultado)

        elif (self.op == "~"):
            return not(resultado)

#------------------------------------------------------------------------------#

class Number(Expr):
    ''' Nodo que almacena los numeros del programa '''
    def __init__(self,value,numeroLinea):
        '''
        * Descripción:
        '''
        self.type = "int"
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        resultado = self.value
        return int(resultado)

#------------------------------------------------------------------------------#

class Booleano(Expr):
    ''' Nodo que almacena los booleanos del programa (true y false) '''
    def __init__(self,value,numeroLinea):
        '''
        * Descripción:
        '''
        self.type = "bool"
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        resultado = self.value

        if (resultado == "true"):
            return True
        elif (resultado == "false"):
            return False

#------------------------------------------------------------------------------#

class Identificadores(Expr):
    ''' Nodo que almacena los identificadores del programa '''

    def __init__(self,value,linea):
        '''
        * Descripción: Constructor de la clase Identificadores.
        '''
        self.type = "ident"
        self.value = value
        self.numeroLinea = linea
        self.sig = None

    def evaluar(self,VariableRobot,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        result,tabla = self.buscar(self.value,tablaSimbolos)
        tipo = result[0]
        resultado = result[3]

        if (resultado != None):
            if (tipo == "int"):
                return int(resultado)

            elif (tipo == "bool"):

                if (resultado == "true"):
                    return True
                else:
                    return False

            elif (tipo == "char"):
                return resultado

        else:

            # El robot no está activo:
            if (result[1] == "robot" and result[2]!=1):
                print("Error en la línea",self.numeroLinea,": el robot \'" +
                    self.value + "\' no ha sido activado.")
                sys.exit()

            # No hay un valor asociado a la variable:
            else:
                print("Error en la línea",self.numeroLinea,": la variable \'"
                    + self.value + "\' no tiene valor asociado.")
                sys.exit()

#------------------------------------------------------------------------------#

class VariableMe(Expr):
    ''' Nodo que almacena la variable me programa '''
    def __init__(self,value,linea):
        '''
        * Descripción: Constructor de la clase VariableMe
        '''
        self.type = "me"
        self.value = value
        self.numeroLinea = linea
        self.sig = None

    def evaluar(self,VariableRobot,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        result,tabla = self.buscar(VariableRobot,tablaSimbolos)
        tipo = result[0]
        resultado = result[3]
        if (resultado != None):
            if (tipo == "int"):
                return int(resultado)

            elif (tipo == "bool"):

                if (resultado == "true"):
                    return True
                if (resultado == "false"):
                    return False

            elif (tipo == "char"):
                return resultado
        else:
            print("Error en la línea",self.numeroLinea,": la variable \'"
                + self.value + "\' no tiene valor asociado.")
            sys.exit()

#------------------------------------------------------------------------------#

class Caracter(Expr):
    ''' Nodo que almacena los caracteres del programa '''
    def __init__(self,value,numeroLinea):
        '''
        * Descripción: Constructor de la clase Caracter.
        '''
        self.type = "char"
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):
        '''
        * Descripción de la función:
        * Variables de entrada:
        * Variables de salida:
        '''

        resultado = self.value
        return resultado

#------------------------------------------------------------------------------#