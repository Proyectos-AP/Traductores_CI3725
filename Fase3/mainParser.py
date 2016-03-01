'''
*
* Universidad Simon Bolivar
* Departamento de Computacion y Tecnologia de la Informacion
* Traductores e Interpretadores - CI3725 (Laboratorio)
*
* Archivo: mainParser.py
*
* Nombres:
*     Alejandra Cordero / Carnet: 12-10645
*     Pablo Maldonado   / Carnet: 12-10561
*
* Descripcion: Codigo principal del parser.
*
*
* Ultima modificacion: 12/02/2016
*
'''

#------------------------------------------------------------------------------#
#                            IMPORTE DE MODULOS                                #
#------------------------------------------------------------------------------#

import sys
import os
from Arbol import *
from Tokens import *
from Lexer import * 
from parserBOT import *
from TablaSimbolos import *
import ply.lex as lex 
import ply.yacc as yacc

#------------------------------------------------------------------------------#
#                          DEFINICION DE FUNCIONES                             #
#------------------------------------------------------------------------------#

def LeerArchivoEntrada(): 
    '''
    * Descripción de la función: Lee el archivo de entrada.
    * Variables de entrada : Ninguna
    * Variables de salida : 
        - data : Almacena toda la informacion que se 
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
        if not data:
            print("Aviso: El archivo que desea utilizar esta vacio.",end=" ")
            print("El programa se cerrara.")
            Archivo.close
            sys.exit()
        Archivo.close
    return data

  #------------------------------------------------------------------------------#

def ImprimirErrores(ArregloErrores):
    '''
    * Descripción de la función: Imprime la lista de tokens que almacena los 
    errores lexicograficos.
    * Variables de entrada: 
        - ArregloErrores : Lista de tokens.
    * Variables de salida: Ninguna.
    '''
    for i in range(len(ArregloErrores)):
        print("Error: Caracter inesperado \"" + ArregloErrores[i].elem + "\" en la fila "\
            + str(ArregloErrores[i].fila) + ", columna " + str(ArregloErrores[i].columna) )

#------------------------------------------------------------------------------#

def ImprimirTokens(ArregloTokens):
    '''
    * Descripción de la función: Imprime la lista de tokens que almacena los 
    tokens realizados a partir del archivo de entrada.
    * Variables de entrada: 
        - ArregloTokens : Lista de tokens
    * Variables de salida: Ninguna.
    '''
    for i in range(len(ArregloTokens)):
        # Se fija el fin de linea
        if ( i == len(ArregloTokens) - 1 ):
            FinLinea ='\n'
        elif ( i%4 == 0 and i != 0 ):
            FinLinea =", \n"  
        else:
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
#                        INICIO DEL PROGRAMA PRINCIPAL                         #
#------------------------------------------------------------------------------#

# Se lee el archivo de entrada:
datos = LeerArchivoEntrada()

# Analisis Lexico:
MiLexer = Lexer(datos)          # Se crea el Lexer
MiLexer.build()                 # Se construye el Lexer
MiLexer.tokenizar()              

if ( len(MiLexer.Errores) != 0 ):
  ImprimirErrores(MiLexer.Errores)

else:
  # Analisis de Sintaxis:
  tokens = MiLexer.tokens 
  #parser = yacc.yacc(errorlog=yacc.NullLogger())
  parser = yacc.yacc()
  Raiz = parser.parse(datos,tracking=True)
  Raiz.imprimirAST(0)
  #print(Raiz.tablaSimbolos.padre.tabla)

#------------------------------------------------------------------------------#
#                        FIN DEL PROGRAMA PRINCIPAL                            #
#------------------------------------------------------------------------------#
