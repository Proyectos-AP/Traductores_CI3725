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
* Ultima modificacion: 25/09/2015
*
'''

#------------------------------------------------------------------------------#
#					         IMPORTE DE MODULOS				          		   #
#------------------------------------------------------------------------------#

import sys
import os
from Lista import * 
import ply.lex as lex

#------------------------------------------------------------------------------#
#					     DEFINICION DE LA CLASE LEXER				           #
#------------------------------------------------------------------------------#

class Lexer():

	def __init__(self,data=None):

		'''
		Descripción de la función: Clase Lexer.
		Variables de entrada:
			* self : Corresponde a la instancia del objeto Lexer.
			* data : Corresponde al input del Lexer.

		Variables de salida:

			* Tokens : Lista de tokens correctos
			* Errores : Lista de tokens con los errores lexicograficos encontrados

		'''
		self.data = data
		self.Tokens = []
		self.Errores = []
		self.reserved = {
		'create'           : 'TkCreate',
		'bot'              : 'TkBot' ,
		'on'               : 'TkOn',
		'activation'       : 'TkActivation' ,
		'desactivation'    : 'TkDeActivation',
		'store'            : 'TkStore' ,
		'end'              : 'TkEnd'  ,
		'execute'          : 'TkExecute' ,
		'activate'         : 'TkActivate',
		'desactivate'      : 'TkDeactivate' ,
		'send'             : 'TkSend' ,   
		'advance'          : 'TkAdvance' ,
		'recive'           : 'TkRecieve',
		'default'          : 'TkDefault' ,
		'me'               : 'TkMe' ,
		'drop'             : 'TkDrop',
		'collect'          : 'TkCollect',
		'as'               : 'TkAs',
		'int'              : 'TkInt',
		'left'             : 'TkLeft',
		'right'            : 'TkRight',
		'up'               : 'TkUp' ,
		'down'             : 'TkDown' ,
		'read'             : 'TkRead',
		'while'            : 'TkWhile' ,
		'bool'             : 'TkBool',
		'if'               : 'TkIf',
		'else'             : 'TkElse'  ,
		'true'             : 'TkTrue'  ,
		'false'            : 'TkFalse',
		'char'             : 'TkChar'
		}

	reserved = {
		'create'           : 'TkCreate',
		'bot'              : 'TkBot' ,
		'on'               : 'TkOn',
		'activation'       : 'TkActivation' ,
		'desactivation'    : 'TkDeActivation',
		'store'            : 'TkStore' ,
		'end'              : 'TkEnd'  ,
		'execute'          : 'TkExecute' ,
		'activate'         : 'TkActivate',
		'desactivate'      : 'TkDeactivate' ,
		'send'             : 'TkSend' ,   
		'advance'          : 'TkAdvance' ,
		'recive'           : 'TkRecieve',
		'default'          : 'TkDefault' ,
		'me'               : 'TkMe' ,
		'drop'             : 'TkDrop',
		'collect'          : 'TkCollect',
		'as'               : 'TkAs',
		'int'              : 'TkInt',
		'left'             : 'TkLeft',
		'right'            : 'TkRight',
		'up'               : 'TkUp' ,
		'down'             : 'TkDown' ,
		'read'             : 'TkRead',
		'while'            : 'TkWhile' ,
		'bool'             : 'TkBool',
		'if'               : 'TkIf',
		'else'             : 'TkElse'  ,
		'true'             : 'TkTrue'  ,
		'false'            : 'TkFalse',
		'char'             : 'TkChar'
	}

	tokens = [
	   'TkComa',
	   'TkPunto',
	   'TkDosPuntos',
	   'TkParAbre',
	   'TkParCierra',
	   'TkSuma',
	   'TkResta',
	   'TkMult',
	   'TkDiv',
	   'TkMod',
	   'TkConjuncion',
	   'TkDisyuncion',
	   'TkNegacion',
	   'TkMenor',
	   'TkMayor',
	   'TkMenorIgual',
	   'TkMayorIgual',
	   'TkIgual',
	   'TkDesigual',
	   'TkIdent',
	   'TkNum',
	   'TkCaracter',
	   'TkCommentL',
	   'TkComillas'
	] + list(reserved.values())

	# Expresiones regulares para tokens simples.
	t_TkPunto        = r'\.'
	t_TkDosPuntos    = r'\:'
	t_TkParAbre      = r'\('
	t_TkParCierra    = r'\)'
	t_TkSuma         = r'\+'
	t_TkResta        = r'-'
	t_TkMult         = r'\*'
	t_TkDiv          = r'/'
	t_TkMod          = r'\%'
	t_TkConjuncion   = r'/\\'
	t_TkDisyuncion   = r'\\/'
	t_TkNegacion     = r'\~'
	t_TkMenor        = r'<'
	t_TkMayor        = r'>'
	t_TkMenorIgual   = r'<='
	t_TkMayorIgual   = r'>='
	t_TkIgual        = r'='
	t_TkDesigual     = r'/='


	# Ignora los tabs y espacios
	t_ignore  = ' \t'
#------------------------------------------------------------------------------#

	def t_TkNum(self,t):

		'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.

			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.
				* t : Variable de tipo LexToken (clase implementada en lex.py).

			Variables de salida:

				* t : Variable de tipo LexToken (clase implementada en lex.py).
		'''
		r'\d+'
		t.value = int(t.value)
		return t

