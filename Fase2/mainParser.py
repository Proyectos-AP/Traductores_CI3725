import sys
import os
from Arbol import *
from Tokens import *
from Lexer import * 
from parserBOT import *
import ply.lex as lex 
import ply.yacc as yacc
#from prueba import tokens


# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

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

    # Se fija el fin de linea
    if ( i==len(ArregloTokens)-1 ):
      FinLinea ='\n'
    elif ( i%4==0 and i!=0 ):
      FinLinea =", \n"  
    else :
      FinLinea=",  "

    # Se imprimen los tokens
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


datos = LeerArchivoEntrada()
MiLexer=Lexer(datos)          # Se crea el Lexer
MiLexer.build()               # Se construye el Lexer
MiLexer.tokenizar() 
tokens = MiLexer.tokens 

if (len(MiLexer.Errores)!= 0 ) :
  # Se imprimen los errores lexicograficos
  ImprimirErrores(MiLexer.Errores)

#parser = yacc.yacc(errorlog=yacc.NullLogger())
parser = yacc.yacc()
Raiz = parser.parse(datos)
Raiz.imprimirAST(0)

# print(Raiz.op)
# print(Raiz.left.op)
# print(Raiz.left.left.value)
# print(Raiz.left.right.value)
# print(Raiz.right.value)
# print(Raiz.right.left.value)

#print(Raiz.type)
#print(Raiz.identificador)
#Raiz.expresiones.imprimirExpresionesBinarias()

# print(Raiz.type)
# print(Raiz.Instrucciones.type)
# print(Raiz.Instrucciones.expresionesCondicional.op)
# print(Raiz.Instrucciones.expresionesCondicional.left.value)
# print(Raiz.Instrucciones.expresionesCondicional.right.value)
# print(Raiz.Instrucciones.exito.type)
# print(Raiz.Instrucciones.exito.Identificadores.value)
# print(Raiz.Instrucciones.fracaso.type)
# print(Raiz.Instrucciones.fracaso.Identificadores.value)
# # print(Raiz.Instrucciones.exito.sig.type)
# # print(Raiz.Instrucciones.exito.sig.Identificadores.value)
# print(Raiz.Instrucciones.sig.type)
# print(Raiz.Instrucciones.sig.Identificadores.value)


# print(Raiz.type)
# print(Raiz.tipoRobot)
# print(Raiz.identificadores.value)
# print(Raiz.listaComportamiento.condicion.type)
# print(Raiz.listaComportamiento.instrucciones.type)
# Raiz.listaComportamiento.instrucciones.expresiones.imprimirExpresionesBinarias()
# print(Raiz.listaComportamiento.instrucciones.sig.type)

# print(Raiz.sig.type)
# print(Raiz.sig.tipoRobot)
# print(Raiz.sig.identificadores.value)
# print(Raiz.sig.listaComportamiento.condicion.type)
# print(Raiz.sig.listaComportamiento.instrucciones.type)
# Raiz.sig.listaComportamiento.instrucciones.expresiones.imprimirExpresionesBinarias()
# print(Raiz.sig.listaComportamiento.instrucciones.sig.type)



# print(Raiz.condicion.type)
# print(Raiz.instrucciones.type)
# print(Raiz.instrucciones.sig.type)

# print(Raiz.sig.type)
# print(Raiz.sig.condicion.type)
# print(Raiz.sig.instrucciones.type)
# Raiz.sig.instrucciones.expresiones.imprimirExpresionesBinarias()
# print(Raiz.sig.instrucciones.sig.type)



# print(Raiz.sig.type)
# print(Raiz.Instrucciones.expresiones.op)
# print(Raiz.Instrucciones.expresiones.left.value)
# print(Raiz.Instrucciones.expresiones.right.value)
# print(Raiz.Instrucciones.InstruccionesWhile.type)
# print(Raiz.Instrucciones.InstruccionesWhile.Identificadores.value)
# print(Raiz.Instrucciones.InstruccionesWhile.sig.type)
# print(Raiz.Instrucciones.InstruccionesWhile.sig.Identificadores.value)
# print(Raiz.sig.sig.type)
# print(Raiz.Instrucciones.sig.Identificadores.value)


# print(Raiz.Instrucciones.Identificadores.value)
# print(Raiz.Instrucciones.Identificadores.sig.value)
# print(Raiz.Instrucciones.Identificadores.sig.sig.value)
# print(Raiz.Instrucciones.sig.type)
# print(Raiz.Instrucciones.sig.Identificadores.value)
# print(Raiz.Instrucciones.sig.sig.type)
# print(Raiz.Instrucciones.sig.sig.Identificadores.value)

# print(Raiz.Identificadores.value)
# print(Raiz.Identificadores.sig.value)
# print(Raiz.Identificadores.sig.sig.value)

# print(Raiz.value)
# print(Raiz.sig.value)
# print(Raiz.sig.sig.value)
#print(Raiz.hijos[1].value)

# print(Raiz.hijos[0].value)
# print(Raiz.hijos[1].value)
#print(Raiz.hijos[1].hijos[1].value)

# print(Raiz.op)
# print(Raiz.left.value)
# print(Raiz.right.op)
# print(Raiz.right.left.value)
# print(Raiz.right.right.value)

# print(Raiz.op)
# print(Raiz.value.op)
# print(Raiz.value.left.op)
# print(Raiz.value.left.left.value)
# print(Raiz.value.left.right.value)
# print(Raiz.value.right.value)