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
#							                  IMPORTE DE MODULOS				          				   #
#------------------------------------------------------------------------------#
import sys
import os
from Tokens import *
from Lexer import * 
import ply.lex as lex

#------------------------------------------------------------------------------#
#						                 FUNCIONES Y PROCEDIMIENTOS				        			   #
#------------------------------------------------------------------------------#
def LeerArchivoEntrada(): 
  '''
    Descripción de la función: Lee el archivo de entrada.

    * Variables de entrada: Ninguna
    * Variables de salida: data// Almacena toda la informacion que se 
                                  encuentra en el archivo de entrada.

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

def ImprimirErrores(ArregloErrores):

  '''
    Descripción de la función: Imprime la lista de tokens que almacena los errores
        lexicograficos.

    * Variables de entrada: ArregloErrores // Lista de tokens
    * Variables de salida: Ninguna.

  '''

  for i in range(len(ArregloErrores)):

    print("Error: Caracter inesperado \""+ArregloErrores[i].elem+"\" en la fila "\
      +str(ArregloErrores[i].fila)+", columna "+str(ArregloErrores[i].columna) )

#------------------------------------------------------------------------------#

def ImprimirTokens(ArregloTokens):

  '''
    Descripción de la función: Imprime la lista de tokens que almacena
      los tokens realizados a partir del archivo de entrada.

    * Variables de entrada: ArregloTokens // Lista de tokens
    * Variables de salida: Ninguna.
    
  '''

  for i in range(len(ArregloTokens)):

    if ( (i%4==0 and i!=0) or (i%4!=0 and i==len(ArregloTokens)-1) ):
      FinLinea ='\n'
    else :
      FinLinea=",  "


    #print(tok.type, tok.value, tok.lineno,self.find_column(self.data,tok),end=" ")
    if (ArregloTokens[i].tipo in {"TkNum","TkCaracter"} ):

      print(ArregloTokens[i].tipo+"("+str(ArregloTokens[i].elem)+")",\
        ArregloTokens[i].fila,ArregloTokens[i].columna,end=FinLinea)

    elif (ArregloTokens[i].tipo=="TkIdent"):

      print(ArregloTokens[i].tipo+"(\""+ArregloTokens[i].elem+"\")",\
        ArregloTokens[i].fila,ArregloTokens[i].columna,end=FinLinea)

    else:
      print(ArregloTokens[i].tipo,ArregloTokens[i].fila,\
        ArregloTokens[i].columna,end=FinLinea)

#------------------------------------------------------------------------------#
#                          INICIO DEL PROGRAMA PRINCIPAL                       #
#------------------------------------------------------------------------------#

datos = LeerArchivoEntrada()  # Se lee el archivo de entrada
MiLexer=Lexer(datos)          # Se crea el Lexer
MiLexer.build()               # Se construye el Lexer
MiLexer.tokenizar()           # Se arman los tokens

# Se verifica si existen caracteres no permitidos en el codigo
if (len(MiLexer.Errores)!= 0 ) :
  # Se imprimen los errores lexicograficos
  ImprimirErrores(MiLexer.Errores)

else:
  # Se imprimen los tokens
  ImprimirTokens(MiLexer.Tokens)

#------------------------------------------------------------------------------#
#						             FIN DEL PROGRAMA PRINCIPAL 				             		   #
#------------------------------------------------------------------------------#
