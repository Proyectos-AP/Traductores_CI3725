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

class VariableMe(Expr):
    def __init__(self,value):
        self.type = "me"
        self.value = value

class Caracter(Expr):
    def __init__(self,value):
        self.type = "caracter"
        self.value = value