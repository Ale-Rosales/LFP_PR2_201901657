from errno import EROFS
from sqlite3 import enable_shared_cache
from pyparsing import col
from soupsieve import select
from Token import Token
from Error import Error
from prettytable import PrettyTable

class Lexico:

    def __init__(self) -> None:
        self.listaTokens = []
        self.listaErrores = []
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
            if self.buffer in ['RESULTADO','VS','TEMPORADA','JORNADA','GOLES','LOCAL','VISITANTE','TOTAL','TABLA','PARTIDOS','TOP','SUPERIOR','INFERIOR','ADIOS']:
                self.addToken(self.buffer, self.linea, self.columna, 'pr_'+self.buffer)
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