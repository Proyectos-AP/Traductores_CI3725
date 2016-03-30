'''
*
* Universidad Simón Bolívar
* Departamento de Computación y Tecnología de la Información
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: TablaSimbolos.py
*
* Nombres:
*     Alejandra Cordero / Carnet: 12-10645
*     Pablo Maldonado   / Carnet: 12-10561
*
* Descripción: Definición de la clase TablaSimbolos.
*
*
* Última modificación: 30/03/2016
*
'''

#------------------------------------------------------------------------------#
#                             DEFINICIÓN DE CLASE                              #
#------------------------------------------------------------------------------#

class TablaSimbolos():

	def __init__(self,padre = None,hijos = None,tipo = "tablaSimbolos",instrucciones = None):
		'''
		* Descripción: Constructor de la clase TablaSimbolos.
		'''

		self.padre = padre
		self.hijos = hijos
		self.tipo = tipo
		self.instrucciones = instrucciones
		self.tabla = {}
		
	def buscar(self,variable):
		'''
		* Descripción de la función: Busca un elemento en las Tablas de 
		  Símbolos de los scopes definidos.
		* Variables de entrada:
			- variable : Elemento a buscar en los scopes definidos.
		* Variables de salida: Si encuentra al elemento buscado en alguno de 
		  los scopes definidos, devuelve la información asociada a él de la 
		  tabla de símbolos. En caso contrario devuelve None.
		'''

		aux = self

		while (aux!=None):

			try:
				return aux.tabla[variable],aux
			except:
				aux = aux.padre

		return None,None

	def buscarLocal(self,variable):
		'''
		* Descripción de la función: Busca un elemento en las Tablas de 
		  Símbolos del scope local.
		* Variables de entrada:
			- variable : Elemento a buscar en el scope local.
		* Variables de salida: Si encuentra al elemento buscado en el scope 
		  actual, devuelve la información asociada a él de la tabla de 
		  símbolos. En caso contrario devuelve None.
		'''

		try:
			return self.tabla[variable]
		except:
			return None

	def insertar(self,variable,tipo,valorAsociado = None,activado = 0,valor = None,coordenada = [0,0]):
		'''
		* Descripción de la función: Inserta un elemento en la Tabla de 
		  Simbolos con su información asociada.
		* Variables de entrada:
			- variable : 
			- tipo : 
			- valorAsociado :
			- activado : 
			- valor :
			- coordenada :
		* Variables de salida: Booleano que indica si el elemento fue insertado
		  en la Tabla de Simbolos.
		'''

		if self.buscarLocal(variable) == None:
			self.tabla[variable] = [tipo,valorAsociado,activado,valor,coordenada]
			return False

		else:
			return True

#------------------------------------------------------------------------------#

