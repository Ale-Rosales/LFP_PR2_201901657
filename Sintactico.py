from pickletools import read_uint1
from re import X
from prettytable import PrettyTable
from Gestor import *

class Sintactico:

    def __init__(self, tokens : list, gestor) -> None:
        self.errores = []
        self.columna = 0
        self.tokens = tokens
        self.gestor = gestor

    def agregarError(self, esperado, obtenido, columna):
        self.errores.append("Error Sintactico: se obtuvo {} en la columna {}, se esperaba {}".format(obtenido, columna, esperado)) 

    def popToken(self):
        try:
            return self.tokens.pop(0)
        except:
            return None

    def viewToken(self):
        try:
            return self.tokens[0]
        except:
            return None

    def AnalizarS(self):
        self.S()

    def S(self):
        self.INICIO()

    def INICIO(self):
        temporal = self.viewToken()
        if temporal is None:
            self.agregarError("pr_RESULTADO | pr_JORNADA | pr_GOLES | pr_TABLA | pr_PARTIDOS | pr_TOP | pr_ADIOS", "EOF",0)
        elif temporal.tipo == 'pr_RESULTADO':
            self.RESULTADO()
        elif temporal.tipo == 'pr_JORNADA':
            self.JORNADA()
        elif temporal.tipo == 'pr_GOLES':
            self.GOLES()
        elif temporal.tipo == 'pr_TABLA':
            self.TABLA()
        elif temporal.tipo == 'pr_PARTIDOS':
            self.PARTIDOS()
        elif temporal.tipo == 'pr_TOP':
            self.TOP()
        elif temporal.tipo == 'pr_ADIOS':
            self.ADIOS()
    
    def RESULTADO(self):
        equipo1 = ""
        equipo2 = ""
        año1 = ""
        guion = ""
        año2 = ""
        fecha = ""
        token = self.popToken()
        if token.tipo == "pr_RESULTADO":
            token = self.popToken()
            if token is None:
                self.agregarError("Cadena","EOF",0)
                return
            elif token.tipo == "Cadena":
                equipo1 = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("pr_VS","EOF",0)
                    return
                elif token.tipo == "pr_VS":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("Cadena","EOF",0)
                        return
                    elif token.tipo == "Cadena":
                        equipo2 = token.lexema
                        token = self.popToken()
                        if token is None:
                            self.agregarError("pr_TEMPORADA","EOF",0)
                            return
                        elif token.tipo == "pr_TEMPORADA":
                            token = self.popToken()
                            if token is None:
                                self.agregarError("Menor que","EOF",0)
                                return
                            elif token.tipo == "Menor que":
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("Entero","EOF",0)
                                    return
                                elif token.tipo == "Entero":
                                    año1 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("Guion","EOF",0)
                                        return
                                    elif token.tipo == "Guion":
                                        guion = token.lexema
                                        token = self.popToken()
                                        if token is None:
                                            self.agregarError("Entero","EOF",0)
                                            return
                                        elif token.tipo == "Entero":
                                            año2 = token.lexema
                                            token = self.popToken()
                                            if token is None:
                                                self.agregarError("Mayor que","EOF",0)
                                                return
                                            elif token.tipo == "Mayor que":
                                                fecha = str(año1)+str(guion)+str(año2)
                                                self.gestor.opResultado(equipo1,equipo2,fecha)
                                            else:
                                                self.agregarError("Mayor que",token.tipo,0)
                                        else:
                                            self.agregarError("Entero",token.tipo,0)
                                    else:
                                        self.agregarError("Guion",token.tipo,0)
                                else:
                                    self.agregarError("Entero",token.tipo,0)
                            else:
                                self.agregarError("Menor que",token.tipo,0)
                        else:
                            self.agregarError("pr_TEMPORADA",token.tipo,0)
                    else:
                        self.agregarError("Cadena",token.tipo,0)
                else:
                    self.agregarError("pr_VS",token.tipo,0)
            else:
                self.agregarError("Cadena",token.tipo,0)
        else:
            self.agregarError("pr_RESULTADO","EOF",0)


    def JORNADA(self):
        pass

    def GOLES(self):
        pass 

    def TABLA(self):
        pass

    def PARTIDOS(self):
        pass

    def TOP(self):
        pass

    def ADIOS(self):
        token = self.popToken()
        if token.tipo == 'pr_ADIOS':
            self.gestor.opAdios()
        else:
            self.agregarError('pr_ADIOS',token.tipo,token.columna)
            
    def ErroresS(self):
        x = PrettyTable()
        x.field_names = ["Descripcion"]
        for error_ in self.errores:
            x.add_row([error_])
        print(x)