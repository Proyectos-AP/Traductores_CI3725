'''
*
* Universidad Simón Bolívar
* Departamento de Computación y Tecnología de la Información
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: Tokens.py
*
* Nombres:
* 	  Alejandra Cordero / Carnet: 12-10645
* 	  Pablo Maldonado   / Carnet: 12-10561
*
* Descripción: Definición de la clase Token.
*
*
* Última modificación: 30/03/2016
*
'''
#------------------------------------------------------------------------------#
#                		DEFINICIÓN DE LAS CLASE TOKEN                          #
#------------------------------------------------------------------------------#

class token:
	def __init__(self,tipo = None,elem = None,fila = None,columna = None):
		'''
		* Descripción: Definición de la clase Token a utilizar en el análisis
		  lexicográfico.
		* Atributos:
			- tipo : Tipo del token
			- elem : Token
			- fila : Linea donde se encuentra el token
			- columna : Columna donde se encuentra el token
		'''
		self.tipo = tipo
		self.elem = elem
		self.fila = fila
		self.columna = columna

#------------------------------------------------------------------------------#