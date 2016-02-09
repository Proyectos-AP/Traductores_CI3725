def agregarHijos(hijo1,hijo2):

	aux = hijo1
	while aux.sig != None:
		aux = aux.sig
	aux.sig = hijo2

	return hijo1

# def agregarHijos(hijo1,hijo2):
#     if not(isinstance(hijo1,list)) and isinstance(hijo2,list):
#         return [hijo1] + hijo2
#     elif isinstance(hijo1,list) and isinstance(hijo2,list):
#         return hijo1 + hijo2
#     else:
#         return [hijo1,hijo2] 

#------#		

class Expr: 
    def imprimirInstruccionesSimples(self,nivelArbol):
        espacio = "  "*nivelArbol
        print(espacio+self.type)

        nivelArbol+=1
        espacio = "  "*nivelArbol
        aux = self.Identificadores
        while (aux != None):
            print(espacio+"- var:",aux.value)
            aux = aux.sig

    def imprimirInstrucciones(self,nivelArbol):
        aux = self
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

    def imprimirExpresionesBinarias(self):
        if (self != None):
            if (self.type=="binop"):
                self.left.imprimirExpresionesBinarias()
                print(self.op,end=" ")
                self.right.imprimirExpresionesBinarias()
            else:
                print(self.value,end=" ")

class BinOp(Expr):
    def __init__(self,left,op,right):
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op

class Number(Expr):
    def __init__(self,value):
        self.type = "number"
        self.value = value

# class MenosUnario(Expr):
#     def __init__(self,value):
#         self.type = "menos unario"
#         self.value = value

class OperadorUnario(Expr):
    def __init__(self,op,value):
        self.type = "operador unario"
        self.value = value
        self.op = op

class NegacionBool(Expr):
    def __init__(self,value):
        self.type = "negacion bool"
        self.value = value

class Booleano(Expr):
    def __init__(self,value):
        self.type = "booleano"
        self.value = value

class Identificadores(Expr):
    def __init__(self,value):
        self.type = "ident"
        self.value = value
        self.sig = None

class VariableMe(Expr):
    def __init__(self,value):
        self.type = "me"
        self.value = value

class Caracter(Expr):
    def __init__(self,value):
        self.type = "caracter"
        self.value = value

class Activate(Expr):
    def __init__(self,listaIdentificadores):
        self.type = "ACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None


class Deactivate(Expr):
    def __init__(self,listaIdentificadores):
        self.type = "DEACTIVATE"
        self.Identificadores = listaIdentificadores
        self.sig = None

class Advance(Expr):
    def __init__(self,listaIdentificadores):
        self.type = "ADVANCE"
        self.Identificadores = listaIdentificadores
        self.sig = None

class Execute(Expr):
    def __init__(self,listaInstrucciones):
        self.type = "EXECUTE"
        self.Instrucciones = listaInstrucciones
        self.sig = None

class While(Expr):
    def __init__(self,listaExpresiones,listaInstrucciones):
        self.type = "ITERACION INDETERMINADA"
        self.expresiones = listaExpresiones
        self.InstruccionesWhile = listaInstrucciones
        self.sig = None

    def imprimirWhile(self,nivelArbol):

        espacio = "  "*nivelArbol
        nivelArbol+=1
        print(espacio+self.type)

        espacio = "  "*nivelArbol
        print(espacio+"-guardia :",end=" ")
        nivelArbol+=1
        self.expresiones.imprimirExpresionesBinarias()
        print("")
        print(espacio+"-instrucciones:")
        self.InstruccionesWhile.imprimirInstrucciones(nivelArbol)
        # while (aux!= None):
        #     if (aux.type in {"ACTIVATE","DEACTIVATE","ADVANCE"}):
        #         aux.imprimirInstruccionesSimples()
        #     else:
        #         if (aux.type == "ITERACION INDETERMINADA"):
        #             aux.imprimirWhile()
        #         elif (aux.type == "CONDICIONAL"):
        #             aux.imprimirCondiional()
        #     aux=aux.sig

