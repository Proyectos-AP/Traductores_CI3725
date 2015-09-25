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

#------------------------------------------------------------------------------#
#					         IMPORTE DE MODULOS				          		   #
#------------------------------------------------------------------------------#

import sys
import os
from Lista import * 
import ply.lex as lex


class Lexer():

	def __init__(self,data=None):
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

	# Regular expression rules for simple tokens
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

	# A regular rule with some action code
	# 
	def t_TkNum(self,t):

		'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.
		'''

	    r'\d+'
	    t.value = int(t.value)    
	    return t

#------------------------------------------------------------------------------#

	# Regla para conjuntos de caracteres. Si el caracter es igual a algun 
	# caracter reservado entonces t.type sera igual al del caracter reservado,
	# de no ser igual a ningun caracter reservado entonces t.type sera
	# igual a TkIdent.

	def t_TkIdent(self,t):
		'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.

		'''
	  r'[a-zA-Z_][a-zA-Z_0-9]*'
	  t.type = self.reserved.get(t.value,'TkIdent')
	  return t

#------------------------------------------------------------------------------#

	# Regla para los comentarios.
	# Los tokens obtenidos por esta expresion regular seran omitidos.
	def t_TkComment(self,t):
		'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.
		'''
	  r'(\$-(.|\n)*?-\$)|(\$\$.*)'
	  pass
	 	# No return value. Token discarded

#------------------------------------------------------------------------------#

	# Regla para caracteres.
	# Este token solo toma caracteres encerrados entre comillas simples
	def t_TkCaracter(self,t):
		'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.
		'''
	    r'\'.\''
	    return t

#------------------------------------------------------------------------------#

	# Define a rule so we can track line numbers
	# Regla para contar los numeros de linea.
	def t_newline(self,t):
		'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.
		'''
	    r'\n+'
	    t.lexer.lineno += len(t.value)

#------------------------------------------------------------------------------#

	# Funcion para localizar el numero de columna de una palabra. 
	#     input is the input text string
	#     token is a token instance
	def find_column(self,input,token):
		'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.
		'''
	    last_cr = input.rfind('\n',0,token.lexpos)
	    column = (token.lexpos - last_cr) 
	    return column

#------------------------------------------------------------------------------#
	# Funcion para el manejo de errores
	def t_error(self,t):

				'''
			Descripción de la función: Regla para tokens correspondientes
			 a numeros.
		'''


	    # print("Error: Caracter inesperado \""+t.value[0]+"\" en la fila\
	    # "+str(t.lineno)+"\, columna "+str(self.find_column(self.data,t)) )

	    ErrorEncontrado = token(None,t.value[0],\
	    	t.lineno,self.find_column(self.data,t))

	    self.Errores+=[ErrorEncontrado] 
	    t.lexer.skip(1)
	
#------------------------------------------------------------------------------#

	# Constructor del lexer
	def build(self,**kwargs):
	    self.lexer = lex.lex(module=self, **kwargs)

#------------------------------------------------------------------------------#

	# Funcion que tokeniza entrada
	def tokenizar(self):
	    self.lexer.input(self.data)
	    while True:
	        tok = self.lexer.token()
	        if not tok: 
	            break
	        #print(tok.type, tok.value, tok.lineno,self.find_column(self.data,tok),end=" ")
	        print(tok.type, tok.value, tok.lineno,self.find_column(self.data,tok))
	        if ( tok.type in {"TkNum","TkIdent","TkCaracter"} ):
	        	NodoToken = token(tok.type,tok.value,tok.lineno,\
	        		self.find_column(self.data,tok))

	        else:
	        	NodoToken = token(tok.type,None,tok.lineno,\
	        		self.find_column(self.data,tok))
	        self.Tokens+=[NodoToken]    


