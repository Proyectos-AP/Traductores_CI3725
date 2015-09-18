'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: main.py
*
* Nombres:
* 		Alejandra Cordero / Carnet: 12-10645
* 		Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion:
*
*
* Ultima modificacion: 17/09/2015
*
'''

################################################################################
#                		DEFINICIÓN DE LAS CLASE TOKEN                          #
################################################################################

class token:
	def __init__(self,tipo=None,elem=None,fila=None,columna=None):
		'''
		Descripción de la función: 
		Variables de entrada: La objetivo de esta funcion es servir de apoyo 
		para realizar el TAD cola mediante el uso de 'listas enlazadas'
			* Self:  Corresponde a la instancia del objeto nodo
			* Valor: Corresponde a el valor que poseera el nodo
			* Prioridad: Corresponde a la prioridad que va a poseer el nosdo
		Variables de salida: No posee variables de salida
		'''
		# Tipo del token
		self.tipo = tipo
		self.elem = elem
		# Fila donde se encuentra el token
		self.fila = fila
		# Fila donde se encuentra el token
		self.columna = columna

################################################################################
#                		DEFINICIÓN DE LAS CLASE LISTA 	                       #
################################################################################

class lista:
	'''
	Descripción de la clase: Lista enlazada. Permite crear otros TADS como 
	pila u cola, a partir de ella.
	'''
	def __init__(self,valor = None, siguiente = None):
		'''
		Descripción de la función: Crea una lista enlazada.
		Variables de entrada:
			* self : lista() -> Corresponde a la instancia del objeto lista.
			* valor : None -> Corresponde al valor almacenado en la lista.
			* siguiente : None / lista() -> Dirección al siguiente elemento.
		Variables de salida: Ninguna.
		'''
		self.valor = None
		self.siguiente = None 
	
#------------------------------------------------------------------------------#
	
	def agregar(self,elemento):
		'''
		Descripción de la función: Agrega un elemento al final de la lista.
		Variables de entrada:
			* self : lista() -> Corresponde al a instancia del objeto lista.
			* elemento : T -> Es el elemento que desea agregarse a la lista.
						  Su tipo debe coincidir con el de los demás de 
						  la lista.
		Variables de salida: Ninguna.
		'''
		if self.valor == None: # La lista está vacía.
			self.valor  = elemento
		elif self.siguiente != None:  # Llamada recursiva para llegar al final.
			self.siguiente.agregar(elemento)
		elif self.siguiente == None: # Se llegó al último elemento.
			self.siguiente = lista()
			self.siguiente.agregar(elemento)
	
#------------------------------------------------------------------------------#
	
	def imprimir(self):
		'''
		Descripción de la función: Agrega un elemento al final de la lista.
		Variables de entrada:
			* self : lista() -> Corresponde al a instancia del objeto lista.
			* elemento : T -> Es el elemento que desea agregarse a la lista.
						  Su tipo debe coincidir con el de los demás de 
						  la lista.
		Variables de salida: Ninguna.
		'''
		print("-------------------------------")
		print("        Imprimiendo lista")
		print("-------------------------------")
		if (self == None or self.valor ==None):
			print(None)
		elif self.valor:
			aux = self
			while aux:

				if (aux.valor.tipo=="TkNum"):
					print(aux.valor.tipo+"("+str(aux.valor.elem)+")",aux.valor.fila,aux.valor.columna)
				elif (aux.valor.tipo=="TkIdent"):
					print(aux.valor.tipo+"(\""+aux.valor.elem+"\")",aux.valor.fila,aux.valor.columna)
				else:
					print(aux.valor.tipo,aux.valor.elem)
				aux = aux.siguiente
	
#------------------------------------------------------------------------------#

	