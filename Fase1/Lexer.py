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
	   'TkMenorIgual',
	   'TkMayor',
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
	t_TkConjuncion   = r'/\\.'
	t_TkDisyuncion   = r'\\/.'
	t_TkNegacion     = r'\~'
	t_TkMenor        = r'<.'
	t_TkMenorIgual   = r'<=.'
	t_TkMayor        = r'>'
	t_TkMayorIgual   = r'>='
	t_TkIgual        = r'='
	t_TkDesigual     = r'/='


	# A string containing ignored characters (spaces and tabs)
	t_ignore  = ' \t'
#------------------------------------------------------------------------------#

	# A regular rule with some action code
	def t_TkNum(self,t):
	    r'\d+'
	    t.value = int(t.value)    
	    return t

#------------------------------------------------------------------------------#

	def t_TkIdent(self,t):
	  r'[a-zA-Z_][a-zA-Z_0-9]*'
	  t.type = self.reserved.get(t.value,'TkIdent')
	  return t

#------------------------------------------------------------------------------#

	def t_TkComment(self,t):
	  r'(\$-(.|\n)*?-\$)|(\$\$.*)'
	  pass
	    # No return value. Token discarded

#------------------------------------------------------------------------------#

	def t_TkCaracter(self,t):
	    r'\'.\''
	    return t

#------------------------------------------------------------------------------#

	# Define a rule so we can track line numbers
	def t_newline(self,t):
	    r'\n+'
	    t.lexer.lineno += len(t.value)

#------------------------------------------------------------------------------#

	# Compute column. 
	#     input is the input text string
	#     token is a token instance
	def find_column(self,input,token):
	    last_cr = input.rfind('\n',0,token.lexpos)
	    column = (token.lexpos - last_cr) 
	    return column

#------------------------------------------------------------------------------#
	# Error handling rule
	def t_error(self,t):
	    # print("Error: Caracter inesperado \""+t.value[0]+"\" en la fila\
	    # "+str(t.lineno)+"\, columna "+str(self.find_column(self.data,t)) )

	    ErrorEncontrado = token(None,t.value[0],\
	    	t.lineno,self.find_column(self.data,t))

	    self.Errores+=[ErrorEncontrado] 
	    t.lexer.skip(1)
	
#------------------------------------------------------------------------------#

	# Build the lexer
	def build(self,**kwargs):
	    self.lexer = lex.lex(module=self, **kwargs)

#------------------------------------------------------------------------------#

	def tokenizar(self):
	    self.lexer.input(self.data)
	    while True:
	        tok = self.lexer.token()
	        if not tok: 
	            break
	        #print(tok.type, tok.value, tok.lineno,self.find_column(self.data,tok),end=" ")
	        #print(tok.type, tok.value, tok.lineno,self.find_column(self.data,tok))
	        if ( tok.type in {"TkNum","TkIdent","TkCaracter"} ):
	        	NodoToken = token(tok.type,tok.value,tok.lineno,\
	        		self.find_column(self.data,tok))

	        else:
	        	NodoToken = token(tok.type,None,tok.lineno,\
	        		self.find_column(self.data,tok))
	        self.Tokens+=[NodoToken]    


