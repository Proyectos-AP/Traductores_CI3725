'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: Arbol.py
*
* Nombres:
*     Alejandra Cordero / Carnet: 12-10645
*     Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion: Definicion de la clase Arbol.
*
*
* Ultima modificacion: 12/02/2016
*
'''
#------------------------------------------------------------------------------#
#                            IMPORTE DE MODULOS                                #
#------------------------------------------------------------------------------#

from TablaSimbolos import *
import sys

#------------------------------------------------------------------------------#
#                        DEFINICION DE LA CLASE ARBOL                          #
#------------------------------------------------------------------------------#

class Expr: 

    ScopeActual = None
    ultimo = None
    Matriz = {}

    def imprimirInstrucciones(self,numeroTabs):
        '''
        * Descripción de la función: Esta funcion imprime las instrucciones del
        arbol de instrucciones.
        * Variables de entrada:
            - numeroTabs: Numero de tabulaciones que tendran las impresiones.
        * Variables de salida: Ninguna
        '''
        aux = self

        if(aux.sig != None):
            espacio = "   "*numeroTabs
            print(espacio+"SECUENCIACION")

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
            aux=aux.sig


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

        # Se imprime el tipo de la instruccion.
        print(espacio+self.type)
        # Se imprimen las identificadores de las instrucciones
        numeroTabs+=1
        espacio = "   "*numeroTabs
        aux = self.Identificadores

        while (aux != None):
            print(espacio+"- var:",aux.value)
            aux = aux.sig


    def imprimirExpresionesBinarias(self,numeroTabs):
        '''
        * Descripción de la función: Esta funcion imprime el arbol de 
        expresiones binarias en preorder.
        * Variables de entrada:
            - numeroTabs: Numero de tabulaciones que tendran las impresiones.
        * Variables de salida: Ninguna
        '''
        numeroTabs+=1
        espacio = "   "*numeroTabs
        if (self != None):
            if (self.type=="EXPRESION_BINARIA"):
                print(espacio+"-operacion: ",self.op)

                if (self.left.type in {"EXPRESION_BINARIA","OPERADOR_UNARIO"}):
                    operadorIzquierdo=self.left.op
      
                else:
                    operadorIzquierdo=self.left.value

                print(espacio+"-operador izquierdo:",operadorIzquierdo)

                if (self.right.type in {"EXPRESION_BINARIA","OPERADOR_UNARIO"}):
                    operadorDerecho=self.right.op

                else:
                    operadorDerecho=self.right.value

                print(espacio+"-operador derecho:",operadorDerecho)

                # Se llama recursivamente la funcion para imprimir
                if (self.left.type=="EXPRESION_BINARIA"):
                    self.left.imprimirExpresionesBinarias(numeroTabs)
                elif(self.left.type=="OPERADOR_UNARIO"):
                    self.left.value.imprimirExpresionesBinarias(numeroTabs)

                if (self.right.type=="EXPRESION_BINARIA"):
                    self.right.imprimirExpresionesBinarias(numeroTabs)
                elif(self.right.type=="OPERADOR_UNARIO"):
                    self.right.value.imprimirExpresionesBinarias(numeroTabs)

            else:
                print(espacio+"-expresion:",self.value)

    def buscar(self,identificador):

        ultimo = Expr.ultimo
        scope = Expr.ScopeActual
        ident = identificador

        # while (ident!= None):

        #     while (scope!= None):
        #         print("VALOR A BUSCAR",ident.value)
        #         resultado,tablaEncontrada = ultimo.buscar(ident.value)

        #         if (resultado!=None):
        #             return resultado,tablaEncontrada
        #             break

        #         else:
        #             scope = scope.scopeAnterior
        #             ultimo = scope.padre

        #     ident = ident.sig

        while (scope!= None):
            resultado,tablaEncontrada = ultimo.buscar(ident)

            if (resultado!=None):
                return resultado,tablaEncontrada
                break

            else:
                scope = scope.scopeAnterior
                if (scope != None):
                    ultimo = scope.padre

    def busqueda(self,tablaSimbolos):

        ultimo = tablaSimbolos
        scope = Expr.ScopeActual
        ident = self
        while (ident!= None):

            while (scope!= None):
                resultado,tablaEncontrada = ultimo.buscar(ident.value)

                if (resultado!=None):
                    return resultado,tablaEncontrada
                    break

                else:
                    scope = scope.scopeAnterior

                    if (scope!=None):
                        ultimo = scope.padre

            ident = ident.sig

    def verificarTipos(self,tipo,elemento):

        mismoTipo = False

        if (tipo == "int" and  isinstance(elemento,int)):
            mismoTipo = True
        elif (tipo == "bool" and isinstance(elemento,bool)):
            mismoTipo = True
        elif (tipo == "char" and isinstance(elemento,str) and len(elemento) == 1):
            mismoTipo = True

        return mismoTipo



#------------------------------------------------------------------------------#
#                               RAIZ DEL AST                                   #
#------------------------------------------------------------------------------#

class RaizAST(Expr):

    def __init__(self,ArbolDeclaracion,ArbolInstruccion):
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

    def ejecutar(self):

        if (self.arbolDeclaracion!= None):
            auxDeclaracion = self.arbolDeclaracion.listaDeclaraciones
            auxDeclaracion.actualizarScope()
            
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
#                      RAIZ DEL ARBOL DE DECLARACIONES                         #
#------------------------------------------------------------------------------#

class Create(Expr):
    def __init__(self,listaDeclaraciones):
        self.type = "CREATE"
        self.listaDeclaraciones = listaDeclaraciones
 
#------------------------------------------------------------------------------#
#                      RAIZ DEL ARBOL DE INSTRUCCIONES                         #
#------------------------------------------------------------------------------#

class Execute(Expr):
    def __init__(self,listaInstrucciones):
        self.type = "EXECUTE"
        self.Instrucciones = listaInstrucciones
        self.sig = None

#------------------------------------------------------------------------------#
#                         RAIZ LISTA DE DECLARACIONES                          #
#------------------------------------------------------------------------------#

class Inicio_Declaracion(Expr):

    def __init__(self,ultimo,scopeAnterior,listaDeclaraciones):
        self.padre = ultimo
        self.scopeAnterior = scopeAnterior
        self.listaDeclaraciones = listaDeclaraciones

    def actualizarScope(self):
        Expr.ScopeActual = self
        Expr.ultimo = self.padre

    def devolverScope(self):
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
        self.type = "STORE"
        self.expresiones = listaExpresiones
        self.numeroLinea = numeroLinea
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):

        if (self.expresiones.type in {"EXPRESION_BINARIA","OPERADOR_UNARIO"}):

            variableParaAlmacenar = self.expresiones.evaluar(VariableRobot,tabla)

        else:
            variableParaAlmacenar = self.expresiones.value
            

        # print("Voy a guardar el valor",variableParaAlmacenar,"en la tabla",tabla.tabla,"con el robot",VariableRobot)
        tabla.tabla["me"][3] = variableParaAlmacenar
        tablaPadre = tabla.padre
        tablaPadre.tabla["me"][3] = variableParaAlmacenar
        tablaPadre.tabla[VariableRobot][3] = variableParaAlmacenar
        # print("Tabla guardad hijo",tabla.tabla)
        # print("Tabla guardada papa",tablaPadre.tabla)

#------------------------------------------------------------------------------#

class Drop(Expr):
    ''' Nodo que almacena el apuntador del arbol de expresiones de la 
        instruccion DROP'''
    def __init__(self,listaExpresiones):
        self.type = "DROP"
        self.expresiones = listaExpresiones
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):

        tablaPadre = tabla.padre
        posicionRobot = tablaPadre.tabla[VariableRobot][4]

        if (self.expresiones.type in {"EXPRESION_BINARIA","OPERADOR_UNARIO"}):

            variableParaAlmacenar = self.expresiones.evaluar(VariableRobot,tabla)


        else:
            variableParaAlmacenar = self.expresiones.value


            if (variableParaAlmacenar == "me"):

                # Se debe verificar si el robot tenia un valor asociado o no:

                variableParaAlmacenar = tablaPadre.tabla[VariableRobot][3]

                if (variableParaAlmacenar == None):
                    print("Error: El robot '" + VariableRobot + "' no tiene valor",
                        end="")
                    print(" asociado para almacenar en la posición " + 
                        str(tuple(posicionRobot)))
                    print("de la Matriz.")
                    sys.exit()

        Expr.Matriz[tuple(posicionRobot)] = variableParaAlmacenar
        #print("El nuevo estado de la matriz es",Expr.Matriz)

        # tabla.tabla["me"][3] = variableParaAlmacenar
        # tablaPadre = tabla.padre
        # tablaPadre.tabla["me"][3] = variableParaAlmacenar
        # tablaPadre.tabla[VariableRobot][3] = variableParaAlmacenar

#------------------------------------------------------------------------------#

class Collect(Expr):
    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion COLLECT '''
    def __init__(self,identificador):
        self.type = "COLLECT"
        self.identificador = identificador
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        # Se busca la posición actual del robot:
        tablaPadre = tabla.padre
        posicionRobot = tablaPadre.tabla[VariableRobot][4]
        identificadorPresente = False

        # Se verifica si hay un identificador:
        if (self.identificador != None):
            # Si hay presente un identificador, el tipo de este debe
            # coincidir con el tipo del robot:
            #print("El identificador es",self.identificador.value)
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
                    #print("La tabla actualizada es",tabla.tabla)
                else:
                    # Se actualiza el valor del robot:
                    tabla.tabla["me"][3] = valorMatriz
                    tablaPadre.tabla["me"][3] = valorMatriz
                    tablaPadre.tabla[VariableRobot][3] = valorMatriz

        #("EL ROBOT ACTUALIZADO ES",tablaPadre.tabla[VariableRobot])

