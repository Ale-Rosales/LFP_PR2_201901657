from distutils.filelist import findall
from errno import EROFS
from sqlite3 import enable_shared_cache
from pyparsing import col
from soupsieve import select
from Token import Token
from Error import Error
from prettytable import PrettyTable
import re

class Lexico:

    def __init__(self) -> None:
        self.listaTokens = []
        self.listaErrores = []
        self.tokensR = []
        self.erroresR = []
        self.linea = 1
        self.columna = 0
        self.buffer = ''
        self.estado = 0
        self.simbolo = ''
        self.i = 0
    
    def addToken(self, caracter, linea, columna, token):
        self.listaTokens.append(Token(caracter,linea, columna, token))
        self.buffer = ''

    def addError(self, caracter, linea, columna):
        self.listaErrores.append(Error('Lexema '+caracter+' no reconocido', linea, columna))
        self.buffer = ''

    def S0(self, caracter :str):
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        elif caracter == '\"':
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        elif caracter == '<':
            self.estado = 5
            self.buffer += caracter
            self.columna += 1
            self.simbolo = 'Menor que'
        elif caracter == '-':
            self.estado = 5
            self.buffer += caracter
            self.columna += 1
            self.simbolo = 'Guion'
        elif caracter == '_':
            self.estado = 5
            self.buffer += caracter
            self.simbolo = "Guion Bajo"
        elif caracter == '>':
            self.estado = 5
            self.buffer += caracter
            self.columna += 1
            self.simbolo = 'Mayor que'
        elif caracter == '\n':
            self.linea += 1
            self.columna = 0
        elif caracter in ['\t',' ']:
            self.columna += 1
        elif caracter == '$':
            pass
        else:
            self.addError(caracter, self.linea, self.columna)
            self.columna += 1
            self.estado = 0
    
    def S1(self,caracter : str):
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.columna += 1
        else:
            if self.buffer in ['RESULTADO','VS','TEMPORADA','JORNADA','GOLES','LOCAL','VISITANTE','TOTAL','TABLA','PARTIDOS','TOP','SUPERIOR','INFERIOR','ADIOS','f','ji','jf','n']:
                self.addToken(self.buffer, self.linea, self.columna, 'pr_'+self.buffer)
                self.estado = 0
                self.i -= 1
            elif re.findall('\w',self.buffer):
                self.addToken(self.buffer, self.linea, self.columna, "String")
                self.estado = 0
                self.i -= 1
            else:
                self.addError(self.buffer, self.linea, self.columna)
                self.columna += 1
                self.estado = 0
                self.i -=1
    
    def S2(self, caracter : str):
        if caracter == '"':
            self.estado = 3
            self.buffer += caracter
            self.columna += 1
        else:
            self.buffer += caracter
            self.columna += 1

    def S3(self, caracter : str):
        self.addToken(self.buffer, self.linea, self.columna, 'Cadena')
        self.estado = 0
        self.i -= 1

    def S4(self, caracter : str):
        if caracter.isdigit():
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        else:
            self.addToken(self.buffer, self.linea, self.columna, 'Entero')
            self.estado = 0
            self.i -= 1

    def S5(self,caracter : str):
        self.addToken(self.buffer, self.linea, self.columna, self.simbolo)
        self.estado = 0
        self.i -= 1

    def Analizar(self, cadena):
        cadena = cadena + '$'
        self.listaErrores = []
        self.listaTokens = []
        self.i = 0
        while self.i < len(cadena):
            if self.estado == 0:
                self.S0(cadena[self.i])
            elif self.estado == 1:
                self.S1(cadena[self.i])
            elif self.estado == 2:
                self.S2(cadena[self.i])
            elif self.estado == 3:
                self.S3(cadena[self.i])
            elif self.estado == 4:
                self.S4(cadena[self.i])
            elif self.estado == 5:
                self.S5(cadena[self.i])
            
            self.i += 1


    def printTokens(self):
        x = PrettyTable()
        x.field_names = ["Lexema","Linea","Columna","Tipo"]
        for token in self.listaTokens:
            x.add_row([token.lexema, token.linea, token.columna, token.tipo])
        print(x)

    def printErrores(self):
        x = PrettyTable()
        x.field_names = ["Descripcion","Linea","Columna"]
        for error in self.listaErrores:
            x.add_row([error.descripcion, error.linea, error.columna])
        print(x) 
    

    #------------------------------------------------------------------AQUI EL QUE SI VA A GUARDAR LOS TOKENS------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def addTokenR(self, caracter, linea, columna, token):
        self.tokensR.append(Token(caracter,linea, columna, token))
        self.buffer = ''
    
    def addErrorR(self, caracter, linea, columna):
        self.erroresR.append(Error('Lexema '+caracter+' no reconocido', linea, columna))
        self.buffer = ''

    def S0R(self, caracter :str):
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        elif caracter == '\"':
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        elif caracter == '<':
            self.estado = 5
            self.buffer += caracter
            self.columna += 1
            self.simbolo = 'Menor que'
        elif caracter == '-':
            self.estado = 5
            self.buffer += caracter
            self.columna += 1
            self.simbolo = 'Guion'
        elif caracter == '_':
            self.estado = 5
            self.buffer += caracter
            self.simbolo = "Guion Bajo"
        elif caracter == '>':
            self.estado = 5
            self.buffer += caracter
            self.columna += 1
            self.simbolo = 'Mayor que'
        elif caracter == '\n':
            self.linea += 1
            self.columna = 0
        elif caracter in ['\t',' ']:
            self.columna += 1
        elif caracter == '$':
            pass
        else:
            self.addErrorR(caracter, self.linea, self.columna)
            self.columna += 1
            self.estado = 0
    
    def S1R(self,caracter : str):
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.columna += 1
        else:
            if self.buffer in ['RESULTADO','VS','TEMPORADA','JORNADA','GOLES','LOCAL','VISITANTE','TOTAL','TABLA','PARTIDOS','TOP','SUPERIOR','INFERIOR','ADIOS','f','ji','jf','n']:
                self.addTokenR(self.buffer, self.linea, self.columna, 'pr_'+self.buffer)
                self.estado = 0
                self.i -= 1
            elif re.findall('\w',self.buffer):
                self.addTokenR(self.buffer, self.linea, self.columna, "String")
                self.estado = 0
                self.i -= 1
            else:
                self.addErrorR(self.buffer, self.linea, self.columna)
                self.columna += 1
                self.estado = 0
                self.i -=1
    
    def S2R(self, caracter : str):
        if caracter == '"':
            self.estado = 3
            self.buffer += caracter
            self.columna += 1
        else:
            self.buffer += caracter
            self.columna += 1

    def S3R(self, caracter : str):
        self.addTokenR(self.buffer, self.linea, self.columna, 'Cadena')
        self.estado = 0
        self.i -= 1

    def S4R(self, caracter : str):
        if caracter.isdigit():
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        else:
            self.addTokenR(self.buffer, self.linea, self.columna, 'Entero')
            self.estado = 0
            self.i -= 1

    def S5R(self,caracter : str):
        self.addTokenR(self.buffer, self.linea, self.columna, self.simbolo)
        self.estado = 0
        self.i -= 1

    def AnalizarR(self, cadena):
        cadena = cadena + '$'
        #self.tokensR = []
        #self.erroresR = []
        self.i = 0
        while self.i < len(cadena):
            if self.estado == 0:
                self.S0R(cadena[self.i])
            elif self.estado == 1:
                self.S1R(cadena[self.i])
            elif self.estado == 2:
                self.S2R(cadena[self.i])
            elif self.estado == 3:
                self.S3R(cadena[self.i])
            elif self.estado == 4:
                self.S4R(cadena[self.i])
            elif self.estado == 5:
                self.S5R(cadena[self.i])
            
            self.i += 1
    
    def printTokensR(self):
        x = PrettyTable()
        x.field_names = ["LexemaL","LineaL","ColumnaL","TipoL"]
        for token in self.tokensR:
            x.add_row([token.lexema, token.linea, token.columna, token.tipo])
        print(x)
    
    def printErroresR(self):
        x = PrettyTable()
        x.field_names = ["DescripcionL","LineaL","ColumnaL"]
        for error in self.erroresR:
            x.add_row([error.descripcion, error.linea, error.columna])
        print(x)

    def clearTokensR(self):
        self.tokensR.clear()

    def clearErroresR(self):
        self.erroresR.clear()