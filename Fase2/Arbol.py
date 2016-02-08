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

class Expr: pass

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
        self.type = "Activate"
        self.Identificadores = listaIdentificadores
        self.sig = None

class Deactivate(Expr):
    def __init__(self,listaIdentificadores):
        self.type = "Deactivate"
        self.Identificadores = listaIdentificadores
        self.sig = None

class Advance(Expr):
    def __init__(self,listaIdentificadores):
        self.type = "Advance"
        self.Identificadores = listaIdentificadores
        self.sig = None

class Execute(Expr):
    def __init__(self,listaInstrucciones):
        self.type = "Execute"
        self.Instrucciones = listaInstrucciones
        self.sig = None

class While(Expr):
    def __init__(self,listaExpresiones,listaInstrucciones):
        self.type = "While"
        self.expresiones = listaExpresiones
        self.InstruccionesWhile = listaInstrucciones
        self.sig = None

class Condicional(Expr):
    def __init__(self,listaExpresiones,exito,fracaso):
        self.type = "Condicional"
        self.expresionesCondicional = listaExpresiones
        self.exito = exito
        self.fracaso = fracaso
        self.sig = None


# class ListaHijos(Expr):
#     def __init__(self,hijo1,hijo2):
#         self.type = "secuencia identifiadores"
#         # if len(hijo2) == 1:
#         # 	self.hijos = [hijo1] + [hijo2]
#         # else:
#         # 	self.hijos = [hijo1] + ListaHijos(hijo2[0],hijo2[1:])
#         self.hijos = agregarHijos(hijo1,hijo2)


