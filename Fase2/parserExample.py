import sys
import os

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
reserved = {
    'create'           : 'TkCreate',
    'bot'              : 'TkBot' ,
    'on'               : 'TkOn',
    'activation'       : 'TkActivation' ,
    'deactivation'     : 'TkDeActivation',
    'store'            : 'TkStore' ,
    'end'              : 'TkEnd'  ,
    'execute'          : 'TkExecute' ,
    'activate'         : 'TkActivate',
    'deactivate'       : 'TkDeactivate' ,
    'send'             : 'TkSend' ,   
    'advance'          : 'TkAdvance' ,
    'recieve'          : 'TkRecieve',
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
    'TkErrorNum'
] + list(reserved.values())

# Expresiones regulares para tokens simples.
t_TkComa         = r','
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

def t_TkErrorNum(t):

    r'[\d_]+[a-zA-Z_]+'
    t.value = t.value[0]
    return t
    
#------------------------------------------------------------------------------#

    # Descripción de la función: Regla para tokens correspondientes
    # a numeros.
def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

#------------------------------------------------------------------------------#

    # Descripción de la función:    Regla para conjuntos de caracteres. 
    # Si el caracter es igual a algun caracter reservado entonces t.type 
    # sera igual al del caracter reservado,de no ser igual a ningun 
    # caracter reservado entonces t.type sera igual a TkIdent.
def t_TkIdent(t):

    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'TkIdent')
    return t

#------------------------------------------------------------------------------#

# Descripción de la función:Regla para contar los numeros de linea.
def t_newline(t):

    r'\n+'
    t.lexer.lineno += len(t.value)

#------------------------------------------------------------------------------#

    # Descripción de la función: Reglas para los comentarios.
    # Los tokens obtenidos por esta expresion regular seran omitidos.
def t_TkComment(t):
    r'(\$-(.|\n)*?-\$)|(\$\$.*)'
    t.lexer.lineno += t.value.count('\n')
    pass

#------------------------------------------------------------------------------#

    # Descripción de la función: Reglas para caracteres. Este token solo 
    # toma caracteres encerrados entre comillas simples.
def t_TkCaracter(t):

    r'\'.\''
    return t

#------------------------------------------------------------------------------#
    # Descripción de la función: Funcion para localizar el numero de 
    # columna de una palabra.
# def NumeroColumna(input,token):

#     last_cr = input.rfind('\n',0,token.lexpos)
#     columna = (token.lexpos - last_cr) 
#     return columna

#------------------------------------------------------------------------------#

    # Descripción de la función: Funcion para el manejo de errores .
def t_error(t):

    ErrorEncontrado = token(None,t.value[0],\
        t.lineno,self.NumeroColumna(self.data,t))
    t.lexer.skip(1)

#-------------------------------------------------------------------------------#  
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','TkSuma','TkResta'),
    ('left','TkMult','TkDiv'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_inicioPrograma(t):
    ''' inicio : TkCreate LISTA_DECLARACIONES TkExecute INSTRUCCIONES_CONTROLADOR TkEnd
                | TkExecute INSTRUCCIONES_CONTROLADOR TkEnd '''

# def p_IniciolistaDeclaraciones(t):
#     ''' INICIO_LISTA_DECLARACIONES :  LISTA_DECLARACIONES LISTA_COMPORTAMIENTOS'''

def p_listaDeclaraciones(t):
    ''' LISTA_DECLARACIONES : TkInt TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd LISTA_DECLARACIONES
                            | TkBool TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd LISTA_DECLARACIONES
                            | TkChar TkBot LISTA_IDENT LISTA_COMPORTAMIENTOS TkEnd LISTA_DECLARACIONES 
                            |'''

def  p_listaIdent(t):
    ''' LISTA_IDENT : LISTA_IDENT TkComa LISTA_IDENT
                    | TkIdent '''
    
# def p_IniciolistaComportamientos(t):
#     ''' INICIO_LISTA_COMPORTAMIENTOS : TkOn CONDICION TkDosPuntos INICIO_INSTRUCCIONES_ROBOT 
#                               |'''

def p_listaComportamientos(t):
    ''' LISTA_COMPORTAMIENTOS : TkOn CONDICION TkDosPuntos INSTRUCCIONES_ROBOT TkEnd LISTA_COMPORTAMIENTOS
                              |'''

def p_condicion(t):
    ''' CONDICION : TkDeActivation
                  | TkActivation
                  | expression
                  | TkDefault''' 

def p_instruccionRobot(t):
    ''' INSTRUCCIONES_ROBOT : INSTRUCCIONES_ROBOT INSTRUCCIONES_ROBOT
                            | TkStore expression TkPunto 
                            | TkCollect GUARDAR_VARIABLE TkPunto 
                            | TkRight EXPRESION_OPCIONAL TkPunto 
                            | TkLeft EXPRESION_OPCIONAL TkPunto 
                            | TkUp EXPRESION_OPCIONAL TkPunto 
                            | TkDown EXPRESION_OPCIONAL TkPunto 
                            | TkRead GUARDAR_VARIABLE TkPunto 
                            | TkSend TkPunto  '''

def p_expresionOpcional(t):
    ''' EXPRESION_OPCIONAL : expression
                           |'''

def p_guardarVariable(t):
    ''' GUARDAR_VARIABLE : TkAs TkIdent
                        |'''

def p_instruccionesControlador(t):
    '''  INSTRUCCIONES_CONTROLADOR : expression
                                    |'''

# def p_expresionExecute(t):
#     ''' expressionE : TkExecute expression '''

def p_statement_assign(t):
    'statement : TkIdent TkIgual expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    '''statement : expression'''

    #print(t[1])

def p_expression_binop(t):
    '''expression : expression TkSuma expression
                  | expression TkResta expression
                  | expression TkMult expression
                  | expression TkDiv expression
                  | expression TkConjuncion expression
                  | expression TkDisyuncion expression '''
    if t[2] == '+'  : 
        #t[0] = t[1] + t[3]
        t[0]=str(t[1])+" + "+str(t[3])
    elif t[2] == '-': 
        #t[0] = t[1] - t[3]
        t[0] = str(t[1])+" - "+str(t[3])
    elif t[2] == '*': 
        #t[0] = t[1] * t[3]
        t[0] = str(t[1])+" * "+str(t[3])
    elif t[2] == '/': 
        #t[0] = t[1] / t[3]
        t[0] = str(t[1])+" / "+str(t[3])
    elif t[2] == '/\\' : 
        print(str(t[1])+"/\\"+str(t[3]) )
    elif t[2] == '\\/': 
        print(str(t[1])+"\\/"+str(t[3]) )

# def p_expression_bool(t):
#     '''expressionBool : expressionBool TkConjuncion expressionBool
#                       | expressionBool TkDisyuncion expressionBool'''
#     if t[2] == '/\\'  : print(str(t[1])+"/\\"+str(t[3]) )
#     elif t[2] == '\\/': print(str(t[1])+"\\/"+str(t[3]) )

def p_expression_True(t):
    '''expressionBool : TkTrue 
                        | TkFalse'''
    t[0] = t[2]

def p_expression_uminus(t):
    'expression : TkResta expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : TkParAbre expression TkParCierra'
    t[0] = t[2]

def p_expression_number(t):
    'expression : TkNum'
    t[0] = t[1]

def p_expression_name(t):
    'expression : TkIdent'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    #print("Syntax error at ")


import ply.yacc as yacc
parser = yacc.yacc()

datos = LeerArchivoEntrada()
parser.parse(datos)
