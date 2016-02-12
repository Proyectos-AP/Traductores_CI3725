'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: Tokens.py
*
* Nombres:
* 	  Alejandra Cordero / Carnet: 12-10645
* 	  Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion: Definicion de la clase Token.
*
*
* Ultima modificacion: 12/02/2016
*
'''
#------------------------------------------------------------------------------#
#                		DEFINICIÓN DE LAS CLASE TOKEN                          #
#------------------------------------------------------------------------------#

class token:
	def __init__(self,tipo = None,elem = None,fila = None,columna = None):
		'''
		- Descripción: Definicion de la clase Token a utilizar en el analisis
		  lexicografico.

		- Atributos:
			* tipo : Tipo del token
			* elem : Token
			* fila : Linea donde se encuentra el token
			* columna : Columna donde se encuentra el token
		'''
		self.tipo = tipo
		self.elem = elem
		self.fila = fila
		self.columna = columna