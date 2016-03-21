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

class TablaSimbolos():

	def __init__(self,padre=None,hijos=None,tipo="tablaSimbolos",instrucciones=None):
		
		self.padre = padre
		self.hijos = hijos
		self.type = tipo
		self.instrucciones = instrucciones
		self.tabla = {}
		

	def buscar(self,variable):

		aux = self
		#print("ADENTRO DE CLASE:",aux)

		while (aux!=None):

			try:
				return aux.tabla[variable],aux
			except:
				aux = aux.padre

		return None,None

	def buscarLocal(self,variable):

		try:
			return self.tabla[variable]
		except:
			return None

	def insertar(self,variable,tipo,valorAsociado=None,activado=0,valor=None,coordenada=(0,0)):

		if self.buscarLocal(variable) == None:
			self.tabla[variable] = [tipo,valorAsociado,activado,valor,coordenada]
			return False

		else:
			return True


