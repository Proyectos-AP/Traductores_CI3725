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

	