#------------------------------------------------------------------------------#

	def t_TkIdent(self,t):
		'''
			Descripción de la función:	Regla para conjuntos de caracteres. 
			Si el caracter es igual a algun caracter reservado entonces t.type 
			sera igual al del caracter reservado,de no ser igual a ningun 
			caracter reservado entonces t.type sera igual a TkIdent.

			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.
				* t : Variable de tipo LexToken (clase implementada en lex.py).

			Variables de salida:

				* t : Variable de tipo LexToken (clase implementada en lex.py).

		'''
		r'[a-zA-Z_][a-zA-Z_0-9]*'
		t.type = self.reserved.get(t.value,'TkIdent')
		return t

#------------------------------------------------------------------------------#

	def t_TkComment(self,t):

		'''
			Descripción de la función: Reglas para los comentarios.
			Los tokens obtenidos por esta expresion regular seran omitidos.

			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.
				* t : Variable de tipo LexToken (clase implementada en lex.py).

			Variables de salida:

				* Ninguno.

		'''
		r'(\$-(.|\n)*?-\$)|(\$\$.*)'
		pass


#------------------------------------------------------------------------------#

	def t_TkCaracter(self,t):
		'''
			Descripción de la función: Reglas para caracteres. Este token solo 
			toma caracteres encerrados entre comillas simples.
			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.
				* t : Variable de tipo LexToken (clase implementada en lex.py).

			Variables de salida:

				* t : Variable de tipo LexToken (clase implementada en lex.py).
		'''
		r'\'.\''
		return t

#------------------------------------------------------------------------------#

	def t_newline(self,t):
		'''
			Descripción de la función:Regla para contar los numeros de linea.
			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.
				* t : Variable de tipo LexToken (clase implementada en lex.py).

			Variables de salida:

				* Ninguno.

		'''
		r'\n+'
		t.lexer.lineno += len(t.value)

#------------------------------------------------------------------------------#

	def Numerocolumna(self,input,token):

		'''
			Descripción de la función: Funcion para localizar el numero de 
										columna de una palabra.
			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.
				* token : Variable de tipo LexToken (clase implementada en lex.py).
				* input : Input de la clase Lexer

			Variables de salida:

				* Ninguno.

		'''
		last_cr = input.rfind('\n',0,token.lexpos)
		columna = (token.lexpos - last_cr) 
		return columna

#------------------------------------------------------------------------------#

	def t_error(self,t):

		'''
			Descripción de la función: Funcion para el manejo de errores .

			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.
				* t : Variable de tipo LexToken (clase implementada en lex.py).

			Variables de salida:

				* Ninguno.

		'''
		ErrorEncontrado = token(None,t.value[0],\
			t.lineno,self.Numerocolumna(self.data,t))
		self.Errores+=[ErrorEncontrado] 
		t.lexer.skip(1)
	
#------------------------------------------------------------------------------#

	def build(self,**kwargs):
		'''
			Descripción de la función: Constructor del lexer.

		'''
		self.lexer = lex.lex(module=self, **kwargs)

#------------------------------------------------------------------------------#

	def tokenizar(self):
		'''
			Descripción de la función: Funcion que tokeniza entrada.
			Variables de entrada:
				* self : Corresponde a la instancia del objeto Lexer.

			Variables de salida:

				* Ninguno.

		'''
		self.lexer.input(self.data)
		while True:
			tok = self.lexer.token()
			if not tok: 
				break
			print(tok.type, tok.value, tok.lineno,self.Numerocolumna(self.data,tok))
			if ( tok.type in {"TkNum","TkIdent","TkCaracter"} ):
				NodoToken = token(tok.type,tok.value,tok.lineno,\
					self.Numerocolumna(self.data,tok))
			else:
				NodoToken = token(tok.type,None,tok.lineno,\
					self.Numerocolumna(self.data,tok))
			self.Tokens+=[NodoToken]    

			#print(tok.type, tok.value, tok.lineno,self.find_column(self.data,tok),end=" ")