#------------------------------------------------------------------------------#

class Read(Expr):

    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion READ '''
    def __init__(self,identificador):
        self.type = "READ"
        self.identificador = identificador
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):

        entrada = input("Introduzca el valor que desea guardar: ")

        if (self.identificador == None):

            VariableAguardar = "me"

        else:
            VariableAguardar= self.identificador.value
            

        # Se verifica el tipo de la entrada
        resultado = tabla.buscarLocal(VariableAguardar)
        tipoRobot = resultado[0]

        if(tipoRobot == "int"):

            try:
                assert(int(entrada) or entrada == "0")
                entrada = int(entrada)
            except:
                print("Error: Entrada \'",entrada,"\' invalida para robot de tipo",tipoRobot)
                sys.exit()


        elif(tipoRobot == "char"):

            try:
                assert(len(entrada)==1 or entrada in {"\\n","\\t","\\'"})
            except:
                print("Error: Entrada \'",entrada,"\' invalida para robot de tipo",tipoRobot)
                sys.exit()

        elif (tipoRobot == "bool"):

            try:
                assert(entrada in {'true','false'})
            except:
                print("Error: Entrada \'",entrada,"\' invalida para robot de tipo",tipoRobot)
                sys.exit()


        # Se modifica el valor de la variable
        tabla.tabla[VariableAguardar][3] = entrada

        # Si el read no tiene identificadores asociados el valor de la entrada
        # se guarda en la variable me.
        if (self.identificador == None):
            tablaPadre = tabla.padre
            tabla.tabla["me"][3] = entrada
            tablaPadre.tabla[VariableRobot][3] = entrada
            tablaPadre.tabla["me"][3] = entrada
 
#------------------------------------------------------------------------------#

class Recieve(Expr):
    def __init__(self):
        self.type = "RECIEVE"
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        print("Recieve")

#------------------------------------------------------------------------------#
    
class Send(Expr):
    def __init__(self):
        self.type = "SEND"
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):

        resultado = tabla.buscarLocal("me")
        valor = resultado[3]

        if (valor == None):
            print("Error: El robot '" + VariableRobot + "' no tiene valor"
                 +  " asociado para imprimir en pantalla.")
            sys.exit()

        tipoVariable = resultado[0]

        if (tipoVariable == "char"):

            if (valor == "\'\\n\'"):
                print()
            elif (valor == "\'\\t\'"):
                print("    ")

            elif (len(valor)>1):
                print(str(valor[1]),end="")

            else:
                print(valor,end="")
        else:
            print(valor,end="")


#------------------------------------------------------------------------------#

class Movimiento(Expr):
    ''' Nodo que almacena la direccion del movimiento del robot '''
    def __init__(self,tipo,listaExpresiones,numeroLinea):
        self.type = tipo
        self.expresiones = listaExpresiones
        self.numeroLinea = numeroLinea
        self.sig = None

    def ejecutar(self,tabla,VariableRobot):
        #print("Movimiento")

        # Verificar si hay una expresion presente, sino mover uno
        # Actualizar la posicion del robot en su variable 

        # aca hay que verificar que sea una expresion numerica 
        # no se si eso se hacia de antes 

        if (self.expresiones != None):

            if (self.expresiones.type in {"EXPRESION_BINARIA","OPERADOR_UNARIO"}):

                numeroPasos = self.expresiones.evaluar(VariableRobot,tabla)

                if (numeroPasos < 0 or not(isinstance(numeroPasos,int))):
                    print("Error: La expresión calculada para realizar el" +
                        "movimiento del robot" + VariableRobot + " no es válida.")
                    sys.exit()

        else:
            numeroPasos = 1

        # print("RESULTADO MOVIMIENTO",numeroPasos)

        # VariableRobot = identificador.value

        tablaPadre = tabla.padre
        posicionAnteriorRobot = tablaPadre.tabla[VariableRobot][4]

        #print("La posicion anterior del robot es",posicionAnteriorRobot)

        # Se actualiza la posición del robot:

        if (self.type == "up"):

            tablaPadre.tabla[VariableRobot][4][1] += numeroPasos

        elif (self.type == "down"):

            tablaPadre.tabla[VariableRobot][4][1] -= numeroPasos

        elif (self.type == "left"):

            tablaPadre.tabla[VariableRobot][4][0] -= numeroPasos

        elif (self.type == "right"):

            tablaPadre.tabla[VariableRobot][4][0] += numeroPasos

        #print("La nueva posicion del robot es", tablaPadre.tabla[VariableRobot][4])

#------------------------------------------------------------------------------#

class Condicion(Expr):
    ''' Nodo que almacena el tipo de condicion de la lista de comportamiento 
    del robot '''
    def __init__(self,type,numeroLinea):
        self.type = type
        self.numeroLinea = numeroLinea
        self.sig = None

#------------------------------------------------------------------------------#

class ListaComportamiento(Expr):
    ''' Lista de comportamiento del robot'''
    def __init__(self,condicion,instrucciones,numeroLinea):
        self.type = "Lista de comportamientos"
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.numeroLinea = numeroLinea
        self.sig = None

#------------------------------------------------------------------------------#

class Declaraciones(Expr):
    ''' Raiz del arbol de las variables declaradas en el programa '''
    def __init__(self,tipoRobot,identificadores,listaComportamiento):
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
        self.type = "ACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

    def verificarActivacion(self):

        ident = self.Identificadores
        ultimo = Expr.ultimo
        scope = Expr.ScopeActual


        while (ident!= None):

            while (scope!= None):
                resultado,tablaEncontrada = ultimo.buscar(ident.value)

                if (resultado!=None):
                    break

                else:
                    scope = scope.scopeAnterior
                    ultimo = scope.padre

            if (resultado[2] == 1):
                print("Error en la linea",ident.numeroLinea,
                    ": activacion ilegal del robot \'"+ident.value+"\'.")
                sys.exit()

            else:
                tablaEncontrada.tabla[ident.value][2] = 1

            resultado,tablaEncontrada = ultimo.buscar(ident.value)
            ident = ident.sig

    def ejecutar(self):

        ultimo = Expr.ultimo
        tablaLocal =  None
        scope = Expr.ScopeActual
        self.verificarActivacion()
        identificador = self.Identificadores


        while (identificador!=None):

            comportamientoEncontrado = 0

            while (scope!= None):
                resultado, tablaEncontrada = ultimo.buscar(identificador.value)

                if (resultado!=None):
                    break

                else:
                    scope = scope.scopeAnterior
                    ultimo = scope.padre

            ListaComportamiento = tablaEncontrada.instrucciones
            tablaEncontrada.tabla["me"] = resultado

            for i in tablaEncontrada.hijos:
                if (i.tipo == "activation"):
                    tablaLocal = i
                    break

            if (tablaLocal != None):
                tablaLocal.tabla["me"] = resultado

            while (ListaComportamiento!= None):

                if (ListaComportamiento.condicion.type == "activation"):
                    aux = ListaComportamiento.instrucciones
                    comportamientoEncontrado = 1
                    while (aux!= None):
                        aux.ejecutar(tablaLocal,identificador.value)
                        aux = aux.sig

                    break

                ListaComportamiento = ListaComportamiento.sig

            if (comportamientoEncontrado == 0):
                print("Error: Comportamiento activation no encontrado.")
                sys.exit()


            identificador = identificador.sig
        

#------------------------------------------------------------------------------#

class Deactivate(Expr):
    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion DEACTIVATE '''
    def __init__(self,listaIdentificadores):
        self.type = "DEACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

    def verificarDesactivacion(self):

        ident = self.Identificadores
        ultimo = Expr.ultimo
        tablaEncontrada = None

        while (ident!= None):

            resultado,tablaEncontrada = ultimo.buscar(ident.value)

            if (resultado[2] == 0):
                print("Error en la linea",ident.numeroLinea,
                    ": desactivacion ilegal del robot \'"+ident.value+"\'.")
                sys.exit()

            else:
                tablaEncontrada.tabla[ident.value][2] = 0

            resultado,tablaEncontrada = ultimo.buscar(ident.value)
            ident = ident.sig

        return tablaEncontrada

    def ejecutar(self):

        ultimo = Expr.ultimo
        tablaLocal =  None
        scope = Expr.ScopeActual
        self.verificarDesactivacion()
        identificador = self.Identificadores


        while (identificador!=None):

            comportamientoEncontrado = 0

            while (scope!= None):
                resultado, tablaEncontrada = ultimo.buscar(identificador.value)

                if (resultado!=None):
                    break

                else:
                    scope = scope.scopeAnterior
                    ultimo = scope.padre

            ListaComportamiento = tablaEncontrada.instrucciones
            tablaEncontrada.tabla["me"] = resultado

            for i in tablaEncontrada.hijos:
                if (i.tipo == "deactivation"):
                    tablaLocal = i
                    break

            if (tablaLocal != None):
                tablaLocal.tabla["me"] = resultado

            while (ListaComportamiento!= None):

                if (ListaComportamiento.condicion.type == "deactivation"):

                    aux = ListaComportamiento.instrucciones
                    comportamientoEncontrado = 1
                    while (aux!= None):
                        aux.ejecutar(tablaLocal,identificador.value)
                        aux = aux.sig

                    break

                ListaComportamiento = ListaComportamiento.sig

            if (comportamientoEncontrado == 0):
                print("Error: Comportamiento deactivation no encontrado.")
                sys.exit()


            identificador = identificador.sig
        

