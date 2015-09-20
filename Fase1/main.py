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

'''

  Cosas que faltan:

    * Crear clases (listo)
    * Ignorar comentarios (listo)
    * Ignorar comillas simples (listo)
    * Buen manejo de errores
    * Imprimir de forma lineal (listo)

'''

#------------------------------------------------------------------------------#
#							                  IMPORTE DE MODULOS				          				   #
#------------------------------------------------------------------------------#
import sys
import os
from Lista import * 
import ply.lex as lex

#------------------------------------------------------------------------------#
#						                 FUNCIONES Y PROCEDIMIENTOS				        			   #
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def LeerArchivoEntrada(): 
  '''
    Descripción de la función: Lee el archivo de entrada, crea los 
    paquetes y los almacena en la cola de prioridades.
    Variables de entrada: Ninguna
    Variables de salida: Ninguna
  '''

  # Verificación de la correctitud de los argumentos dados.
  try:
  # Se verifica que se introduzcan los argumentos necesarios.
    assert(len(sys.argv) == 2)
    NombreArchivoEntrada = sys.argv[1]
    # Se verifica que el archivo de entrada esté en el directorio
    # correspondiente.
    assert(os.path.isfile(NombreArchivoEntrada))
  except:
    print("Error: Los argumentos dados no son validos")
    print("El programa se cerrará.")
    sys.exit()
  # Lectura del archivo de entrada.
  with open(NombreArchivoEntrada,'r') as Archivo:
    data = Archivo.read()
    Archivo.close

  return data

#------------------------------------------------------------------------------#
#           INICIO DEL PROGRAMA PRINCIPAL                #
#------------------------------------------------------------------------------#

# List of token names.   This is always required
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
    'char'             : 'TkCaracter'
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
   'TkComment',
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

# A regular rule with some action code
def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_TkIdent(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'TkIdent')
  return t

def t_TkComment(t):
    r'\$-[^-]*-\$'
    pass
    # No return value. Token discarded

def t_TkComillas(t):
    r'\'-[^-]*-\''
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
      last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0],t.lineno,t.lexpos)
    t.lexer.skip(1)
    #exit(0)

# Build the lexer
lexer = lex.lex()
ListaTokens = lista()

################################################################################

datos = LeerArchivoEntrada()
# Give the lexer some input
lexer.input(datos)

# Tokenize
#while True:
 #   tok = lexer.token()
  #  if not tok: 
   #     break      # No more input
    #print(tok)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok.type, tok.value, tok.lineno,find_column(datos,tok),end=" ")
    Nodo = token(tok.type,tok.value,tok.lineno,find_column(datos,tok))
    ListaTokens.agregar(Nodo)
 
ListaTokens.imprimir()  

#------------------------------------------------------------------------------#
#						             FIN DEL PROGRAMA PRINCIPAL 				             		   #
#------------------------------------------------------------------------------#
