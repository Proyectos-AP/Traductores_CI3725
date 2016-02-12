'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: mainParser.py
*
* Nombres:
*     Alejandra Cordero / Carnet: 12-10645
*     Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion: Definicion de la clase Arbol.
*
*
* Ultima modificacion: 11/02/2016
*
'''


#------------------------------------------------------------------------------#
#                        DEFINICION DE LA CLASE ARBOL                          #
#------------------------------------------------------------------------------#

class Expr: 


    def imprimirInstrucciones(self,numeroTabs):
        '''
          Descripción de la función: Esta funcion imprime las instrucciones del
                                    arbol de instrucciones.

          * Variables de entrada:
                                 - numeroTabs: Numero de tabulaciones que 
                                                tendran las impresiones.
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
          Descripción de la función: Esta funcion imprime el conjunto de 
                                    instrucciones que son de la forma 
                                    INSTRUCCION LISTA_DE_IDENTIFICADORES, es 
                                    decir, ACTIVATE,DEACTIVATE,ADVANCE.

          * Variables de entrada:
                                 - numeroTabs: Numero de tabulaciones que 
                                                tendran las impresiones.
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
          Descripción de la función: Esta funcion imprime el arbol de 
                                    expresiones binarias en preorder.

          * Variables de entrada:
                                 - numeroTabs: Numero de tabulaciones que 
                                                tendran las impresiones.
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
          Descripción de la función: Esta funcion se encarga de imprimir la rama
                                    de instrucciones del AST.
    
          * Variables de entrada:
                                 - numeroTabs: Numero de tabulaciones que 
                                                tendran las impresiones.
          * Variables de salida: Ninguna

        '''

        espacio = "   "*numeroTabs
        numeroTabs+=1
        if (self.arbolInstruccion!=None):
            print(espacio+"INICIO PROGRAMA")
            aux = self.arbolInstruccion.Instrucciones
            aux.imprimirInstrucciones(numeroTabs)

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
#                         LISTA DE DECLARACIONES                               #
#------------------------------------------------------------------------------#

class Store(Expr):

    ''' Nodo que almacena el apuntador del arbol de expresiones de la 
        instruccion STORE'''
    def __init__(self,listaExpresiones):
        self.type = "STORE"
        self.expresiones = listaExpresiones
        self.sig = None

#------------------------------------------------------------------------------#

class Drop(Expr):

    ''' Nodo que almacena el apuntador del arbol de expresiones de la 
        instruccion DROP'''
    def __init__(self,listaExpresiones):
        self.type = "DROP"
        self.expresiones = listaExpresiones
        self.sig = None

#------------------------------------------------------------------------------#

class Collect(Expr):

    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion COLLECT '''
    def __init__(self,identificador):
        self.type = "COLLECT"
        self.identificador = identificador
        self.sig = None

#------------------------------------------------------------------------------#

class Read(Expr):

    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion READ '''
    def __init__(self,identificador):
        self.type = "READ"
        self.identificador = identificador
        self.sig = None

#------------------------------------------------------------------------------#

class Recieve(Expr):
    def __init__(self):
        self.type = "RECIEVE"
        self.sig = None

#------------------------------------------------------------------------------#
    
class Send(Expr):
    def __init__(self):
        self.type = "SEND"
        self.sig = None

#------------------------------------------------------------------------------#

class Movimiento(Expr):

    ''' Nodo que almacena la direccion del movimiento del robot '''
    def __init__(self,tipo,listaExpresiones):
        self.type = tipo
        self.expresiones = listaExpresiones
        self.sig = None

#------------------------------------------------------------------------------#

class Condicion(Expr):

    ''' Nodo que almacena el tipo de condicion de la lista de comportamiento del
         robot '''
    def __init__(self,type):
        self.type = type
        self.sig = None

#------------------------------------------------------------------------------#

class ListaComportamiento(Expr):

    ''' Lista de comportamiento del robot'''
    def __init__(self, condicion,instrucciones):
        self.type = "Lista de comportamientos"
        self.condicion = condicion
        self.instrucciones = instrucciones
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

#------------------------------------------------------------------------------#

class Deactivate(Expr):

    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion DEACTIVATE '''
    def __init__(self,listaIdentificadores):
        self.type = "DEACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

#------------------------------------------------------------------------------#

class Advance(Expr):

    ''' Nodo que almacena el apuntador de la lista de identificadores de la 
        instruccion ADVANCE '''
    def __init__(self,listaIdentificadores):
        self.type = "ADVANCE"
        self.Identificadores = listaIdentificadores
        self.sig = None

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
          Descripción de la función: Esta funcion se encarga de imprimir
                                    la instruccion WHILE con su guardia y sus 
                                    instrucciones .

          * Variables de entrada:
                                 - numeroTabs: Numero de tabulaciones que 
                                                tendran las impresiones.
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
          Descripción de la función: Esta funcion se encarga de imprimir
                                    la instruccion IF con su guardia y sus 
                                    instrucciones .

          * Variables de entrada:
                                 - numeroTabs: Numero de tabulaciones que 
                                                tendran las impresiones.
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

#------------------------------------------------------------------------------#
#                               EXPRESIONES                                    #
#------------------------------------------------------------------------------#

class ExpresionBinaria(Expr):

    ''' Raiz del arbol de las expresiones binarias '''
    def __init__(self,left,op,right):
        self.type = "EXPRESION_BINARIA"
        self.left = left
        self.right = right
        self.op = op

#------------------------------------------------------------------------------#

class OperadorUnario(Expr):

    ''' Raiz del arbol de las expresiones unarias '''
    def __init__(self,op,value):
        self.type = "OPERADOR_UNARIO"
        self.op = op
        self.value = value

#------------------------------------------------------------------------------#

class Number(Expr):

    ''' Nodo que almacena los numeros del programa '''
    def __init__(self,value):
        self.type = "number"
        self.value = value

#------------------------------------------------------------------------------#

class Booleano(Expr):

    ''' Nodo que almacena los booleanos del programa (true y false) '''
    def __init__(self,value):
        self.type = "booleano"
        self.value = value

#------------------------------------------------------------------------------#

class Identificadores(Expr):

    ''' Nodo que almacena los identificadores del programa '''
    def __init__(self,value):
        self.type = "ident"
        self.value = value
        self.sig = None

#------------------------------------------------------------------------------#

class VariableMe(Expr):

    ''' Nodo que almacena la variable me programa '''
    def __init__(self,value):
        self.type = "me"
        self.value = value

#------------------------------------------------------------------------------#

class Caracter(Expr):

    ''' Nodo que almacena los caracteres del programa '''
    def __init__(self,value):
        self.type = "caracter"
        self.value = value

#------------------------------------------------------------------------------#