class Condicional(Expr):
    def __init__(self,listaExpresiones,exito,fracaso):
        self.type = "CONDICIONAL"
        self.expresionesCondicional = listaExpresiones
        self.exito = exito
        self.fracaso = fracaso
        self.sig = None

    def imprimirCondicional(self,nivelArbol):
        espacio = "  "*nivelArbol
        nivelArbol+=1
        print(espacio+self.type)
        espacio = "  "*nivelArbol
        print(espacio+"-guardia :",end=" ")
        nivelArbol+=1
        self.expresionesCondicional.imprimirExpresionesBinarias()
        print("")
        print(espacio+"-exito:")

        self.exito.imprimirInstrucciones(nivelArbol)

        if(self.fracaso!=None):
            print(espacio+"-fracaso:")
            self.fracaso.imprimirInstrucciones(nivelArbol)
            # while (aux!= None):
            #     if (aux.type in {"ACTIVATE","DEACTIVATE","ADVANCE"}):
            #         aux.imprimirInstruccionesSimples()
            #     else:
            #         pass
            #     aux=aux.sig



class Store(Expr):
    def __init__(self,listaExpresiones):
        self.type = "STORE"
        self.expresiones = listaExpresiones
        self.sig = None

class Recieve(Expr):
    def __init__(self):
        self.type = "RECIEVE"
        self.sig = None

class Send(Expr):
    def __init__(self):
        self.type = "SEND"
        self.sig = None

class Collect(Expr):
    def __init__(self,identificador):
        self.type = "COLLECT"
        self.identificador = identificador
        self.sig = None

class Drop(Expr):
    def __init__(self,listaExpresiones):
        self.type = "DROP"
        self.expresiones = listaExpresiones
        self.sig = None

class Movimiento(Expr):
    def __init__(self,tipo,listaExpresiones):
        self.type = tipo
        self.expresiones = listaExpresiones
        self.sig = None

class Read(Expr):
    def __init__(self,identificador):
        self.type = "READ"
        self.identificador = identificador
        self.sig = None

class Deactivation(Expr):
    def __init__(self):
        self.type = "DEACTIVATION"
        self.sig = None

class Activation(Expr):
    def __init__(self):
        self.type = "ACTIVATION"
        self.sig = None

class Default(Expr):
    def __init__(self):
        self.type = "DEFAULT"
        self.sig = None

class ListaComportamiento(Expr):
    """docstring for ListaComportamiento"""
    def __init__(self, condicion,instrucciones):
        self.type = "Lista de comportamientos"
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.sig = None

class Declaraciones(Expr):
    def __init__(self,tipoRobot,identificadores,listaComportamiento):
        self.type = "DECLARACIONES"
        self.tipoRobot = tipoRobot
        self.identificadores = identificadores
        self.listaComportamiento = listaComportamiento
        self.sig = None

class Create(Expr):
    def __init__(self,listaDeclaraciones):
        self.type = "CREATE"
        self.listaDeclaraciones = listaDeclaraciones

class RaizAST(Expr):
    def __init__(self,ArbolDeclaracion,ArbolInstruccion):
        self.type = "RaizAST"
        self.arbolDeclaracion = ArbolDeclaracion
        self.arbolInstruccion = ArbolInstruccion
        self.sig = None

    def imprimirAST(self,nivelArbol):

        espacio = "  "*nivelArbol
        nivelArbol+=1
        if (self.arbolInstruccion!=None):
            print(espacio+"SECUENCIACION")
            aux = self.arbolInstruccion.Instrucciones
            # print(aux)
            aux.imprimirInstrucciones(nivelArbol)
        
        


# class ListaHijos(Expr):
#     def __init__(self,hijo1,hijo2):
#         self.type = "secuencia identifiadores"
#         # if len(hijo2) == 1:
#         # 	self.hijos = [hijo1] + [hijo2]
#         # else:
#         # 	self.hijos = [hijo1] + ListaHijos(hijo2[0],hijo2[1:])
#         self.hijos = agregarHijos(hijo1,hijo2)


