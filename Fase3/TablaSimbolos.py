'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: TablaSimbolos.py
*
* Nombres:
*     Alejandra Cordero / Carnet: 12-10645
*     Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion: Definicion de la clase TablaSimbolos.
*
*
* Ultima modificacion: 27/02/2016
*
'''

#------------------------------------------------------------------------------#
#                            IMPORTE DE MODULOS                                #
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
#                             DEFINICION DE CLASE                              #
#------------------------------------------------------------------------------#

class TopeDeTablaSimbolos():

	def __init__(self,padre=None,hijos=None):

		self.type = "top"
		self.padre = padre
		self.hijos = hijos


class TablaSimbolos():

	def __init__(self,padre=None):
		
		self.type = "tablaSimbolos"
		self.tabla = {}
		self.padre = padre

	def buscar(self,variable):

		aux = self
		#print(aux.tabla)

		while (aux!=None):

			try:
				return aux.tabla[variable]
			except:
				aux = aux.padre

		return None

	def buscarLocal(self,variable):

		try:
			return self.tabla[variable]
		except:
			return None

	def insertar(self,variable,tipo,valorAsociado=None):

		if self.buscarLocal(variable) == None:

			self.tabla[variable] = [tipo,valorAsociado]
			return False

		else:
			return True


