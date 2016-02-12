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
* Descripcion: Codigo principal del parser.
*
*
* Ultima modificacion: 02/10/2015
*
'''


#------------------------------------------------------------------------------#
#                        DEFINICION DE LA CLASE ARBOL                          #
#------------------------------------------------------------------------------#

class Expr: 
    def imprimirInstruccionesSimples(self,nivelArbol):
        espacio = "   "*nivelArbol
        print(espacio+self.type)

        nivelArbol+=1
        espacio = "   "*nivelArbol
        aux = self.Identificadores
        while (aux != None):
            print(espacio+"- var:",aux.value)
            aux = aux.sig

    def imprimirInstrucciones(self,nivelArbol):
        aux = self
        if(aux.sig != None):
            espacio = "   "*nivelArbol
            print(espacio+"SECUENCIACION")
        while (aux!= None):
            if (aux.type in {"ACTIVATE","DEACTIVATE","ADVANCE"}):
                aux.imprimirInstruccionesSimples(nivelArbol)
            elif (aux.type in {"ITERACION INDETERMINADA","CONDICIONAL"}):
                if (aux.type == "ITERACION INDETERMINADA"):
                    aux.imprimirWhile(nivelArbol)
                elif (aux.type == "CONDICIONAL"):
                    aux.imprimirCondicional(nivelArbol)
            else:
                aux.imprimirAST(nivelArbol)
            aux=aux.sig

    def imprimirExpresionesBinarias(self,nivelArbol):
        nivelArbol+=1
        espacio = "   "*nivelArbol
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

                if (self.left.type=="EXPRESION_BINARIA"):
                    self.left.imprimirExpresionesBinarias(nivelArbol)
                elif(self.left.type=="OPERADOR_UNARIO"):
                    self.left.value.imprimirExpresionesBinarias(nivelArbol)

                if (self.right.type=="EXPRESION_BINARIA"):
                    self.right.imprimirExpresionesBinarias(nivelArbol)
                elif(self.right.type=="OPERADOR_UNARIO"):
                    self.right.value.imprimirExpresionesBinarias(nivelArbol)

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

    def imprimirAST(self,nivelArbol):

        espacio = "   "*nivelArbol
        nivelArbol+=1
        if (self.arbolInstruccion!=None):
            print(espacio+"INICIO PROGRAMA")
            aux = self.arbolInstruccion.Instrucciones
            aux.imprimirInstrucciones(nivelArbol)

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
    def __init__(self,listaExpresiones):
        self.type = "STORE"
        self.expresiones = listaExpresiones
        self.sig = None

#------------------------------------------------------------------------------#

class Drop(Expr):
    def __init__(self,listaExpresiones):
        self.type = "DROP"
        self.expresiones = listaExpresiones
        self.sig = None

#------------------------------------------------------------------------------#

class Collect(Expr):
    def __init__(self,identificador):
        self.type = "COLLECT"
        self.identificador = identificador
        self.sig = None

#------------------------------------------------------------------------------#

class Read(Expr):
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
    def __init__(self,tipo,listaExpresiones):
        self.type = tipo
        self.expresiones = listaExpresiones
        self.sig = None

#------------------------------------------------------------------------------#

class Condicion(Expr):
    def __init__(self,type):
        self.type = type
        self.sig = None

#------------------------------------------------------------------------------#

class ListaComportamiento(Expr):
    """docstring for ListaComportamiento"""
    def __init__(self, condicion,instrucciones):
        self.type = "Lista de comportamientos"
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.sig = None

#------------------------------------------------------------------------------#

class Declaraciones(Expr):
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
    def __init__(self,listaIdentificadores):
        self.type = "ACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

#------------------------------------------------------------------------------#

class Deactivate(Expr):
    def __init__(self,listaIdentificadores):
        self.type = "DEACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

#------------------------------------------------------------------------------#

class Advance(Expr):
    def __init__(self,listaIdentificadores):
        self.type = "ADVANCE"
        self.Identificadores = listaIdentificadores
        self.sig = None

#------------------------------------------------------------------------------#

class While(Expr):
    def __init__(self,listaExpresiones,listaInstrucciones):
        self.type = "ITERACION INDETERMINADA"
        self.expresiones = listaExpresiones
        self.InstruccionesWhile = listaInstrucciones
        self.sig = None

    def imprimirWhile(self,nivelArbol):

        espacio = "   "*nivelArbol
        nivelArbol+=1
        print(espacio+self.type)

        espacio = "   "*nivelArbol
        print(espacio+"-guardia :",self.expresiones.type)


        nivelArbolExpr=nivelArbol+1
        if(self.expresiones.type=="OPERADOR_UNARIO"):
            expr = self.expresiones.value
            nivelArbol2= nivelArbol+1
            espacio2 = "   "*nivelArbol2
            nivelArbolExpr=nivelArbol2

            print(espacio2+"-operador unario:",self.expresiones.op)
            
        else:
            expr = self.expresiones

        expr.imprimirExpresionesBinarias(nivelArbolExpr)
        nivelArbol+=1
        print(espacio+"-instrucciones:")
        self.InstruccionesWhile.imprimirInstrucciones(nivelArbol)

#------------------------------------------------------------------------------#

class Condicional(Expr):
    def __init__(self,listaExpresiones,exito,fracaso):
        self.type = "CONDICIONAL"
        self.expresionesCondicional = listaExpresiones
        self.exito = exito
        self.fracaso = fracaso
        self.sig = None

    def imprimirCondicional(self,nivelArbol):
        espacio = "   "*nivelArbol
        print(espacio+self.type)
        nivelArbol+=1
        espacio = "   "*nivelArbol

        print(espacio+"-guardia :",self.expresionesCondicional.type)

        nivelArbol2 = nivelArbol + 1
        espacio2 = "   "*nivelArbol2
        nivelArbolExpr = nivelArbol

        if(self.expresionesCondicional.type=="OPERADOR_UNARIO"):
            expr = self.expresionesCondicional.value
            nivelArbolExpr = nivelArbol2
            print(espacio2+"-operador unario:",self.expresionesCondicional.op)
        else:
            expr = self.expresionesCondicional


        expr.imprimirExpresionesBinarias(nivelArbolExpr)
        print(espacio+"-exito:")

        nivelArbol+=1
        self.exito.imprimirInstrucciones(nivelArbol)

        if(self.fracaso!=None):
            print(espacio+"-fracaso:")
            self.fracaso.imprimirInstrucciones(nivelArbol)

#------------------------------------------------------------------------------#
#                               EXPRESIONES                                    #
#------------------------------------------------------------------------------#

class BinOp(Expr):
    def __init__(self,left,op,right):
        self.type = "EXPRESION_BINARIA"
        self.left = left
        self.right = right
        self.op = op

#------------------------------------------------------------------------------#

class Number(Expr):
    def __init__(self,value):
        self.type = "number"
        self.value = value

#------------------------------------------------------------------------------#

class OperadorUnario(Expr):
    def __init__(self,op,value):
        self.type = "OPERADOR_UNARIO"
        self.op = op
        self.value = value

#------------------------------------------------------------------------------#

class NegacionBool(Expr):
    def __init__(self,value):
        self.type = "negacion bool"
        self.value = value

#------------------------------------------------------------------------------#

class Booleano(Expr):
    def __init__(self,value):
        self.type = "booleano"
        self.value = value

#------------------------------------------------------------------------------#

class Identificadores(Expr):
    def __init__(self,value):
        self.type = "ident"
        self.value = value
        self.sig = None

#------------------------------------------------------------------------------#

class VariableMe(Expr):
    def __init__(self,value):
        self.type = "me"
        self.value = value

#------------------------------------------------------------------------------#

class Caracter(Expr):
    def __init__(self,value):
        self.type = "caracter"
        self.value = value
        
#------------------------------------------------------------------------------#