#------------------------------------------------------------------------------#

class Advance(Expr):
    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion ADVANCE '''
    def __init__(self,listaIdentificadores):
        self.type = "ADVANCE"
        self.Identificadores = listaIdentificadores

        self.sig = None

    def verificarActivacion(self):

        ident = self.Identificadores
        ultimo = Expr.ultimo
        scope = Expr.ScopeActual

        while (ident!= None):

            while (scope!= None):
                resultado,tablaEncontrada = ultimo.buscar(ident.value)

                if (resultado!=None):
                    break

                else:
                    scope = scope.scopeAnterior
                    ultimo = scope.padre

            if (resultado[2] == 0):
                print("Error en la línea " + str(ident.numeroLinea) +
                    ": el robot \'"+ident.value+"\' no está activado.")
                sys.exit()

            resultado,tablaEncontrada = ultimo.buscar(ident.value)
            ident = ident.sig

    def ejecutar(self):

        ultimo = Expr.ultimo
        tablaLocal =  None
        scope = Expr.ScopeActual
        # Los robots que se avanzaran deben estar activados:
        self.verificarActivacion()
        identificador = self.Identificadores


        while (identificador != None):

            while (scope != None):
                resultado, tablaEncontrada = ultimo.buscar(identificador.value)

                if (resultado!=None):
                    break

                else:
                    scope = scope.scopeAnterior
                    ultimo = scope.padre

            ListaComportamiento = tablaEncontrada.instrucciones
            tablaEncontrada.tabla["me"] = resultado
            indiceTablaComportamiento = 0 

            while (ListaComportamiento!= None):

                # Nota: Si no se encuentra ninguna expresión que se cumpla
                # ni comportamiento default, el programa NO dará error.

                if (ListaComportamiento.condicion.type == "EXPRESION_BINARIA"):
                    # Se verifica si se cumple alguna de las condiciones:
                    resultadoExpresion = ListaComportamiento.condicion.evaluar(identificador.value,tablaEncontrada )

                    if (resultadoExpresion):
                        for i in tablaEncontrada.hijos:
                            if (i.tipo == "EXPRESION_BINARIA" and tablaEncontrada.hijos.index(i) == indiceTablaComportamiento):
                               tablaLocal = i
                               break

                        if (tablaLocal != None):
                            tablaLocal.tabla["me"] = resultado

                        aux = ListaComportamiento.instrucciones
                        while (aux!= None):
                            aux.ejecutar(tablaLocal,identificador.value)
                            aux = aux.sig
                        break
                ListaComportamiento = ListaComportamiento.sig
                indiceTablaComportamiento = indiceTablaComportamiento + 1


            ListaComportamiento = tablaEncontrada.instrucciones
            while (ListaComportamiento!=None):
  
                # En caso de que no hayan, se busca el comportamiento default.
                if (ListaComportamiento.condicion.type == "default"):

                        for i in tablaEncontrada.hijos:
                            if (i.tipo == "default"):
                                tablaLocal = i
                                break

                        if (tablaLocal != None):
                            tablaLocal.tabla["me"] = resultado


                        aux = ListaComportamiento.instrucciones
                        while (aux != None):
                            aux.ejecutar(tablaLocal,identificador.value)
                            aux = aux.sig

                ListaComportamiento = ListaComportamiento.sig

            identificador = identificador.sig
        
#------------------------------------------------------------------------------#

class While(Expr):
    ''' Raiz del arbol de instrucciones y expresiones de la iteracion
         indeterminada '''
    def __init__(self,listaExpresiones,listaInstrucciones):
        self.type = "ITERACION INDETERMINADA"
        self.expresiones = listaExpresiones
        self.InstruccionesWhile = listaInstrucciones
        self.sig = None

    def imprimirWhile(self,numeroTabs):
        '''
        * Descripción de la función: Esta funcion se encarga de imprimir
        la instruccion WHILE con su guardia y sus instrucciones.
        * Variables de entrada:
            - numeroTabs: Numero de tabulaciones que tendran las impresiones.
        * Variables de salida: Ninguna
        '''
        # Se calcula el numero de tabs para la instruccion WHILE
        espacio = "   "*numeroTabs
        numeroTabs+=1

        # Se imprime un WHILE
        print(espacio+self.type)

        espacio = "   "*numeroTabs
        print(espacio+"-guardia :",self.expresiones.type)

        # Numero de tabs para las expresiones
        numeroTabsExpr=numeroTabs+1         
        if(self.expresiones.type=="OPERADOR_UNARIO"):
            expr = self.expresiones.value

            # Se calcula una nueva cantidad de tabs para las expresiones
            numeroTabs2= numeroTabs+1
            espacio2 = "   "*numeroTabs2
            numeroTabsExpr=numeroTabs2

            print(espacio2+"-operador unario:",self.expresiones.op)
            
        else:
            expr = self.expresiones

        expr.imprimirExpresionesBinarias(numeroTabsExpr)

        # Numero de tabs para las instrucciones
        numeroTabs+=1
        print(espacio+"-instrucciones:")
        self.InstruccionesWhile.imprimirInstrucciones(numeroTabs)

    def ejecutar(self):

        tabla = Expr.ultimo
        resultado = self.expresiones.evaluar(None,tabla)

        if (resultado == True):
            while True:
                aux = self.InstruccionesWhile
                while (aux!=None):
                    aux.ejecutar()
                    aux = aux.sig

                resultado = self.expresiones.evaluar(None,tabla)

                if (resultado != True):
                    break

                    

#------------------------------------------------------------------------------#

class Condicional(Expr):
    ''' Raiz del arbol de instrucciones y expresiones del condicional '''
    def __init__(self,listaExpresiones,exito,fracaso):
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

        # Se calcula el numero de tabs para la instruccion IF
        espacio = "   "*numeroTabs
        print(espacio+self.type)

        # Se calcula el numero de tabs para la guardia del IF
        numeroTabs+=1
        espacio = "   "*numeroTabs

        print(espacio+"-guardia :",self.expresionesCondicional.type)

        # Se calcula el numero de tabs para las expresiones
        numeroTabs2 = numeroTabs + 1
        espacio2 = "   "*numeroTabs2
        numeroTabsExpr = numeroTabs

        if(self.expresionesCondicional.type=="OPERADOR_UNARIO"):

            # Se recalcula el numero de tabs para las expresiones
            expr = self.expresionesCondicional.value
            numeroTabsExpr = numeroTabs2
            print(espacio2+"-operador unario:",self.expresionesCondicional.op)

        else:
            expr = self.expresionesCondicional


        expr.imprimirExpresionesBinarias(numeroTabsExpr)
        print(espacio+"-exito:")

        numeroTabs+=1    # Numero de tabs para las instrucciones del IF
        self.exito.imprimirInstrucciones(numeroTabs)

        if(self.fracaso!=None):
            print(espacio+"-fracaso:")
            self.fracaso.imprimirInstrucciones(numeroTabs)

    def ejecutar(self):

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
    ''' Raiz del arbol de las expresiones binarias '''
    def __init__(self,left,op,right,linea):
        self.type = "EXPRESION_BINARIA"
        self.left = left
        self.right = right
        self.op = op
        self.numeroLinea = linea

    def evaluar(self,VariableRobot,tablaSimbolos):

      
        resultadoIzq = self.left.evaluar(VariableRobot,tablaSimbolos)
        resultadoDer = self.right.evaluar(VariableRobot,tablaSimbolos)
        
        if (self.op == "+"):
            return resultadoIzq + resultadoDer

        elif (self.op == "-"):
            return resultadoIzq - resultadoDer

        elif (self.op == "/"): 
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
        self.type = "OPERADOR_UNARIO"
        self.op = op
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):

        resultado = self.value.evaluar(VariableRobot,tablaSimbolos)

        if (self.op == "-"):
            return (- resultado)

        elif (self.op == "~"):
            return not(resultado)

#------------------------------------------------------------------------------#

class Number(Expr):
    ''' Nodo que almacena los numeros del programa '''
    def __init__(self,value,numeroLinea):
        self.type = "int"
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):

        resultado = self.value
        return int(resultado)

#------------------------------------------------------------------------------#

class Booleano(Expr):
    ''' Nodo que almacena los booleanos del programa (true y false) '''
    def __init__(self,value,numeroLinea):
        self.type = "bool"
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):

        resultado = self.value

        if (resultado == "true"):
            return True
        elif (resultado == "false"):
            return False

#------------------------------------------------------------------------------#

class Identificadores(Expr):
    ''' Nodo que almacena los identificadores del programa '''

    def __init__(self,value,linea):
        self.type = "ident"
        self.value = value
        self.numeroLinea = linea
        self.sig = None

    def evaluar(self,VariableRobot,tablaSimbolos):

        result,tabla = self.busqueda(tablaSimbolos)
        tipo = result[0]
        resultado = result[3]
        if (resultado != None):
            if (tipo== "int"):
                return int(resultado)

            elif (tipo == "bool"):

                if (resultado == "true"):
                    return True
                else:
                    return False

            elif (tipo == "char"):
                return resultado

        else:
            print("Error en la linea",self.numeroLinea,": la variable \'"
                +self.value+"\' no tiene valor asociado")

#------------------------------------------------------------------------------#

class VariableMe(Expr):
    ''' Nodo que almacena la variable me programa '''
    def __init__(self,value,linea):
        self.type = "me"
        self.value = value
        self.numeroLinea = linea
        self.sig = None

    def evaluar(self,VariableRobot,tablaSimbolos):

        result,tabla = self.buscar(VariableRobot)
        tipo = result[0]
        resultado = result[3]
        if (resultado != None):
            if (tipo== "int"):
                return int(resultado)

            elif (tipo == "bool"):

                if (resultado == "true"):
                    return True
                if (resultado == "false"):
                    return False

            elif (tipo == "char"):
                return resultado

        else:
            print("Error en la linea",self.numeroLinea,": la variable \'"
                +self.value+"\' no tiene valor asociado")

#------------------------------------------------------------------------------#

class Caracter(Expr):
    ''' Nodo que almacena los caracteres del programa '''
    def __init__(self,value,numeroLinea):
        self.type = "char"
        self.value = value
        self.numeroLinea = numeroLinea

    def evaluar(self,VariableRobot,tablaSimbolos):

        resultado = self.value
        return resultado



#------------------------------------------------------------------------------#



